"""Generic pusher for a `*.new-cases.json` file of {section_id, title, preface, preconds, steps,
expected, refs, priority_id, custom_devtypes} rows, straight into an already-existing section_id
(no new sections needed — these are just more cases in existing folders). Suite-locked via
TestRailWriter/TESTRAIL_WRITE_SUITE_ID. Dry-run by default.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=<suite id>
  python proposals/coherence-audit/fixes/push_new_cases.py <file.new-cases.json> [--commit]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id
from system_test_ops.testrail.client import TestRailClient, TestRailError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--project", type=int, default=42)
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args()
    suite = load_write_suite_id()
    if suite is None:
        print("error: TESTRAIL_WRITE_SUITE_ID not set", file=sys.stderr)
        return 2
    client = TestRailClient()
    writer = TestRailWriter(client, a.project, suite, commit=a.commit)
    rows = json.loads(Path(a.file).read_text(encoding="utf-8"))
    mode = "COMMIT" if a.commit else "DRY-RUN"
    print(f"[{mode}] push new cases from {a.file} -> suite {suite}")
    created = skipped = errors = 0
    for row in rows:
        extra = {
            "template_id": 1,
            "type_id": 2,
            "priority_id": row.get("priority_id", 1),
            "custom_devtypes": row.get("custom_devtypes") or [200],
            "custom_autoconfirmation": False,
            "custom_revstatus": 2,
            "custom_preface": row["preface"],
            "custom_preconds": row["preconds"],
            "custom_steps_seperated": row["steps"],
            "custom_expected": row["expected"],
        }
        try:
            res = writer.add_case(row["section_id"], row["title"], refs=row.get("refs", ""), extra=extra)
        except TestRailError as exc:
            print(f"  ERROR creating '{row['title'][:70]}': {exc}")
            errors += 1
            continue
        if res.get("skipped"):
            skipped += 1
            print(f"  skip (exists): {row['title'][:70]}")
        elif res.get("_dry_run"):
            created += 1
            print(f"  would create [section {row['section_id']}]: {row['title'][:70]}")
        else:
            created += 1
            print(f"  -> C{res.get('id')} [section {row['section_id']}]: {row['title'][:70]}")
    print(f"[{mode}] created/would-create={created} skipped={skipped} errors={errors}")
    if not a.commit:
        print("(dry-run only — nothing written. Re-run with --commit.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
