#!/usr/bin/env python3
"""
book.py — Holden's book of business.

A local, private customer book. Import CRM exports, rank who to work today,
track follow-up cadence, and measure response time.

Python 3.8+. Standard library only — nothing to install.

The dealership's CRM owns the dealership's data. This owns the working notes
on the relationships, so the follow-up cadence survives a CRM migration, a
lead-routing change, or a move to another store.

PRIVACY: this refuses to store SSNs, dates of birth, account or card numbers,
and credit-application fields. See scrub_row(). Keep book.db off cloud sync.
"""

import argparse
import csv
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, date

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("BOOK_DB", os.path.join(HERE, "data", "book.db"))

# --------------------------------------------------------------------------
# Fields we refuse to ingest, no matter what the export contains.
# --------------------------------------------------------------------------
BANNED = re.compile(
    r"ssn|social.?security|date.?of.?birth|\bdob\b|birth.?date|"
    r"credit.?score|fico|bureau|account.?number|acct.?num|routing|"
    r"card.?number|cvv|driver.?licen|license.?num|passport",
    re.I,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS contacts (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    phone         TEXT,
    email         TEXT,
    consent       TEXT DEFAULT 'unknown',   -- yes | no | unknown
    source        TEXT,
    status        TEXT DEFAULT 'active',    -- active | sold | lost
    year          INTEGER,
    make          TEXT,
    model         TEXT,
    trim          TEXT,
    mileage       INTEGER,
    equity        REAL,                     -- positive = above water
    lease_end     TEXT,                     -- YYYY-MM-DD
    service_appt  TEXT,                     -- YYYY-MM-DD
    sold_date     TEXT,                     -- YYYY-MM-DD
    interest      TEXT,                     -- vehicle they asked about
    notes         TEXT,
    created       TEXT NOT NULL,
    updated       TEXT NOT NULL,
    UNIQUE(name, phone)
);
CREATE TABLE IF NOT EXISTS touches (
    id          INTEGER PRIMARY KEY,
    contact_id  INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    ts          TEXT NOT NULL,
    channel     TEXT NOT NULL,   -- call | text | email | video | in-person
    direction   TEXT DEFAULT 'out',
    note        TEXT
);
CREATE TABLE IF NOT EXISTS leads (
    id           INTEGER PRIMARY KEY,
    contact_id   INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    received_at  TEXT NOT NULL,
    responded_at TEXT,
    source       TEXT
);
CREATE INDEX IF NOT EXISTS idx_touch_contact ON touches(contact_id);
CREATE INDEX IF NOT EXISTS idx_lead_contact  ON leads(contact_id);
"""

# Fuzzy header mapping — CRM exports never agree on column names.
COLUMN_HINTS = {
    "name":         ["customer name", "full name", "name", "contact", "client"],
    "first":        ["first name", "firstname", "first"],
    "last":         ["last name", "lastname", "last", "surname"],
    "phone":        ["cell", "mobile", "phone", "primary phone", "telephone"],
    "email":        ["email", "e-mail", "email address"],
    "consent":      ["consent", "opt in", "opt-in", "sms consent", "text consent",
                     "do not text", "opt out", "opt-out", "dnc"],
    "source":       ["source", "lead source", "origin", "channel"],
    "status":       ["status", "lead status", "stage"],
    "year":         ["year", "vehicle year", "model year"],
    "make":         ["make", "vehicle make"],
    "model":        ["model", "vehicle model"],
    "trim":         ["trim", "vehicle trim", "series"],
    "mileage":      ["mileage", "odometer", "miles"],
    "equity":       ["equity", "positive equity", "equity position"],
    "lease_end":    ["lease end", "lease maturity", "maturity date", "lease exp"],
    "service_appt": ["service appointment", "appointment date", "ro date",
                     "service date", "appt"],
    "sold_date":    ["sold date", "delivery date", "purchase date", "sale date"],
    "interest":     ["vehicle of interest", "interest", "desired vehicle",
                     "requested vehicle"],
    "notes":        ["notes", "comment", "comments", "memo"],
}


def today():
    return date.today()


def now_iso():
    return datetime.now().replace(microsecond=0).isoformat(" ")


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


# --------------------------------------------------------------------------
# Import
# --------------------------------------------------------------------------

def map_headers(headers):
    """Best-effort map of a CRM export's headers onto our field names."""
    mapping, used = {}, set()
    norm = {h: h.strip().lower() for h in headers if h}
    for field, hints in COLUMN_HINTS.items():
        best, best_len = None, -1
        for h, low in norm.items():
            if h in used:
                continue
            for hint in hints:
                # exact beats substring; longer hint beats shorter
                if low == hint and len(hint) > best_len:
                    best, best_len = h, len(hint) + 100
                elif hint in low and len(hint) > best_len:
                    best, best_len = h, len(hint)
        if best:
            mapping[field] = best
            used.add(best)
    return mapping


def scrub_row(row):
    """Drop any column whose header looks like regulated or sensitive data."""
    dropped = []
    clean = {}
    for k, v in row.items():
        if k and BANNED.search(k):
            dropped.append(k.strip())
        else:
            clean[k] = v
    return clean, dropped


def norm_phone(v):
    if not v:
        return None
    d = re.sub(r"\D", "", str(v))
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d or None


def norm_consent(v):
    if v is None or str(v).strip() == "":
        return "unknown"
    s = str(v).strip().lower()
    if s in ("y", "yes", "true", "1", "opted in", "opt in", "granted", "consented"):
        return "yes"
    if s in ("n", "no", "false", "0", "opted out", "opt out", "dnc", "do not text",
             "stop", "unsubscribed"):
        return "no"
    return "unknown"


def norm_date(v):
    if not v:
        return None
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d-%b-%Y",
                "%Y/%m/%d", "%m-%d-%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def norm_num(v):
    if v is None or str(v).strip() == "":
        return None
    s = re.sub(r"[$,()\s]", "", str(v))
    neg = "(" in str(v) or s.startswith("-")
    s = s.lstrip("-")
    try:
        n = float(s)
        return -n if neg else n
    except ValueError:
        return None


def cmd_import(args):
    conn = connect()
    path = args.file
    if not os.path.exists(path):
        sys.exit(f"No such file: {path}")

    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(fh, dialect=dialect)
        rows = list(reader)

    if not rows:
        sys.exit("File has no data rows.")

    mapping = map_headers(list(rows[0].keys()))
    if "name" not in mapping and not ("first" in mapping and "last" in mapping):
        sys.exit(
            "Could not find a name column.\n"
            f"Headers seen: {', '.join(h for h in rows[0] if h)}"
        )

    def get(row, field):
        col = mapping.get(field)
        return row.get(col) if col else None

    added = updated_n = skipped = 0
    all_dropped = set()

    for row in rows:
        row, dropped = scrub_row(row)
        all_dropped.update(dropped)

        name = (get(row, "name") or "").strip()
        if not name:
            first = (get(row, "first") or "").strip()
            last = (get(row, "last") or "").strip()
            name = f"{first} {last}".strip()
        if not name:
            skipped += 1
            continue

        rec = {
            "name": name,
            "phone": norm_phone(get(row, "phone")),
            "email": (get(row, "email") or "").strip().lower() or None,
            "consent": norm_consent(get(row, "consent")),
            "source": (get(row, "source") or "").strip() or None,
            "status": (get(row, "status") or "active").strip().lower() or "active",
            "year": int(norm_num(get(row, "year")) or 0) or None,
            "make": (get(row, "make") or "").strip() or None,
            "model": (get(row, "model") or "").strip() or None,
            "trim": (get(row, "trim") or "").strip() or None,
            "mileage": int(norm_num(get(row, "mileage")) or 0) or None,
            "equity": norm_num(get(row, "equity")),
            "lease_end": norm_date(get(row, "lease_end")),
            "service_appt": norm_date(get(row, "service_appt")),
            "sold_date": norm_date(get(row, "sold_date")),
            "interest": (get(row, "interest") or "").strip() or None,
            "notes": (get(row, "notes") or "").strip() or None,
        }

        cur = conn.execute(
            "SELECT id FROM contacts WHERE name=? AND IFNULL(phone,'')=IFNULL(?,'')",
            (rec["name"], rec["phone"]),
        ).fetchone()

        if cur:
            # Update only fields that arrived non-empty; never blank out history.
            sets, vals = [], []
            for k, v in rec.items():
                if k == "name" or v in (None, "", "unknown"):
                    continue
                sets.append(f"{k}=?")
                vals.append(v)
            if sets:
                sets.append("updated=?")
                vals.extend([now_iso(), cur["id"]])
                conn.execute(f"UPDATE contacts SET {', '.join(sets)} WHERE id=?", vals)
                updated_n += 1
        else:
            rec["created"] = rec["updated"] = now_iso()
            cols = ", ".join(rec)
            qs = ", ".join("?" * len(rec))
            conn.execute(f"INSERT INTO contacts ({cols}) VALUES ({qs})",
                         list(rec.values()))
            added += 1

    conn.commit()

    print(f"Imported {path}")
    print(f"  {added} new · {updated_n} updated · {skipped} skipped (no name)")
    print(f"  mapped: {', '.join(sorted(mapping))}")
    unmapped = [h for h in rows[0] if h and h not in mapping.values()
                and not BANNED.search(h)]
    if unmapped:
        print(f"  ignored columns: {', '.join(sorted(unmapped)[:12])}")
    if all_dropped:
        print(f"  REFUSED (sensitive): {', '.join(sorted(all_dropped))}")


# --------------------------------------------------------------------------
# Ranking
# --------------------------------------------------------------------------

def days_until(iso):
    if not iso:
        return None
    try:
        return (date.fromisoformat(iso) - today()).days
    except ValueError:
        return None


def last_touch(conn, cid):
    r = conn.execute(
        "SELECT ts FROM touches WHERE contact_id=? ORDER BY ts DESC LIMIT 1", (cid,)
    ).fetchone()
    return r["ts"] if r else None


def days_since_touch(conn, cid):
    ts = last_touch(conn, cid)
    if not ts:
        return None
    try:
        return (today() - datetime.fromisoformat(ts).date()).days
    except ValueError:
        return None


def score(conn, c):
    """Return (tier, score, reason) — lower tier is more urgent."""
    eq = c["equity"] or 0
    svc = days_until(c["service_appt"])
    lease = days_until(c["lease_end"])
    sold = c["sold_date"]
    since = days_since_touch(conn, c["id"])

    # Tier 1 — positive equity AND in the service lane within a week
    if eq > 0 and svc is not None and 0 <= svc <= 7:
        return (1, 1000 + eq / 100,
                f"${eq:,.0f} equity · service {c['service_appt']}")

    # Tier 2 — lease maturing inside the working window
    if lease is not None and 0 <= lease <= 120:
        return (2, 900 - lease, f"lease ends {c['lease_end']} ({lease}d)")

    # Tier 3 — in the service lane this week, equity unknown or flat
    if svc is not None and 0 <= svc <= 7:
        return (3, 800 - svc, f"service {c['service_appt']}")

    # Tier 4 — positive equity, no scheduled reason to talk
    if eq > 0:
        return (4, 700 + eq / 100, f"${eq:,.0f} equity")

    # Tier 5 — sold-customer anniversary touches
    if sold:
        d = days_until(sold)
        if d is not None:
            age = -d
            for target, label in ((30, "30-day"), (90, "90-day"), (365, "1-year")):
                if target - 7 <= age <= target + 7:
                    return (5, 600, f"{label} follow-up (sold {sold})")

    # Tier 6 — gone quiet
    if since is not None and since >= 60:
        return (6, 500 - min(since, 400), f"no contact in {since} days")
    if since is None and c["status"] == "active":
        return (6, 400, "never contacted")

    return (9, 0, "")


def fmt_contact(c, reason, conn):
    veh = " ".join(str(x) for x in (c["year"], c["make"], c["model"], c["trim"]) if x)
    bits = [f"  {c['name']}"]
    if veh:
        bits.append(f"    {veh}" + (f" · {c['mileage']:,} mi" if c["mileage"] else ""))
    bits.append(f"    {reason}")
    consent = c["consent"] or "unknown"
    if consent == "yes":
        bits.append("    consent: YES — text or call")
    elif consent == "no":
        bits.append("    consent: NO — do not text. Call only.")
    else:
        bits.append("    consent: UNKNOWN — call, do not text")
    if c["phone"]:
        p = c["phone"]
        bits.append(f"    {p[:3]}-{p[3:6]}-{p[6:]}" if len(p) == 10 else f"    {p}")
    return "\n".join(bits)


def cmd_brief(args):
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM contacts WHERE status != 'lost'"
    ).fetchall()

    scored = []
    for c in rows:
        tier, sc, reason = score(conn, c)
        if tier <= 6:
            scored.append((tier, -sc, c, reason))
    scored.sort(key=lambda x: (x[0], x[1]))

    limit = args.limit
    shown = scored[:limit]

    TIERS = {
        1: "IN THE SERVICE LANE WITH EQUITY — best opportunity in the building",
        2: "LEASE MATURING — a deadline exists whether you call or not",
        3: "IN THE SERVICE LANE THIS WEEK",
        4: "POSITIVE EQUITY — no scheduled reason to talk, so write a good opener",
        5: "SOLD-CUSTOMER ANNIVERSARY — referral and repeat engine",
        6: "GONE QUIET — confirm consent before any text",
    }

    d = today()
    print(f"\n{'='*66}")
    print(f"  DAILY BRIEF — {d.strftime('%A, %B')} {d.day}, {d.year}")
    print(f"{'='*66}")

    if not shown:
        print("\n  Nothing ranked. Import a CRM export first:")
        print("    python3 tools/book.py import <export.csv>\n")
        return

    current = None
    for tier, _, c, reason in shown:
        if tier != current:
            current = tier
            print(f"\n── {TIERS[tier]}\n")
        print(fmt_contact(c, reason, conn))
        print()

    if len(scored) > limit:
        print(f"  … {len(scored) - limit} more ranked below the cut. "
              f"Use --limit to see further.\n")

    print("  TODAY'S THREE")
    print("  [ ] Respond to every new lead in under 5 minutes.")
    print("  [ ] Send 3 personalized videos.")
    print("  [ ] Ask 1 delivered customer for a review that names you.\n")


