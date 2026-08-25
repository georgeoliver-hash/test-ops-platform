"""Push the ABT Operator/Passenger portal-split cases (built by build_abt_portal_split.py) into
suite 30279, and retire the 56 superseded sources (ZZ_DELETE_REVIEW). Suite-locked via
TestRailWriter/TESTRAIL_WRITE_SUITE_ID same as every other writer in this repo. Dry-run by default.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=30279
  python proposals/coherence-audit/fixes/push_abt_portal_split.py [--commit]
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id, TestRailWriteError

HERE = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args()

    suite = load_write_suite_id()
    if suite is None:
        print("error: TESTRAIL_WRITE_SUITE_ID not set")
        return 2

    client = TestRailClient()
    writer = TestRailWriter(client, 42, suite, commit=a.commit)
    mode = "COMMIT" if a.commit else "DRY-RUN"
    print(f"[{mode}] ABT portal-split push -> suite {suite}")

    new_cases = json.loads((HERE / "abt-portal-split.new-cases.json").read_text(encoding="utf-8"))
    created = skipped = errors = 0
    for row in new_cases:
        section_path = row["section_path"]
        leaf = writer.find_or_create_section_path(section_path)
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
            res = writer.add_case(leaf, row["title"], refs=row["refs"], extra=extra)
        except TestRailWriteError as exc:
            print(f"  ERROR creating '{row['title'][:60]}': {exc}")
            errors += 1
            continue
        if res.get("skipped"):
            skipped += 1
            print(f"  skip (exists): {row['title'][:70]}")
        elif res.get("_dry_run"):
            created += 1
            print(f"  would create [{'/'.join(section_path)}]: {row['title'][:70]}")
        else:
            created += 1
            print(f"  -> C{res.get('id')} [{'/'.join(section_path)}]: {row['title'][:70]}")

    print(f"[{mode}] new cases: created/would-create={created} skipped={skipped} errors={errors}")

    # Retire the 56 sources
    retire = json.loads((HERE / "abt-portal-split.retire.rewrite.json").read_text(encoding="utf-8"))
    by_id = {int(c["id"]): c for c in client.get_cases(42, suite)}
    removed = missing = 0
    for r in retire:
        cid = int(r["id"])
        ex = by_id.get(cid)
        if not ex:
            missing += 1
            print(f"  MISSING C{cid}")
            continue
        title = ex.get("title", "")
        if title.upper().startswith("ZZ_DELETE"):
            continue
        if a.commit:
            writer.update_case_fields(cid, {"title": f"ZZ_DELETE_REVIEW - {title}"}, section_id=ex.get("section_id"))
        removed += 1
        print(f"  {'retired' if a.commit else 'would retire'} C{cid}: {title[:70]}")

    print(f"[{mode}] retired(ZZ)={removed} missing={missing}")
    if not a.commit:
        print("(dry-run only — nothing written. Re-run with --commit.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
