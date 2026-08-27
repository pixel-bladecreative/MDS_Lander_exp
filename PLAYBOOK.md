# The 14-Day Sprint

For: a Mazda salesperson at Bob Penkhus Mazda at Powers, Colorado Springs.

Nothing here requires permission, budget, or a system you do not already have.
Everything here is designed to make money before anything gets built.

---

## The premise

The problem is not "not enough leads." Every salesperson believes that.

The problem is **competing for the store's leads on a rotation** — a zero-sum
fight against the person standing next to you, and when floor traffic is slow,
everyone's slice thins at the same time.

The only durable fix is a **book of business you own**: people who walk in
asking for you by name. Everything below is judged on whether it builds that.

Two weeks will not build a book. Two weeks will prove which of these is worth
building on, and should pay for itself while doing it.

---

## Week 1 — Speed and honesty

### Day 1: Fix response time. This is the whole game.

The median dealership takes **47 minutes** to respond to an internet lead.
Leads answered inside five minutes close at **25–32%**. After an hour, **3–5%**.
78% of buyers buy from whoever responds first.

You do not need a tool for this. You need notifications on and a decision.

- Turn on push notifications for the CRM and Marketplace. Sound on.
- Set a personal rule: **every new lead gets a real response inside 5 minutes**,
  even standing with another customer. "Give me ten seconds" is an acceptable
  thing to say to the person in front of you.
- Use `lead-response` from your phone. Ninety seconds, not twenty minutes.
- **Track it.** `book.py lead <id>` when one arrives, `--respond` when you
  reply. `book.py stats` shows your median and your percentage under five
  minutes. You cannot improve what you are not looking at.

This single change, done consistently, will outperform everything else on this
page combined. It costs nothing.

### Day 2: Get the service appointment list

Ask the service manager for tomorrow's appointments — names and vehicles. Not a
data request, a favor. Bring coffee.

Service customers convert at roughly **3x cold internet leads**. They are
already in the building, already trust the store, and are sitting in a lounge
with nothing to do for two hours.

Run it through `daily-brief`. Go introduce yourself. Do not pitch. Offer to run
their numbers while they wait.

Do this every day for fourteen days.

### Day 3: Turn on equity

You can see equity and lease maturity in the CRM. Most people never look.

- Export everyone with positive equity and every lease maturing in 120 days.
- Import it once: `python3 tools/book.py import <export.csv>`
- `python3 tools/book.py brief` ranks them by close probability and flags
  consent per person. Then ask Claude to write the openers.
- **Check consent before texting anyone.** The tool flags it; respect the flag.
  No consent means call — and calling converts better on these conversations
  anyway.

Re-export and re-import whenever you want; it updates people instead of
duplicating them. Read the privacy section in `tools/README.md` before the
first import, and confirm with your GM what you're permitted to take
off-system.

Equity leads close at 15–22% against 3–7% for internet leads. This is the
highest-conversion prospecting that exists and it is sitting in a system you
already have open.

### Day 4: Start the video habit

Three personalized videos a day. Under 60 seconds. Shot on your phone.

Say their name in the first three seconds, walk to the actual car, answer the
one thing they asked about, **point out one honest flaw**, offer two specific
times.

The flaw is what makes it work. Volunteering a scuff makes everything else you
say believable, and nobody else does it.

Video follow-up gets meaningfully more replies than text. Three a day is
sixty in a month, and roughly zero other salespeople in Colorado Springs are
sending any.

### Day 5: Ask for reviews. Correctly.

At every delivery, ask for a Google review **that mentions your name**.

Not "please review us." Say: *"If you'd leave a review and mention me by name,
it genuinely helps people find me."* Then text them the direct link before they
pull off the lot — asking later means it never happens.

Why the name matters: people search for a salesperson, not just a store. And
review count, recency, and what reviewers actually say are the heaviest inputs
into how AI assistants answer "who should I talk to at a Mazda dealer in
Colorado Springs." That question is being asked right now and the answer is
currently somebody else.

This is a compounding asset that costs one sentence per delivery.

### Days 6–7: The first shoot day

Two hours. Ten videos. One setup.

