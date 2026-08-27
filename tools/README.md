# book.py — your book of business

A local, private customer book. Import a CRM export, get a ranked plan for the
day, track follow-up cadence, and measure your response time.

**Python 3.8+, standard library only.** Nothing to install.

The dealership's CRM owns the dealership's data. This owns your working notes
on the relationships — so your follow-up cadence survives a CRM migration, a
lead-routing change, or a move to another store.

---

## First run

```bash
# 1. Export a list from the CRM as CSV. Anything you can see, you can export.
# 2. Import it:
python3 tools/book.py import ~/Downloads/crm_export.csv

# 3. Get your day:
python3 tools/book.py brief
```

That's it. Column names are matched loosely — `Cell Phone`, `Mobile`, and
`Primary Phone` all resolve to the same field. Re-importing the same file
updates existing people instead of duplicating them, and never blanks out a
field with an empty one, so you can re-export daily without losing anything.

---

## Commands

| Command | Does |
|---|---|
| `import <file.csv>` | Ingest a CRM export. Safe to re-run. |
| `brief` | Today's ranked action list. `--limit 12` |
| `due` | Who's gone too long without a touch. `--days 30` |
| `log <id> <channel>` | Record a touch. `call`/`text`/`email`/`video`/`in-person` |
| `lead <id>` | Stamp a lead as arrived |
| `lead <id> --respond` | Stamp your reply — prints your response time |
| `stats` | Pipeline and response-time numbers. `--days 14` |
| `find <query>` | Look someone up by name, phone, email, or model |

## How `brief` ranks people

Not by age — by close probability:

1. **Positive equity + in the service lane this week.** Equity leads close at
   15–22%; service customers convert ~3x cold leads. Best opportunity in the
   building.
2. **Lease maturing inside 120 days.** The deadline exists whether you call or
   not. Someone is getting this deal.
3. **In the service lane this week**, equity flat or unknown.
4. **Positive equity, no scheduled reason to talk.** Needs your best opener.
5. **Sold-customer anniversaries** at 30 / 90 / 365 days.
6. **Gone quiet** — 60+ days, or never contacted.

Capped at 12 by default. A brief you finish beats a list you abandon at name
four; it tells you how many fell below the cut.

**Consent is shown on every entry**, and the tool never suggests a text to
someone whose consent isn't confirmed — it tells you to call instead.

## Measuring response time

This is the one number worth watching. Industry median is 47 minutes. Leads
answered inside 5 minutes close at 25–32%; after an hour, 3–5%.

```bash
python3 tools/book.py lead 42            # lead just came in
# ... you respond ...
python3 tools/book.py lead 42 --respond  # prints elapsed time
python3 tools/book.py stats              # median + % under 5 min
```

Log it for two weeks and you'll know whether the discipline is real.

---

## Privacy — read this once

**`book.py` refuses to store** SSNs, dates of birth, credit scores, bureau
data, account/routing/card numbers, and driver's license numbers. If your
export contains those columns, they're dropped at import and the tool tells
you which ones it refused. This is deliberate and not configurable.

**Your responsibilities:**

- **Confirm with your GM what you're allowed to take off-system.** Being
  authorized to *access* the CRM is not the same as being authorized to *copy
  customer data to a personal machine.* Ask before the first import. Most
  stores are fine with a working list; nearly none are fine with a full
  database dump, and the difference matters.
- **`data/` is gitignored.** Never commit it, never sync it to a personal
  cloud drive, never email it.
- **Keep only what you need** — name, contact, vehicle, equity, dates. Nothing
  financial beyond an equity figure.
- **Full-disk encryption on.** FileVault on Mac, BitLocker on Windows.
- **If you leave the store**, ask what you're permitted to keep. Relationships
  are yours; the dealership's customer database is not.

This tool is deliberately small and boring for exactly this reason. It holds a
call list, not a credit file.

---

## Using it with Claude

The `daily-brief` skill reads this tool's output. On the rig:

> "Run the brief and write me an opener for each of the top five."

Claude runs `book.py brief`, reads the ranking, and writes the openers using
the product knowledge and compliance rules in `reference/`. That's the loop:
the tool decides *who*, Claude writes *what to say*, you decide whether to send
it.
