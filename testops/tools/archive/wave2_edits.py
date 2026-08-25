"""Wave 2 of George's POS review (review-notes-register.md) — APPEND-ONLY field edits.

Unlike a YAML push (which replaces a whole case body), this reads each live field and appends a
single line only if it is not already present, then does a partial `update_case`. Idempotent and
suite-locked (writes go only to TESTRAIL_WRITE_SUITE_ID).

Categories:
  banner   (#18) append "green success banner" outcome to the last step of every ticket-ISSUE case
  payment  (#6/#7) append a payment data-variation line to top-up + issue cases
                   (Metro products = Cash / Card only; no Warrant)
  child    (#9)  append an Adult / Child passenger-type variation to STANDARD journey tickets only
  concession(#8) enumerate the missing Half-Fare sub-types + DLA on the existing entitlement case

Usage:  python -m tools.wave2_edits [--only banner,payment,child,concession] [--commit]
"""
from __future__ import annotations

import argparse
import sys

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id

PID = 42  # TFTS - System Test

BANNER_AND = "**AND** a green success banner is displayed following the successful ticket issue"
PAY_FULL = " Data variations: payment by Cash / Warrant / Card."
PAY_METRO = " Data variations: payment by Cash / Card (Warrant not available on Metro)."
CHILD_LINE = " Data variations: passenger type (Adult / Child)."
CONCESSION_PREFACE = " Half-Fare sub-types include Partially Sighted, Learning Disability and No Driving Licence; DLA is also an entitlement card."
CONCESSION_AND = "**AND** Half-Fare sub-types (Partially Sighted, Learning Disability, No Driving Licence) and DLA each set the matching ticket type"

# Top-up/issue cases that are negative/utility (no product sale) — payment variation is noise here.
PAY_EXCLUDE = (
    "cancel", "limit", "mini statement", "non-toppable", "expired",
    "recognised by other", "blank card options",
)

# Ticket cases that should NOT get an Adult/Child line (specific products / passenger types).
CHILD_EXCLUDE = (
    "warrant", "jobseeker", "family & friends", "ilink", "dependent", "dependant",
    "rambler", "substitution", "visitor", "cross-border", "season",
)


def section_paths(client: TestRailClient):
    secs = client.get_sections(PID, load_write_suite_id())
    byid = {int(s["id"]): s for s in secs}

    def path(sid):
        s = byid[sid]
        p = s.get("parent_id")
        return (path(int(p)) if p else ()) + (s.get("name", ""),)

    return {int(cid): " / ".join(path(int(cid))) for cid in byid}


def is_metro(title: str, secpath: str) -> bool:
    return "metro" in title.lower() or secpath.startswith("Metro /")


