# Mazda Sales Kit

A working kit for an individual Mazda salesperson at **Bob Penkhus Mazda at
Powers**, Colorado Springs (80923) — built to be operated solo, from a phone,
between customers.

Not a marketing campaign. A set of tools and a two-week plan for generating
business you own rather than waiting on the rotation.

---

## Start here

1. **Read [`PLAYBOOK.md`](PLAYBOOK.md).** The 14-day sprint. Nothing in it needs
   permission, budget, or a system you do not already have.
2. **Set up [`PHONE-KIT.md`](PHONE-KIT.md).** Fifteen minutes, once. This is
   what you actually use on the floor.
3. **Skim the `reference/` files.** You do not need to memorize them — the
   skills read them for you — but knowing what is in there tells you what you
   can ask for.

---

## What's in here

### Skills — `.claude/skills/`

| Skill | Use it for |
|---|---|
| **lead-response** | Fast, personal first responses. Consent-checked. The highest-value tool in the kit. |
| **deal-math** | Payment scenarios, cash vs. APR, honest total-cost comparisons. |
| **video-scripts** | Batch content for TikTok/Reels/Shorts, plus 1:1 customer videos. |
| **daily-brief** | Turns a pasted CRM view into a ranked plan with openers written. |

### Tooling — `tools/`

**`book.py`** — Holden's book of business. Imports CRM exports, ranks who to
work today by close probability, tracks follow-up cadence, and measures
response time against the 5-minute window. Python stdlib only, nothing to
install, all data local. See [`tools/README.md`](tools/README.md).

```bash
python3 tools/book.py import ~/Downloads/crm_export.csv
python3 tools/book.py brief
```

It refuses to store SSNs, dates of birth, credit scores, and account numbers.
`tools/data/` is gitignored. Read the privacy section before the first import.

### Reference — `reference/`

| File | Contains |
|---|---|
| **mazda-lineup-2026.md** | The lineup, honest strengths and weaknesses, current incentive snapshot |
| **colorado-springs-market.md** | The Fort Carson military market, local content angles, competitive set |
| **objections.md** | What objections actually mean and what to say |
| **compliance.md** | TCPA, advertising claims, customer privacy. Read this once. |

---

## Setup

**On the rig (primary).** Clone the repo and run Claude Code in it — the skills
load automatically and Claude can run `book.py` directly. Needs Python 3.8+.

```bash
git clone <this repo>
cd MDS_Lander_exp
python3 tools/book.py import ~/Downloads/crm_export.csv
```

Then just talk to it: *"Run the brief and write me an opener for each of the
top five."*

**On a phone (on the floor).** Create a Project in the Claude app, add the four
`reference/` files as project knowledge, and use the prompts in
[`PHONE-KIT.md`](PHONE-KIT.md). No `book.py` there — the phone is for drafting
responses fast, the rig is for planning.

---

## Two things this kit takes seriously

**Incentives go stale.** Mazda publishes new programs monthly, usually around
the 3rd, and regional cash differs from national. The snapshot in
`reference/mazda-lineup-2026.md` is dated and the `deal-math` skill is
instructed to verify current programs before doing any math. **Your desk is the
authority — not this repo and not the internet.**

**Compliance is not decoration.** TCPA damages run $500–$1,500 per message and
auto dealers are a favored target. Every skill that drafts outbound checks
consent before writing a word, and none of them will help you send a bulk
message to a list. Read `reference/compliance.md` once so you know why.

---

## What this deliberately does not do

- **Nothing sends on its own.** Every message goes out because you read it and
  decided to. An automated system texting customers is a TCPA problem and a
  quality problem with your name on it.
- **No AI avatars of you.** Trust is the product in this business. Use AI for
  scripts, captions, and editing — not for your face.
- **No landing page yet.** It is the most enjoyable thing to build and the
  slowest to pay. Build it once the sprint shows video is producing DMs and
  there is real traffic to send somewhere.

---

## The idea underneath all of it

The problem was never lead volume. It was competing for the store's leads on a
rotation — a fight you cannot win by trying harder.

Speed, honesty, and follow-through are the only three things fully within your
control, and all three are rare enough to be a genuine advantage.