Use `video-scripts` to generate a batch. **Lead with "PCSing to Fort Carson?
Watch this before you buy a car."**

That video works because the audience is enormous here, it renews itself every
posting cycle, the intent is about as high as it gets, and essentially nobody
is making it. Everyone else in this market is posting inventory walkarounds
that get no distribution.

Post one a day for the next two weeks. Do not evaluate results before day 14.

---

## Week 2 — Volume and compounding

### Day 8: Facebook Marketplace

Marketplace is now the second-largest automotive listing channel in the US by
used-car lead volume. Over 40% of used-vehicle buyers under 40 start there.
Listing is free.

- Confirm how your store handles Marketplace and what you are permitted to post
  personally. You have free rein — use it, but know the store's process.
- Real photos of real units. Never stock images presented as your inventory.
- **Respond within 5 minutes.** Marketplace buyers message four sellers at once
  and buy from whoever answers first. This is the same discipline as Day 1
  pointed at a different inbox.

### Day 9: The military practice

Colorado Springs is one of the most military-dense metros in the country —
Fort Carson, Peterson, Schriever, the Academy, Cheyenne Mountain.

Mazda Military Appreciation is **$500**, stackable, and covers active duty,
reserves, retirees, disabled veterans, **and anyone within two years of
separation**. Almost nobody knows that last one.

But the $500 is not the opportunity. **The opportunity is becoming the Mazda
person the base recommends.** That means knowing PCS timing, what happens to a
payment during a deployment, SCRA rate protections, and being willing to tell a
young E-3 honestly that they should not be in a $700 payment.

That costs you one deal and earns you a unit. Peak PCS season runs roughly May
through August — build the practice now, before it arrives.

Make the "PCSing to Fort Carson? Watch this before you buy a car" video.

### Day 10: Work the dead

Pull leads marked lost 60–180 days ago. **Confirm consent on every one.**

One honest message, no pitch:

> "Hey [name] — [your name] at Penkhus. No pitch. Just making sure you landed
> somewhere good. If you already bought, genuinely congrats — what'd you get?
> If you're still looking, I'm here."

The reply rate is remarkable, and the ones who already bought frequently become
referral sources. Nobody else in the store is touching these.

### Day 11: Build the follow-up cadence

Every sold customer, on a schedule: **day 30, day 90, day 365**, plus every
service visit, plus lease maturity minus 120 days.

Most salespeople deliver a car and never speak to that person again — which is
why most salespeople start from zero every month.

Every touch carries new information. "Just checking in" is not information and
it teaches people to ignore you.

### Day 12: The second shoot day

Ten more. By now you know which of the first ten performed.

**Do not chase views.** Chase saves, shares, and DMs. A video with 400 views
and six DMs beats one with 40,000 views and none. You are not building an
audience, you are building a customer list.

### Days 13–14: Look at what happened

Honestly, on paper:

- Average response time, day 1 vs day 14
- Videos sent · replies received
- Service-lane conversations · appointments set
- Equity conversations · appointments set
- Reviews earned that name you
- Which video angle produced actual DMs
- **Units sold, and how many you sourced yourself**

The last line is the only one that ultimately matters. Everything else is
leading indicators.

---

## After the sprint

What you learn in fourteen days determines what gets built next:

- **If video is producing DMs** → the personal landing page becomes worth
  building. It gives all that traffic somewhere to go that is not the store's
  generic site, structured so AI assistants surface you by name.
- **If the service lane is producing** → push for a standing daily list and
  formalize it with the service manager.
- **If Marketplace is producing** → volume and speed tooling.
- **If none of it is producing** → the assumptions were wrong, and finding that
  out in two weeks for zero dollars is the cheapest possible outcome.

---

## The three rules underneath all of it

1. **Speed beats polish.** A good response in four minutes beats a perfect one
   in forty.
2. **Honesty is the differentiator.** Naming the flaw, doing the math against
   yourself, telling someone the Telluride has more third-row room. Every
   competitor is optimizing for the close. Optimize for being believed.
3. **Own the relationship, not the transaction.** The commission is this month.
   The book is the career.
