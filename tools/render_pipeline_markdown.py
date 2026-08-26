"""Render pipeline_reference.json (from render_pipeline_reference.py) into a Confluence-ready
Markdown doc. Kept as a separate step so the JSON stays reusable for other renderers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def esc(text: object) -> str:
    return str(text).replace("|", "\\|") if text is not None else "—"


def main() -> None:
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    data = json.loads(in_path.read_text(encoding="utf-8"))

    lines: list[str] = []
    lines.append("# Test-Ops Pipeline Reference — All 14 Processes")
    lines.append("")
    lines.append(
        "Generated 2026-08-26 directly from `system-test-ops/.claude/pipelines/*.yaml` via "
        "`test-ops-platform`'s `model/pipelines.py` — every row below is real data, not a "
        "summary written by hand."
    )
    lines.append("")
    lines.append(
        "**Repo location for every step below: `system-test-ops`** — this data all lives in "
        "that one repo today. The eventual target is a nested `Platform/` folder inside "
        "`flowbird-group/sit`; that migration has not happened yet."
    )
    lines.append("")
    lines.append(
        "**Legend:** CLI = deterministic code · AGENT = AI/judgement · HUMAN = needs a person · "
        "GATE = pass/fail check · COMPOSITE_REF = runs a whole other pipeline inline."
    )
    lines.append("")
    lines.append("## At a glance — AI-density per pipeline")
    lines.append("")
    lines.append("| Pipeline | cli | agent | human | gate | composite_ref |")
    lines.append("|---|---|---|---|---|---|")
    for pl in data:
        d = pl["density"]
        lines.append(
            f"| {pl['id']} | {d['cli']} | {d['agent']} | {d['human']} | {d['gate']} | "
            f"{d['composite_ref']} |"
        )
    lines.append("")

    for pl in data:
        lines.append(f"## {pl['id']}")
        lines.append("")
        lines.append(f"- **Slash command:** {pl['slash_command'] or '_(composite — no direct command)_'}")
        lines.append(f"- **UI action:** `{pl['ui_action']}`")
        lines.append(f"- **Description:** {pl['description']}")
        if pl["guardrails"]:
            lines.append(f"- **Guardrails:** {', '.join(pl['guardrails'])}")
        lines.append("")
        lines.append("| # | Step | Kind | Agent / command | Loop (fan-out) | Guardrails |")
        lines.append("|---|---|---|---|---|---|")
        for i, s in enumerate(pl["steps"], 1):
            detail = s["agent"] or s["command"] or (f"-> {s['ref']}" if s["ref"] else None) \
                or (f"-> {s['ref_pipeline']}" if s["ref_pipeline"] else None) or "—"
            loop = s["loop"] or "—"
            gr = ", ".join(s["guardrails"]) if s["guardrails"] else "—"
            lines.append(
                f"| {i} | {s['id']} | {s['kind'].upper()} | {esc(detail)} | {esc(loop)} | {esc(gr)} |"
            )
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
