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

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import zipfile
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
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

from model import automation_tests, devices, flows, functions, pipelines  # noqa: E402
from Platform.webapp import case_review, gap_exchange, reviews, runner, store  # noqa: E402

WEBAPP_ROOT = Path(__file__).resolve().parent
FIXTURES = WEBAPP_ROOT / "fixtures"
KEEP_DEVICE_TYPES = ["ETM", "POS", "TVM", "GV", "PV", "HHD", "BV"]

# Periodic scheduled-scan checker (George, 2026-09-22: "does our tool need to
# automatically read the docs... and make suggestions"). This app isn't a 24/7 service
# (single-user, local, per store.py's own module docstring) -- "scheduled" here honestly
# means "checked on the next app usage after the interval has elapsed", via this
# in-process poll, NOT a real always-on cron. A target only ever gets scanned if it was
# explicitly opted in via /api/scheduled-checks (never on by default).
_SCHEDULER_POLL_SECONDS = 1800


def _scheduled_check_loop() -> None:
    while True:
        try:
            for due in store.get_due_scheduled_checks():
                run_id = runner.start_scheduled_scan(due["project"], due["device"])
                store.mark_scheduled_check_run(due["project"], due["device"], run_id, datetime.now(timezone.utc).isoformat())
        except Exception:
            pass  # best-effort background loop -- one bad target must never kill the whole poller
        time.sleep(_SCHEDULER_POLL_SECONDS)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    threading.Thread(target=_scheduled_check_loop, daemon=True).start()
    yield


app = FastAPI(title="Test-Ops Console API", lifespan=_lifespan)
store.init_db()


class SuiteMappingIn(BaseModel):
    project: str
    device: str
    old_suite: str = ""
    new_suite: str
    new_suite_id: int | None = None
    old_suite_id: int | None = None
    fresh_build: bool = False
    # The real TestRail project these suites live under -- NOT the same as `project` above
    # (this console's own label). Found live, 2026-09-14: NJT's real suites live under TestRail
    # project 27 ("UK Bus Projects"), not the .env default (42, where Translink's suites live)
    # -- a single global default can't serve every target correctly.
    testrail_project_id: int | None = None
    # The real TestRail project the NEW suite lives under -- kept separate from
    # testrail_project_id (the OLD suite's project) because they can genuinely differ
    # (found live: a dry-run target's old suite sat under project 27, its new suite
    # under project 12).
    new_testrail_project_id: int | None = None


class RunRequest(BaseModel):
    project: str
    device: str
    # Whatever a pipeline's own `inputs:` list declares beyond project/device (e.g.
    # ingest-docs' docs_path) — validated as required/missing against that list below,
    # not a hardcoded field per pipeline.
    extra_inputs: dict[str, str] = {}


class GapAnswerIn(BaseModel):
    project: str
    device: str | None = None
    gap_ref: str
    question: str
    answer: str
    answered_by: str = "George Oliver"
    entry_type: str = "answer"  # "answer" | "clarification_request" | "conflict"


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
        store.upsert_suite_mapping(
            body.project, body.device, body.old_suite, body.new_suite, body.new_suite_id, body.old_suite_id,
            body.fresh_build, body.testrail_project_id, body.new_testrail_project_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True}


