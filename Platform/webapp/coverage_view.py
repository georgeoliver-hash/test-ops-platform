"""Automation coverage metrics for the console: how the Robot tests tie to TestRail cases, and which TestRail sections
have a linked functional test. Read-only: it reads the two draft files system-test-ops writes
(robot-case-mapping-DRAFT.csv, robot-coverage-audit-DRAFT.csv) and counts them. Nothing is computed from a guess.

Both files live in system-test-ops/proposals/<Project>-<Device>-.../ ; they are refreshed by re-running
tools/draft_robot_case_mapping.py and tools/audit_robot_coverage.py (see that repo's CLAUDE.md).
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

MAPPING = "robot-case-mapping-DRAFT.csv"
AUDIT = "robot-coverage-audit-DRAFT.csv"
HOW = ("explicit", "title", "similar", "map-edge", "none")
FLAGS = ("ZERO", "PROVISIONAL", "REACH-ONLY", "OK")


def find_folder(proposals: Path, project: str, device: str) -> Path | None:
    """The proposals folder for this target: named '<Project>-<Device>-...' and holding both draft files."""
    if not proposals.is_dir():
        return None
    prefix = f"{project}-{device}-".lower()
    for d in sorted(proposals.iterdir()):
        if d.is_dir() and d.name.lower().startswith(prefix) and (d / MAPPING).is_file() and (d / AUDIT).is_file():
            return d
    return None


def _rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _int(v: str) -> int:
    return int(v) if (v or "").strip().isdigit() else 0


def _stamp(*paths: Path) -> str:
    newest = max(p.stat().st_mtime for p in paths)
    return datetime.fromtimestamp(newest, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def coverage(proposals: Path, project: str, device: str) -> dict:
    folder = find_folder(proposals, project, device)
    if folder is None:
        return {"available": False,
                "reason": f"No coverage drafts for {project}/{device} yet. Run tools/draft_robot_case_mapping.py then "
                          "tools/audit_robot_coverage.py in system-test-ops."}
    mapping, audit = _rows(folder / MAPPING), _rows(folder / AUDIT)
    how = {k: 0 for k in HOW}
    approved = 0
    for r in mapping:
        how[r.get("how_found") if r.get("how_found") in how else "none"] += 1
        if (r.get("approved_case_id") or "").strip():
            approved += 1
    tests = len(mapping)
    expected = tests - how["map-edge"]                      # tests that should have a case (an edge test checks the map)
    linked = how["explicit"] + approved
    flags = {k: 0 for k in FLAGS}
    sections = []
    for r in audit:
        flag = r.get("flag") if r.get("flag") in flags else "ZERO"
        flags[flag] += 1
        sections.append({"section": r["section"], "cases": _int(r["cases"]), "ready": _int(r["ready"]), "linked": _int(r["linked_live_tests"]),
                         "provisional": _int(r["provisional_tests"]), "kinds": r["linked_kinds"], "flag": flag,
                         "proposal": r["proposed_functional_smoke"]})
    sections.sort(key=lambda s: (FLAGS.index(s["flag"]), -s["ready"], s["section"]))
    return {"available": True, "folder": folder.name, "generated": _stamp(folder / MAPPING, folder / AUDIT),
            "tests": {"total": tests, "should_have_a_case": expected, "linked": linked, "approved_in_csv": approved, **{k.replace("-", "_"): v for k, v in how.items()}},
            "sections": {"total": len(audit), **{k.replace("-", "_"): v for k, v in flags.items()}},
            "gaps": sections,
            "note": "Draft numbers. A suggested link (title / similar) is not coverage; approve rows in the mapping CSV and re-run the audit."}
