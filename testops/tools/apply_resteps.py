"""Apply multi-step re-authoring to existing cases, in place, by case id.

Reads one or more restep JSON files (each an array of {id, preconds, steps:[{content,expected}]})
and updates ONLY custom_preconds + custom_steps_seperated on each case, via the guarded
suite-locked writer. Leaves title/objective/expected/enrichment tags untouched.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=<suite id>
  python tools/apply_resteps.py <restep.json> [<restep2.json> ...] [--commit]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--project", type=int, default=42)
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    suite = load_write_suite_id()
    if suite is None:
        print("error: TESTRAIL_WRITE_SUITE_ID not set", file=sys.stderr)
        return 2

    client = TestRailClient()
    writer = TestRailWriter(client, args.project, suite, commit=args.commit)
    mode = "COMMIT" if args.commit else "DRY-RUN"
    print(f"[{mode}] apply resteps -> project {args.project}, write suite {suite}")

    # Build id->section_id map for the write suite so we can verify each case belongs to it.
    by_id = {int(c["id"]): c for c in client.get_cases(args.project, suite)}

    total = updated = skipped = missing = 0
    for fp in args.files:
        data = json.loads(Path(fp).read_text(encoding="utf-8"))
        for rec in data:
            total += 1
            cid = int(rec["id"])
            existing = by_id.get(cid)
            if not existing:
                missing += 1
                print(f"  MISSING C{cid} (not in write suite {suite}) — skipped")
                continue
            # Never rewrite cases already marked for deletion — they will be binned in the UI.
            if "ZZ_DELETE" in (existing.get("title") or "").upper():
                skipped += 1
                continue
            steps = rec.get("steps") or []
            if not steps:
                skipped += 1
                continue
            extra = {"custom_steps_seperated": steps}
            if rec.get("preconds"):
                extra["custom_preconds"] = rec["preconds"]
            writer.update_case_fields(cid, extra, section_id=existing.get("section_id"))
            updated += 1
    print(f"  cases: {total}  updated: {updated}  skipped(no-steps): {skipped}  missing: {missing}")
    if not args.commit:
        print("  (dry-run — re-run with --commit to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
