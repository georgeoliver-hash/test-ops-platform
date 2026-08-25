"""Dump full suite 30253 (POS, project 42) raw cases to JSON for offline analysis."""
from __future__ import annotations
import json
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient

HERE = Path(__file__).parent

def main():
    client = TestRailClient()
    cases = client.get_cases(42, 30253)
    out = []
    for c in cases:
        cid = c.get("id")
        full = client.get_case(cid)
        out.append(full)
    (HERE / "pos-suite-30253-raw.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"dumped {len(out)} cases")

if __name__ == "__main__":
    main()