@app.get("/api/testrail/projects")
def get_testrail_projects():
    """Real project list straight from TestRail -- for a dropdown, so a target never again
    gets pointed at the wrong project by a hand-typed id (found live, 2026-09-14: NJT's
    suites live under project 27, not the .env default 42)."""
    parts = [str(runner._VENV_PYTHON), "-m", "system_test_ops", "list-projects"]
    try:
        result = subprocess.run(parts, cwd=str(runner.SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HTTPException(status_code=500, detail=f"Could not reach TestRail via the CLI: {exc}") from exc
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=(result.stderr or result.stdout or "list-projects failed").strip())
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected output from list-projects: {exc}") from exc


@app.get("/api/testrail/suites")
def get_testrail_suites(project_id: int):
    """Real suite list for one TestRail project -- same rationale as /api/testrail/projects."""
    parts = [str(runner._VENV_PYTHON), "-m", "system_test_ops", "list-suites", "--project", str(project_id)]
    try:
        result = subprocess.run(parts, cwd=str(runner.SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HTTPException(status_code=500, detail=f"Could not reach TestRail via the CLI: {exc}") from exc
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=(result.stderr or result.stdout or "list-suites failed").strip())
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected output from list-suites: {exc}") from exc


@app.get("/api/suite-mappings/git-status")
def get_suite_targets_git_status():
    """Read-only: has system-test-ops/knowledge/suite_targets.yaml (the ONE canonical target
    list, shared with the wider department via that repo) got local changes not yet
    committed, or commits not yet pushed to origin? This app never runs git commit/push
    itself for this file -- sharing a newly added target with a colleague is a deliberate
    manual step, same as every other repo write this tool makes."""
    return store.suite_targets_git_status()


@app.delete("/api/suite-mappings/{project}/{device}")
def remove_suite_mapping(project: str, device: str):
    deleted = store.delete_suite_mapping(project, device)
    if not deleted:
        raise HTTPException(status_code=404, detail="No such mapping")
    return {"ok": True}


class ApproveTargetIn(BaseModel):
    approved_by: str = "George Oliver"


@app.post("/api/suite-mappings/{project}/{device}/approve")
def approve_suite_mapping(project: str, device: str, body: ApproveTargetIn):
    """Real, persisted sign-off on a target — replaces the old cosmetic #approveCheck
    checkbox. This is a precondition the runner checks independently of any single run's
    own per-step human gate before letting a push+--commit step execute."""
    try:
        updated = store.approve_suite_mapping(project, device, body.approved_by)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=404, detail="No such mapping — add it first.")
    return updated


@app.get("/api/credentials/status")
def get_credentials_status():
    """Never the API key itself — only whether one is configured, and for which TestRail
    URL/user. See store.py's module docstring for the encryption-at-rest design."""
    return store.get_credentials_status()


@app.post("/api/credentials/check-connection")
def check_connection():
    """Real, live TestRail connectivity check -- 'Configured' above only ever meant a row
    was saved; this actually calls TestRail (via the same system_test_ops CLI check every
    real pipeline step relies on) and reports what really happened, right now."""
    return runner.check_testrail_connection()


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
def list_docs(project: str, device: str, kind: str = "functional"):
    """Files dropped for this project/device pair, ready for a future ingest-docs run to
    pick up. Storage only today — no pipeline actually consumes this folder yet (that needs
    the agent-run wiring the 'Run' buttons on pipeline pages are already stubbed out for).

    `kind` (George, 2026-09-28): "functional" (default, unchanged) or "design" -- a real,
    separate bucket for anything UI/UX-visual (Figma exports, Overflow JSON, images, ...),
    replacing today's single flow_data_path field on Onboarding."""
    if kind not in ("functional", "design"):
        raise HTTPException(status_code=400, detail="kind must be 'functional' or 'design'.")
    return store.list_docs(project, device, kind)


def _validated_target(project: str, device: str) -> tuple[str, str]:
    """400 on any project/device that isn't a plain name. These are interpolated into a
    real filesystem path (uploads/<project>/<device>/), so `project=../../PWNED` wrote
    outside the data dir entirely before this existed -- found 2026-09-23 by an
    end-to-end sweep."""
    try:
        return store.safe_path_segment(project, "project"), store.safe_path_segment(device, "device")
    except store.UnsafeNameError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/docs/folder")
def get_docs_folder(project: str, device: str):
    """Real docs_path for the Ingest run form. `source` tells the frontend which one it
    got, so it can say so honestly instead of implying "uploaded" when it's really the
    synced folder.

    Returns `options` too: when BOTH a synced library and uploaded files exist, the user
    picks (George, 2026-09-23: he'd have uploaded 660MB and Ingest would have read the
    other folder anyway if it silently won with no hint).

    CHANGED 2026-09-30 (George, real live confusion + a genuine architecture mistake):
    the default used to be "whichever has more real files" -- which silently prefers a
    huge, possibly-stale synced folder over a small, deliberately curated set of uploads
    that are actually the current true source (Translink POS: 3 real uploaded docs vs.
    75 old synced-folder files that had already been superseded). File count is not a
    signal of which one is *current* -- it's just a signal of which is *bigger*. Uploads
    now win whenever any real upload exists; the synced folder becomes an explicit,
    clearly-labelled secondary choice (still useful for bulk-importing a big local
    library George hasn't hand-picked from yet -- the reason it was built in the first
    place, per the 2026-09-23 note above) rather than a silent, count-based default."""
    project, device = _validated_target(project, device)

    def _count(path: Path) -> int:
        try:
            return sum(1 for f in path.rglob("*") if f.is_file() and f.stat().st_size > 0)
        except OSError:
            return 0

    options = []
    uploads = Path(store.uploads_dir_path(project, device))
    upload_count = _count(uploads)
    options.append({"path": str(uploads), "source": "uploads_folder",
                    "label": "Docs uploaded in this console", "file_count": upload_count})
    real = store.resolve_ingest_docs_source(project)
    if real["path"]:
        options.append({"path": real["path"], "source": "requirements_folder",
                        "label": "Synced requirements folder", "file_count": _count(Path(real["path"]))})

    by_source = {o["source"]: o for o in options}
    if by_source["uploads_folder"]["file_count"] > 0:
        chosen = by_source["uploads_folder"]
    elif "requirements_folder" in by_source:
        chosen = by_source["requirements_folder"]
    else:
        chosen = by_source["uploads_folder"]
    return {"path": chosen["path"], "source": chosen["source"], "options": options}


_CONVERTIBLE_EXTS = {".docx", ".xlsx", ".pdf", ".csv", ".txt"}


@app.get("/api/docs/folder-files")
def get_docs_folder_files(project: str, device: str, path: str | None = None):
    """Real, actually-present convertible files under this target's docs folder --
    George, 2026-09-28: "only_file? can this not be a drop-down? of the recently
    uploaded files". Capped at 300 entries (`truncated: true` past that) so a large
    synced library (e.g. Translink's real 650MB folder) can't make this call
    pathologically slow or the response pathologically huge -- the field still accepts
    free text too, this is a convenience list, not the only path in.

    `path` (added 2026-09-30, George: switching the docs-source toggle "literally never
    changes" what this list shows) -- lets the caller ask for a SPECIFIC option's files
    (uploads vs. synced folder) instead of always getting whichever `/api/docs/folder`
    would resolve to by default. Must exactly match one of that same endpoint's real
    `options[].path` values for this project/device -- never an arbitrary client-supplied
    path, to keep this read strictly to the two real, already-validated candidates."""
    project, device = _validated_target(project, device)
    resolved = get_docs_folder(project, device)
    if path is not None:
        if path not in {o["path"] for o in resolved["options"]}:
            raise HTTPException(status_code=400, detail="path must match a real docs-source option for this target.")
        folder = Path(path)
    else:
        folder = Path(resolved["path"]) if resolved["path"] else Path(store.uploads_dir_path(project, device))
    if not folder.is_dir():
        return {"available": False, "files": [], "truncated": False}
    files = []
    truncated = False
    for f in sorted(folder.rglob("*")):
        if not (f.is_file() and f.stat().st_size > 0 and f.suffix.lower() in _CONVERTIBLE_EXTS):
            continue
        if len(files) >= 300:
            truncated = True
            break
        files.append(f.relative_to(folder).as_posix())
    return {"available": True, "files": files, "truncated": truncated}


_FBD_RE = re.compile(r"FBD-\d+", re.IGNORECASE)


@app.get("/api/docs/ingest-map")
def get_ingest_map(project: str, device: str):
    """Traces every raw doc at this target's resolved docs_path through to what it
    actually became -- built so a person can SEE the real pipeline (raw -> converted ->
    distilled spec note -> device-relevant), not just be told it's correct.

    George, 2026-09-25, after getting confused tracing why onboard-suite's 23 POS areas
    looked wrong next to 131+ raw uploaded files: "we need an easy way... some way of
    seeing all the docs uploads on one side, then like an arrow pointing... to the
    ingested docs now... people can visually see ah okay onboarding is right".

    Join key is the FBD-id embedded in both a raw filename ("...(FBD-100318) V5.00.docx")
    and its distilled note's own filename ("FBD-100318-barcode-product-configuration.md")
    -- NOT the prose `**Source:**` citation text, which isn't a stable string to match
    against (e.g. FBD-100183's note cites "POS Hardware Specification V6.00 (FBD-100183,
    ...)" -- title and FBD-id in different clauses, format not consistent note-to-note).
    The FBD-id itself is present and consistent in both places, so that's the real join.
    A raw doc with no FBD-id in its filename (CONOPS decks, crib sheets, ABT nutshell
    pptx, ...) can never be claimed as "became note X" without guessing -- it's reported
    as reference-only if converted, same as a doc whose FBD-id has no current note."""
    project, device = _validated_target(project, device)
    docs = get_docs_folder(project, device)
    docs_path = Path(docs["path"])
    text_dir = runner.SYSTEM_TEST_OPS_ROOT / "dev" / f"{project}-requirements" / "_text"
    specs_dir = SYSTEM_TEST_OPS_KNOWLEDGE / project.lower() / "specs"

    note_by_fbd: dict[str, str] = {}
    if specs_dir.is_dir():
        for note in specs_dir.glob("*.md"):
            m = _FBD_RE.search(note.stem)
            if m:
                note_by_fbd[m.group(0).upper()] = note.name
    total_notes = len(note_by_fbd)

    relevant_reason: dict[str, dict] = {}
    classifier_available = True
    try:
        knowledge = _archive_knowledge_dry_run(project, device)
        relevant_reason = {m["file"]: m for m in knowledge["archived"]}
    except HTTPException:
        # No classifier config for this project yet, or the tool errored -- report the
        # trace anyway (raw -> converted -> distilled still stands on its own), just
        # without the device-relevance layer on top. Never silently 500 the whole view
        # over a secondary layer.
        classifier_available = False

    rows = []
    try:
        raw_files = sorted(f for f in docs_path.rglob("*") if f.is_file() and f.stat().st_size > 0)
    except OSError:
        raw_files = []

    for f in raw_files:
        text_file = text_dir / f"{f.name}.txt"
        converted = text_file.is_file()
        m = _FBD_RE.search(f.name)
        fbd = m.group(0).upper() if m else None
        note_file = note_by_fbd.get(fbd) if fbd else None

        if note_file:
            if not classifier_available:
                rows.append({"file": f.name, "category": "distilled_unclassified", "note": note_file, "reason": None})
            elif note_file in relevant_reason:
                match = relevant_reason[note_file]
                rows.append({"file": f.name, "category": "distilled_relevant", "note": note_file,
                             "reason": match["reason"], "confidence": match["confidence"]})
            else:
                rows.append({"file": f.name, "category": "distilled_not_relevant", "note": note_file, "reason": None})
        elif converted:
            rows.append({"file": f.name, "category": "reference_only", "note": None, "reason": None})
        else:
            rows.append({"file": f.name, "category": "not_converted", "note": None, "reason": None})

    counts = {
        "total_raw": len(rows),
        "distilled_relevant": sum(1 for r in rows if r["category"] == "distilled_relevant"),
        "distilled_not_relevant": sum(1 for r in rows if r["category"] == "distilled_not_relevant"),
        "distilled_unclassified": sum(1 for r in rows if r["category"] == "distilled_unclassified"),
        "reference_only": sum(1 for r in rows if r["category"] == "reference_only"),
        "not_converted": sum(1 for r in rows if r["category"] == "not_converted"),
        "total_distilled_notes": total_notes,
        "relevant_notes": len(relevant_reason) if classifier_available else None,
    }
    return {"docs_path": str(docs_path), "docs_source": docs["source"],
            "classifier_available": classifier_available, "counts": counts, "rows": rows}


@app.post("/api/docs")
async def upload_doc(project: str, device: str, file: UploadFile = File(...), kind: str = "functional"):
    project, device = _validated_target(project, device)
    if kind not in ("functional", "design"):
        raise HTTPException(status_code=400, detail="kind must be 'functional' or 'design'.")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename given.")
    content = await file.read()
    try:
        store.save_doc(project, device, file.filename, content, kind)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True}


# Sized for a real project library, not a toy: Translink's is ~660MB / 352 files
# decompressed (2026-09-23). Still a genuine zip-bomb guard, just not one that blocks
# the actual job. The zip is read straight off UploadFile's on-disk spool rather than
# into memory, so a big archive costs disk, not RAM.
_ZIP_MAX_ENTRIES = 5000
_ZIP_MAX_TOTAL_BYTES = 3 * 1024 * 1024 * 1024  # 3GB decompressed


@app.post("/api/docs/bulk")
async def upload_docs_bulk(project: str, device: str, files: list[UploadFile] = File(...)):
    """Upload several files at once, OR one .zip containing many -- George, 2026-09-22:
    "a way to upload a zip file or folder... instead of me uploading one file by one".
    A .zip's entries are extracted and saved individually (flattened to their basename,
    same as a normal upload -- this folder was never nested); any non-.zip file in the
    same request is saved as-is, so "select 12 files + drag a zip" in one go both work.
    Real zip-bomb guard: refuses if declared entry count/total size is excessive, checked
    BEFORE extracting anything."""
    project, device = _validated_target(project, device)
    saved: list[str] = []
    errors: list[str] = []
    for upload in files:
        name = upload.filename or ""
        if name.lower().endswith(".zip"):
            try:
                # UploadFile already spools to a temp file on disk past ~1MB, so hand
                # zipfile that file object directly -- `await upload.read()` on a 660MB
                # archive would have pulled the entire thing into memory for no reason.
                upload.file.seek(0)
                with zipfile.ZipFile(upload.file) as zf:
                    infos = [i for i in zf.infolist() if not i.is_dir()]
                    if len(infos) > _ZIP_MAX_ENTRIES:
                        errors.append(f"{name}: refused -- {len(infos)} entries exceeds the {_ZIP_MAX_ENTRIES} limit.")
                        continue
                    total = sum(i.file_size for i in infos)
                    if total > _ZIP_MAX_TOTAL_BYTES:
                        errors.append(f"{name}: refused -- {total} decompressed bytes exceeds the {_ZIP_MAX_TOTAL_BYTES} limit.")
                        continue
                    for info in infos:
                        if "__MACOSX/" in info.filename or info.filename.endswith(".DS_Store"):
                            continue  # zip metadata junk, not a real doc -- checked on the full path, not just the flattened basename
                        entry_name = Path(info.filename).name  # flattened -- never trust the zip's own path (traversal-safe)
                        if not entry_name or entry_name.startswith("."):
                            continue  # directory-only entries with no basename, or a dotfile
                        try:
                            store.save_doc(project, device, entry_name, zf.read(info))
                            saved.append(entry_name)
                        except ValueError as exc:
                            errors.append(f"{entry_name}: {exc}")
            except zipfile.BadZipFile:
                errors.append(f"{name}: not a valid zip file.")
            continue
        if not name:
            errors.append("(unnamed file): no filename given.")
            continue
        content = await upload.read()
        try:
            store.save_doc(project, device, name, content)
            saved.append(name)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
    return {"ok": True, "saved": saved, "errors": errors}