def cmd_due(args):
    """Follow-up cadence: who has gone too long without a touch."""
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM contacts WHERE status='active'"
    ).fetchall()
    out = []
    for c in rows:
        since = days_since_touch(conn, c["id"])
        if since is None or since >= args.days:
            out.append((since if since is not None else 9999, c))
    out.sort(key=lambda x: -x[0])
    print(f"\n  {len(out)} contacts with no touch in {args.days}+ days\n")
    for since, c in out[:args.limit]:
        label = "never" if since == 9999 else f"{since}d ago"
        print(f"  [{c['id']:>4}] {c['name']:<28} last: {label:<10} "
              f"consent: {c['consent']}")
    print()


def cmd_log(args):
    conn = connect()
    c = conn.execute("SELECT * FROM contacts WHERE id=?", (args.id,)).fetchone()
    if not c:
        sys.exit(f"No contact with id {args.id}")
    conn.execute(
        "INSERT INTO touches (contact_id, ts, channel, direction, note) "
        "VALUES (?,?,?,?,?)",
        (args.id, now_iso(), args.channel, args.direction, args.note),
    )
    conn.commit()
    print(f"Logged {args.channel} to {c['name']}.")


def cmd_lead(args):
    """Record a lead arriving, or stamp your response — this is how response
    time gets measured, and response time is the whole ballgame."""
    conn = connect()
    if args.respond:
        r = conn.execute(
            "SELECT l.id, l.received_at, c.name FROM leads l "
            "JOIN contacts c ON c.id=l.contact_id "
            "WHERE l.contact_id=? AND l.responded_at IS NULL "
            "ORDER BY l.received_at DESC LIMIT 1", (args.id,)
        ).fetchone()
        if not r:
            sys.exit("No open lead for that contact.")
        conn.execute("UPDATE leads SET responded_at=? WHERE id=?",
                     (now_iso(), r["id"]))
        conn.commit()
        mins = (datetime.now()
                - datetime.fromisoformat(r["received_at"])).total_seconds() / 60
        verdict = "under 5 — good" if mins <= 5 else "over 5 — tighten it up"
        print(f"Response to {r['name']}: {mins:.1f} min ({verdict})")
    else:
        conn.execute(
            "INSERT INTO leads (contact_id, received_at, source) VALUES (?,?,?)",
            (args.id, now_iso(), args.source),
        )
        conn.commit()
        print(f"Lead logged. Respond, then: book.py lead {args.id} --respond")


