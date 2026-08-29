# BRIEF — Onus IV mobile-service launch scroll-film

Durable brief. Chat context gets compacted on long Lane B builds; this file does not.
If you are resuming: read this first.

## The job

A dedicated landing page for **Onus IV Therapy + Longevity**'s new **mobile IV service**
(client: Onus IV — Spencer sells them SEM + consulting; web dev is an open opportunity).

Same build pattern as the Retail Edge lander for MODUS on
`claude/retail-edge-landing-page-qzdxaw` in this repo: a scroll-scrubbed cinematic film
that *is* the hero, then real content sections and a lead form beneath it.

**Angle Spencer set:** self-improvement. Getting the edge on life. Peptide therapy,
hormone treatment and traditional IV framed as a *biohack that levels you up* — not as
sick-care. The mobile unit is the delivery mechanism for that whole stack.

## The strategic tension, and how this page resolves it

Onus's mobile page as written is a **group/event logistics** offer — 4-person minimum,
weddings, bachelorette parties, corporate retreats, ski trips. That is a convenience
story. The "edge on life / level up" angle is their **longevity** story — peptides,
hormones, NAD+. Two different buyers.

Resolution: **the friction is the thing being removed.** What stops people optimising
consistently is not the protocol, it is the drive, the appointment, the Tuesday. Mobile
deletes that. So the page argues *the clinic comes to you* as the unlock for the whole
optimisation stack, and keeps the group/event mechanics as the concrete, honest offer.

## Hard content rules

1. **Do not lean on specific compounds.** Google's healthcare / prescription-drug policy
   is live exposure here (GLP-1s, TRT/BHRT, NAD+, high-dose vitamin C). Talk in
   categories — "peptide therapy", "hormone optimisation", "IV hydration" — not doses,
   not brand-name drugs, not outcome promises. No "cures", no "treats", no numbers on
   efficacy. This is Spencer's explicit instruction and it protects their entire booking
   channel.
2. **Never generate footage containing a real third-party brand mark**, a real person's
   likeness, or a fabricated clinical scene presented as documentary. Generated frames
   carry the Onus world only.
3. **Real proof comes from real photos only** — the ones Onus already publishes on
   onusiv.com. Those are in `site/assets/img/`.
4. **Seed keyframes with the real mobile unit photograph** so the generated van is
   *their* van (black + green wrap, mountain/pine graphic), not an invented Sprinter.
5. **No medical claims in generated imagery either** — no needles in arms, no IV
   catheters being placed, no blood.

## Verified facts (from onusiv.com, 2026-08-26)

- **Mobile launches September 2026.** This is a launch page, not an evergreen page.
- Groups of **4 or more**. **48-hour** notice. Subject to staff availability.
- Pricing: **$100 travel fee** + cost of each drip · **10% off** at 10+ drips ·
  **20% staff gratuity** on all mobile services · **+$50** after-hours, subject to
  availability.
- Team is **ER-certified**, same hospital-based protocols as the clinics.
- Serves Denver + surrounding Colorado areas. Home, hotel, wedding venue, event.
- Named use cases: weddings, bachelor/bachelorette, corporate retreats, group travel,
  ski trips, marathon recovery, pre-flu-season immunity, out-of-town guests at altitude.
- Roughly **30–45 minutes per person** on site.
- Popular mobile drips (by need-state name only): Hangover · Immunity · Altitude ·
  Muscle Recovery.
- Text-your-zip intake: **+1 720-706-6304** (`sms:+17207066304`), prefilled body asking
  name / zip / preferred date+time.
- **7 Colorado locations**: LoHi, Wheat Ridge, Boulder, Denver Tech Center,
  Highlands Ranch, Fort Collins (first franchise, 2025), Central Park (coming soon).
- Founded **2014**; 10+ years operating.
- **5.0 stars, 409 reviews** (Birdeye, Denver location).
- Credentials: LegitScript certified · AIVA member · American Peptide Association ·
  peptides sourced from 503A compounding pharmacies · Colorado Owned & Operated.
- Press/awards on their site: Westword Best of Denver 2026 Readers' Choice, Denver
  Business Journal Fastest Growing, Goldman Sachs 10KSB alumni, CBS Denver, Denver Post,
  5280, Outside, Runner's World, Mile High Sports.
- Socials: instagram.com/onusiv · facebook.com/onusivbar · x.com/onus_iv

## Brand system (pulled live from onusiv.com/dist/main.css)