def child_eligible(title: str) -> bool:
    t = title.lower()
    if any(x in t for x in CHILD_EXCLUDE):
        return False
    # standard journey tickets
    return any(x in t for x in ("single", "day return", "return", "day ticket"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="banner,payment,child,concession")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()
    cats = {c.strip() for c in args.only.split(",")}

    from dotenv import load_dotenv
    load_dotenv()
    sid = load_write_suite_id()
    if not sid:
        print("error: TESTRAIL_WRITE_SUITE_ID not set."); return 2
    client = TestRailClient()
    writer = TestRailWriter(client, PID, sid, commit=args.commit)
    paths = section_paths(client)
    cases = {int(c["id"]): c for c in client.get_cases(PID, sid)}
    mode = "COMMIT" if args.commit else "DRY-RUN"
    print(f"[{mode}] Wave 2 edits -> suite {sid}; categories: {sorted(cats)}\n")

    n_edit = n_skip = 0

    def secpath(c):
        return paths.get(int(c["section_id"]), "?")

    # ---- banner (#18): ticket-issue cases ----
    if "banner" in cats:
        print("== #18 green success banner (ticket-issue cases) ==")
        for cid, c in sorted(cases.items()):
            sp = secpath(c)
            if not sp.endswith("/ Tickets"):
                continue
            steps = c.get("custom_steps_seperated") or []
            if not steps:
                continue
            joined = "\n".join((s.get("expected") or "") for s in steps).lower()
            if "green" in joined and "banner" in joined:
                n_skip += 1
                continue
            new_steps = [dict(s) for s in steps]
            last = new_steps[-1]
            last["expected"] = (last.get("expected") or "").rstrip() + "\n" + BANNER_AND
            res = writer.update_case_fields(cid, {"custom_steps_seperated": new_steps}, section_id=c["section_id"])
            n_edit += 1
            print(f"  + C{cid} {c['title'].encode('ascii','replace').decode()[:42]:42} banner {'(would)' if res.get('_dry_run') else 'OK'}")

    # ---- payment (#6/#7): top-up + issue cases ----
    if "payment" in cats:
        print("\n== #6/#7 payment data-variation (top-up + issue) ==")
        for cid, c in sorted(cases.items()):
            sp = secpath(c)
            if "Screen Validation" in sp:  # visual-check cases — never get a payment data line
                continue
            is_topup = sp.endswith("/ Top Up") or sp.endswith("/ Top Up & Validation / Top Up")
            is_issue = sp.endswith("/ Issue from Blank") or sp == "Ulsterbus / Issue Card"
            if not (is_topup or is_issue):
                continue
            if any(x in c["title"].lower() for x in PAY_EXCLUDE):  # negative/utility case
                continue
            exp = c.get("custom_expected") or ""
            low = exp.lower()
            if "payment by" in low or "warrant" in low or "cash / card" in low:
                n_skip += 1
                continue
            line = PAY_METRO if is_metro(c["title"], sp) else PAY_FULL
            res = writer.update_case_fields(cid, {"custom_expected": exp.rstrip() + line}, section_id=c["section_id"])
            n_edit += 1
            tag = "metro" if line is PAY_METRO else "full"
            print(f"  + C{cid} {c['title'].encode('ascii','replace').decode()[:42]:42} pay/{tag} {'(would)' if res.get('_dry_run') else 'OK'}")

    # ---- child (#9): standard journey tickets ----
    if "child" in cats:
        print("\n== #9 Adult/Child passenger-type variation (standard journey tickets) ==")
        skipped_products = []
        for cid, c in sorted(cases.items()):
            sp = secpath(c)
            if not sp.endswith("/ Tickets"):
                continue
            title = c["title"]
            exp = c.get("custom_expected") or ""
            if "child" in exp.lower():
                n_skip += 1
                continue
            if not child_eligible(title):
                skipped_products.append(f"C{cid} {title.encode('ascii','replace').decode()}")
                continue
            res = writer.update_case_fields(cid, {"custom_expected": exp.rstrip() + CHILD_LINE}, section_id=c["section_id"])
            n_edit += 1
            print(f"  + C{cid} {title.encode('ascii','replace').decode()[:42]:42} child {'(would)' if res.get('_dry_run') else 'OK'}")
        if skipped_products:
            print("  -- deliberately NOT given Adult/Child (specific product/passenger type) — confirm:")
            for s in skipped_products:
                print(f"       {s}")

    # ---- concession (#8): enumerate missing variants on C4100427 ----
    if "concession" in cats:
        print("\n== #8 Half-Fare sub-types + DLA on entitlement case C4100427 ==")
        c = cases.get(4100427)
        if not c:
            print("  ! C4100427 not found")
        else:
            pre = c.get("custom_preface") or ""
            steps = c.get("custom_steps_seperated") or []
            if "partially sighted" in (pre + str(steps)).lower():
                print("  = already enumerated; skipping"); n_skip += 1
            else:
                new_pre = pre.rstrip() + CONCESSION_PREFACE
                new_steps = [dict(s) for s in steps]
                if new_steps:
                    new_steps[-1]["expected"] = (new_steps[-1].get("expected") or "").rstrip() + "\n" + CONCESSION_AND
                res = writer.update_case_fields(
                    4100427,
                    {"custom_preface": new_pre, "custom_steps_seperated": new_steps},
                    section_id=c["section_id"],
                )
                n_edit += 1
                print(f"  + C4100427 enumerated Half-Fare sub-types + DLA {'(would)' if res.get('_dry_run') else 'OK'}")

    print(f"\n[{mode}] {n_edit} case(s) to edit, {n_skip} already-compliant (skipped).")
    if not args.commit:
        print("Dry-run only. Re-run with --commit to apply, then audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
