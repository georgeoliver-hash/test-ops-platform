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
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import zipfile
from contextlib import asynccontextmanager
from datetime import datetime, timezone
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

from model import automation_tests, devices, features, flows, functions, pipelines  # noqa: E402
from Platform.webapp import runner, store  # noqa: E402

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
    """Real docs_path for the Ingest run form -- prefers the actual synced requirements
    library (TestOpsRequirements/<project>/_current/) over the console's own small
    upload folder, which was silently winning even when it was empty and the real docs
    sat untouched elsewhere (George, 2026-09-22: "the platform says there is no docs
    uploaded for translink pos"). `source` tells the frontend which one it got, so it can
    say so honestly instead of implying "uploaded" when it's really the synced folder.

    Returns `options` too: when BOTH a synced library and uploaded files exist, the user
    picks. Preferring the synced folder silently meant uploads were ignored with no hint
    (George, 2026-09-23: he'd have uploaded 660MB and Ingest would have read the other
    folder anyway) -- the preference is still the default, it's just no longer a secret."""
    project, device = _validated_target(project, device)

    def _count(path: Path) -> int:
        try:
            return sum(1 for f in path.rglob("*") if f.is_file())
        except OSError:
            return 0

    options = []
    real = store.resolve_ingest_docs_source(project)
    if real["path"]:
        options.append({"path": real["path"], "source": "requirements_folder",
                        "label": "Synced requirements folder", "file_count": _count(Path(real["path"]))})
    uploads = Path(store.uploads_dir_path(project, device))
    upload_count = _count(uploads)
    if upload_count or not options:
        options.append({"path": str(uploads), "source": "uploads_folder",
                        "label": "Docs uploaded in this console", "file_count": upload_count})

    chosen = options[0]
    return {"path": chosen["path"], "source": chosen["source"], "options": options}


@app.post("/api/docs")
async def upload_doc(project: str, device: str, file: UploadFile = File(...)):
    project, device = _validated_target(project, device)
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename given.")
    content = await file.read()
    try:
        store.save_doc(project, device, file.filename, content)
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
def remove_doc(project: str, device: str, filename: str):
    project, device = _validated_target(project, device)
    if not store.delete_doc(project, device, filename):
        raise HTTPException(status_code=404, detail="No such file")
    return {"ok": True}


@app.post("/api/docs/{project}/refresh-check")
def refresh_docs_check(project: str):
    """Real change-detection against the project's local requirements folder
    (%USERPROFILE%\\TestOpsRequirements\\<project>\\_current\\, see .env.example's
    documented convention) -- what's new/changed/removed since the last check. Fixed
    2026-09-22: was pointing at the project folder's TOP level, which also holds
    ingest_docs.py's own reconciliation logs (_dropped_versions.txt etc.) -- those were
    being reported as doc "changes" too. Uses the same real resolution as
    /api/docs/folder, so both agree on where the real docs actually are."""
    real = store.resolve_ingest_docs_source(project)
    req_dir = Path(real["path"]) if real["path"] else (Path.home() / "TestOpsRequirements" / project.lower())
    return store.check_docs_for_changes(project, req_dir)


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
        "runnable": runner.is_runnable(p.id),
    }


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
    return run


