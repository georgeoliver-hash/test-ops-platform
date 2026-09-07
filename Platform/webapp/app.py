"""Test-Ops Console — the first real (wired-up) version of the front end.

Read-only by design (per George, 2026-09-07): every endpoint here reads real data — the
mirrored device/function/feature/pipeline model, or a genuinely-generated build-stats /
gap-register run — and returns it as JSON for the static frontend to render. Nothing here
writes to TestRail, pushes a case, or calls an AI agent. That's deliberate: this is the
proving slice before any write path gets wired in.

Two data sources, both real, neither faked:
  - model/{devices,functions,flows,features,pipelines}.py — live, called on every request,
    straight from the mirrored SIT schema + the real .claude/pipelines/*.yaml.
  - webapp/fixtures/*.json — a real `build-stats`/`gap-register` run captured against real
    system-test-ops report data (POS, 2026-08-07 vs 2026-07-23) and committed, since running
    those commands live needs TestRail credentials this app doesn't have yet. Labelled as
    fixture data in the API response, not presented as live.

Run: uvicorn Platform.webapp.app:app --reload --app-dir . (from the repo root)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

_PLATFORM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PLATFORM_ROOT))
sys.path.insert(0, str(_PLATFORM_ROOT.parent / "tools"))

# model/pipelines.py resolves its root from this env var AT IMPORT TIME. The sandbox's own
# Platform/testops/.claude is stale (June, predates the pipelines/ split) — point this at a
# real system-test-ops checkout, same convention as sync_sit_mirror.py's --sit-path, unless
# the caller already set it themselves.
if "TESTOPS_CLAUDE_ROOT" not in os.environ:
    _live_sto = _PLATFORM_ROOT.parent.parent / "system-test-ops" / ".claude"
    if _live_sto.is_dir():
        os.environ["TESTOPS_CLAUDE_ROOT"] = str(_live_sto)

from model import devices, features, pipelines  # noqa: E402

WEBAPP_ROOT = Path(__file__).resolve().parent
FIXTURES = WEBAPP_ROOT / "fixtures"
KEEP_DEVICE_TYPES = ["ETM", "POS", "TVM", "GV", "PV", "HHD", "BV"]

app = FastAPI(title="Test-Ops Console API")


@app.get("/api/taxonomy")
def get_taxonomy():
    """Real project -> device -> model taxonomy, parsed live from the mirrored
    EquipmentTypes.json (model/devices.py). Same data the front-end target-switcher uses."""
    out = {}
    for project in devices.list_mirrored_projects():
        registry = devices.load_registry(project)
        out[project] = {
            et.device_type: et.equipment_type_names
            for et in registry.equipment_types
            if et.device_type in KEEP_DEVICE_TYPES
        }
    return out


@app.get("/api/features")
def get_features():
    """Common features vs. cited bespoke project variants (model/features.py) — the
    functionality-axis layer, including the ITSO/DESFire correction as real seed data."""
    reg = features.load_feature_registry()
    return {
        "features": [f.model_dump() for f in reg.features],
        "variants": [v.model_dump() for v in reg.variants],
        "gaps": {
            project: [f.key for f in reg.features_missing_variants(project)]
            for project in {v.project for v in reg.variants}
        },
    }


@app.get("/api/pipelines")
def get_pipelines():
    """Every pipeline's AI-density (cli/agent/human/gate counts), derived live from the real
    .claude/pipelines/*.yaml files — not a hand-maintained table that can go stale."""
    try:
        index = pipelines.load_pipeline_index()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    density = pipelines.ai_density_report()
    return [
        {
            "id": e.id, "ui_action": e.ui_action, "slash_command": e.slash_command,
            "density": density.get(e.id, {}),
        }
        for e in index
    ]


@app.get("/api/pipelines/{pipeline_id}")
def get_pipeline_detail(pipeline_id: str):
    """Full ordered step list for one pipeline, straight from its real YAML file."""
    try:
        p = pipelines.load_pipeline(pipeline_id)
    except (KeyError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "id": p.id,
        "description": p.description,
        "trigger": p.trigger.model_dump(),
        "guardrails": p.guardrails,
        "steps": [s.model_dump() for s in p.steps],
    }


@app.get("/api/build-stats")
def get_build_stats():
    """Suite health — real numbers from an actual `build-stats` run against real POS report
    data (2026-08-07 vs 2026-07-23), committed as a fixture since live TestRail creds aren't
    wired into this app yet. `is_fixture: true` says so explicitly."""
    path = FIXTURES / "pos-build-stats.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No build-stats fixture found")
    data = json.loads(path.read_text(encoding="utf-8"))
    data["is_fixture"] = True
    data["fixture_note"] = "Real build-stats run, 2026-08-07 vs 2026-07-23 POS report data — not a live TestRail call."
    return data


@app.get("/api/gap-register")
def get_gap_register(limit: int = 25):
    """Real GAP/UNCONFIRMED markers, from an actual `gap-register` run over the real repo
    (2026-09-07). 968 found repo-wide — capped for display, count always shown uncapped."""
    path = FIXTURES / "gaps.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No gap-register fixture found")
    markers = json.loads(path.read_text(encoding="utf-8"))
    return {"total": len(markers), "shown": markers[:limit], "is_fixture": True}


@app.get("/api/repo-map")
def get_repo_map():
    """File -> purpose -> line count, generated live on every request from the real
    module docstrings / agent frontmatter — see tools/render_repo_map.py."""
    from render_repo_map import build_sections  # imported lazily; lives in tools/

    sto_root = _PLATFORM_ROOT.parent.parent / "system-test-ops"
    if not sto_root.is_dir():
        raise HTTPException(
            status_code=503,
            detail=f"system-test-ops checkout not found at {sto_root} — set it up alongside test-ops-platform.",
        )
    sections = build_sections(sto_root, _PLATFORM_ROOT.parent)
    return [
        {"title": title, "files": [{"path": p, "purpose": purpose, "lines": loc} for p, purpose, loc in rows]}
        for title, rows in sections
    ]


app.mount("/", StaticFiles(directory=str(WEBAPP_ROOT / "static"), html=True), name="static")
