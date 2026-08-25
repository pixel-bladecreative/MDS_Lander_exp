#!/usr/bin/env python3
"""pack_artifact.py — fold site/index.html into one self-contained page.

An Artifact is served under a strict CSP (no external hosts except Google
Fonts) and capped at 16MB rendered, so the deployable build's ~600 streamed
frames cannot go across as-is. This packer produces a viewing copy:

  * frames decimated and re-encoded to fit the cap, inlined as data URIs
  * product photography inlined as data URIs
  * the document skeleton stripped, since the Artifact host supplies it

The repo keeps the full-rate build for real deployment. This is the preview,
and the header on the packed page says so rather than passing itself off as
the shipped asset.
"""
import base64
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.expanduser("~/bin/ffmpeg")
SRC = os.path.join(ROOT, "site", "index.html")
FRAMES = os.path.join(ROOT, "site", "frames")
OUT = os.path.join(ROOT, "artifact", "retail-edge.html")

STRIDE = int(os.environ.get("STRIDE", "2"))      # 2 -> 12fps
WIDTH = int(os.environ.get("ART_W", "900"))
Q = os.environ.get("ART_Q", "7")
BUDGET = 15_000_000                              # leave headroom under the 16MB cap


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def main():
    html = open(SRC).read()
    tmp = os.path.join("/tmp", "re_art_frames")
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))

    src_frames = sorted(f for f in os.listdir(FRAMES) if f.startswith("f_"))
    picked = src_frames[::STRIDE]
    print(f"{len(src_frames)} frames -> {len(picked)} at stride {STRIDE}, {WIDTH}px q{Q}")

    uris = []
    for i, f in enumerate(picked):
        o = os.path.join(tmp, f"a_{i:04d}.jpg")
        subprocess.run([FFMPEG, "-v", "error", "-y", "-i", os.path.join(FRAMES, f),
                        "-vf", f"scale={WIDTH}:-2", "-q:v", Q, o], check=True)
        uris.append(b64(o, "image/jpeg"))
    payload = sum(len(u) for u in uris)
    print(f"frame payload: {payload/1e6:.1f}MB base64")

    # Inline the photography the content sections use.
    imgs = sorted(set(re.findall(r'assets/img/([^"\')]+)', html)))
    inline = {}
    for name in imgs:
        p = os.path.join(ROOT, "site", "assets", "img", name)
        if not os.path.exists(p):
            print(f"  ! missing {name}")
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        if ext in ("jpg", "jpeg"):
            small = os.path.join(tmp, "img_" + name)
            subprocess.run([FFMPEG, "-v", "error", "-y", "-i", p,
                            "-vf", "scale='min(1200,iw)':-2", "-q:v", "5", small], check=True)
            inline[name] = b64(small, "image/jpeg")
        else:
            inline[name] = b64(p, "image/png")
    img_payload = sum(len(v) for v in inline.values())
    print(f"image payload: {img_payload/1e6:.1f}MB base64")

    total = payload + img_payload + len(html)
    if total > BUDGET:
        sys.exit(f"OVER BUDGET: {total/1e6:.1f}MB > {BUDGET/1e6:.1f}MB — raise STRIDE or lower ART_W")

    for name, uri in inline.items():
        html = html.replace(f"assets/img/{name}", uri)

    # The Artifact host wraps the file in its own doctype/head/body.
    html = re.sub(r"^[\s\S]*?<head>", "", html, count=1)
    html = html.replace("</head>", "", 1)
    html = re.sub(r"<body[^>]*>", "", html, count=1)
    html = html.replace("</body>", "").replace("</html>", "")
    html = re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>', "", html)

    frames_js = "window.EMBEDDED_FRAMES=[" + ",".join(f'"{u}"' for u in uris) + "];"
    html = html.replace("<script>", "<script>" + frames_js, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(html)
    print(f"wrote {OUT}  {os.path.getsize(OUT)/1e6:.1f}MB")


if __name__ == "__main__":
    main()
