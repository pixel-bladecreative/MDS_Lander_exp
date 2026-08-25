#!/usr/bin/env python3
"""gen_clips.py <storyboard.json> <outdir> [max_clips]

Sequential both-ends-pinned clip chain on Kie's Seedance 2.5.

Two rules from the skill's playbook that this file exists to enforce:

  1. Every clip is pinned at BOTH ends, so it is forced to LAND on the next
     keyframe instead of drifting somewhere and jump-cutting back.
  2. The START pin is the previous clip's real extracted last frame, NOT the
     previous keyframe. That is what makes the join invisible, and it is why
     this loop is strictly sequential — clip N must finish before N+1 starts.
     Never fan these out in parallel.

Seedance 2.5 quirk: pinned tasks REJECT `aspect_ratio` ("first-frame and
first-last-frame tasks only support adaptive aspect ratio"), so the field is
omitted and the frame shape is inherited from the keyframes.

Resumable — a clip already on disk is not regenerated, so a crash after a paid
render does not bill twice. Credit balance is logged around every call.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

KEY = os.environ.get("KIE_API_KEY")
if not KEY:
    sys.exit("ERROR: KIE_API_KEY not set")
UPLOAD_PATH = os.environ.get("KIE_UPLOAD_PATH", "retail-edge")
MODEL = os.environ.get("SEEDANCE_MODEL", "bytedance/seedance-2-5")
RES = os.environ.get("CLIP_RES", "720p")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
HDRS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "User-Agent": UA}
JOBS_CREATE = "https://api.kie.ai/api/v1/jobs/createTask"
JOBS_INFO = "https://api.kie.ai/api/v1/jobs/recordInfo"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"
CREDIT = "https://api.kie.ai/api/v1/chat/credit"
FFMPEG = os.path.expanduser("~/bin/ffmpeg")


def req(url, body=None, timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=HDRS,
                               method="POST" if data else "GET")
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return json.loads(f.read())


def fetch(url, out, timeout=900):
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


def upload(path, folder):
    """Publish a LOCAL file to Kie's CDN.

    Only extracted last frames need this — keyframes already live on Kie's CDN
    and re-uploading them would be a large redundant payload. Downscaled to
    1080p-wide JPEG first so the base64 body stays small enough to survive.
    """
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    d = req(UPLOAD, {"base64Data": f"data:image/jpeg;base64,{b64}",
                     "uploadPath": f"{UPLOAD_PATH.rstrip('/')}/{folder}",
                     "fileName": os.path.basename(path)}, timeout=300)
    if not d.get("success"):
        raise RuntimeError(f"upload failed: {d}")
    return d["data"]["downloadUrl"]


def extract_last(clip, out):
    """The chain's start pin — the clip's REAL final frame.

    A 1-frame `-sseof -0.05` window is not reliable: depending on where the
    container's last keyframe falls, ffmpeg exits 0 having written nothing, and
    the chain then breaks one step later with a confusing missing-file error.
    Decode a generous tail and let `-update 1` overwrite until the last frame
    wins, widening the window if that somehow still produces nothing.
    """
    for window in ("-0.6", "-2", "-5"):
        subprocess.run([FFMPEG, "-v", "error", "-y", "-sseof", window, "-i", clip,
                        "-vf", "scale=1080:-2", "-q:v", "2", "-update", "1",
                        out], check=True)
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            return
    raise RuntimeError(f"could not extract a last frame from {clip}")


def gen_clip(prompt, first_url, last_url, dur, out):
    body = {"model": MODEL, "input": {
        "prompt": prompt,
        "first_frame_url": first_url,
        "last_frame_url": last_url,
        "resolution": RES,
        "duration": dur,
    }}
    d = req(JOBS_CREATE, body)
    if d.get("code") != 200:
        raise RuntimeError(f"createTask {d.get('code')}: {d.get('msg')}")
    tid = d["data"]["taskId"]
    open(f"{out}.task-id", "w").write(tid)   # persist before waiting — a lost id
    log(f"    task {tid}")                   # after a paid render costs it twice
    for i in range(240):
        time.sleep(10)
        s = req(f"{JOBS_INFO}?taskId={tid}")["data"]
        st = s.get("state")
        if st == "success":
            url = json.loads(s["resultJson"])["resultUrls"][0]
            fetch(url, out)
            return
        if st == "fail":
            raise RuntimeError(f"clip failed: {s.get('failMsg') or s.get('failCode')}")
        if i and i % 6 == 0:
            log(f"    ...{i * 10}s  state={st}")
    raise TimeoutError("clip timed out")


def main():
    sb = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else len(sb["clips"])
    os.makedirs(out, exist_ok=True)
    kfdir = os.environ.get("KF_DIR") or os.path.join(os.path.dirname(out) or ".", "keyframes")
    kf_urls = [open(os.path.join(kfdir, f"{k['id']}.url")).read().strip()
               for k in sb["keyframes"]]

    log(f"model={MODEL} res={RES}  credits={credits()}")
    first_url = kf_urls[0]
    for i, c in enumerate(sb["clips"][:limit]):
        p = os.path.join(out, f"{i:02d}-{c['id']}.mp4")
        chain = os.path.join(out, f"{i:02d}-{c['id']}-last.jpg")
        chain_url_f = chain + ".url"

        if os.path.exists(p) and os.path.getsize(p) > 100_000:
            log(f"{c['id']} cached")
        else:
            before = credits()
            log(f"{c['id']} {sb['keyframes'][i]['id']}->{sb['keyframes'][i+1]['id']} "
                f"{c.get('duration', 5)}s  credits={before}")
            gen_clip(c["prompt"], first_url, kf_urls[i + 1],
                     c.get("duration", 5), p)
            after = credits()
            log(f"{c['id']} done {os.path.getsize(p)//1024}KB  "
                f"cost={before - after:.0f}  credits={after}")

        # Hand this clip's REAL last frame to the next clip as its start pin.
        if i + 1 < min(limit, len(sb["clips"])):
            if os.path.exists(chain_url_f):
                first_url = open(chain_url_f).read().strip()
                log(f"    last frame cached")
            else:
                extract_last(p, chain)
                first_url = upload(chain, sb["name"])
                open(chain_url_f, "w").write(first_url)
                log(f"    last frame uploaded -> next start pin")


if __name__ == "__main__":
    main()
