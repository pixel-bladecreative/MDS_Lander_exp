#!/usr/bin/env python3
"""gen_keyframes.py <storyboard.json> <outdir> [only_id ...]

Keyframe chain for the Retail Edge film. Adapted from the skill's kie-chain.py
with one addition it does not have: a keyframe may carry EXTRA references
besides the previous frame.

That matters here because this is a real physical product. Seeding the frames
with a photograph of the actual hardware keeps Seedance rendering the real
Retail Edge unit instead of inventing a barrier that no booth visitor would
recognise. The reference used is the bare Attachment Stand — it carries no
third-party banner artwork, so it anchors geometry without bleeding another
brand's graphics into our frames.

Resumable: anything already on disk is not regenerated. Logs the credit balance
around every call so the spend is measured, not estimated.
"""
import json
import os
import sys
import time
import urllib.request

KEY = os.environ.get("KIE_API_KEY")
if not KEY:
    sys.exit("ERROR: KIE_API_KEY not set")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
HDRS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "User-Agent": UA}
JOBS_CREATE = "https://api.kie.ai/api/v1/jobs/createTask"
JOBS_INFO = "https://api.kie.ai/api/v1/jobs/recordInfo"
CREDIT = "https://api.kie.ai/api/v1/chat/credit"


def req(url, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=HDRS,
                               method="POST" if data else "GET")
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return json.loads(f.read())


def fetch(url, out, timeout=600):
    """Kie's CDN 403s anything without a browser UA."""
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=timeout) as src, open(out, "wb") as f:
        f.write(src.read())


def credits():
    try:
        return req(CREDIT)["data"]
    except Exception:
        return -1


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def gen_still(prompt, refs, aspect, out):
    inp = {"prompt": prompt, "aspect_ratio": aspect,
           "resolution": os.environ.get("KF_RES", "1K"), "output_format": "png"}
    if refs:
        inp["image_urls"] = refs
    d = req(JOBS_CREATE, {"model": "nano-banana-2", "input": inp})
    if d.get("code") != 200:
        raise RuntimeError(f"createTask: {d.get('code')} {d.get('msg')}")
    tid = d["data"]["taskId"]
    # Persist the id the moment it is issued — a lost id after a paid render
    # means paying for that render twice.
    open(f"{out}.task-id", "w").write(tid)
    for _ in range(150):
        time.sleep(4)
        s = req(f"{JOBS_INFO}?taskId={tid}")["data"]
        if s.get("state") == "success":
            url = json.loads(s["resultJson"])["resultUrls"][0]
            fetch(url, out)
            return url
        if s.get("state") == "fail":
            raise RuntimeError(f"still failed: {s.get('failMsg')}")
    raise TimeoutError("still timed out")


def main():
    sb = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    only = set(sys.argv[3:])
    os.makedirs(outdir, exist_ok=True)
    aspect = sb.get("aspect", "16:9")
    style = sb.get("style", "")

    extra = {}
    hw = os.path.join(os.path.dirname(outdir) or ".", "hardware-ref.url")
    if os.path.exists(hw):
        extra["hardware"] = open(hw).read().strip()

    prev = None
    for k in sb["keyframes"]:
        p = os.path.join(outdir, f"{k['id']}.png")
        um = os.path.join(outdir, f"{k['id']}.url")
        if os.path.exists(um):
            prev = open(um).read().strip()
            log(f"{k['id']} cached")
            continue
        if only and k["id"] not in only:
            log(f"{k['id']} skipped (not requested) — chain stops here")
            break
        # Previous keyframe first: it is the dominant reference, so the world
        # (palette, light, materials, scale) is inherited rather than reinvented.
        refs = ([prev] if prev else []) + [extra[r] for r in k.get("refs", [])
                                           if r in extra]
        before = credits()
        log(f"{k['id']} generating  refs={len(refs)}  credits={before}")
        url = gen_still(f"{k['prompt']} {style}".strip(), refs, aspect, p)
        after = credits()
        log(f"{k['id']} done  {os.path.getsize(p)//1024}KB  "
            f"cost={before - after:.0f}  credits={after}")
        open(um, "w").write(url)
        prev = url


if __name__ == "__main__":
    main()
