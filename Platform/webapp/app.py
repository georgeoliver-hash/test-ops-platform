"""Test-Ops Console — the first real (wired-up) version of the front end.

Read-only against TestRail by design (per George, 2026-09-07): every data endpoint here
reads real data — the mirrored device/function/feature/pipeline model, or a genuinely-
generated build-stats / gap-register run — and returns it as JSON. Nothing here writes to
TestRail, pushes a case, or calls an AI agent. That boundary is unchanged.

Separately, this app DOES have real local writes now (2026-09-07): a settings area for
TestRail credentials (encrypted at rest, see store.py) and user-editable suite mappings.
That's local app configuration on the machine running the app, not a TestRail write — a
different trust boundary, same one system-test-ops' own `.env` file already relies on.

Three data sources, all real, none faked:
  - model/{devices,functions,flows,features,pipelines}.py — live, called on every request,
    straight from the mirrored SIT schema + the real .claude/pipelines/*.yaml.
  - webapp/fixtures/*.json — a real `build-stats`/`gap-register` run captured against real
    system-test-ops report data (POS, 2026-08-07 vs 2026-07-23) and committed, since running
    those commands live needs TestRail credentials this app doesn't have a live call for
    yet. Labelled as fixture data in the API response, not presented as live.
  - webapp/data/console.db (gitignored, local-only) — suite mappings + encrypted TestRail
    credentials, single-user today (see store.py's module docstring for why).
  - webapp/data/uploads/<project>/<device>/ (gitignored, local-only) — docs dropped via the
    UI for a future ingest-docs/add-feature run. Storage only — no pipeline reads this
    folder yet.

Run: uvicorn Platform.webapp.app:app --reload --app-dir . (from the repo root)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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

# NOTE: model/devices.py, model/functions.py and model/flows.py all read the same
# SIT_SCHEMA_ROOT env var, but resolve three DIFFERENT real subtrees under it (ConfigSets/
# for devices, scattered Resources/Devices/*/Bindings/ for functions, ConfigSets/*/ScreenFlow
# for flows) -- unlike TESTOPS_CLAUDE_ROOT, one shared live-`sit`-checkout default can't
# correctly serve all three at once without replicating sync_sit_mirror.py's scatter/gather
# logic. So this deliberately does NOT auto-point at a live `sit` checkout the way
# TESTOPS_CLAUDE_ROOT does -- sit-mirror/ (re-synced via tools/sync_sit_mirror.py) stays the
# real, working source for now. Point SIT_SCHEMA_ROOT at a live checkout's ConfigSets/
# yourself only if you're using devices.py alone and know the other two won't be called.

# system-test-ops' own .env, same sibling-checkout convention as TESTOPS_CLAUDE_ROOT above.
# George already has real TESTRAIL_* values there (used by that repo's CLI) -- the console
# offers to import them rather than asking him to retype credentials that already exist on
# this machine. Detection/import both happen server-side; the key itself is never sent to
# the frontend at any point (see store.py's detect_/import_sibling_env_credentials).
SIBLING_ENV_PATH = _PLATFORM_ROOT.parent.parent / "system-test-ops" / ".env"
SYSTEM_TEST_OPS_KNOWLEDGE = _PLATFORM_ROOT.parent.parent / "system-test-ops" / "knowledge"

from model import devices, features, flows, functions, pipelines  # noqa: E402
from Platform.webapp import runner, store  # noqa: E402

WEBAPP_ROOT = Path(__file__).resolve().parent
FIXTURES = WEBAPP_ROOT / "fixtures"
KEEP_DEVICE_TYPES = ["ETM", "POS", "TVM", "GV", "PV", "HHD", "BV"]

app = FastAPI(title="Test-Ops Console API")
store.init_db()


class SuiteMappingIn(BaseModel):
    project: str
    device: str
    old_suite: str
    new_suite: str
    new_suite_id: int | None = None


class RunRequest(BaseModel):
    project: str
    device: str


class CredentialsIn(BaseModel):
    testrail_url: str
    testrail_user: str
    testrail_api_key: str


@app.get("/api/me")
def get_me():
    return store.get_current_user()


@app.get("/api/suite-mappings")
def get_suite_mappings():
    """Real, user-editable old(read-only source)/new(write target) suite pairs, keyed per
    project+device — never a single global suite. Seeded with the one documented pair
    (Translink/POS) from system-test-ops' CLAUDE.md; every other combination is absent
    here until a real person confirms and adds it."""
    return store.list_suite_mappings()


@app.post("/api/suite-mappings")
def put_suite_mapping(body: SuiteMappingIn):
    try:
        store.upsert_suite_mapping(body.project, body.device, body.old_suite, body.new_suite, body.new_suite_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True}


@app.delete("/api/suite-mappings/{project}/{device}")
def remove_suite_mapping(project: str, device: str):
    deleted = store.delete_suite_mapping(project, device)
    if not deleted:
        raise HTTPException(status_code=404, detail="No such mapping")
    return {"ok": True}


@app.get("/api/credentials/status")
def get_credentials_status():
    """Never the API key itself — only whether one is configured, and for which TestRail
    URL/user. See store.py's module docstring for the encryption-at-rest design."""
    return store.get_credentials_status()


