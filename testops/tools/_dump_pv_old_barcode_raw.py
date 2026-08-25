"""One-off: dump raw get_cases(42, 10047) full body fields for barcode + smartcard families, read-only."""
import json
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient

client = TestRailClient()
cases = client.get_cases(42, 10047)

out_dir = Path("proposals/coherence-audit/fixes")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "pv-suite-10047-old-raw.json"
out_path.write_text(json.dumps({"cases": cases}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(cases)} old-suite cases -> {out_path}")
