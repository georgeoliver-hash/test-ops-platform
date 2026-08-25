"""One-off: re-dump raw get_cases(42, 30255) after the card-variant-sweep commit, for verification."""
import json
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient

client = TestRailClient()
cases_new = client.get_cases(42, 30255)

out_dir = Path("proposals/coherence-audit/fixes")
out_path = out_dir / "pv-suite-30255-raw.json"
sections_new = client.get_sections(42, 30255)
out_path.write_text(json.dumps({"cases": cases_new, "sections": sections_new}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(cases_new)} new-suite cases -> {out_path}")
