"""Dump the FULL body (title, section, refs, preface, preconds, steps, expected) of the 23
Data-variations POS cases identified by _find_variations.py, for manual review."""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).parent
cases = json.loads((HERE / "pos-suite-30253-raw.json").read_text(encoding="utf-8"))
by_id = {c["id"]: c for c in cases}

IDS = [4100427,4100413,4100419,4100420,4100421,4100423,4100393,4100394,4100395,4100396,4100397,
       4100399,4100400,4100401,4100503,4100504,4100392,4100403,4100404,4100405,4100407,4100408,4100410]

lines = []
for cid in IDS:
    c = by_id.get(cid)
    if not c:
        lines.append(f"=== C{cid} MISSING ===")
        continue
    lines.append(f"\n{'='*100}\n=== C{cid} :: {c.get('title')}  [section_id={c.get('section_id')}]")
    lines.append(f"Refs: {c.get('refs')}")
    lines.append(f"custom_devtypes: {c.get('custom_devtypes')}")
    lines.append(f"PREFACE: {c.get('custom_preface')}")
    lines.append(f"PRECONDS: {c.get('custom_preconds')}")
    for i, s in enumerate(c.get("custom_steps_seperated") or []):
        lines.append(f"  STEP{i+1} content: {s.get('content')}")
        lines.append(f"  STEP{i+1} expected: {s.get('expected')}")
    lines.append(f"EXPECTED: {c.get('custom_expected')}")

out_text = "\n".join(lines)
(HERE / "_variations_full_bodies.txt").write_text(out_text, encoding="utf-8")
print("wrote", len(IDS), "cases")
