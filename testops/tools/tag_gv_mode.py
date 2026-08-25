"""Append MODE-* direction tags to every case's `refs` field in GV suite 30286.

Classification is grounded in the live suite content (pulled fresh) + the direction-split logic
in proposals/gv-suite-restructure/structure.md. See proposals/gv-suite-restructure/mode-coverage.md
for the full per-case rationale. This script only APPENDS to refs (never overwrites existing refs)
and is suite-locked via TestRailWriter to the suite in TESTRAIL_WRITE_SUITE_ID.

Usage:
  $env:TESTRAIL_WRITE_SUITE_ID="30286"
  .venv\\Scripts\\python.exe tools/tag_gv_mode.py --sample     # dry-run, first 5 only, prints diff
  .venv\\Scripts\\python.exe tools/tag_gv_mode.py --dry-run    # dry-run, all cases
  .venv\\Scripts\\python.exe tools/tag_gv_mode.py --commit     # real writes
"""
from __future__ import annotations
import argparse
import sys

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id

PROJECT = 42
SUITE = 30286

# Cases explicitly excluded from mode tagging (slated for deletion, not part of the live suite).
EXCLUDED = {4104038}

# id -> list of MODE-* tags to append (in the order they should be added).
TAGS: dict[int, list[str]] = {}


def _all(ids, tag):
    for i in ids:
        TAGS.setdefault(i, []).append(tag)


# ---- Functional / ABT cEMV Taps ----
# Direction-explicit cases (named in title / structure.md's deny-list-exception + tap-classification split)
TAGS[4104017] = ["MODE-ENTRY-ONLY"]   # "...is rejected in entry mode..."
TAGS[4104026] = ["MODE-ENTRY-ONLY"]   # "an entry-configured gate audits the tap as a Tap On"
TAGS[4104027] = ["MODE-EXIT-ONLY"]    # "an exit-configured gate audits the tap as a Tap Off"
# deny-list exception: structure.md names it "Exit / bi-directional" -> applies to every config
# that has an exit-capable direction (Exit, and both Bi-di configs), not Entry.
TAGS[4104025] = ["MODE-EXIT-ONLY", "MODE-BIDI-AB-ONLY", "MODE-BIDI-BA-ONLY"]

_ABT_ALL = [
    4104011, 4104012, 4104013, 4104014, 4104015, 4104016, 4104018, 4104019,
    4104020, 4104021, 4104022, 4104023, 4104024,
    4104418, 4104419, 4104420,
]
_all(_ABT_ALL, "MODE-ALL")

# ---- Functional / Multi-Use Barcode Validation (+ Passback) ----
_BARCODE_PASSBACK_ALL = [
    4104028, 4104029, 4104030, 4104031, 4104032, 4104033, 4104034, 4104035,
    4104036, 4104037, 4104039, 4104040, 4104041, 4104042, 4104043, 4104044,
    4104045, 4104046, 4104047,
    4104421, 4104422, 4104423, 4104424, 4104425, 4104426, 4104427, 4104428,
    4104429, 4104430, 4104431,
    4104048, 4104049, 4104050, 4104051, 4104052,
]
_all(_BARCODE_PASSBACK_ALL, "MODE-ALL")

# ---- Functional / Commissioning & Router (field procedure, direction-irrelevant) ----
_COMMISSIONING_PRIMARY = list(range(4104053, 4104064))  # 4104053..4104063
_all(_COMMISSIONING_PRIMARY, "MODE-PRIMARY-ONLY")

# ---- Functional / Technician Menu (direction-irrelevant) ----
_TECH_MENU_PRIMARY = list(range(4104064, 4104076))  # 4104064..4104075
_all(_TECH_MENU_PRIMARY, "MODE-PRIMARY-ONLY")

# ---- Non-Functional / HMI Screens (screen wording is direction-irrelevant) ----
_HMI_PRIMARY = list(range(4104076, 4104091)) + [4104111, 4104112]  # 4104076..4104090, +111,112
_all(_HMI_PRIMARY, "MODE-PRIMARY-ONLY")

# ---- Non-Functional / Resilience ----
_RESILIENCE_ALL = [4104091, 4104093, 4104101]           # gate-arm / ERB / throughput -> gate-movement relevant
_RESILIENCE_PRIMARY = [4104092, 4104094, 4104095, 4104096, 4104097, 4104098, 4104099, 4104100]
_all(_RESILIENCE_ALL, "MODE-ALL")
_all(_RESILIENCE_PRIMARY, "MODE-PRIMARY-ONLY")

# ---- Smoke ----
_SMOKE_ALL = [4104103, 4104104, 4104105]
_SMOKE_PRIMARY = [4104102, 4104106]
_all(_SMOKE_ALL, "MODE-ALL")
_all(_SMOKE_PRIMARY, "MODE-PRIMARY-ONLY")


def compute_new_refs(existing_refs: str | None, new_tags: list[str]) -> str | None:
    """Append new_tags to the existing comma-separated refs string, de-duplicated. None if no change."""
    existing = [r.strip() for r in (existing_refs or "").split(",") if r.strip()]
    to_add = [t for t in new_tags if t not in existing]
    if not to_add:
        return None
    return ", ".join(existing + to_add)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sample", action="store_true", help="dry-run, print first 5 planned changes only")
    a = ap.parse_args()

    commit = bool(a.commit)
    suite = load_write_suite_id()
    if commit and suite != SUITE:
        print(f"error: TESTRAIL_WRITE_SUITE_ID={suite!r}, expected {SUITE}", file=sys.stderr)
        return 2

    client = TestRailClient()
    cases = client.get_cases(PROJECT, SUITE)
    by_id = {int(c["id"]): c for c in cases}

    writer = TestRailWriter(client, PROJECT, SUITE, commit=commit)

    planned = []
    for cid, tags in TAGS.items():
        if cid in EXCLUDED:
            continue
        cse = by_id.get(cid)
        if not cse:
            print(f"  MISSING C{cid} (not found in live suite)", file=sys.stderr)
            continue
        new_refs = compute_new_refs(cse.get("refs"), tags)
        if new_refs is None:
            continue  # already tagged
        planned.append((cid, cse.get("title"), cse.get("refs"), new_refs, cse.get("section_id")))

    # sanity: every non-excluded live case should have a tag plan (or already be tagged)
    untagged = [cid for cid in by_id if cid not in TAGS and cid not in EXCLUDED]
    if untagged:
        print(f"WARNING: {len(untagged)} live case(s) have no classification: {untagged}", file=sys.stderr)

    if a.sample:
        planned = planned[:5]

    print(f"[{'COMMIT' if commit else 'DRY-RUN'}] {len(planned)} case(s) to update (of {len(TAGS)} classified, {len(by_id)} live)")
    for cid, title, old, new, section_id in planned:
        print(f"  C{cid} | {title}")
        print(f"      refs: {old!r} -> {new!r}")
        writer.update_case_fields(cid, {"refs": new}, section_id=section_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
