#!/usr/bin/env python3
"""continuity_gate.py <frames-dir> [step]

Python port of the skill's continuity-gate.sh (this container has no zsh).
The judging logic is copied deliberately, because the subtlety is the whole
point of the gate:

  A seam gate cannot fail. Chaining sets each clip's start image to the previous
  clip's real last frame, so junctions match BY CONSTRUCTION. What escapes is the
  MIDDLE of a clip, where a generated shot can jump-cut or freeze while every
  junction still scores perfectly.

  Absolute SSIM is also the wrong test. A fast but perfectly smooth dolly changes
  most of the frame and scores low; a hard cut between two similar frames scores
  high. So every pair is judged against its own LOCAL median, never a global
  constant:

    smooth motion -> consistent with neighbours, however low
    hard cut      -> sudden collapse far below the local median
    freeze        -> ~1.0, camera stopped, a dead zone under the playhead

  PASS  no pair below 45% of its local median, and at most 2 frozen pairs.
"""
import os
import re
import subprocess
import sys

FFMPEG = os.path.expanduser("~/bin/ffmpeg")


def ssim(a, b):
    out = subprocess.run([FFMPEG, "-i", a, "-i", b, "-lavfi", "ssim", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"All:([0-9.]+)", out)
    return float(m.group(1)) if m else None


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def main():
    d = sys.argv[1]
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    frames = sorted(f for f in os.listdir(d) if f.startswith("f_") and f.endswith(".jpg"))
    if len(frames) < 4:
        sys.exit(f"no frames in {d}")
    print(f"continuity gate — {d}  ({len(frames)} frames, every {step})")

    picks = frames[::step]
    scores, names = [], []
    for i in range(1, len(picks)):
        s = ssim(os.path.join(d, picks[i - 1]), os.path.join(d, picks[i]))
        if s is not None:
            scores.append(s)
            names.append(f"{picks[i-1]}->{picks[i]}")

    if len(scores) < 3:
        sys.exit("FAIL measured too few pairs to judge")

    cuts, frozen = [], []
    for i, s in enumerate(scores):
        lo, hi = max(0, i - 3), min(len(scores), i + 4)
        lm = median(scores[lo:hi])
        if s < 0.45 * lm:
            cuts.append(f"{names[i]}  {s:.4f} vs local {lm:.4f}")
        if s > 0.995:
            frozen.append(f"{names[i]}  {s:.4f}")

    print(f"  median {median(scores):.4f} over {len(scores)} pairs "
          f"— absolute value is NOT the test; local shape is")
    if cuts:
        print(f"  {len(cuts)} hard cuts (collapse vs local baseline):")
        for c in cuts[:6]:
            print(f"    {c}")
    if frozen:
        print(f"  {len(frozen)} frozen pairs (camera stopped — dead scroll zone):")
        for f in frozen[:6]:
            print(f"    {f}")

    fail = False
    if cuts:
        print(f"  FAIL {len(cuts)} cuts — a sequence of shots, not one move")
        fail = True
    if len(frozen) > 2:
        print(f"  FAIL {len(frozen)} frozen pairs — the scroll will stall here")
        fail = True
    if fail:
        print("\nREJECTED. Do not build on this footage — regenerate it.")
        sys.exit(1)
    print("  PASS — one continuous move")


if __name__ == "__main__":
    main()
