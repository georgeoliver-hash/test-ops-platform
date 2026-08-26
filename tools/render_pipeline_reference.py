"""One-off render: full 14-pipeline reference doc from real model/pipelines.py data.

Not wired into any CLI yet -- run directly when the Confluence-ready reference needs
regenerating after pipelines/*.yaml changes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Platform"))
from model import pipelines as p  # noqa: E402


def main() -> None:
    data = []
    for entry in p.load_pipeline_index():
        pl = p.load_pipeline(entry.id)
        steps = []
        for s in pl.steps:
            steps.append(
                {
                    "id": s.id,
                    "kind": s.kind.value if s.kind else "composite_ref",
                    "agent": s.agent,
                    "command": s.command,
                    "loop": s.loop,
                    "ref": s.ref,
                    "ref_pipeline": s.ref_pipeline,
                    "guardrails": s.guardrails,
                }
            )
        data.append(
            {
                "id": pl.id,
                "ui_action": pl.trigger.ui_action,
                "slash_command": pl.trigger.slash_command,
                "description": pl.description,
                "guardrails": pl.guardrails,
                "steps": steps,
                "density": pl.ai_density(),
            }
        )

    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("pipeline_reference.json")
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"wrote {len(data)} pipelines -> {out_path}")


if __name__ == "__main__":
    main()
