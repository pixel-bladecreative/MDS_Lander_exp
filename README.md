# Onus iV — Mobile IV landing page

A campaign landing page for **Onus iV Therapy + Longevity**'s mobile IV service,
which opens **September 2026**. Client: Onus IV.

The page opens as a scroll-scrubbed film called **The Descent**: one unbroken fall
from above the cloud deck at 11,800 ft, down through the Front Range, down into a
Denver neighbourhood, and down to the van waiting at the curb — landing at 5,280 ft
as the vehicle fills the frame. Below the film sit the three-step booking flow,
the four need-states, the proof, the founders, the mechanics and the request form.

---

## The one thing left to do — wire up the form

Open `site/index.html`, find the config block at the top of the page script, and
set one constant:

```js
var ENDPOINT        = "";      // <- the real URL goes here
var ENDPOINT_METHOD = "POST";
var ENDPOINT_AS_JSON= true;    // false => sends FormData instead
```

While `ENDPOINT` is empty the form still validates, still shows the confirmation
state, and logs its payload to the console — so the page demos completely before it
is connected to anything.

**Payload posted** (verified, not assumed):

```json
{
  "first_name": "Dana", "last_name": "Reyes", "email": "dana@example.com",
  "phone": "720-555-0111", "event_date": "2026-10-04", "zip": "80211",
  "group_size": "7–10", "occasion": "Wedding", "message": "",
  "consent": "on", "source": "onus-mobile-lander",
  "page": "https://…", "submitted_at": "2026-08-29T02:11:04.128Z",
  "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "mobile-iv-launch"
}
```

Any `utm_*` on the URL is captured automatically. A campaign link can also prefill
the form and save the recipient the typing:

```
https://…/?fname=Dana&lname=Reyes&email=dana%40example.com&phone=7205550111&zip=80211
```

Accepted keys: `fname`, `lname`, `email`, `phone`, `zip`.

### Turn off the draft banner for production

```js
var PREVIEW_BANNER = true;   // -> false
```

An amber bar marks the page as a draft and says the form is not connected, so a
reviewer does not submit a test entry and wonder where it went. It is dismissible
and the dismissal persists in `localStorage`, so it stays out of screenshots.

---

## Deploying

The page is static — no build step, nothing bundled. Upload the contents of `site/`
to any host.

```
site/
├── index.html
├── _headers            cache policy (Netlify/Cloudflare format)
├── assets/img/         real Onus photography, credential marks, the logo lockup
├── frames/             720 JPEG frames — the 16:9 film
└── frames-mobile/      720 JPEG frames — the 9:16 film
```

### Netlify

`netlify.toml` is committed and publishes `site/` with no build command. Either
connect the repo and pick this branch, or drag `site/` into the Netlify UI.

Frames are ~85MB across both sets and are served with a one-year immutable cache.
If the object count ever matters, they can move to a CDN without touching anything
else — set `FRAME_DIR_DESKTOP` / `FRAME_DIR_MOBILE` at the top of the page script
to the CDN prefix.

`<meta name="robots" content="noindex, follow">` is set, and `netlify.toml` sends
`X-Robots-Tag` to match. This is a campaign destination and should not compete with
onusiv.com in search. Remove both if that changes.

---

## Why there are two films

A 16:9 film in a 390×844 portrait viewport has two bad options: letterbox to a
strip, or centre-crop and keep 26% of every frame. Cropping was not survivable —
the payoff is the van, and a centre crop of a landscape frame loses the street it
arrives on.

So there are two real films, same journey, same grade, **both exactly 720 frames**,
so the playhead maps 1:1 when the breakpoint swaps at 768px. The swap closes the
outgoing `ImageBitmap`s rather than leaking them on every rotation.

---

## Regenerating or editing the film

Everything needed is in `film/` and `tools/`. Requires `KIE_API_KEY` and ffmpeg.