@app.get("/api/setup-status")
def get_setup_status(project: str, device: str):
    """Real readiness signal for the sidebar's fade-until-set-up gate (George, 2026-09-08).
    `docs_configured` deliberately checks TWO real things, not just console uploads: an
    established project like Translink already has real knowledge/<project>/ content from
    years of work that never went through this app's upload feature — gating on uploads
    alone would wrongly show it as "not set up". A brand-new project with neither is
    honestly not set up yet."""
    creds = store.get_credentials_status()
    suite_id = store.get_new_suite_id(project, device)
    docs = store.list_docs(project, device)
    knowledge_dir = SYSTEM_TEST_OPS_KNOWLEDGE / project.lower()
    has_knowledge = knowledge_dir.is_dir() and any(knowledge_dir.rglob("*.md"))
    return {
        "credentials_configured": creds["configured"],
        "suite_configured": suite_id is not None,
        "docs_configured": bool(docs) or has_knowledge,
        "ready": creds["configured"] and suite_id is not None and (bool(docs) or has_knowledge),
    }


@app.post("/api/credentials")
def put_credentials(body: CredentialsIn):
    try:
        store.save_credentials(body.testrail_url, body.testrail_user, body.testrail_api_key)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.get_credentials_status()


@app.delete("/api/credentials")
def remove_credentials():
    store.delete_credentials()
    return {"ok": True}


@app.get("/api/credentials/detect-env")
def detect_env_credentials():
    """Read-only peek at the sibling system-test-ops/.env this machine already has — never
    the key itself, just enough (url/user) to show what an import would bring in."""
    found = store.detect_sibling_env_credentials(SIBLING_ENV_PATH)
    return {"found": found is not None, **(found or {})}


@app.post("/api/credentials/import-env")
def import_env_credentials():
    if not store.import_sibling_env_credentials(SIBLING_ENV_PATH):
        raise HTTPException(status_code=404, detail="No TestRail credentials found in system-test-ops/.env")
    return store.get_credentials_status()


@app.get("/api/docs")
def list_docs(project: str, device: str):
    """Files dropped for this project/device pair, ready for a future ingest-docs run to
    pick up. Storage only today — no pipeline actually consumes this folder yet (that needs
    the agent-run wiring the 'Run' buttons on pipeline pages are already stubbed out for)."""
    return store.list_docs(project, device)


@app.post("/api/docs")
async def upload_doc(project: str, device: str, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename given.")
    content = await file.read()
    try:
        store.save_doc(project, device, file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True}


@app.delete("/api/docs/{project}/{device}/{filename}")
def remove_doc(project: str, device: str, filename: str):
    if not store.delete_doc(project, device, filename):
        raise HTTPException(status_code=404, detail="No such file")
    return {"ok": True}


@app.post("/api/docs/{project}/refresh-check")
def refresh_docs_check(project: str):
    """Real change-detection against the project's local requirements folder
    (%USERPROFILE%\\TestOpsRequirements\\<project>\\, see .env.example's documented
    convention) -- what's new/changed/removed since the last check. Does NOT re-parse
    anything into knowledge/*.md; that's the still-unbuilt ingest-docs pipeline. This just
    means nothing silently goes stale between now and when that exists."""
    req_dir = Path.home() / "TestOpsRequirements" / project.lower()
    return store.check_docs_for_changes(project, req_dir)


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
    """Every pipeline's AI-density (cli/agent/human/gate counts) and real description,
    derived live from the real .claude/pipelines/*.yaml files — not a hand-maintained
    table that can go stale."""
    try:
        index = pipelines.load_pipeline_index()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    density = pipelines.ai_density_report()
    out = []
    for e in index:
        p = pipelines.load_pipeline(e.id)
        out.append({
            "id": e.id, "ui_action": e.ui_action, "slash_command": e.slash_command,
            "description": p.description, "density": density.get(e.id, {}),
            "runnable": runner.is_runnable(e.id),
        })
    return out


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
        "runnable": runner.is_runnable(p.id),
    }