# --- Upload review gate (George, 2026-09-23: "a gate here for uploads too, that older
# versioned numbers are not counted... you get a pop up where you say not needed / no and
# skip") ------------------------------------------------------------------------------
# Files land in a staging folder first, get classified, and only what you keep is
# committed. Staged once, not uploaded twice -- a 630MB library over the wire twice would
# be absurd.
_UPLOAD_STAGING: dict[str, dict] = {}


def _ingest_doc_helpers():
    """Reuse ingest_docs.py's OWN version/exclusion rules rather than re-implementing
    them here -- a second copy would drift from the tool that actually does the ingest."""
    tools_dir = _PLATFORM_ROOT.parent.parent / "system-test-ops" / "tools"
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from ingest_docs import excluded_reason, family_key, version_of  # noqa: PLC0415
    return excluded_reason, family_key, version_of


def _classify_staged(names: list[str]) -> dict:
    """Split staged files into keep / superseded / excluded, using the real ingest rules."""
    try:
        excluded_reason, family_key, version_of = _ingest_doc_helpers()
    except Exception:
        return {"keep": names, "superseded": [], "excluded": [], "rules_available": False}

    excluded, families = [], {}
    for rel in names:
        reason = excluded_reason(rel)
        if reason:
            excluded.append({"file": rel, "reason": reason})
            continue
        families.setdefault(family_key(rel), []).append((version_of(rel.split("/")[-1]), rel))

    keep, superseded = [], []
    for members in families.values():
        members.sort(reverse=True)
        keep.append(members[0][1])
        for _, rel in members[1:]:
            superseded.append({"file": rel, "superseded_by": members[0][1]})
    return {"keep": sorted(keep), "superseded": superseded, "excluded": excluded, "rules_available": True}


@app.post("/api/docs/bulk/stage")
async def stage_docs_bulk(project: str, device: str, files: list[UploadFile] = File(...)):
    """Upload once into a staging folder and report what's in it -- older versions of the
    same doc, and non-document noise -- so a human decides before anything is kept."""
    project, device = _validated_target(project, device)
    token = uuid.uuid4().hex
    staging = Path(tempfile.mkdtemp(prefix=f"testops-upload-{token}-"))
    names, errors = [], []
    for upload in files:
        name = upload.filename or ""
        if name.lower().endswith(".zip"):
            try:
                upload.file.seek(0)
                with zipfile.ZipFile(upload.file) as zf:
                    infos = [i for i in zf.infolist() if not i.is_dir()]
                    if len(infos) > _ZIP_MAX_ENTRIES:
                        errors.append(f"{name}: refused -- {len(infos)} entries exceeds the {_ZIP_MAX_ENTRIES} limit.")
                        continue
                    total = sum(i.file_size for i in infos)
                    if total > _ZIP_MAX_TOTAL_BYTES:
                        errors.append(f"{name}: refused -- {total} decompressed bytes exceeds the {_ZIP_MAX_TOTAL_BYTES} limit.")
                        continue
                    for info in infos:
                        if "__MACOSX/" in info.filename or info.filename.endswith(".DS_Store"):
                            continue
                        rel = info.filename.replace("\\", "/")
                        flat = Path(rel).name
                        if not flat or flat.startswith("."):
                            continue
                        (staging / flat).write_bytes(zf.read(info))
                        names.append(rel)  # keep the zip's own path -- archive/ rules need it
            except zipfile.BadZipFile:
                errors.append(f"{name}: not a valid zip file.")
            continue
        if not name:
            errors.append("(unnamed file): no filename given.")
            continue
        (staging / Path(name).name).write_bytes(await upload.read())
        names.append(name)

    verdict = _classify_staged(names)
    _UPLOAD_STAGING[token] = {"dir": str(staging), "project": project, "device": device, "names": names}
    return {"token": token, "errors": errors, **verdict}


class CommitStagedIn(BaseModel):
    token: str
    skip: list[str] = []


@app.post("/api/docs/bulk/commit")
def commit_docs_bulk(body: CommitStagedIn):
    """Keep everything staged except `skip`, then bin the staging folder."""
    staged = _UPLOAD_STAGING.pop(body.token, None)
    if staged is None:
        raise HTTPException(status_code=404, detail="Nothing staged under that token (already committed, or the server restarted).")
    staging = Path(staged["dir"])
    skip = {Path(s).name for s in body.skip}
    saved, errors = [], []
    for rel in staged["names"]:
        flat = Path(rel).name
        if flat in skip:
            continue
        src = staging / flat
        if not src.is_file():
            continue
        try:
            store.save_doc(staged["project"], staged["device"], flat, src.read_bytes())
            saved.append(flat)
        except ValueError as exc:
            errors.append(f"{flat}: {exc}")
    shutil.rmtree(staging, ignore_errors=True)
    return {"ok": True, "saved": saved, "skipped": sorted(skip), "errors": errors}


@app.delete("/api/docs/{project}/{device}/{filename}")
def remove_doc(project: str, device: str, filename: str, kind: str = "functional"):
    project, device = _validated_target(project, device)
    if kind not in ("functional", "design"):
        raise HTTPException(status_code=400, detail="kind must be 'functional' or 'design'.")
    if not store.delete_doc(project, device, filename, kind):
        raise HTTPException(status_code=404, detail="No such file")
    return {"ok": True}


# --- Archive existing docs & knowledge (George, 2026-09-24: re-uploading a fresh device
# library shouldn't leave old derived knowledge notes silently mixed in with what gets
# freshly distilled this time) --------------------------------------------------------
# `tools/archive_knowledge.py` (sibling repo) classifies knowledge notes device-by-device
# and reports a confidence tier per match, but it's all-or-nothing per invocation -- no
# way to ask it to move only some of the matches. Real dry-run data (2026-09-24, Translink
# POS): most matches are medium/low-confidence cross-device mentions, not POS-specific --
# archiving everything the tool reports would sweep away genuinely shared knowledge. So the
# webapp does the actual (partial) move itself: preview calls the tool in --dry-run to get
# reasons/confidence, the human picks a subset, commit moves only that subset -- same
# never-delete, always-move-to-a-timestamped-folder contract the tool itself uses, just
# with the human's selection applied before anything happens.
#
# The preview token used to be an in-memory dict here -- found live, 2026-09-24: George runs
# this server with `uvicorn --reload`, which restarts the worker on any watched file change,
# silently dropping an in-flight token between preview and the human clicking "Archive
# selected" (a real gap of minutes, not a rare race). Persisted via store.py's
# archive_previews table instead, so a reload mid-review no longer loses the selection.


