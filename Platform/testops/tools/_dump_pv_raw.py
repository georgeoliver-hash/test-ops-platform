"""One-off: dump raw get_cases(42, 30255) and get_cases(42, 10047 smartcard section) with full body fields."""
import json
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient

client = TestRailClient()
cases_new = client.get_cases(42, 30255)
sections_new = client.get_sections(42, 30255)

out_dir = Path("proposals/coherence-audit/fixes")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "pv-suite-30255-raw.json"
out_path.write_text(json.dumps({"cases": cases_new, "sections": sections_new}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(cases_new)} new-suite cases, {len(sections_new)} sections -> {out_path}")