```bash
# 1. audit the storyboard's direction of travel — free, and the only gate that
#    runs BEFORE money is spent
python3 ~/.claude/skills/synced/*/scroll-film-studio/scripts/vector-check.py film/storyboard.json

# 2. keyframes (8 credits each at 1K — iterate here, never on clips)
KF_RES=1K python3 film/gen_keyframes.py film/storyboard.json film/keyframes

# 3. clips — sequential, both ends pinned (315 credits each at 720p)
export KIE_UPLOAD_PATH=onus-iv
CLIP_RES=720p python3 film/gen_clips.py film/storyboard.json film/clips 6

# 4. assemble + extract every frame at the native rate
bash tools/assemble.sh film/clips site/frames

# 5. prove it is one continuous move, not a reel of shots
python3 tools/continuity_gate.py site/frames 8
```

Mobile is the same with `film/storyboard-mobile.json`, `KF_DIR=film/keyframes-mobile`
and `WIDTH=720` on assemble.

Both scripts are **resumable** — anything already on disk is not regenerated, so a
crash after a paid render does not bill twice.

### Cost, measured on this build

| Call | Credits |
|---|---|
| `nano-banana-2` still @ 1K | **8** |
| `bytedance/seedance-2-5`, 5s @ 720p, both ends pinned | **315** |

Whole build, both films: 14 keyframes (112) + 12 clips (3,780) ≈ **3,892 credits**.

---

## Verifying changes

```bash
cd site && nohup python3 -m http.server 8899 >/dev/null 2>&1 &

node tools/browser/film.mjs     http://localhost:8899/index.html shots 1440 900 d
node tools/browser/sections.mjs http://localhost:8899/index.html shots 390 844 m
node ~/.claude/skills/synced/*/scroll-film-studio/scripts/copy-gate.js site/index.html
```

`tools/browser/launch.mjs` carries the two flags headless Chromium needs to reach
the network in a Claude Code remote session (`--proxy-server=$HTTPS_PROXY` and
`--ssl-version-max=tls1.2`). Without both, every request fails
`ERR_CONNECTION_RESET` while curl to the same host succeeds.

**Do not trust a screenshot that was taken too early.** Beat text fades in over
750ms; a capture at 600ms shows it half-transparent and looks exactly like a
contrast bug. `film.mjs` drives `window.__settle()` and waits. Before concluding
anything is broken, read `window.__filmStats()` — if `playhead === target` the
engine is fine and the capture was early.

The page also honours `?jump=<scrollY>`, which lands pre-scrolled and force-settled.

---

## Content rules this build follows

**No named compounds.** Google's healthcare and prescription-drug policies are live
exposure for this account, and a suspension would take out their entire booking
channel. The page talks in need-states — Hangover, Immunity, Altitude, Recovery —
and never names a drug, a dose or an outcome.

**"ER-certified team", never "registered nurse".** In-clinic staff are RNs today,
but mobile crew composition can change with staffing and "ER-certified" holds
through that. This is deliberate margin, decided by Spencer. Do not "upgrade" it.

**No generated third-party brand marks, and no generated people.** Every van
keyframe keeps the grille turned away and forbids badges, emblems and lettering —
an earlier prototype rendered a Mercedes three-pointed star into client-facing
footage. Faces drift across clips, so people come only from photographs Onus
already publishes.

**Lime never grades a photograph.** `#83F214` is an accent on near-black. The
earlier prototype interpolated every image toward it on scroll and reached a
measured +16 green bias by the footer.

**The founder story is quoted, not remembered.** See `BRIEF.md` — a previous build
stated that Onus began in 2015 as a mobile Sprinter service and that the locations
came afterwards. Their own Our Story page says the company was born on a mountain
bike in 2014 and launched at the Colfax Marathon in May 2015, and there were three
founders. That error came from the `agency-clients` skill, which still carries the
wrong line.

---

## Open items

| Item | Owner |
|---|---|
| Form endpoint URL | Onus / Spencer |
| Photographs of Chaz Faulhaber and Kristy Anderson | Onus |
| Correct the `agency-clients` skill's Onus founding line | Spencer |
| Flip `PREVIEW_BANNER` to `false` before it goes to the client as final | whoever ships it |

The founder section ships as a typographic block with names and titles and **no
portrait**. A generated face on a real named executive is not an option.
