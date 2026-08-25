"""Tag every live case in the NEW TVM suite (30284) with a MODE-* Refs tag.

Four tags (per George's mode-execution tagging scheme, 2026-07-27):
  MODE-ALL            shared case, outcome could plausibly differ by mode (fare/ticket/product/
                       rail-vs-bus-vs-glider config-driven) -> run once per relevant mode config.
  MODE-NIRRAIL-ONLY   genuinely NIR-Rail-specific (rail/cross-border products, NIR legacy stages).
  MODE-ULSTERBUS-ONLY / MODE-METRO-ONLY / MODE-GLIDER-ONLY   genuinely specific to that one mode.
  MODE-PRIMARY-ONLY   shared AND mode-irrelevant (EMS/alarmboard/commissioning mechanics, cash-
                       hardware/BNR mechanics, most non-functional, generic UI/menu). Run once.

Classification is rule-based on section path + title, grounded in the case content read during
the audit pass (proposals/tvm-suite-restructure/*.cases.yaml + live suite dump). ZZ_DELETE_REVIEW
cases are excluded (pending deletion, not live coverage).

Usage:
  python tools/tag_tvm_modes.py --dry-run            # sample / full dry-run, no writes
  python tools/tag_tvm_modes.py --commit             # actually append the tag via update_case_fields
"""
from __future__ import annotations

import argparse
from collections import Counter

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

PROJECT_ID = 42
SUITE_ID = 30284

MODE_ALL = "MODE-ALL"
MODE_NIRRAIL = "MODE-NIRRAIL-ONLY"
MODE_ULSTERBUS = "MODE-ULSTERBUS-ONLY"
MODE_METRO = "MODE-METRO-ONLY"
MODE_GLIDER = "MODE-GLIDER-ONLY"
MODE_PRIMARY = "MODE-PRIMARY-ONLY"


def build_section_paths(sections: list[dict]) -> dict[int, str]:
    by_id = {s["id"]: s for s in sections}

    def path(sid: int) -> str:
        s = by_id[sid]
        parent = s.get("parent_id")
        prefix = path(parent) + " / " if parent else ""
        return prefix + s["name"]

    return {sid: path(sid) for sid in by_id}


# Section-path -> default tag (checked by exact path OR path-prefix, most specific first).
SECTION_DEFAULT = [
    ("Functional / Sales - Tickets / Rail & Cross-Border (Kiosk)", MODE_NIRRAIL),
    ("Functional / Payments - Cash / Note Recycler & Change (Astreo only)", MODE_PRIMARY),
    ("Functional / Payments - Cash / Note Recycler & Change (Kiosk only)", MODE_PRIMARY),
    ("Functional / Payments - Cash / Coin Recycler Hopper (Kiosk only)", MODE_PRIMARY),
    ("Functional / Payments - Cash", MODE_PRIMARY),  # exact (children handled above)
    ("Functional / Payments - EMV & Contactless", MODE_PRIMARY),
    ("Functional / Commissioning & Deployment", MODE_PRIMARY),
    ("Functional / Sales - Tickets / Ticket Issue", MODE_ALL),
    ("Functional / Sales - Tickets / Advance & 3-Day", MODE_ALL),
    ("Functional / Sales - Tickets / Basket", MODE_ALL),
    ("Functional / Sales - Tickets / Grouped Stops", MODE_ALL),
    ("Functional / Sales - Tickets / Ticket Collection", MODE_PRIMARY),
    ("Functional / Sales - Tickets / Ticket Numbering", MODE_PRIMARY),
    ("Functional / Barcode Redemption", None),  # case-by-case below
    ("Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only", MODE_PRIMARY),
    ("Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only", MODE_PRIMARY),
    ("Non-Functional / EMS & TMS Maintenance", MODE_PRIMARY),  # exact
    ("Non-Functional / Resilience", MODE_PRIMARY),
    ("Smoke", MODE_ALL),
]