| Token | Hex |
|---|---|
| secondary — **electric lime** (the signature) | `#83F214` |
| primary — orange | `#FF9900` |
| dark-primary — burnt orange | `#E28701` |
| dark — near-black olive | `#292C1F` |
| dark-green — olive | `#444837` |
| khaki — sage | `#8CA87D` |
| ice | `#ECEAE4` |
| light | `#EDEAE4` |
| mist | `#DDD8D0` |
| titanium | `#E4E4E4` |
| info — pale blue | `#9FBDCB` |

Fonts, as used on their live site: **League Gothic** (display — tall condensed grotesque)
· **Trispace** (technical/UI — squarish, variable) · **Outfit** (secondary sans).

### Their real visual signature — use it, don't invent one
- Charcoal / near-black walls carrying **black topographic contour lines**.
- **Electric-green paracord** IV hangers on carabiners. This is the single most
  recognisable thing in their clinics.
- Warm **amber / chartreuse** drip bags lit from behind.
- Colorado: Flatirons, snow, ponderosa, high-desert playa, alpenglow.
- The **black-and-green wrapped Sprinter van** with a pine/mountain graphic.
- Staff in black tees. One real photo has a shirt reading "LEVEL UP WITH PEPTIDES".

### Their real voice (quote-adjacent, reuse the cadence)
"Take Onus of your health + wellbeing" · **#LIVEBETTERLONGER** · **#yourbestdays** ·
"your best days are still ahead" · "Real optimization, run by real clinicians" ·
"Age on your terms" · "Weight loss, leveled up" · "Level up with peptides".

## Real assets in `site/assets/img/`

| File | What it is |
|---|---|
| `onus-mobile-van.jpg` | **The hero asset.** Their real wrapped Sprinter on a high-desert playa at golden hour, mountains behind. Keyframe seed for the film. |
| `onus-lounge-drip.jpg` | Highlands Ranch lounge — green cords, topo wall, amber bag, clients reclining. The brand world in one frame. |
| `onus-green-lines.jpg` | Three green paracords + amber bags against a dark topo wall. |
| `onus-medic-mixing.jpg` | ER-certified staffer drawing into a bag. Documentary, real. |
| `onus-medic-bag.jpg` | Smiling medic holding a prepared bag. Warm, human. |
| `onus-consult-peptides.jpg` | Clinician and client at a consult with a vial case. |
| `onus-levelup-tee.jpg` | Staffer in the "LEVEL UP WITH PEPTIDES" tee with a client. |
| `onus-flatirons-run.jpg` | Trail runner, snow, Flatirons. Colorado proof. |
| `onus-outdoors-wide.jpg`, `onus-membership.jpg`, `onus-consult-wide.jpg` | supporting |
| `bag-*.jpg`, `shot-*.jpg` | isolated product renders on white |
| `cred-*.jpg` | LegitScript, AIVA, Colorado, American Peptide Assoc, Westword BOD |
| `press-*.jpg` | Denver Post, CBS, 5280, Outside, Runner's World, Mile High, DBJ, Goldman |
| `onus-logo-white.png` / `onus-logo-dark.png` | lockup, 2700×830, transparent |

## Engine + environment

- **Kie.ai.** `KIE_API_KEY` is set. Balance at session start: **14,692 credits**.
- Model: **`bytedance/seedance-2-5`**. Keyframes: **`nano-banana-2`** at `1K`.
- **Seedance 2.5 pinned tasks reject `aspect_ratio`** — omit it when pinning both ends.
- Measured costs from the Retail Edge build on this same account:
  `nano-banana-2` @1K = **8 credits** · @2K = 642 (never use 2K) ·
  `seedance-2-5` 5s @720p both-ends-pinned = **315 credits**.
- ffmpeg/ffprobe **7.0.2 static at `~/bin/`** — installed this session from
  johnvansickle.com. apt has no ffmpeg in this container.
