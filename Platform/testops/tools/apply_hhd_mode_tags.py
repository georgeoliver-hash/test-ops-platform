"""Append a MODE-* tag to every case's Refs field in suite 30285 (HHD, project 42).

Tag scheme (agreed with George, 2026-07-27):
  MODE-BOTH            shared case where the outcome could plausibly differ by mode
                        (fare/ticket/product/entitlement/config-driven), even if steps identical.
  MODE-NIRRAIL-ONLY    already mode-specific to NIR-Rail.
  MODE-GLIDER-ONLY     already mode-specific to Glider (Metro/Ulsterbus).
  MODE-PRIMARY-ONLY    shared AND genuinely mode-irrelevant (Sign On, most Non-Functional,
                        general device/hardware mechanics) - only needs running once.

The ID -> tag map lives in a sibling file (hhd_mode_tags.py) built from a full-body read of every
live case in the suite cross-checked against proposals/hhd-suite-restructure/structure.md. Every
one of the 335 live cases is covered exactly once (verified before this script is ever run).

APPENDS to the existing Refs value (never overwrites) via the guarded, suite-locked
`update_case_fields` writer - so REQ-####/FBD-#####/TIBU-#### citations already on a case are
preserved.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=30285
  python tools/apply_hhd_mode_tags.py [--sample N] [--commit]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from system_test_ops.testrail.client import TestRailClient  # noqa: E402
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id, TestRailWriteError  # noqa: E402
from hhd_mode_tags import TAG_MAP  # noqa: E402

PROJECT_ID = 42
SUITE_ID = 30285
VALID_TAGS = {"MODE-BOTH", "MODE-NIRRAIL-ONLY", "MODE-GLIDER-ONLY", "MODE-PRIMARY-ONLY"}
REFS_MAX_LEN = 250


def append_ref(existing: str | None, tag: str) -> str:
    parts = [p.strip() for p in (existing or "").split(",") if p.strip()]
    if any(p.upper() == tag.upper() for p in parts):
        return ",".join(parts)  # already present, no-op
    parts.append(tag)
    return ",".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="only process the first N cases (dry-run sanity check)")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    suite = load_write_suite_id()
    if suite != SUITE_ID:
        print(f"error: TESTRAIL_WRITE_SUITE_ID must be {SUITE_ID}, got {suite}", file=sys.stderr)
        return 2

    client = TestRailClient()
    writer = TestRailWriter(client, PROJECT_ID, suite, commit=args.commit)

    cases = client.get_cases(PROJECT_ID, suite)
    by_id = {int(c["id"]): c for c in cases}

    missing = [cid for cid in TAG_MAP if cid not in by_id]
    unmapped_live = [
        int(c["id"]) for c in cases
        if not (c.get("title") or "").upper().startswith("ZZ_DELETE") and int(c["id"]) not in TAG_MAP
    ]
    if missing:
        print(f"error: {len(missing)} mapped ids not found in suite: {missing[:10]}...", file=sys.stderr)
        return 2
    if unmapped_live:
        print(f"error: {len(unmapped_live)} live cases have no tag mapping: {unmapped_live[:10]}...", file=sys.stderr)
        return 2

    items = list(TAG_MAP.items())
    if args.sample:
        items = items[: args.sample]

    print(f"[{'COMMIT' if args.commit else 'DRY-RUN'}] tagging {len(items)} cases in suite {suite}")
    counts: dict[str, int] = {t: 0 for t in VALID_TAGS}
    skipped = updated = 0
    overflow: list[tuple[int, str, int]] = []
    for cid, tag in items:
        assert tag in VALID_TAGS, f"bad tag {tag} for C{cid}"
        case = by_id[cid]
        new_refs = append_ref(case.get("refs"), tag)
        if new_refs == (case.get("refs") or "").strip():
            skipped += 1
            continue
        if len(new_refs) > REFS_MAX_LEN:
            overflow.append((cid, tag, len(new_refs)))
            print(f"  SKIP (refs too long: {len(new_refs)} > {REFS_MAX_LEN}) C{cid}: {tag}")
            continue
        try:
            writer.update_case_fields(cid, {"refs": new_refs}, section_id=case.get("section_id"))
        except TestRailWriteError as exc:
            overflow.append((cid, tag, len(new_refs)))
            print(f"  SKIP (write rejected: {exc}) C{cid}: {tag}")
            continue
        updated += 1
        counts[tag] += 1
        if not args.commit:
            print(f"  C{cid}: {tag}  refs -> {new_refs!r}")

    print(f"  updated: {updated}  already-tagged/skipped: {skipped}  overflow-flagged: {len(overflow)}")
    print(f"  by tag: {counts}")
    if overflow:
        print(f"  OVERFLOW cases (refs field would exceed {REFS_MAX_LEN} chars - not written, flagged for review):")
        for cid, tag, length in overflow:
            print(f"    C{cid}: {tag}  (would be {length} chars)")
    if not args.commit:
        print("  (dry-run - pass --commit to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