def _archive_knowledge_dry_run(project: str, device: str) -> dict:
    parts = [str(runner._VENV_PYTHON), "tools/archive_knowledge.py",
              "--project", project, "--device", device, "--dry-run"]
    result = subprocess.run(parts, cwd=str(runner.SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise HTTPException(status_code=502, detail=f"archive_knowledge.py --dry-run failed: {result.stderr.strip() or result.stdout.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"archive_knowledge.py returned non-JSON output: {result.stdout[:500]!r}") from exc


@app.post("/api/docs/{project}/{device}/archive/preview")
def preview_archive(project: str, device: str):
    """Both layers in one response: uploaded raw files sitting in this console's own
    upload folder, and derived knowledge/<project>/specs/*.md notes classified against
    this device (with a match reason + confidence tier each, direct from the CLI tool --
    nothing here re-derives or second-guesses that classification, only the SELECTION of
    what to actually archive is this webapp's job, not the classifier's)."""
    project, device = _validated_target(project, device)
    knowledge = _archive_knowledge_dry_run(project, device)
    uploads = store.list_docs(project, device)
    token = uuid.uuid4().hex
    store.save_archive_preview(token, project, device, {
        "archived": knowledge["archived"],  # [{file, reason, confidence}]
        "uploads": [u["filename"] for u in uploads],
    })
    return {"token": token, "knowledge_matches": knowledge["archived"],
            "knowledge_kept_count": len(knowledge["kept"]), "uploads": uploads}


class CommitArchiveIn(BaseModel):
    token: str
    knowledge_files: list[str] = []  # subset of preview's knowledge_matches[].file to actually archive
    upload_files: list[str] = []     # subset of preview's uploads[].filename to actually archive


@app.post("/api/docs/{project}/{device}/archive/commit")
def commit_archive(project: str, device: str, body: CommitArchiveIn):
    project, device = _validated_target(project, device)
    preview = store.pop_archive_preview(body.token)
    if preview is None:
        raise HTTPException(status_code=404, detail="Nothing previewed under that token (already committed, expired, or the server restarted). Run preview again.")
    if preview["project"] != project or preview["device"] != device:
        raise HTTPException(status_code=400, detail="Token was previewed for a different project/device.")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    archived_knowledge: list[str] = []
    knowledge_errors: list[str] = []
    knowledge_archive_dir: Path | None = None
    reasons_by_file = {m["file"]: m for m in preview["archived"]}
    selected_knowledge = [f for f in body.knowledge_files if f in reasons_by_file]
    if selected_knowledge:
        specs_dir = SYSTEM_TEST_OPS_KNOWLEDGE / project.lower() / "specs"
        archive_dir = specs_dir / "_archive" / stamp
        n = 1
        while archive_dir.exists():
            n += 1
            archive_dir = specs_dir / "_archive" / f"{stamp}-{n}"
        for filename in selected_knowledge:
            src = specs_dir / filename
            if not src.is_file():
                knowledge_errors.append(f"{filename}: not found in {specs_dir} (already archived by another run?)")
                continue
            archive_dir.mkdir(parents=True, exist_ok=True)
            src.rename(archive_dir / filename)
            archived_knowledge.append(filename)
        if archived_knowledge:
            knowledge_archive_dir = archive_dir
            manifest = archive_dir / "ARCHIVE-MANIFEST.md"
            lines = [f"# Archived knowledge notes — {project}/{device} — {stamp}", "",
                     "Selected via the Test-Ops Console's Archive review step (a human-chosen subset of",
                     "what `tools/archive_knowledge.py --dry-run` reported, not the full match list).", ""]
            for filename in archived_knowledge:
                m = reasons_by_file[filename]
                lines.append(f"- `{filename}` — {m['reason']} (confidence: {m['confidence']})")
            manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    archived_uploads: list[str] = []
    upload_errors: list[str] = []
    selected_uploads = [f for f in body.upload_files if f in set(preview["uploads"])]
    if selected_uploads:
        uploads_dir = Path(store.uploads_dir_path(project, device))
        upload_archive_dir = uploads_dir / "_archive" / stamp
        for filename in selected_uploads:
            safe_name = Path(filename).name
            src = uploads_dir / safe_name
            if not src.is_file():
                upload_errors.append(f"{filename}: not found (already archived or removed?)")
                continue
            upload_archive_dir.mkdir(parents=True, exist_ok=True)
            src.rename(upload_archive_dir / safe_name)
            archived_uploads.append(safe_name)

    return {
        "ok": True,
        "archived_knowledge": archived_knowledge,
        "knowledge_errors": knowledge_errors,
        "archived_uploads": archived_uploads,
        "upload_errors": upload_errors,
        "archive_dir": str(knowledge_archive_dir) if knowledge_archive_dir else None,
    }


# Confirmed non-client (George, 2026-09-22: "remove sit1 not a project") -- SIT1 is real,
# mirrored data (Resources/Common/ConfigSets/SIT1 in the real `sit` repo), but it sits
# there alongside that repo's own Generic/Product/Universal scaffolding, not the real
# clients (Translink, NJT, NTA, EdinTram, Rouen, UKBus, PerthSys). It's the SIT
# framework's own internal/demo ConfigSet, not a Flowbird project -- excluded here only,
# never deleted from the mirror itself (not ours to touch, and it may serve a real
# framework purpose there).
NON_CLIENT_MIRRORED_PROJECTS = {"SIT1"}


@app.get("/api/taxonomy")
def get_taxonomy():
    """Real project -> device -> model taxonomy, parsed live from the mirrored
    EquipmentTypes.json (model/devices.py). Same data the front-end target-switcher uses."""
    out = {}
    for project in devices.list_mirrored_projects():
        if project in NON_CLIENT_MIRRORED_PROJECTS:
            continue
        registry = devices.load_registry(project)
        out[project] = {
            et.device_type: et.equipment_type_names
            for et in registry.equipment_types
            if et.device_type in KEEP_DEVICE_TYPES
        }
    return out


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
def get_pipeline_detail(pipeline_id: str, project: str | None = None):
    """Full ordered step list for one pipeline, straight from its real YAML file.

    Composite `{id, ref: <other-pipeline>}` steps are expanded to the steps that will
    REALLY run, using the same runner.py flattening the executor itself uses. Without
    this, new-suite-from-docs ("Build") showed two bare rows with no kind and no command
    -- George, 2026-09-23: "what is build? just human things its not needed, there is no
    run to be done here." It was in fact fully runnable; the page just wasn't showing the
    ~20 real inlined steps behind those two rows."""
    try:
        p = pipelines.load_pipeline(pipeline_id)
    except (KeyError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if any(s.is_composite_ref for s in p.steps):
        try:
            steps = runner._flatten_steps(p, project or "")
        except Exception:
            steps = p.steps  # a bad/circular ref shouldn't 500 the page -- show the raw shape
    else:
        steps = p.steps
    return {
        "id": p.id,
        "description": p.description,
        "trigger": p.trigger.model_dump(),
        "guardrails": p.guardrails,
        "steps": [s.model_dump() for s in steps],
        "inputs": [i.model_dump() for i in p.inputs],
        "preconditions": p.preconditions,
        "runnable": runner.is_runnable(p.id),
    }


@app.get("/api/pipelines/{pipeline_id}/walkthrough")
def get_pipeline_walkthrough(pipeline_id: str):
    """The real, already-authored `.claude/commands/{pipeline_id}.md` teammate walkthrough
    for this pipeline, if one exists -- George, 2026-09-28: "can we not do the same thing
    for every pipeline" (referring to audit-flows' step-by-step guide card). Reuses this
    real content rather than re-authoring 22 separate prose blocks that would drift from
    the actual slash command: `available: false` for the handful of pipelines that don't
    have one yet (composite pipelines, or ones genuinely not written up) -- shown honestly
    on the console rather than inventing a walkthrough for a pipeline that doesn't have one."""
    try:
        pipelines.load_pipeline(pipeline_id)  # 404s the same way get_pipeline_detail does
    except (KeyError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    path = pipelines.commands_root() / f"{pipeline_id}.md"
    if not path.is_file():
        return {"available": False, "markdown": None}
    return {"available": True, "markdown": path.read_text(encoding="utf-8")}


@app.post("/api/pipelines/{pipeline_id}/run")
def run_pipeline(pipeline_id: str, body: RunRequest):
    """Kicks off a REAL run of any pipeline (2026-09-14: the RUNNABLE_PIPELINES allowlist
    is gone — every pipeline runs through the generic step-executor in runner.py). Safety
    now lives at the step level: any step that would `push --commit` is always forced into
    a human-approval gate there, never here.

    A pipeline's own `inputs:` list (e.g. ingest-docs' required `docs_path`) is the source
    of truth for what else a run needs beyond project/device — checked here so a missing
    one 400s with a clear message instead of the run silently starting with an unresolved
    `{placeholder}` in a step command."""
    try:
        pipeline = pipelines.load_pipeline(pipeline_id)
    except (KeyError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    # project/device are top-level RunRequest fields; old_suite_id/new_suite_id/suite_id are
    # derived automatically from suite_mappings by runner._build_params — only inputs
    # outside that system-derived set (e.g. ingest-docs' docs_path) need a real value here.
    _SYSTEM_DERIVED_INPUTS = {"project", "device", "old_suite_id", "new_suite_id", "suite_id"}
    for inp in pipeline.inputs:
        if inp.name in _SYSTEM_DERIVED_INPUTS:
            continue
        if inp.required and not body.extra_inputs.get(inp.name):
            raise HTTPException(status_code=400, detail=f"Missing required input '{inp.name}' for pipeline '{pipeline_id}'.")

    try:
        run_id = runner.start_run(pipeline_id, body.project, body.device, body.extra_inputs)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"run_id": run_id}


@app.get("/api/pipelines/runs/{run_id}")
def get_pipeline_run(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    # Real, server-side auto-approve state folded into the same poll the UI already makes
    # every 2s -- no separate round-trip needed just to know whether it's on.
    return {**run, "auto_approve": run_id in runner._auto_approve_runs}


@app.get("/api/pipelines/runs/{run_id}/steps")
def get_pipeline_run_steps(run_id: str):
    """Granular per-step progress for one run — the poll target for the step list UI."""
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    steps = store.get_steps(run_id)
    for s in steps:  # tells the UI which waiting steps get a "Review & decide" pop-up
        s["has_review"] = s["kind"] == "human" and reviews.has_review(run, s["step_id"])
    return steps


@app.get("/api/pipelines/runs/{run_id}/steps/{step_id}/review")
def get_step_review(run_id: str, step_id: str):
    """Everything the Review & decide pop-up shows for a waiting human step."""
    try:
        spec = reviews.get_review(run_id, step_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if spec is None:
        raise HTTPException(status_code=404, detail="This step has no review.")
    return spec


class StepDecisionIn(BaseModel):
    choices: list[str] | None = None
    note: str | None = None
    by: str


class StepStopIn(BaseModel):
    note: str | None = None
    by: str


@app.post("/api/pipelines/runs/{run_id}/steps/{step_id}/decide")
def decide_step(run_id: str, step_id: str, body: StepDecisionIn):
    """Record a person's choice + note for a waiting human step, then continue the run."""
    try:
        reviews.decide(run_id, step_id, body.choices, body.note, body.by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except runner.CaseReviewPendingError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except runner.TargetNotApprovedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return {"ok": True}


@app.post("/api/pipelines/runs/{run_id}/steps/{step_id}/stop")
def stop_step(run_id: str, step_id: str, body: StepStopIn):
    """The person does not approve: stop the run here, with who and why on record."""
    try:
        reviews.stop(run_id, step_id, body.note, body.by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"ok": True}


@app.post("/api/pipelines/runs/{run_id}/steps/{step_id}/resolve")
def resolve_pipeline_run_step(run_id: str, step_id: str):
    """Advances a step that's currently `waiting_human` (a plain confirmation, or a real
    `push --commit` approval gate) and resumes the run. This is the real "Approve & Push"
    action — there is no other path in this app that lets a run past that gate."""
    step = store.get_step(run_id, step_id)
    if step is None:
        raise HTTPException(status_code=404, detail="No such step")
    if step["status"] != "waiting_human":
        raise HTTPException(status_code=409, detail=f"Step '{step_id}' is not waiting for approval (status={step['status']}).")
    if reviews.needs_decision(run_id, step_id):
        raise HTTPException(status_code=409, detail=f"Step '{step_id}' needs a choice -- use Review & decide.")
    try:
        runner.resolve_step(run_id, step_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except runner.TargetNotApprovedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except runner.CaseReviewPendingError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"ok": True}


@app.post("/api/pipelines/runs/{run_id}/steps/{step_id}/retry")
def retry_pipeline_run_step(run_id: str, step_id: str):
    """Resumes a failed run from the step that actually failed, not from step 1 -- some
    steps (author_area's per-area agent calls) take several minutes each, so a late
    failure in a long onboard-suite run shouldn't throw away everything before it."""
    try:
        runner.retry_failed_step(run_id, step_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"ok": True}


@app.post("/api/pipelines/runs/{run_id}/cancel")
def cancel_pipeline_run(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    runner.cancel_run(run_id)
    return {"ok": True}


class AutoApproveIn(BaseModel):
    enabled: bool


@app.post("/api/pipelines/runs/{run_id}/auto-approve")
def set_run_auto_approve(run_id: str, body: AutoApproveIn):
    """George, 2026-09-30: "plus auto mode seems to not actual work?" -- it was a
    browser-side (JS) toggle that silently reset on any page reload/navigation, with no
    visible sign it had turned off. The run itself already lives server-side; this flag now
    does too (runner._auto_approve_runs, same in-memory pattern as _cancel_events), so it
    survives navigating away from the page and doesn't depend on any one browser tab."""
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    runner.set_auto_approve(run_id, body.enabled)
    return {"ok": True}


@app.get("/api/pipelines/runs/{run_id}/auto-approve")
def get_run_auto_approve(run_id: str):
    return {"enabled": run_id in runner._auto_approve_runs}


@app.get("/api/pipelines/runs/{run_id}/steps/{step_id}/artifact")
def get_pipeline_step_artifact(run_id: str, step_id: str):
    """Real file a loop-fanned area step (author_area[<area>] / push_area[<area>]) actually
    produced -- George: "what happened to giving a link to where the test cases are for the
    area to push? so we can actually check it". The push gate's own warning said "check what
    was drafted... above", but "above" was only the agent's raw reply text -- never an
    actual link to the real proposals/<project>-<device>-suite-restructure/<area>.cases.yaml
    gherkin-author wrote. Read-only; the path is built server-side from the RUN's own
    project/device (never client-supplied) plus the area parsed from the step id, and
    checked to still resolve inside proposals/ -- the only place this step ever writes."""
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    area = runner.step_area(step_id)
    if area is None:
        raise HTTPException(status_code=400, detail=f"'{step_id}' isn't a per-area step.")
    rel_path = Path("proposals") / f"{run['project']}-{run['device']}-suite-restructure" / f"{area}.cases.yaml"
    root = runner.SYSTEM_TEST_OPS_ROOT.resolve()
    full_path = (root / rel_path).resolve()
    if root != full_path and root not in full_path.parents:
        raise HTTPException(status_code=400, detail="Resolved path escapes the repo.")
    if not full_path.is_file():
        return {"available": False, "path": str(rel_path)}
    text = full_path.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > 200_000
    return {"available": True, "path": str(rel_path), "content": text[:200_000], "truncated": truncated}


@app.get("/api/pipelines/{pipeline_id}/last-run")
def get_last_pipeline_run(pipeline_id: str, project: str, device: str):
    """A real 'last run' timestamp for this pipeline+target, or null if never run.
    Only meaningful for pipelines that are actually runnable (today: audit)."""
    return store.get_latest_run(pipeline_id, project, device) or {"status": None}


@app.get("/api/runs/recent")
def get_recent_runs_across_everything(limit: int = 50):
    """Real run activity across every pipeline/project/device -- the Reports tab's "Tool
    activity" feed (George, 2026-09-28)."""
    return store.get_recent_runs(limit=limit)


@app.get("/api/pipelines/{pipeline_id}/runs")
def get_pipeline_runs(pipeline_id: str, project: str, device: str, limit: int = 20):
    """Real run history for this pipeline+target (ISSUES.md round 4's Log tab ask) --
    every real row, not just the latest. `extra_inputs` (e.g. which fix_version/JIRA
    key(s) a run was actually given) comes back per-run where it was recorded; older runs
    predating that column just have it as null, shown honestly, never backfilled."""
    return store.get_runs(pipeline_id, project, device, limit=limit)


@app.get("/api/pipelines/ingest-docs/runs/{run_id}/knowledge-files")
def get_ingest_docs_run_knowledge_files(run_id: str, project: str):
    """Which real knowledge/{project}/specs/*.md file(s) a specific past ingest-docs run
    actually produced -- for update-suite-from-docs' "just pick one of my recent ingests"
    ask (George, 2026-09-28: "people will more likely know this is the recent ingest time I
    did, and choose that to confirm what knowledge docs to be examined").

    Deliberately NOT a filename guess off the source doc -- `distil` is an agent step with
    no enforced naming contract back to its source, so pattern-matching a slug would be
    exactly the kind of invented fact this whole app exists to avoid. Instead this is a
    real, grounded correlation: the `distil` step's own recorded started_at/finished_at
    window (when it actually ran) against each knowledge file's real filesystem mtime.
    `distil` is the only step in ingest-docs that ever writes into knowledge/{project}/specs/,
    so a file whose mtime falls inside that exact window was, in fact, written by this run."""
    step = store.get_step(run_id, "distil")
    if step is None or not step.get("started_at"):
        return {"available": False, "reason": "No recorded distil step for this run yet (still running, or predates this feature).", "files": []}
    started = datetime.fromisoformat(step["started_at"])
    finished_raw = step.get("finished_at")
    finished = datetime.fromisoformat(finished_raw) if finished_raw else datetime.now(timezone.utc)
    buffer = timedelta(seconds=120)  # clock-skew/filesystem-flush margin, not a guess window
    specs_dir = runner.SYSTEM_TEST_OPS_ROOT / "knowledge" / project.lower() / "specs"
    if not specs_dir.is_dir():
        return {"available": True, "files": []}
    matches = []
    for f in sorted(specs_dir.glob("*.md")):
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if started - buffer <= mtime <= finished + buffer:
            matches.append({
                "path": f"knowledge/{project.lower()}/specs/{f.name}",
                "modified_at": mtime.isoformat(),
            })
    return {"available": True, "files": matches}


@app.get("/api/pipelines/runs/{run_id}/cost")
def get_pipeline_run_cost(run_id: str):
    """Real total cost/tokens for one run, summed from its own agent steps' recorded
    `claude -p --output-format json` usage (see runner.py). `available: false` for a run
    with no cost-tracked steps -- predates the tracking, or genuinely had none (pure
    cli/human/gate pipeline)."""
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    return store.get_run_cost(run_id)


class ScheduledCheckIn(BaseModel):
    project: str
    device: str
    enabled: bool
    interval_days: int = 7


class ScheduledCheckTargetIn(BaseModel):
    project: str
    device: str


@app.get("/api/scheduled-checks")
def list_scheduled_checks():
    """Every target's real scheduled-scan settings (enabled/interval/last run) -- powers
    the Scheduled checks page. Never includes a target that hasn't been explicitly opted
    in (nothing is scanned by default)."""
    return store.list_scheduled_checks()


@app.post("/api/scheduled-checks")
def set_scheduled_check(body: ScheduledCheckIn):
    if body.interval_days < 1:
        raise HTTPException(status_code=400, detail="interval_days must be at least 1.")
    if body.interval_days > 365:
        raise HTTPException(status_code=400, detail="interval_days must be 365 or fewer.")
    # A blank target used to create an enabled row the background poller would then scan
    # forever against a docs_path spanning every project (2026-09-23 sweep).
    _validated_target(body.project, body.device)
    store.set_scheduled_check(body.project, body.device, body.enabled, body.interval_days)
    return {"ok": True}


@app.get("/api/scheduled-checks/suggestions")
def get_scheduled_scan_suggestions():
    """The actionable feed itself (George, 2026-09-22: "a good report to get going with
    actionables") -- every completed scheduled-scan run not yet marked reviewed, across
    every target, newest first.

    CHANGED 2026-09-30 (George, real bug found live): this used to count every completed
    run as a "suggestion" -- including one where the agent explicitly declined to
    recommend anything ("I won't invent findings... not recommending a pipeline"),
    which showed as a notification implying something needed attention when it didn't.
    `suggest_next` now replies with a strict JSON envelope (has_recommendation/summary/
    recommendation) -- only runs where has_recommendation is genuinely true are
    surfaced here. A run whose summary doesn't parse as that JSON (a legacy run from
    before this change, or a genuine agent failure) is treated the same conservative
    way -- not shown as an actionable suggestion, since we can't confirm it has one."""
    runs = store.get_unreviewed_scheduled_scan_suggestions()
    out = []
    for run in runs:
        try:
            parsed = json.loads(run.get("summary") or "")
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(parsed, dict) or not parsed.get("has_recommendation"):
            continue
        out.append({**run, "summary": parsed.get("summary") or "", "recommendation": parsed.get("recommendation") or ""})
    return out


@app.post("/api/scheduled-checks/suggestions/{run_id}/review")
def review_scheduled_scan_suggestion(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    store.mark_scheduled_scan_suggestion_reviewed(run_id)
    return {"ok": True}


@app.post("/api/scheduled-checks/run-now")
def run_scheduled_check_now(body: ScheduledCheckTargetIn):
    _validated_target(body.project, body.device)
    """Manual "Run now" -- same real scheduled-scan pipeline the background poller uses,
    just triggered on demand. Marks last_run_at too, so the automatic poller doesn't
    immediately consider this target due again right after a manual run."""
    run_id = runner.start_scheduled_scan(body.project, body.device)
    store.mark_scheduled_check_run(body.project, body.device, run_id, datetime.now(timezone.utc).isoformat())
    return {"ok": True, "run_id": run_id}


@app.get("/api/ai-usage")
def get_ai_usage():
    """Per-pipeline average real cost/tokens per run, across every run with recorded cost
    data -- the dashboard's AI-usage widget (George, 2026-09-22: "a pipeline AI token
    usage visual to each pipeline... a medium sized quick view bit on main page of average
    tokens used per run"). Tool-wide, not scoped to the current target."""
    return store.get_all_pipelines_cost_summary()


@app.get("/api/run-comments")
def get_run_comments(project: str, device: str, which: str = "new", last_n: int = 5):
    """Real TestRail run-result comments (reviewer notes on Passed/Failed/Invalid/etc),
    read-only. Answers George's 2026-09-08 question directly: not built before this."""
    if which not in ("old", "new"):
        raise HTTPException(status_code=400, detail="which must be 'old' or 'new'")
    return runner.get_run_comments(project, device, which, last_n)


class RelevancePreviewIn(BaseModel):
    project: str
    docs_path: str


@app.post("/api/docs/relevance-preview")
def preview_docs_relevance(body: RelevancePreviewIn):
    """Real convert + relevance-gate check, standalone, before committing to a tracked
    Ingest run (George, 2026-09-22: "an initial review of the docs before ingesting, so
    it can pass the gate"). No AI, no distil -- just the same two real steps a run would
    hit first, so a bad upload is caught here rather than mid-run."""
    if not body.docs_path.strip() or not Path(body.docs_path).is_dir():
        raise HTTPException(status_code=400, detail=f"docs_path is not a readable folder: {body.docs_path!r}")
    return runner.preview_docs_relevance(body.project, body.docs_path)


@app.get("/api/suite-sections")
def get_suite_sections(project: str, device: str):
    """Real, live section tree for the target's new suite -- the checkbox tree behind
    targeted-run (George, 2026-09-22: "select EMV, not Sign On"). Read-only."""
    return runner.get_suite_sections(project, device)


class AskIn(BaseModel):
    project: str
    device: str | None = None
    question: str


@app.post("/api/ask")
def post_ask(body: AskIn):
    """The 'ask' box next to the target picker -- a real, synchronous one-shot agent call
    (not a background pipeline run), scoped to the current project/device. See
    runner.ask_question for the grounding rules and the 5-state honest-non-answer taxonomy."""
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question must not be empty.")
    return runner.ask_question(body.project, body.device, question)


@app.get("/api/suite-comparison")
def get_suite_comparison(project: str, device: str):
    """Real, live old-vs-new case counts (two read-only TestRail pulls) -- one of the
    'suggestions' from ISSUES.md, now buildable with old_suite_id stored."""
    return runner.compare_suite_case_counts(project, device)


@app.get("/api/suite-name-drift")
def get_suite_name_drift(project: str, device: str):
    """Real, live check: does the display name stored for this target's old/new suite
    still match what TestRail actually calls it right now (George: 'do we need to ensure
    the naming is correct for the ID or refresh if been changed')."""
    return runner.check_suite_name_drift(project, device)


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


@app.get("/api/confidence-score")
def get_confidence_score():
    """Coverage confidence score — the 3 real inputs you picked (spec citation %, gap-free %,
    automation-reference %), equally weighted, POS/Translink only (the one target with real
    captured data). Same fixture convention as build-stats/run-health: real numbers from a
    real snapshot, not a live TestRail call. Never shown as a bare number — the breakdown of
    all 3 inputs travels with it so it's never opaque."""
    path = FIXTURES / "pos-confidence-score.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No confidence-score fixture found")
    data = json.loads(path.read_text(encoding="utf-8"))
    data["is_fixture"] = True
    data["fixture_note"] = "Real citation/automation/gap numbers, POS suite 30253, 2026-09-28 — not a live TestRail call."
    return data


_GAP_PROJECT_PATH_HINTS = {
    "translink": ("tfts-system-test", "reports\\translink", "reports/translink",
                  "etm-suite-restructure", "gv-suite-restructure", "hhd-suite-restructure",
                  "pv-suite-restructure", "tvm-suite-restructure", "knowledge\\translink", "knowledge/translink"),
    "njt": ("knowledge\\njt", "knowledge/njt", "njt-fr-suite-restructure"),
}


def _infer_gap_project(file_path: str) -> str | None:
    """Best-effort project tag from a marker's file path -- a real, checked mapping (not
    a guess at content) built from the actual real directory layout under system-test-ops
    (`reports/tfts-system-test/` = Translink's real TestRail project name, `knowledge/njt/`
    = NJT, etc). Returns None (not a project) for markers under shared/common paths like
    proposals/coherence-audit -- those aren't any one project's, so scoping them to one
    would be a fabrication, not a fact."""
    lowered = file_path.lower()
    for project, hints in _GAP_PROJECT_PATH_HINTS.items():
        if any(h in lowered for h in hints):
            return project
    return None


# Device tag, same honest approach as _infer_gap_project: real path-hint checks against the
# actual system-test-ops directory/naming convention (<device>-suite-restructure/,
# coherence-audit/fixes/<device>-*, knowledge/flows/<project>-<device>-*), never a content
# guess. Checked against the real gaps.json fixture's actual paths, 2026-09-18 (ISSUES.md:
# "if I change target to Translink POS and Translink ETM then device GAPs will differ").
# A marker with no matching hint gets device=None -- an honest "not inferable", not a guess.
#
# FOUND LIVE 2026-09-30 (George: "i have 10 markers for gaps and unconfirmed after doing a
# refresh against new docs?" -- real total was 171 for POS alone): the fresh distil run for
# Translink/POS wrote knowledge/translink/specs/POS-FS-*.md and POS-Topology-*.md -- a
# device-CODE-PREFIXED filename inside specs/, a naming convention this hint list had never
# seen (it only knew directory-name conventions like pos-suite-restructure/, fixes/pos/).
# None of the existing "pos" hints match "specs/pos-fs-operator.md" (no surrounding dashes),
# so all 22 new notes silently inferred device=None and vanished from the Translink/POS
# Gaps page -- leaving only the handful of older FBD-*-pos-*.md markers that happened to
# contain literal "-pos-". Added a `specs/<device>-` / `specs\<device>-` prefix hint for
# every device so this naming convention (now the real one standards-keeper produces) is
# recognised for all of them, not just POS.
_GAP_DEVICE_PATH_HINTS = {
    "etm": ("etm-suite-restructure", "njt-fr-suite-restructure", "-etm-", "fixes\\etm",
            "fixes/etm", "fixes\\etm-deep-audit", "knowledge\\njt\\specs", "knowledge/njt/specs",
            "specs\\etm-", "specs/etm-"),
    "pos": ("pos-suite-restructure", "-pos-", "fixes\\pos", "fixes/pos",
            "specs\\pos-", "specs/pos-"),
    "gv": ("gv-suite-restructure", "-gv-", "fixes\\gv", "fixes/gv",
           "specs\\gv-", "specs/gv-"),
    "hhd": ("hhd-suite-restructure", "-hhd-", "fixes\\hhd", "fixes/hhd",
            "specs\\hhd-", "specs/hhd-"),
    "pv": ("pv-suite-restructure", "-pv-", "fixes\\pv", "fixes/pv",
           "specs\\pv-", "specs/pv-"),
    "tvm": ("tvm-suite-restructure", "-tvm-", "fixes\\tvm", "fixes/tvm",
            "specs\\tvm-", "specs/tvm-"),
    "bos": ("bos-abt-suite-restructure", "abt-", "fixes\\abt", "fixes/abt", "spec-grounded\\abt", "spec-grounded/abt",
            "specs\\bos-", "specs/bos-"),
}


def _infer_gap_device(file_path: str) -> str | None:
    lowered = file_path.lower()
    for device, hints in _GAP_DEVICE_PATH_HINTS.items():
        if any(h in lowered for h in hints):
            return device.upper()
    return None


def _load_knowledge_device_map(project: str) -> dict:
    """Real, cited device classification for knowledge/{project}/specs/*.md, produced by
    `tools/classify_knowledge_notes.py` (ingest-docs' classify_knowledge_devices step). Empty
    dict (not an error) when no map exists yet for this project -- older projects/notes fall
    back to the path-hint guesser below rather than blocking on a one-time backfill."""
    path = runner.SYSTEM_TEST_OPS_ROOT / "knowledge" / project.lower() / "specs" / "_device-map.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("notes", {})
    except (json.JSONDecodeError, OSError):
        return {}


def _gap_devices_for(file_path: str, device_map: dict) -> list[str]:
    """George, 2026-09-30: "we need to know it is a translink project but that shouldn't
    determine how we store our knowledge and distill it" -- the project is a static fact of
    the folder a marker's file lives in; the device never was, and guessing it from filename
    substrings was fragile (Device-Endpoints-STE12-pv-and-pos-local-services.md, a note that
    genuinely covers BOTH PV and POS, matched "-pos-" as a substring of "...pv-and-pos-local..."
    and got silently POS-only, leaking PV-specific markers into a POS-scoped view). Prefers the
    real, cited, possibly-multi-device classification from classify_knowledge_notes.py when
    this exact file was covered by it; falls back to the old single-device path-hint guess only
    for files it hasn't classified (older notes, non-knowledge paths like reports/proposals)."""
    basename = file_path.replace("\\", "/").rsplit("/", 1)[-1]
    if basename in device_map:
        return device_map[basename].get("devices", [])
    single = _infer_gap_device(file_path)
    return [single] if single else []


@app.get("/api/gap-register")
def get_gap_register(
    limit: int = 25, offset: int = 0, project: str | None = None,
    device: str | None = None, category: str | None = None,
):
    """Real GAP/UNCONFIRMED markers, from an actual `gap-register` run over the real repo.
    Supports real offset/limit pagination.

    SIMPLIFIED 2026-09-29 (ISSUES.md, real ask + a real bug this fixes): the old
    project/device/common/bespoke 4-way scope split defaulted to "project" -- which mixes
    every device's markers together, so a marker tagged Translink/ETM could show while
    targeting Translink/POS ("Im pretty sure the gaps related to all things translink...
    even though im targeted POS"). Confirmed live: that was a real default-scope bug, not a
    misread. Now: `project` alone filters to that project (any device); `project` + `device`
    both given filters to exactly that pair -- there is no other mode. The Gaps page always
    passes both now. Charts that want the repo-wide picture (e.g. Health's "Gaps by device")
    still work by passing neither.

    UPDATED 2026-09-30: a marker's device(s) now prefer the real classify_knowledge_notes.py
    map over the old path-hint guess -- see `_gap_devices_for`. A marker can genuinely belong
    to more than one device; `device["device"]` stays a single value for backward-compat display
    (repo-wide chart, the gap-answer modal's pre-filled field) but the project+device FILTER
    below checks the full `devices` list, so a multi-device note now correctly shows under
    every device it actually covers instead of exactly one.
    """
    # Validated 2026-09-23 (end-to-end sweep): limit=-1 previously ignored the limit and
    # dumped all 972 markers (~219KB), offset=-1 silently returned an empty page beside a
    # non-zero total -- while the sibling /api/run-comments already 400s on a bad `which`.
    # Ceiling is generous on purpose -- "fetch them all" is a real, legitimate call (there
    # are ~972 markers repo-wide, and the Health dashboard chart relies on it).
    if limit < 1 or limit > 2000:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 2000.")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be 0 or greater.")
    path = FIXTURES / "gaps.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No gap-register fixture found")
    markers = json.loads(path.read_text(encoding="utf-8"))
    device_maps: dict[str, dict] = {}
    for m in markers:
        m["project"] = _infer_gap_project(m["file"])
        if m["project"] and m["project"] not in device_maps:
            device_maps[m["project"]] = _load_knowledge_device_map(m["project"])
        devices = _gap_devices_for(m["file"], device_maps.get(m["project"], {}))
        m["devices"] = devices
        # For a multi-device marker, showing an arbitrary "first" device would contradict
        # the very filter that surfaced it (e.g. a POS+PV note appearing under device=POS
        # but reporting "device": "PV") -- when a specific device was asked for, that's the
        # one relevant to this view and is guaranteed to already be in `devices`. Only the
        # repo-wide/project-only case (no device asked for) falls back to an arbitrary pick,
        # purely for the "Gaps by device" chart's bucketing.
        m["device"] = (device.upper() if device and device.upper() in devices else (devices[0] if devices else None))
    if project and device:
        markers = [m for m in markers if m["project"] == project.lower() and device.upper() in m["devices"]]
    elif project:
        markers = [m for m in markers if m["project"] == project.lower()]
    # George, 2026-09-28: "re-write all" GAP/UNCONFIRMED markers in plain English -- merged
    # in here from clarify-gaps' real output, keyed by (file, line) -- the same stable
    # identity gap-register's own mechanical grep uses. A marker with no cached rewrite yet
    # (clarify-gaps never run for it) just has no `plain_english` field -- shown honestly
    # as the raw marker text, never a fabricated rewrite.
    if project:
        clarify_path = runner.SYSTEM_TEST_OPS_ROOT / "reports" / project / "clarify-gaps" / "plain-english.json"
        if clarify_path.is_file():
            try:
                rewrites = {(r["file"], r["line"]): r["plain_english"] for r in json.loads(clarify_path.read_text(encoding="utf-8"))}
            except (json.JSONDecodeError, KeyError):
                rewrites = {}
            for m in markers:
                pe = rewrites.get((m["file"], m["line"]))
                if pe:
                    m["plain_english"] = pe
    # George, 2026-10-01: sort gaps by what would close them (group-gaps pipeline). Each marker gets its
    # group; with a device selected, gaps that only concern another device are left out of the list (and
    # counted) instead of padding a POS to-do list. Markers the pipeline has not classified yet keep working.
    groups_by_loc: dict[tuple[str, str], dict] = {}
    if project:
        gp = runner.SYSTEM_TEST_OPS_ROOT / "reports" / project / "clarify-gaps" / "gap-groups.expanded.json"
        if gp.is_file():
            try:
                groups_by_loc = {(r["file"], str(r["line"])): r for r in json.loads(gp.read_text(encoding="utf-8"))}
            except (json.JSONDecodeError, KeyError, TypeError):
                groups_by_loc = {}
    hidden_other_device = 0
    if groups_by_loc:
        kept = []
        for m in markers:
            g = groups_by_loc.get((m["file"], str(m["line"])))
            m["category"] = g["category"] if g else None
            if g:
                m.update(evidence=g["evidence"], spec_ref=g["spec_ref"], scoped_devices=g["devices"],
                         gap_id=g.get("gap_id"), summary=g.get("summary") or None, question=g.get("question") or None)
                if device and (g["category"] == "other-device" or not ("ALL" in g["devices"] or device.upper() in g["devices"])):
                    hidden_other_device += 1
                    continue
            kept.append(m)
        markers = kept
    category_counts: dict[str, int] = {}
    for m in markers:
        k = m.get("category") or "unclassified"
        category_counts[k] = category_counts.get(k, 0) + 1
    if category:
        markers = [m for m in markers if (m.get("category") or "unclassified") == category]
    return {
        "total": len(markers), "shown": markers[offset:offset + limit],
        "offset": offset, "limit": limit, "is_fixture": True,
        "grouped": bool(groups_by_loc), "category_counts": category_counts,
        "hidden_other_device": hidden_other_device,
    }


class GapImportIn(BaseModel):
    csv_text: str
    by: str | None = None


@app.get("/api/gap-export")
def export_gaps(project: str, device: str | None = None):
    """The grouped gaps as a CSV for reviewers to fill in (Verdict / Answer / Answered by / Evidence)."""
    from fastapi.responses import FileResponse
    try:
        path = gap_exchange.export_csv(project, device)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (RuntimeError, OSError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    name = f"gaps-{project.lower()}-{(device or 'all').lower()}-{datetime.now().strftime('%Y-%m-%d')}.csv"
    return FileResponse(path, media_type="text/csv", filename=name)


@app.post("/api/gap-import")
def import_gaps(project: str, body: GapImportIn, device: str | None = None):
    """Take back a filled-in export: every answered row is recorded in the gap-answers log, matched to
    its gap by Gap ID. Bad rows are reported, never block the good ones; nothing edits a case."""
    try:
        return gap_exchange.import_csv(project, device, body.csv_text, body.by)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except csv.Error as exc:
        raise HTTPException(status_code=400, detail=f"That does not look like the exported CSV: {exc}") from exc


@app.post("/api/gap-register/refresh")
def refresh_gap_register():
    """Real 're-check against newly ingested docs' action (George, 2026-09-29) -- runs the
    actual gap-register CLI live (a cheap, read-only grep over knowledge/proposals/reports,
    no AI), replacing the static fixture. Not a fabricated re-scan -- the exact same command
    that produced the fixture originally, just run again, now."""
    return runner.refresh_gap_register()


@app.get("/api/gap-answers")
def list_gap_answers(project: str | None = None):
    """Local, code-only Q&A audit log — real timestamps, never AI-written. Does not edit
    the actual gap-register/knowledge files; that's the separate, unbuilt ingest pipeline."""
    return store.list_gap_answers(project)


@app.post("/api/gap-answers")
def add_gap_answer(body: GapAnswerIn):
    try:
        answer_id = store.add_gap_answer(
            body.project, body.gap_ref, body.question, body.answer, body.answered_by,
            body.device, body.entry_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "id": answer_id}


@app.delete("/api/gap-answers/{answer_id}")
def remove_gap_answer(answer_id: int):
    if not store.delete_gap_answer(answer_id):
        raise HTTPException(status_code=404, detail="No such answer")
    return {"ok": True}


class CaseFixIn(BaseModel):
    rule: str
    fields: dict
    by: str


class CaseWaiveIn(BaseModel):
    rule: str
    reason: str
    by: str


class CaseRuleIn(BaseModel):
    rule: str
    by: str = "unknown"


@app.get("/api/case-review")
def get_case_review(project: str, device: str):
    """Cases the build's repair step would not guess at (no steps, compound THENs it could not
    cut cleanly) -- the human half of the definition-of-done gate. `open` > 0 blocks the build's
    human_cleanup step from being approved."""
    return case_review.load(project, device)


@app.get("/api/case-review/log")
def get_case_review_log(project: str, device: str):
    """Every fix / accept / reopen made on the Case Review screen, with who, why and when,
    plus counts for today and all time. Kept in the console DB, not the plan file, so a
    re-check never erases it."""
    return case_review.log(project, device)


@app.post("/api/case-review/recheck")
def recheck_case_review(project: str, device: str):
    """Re-audit live TestRail: items fixed elsewhere drop off, waivers carry over."""
    result = case_review.recheck(project, device)
    if not result.get("ok"):
        raise HTTPException(status_code=502, detail=result.get("error", "Re-check failed."))
    return result


@app.post("/api/case-review/{case_id}/fix")
def fix_case_review(case_id: int, project: str, device: str, body: CaseFixIn):
    """Save a human's edit to TestRail. Refused (422, nothing written) if the edited case
    still breaks the standard -- the response says which rule."""
    try:
        result = case_review.fix(project, device, case_id, body.rule, body.fields, body.by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not result.get("ok"):
        raise HTTPException(status_code=422, detail=result.get("error", "Not saved."))
    return result


@app.post("/api/case-review/{case_id}/waive")
def waive_case_review(case_id: int, project: str, device: str, body: CaseWaiveIn):
    try:
        return case_review.waive(project, device, case_id, body.rule, body.reason, body.by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/case-review/{case_id}/reopen")
def reopen_case_review(case_id: int, project: str, device: str, body: CaseRuleIn):
    try:
        case_review.reopen(project, device, case_id, body.rule, body.by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True}


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


@app.get("/api/sit-mirror/status")
def get_sit_mirror_status():
    """George, 2026-09-28: "is it not really up to date? real reflection of what we
    actually have or is it purely based on the sit clone/pull we do?" -- answer, confirmed:
    the Keywords/Screen-flows views under "SIT (view only)" read `sit-mirror/`, a one-way,
    point-in-time copy (`tools/sync_sit_mirror.py`), never a live connection to the real sit
    repo. This surfaces the one real, checkable fact that made the staleness concrete: the
    mirror root's own filesystem mtime (last touched by a sync run), so the console can show
    it honestly instead of silently looking as current as a live view would."""
    root = functions._default_root()
    if not root.is_dir():
        return {"available": False}
    mtime = datetime.fromtimestamp(root.stat().st_mtime, tz=timezone.utc)
    days_stale = (datetime.now(timezone.utc) - mtime).days
    return {"available": True, "last_synced": mtime.isoformat(), "days_stale": days_stale}


@app.get("/api/automation/tests")
def get_automation_tests(project: str | None = None, device_type: str | None = None, q: str | None = None):
    """Real automation-test inventory, parsed live from test-automation-sit's own .robot
    files -- how many tests exist, for what project/device/feature (George, 2026-09-10).
    Not the same axis as SIT keywords -- this counts actual written tests."""
    suites = automation_tests.load_all_suites()
    all_summary = automation_tests.summarize(suites)  # unfiltered -- dropdowns always list every real project/device seen, not just what's currently filtered to
    filtered = suites
    if project:
        filtered = [s for s in filtered if (s.project or "").lower() == project.lower()]
    if device_type:
        filtered = [s for s in filtered if any(d.lower() == device_type.lower() for d in s.device_types)]
    if q:
        needle = q.lower()
        filtered = [s for s in filtered if any(needle in c.name.lower() for c in s.cases) or needle in (s.feature or "").lower()]
    # Bug fix (2026-09-17): summary used to always be computed from the FULL suite list even
    # when project/device_type filters were passed -- so a filtered dashboard view's stat
    # cards/bars silently kept showing global totals instead of the filtered picture.
    summary = all_summary if filtered is suites else automation_tests.summarize(filtered)
    return {
        "summary": summary,
        "projects": sorted(all_summary["by_project"].keys()),
        "device_types": sorted(all_summary["by_device_type"].keys()),
        "suites": [s.model_dump() for s in filtered],
    }


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
    ats_root = _PLATFORM_ROOT.parent.parent / "test-automation-sit"
    sections = build_sections(sto_root, _PLATFORM_ROOT.parent, ats_root if ats_root.is_dir() else None)
    return [
        {"title": title, "files": [{"path": p, "purpose": purpose, "lines": loc} for p, purpose, loc in rows]}
        for title, rows in sections
    ]


_REPORTS_ROOT = (_PLATFORM_ROOT.parent.parent / "system-test-ops" / "reports").resolve()


@app.get("/api/reports")
def list_reports(project: str | None = None):
    """Real generated report artefacts (coverage.md, run-health-report.md,
    build-complete.md, consolidation-audit.md, etc.) under system-test-ops/reports/ --
    the Reports tab's file list (George, 2026-09-22: "start putting into the... report
    spaces"). Filesystem-walked live, not a cached index -- these are gitignored, so
    nothing but the real disk state is authoritative. Newest first. `project` filters to
    that top-level folder (reports/<project>/...) when given."""
    if not _REPORTS_ROOT.is_dir():
        return []
    out = []
    for path in _REPORTS_ROOT.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(_REPORTS_ROOT)
        parts = rel.parts
        # Only a real subdirectory is a project -- a file sitting loose directly in
        # reports/ (e.g. alignment-audit.md) used to become its own fake "project"
        # alongside the real ones (2026-09-23 sweep).
        report_project = parts[0] if len(parts) > 1 else ""
        if project and report_project.lower() != project.lower():
            continue
        stat = path.stat()
        out.append({
            "project": report_project,
            "path": str(rel).replace("\\", "/"),
            "filename": path.name,
            "size": stat.st_size,
            "modified_at": stat.st_mtime,
        })
    out.sort(key=lambda r: r["modified_at"], reverse=True)
    return out


@app.get("/api/reports/content")
def get_report_content(path: str):
    """Raw text of one report file, for the Reports tab's preview -- `path` must resolve
    inside reports/, never outside it (real path-traversal guard, not just a string check:
    resolves symlinks/`..` and confirms the result is still under _REPORTS_ROOT)."""
    candidate = (_REPORTS_ROOT / path).resolve()
    if _REPORTS_ROOT not in candidate.parents or not candidate.is_file():
        raise HTTPException(status_code=404, detail="No such report file")
    try:
        return {"path": path, "text": candidate.read_text(encoding="utf-8", errors="replace")}
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Could not read report: {exc}") from exc


@app.middleware("http")
async def _no_stale_static_cache(request, call_next):
    """Found live, 2026-09-28: George's browser kept showing the OLD index.html/JS after
    several real, verified-live server updates -- StaticFiles serves Last-Modified/ETag but
    no Cache-Control, so the browser's own heuristic caching could silently serve a stale
    disk copy without even revalidating. This actively-iterated local dev console should
    never look stale from a plain refresh -- forces every response to revalidate (still
    cheap: a real change still round-trips, an unchanged file still gets a fast 304)."""
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return response


app.mount("/", StaticFiles(directory=str(WEBAPP_ROOT / "static"), html=True), name="static")
