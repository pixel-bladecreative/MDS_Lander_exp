# BRIEF — Retail Edge post-tradeshow lead-capture scroll-film

Durable brief. Chat context gets compacted on long Lane B builds; this file does not.
If you are resuming: read this first, then `docs/STATUS.md`.

## The job
Post-trade-show landing page for **Retail Edge** (MODUS, CO. — client: Modus/ZonePro).
Email goes out to attendees who visited the booth; we already have their addresses.
Page must capture lead info and route them to an expert to **start customization fast**.

Central idea: *"Thank you for visiting us at our booth."* They have already touched the
product. Do not re-explain it from zero — reactivate the memory, prove it at scale, make
the customization feel like the fun part, then take the form fill.

## Decisions locked (from Spencer, 2026-08-25)
- **Lane B** — cinematic generated footage, scroll-scrubbed. Not pure-code.
- **Form endpoint: placeholder.** Single `ENDPOINT` constant at top of the page script.
  Fully validated client-side. Modus (or Spencer) drops the real URL in later.
- **No trade show named.** Evergreen "our booth" copy — reusable next show, no edit.
- **All four SKUs**, Single Mobile Stand as hero. Other three in a spec-comparison row.
  Form asks which SKU they want — that is a real qualifier for the expert call.

## Video engine
- **Kie.ai.** `KIE_API_KEY` is set in env. No Higgsfield on this machine.
- Model: **`bytedance/seedance-2-5`** (highest Seedance Kie exposes; `bytedance/seedance-2`
  also valid, `seedance-2.0`/`2.5`/`v1-pro` are NOT).
- **Seedance 2.5 pinned tasks reject `aspect_ratio`** — "first-frame and first-last-frame
  tasks only support adaptive aspect ratio". Omit the field when pinning both ends.
- Keyframes: `nano-banana-2`, chained (kf N+1 references kf N).
- `KIE_UPLOAD_PATH=retail-edge` — verified working:
  `https://tempfile.redpandaai.co/kieai/11673325/retail-edge/...`
- ffmpeg/ffprobe 7.0.2 static at `~/bin/` (apt is broken in this container — do not retry apt).
- Credits: 9166 at session start. 205 burned on accidental schema probes (createTask
  returns 200 and BILLS even for a junk prompt — never probe schema with a valid `prompt`).

## Hard content rules
1. **Never generate footage containing real third-party brand marks.** No M&M's, Oreo,
   ROAR, HIPPEAS, Walmart, Nabisco in generated frames. Fabricating brand deployments
   that never happened is a real legal problem. Generated banners carry Retail Edge or
   neutral store messaging only.
2. **Real third-party proof comes from real photos only** — the ones Modus already
   publishes on madebymodus.com. Those are in `site/assets/img/`.
3. **Seed keyframes with the real product photography** so the generated hardware is the
   actual Retail Edge unit, not an invented barrier. This is a physical product; an
   AI-hallucinated version of it on the client's own lander is a credibility hole.

## Brand system (pulled live from their Elementor kit)
| Token | Hex |
|---|---|
| primary (navy) | `#0F4068` |
| secondary (blue) | `#1B76B9` |
| accent (amber) | `#FBA919` |
| text/black | `#010000` |
| grey | `#717274` |
| light grey | `#CFCFCE` |
| pale blue | `#8EA8D0` |
| purple (Spotlight brand, avoid here) | `#662D91` |

Fonts: **Readex Pro** (display + body, 700/400) · **Nunito Sans** (accent, 800).

## Product facts (verified from madebymodus.com)
Positioning: *"Where Loss Prevention Meets Advertising."*

| SKU | Banner | Retracted | Weight |
|---|---|---|---|
| Single Mobile Stand *(hero)* | 12 ft × 35 in | 17 in W × 42 in H | 55 lbs |
| Dual Mobile Stand | 24 ft × 35 in (2 banners) | 18 in W × 40 in H | 72 lbs |
| Mounted Barrier | 12 ft × 35 in | 3 in dia. canister | 9 lbs |
| Attachment Stand | — (anchor point) | — | — |

Shared: industrial aluminium + reinforced steel base; DuraSafe™ / Luminex™ banner fabric,
sustainably produced, fully VOC-free, sag-free photo-quality graphics; **quick-swap
cartridge** (banner changes in seconds, no tools); **push-through safety latch**
(proprietary, controlled emergency access, fire-code compliant; hook latch also available);
full-colour **dual-sided** print; customizable length.

Applications: closed registers, unmanned aisles, exits, wide aisles, self-checkout bays.
Verticals: big-box home improvement, national supermarket, high-traffic retail.
Case study: **Walmart** — eliminated unattended register access & shrink risk; custom
banners with clear lane-closed messaging; seamless integration into existing checkout layouts.
Phone on the product pages: 801-881-0011.

## Real assets in `site/assets/img/`
| File | What it is | Use |
|---|---|---|
| `Retail_Edge_Video_Poster-scaled.jpg` | Real Walmart lane, associate, HIPPEAS banner, "LANE CLOSED" | strongest real proof shot |
| `IMG_1158-scaled.jpg` | Walmart "Lane Closed / Caja cerrada" in-store | bilingual proof |
| `Retail_Edge-Single-Mobile_Stand-Oreo-scaled.jpg` | studio, pure white, Oreo banner + BOGO | hero SKU card / keyframe seed |
| `Retail_Edge-Dual-Mobile_Stand-Roar-scaled.jpg` | studio, pure white, ROAR dual banner | SKU card |
| `Retail_Edge-Mounted_Barrier-MMs-scaled.jpg` | studio, pure white, M&M's banner | SKU card |
| `Retail_Edge-Attachment_Stand-1-scaled.jpg` | studio, pure white, bare stand | SKU card |
| `Retail_Edge_Hor_SHAD_NoR.png` / `Retail_Edge_noTM.png` | Retail Edge wordmark | header/footer |
| `MODUS_Logo_WHT.png` / `MODUS_Logo_Blue.png` | MODUS wordmark | footer |
| `Walmart-Logo.png` | Walmart mark | proof strip only |

Product video (47MB, 1080p) lives at
`https://madebymodus.com/wp-content/uploads/2026/04/retailedge_product_video_v1281080p.mp4`
— hotlink click-to-play if used at all. Do NOT commit it.

## Do-nots
- Do not commit `film/clips/`, `film/keyframes/`, or any raw mp4. Runtime `frames/` only.
- Do not run a preview server in the foreground — `nohup … &`, poll with curl, `pkill` after.
- Do not narrate the page's own mechanic in copy ("as you scroll…") — `copy-gate.js` fails it.
- Do not use `aspect_ratio` on pinned Seedance 2.5 calls.
- Do not push to any branch except `claude/retail-edge-landing-page-qzdxaw`.
