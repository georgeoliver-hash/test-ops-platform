"""Push the POS Data-variations expansion (built by build_pos_variant_expansion.py) into suite
30253: retitle+rewrite the 23 primary cases in place, and create the 73 new per-variant cases in
the same section as their family's original case. Suite-locked via TestRailWriter/
TESTRAIL_WRITE_SUITE_ID same as every other writer in this repo. Dry-run by default.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=30253
  python proposals/coherence-audit/fixes/push_pos_variant_expansion.py [--commit]
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
    print(f"[{mode}] POS variant-expansion push -> suite {suite}")

    # --- 1. retitle+rewrite the 23 primaries in place ---
    rewrite_rows = json.loads((HERE / "pos-variant-expansion.rewrite.json").read_text(encoding="utf-8"))
    by_id = {int(c["id"]): c for c in client.get_cases(42, suite)}
    upd = missing = skip = 0
    for r in rewrite_rows:
        cid = int(r["id"])
        ex = by_id.get(cid)
        if not ex:
            missing += 1
            print(f"  MISSING C{cid}")
            continue
        extra = {"title": r["title"]}
        if r.get("preface"):
            extra["custom_preface"] = r["preface"]
        if r.get("preconds"):
            extra["custom_preconds"] = r["preconds"]
        if r.get("expected"):
            extra["custom_expected"] = r["expected"]
        if r.get("steps"):
            steps = r["steps"]
            bad = [i for i, s in enumerate(steps) if not (s.get("content") or "").strip() or not (s.get("expected") or "").strip()]
            if bad:
                print(f"  REFUSED C{cid}: blank step(s) {bad} - not pushed")
                skip += 1
                continue
            extra["custom_steps_seperated"] = steps
        if r.get("refs"):
            extra["refs"] = r["refs"]
        writer.update_case_fields(cid, extra, section_id=ex.get("section_id"))
        upd += 1
        print(f"  {'updated' if a.commit else 'would update'} C{cid}: {r['title'][:70]}")
    print(f"[{mode}] primaries: updated={upd} skipped={skip} missing={missing}")

    # --- 2. create the new per-variant cases ---
    new_rows = json.loads((HERE / "pos-variant-expansion.new-cases.json").read_text(encoding="utf-8"))
    created = nskip = errors = 0
    for row in new_rows:
        section_path = row["section_path"]
        leaf = writer.find_or_create_section_path(section_path)
        steps = row["steps"]
        bad = [i for i, s in enumerate(steps) if not (s.get("content") or "").strip() or not (s.get("expected") or "").strip()]
        if bad:
            print(f"  REFUSED new '{row['title'][:60]}': blank step(s) {bad}")
            errors += 1
            continue
        extra = {
            "template_id": 1,
            "type_id": 2,
            "priority_id": 1,
            "custom_devtypes": row.get("custom_devtypes") or [5],
            "custom_revstatus": 1,
            "custom_autoconfirmation": False,
            "custom_preface": row["preface"],
            "custom_preconds": row["preconds"],
            "custom_steps_seperated": steps,
            "custom_expected": row["expected"],
        }
        try:
            res = writer.add_case(leaf, row["title"], refs=row.get("refs"), extra=extra)
        except TestRailWriteError as exc:
            print(f"  ERROR creating '{row['title'][:60]}': {exc}")
            errors += 1
            continue
        if res.get("skipped"):
            nskip += 1
            print(f"  skip (exists): {row['title'][:70]}")
        elif res.get("_dry_run"):
            created += 1
            print(f"  would create [{'/'.join(section_path)}]: {row['title'][:70]}")
        else:
            created += 1
            print(f"  -> C{res.get('id')} [{'/'.join(section_path)}]: {row['title'][:70]}")

    print(f"[{mode}] new cases: created/would-create={created} skipped={nskip} errors={errors}")
    if not a.commit:
        print("(dry-run only - nothing written. Re-run with --commit.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