def cmd_stats(args):
    conn = connect()
    n = conn.execute("SELECT COUNT(*) c FROM contacts").fetchone()["c"]
    eq = conn.execute(
        "SELECT COUNT(*) c FROM contacts WHERE equity > 0").fetchone()["c"]
    lease = conn.execute(
        "SELECT COUNT(*) c FROM contacts WHERE lease_end IS NOT NULL "
        "AND lease_end <= date('now','+120 day') AND lease_end >= date('now')"
    ).fetchone()["c"]
    consent = dict(conn.execute(
        "SELECT consent, COUNT(*) FROM contacts GROUP BY consent").fetchall())

    since = (datetime.now() - timedelta(days=args.days)).isoformat(" ")
    touches = conn.execute(
        "SELECT channel, COUNT(*) c FROM touches WHERE ts >= ? "
        "GROUP BY channel ORDER BY c DESC", (since,)).fetchall()

    resp = conn.execute(
        "SELECT received_at, responded_at FROM leads "
        "WHERE responded_at IS NOT NULL AND received_at >= ?", (since,)).fetchall()
    times = []
    for r in resp:
        try:
            times.append((datetime.fromisoformat(r["responded_at"])
                          - datetime.fromisoformat(r["received_at"])).total_seconds() / 60)
        except ValueError:
            pass

    print(f"\n  BOOK — {n} contacts")
    print(f"    positive equity        {eq}")
    print(f"    lease maturing <120d   {lease}")
    print(f"    consent yes/no/unknown "
          f"{consent.get('yes',0)}/{consent.get('no',0)}/{consent.get('unknown',0)}")

    print(f"\n  LAST {args.days} DAYS")
    if touches:
        for t in touches:
            print(f"    {t['channel']:<12} {t['c']}")
    else:
        print("    no touches logged")

    if times:
        times.sort()
        med = times[len(times)//2]
        under5 = sum(1 for t in times if t <= 5)
        noun = "lead" if len(times) == 1 else "leads"
        print(f"\n  RESPONSE TIME ({len(times)} {noun})")
        print(f"    median                 {med:.1f} min")
        print(f"    under 5 min            {under5}/{len(times)} "
              f"({100*under5/len(times):.0f}%)")
        print(f"    industry median is 47 min. Leads answered inside 5 minutes")
        print(f"    close at 25-32%; after an hour, 3-5%.")
    else:
        print(f"\n  RESPONSE TIME — nothing logged yet.")
        print(f"    Log a lead:     book.py lead <id>")
        print(f"    Stamp reply:    book.py lead <id> --respond")
    print()


def cmd_find(args):
    conn = connect()
    q = f"%{args.query}%"
    rows = conn.execute(
        "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? "
        "OR model LIKE ? ORDER BY name LIMIT ?",
        (q, q, q, q, args.limit)).fetchall()
    if not rows:
        print("  No match.")
        return
    print()
    for c in rows:
        veh = " ".join(str(x) for x in (c["year"], c["make"], c["model"]) if x)
        since = days_since_touch(conn, c["id"])
        last = "never" if since is None else f"{since}d ago"
        print(f"  [{c['id']:>4}] {c['name']:<26} {veh:<22} "
              f"consent:{c['consent']:<8} last:{last}")
    print()


def main():
    p = argparse.ArgumentParser(
        prog="book.py", description="Holden's book of business.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("import", help="ingest a CRM export (CSV/TSV)")
    s.add_argument("file")
    s.set_defaults(func=cmd_import)

    s = sub.add_parser("brief", help="today's ranked action list")
    s.add_argument("--limit", type=int, default=12)
    s.set_defaults(func=cmd_brief)

    s = sub.add_parser("due", help="who has gone too long without a touch")
    s.add_argument("--days", type=int, default=30)
    s.add_argument("--limit", type=int, default=40)
    s.set_defaults(func=cmd_due)

    s = sub.add_parser("log", help="record a touch")
    s.add_argument("id", type=int)
    s.add_argument("channel",
                   choices=["call", "text", "email", "video", "in-person"])
    s.add_argument("--direction", default="out", choices=["out", "in"])
    s.add_argument("--note", default=None)
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("lead", help="log a lead arriving / stamp your response")
    s.add_argument("id", type=int)
    s.add_argument("--respond", action="store_true")
    s.add_argument("--source", default=None)
    s.set_defaults(func=cmd_lead)

    s = sub.add_parser("stats", help="pipeline and response-time numbers")
    s.add_argument("--days", type=int, default=14)
    s.set_defaults(func=cmd_stats)

    s = sub.add_parser("find", help="look someone up")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_find)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Piping into head/more closes stdout early. Exit quietly.
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
