"""One-off: dump raw get_cases(42, 30286) to a reference JSON with full body fields."""
import json
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient

client = TestRailClient()
cases = client.get_cases(42, 30286)
sections = client.get_sections(42, 30286)

out_dir = Path("proposals/coherence-audit/fixes")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "gv-suite-30286-raw.json"
out_path.write_text(json.dumps({"cases": cases, "sections": sections}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(cases)} cases, {len(sections)} sections -> {out_path}")