# Title substrings -> override tag, checked case-insensitively, most specific wins.
TITLE_OVERRIDES: list[tuple[str, str]] = [
    # Commissioning & Deployment / EMS Maintenance: product-catalog-by-location is mode-driven.
    ("topology makes home-location products sellable", MODE_ALL),
    ("changing location changes sellable products", MODE_ALL),
    ("configuration topology — home location sets the selling operator", MODE_ALL),
    ("configuration topology — destination outside triangle unavailable", MODE_ALL),
    # Ticket Issue exceptions
    ("buy a product in a different language", MODE_PRIMARY),
    ("the sale posts an audit record to the back office", MODE_PRIMARY),
    ("cross border, family & friends and concession rail products print a multi-use barcode", MODE_NIRRAIL),
    # Resilience — Multi-Modal Home
    ("multi-modal home — selecting bus shows the bus home", MODE_ALL),
    ("multi-modal home — selecting rail shows the rail home", MODE_NIRRAIL),
    # Barcode Redemption — case-by-case (section default is None, so every case here needs a hit)
    ("ticket collection — a valid booking reference collects and prints the pre-paid ticket", MODE_ALL),
    ("ticket collection — the booking reference is validated against the back office", MODE_PRIMARY),
    ("ticket collection — a successful redemption emits a barcode redemption event", MODE_PRIMARY),
    ("ticket collection — an offline redemption still prints and queues an offline event", MODE_PRIMARY),
    ("ticket collection — a redemption above the barcode ceiling limit cannot validate offline", MODE_PRIMARY),
    ("ticket collection — a redemption below the barcode ceiling limit validates offline", MODE_PRIMARY),
    ("booking reference — an invalid booking reference is rejected", MODE_PRIMARY),
    ("booking reference — a malformed reference entry is rejected before submission", MODE_PRIMARY),
    ("ticket collection — a collection against a legacy stage resolves the legacy stage name", MODE_NIRRAIL),
    ("single-use only — a multi-use ticket's collect ticket code is rejected", MODE_PRIMARY),
    ("single-use only — collection accepts a booking reference and not a scanned barcode", MODE_PRIMARY),
    ("ticket collection — a business error shows an error screen and returns to home after the timeout", MODE_PRIMARY),
    ("ticket collection — repeated server errors retry and then fall back", MODE_PRIMARY),
    ("ticket collection — an already-redeemed booking reference is rejected as used", MODE_PRIMARY),
    ("barcode ticket format — a collected ticket prints in the barcode ticket layout (cross border)", MODE_NIRRAIL),
    ("barcode ticket format — a collected ticket prints in the barcode ticket layout (3 day select)", MODE_NIRRAIL),
    ("barcode ticket format — a collected ticket prints in the barcode ticket layout", MODE_ALL),
]


def classify(path: str, title: str) -> tuple[str | None, str]:
    """Return (tag, reason). tag is None if unresolved (flag for manual review)."""
    tl = title.lower()
    for substr, tag in TITLE_OVERRIDES:
        if substr in tl:
            return tag, f"title override: {substr!r}"
    # longest-matching section path prefix
    best = None
    for sec_path, tag in SECTION_DEFAULT:
        if path == sec_path or path.startswith(sec_path + " / "):
            if best is None or len(sec_path) > len(best[0]):
                best = (sec_path, tag)
    if best and best[1] is not None:
        return best[1], f"section default: {best[0]!r}"
    return None, "UNRESOLVED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true", help="Actually write refs (default dry-run)")
    ap.add_argument("--sample", type=int, default=0, help="Only process first N classified cases (dry-run sanity)")
    args = ap.parse_args()

    client = TestRailClient()
    cases = client.get_cases(PROJECT_ID, SUITE_ID)
    sections = client.get_sections(PROJECT_ID, SUITE_ID)
    paths = build_section_paths(sections)

    tally: Counter[str] = Counter()
    unresolved: list[tuple[int, str, str]] = []
    excluded_delete = 0
    plan: list[tuple[dict, str]] = []

    for c in cases:
        title = c["title"]
        if title.startswith("ZZ_DELETE_REVIEW"):
            excluded_delete += 1
            continue
        path = paths[c["section_id"]]
        tag, reason = classify(path, title)
        if tag is None:
            unresolved.append((c["id"], path, title))
            continue
        tally[tag] += 1
        plan.append((c, tag))

    print(f"Total live cases considered: {len(cases) - excluded_delete} (excluded {excluded_delete} ZZ_DELETE_REVIEW)")
    print("Tally per tag:")
    for tag, n in tally.most_common():
        print(f"  {tag}: {n}")
    if unresolved:
        print(f"\nUNRESOLVED ({len(unresolved)}) — needs manual classification:")
        for cid, path, title in unresolved:
            print(f"  C{cid}  [{path}]  {title}")

    if args.sample:
        plan = plan[: args.sample]
        print(f"\n--sample: limiting to first {len(plan)} cases")

    writer = TestRailWriter(client, PROJECT_ID, SUITE_ID, commit=args.commit)
    applied = 0
    skipped_existing = 0
    for c, tag in plan:
        existing_refs = (c.get("refs") or "").strip()
        existing_list = [r.strip() for r in existing_refs.split(",") if r.strip()] if existing_refs else []
        if tag in existing_list:
            skipped_existing += 1
            continue
        new_refs = ", ".join(existing_list + [tag])
        res = writer.update_case_fields(int(c["id"]), {"refs": new_refs}, section_id=c["section_id"])
        applied += 1
        if applied <= 5 or not args.commit:
            print(f"  C{c['id']}: {existing_refs!r} -> {new_refs!r}  [{res.get('_dry_run', 'COMMITTED')}]")

    print(f"\n{'DRY-RUN — ' if not args.commit else ''}Applied to {applied} cases; {skipped_existing} already tagged.")
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