@app.get("/api/pipelines/runs/{run_id}/steps")
def get_pipeline_run_steps(run_id: str):
    """Granular per-step progress for one run — the poll target for the step list UI."""
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="No such run")
    return store.get_steps(run_id)


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
    try:
        runner.resolve_step(run_id, step_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except runner.TargetNotApprovedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
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


@app.get("/api/pipelines/{pipeline_id}/last-run")
def get_last_pipeline_run(pipeline_id: str, project: str, device: str):
    """A real 'last run' timestamp for this pipeline+target, or null if never run.
    Only meaningful for pipelines that are actually runnable (today: audit)."""
    return store.get_latest_run(pipeline_id, project, device) or {"status": None}


@app.get("/api/pipelines/{pipeline_id}/runs")
def get_pipeline_runs(pipeline_id: str, project: str, device: str, limit: int = 20):
    """Real run history for this pipeline+target (ISSUES.md round 4's Log tab ask) --
    every real row, not just the latest. `extra_inputs` (e.g. which fix_version/JIRA
    key(s) a run was actually given) comes back per-run where it was recorded; older runs
    predating that column just have it as null, shown honestly, never backfilled."""
    return store.get_runs(pipeline_id, project, device, limit=limit)


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
    every target, newest first."""
    return store.get_unreviewed_scheduled_scan_suggestions()


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


@app.get("/api/suite-comparison")
def get_suite_comparison(project: str, device: str):
    """Real, live old-vs-new case counts (two read-only TestRail pulls) -- one of the
    'suggestions' from ISSUES.md, now buildable with old_suite_id stored."""
    return runner.compare_suite_case_counts(project, device)


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
_GAP_DEVICE_PATH_HINTS = {
    "etm": ("etm-suite-restructure", "njt-fr-suite-restructure", "-etm-", "fixes\\etm",
            "fixes/etm", "fixes\\etm-deep-audit", "knowledge\\njt\\specs", "knowledge/njt/specs"),
    "pos": ("pos-suite-restructure", "-pos-", "fixes\\pos", "fixes/pos"),
    "gv": ("gv-suite-restructure", "-gv-", "fixes\\gv", "fixes/gv"),
    "hhd": ("hhd-suite-restructure", "-hhd-", "fixes\\hhd", "fixes/hhd"),
    "pv": ("pv-suite-restructure", "-pv-", "fixes\\pv", "fixes/pv"),
    "tvm": ("tvm-suite-restructure", "-tvm-", "fixes\\tvm", "fixes/tvm"),
    "bos": ("bos-abt-suite-restructure", "abt-", "fixes\\abt", "fixes/abt", "spec-grounded\\abt", "spec-grounded/abt"),
}


def _infer_gap_device(file_path: str) -> str | None:
    lowered = file_path.lower()
    for device, hints in _GAP_DEVICE_PATH_HINTS.items():
        if any(h in lowered for h in hints):
            return device.upper()
    return None


_GAP_SCOPES = ("project", "device", "common", "bespoke")


@app.get("/api/gap-register")
def get_gap_register(
    limit: int = 25, offset: int = 0, project: str | None = None,
    device: str | None = None, scope: str | None = None,
):
    """Real GAP/UNCONFIRMED markers, from an actual `gap-register` run over the real repo
    (re-run 2026-09-08, 972 found repo-wide). Supports real offset/limit pagination and an
    optional best-effort project filter (see _infer_gap_project) -- George's ask
    (2026-09-11): scope this to the current target, and let people page through all of it
    rather than only ever seeing the first N.

    `scope` (added 2026-09-18, ISSUES.md's "Project GAPs / Device GAPs / Common GAPs /
    Bespoke GAPs" split) narrows further:
      - "project": markers tagged with the given `project` (device ignored -- stays stable
        across a device switch within the same project, per George's ask).
      - "device": markers tagged with BOTH the given `project` AND `device`.
      - "common": markers with no inferred project at all -- genuinely shared/cross-cutting
        content (e.g. proposals/coherence-audit), not any one project's.
      - "bespoke": markers WITH an inferred project. CHANGED (ISSUES.md round 2, real ask,
        overriding the original 2026-09-18 design call noted below): now ALSO narrowed to
        the current `project` when one is given -- George found NJT/ETM questions showing
        under Bespoke while targeting Translink/POS and asked for it scoped like the other
        three. Only falls back to repo-wide (every bespoke marker, any project) when no
        `project` is supplied at all, so the tab still shows something with no target set.
    """
    # Validated 2026-09-23 (end-to-end sweep): limit=-1 previously ignored the limit and
    # dumped all 972 markers (~219KB), offset=-1 silently returned an empty page beside a
    # non-zero total, and an unknown scope ("banana", "BESPOKE", "") was silently treated
    # as no-scope -- while the sibling /api/run-comments already 400s on a bad `which`.
    # Ceiling is generous on purpose -- "fetch them all" is a real, legitimate call
    # (there are ~972 markers repo-wide, and the Gaps page's partition views rely on it).
    # The actual bug was a NEGATIVE limit silently returning everything.
    if limit < 1 or limit > 2000:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 2000.")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be 0 or greater.")
    if scope is not None and scope not in _GAP_SCOPES:
        raise HTTPException(status_code=400, detail=f"scope must be one of {_GAP_SCOPES}.")
    path = FIXTURES / "gaps.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="No gap-register fixture found")
    markers = json.loads(path.read_text(encoding="utf-8"))
    for m in markers:
        m["project"] = _infer_gap_project(m["file"])
        m["device"] = _infer_gap_device(m["file"])
    if scope == "project" and project:
        markers = [m for m in markers if m["project"] == project.lower()]
    elif scope == "device" and project and device:
        markers = [m for m in markers if m["project"] == project.lower() and m["device"] == device.upper()]
    elif scope == "common":
        markers = [m for m in markers if m["project"] is None]
    elif scope == "bespoke" and project:
        markers = [m for m in markers if m["project"] == project.lower()]
    elif scope == "bespoke":
        markers = [m for m in markers if m["project"] is not None]
    elif project:
        markers = [m for m in markers if m["project"] == project.lower()]
    return {
        "total": len(markers), "shown": markers[offset:offset + limit],
        "offset": offset, "limit": limit, "is_fixture": True, "scope": scope,
    }


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
    sections = build_sections(sto_root, _PLATFORM_ROOT.parent)
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


app.mount("/", StaticFiles(directory=str(WEBAPP_ROOT / "static"), html=True), name="static")