@app.post("/api/pipelines/{pipeline_id}/run")
def run_pipeline(pipeline_id: str, body: RunRequest):
    """Kicks off a REAL run — today, only `audit` (read-only) is wired. Every other pipeline
    stays disabled in the UI on purpose (George's call, 2026-09-08: read-only pipelines get
    proven safe before any write-capable one gets wired up)."""
    if not runner.is_runnable(pipeline_id):
        raise HTTPException(status_code=400, detail=f"'{pipeline_id}' isn't wired to run yet — only {sorted(runner.RUNNABLE_PIPELINES)} are.")
    try:
        run_id = runner.start_audit_run(body.project, body.device)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"run_id": run_id}


@app.get("/api/pipelines/runs/{run_id}")
def get_pipeline_run(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    return run


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


@app.get("/api/run-health")
def get_run_health(limit: int = 15):
    """Real run-health data for POS (2026-08-07, 6 runs considered) — a genuine `runs` CLI
    output, not synthesised. Flagged cases sorted worst-first (most failures); counts by
    flag type shown uncapped even though the list itself is capped for display."""
    path = FIXTURES / "pos-run-health.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No run-health fixture found")
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    flag_names = ("always_failing", "never_executed", "flaky", "recently_regressed", "orphaned")
    flagged = [c for c in cases if any(c.get(f) for f in flag_names)]
    flagged.sort(key=lambda c: (c.get("failed", 0), c.get("executed_count", 0)), reverse=True)
    counts = {f: sum(1 for c in cases if c.get(f)) for f in flag_names}
    return {
        "suite": data.get("suite"), "project": data.get("project"),
        "runs_considered": len(data.get("run_ids", [])),
        "cases_total": len(cases), "flagged_total": len(flagged),
        "counts": counts, "shown": flagged[:limit],
        "is_fixture": True,
        "fixture_note": "Real `runs` CLI output, POS suite 30253, 2026-08-07 (6 runs) — not a live TestRail call.",
    }


@app.get("/api/gap-register")
def get_gap_register(limit: int = 25):
    """Real GAP/UNCONFIRMED markers, from an actual `gap-register` run over the real repo
    (re-run 2026-09-08, 972 found repo-wide) — capped for display, count always shown
    uncapped."""
    path = FIXTURES / "gaps.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No gap-register fixture found")
    markers = json.loads(path.read_text(encoding="utf-8"))
    return {"total": len(markers), "shown": markers[:limit], "is_fixture": True}


@app.get("/api/automation/keywords")
def get_automation_keywords(device_family: str | None = None, q: str | None = None):
    """Real SIT function keywords, parsed live from Bindings/*.robot files (model/functions.py)
    -- view-only, per George 2026-09-08 ('just for viewing'). Same data test-automation-sit's
    Given/When/Then steps already resolve against; nothing here writes anything."""
    keywords = functions.load_all_keywords()
    if device_family:
        keywords = [k for k in keywords if k.device_family.lower() == device_family.lower()]
    if q:
        needle = q.lower()
        keywords = [k for k in keywords if needle in k.phrase.lower()]
    families = sorted({k.device_family for k in functions.load_all_keywords()})
    return {"total": len(keywords), "device_families": families, "keywords": [k.model_dump() for k in keywords]}


@app.get("/api/automation/flows")
def get_automation_flow_devices(project: str):
    """Device types with a real screenflow_map.jsonc for this project (model/flows.py)."""
    return {"project": project, "device_types": flows.available_screen_graphs(project)}


@app.get("/api/automation/flows/{project}/{device_type}")
def get_automation_flow_graph(project: str, device_type: str):
    """One device's real screen-transition graph, straight from SIT's discovery output."""
    try:
        graph = flows.load_screen_graph(project, device_type)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return graph.model_dump()


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