- `pip install Pillow numpy` done this session; neither ships in the image.
- Chromium is preinstalled at `/opt/pw-browsers/chromium`
  (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`). Never run `playwright install`.

## CORRECTED FACTS — the prototype got these wrong (verified 2026-08-29)

A first prototype was built on another surface and deployed to
`https://comfy-starship-e7961e.netlify.app`. Its founder section is **false**.
It reads: *"Chaz Faulhaber co-founded Onus iV in 2015 as a mobile Sprinter
service. The locations came afterwards… The van never stopped running."*

**Primary sources say otherwise.** From onusiv.com/our-story, verbatim:

> "Onus was born upon the wheels of a mountain bike in the summer of 2014, when
> three riders in the Colorado Rockies found themselves dehydrated, exhausted and
> in need of repair. Having experienced the benefits of an iV in Las Vegas, NV &
> Scottsdale, AZ, the riders knew what they wanted and set out to provide the same
> service to the Colorado Front Range."

| Claim on the prototype | Verified |
|---|---|
| "co-founded … in 2015" | Born summer **2014** (their Our Story; "Since 2014" on the peptides page). First location opened 2015. Both can be said, but not "founded 2015" alone. |
| "as a mobile Sprinter service" | **False.** It started from a mountain-bike ride and an IV experienced in Las Vegas / Scottsdale. |
| "The locations came afterwards" | **Inverted.** The clinics came first. |
| "The van never stopped running" | **False, and self-defeating** — mobile IV is *launching September 2026*. The page claims the company began as the thing it is about to launch. |
| Chaz as the sole named founder | There were **three** founders: Chaz Faulhaber (CMO), **Dr. Ben Wilks, MD**, and **Kristy Anderson**. Naming only the marketing co-founder and omitting the physician is a bad look for a medical brand. |

**Where the error came from — fix this at the source.** The `agency-clients`
skill states: *"Founded 2015, co-founder Chaz Faulhaber, began as a mobile
Sprinter-van service."* That line is wrong and it is what the prototype
faithfully repeated. It will keep poisoning future sessions until it is edited.

**Rule for this build: no origin-story claim ships unless it is quoted or
paraphrased from onusiv.com. Do not source company history from the skill.**
If the founder section stays at all, it must credit all three founders or none,
and must not claim the company began as a mobile service.

## FOUNDERS — client-approved, verified 2026-08-29

Client agreed the page features **Chaz and Kristy** together. They are married and
co-own and run the business.

| Person | Title | Source |
|---|---|---|
| **Chaz Faulhaber** | Founder & Chief Marketing Officer | client; ShoutoutColorado |
| **Kristy Anderson** | Co-founder; **head of operations and business strategy** | onusiv.com blog, "Co-Founder Kristy in Boulder Lifestyle Magazine" |
| Dr. Benjamin Wilks, MD | Co-founder, board-certified ER physician | VoyageDenver; press |

**Her surname is Anderson, not Faulhaber.** They are married; she does not use his
name professionally. Getting this wrong on their own landing page is not survivable.

### The true origin, in Chaz's own words
From the VoyageDenver interview:

> "In 2014, Kristy and I tried out an iV after a mountain bike race and felt amazing.
> Our recovery was practically instant & we noticed numerous other benefits, from a
> reduction in cramping to improved appetite."

They met Dr. Wilks through a mutual friend. **Onus iV Hydration launched at the
Colfax Marathon in May 2015.** Use **2015** as the founding year — it is what the
client says and it matches the launch.

### The story the client wants told
They are bringing the experience of running **brick-and-mortar clinics** *to* the
mobile experience. Helping people feel and perform better **since 2015**. Real
**registered nurses** administering treatment.

Note the direction of travel: clinics first, mobile now. This is the opposite of
what the prototype claimed, and it is also the film's vector — see below.

**Open question to confirm with Spencer before it ships:** the site says
"**ER-certified team**" and "hospital-based protocols"; the client says "real
**registered nurses**". Those are different credential claims. Do not blend them.
Confirm which is accurate for the mobile crew and use only that.

## Assets still needed from Spencer
Instagram is login-walled from this container — all four reel URLs return the SPA
shell with no metadata, so no media or captions can be pulled. Real footage and
stills of Chaz, Kristy and the mobile van need to be downloaded and dropped into
`site/assets/img/` (or Drive) before they can be used.

## Do-nots

- Do not commit `film/clips/`, `film/keyframes/`, or any raw mp4. Runtime `frames/` only.
- Do not run a preview server in the foreground — `nohup … &`, poll with curl, `pkill`.
- Do not narrate the page's own mechanic in copy ("as you scroll…") — `copy-gate.js`
  fails it, and it reads as a brief instead of a website.
- Do not use `aspect_ratio` on pinned Seedance 2.5 calls.
- Do not push to any branch except `claude/onus-iv-mobile-landing-iheqbg`.
- The literal string `placeholder=` in markup trips `copy-gate.js`. Use hint text under
  the label instead — better a11y anyway.
