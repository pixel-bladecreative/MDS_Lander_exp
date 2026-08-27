---
name: daily-brief
description: Turn a raw CRM export, lead list, or service appointment list into a ranked action plan for the day, with a specific opener written for each person. Use at the start of a shift, when a lead list feels overwhelming, or to plan equity and lease-maturity outreach. Works from pasted data — no system integration needed.
---

# Daily Brief

The goal is that he walks in with a plan instead of a list. Twelve names sorted
by close probability, each with the first sentence already written, beats two
hundred names in a CRM he will not open.

**This works entirely off pasted data.** He copies whatever he can see — a CRM
view, a lead list, tomorrow's service appointments — and pastes it in. No
integration, no access request, no IT ticket.

---

## Step 1 — Take whatever he has

Accept messy input. A screenshot's worth of text, a CSV, a half-formatted table
someone printed. Do not send him back to get cleaner data.

Useful fields when present: name, vehicle owned or inquired about, last contact
date, lead source, consent/opt-out status, equity or lease maturity, service
appointment time.

If consent status is missing, flag it and default to phone-call
recommendations rather than text.

## Step 2 — Rank by close probability, not by age

This is the part CRMs do badly. Rough ordering, best first:

| Tier | Who | Why |
|---|---|---|
| 1 | **Positive equity + in service tomorrow** | Equity leads close at 15–22%; service customers convert ~3x cold leads. Best opportunity in the building. |
| 2 | **Lease maturing in 60–120 days** | A deadline exists whether or not he calls. Someone is getting this deal. |
| 3 | **Inbound lead from the last 48 hours, no contact yet** | Still inside the window where speed matters. |
| 4 | **Positive equity, no service visit scheduled** | Real opportunity, no natural reason to call — needs the best written opener. |
| 5 | **Sold customers at 30 / 90 / 365 days** | Referral and repeat engine. Cheap to maintain, most people skip it. |
| 6 | **Aged leads, 60+ days, consent confirmed** | Low hit rate, high volume. Batch these. |

**Cap the list at 12.** A brief he actually finishes beats a complete list he
abandons at name four. Say explicitly how many were left off and why, so he
knows the tail exists.

## Step 3 — Write a real opener for each

Not a template with a name merged in. **One specific reason this person, today.**

> **Dana Whitfield** — 2021 CX-5 Touring, 47k mi · service Thu 9:00 AM ·
> ~$3,400 positive equity
> *In the lounge for two hours Thursday. Go say hello around 9:15.*
> "Dana? I'm [NAME] — I don't want to interrupt your morning, but while you're
> waiting: your CX-5 is worth more right now than what you owe, which doesn't
> happen often. Want me to run what a new one looks like? Takes ten minutes and
> you're sitting here anyway."

> **SFC Marcus Bell** — 2022 CX-9, lease matures 11/14 · Fort Carson
> *Lease ends in 79 days. Call, don't text — no consent on file.*
> "Sergeant Bell, [NAME] at Penkhus. Your lease is up in November and I wanted
> you to hear the options from me before the mailers start. Also — the military
> $500 stacks with what's on the CX-90 right now. Two minutes?"

Each entry: **who, why now, what to say.** Nothing else.

## Step 4 — Add the daily non-negotiables

Close every brief with the same three, because they are what actually move the
number and they are the first things to slip on a busy day:

```
TODAY'S THREE
□ Respond to every new lead in under 5 minutes. No exceptions.
□ Send 3 personalized videos.
□ Ask 1 delivered customer for a review that mentions your name.
```

That third one compounds quietly. Reviews naming him are how he gets found —
by people searching, and increasingly by AI assistants answering "who should I
talk to at a Mazda dealer in Colorado Springs." Review count, recency, and what
reviewers actually say are the heaviest inputs into those recommendations.

## Step 5 — Consent gate

Before recommending any text outreach, check consent state. No consent on file
means **recommend a phone call instead** — always compliant, and on an equity
or lease conversation it converts better anyway.

Never recommend a bulk send. Never recommend automated outbound. See
`reference/compliance.md`.

---

## Weekly variant

Once a week, ask for a wider pull and produce a themed batch instead:

- **Lease maturity sweep** — everything maturing in the next 120 days
- **Equity sweep** — everyone above a positive-equity threshold
- **Orphan owners** — customers whose original salesperson has left the store.
  Nobody owns these people. He can.
- **Sold-customer anniversaries** — 1-year and 3-year touches

## Reference

- `reference/compliance.md` — consent rules before any outreach
- `reference/mazda-lineup-2026.md` — current incentives to reference in openers
- `reference/colorado-springs-market.md` — military eligibility, altitude angle
- `reference/objections.md` — when the call goes past hello
