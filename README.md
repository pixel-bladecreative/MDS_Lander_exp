# Retail Edge — post-booth landing page

A lead-capture landing page for **Retail Edge** (MODUS, CO.), built for the email
that goes out to trade-show attendees who visited the booth.

The page opens as a scroll-scrubbed film: one unbroken forward push down a dark,
closed checkout lane, through the banner that seals it, and out into a bright
store where every lane is closed and carrying a message — the last one blank.
Below the film sit the Walmart proof, the four-unit lineup, the three-step
customization path, and the form.

---

## Wiring the form up — the one thing left to do

Open `site/index.html`, find the top of the page script, and set one constant:

```js
var ENDPOINT = "";                 // <- put the real URL here
var ENDPOINT_METHOD = "POST";
var ENDPOINT_AS_JSON = true;       // false => sends FormData instead
```

While `ENDPOINT` is empty the form still validates, still shows the confirmation
state, and logs the payload to the console — so the page demos fully before it is
connected to anything. Nothing else needs to change.

**Payload posted** (verified, not assumed):

```json
{
  "first_name": "Dana", "last_name": "Reyes", "email": "dana@bigboxco.com",
  "phone": "", "company": "BigBox Co", "role": "Director, Loss Prevention",
  "locations": "51–250 locations", "units_estimate": "", "timeline": "This quarter",
  "application": ["Closed registers", "Self-checkout bays"],
  "product": "Dual Mobile Stand", "message": "", "consent": "yes",
  "source": "retail-edge-booth-followup",
  "page": "https://…", "submitted_at": "2026-08-25T19:10:14.833Z",
  "utm_source": "tradeshow", "utm_medium": "email", "utm_campaign": "booth-followup"
}
```

Multi-select fields (`application`, `product`) arrive as arrays when more than one
is ticked and as a string when one is. Whatever receives this should handle both.

### Prefill from the email link

We already have these people's addresses, so the campaign link should carry them
and save the recipient the typing:

```
https://…/retail-edge/?fname=Dana&lname=Reyes&email=dana%40bigboxco.com&company=BigBox%20Co
```

Accepted keys: `fname`, `lname`, `email`, `company`, `phone`, `role`.
Any `utm_*` on the URL is captured into the payload automatically.

---

## Deploying

The page is static. Upload the contents of `site/` to any host:

```
site/
├── index.html
├── assets/img/        product photography + wordmarks
├── frames/            600 JPEG frames — the 16:9 film
└── frames-mobile/     600 JPEG frames — the 9:16 film
```

Roughly 55MB, almost all of it frames. Nothing is bundled or compiled; there is no
build step. The only external request is Google Fonts (Readex Pro + Nunito Sans).

If the host charges by the object or the frames feel heavy, they can move to a CDN
without touching anything else — set `FRAME_DIR_DESKTOP` / `FRAME_DIR_MOBILE` at
the top of the script to the CDN prefix.

`<meta name="robots" content="noindex, follow">` is set, since this is a campaign
destination and not something that should compete with madebymodus.com in search.
Remove it if that changes.

---

## Why there are two films

A 16:9 film in a portrait phone viewport has two bad options: letterbox to a strip,
or centre-crop. Cropping was not survivable here — the payoff is the blank banner,
and it sits in the left third of the frame, so a centre crop cuts off the thing the
whole page is arguing toward.

So there are two real films, same journey, same grade, **both exactly 600 frames**
so the playhead maps 1:1 when the breakpoint swaps at 768px. The swap closes the
outgoing `ImageBitmap`s rather than leaking them on every rotation.

---

## Regenerating or editing the film

Everything needed is in `film/` and `tools/`. Requires `KIE_API_KEY` and ffmpeg.

```bash
# 1. audit the storyboard's direction of travel — free, and the only gate that
#    runs BEFORE money is spent
python3 ~/.claude/skills/synced/scroll-film-studio/scripts/vector-check.py film/storyboard.json

# 2. keyframes (8 credits each at 1K — iterate here, not on clips)
KF_RES=1K python3 film/gen_keyframes.py film/storyboard.json film/keyframes

# 3. clips — sequential, both ends pinned (315 credits each at 720p)
export KIE_UPLOAD_PATH=retail-edge
CLIP_RES=720p python3 film/gen_clips.py film/storyboard.json film/clips 5

# 4. assemble + extract every frame at native rate
bash tools/assemble.sh film/clips site/frames

# 5. prove it is one continuous move, not a reel of shots
python3 tools/continuity_gate.py site/frames 8
```

Mobile is the same with `film/storyboard-mobile.json`, `KF_DIR=film/keyframes-mobile`,
and `WIDTH=720` on assemble.

Both scripts are **resumable** — anything already on disk is not regenerated, so a
crash after a paid render does not bill twice.

### Cost, measured on this build

| Call | Credits |
|---|---|
| `nano-banana-2` still @ 2K | 642 |
| `nano-banana-2` still @ 1K | **8** |
| `bytedance/seedance-2-5`, 5s @ 720p, both ends pinned | 315 |

A 2K still costs 80× a 1K one and buys nothing — keyframes are only pin targets.
Whole build (both films, including redos): **4,168 credits ≈ $21**.

---

## Verifying changes

```bash
cd site && nohup python3 -m http.server 8899 >/dev/null 2>&1 &

node tools/shot.js  http://localhost:8899/index.html out.png 1440 900 6513
node tools/probe.js http://localhost:8899/index.html 6513
node ~/.claude/skills/synced/scroll-film-studio/scripts/copy-gate.js site/index.html
```

**Headless Chromium throttles `requestAnimationFrame` to roughly 1fps.** The eased
playhead advances about four steps in four seconds, so a screenshot taken by simply
waiting shows a frame mid-easing — it looks exactly like a stuck film. `tools/shot.js`
drives the page's `window.__settle()` hook instead. Before concluding anything is
broken, check `window.__filmStats()`: if `playhead === target` the engine is fine and
the capture was early.

The page also honours `?jump=<scrollY>` (lands pre-scrolled and force-settled) and
`?jank` (logs per-frame rAF p95/max to the console).

---

## Content rules this build follows

**No generated frame contains a real third-party brand mark.** The M&M's, Oreo,
ROAR, HIPPEAS and Walmart artwork on this page comes only from photographs MODUS
already publishes on madebymodus.com. Generating new footage of, say, a branded
Walmart lane would be fabricating a deployment that never happened, on the client's
own landing page. Generated banners carry neutral navy-and-amber only.

The keyframes were seeded with a photograph of the real bare hardware so the film
renders the actual product. Booth visitors have handled this thing; an invented
barrier would be a credibility hole.
