"""Recovery for the consolidation bin step.

A PowerShell heredoc mangled the em-dash when generating consolidate-bin-2.cases.yaml, so the title
`match` missed and the push CREATED 30 junk duplicate ZZ cases instead of renaming the originals.
This file-based script (clean UTF-8 — no heredoc) fixes it:
  1. Re-label the 30 junk duplicates (ZZ_DELETE_REVIEW ... "(folded)") as ZZ_DELETE_DUP.
  2. Properly retire the 30 original active cases -> ZZ_DELETE_REVIEW ... (folded).
Idempotent-ish: step 2 skips a title already renamed/missing.
"""
from __future__ import annotations

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

ORIGINALS = [
    "FLU — change boarding stage manually",
    "FLU — journey type toggle",
    "FLU — preset and menu-type products",
    "FLU — selection times out to the default product",
    "FLU — last transaction display and success timeout",
    "FLU — default ticket class reverts on timeout",
    "FLU — Easibus product menu",
    "Ticket Issue — annulment times out",
    "Ticket Issue — annulment refused for non-annullable transactions",
    "Ticket Issue — issue with a change receipt",
    "Promo Menu — add an additional child to a family product",
    "Promo Menu — basket tracker persists in sub-menus",
    "Basket Mode — change line-item quantity",
    "Smartcard — direction and transfer-period rules",
    "Smartcard top-up — maximum journeys enforced",
    "Smartcard top-up — expired journeys removed",
    "ABT — passback on second tap",
    "ABT — mobile wallet taps",
    "ABT — EMV validation failure variants",
    "Driver options — messages",
    "Driver options — Word and Colour of the Day",
    "Driver options — paper status",
    "Driver options — ticket history and last ticket",
    "Driver options — reboot card reader",
    "Driver options — report faulty reader",
    "Supervisor — GPS information",
    "Technician — view and print versions",
    "Barcode — online validation failures",
    "GPS — arrival and departure at stops",
    "GPS — look ahead",
]


def main() -> int:
    client = TestRailClient()
    writer = TestRailWriter(client, 42, 30254, commit=True)
    cases = client.get_cases(42, 30254)

    # Step 1: junk duplicates = ZZ_DELETE_REVIEW cases ending "(folded)" (the proper retirements
    # below have not been created yet, so right now these are only the 30 mangled dups).
    junk = [c for c in cases
            if str(c.get("title", "")).startswith("ZZ_DELETE_REVIEW")
            and str(c.get("title", "")).endswith("(folded)")]
    print(f"Step 1 — re-labelling {len(junk)} junk duplicate(s) as ZZ_DELETE_DUP")
    for c in junk:
        cid = int(c["id"])
        writer.update_case_fields(cid, {"title": f"ZZ_DELETE_DUP (created in error) - C{cid}"},
                                  section_id=c.get("section_id"))

    # Step 2: retire the 30 originals by exact (clean) title.
    print(f"Step 2 — retiring {len(ORIGINALS)} original cases as ZZ_DELETE_REVIEW")
    missing = []
    for t in ORIGINALS:
        res = writer.update_case(t, new_title=f"ZZ_DELETE_REVIEW - {t} (folded)")
        if res.get("missing"):
            missing.append(t)
        else:
            print(f"  retired: {t}")
    if missing:
        print("\nNOT FOUND (check title):")
        for t in missing:
            print(f"  - {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
