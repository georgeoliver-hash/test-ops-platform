"""Local, single-machine persistence: suite mappings + encrypted TestRail credentials.

Deliberately NOT a shared/multi-user service (per George, 2026-09-07: "just me for now").
Everything lives in a local SQLite file that never leaves the machine and is gitignored
(Platform/webapp/data/) — the same trust boundary system-test-ops' own `.env` already
uses, just with a real UI in front of it instead of a text file.

Security notes (read before touching this file):
  - The TestRail API key is encrypted at rest with Fernet (AES-128-CBC + HMAC), using a key
    generated on first run and stored in `data/secret.key`, gitignored, never logged.
  - The API key is NEVER returned to the frontend once saved — `get_credentials_status()`
    tells the caller whether one is configured and what URL/user it's for, but the key
    itself only comes back inside `decrypt_api_key()`, called server-side when something
    actually needs to call TestRail (not built yet — no live TestRail call exists in this
    app today).
  - If `data/secret.key` is ever lost or rotated, every stored credential becomes
    undecryptable — that's intentional (no secondary "recovery" path that would itself be
    a weaker copy of the secret) and the UI should just prompt the user to re-enter it.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
from contextlib import contextmanager
from pathlib import Path

import yaml
from cryptography.fernet import Fernet, InvalidToken

DEFAULT_USER_ID = 1  # single-user today; a real multi-user model is future work, not this one.


def _data_dir() -> Path:
    """Resolved fresh on every call, NOT cached as a module-level global.

    A frozen `DATA_DIR = ...` global would lock in whichever TESTOPS_WEBAPP_DATA_DIR was set
    at first import forever, for every caller sharing this cached module — exactly the bug
    model/pipelines.py used to have (see that module's _default_root() docstring). Recompute
    per call so each test/caller's own environment always wins, no reload dance required.
    """
    override = os.environ.get("TESTOPS_WEBAPP_DATA_DIR")
    return Path(override) if override else Path(__file__).resolve().parent / "data"


def _db_path() -> Path:
    return _data_dir() / "console.db"


def _key_path() -> Path:
    return _data_dir() / "secret.key"


def _ensure_data_dir() -> None:
    _data_dir().mkdir(parents=True, exist_ok=True)


def _repo_root() -> Path:
    """test-ops-platform's own repo root (Platform/webapp/store.py -> Platform -> repo root)
    -- where `Platform/config/suite_targets.yaml` lives and where its git status is checked."""
    return Path(__file__).resolve().parent.parent.parent


def _suite_targets_path() -> Path:
    """Overridable for tests (TESTOPS_SUITE_TARGETS_PATH), same convention as
    TESTOPS_WEBAPP_DATA_DIR -- so tests never read/write the real, git-tracked repo file."""
    override = os.environ.get("TESTOPS_SUITE_TARGETS_PATH")
    return Path(override) if override else _repo_root() / "Platform" / "config" / "suite_targets.yaml"


def _default_seed_targets() -> list[dict]:
    """Bootstraps `suite_targets.yaml` the first time it's missing (e.g. a fresh test temp
    dir). The real, committed copy at Platform/config/suite_targets.yaml carries the same
    content plus source citations -- this is just enough to keep tests self-contained."""
    return [
        {"project": "Translink", "device": "POS", "old_suite": "AA-POS Acceptance Test", "old_suite_id": 9317,
         "new_suite": "GG - POS - Claude Suite", "new_suite_id": 30253, "fresh_build": False},
        {"project": "Translink", "device": "ETM", "old_suite": "AA-ETM-Acceptance Test", "old_suite_id": 4943,
         "new_suite": "NEW ETM-Acceptance Suite", "new_suite_id": 30254, "fresh_build": False},
        {"project": "Translink", "device": "GV", "old_suite": "AA - Gate Validator - Acceptance Test", "old_suite_id": 14973,
         "new_suite": "NEW GV Test Suite", "new_suite_id": 30286, "fresh_build": False},
        {"project": "Translink", "device": "TVM", "old_suite": "AA-TVM-Acceptance Test-V03", "old_suite_id": 5602,
         "new_suite": "NEW TVM Test Suite", "new_suite_id": 30284, "fresh_build": False},
        {"project": "Translink", "device": "HHD", "old_suite": "AA-HHD-Acceptance", "old_suite_id": 5446,
         "new_suite": "NEW HHD Test Suite", "new_suite_id": 30285, "fresh_build": False},
        {"project": "Translink", "device": "PV", "old_suite": "AA-Platform Validator Acceptance Test", "old_suite_id": 10047,
         "new_suite": "NEW PV-Acceptance Test Suite", "new_suite_id": 30255, "fresh_build": False},
        {"project": "Translink", "device": "BOS", "old_suite": "2.1-Backoffice Systems - Acceptance Suite", "old_suite_id": 14441,
         "new_suite": "NEW BOS & ABT Suite", "new_suite_id": 30279, "fresh_build": False},
        {"project": "NJT", "device": "ETM", "old_suite": "", "old_suite_id": None,
         "new_suite": "NJT - SystemTestOps", "new_suite_id": 30295, "fresh_build": True},
    ]


def _load_suite_targets() -> list[dict]:
    """Reads the git-tracked target list, bootstrapping it with the default seed if the file
    doesn't exist yet (fresh clone, or an isolated test temp path)."""
    path = _suite_targets_path()
    if not path.is_file():
        defaults = _default_seed_targets()
        _save_suite_targets(defaults)
        return defaults
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("targets") or []


def _save_suite_targets(entries: list[dict]) -> None:
    path = _suite_targets_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump({"version": 1, "targets": entries}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _sync_target_to_yaml(project: str, device: str, old_suite: str, new_suite: str,
                          new_suite_id: int | None, old_suite_id: int | None, fresh_build: bool) -> None:
    """Write-through so any create/edit made via upsert_suite_mapping (i.e. the existing
    "Add this pair" / "Edit this pair" UI) lands in the shared, git-trackable file too --
    not just the caller's own local SQLite db. Committing + pushing this file is still a
    manual step outside the app (see suite_targets_git_status) -- this only stages the
    change on disk."""
    entries = _load_suite_targets()
    entry = {
        "project": project, "device": device, "old_suite": old_suite, "old_suite_id": old_suite_id,
        "new_suite": new_suite, "new_suite_id": new_suite_id, "fresh_build": fresh_build,
    }
    for i, e in enumerate(entries):
        if e.get("project") == project and e.get("device") == device:
            entries[i] = entry
            break
    else:
        entries.append(entry)
    _save_suite_targets(entries)


def suite_targets_git_status() -> dict:
    """Read-only check of whether Platform/config/suite_targets.yaml has changes that
    haven't been committed, or commits that haven't been pushed -- this app never commits or
    pushes it automatically (see docs/gareth-onboarding-guide.md: sharing a new target is a
    deliberate, human "push this so others see it" step, same as every other repo write this
    tool makes). Returns {"status": "clean"|"uncommitted"|"unpushed"|"unknown", ...}."""
    repo_root = _repo_root()
    rel_path = "Platform/config/suite_targets.yaml"
    try:
        porcelain = subprocess.run(
            ["git", "status", "--porcelain", "--", rel_path],
            cwd=repo_root, capture_output=True, text=True, timeout=10,
        )
        if porcelain.returncode != 0:
            return {"status": "unknown", "detail": porcelain.stderr.strip()}
        if porcelain.stdout.strip():
            return {"status": "uncommitted"}
        ahead = subprocess.run(
            ["git", "log", "@{u}..", "--oneline", "--", rel_path],
            cwd=repo_root, capture_output=True, text=True, timeout=10,
        )
        if ahead.returncode != 0:
            return {"status": "unknown", "detail": ahead.stderr.strip() or "no upstream configured"}
        if ahead.stdout.strip():
            return {"status": "unpushed"}
        return {"status": "clean"}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "unknown", "detail": str(exc)}


def _load_or_create_key() -> bytes:
    _ensure_data_dir()
    key_path = _key_path()
    if key_path.is_file():
        return key_path.read_bytes()
    key = Fernet.generate_key()
    key_path.write_bytes(key)
    try:
        os.chmod(key_path, 0o600)  # best-effort; Windows ACLs differ, but no harm trying
    except OSError:
        pass
    return key


@contextmanager
def _connect():
    _ensure_data_dir()
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, display_name TEXT NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS suite_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project TEXT NOT NULL,
                device TEXT NOT NULL,
                old_suite TEXT NOT NULL,
                new_suite TEXT NOT NULL,
                new_suite_id INTEGER,
                old_suite_id INTEGER,
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, project, device)
            )"""
        )
        # Migration for DBs created before new_suite_id/old_suite_id existed (2026-09-08/09)
        # -- needed to actually run a pipeline against a suite (the CLI takes a numeric
        # --suite id, not a name) and to compare old vs new case counts. Pre-existing rows
        # just get these backfilled below via the same INSERT OR IGNORE seed keys, or stay
        # NULL until edited if they're a custom row George added by hand.
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(suite_mappings)").fetchall()}
        if "new_suite_id" not in cols:
            conn.execute("ALTER TABLE suite_mappings ADD COLUMN new_suite_id INTEGER")
        if "old_suite_id" not in cols:
            conn.execute("ALTER TABLE suite_mappings ADD COLUMN old_suite_id INTEGER")
        # Real, persisted target sign-off (2026-09-14) -- replaces the client-side-only
        # #approveCheck cosmetic checkbox. NULL/NULL means never approved; the runner treats
        # that as a hard block on any push+--commit step regardless of the per-step human
        # gate Phase 1 already added -- both must be true, not either/or.
        if "approved_by" not in cols:
            conn.execute("ALTER TABLE suite_mappings ADD COLUMN approved_by TEXT")
        if "approved_at" not in cols:
            conn.execute("ALTER TABLE suite_mappings ADD COLUMN approved_at TEXT")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS credentials (
                user_id INTEGER PRIMARY KEY,
                testrail_url TEXT NOT NULL,
                testrail_user TEXT NOT NULL,
                encrypted_api_key BLOB NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS doc_snapshots (
                user_id INTEGER NOT NULL,
                project TEXT NOT NULL,
                rel_path TEXT NOT NULL,
                mtime REAL NOT NULL,
                size INTEGER NOT NULL,
                PRIMARY KEY (user_id, project, rel_path)
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS gap_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project TEXT NOT NULL,
                device TEXT,
                gap_ref TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                answered_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )
        # entry_type distinguishes a real answer from a "please clarify" reply or a
        # "this conflicts with the spec" flag -- George's ask (2026-09-11): a way to ask
        # for more info, and a tab for answers that actually conflict with spec/functionality.
        gap_cols = {r["name"] for r in conn.execute("PRAGMA table_info(gap_answers)").fetchall()}
        if "entry_type" not in gap_cols:
            conn.execute("ALTER TABLE gap_answers ADD COLUMN entry_type TEXT NOT NULL DEFAULT 'answer'")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS pipeline_runs (
                id TEXT PRIMARY KEY,
                pipeline_id TEXT NOT NULL,
                project TEXT NOT NULL,
                device TEXT NOT NULL,
                status TEXT NOT NULL,
                cli_output TEXT,
                summary TEXT,
                report_path TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        # Granular per-step tracking alongside pipeline_runs (added for the generic
        # step-executor, 2026-09-14) -- pipeline_runs stays the overall run's status/
        # summary; this table is what a "waiting_human" gate, a per-step output tail, and
        # a resume-from-step-N continuation all key off.
        conn.execute(
            """CREATE TABLE IF NOT EXISTS pipeline_run_steps (
                run_id TEXT NOT NULL,
                step_id TEXT NOT NULL,
                kind TEXT,
                status TEXT NOT NULL,
                output TEXT,
                started_at TEXT,
                finished_at TEXT,
                PRIMARY KEY (run_id, step_id)
            )"""
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (id, display_name) VALUES (?, ?)",
            (DEFAULT_USER_ID, "George Oliver"),
        )
        # Seed from the git-tracked Platform/config/suite_targets.yaml (2026-09-14) --
        # replaces the old hardcoded Python literal list so that adding a target through the
        # UI (upsert_suite_mapping -> _sync_target_to_yaml) is visible to a colleague after
        # they commit+push that file and a teammate `git pull`s, without a code change.
        # INSERT OR IGNORE so re-running init_db doesn't clobber a user's own local edits.
        for target in _load_suite_targets():
            project, device = target["project"], target["device"]
            old_suite, new_suite = target.get("old_suite") or "", target["new_suite"]
            new_suite_id, old_suite_id = target.get("new_suite_id"), target.get("old_suite_id")
            conn.execute(
                """INSERT OR IGNORE INTO suite_mappings
                   (user_id, project, device, old_suite, new_suite, new_suite_id, old_suite_id, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
                (DEFAULT_USER_ID, project, device, old_suite, new_suite, new_suite_id, old_suite_id),
            )
            # Backfill for rows created before new_suite_id/old_suite_id existed (pre-migration)
            conn.execute(
                """UPDATE suite_mappings SET new_suite_id = ?
                   WHERE user_id = ? AND project = ? AND device = ? AND new_suite_id IS NULL""",
                (new_suite_id, DEFAULT_USER_ID, project, device),
            )
            conn.execute(
                """UPDATE suite_mappings SET old_suite_id = ?
                   WHERE user_id = ? AND project = ? AND device = ? AND old_suite_id IS NULL""",
                (old_suite_id, DEFAULT_USER_ID, project, device),
            )


def get_current_user(user_id: int = DEFAULT_USER_ID) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT id, display_name FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else {"id": user_id, "display_name": "Unknown"}


def list_suite_mappings(user_id: int = DEFAULT_USER_ID) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT project, device, old_suite, new_suite, new_suite_id, old_suite_id, "
            "approved_by, approved_at, updated_at "
            "FROM suite_mappings WHERE user_id = ? ORDER BY project, device",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def approve_suite_mapping(project: str, device: str, approved_by: str, user_id: int = DEFAULT_USER_ID) -> dict | None:
    """Real sign-off on a target -- a precondition the runner checks before letting any
    push+--commit step actually execute, independent of that step's own per-run human
    gate. Returns the updated row, or None if no mapping exists for this project/device."""
    if not approved_by.strip():
        raise ValueError("approved_by is required — no anonymous approvals.")
    with _connect() as conn:
        cur = conn.execute(
            """UPDATE suite_mappings SET approved_by = ?, approved_at = datetime('now')
               WHERE user_id = ? AND project = ? AND device = ?""",
            (approved_by.strip(), user_id, project, device),
        )
        if cur.rowcount == 0:
            return None
        row = conn.execute(
            "SELECT project, device, old_suite, new_suite, new_suite_id, old_suite_id, "
            "approved_by, approved_at, updated_at FROM suite_mappings "
            "WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
        return dict(row) if row else None


def is_target_approved(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT approved_by FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
        return bool(row and row["approved_by"])


def get_new_suite_id(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> int | None:
    """The numeric TestRail suite id to actually run a pipeline against — the CLI's --suite
    flag needs a real id, not the display name stored in new_suite."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT new_suite_id FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
        return row["new_suite_id"] if row else None


def get_suite_ids(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> dict | None:
    """Both numeric suite ids for a target, e.g. for an old-vs-new case-count comparison."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT old_suite_id, new_suite_id FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
        return dict(row) if row else None


def upsert_suite_mapping(project: str, device: str, old_suite: str, new_suite: str, new_suite_id: int | None = None, old_suite_id: int | None = None, fresh_build: bool = False, user_id: int = DEFAULT_USER_ID) -> None:
    """`fresh_build=True` means this target genuinely has no old suite — the tool is
    building a suite purely from documentation, not migrating an existing one (George,
    2026-09-10: NJT is the real first case for this — 'the purpose here was to see if the
    tool could create a suite based off purely documentation'). old_suite is then stored
    as '' (empty string, not NULL — old_suite stays NOT NULL at the schema level so
    existing rows/tooling that assume it's always a string don't need a migration); every
    other caller still gets the normal old_suite-is-required validation."""
    if not (project.strip() and device.strip() and new_suite.strip()):
        raise ValueError("project, device, and new_suite are all required — no blanks.")
    if not fresh_build and not old_suite.strip():
        raise ValueError("old_suite is required unless this is an explicit fresh build (no prior suite to reference).")
    old_suite = "" if fresh_build else old_suite.strip()
    project, device, new_suite = project.strip(), device.strip(), new_suite.strip()
    with _connect() as conn:
        conn.execute(
            """INSERT INTO suite_mappings (user_id, project, device, old_suite, new_suite, new_suite_id, old_suite_id, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(user_id, project, device)
               DO UPDATE SET old_suite = excluded.old_suite, new_suite = excluded.new_suite,
                             new_suite_id = COALESCE(excluded.new_suite_id, suite_mappings.new_suite_id),
                             old_suite_id = COALESCE(excluded.old_suite_id, suite_mappings.old_suite_id),
                             updated_at = excluded.updated_at""",
            (user_id, project, device, old_suite, new_suite, new_suite_id, old_suite_id),
        )
        row = conn.execute(
            "SELECT new_suite_id, old_suite_id FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
    # Write-through to the shared, git-tracked file -- only for the real single-user default,
    # matching the fact this whole file (and this app) has no multi-user concept yet.
    if user_id == DEFAULT_USER_ID:
        _sync_target_to_yaml(project, device, old_suite, new_suite, row["new_suite_id"], row["old_suite_id"], fresh_build)


def delete_suite_mapping(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        )
        return cur.rowcount > 0


def create_run(run_id: str, pipeline_id: str, project: str, device: str) -> None:
    with _connect() as conn:
        conn.execute(
            """INSERT INTO pipeline_runs (id, pipeline_id, project, device, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, 'running', datetime('now'), datetime('now'))""",
            (run_id, pipeline_id, project, device),
        )


def update_run(run_id: str, **fields) -> None:
    """fields: any of status, cli_output, summary, report_path, error."""
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    with _connect() as conn:
        conn.execute(
            f"UPDATE pipeline_runs SET {set_clause}, updated_at = datetime('now') WHERE id = ?",
            (*fields.values(), run_id),
        )


def get_run(run_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM pipeline_runs WHERE id = ?", (run_id,)).fetchone()
        return dict(row) if row else None


def create_step_rows(run_id: str, steps: list[tuple[str, str | None]]) -> None:
    """`steps`: ordered (step_id, kind) pairs for this run's flattened step list, inserted
    as status='pending'. `kind` is a free string (cli/agent/human/gate/None) — no CHECK
    constraint, matching pipeline_runs' own free-text status column."""
    if not steps:
        return
    with _connect() as conn:
        conn.executemany(
            "INSERT INTO pipeline_run_steps (run_id, step_id, kind, status) VALUES (?, ?, ?, 'pending')",
            [(run_id, step_id, kind) for step_id, kind in steps],
        )


def update_step(run_id: str, step_id: str, **fields) -> None:
    """fields: any of status, output, started_at, finished_at."""
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    with _connect() as conn:
        conn.execute(
            f"UPDATE pipeline_run_steps SET {set_clause} WHERE run_id = ? AND step_id = ?",
            (*fields.values(), run_id, step_id),
        )


def get_steps(run_id: str) -> list[dict]:
    """Ordered by rowid (insertion order == pipeline step order) — the poll target for a
    run's live step-by-step progress."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM pipeline_run_steps WHERE run_id = ? ORDER BY rowid", (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_step(run_id: str, step_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM pipeline_run_steps WHERE run_id = ? AND step_id = ?", (run_id, step_id),
        ).fetchone()
        return dict(row) if row else None


def get_latest_run(pipeline_id: str, project: str, device: str) -> dict | None:
    """Most recent real run for this pipeline+target — a genuine 'last audited' timestamp,
    not a guess, now that runs are actually tracked (see runner.py). Was flagged in
    ISSUES.md as unbuildable ('no structured event source yet') until audit got wired."""
    with _connect() as conn:
        row = conn.execute(
            """SELECT * FROM pipeline_runs WHERE pipeline_id = ? AND project = ? AND device = ?
               ORDER BY created_at DESC LIMIT 1""",
            (pipeline_id, project, device),
        ).fetchone()
        return dict(row) if row else None


def add_gap_answer(
    project: str, gap_ref: str, question: str, answer: str, answered_by: str,
    device: str | None = None, entry_type: str = "answer", user_id: int = DEFAULT_USER_ID,
) -> int:
    """A real, dated, code-only audit-trail entry for a gap-register question getting
    answered -- George's explicit ask (2026-09-09): 'a log of confirm gap changes, answers,
    dates times etc... if this could be code not AI that would be great.' No AI writes
    this; it's a plain INSERT, timestamped by SQLite's own datetime('now').

    entry_type is 'answer' (default), 'clarification_request' (asking the doc/case owner
    for more info before an answer can be given), or 'conflict' (the answer contradicts
    spec/functionality as it stands today) -- George's ask (2026-09-11) for a reply flow
    and a conflicts tab. This is a real classification the person logging the entry picks,
    not something inferred.

    Deliberately does NOT edit the actual knowledge/*.md or gap-register.md file the
    gap_ref points at -- that's still the bigger, unbuilt, write-capable ingest pipeline.
    This is the local record of the human decision, safe to build now."""
    if not (project.strip() and gap_ref.strip() and question.strip() and answer.strip() and answered_by.strip()):
        raise ValueError("project, gap_ref, question, answer, and answered_by are all required — no blanks.")
    if entry_type not in ("answer", "clarification_request", "conflict"):
        raise ValueError("entry_type must be 'answer', 'clarification_request', or 'conflict'.")
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO gap_answers (user_id, project, device, gap_ref, question, answer, answered_by, entry_type, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
            (user_id, project.strip(), (device or "").strip() or None, gap_ref.strip(), question.strip(), answer.strip(), answered_by.strip(), entry_type),
        )
        return cur.lastrowid


def list_gap_answers(project: str | None = None, user_id: int = DEFAULT_USER_ID) -> list[dict]:
    with _connect() as conn:
        if project:
            rows = conn.execute(
                "SELECT * FROM gap_answers WHERE user_id = ? AND project = ? ORDER BY created_at DESC",
                (user_id, project),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM gap_answers WHERE user_id = ? ORDER BY created_at DESC", (user_id,),
            ).fetchall()
        return [dict(r) for r in rows]


def delete_gap_answer(answer_id: int, user_id: int = DEFAULT_USER_ID) -> bool:
    with _connect() as conn:
        cur = conn.execute("DELETE FROM gap_answers WHERE id = ? AND user_id = ?", (answer_id, user_id))
        return cur.rowcount > 0


def get_credentials_status(user_id: int = DEFAULT_USER_ID) -> dict:
    """Never includes the API key itself — only whether one is configured, and for which
    TestRail URL/user, so the UI can show 'configured' without ever handling the secret."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT testrail_url, testrail_user, updated_at FROM credentials WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if not row:
            return {"configured": False}
        return {"configured": True, "testrail_url": row["testrail_url"], "testrail_user": row["testrail_user"], "updated_at": row["updated_at"]}


def save_credentials(testrail_url: str, testrail_user: str, testrail_api_key: str, user_id: int = DEFAULT_USER_ID) -> None:
    if not (testrail_url.strip() and testrail_user.strip() and testrail_api_key.strip()):
        raise ValueError("TestRail URL, user, and API key are all required — no blanks.")
    key = _load_or_create_key()
    encrypted = Fernet(key).encrypt(testrail_api_key.strip().encode("utf-8"))
    with _connect() as conn:
        conn.execute(
            """INSERT INTO credentials (user_id, testrail_url, testrail_user, encrypted_api_key, updated_at)
               VALUES (?, ?, ?, ?, datetime('now'))
               ON CONFLICT(user_id) DO UPDATE SET
                 testrail_url = excluded.testrail_url, testrail_user = excluded.testrail_user,
                 encrypted_api_key = excluded.encrypted_api_key, updated_at = excluded.updated_at""",
            (user_id, testrail_url.strip(), testrail_user.strip(), encrypted),
        )


def delete_credentials(user_id: int = DEFAULT_USER_ID) -> bool:
    with _connect() as conn:
        cur = conn.execute("DELETE FROM credentials WHERE user_id = ?", (user_id,))
        return cur.rowcount > 0


def _uploads_root() -> Path:
    return _data_dir() / "uploads"


def _uploads_dir(project: str, device: str) -> Path:
    """One folder per project/device pair — mirrors suite_mappings' keying, so a doc dropped
    here has an unambiguous target when a future ingest-docs run picks it up."""
    return _uploads_root() / project / device


def uploads_dir_path(project: str, device: str) -> str:
    """Absolute path to this target's upload folder — used to default ingest-docs' required
    `docs_path` run input to wherever docs were actually dropped via the UI, rather than
    making George hand-type a path. Returned even if the folder doesn't exist yet/is empty
    (str, not Path, since it crosses the API as plain JSON)."""
    return str(_uploads_dir(project, device))


def list_docs(project: str, device: str) -> list[dict]:
    d = _uploads_dir(project, device)
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.iterdir()):
        if p.is_file():
            stat = p.stat()
            out.append({"filename": p.name, "size_bytes": stat.st_size, "uploaded_at": stat.st_mtime})
    return out


def save_doc(project: str, device: str, filename: str, content: bytes) -> None:
    """Raw filename only — no path segments allowed, so a crafted name can't escape the
    project/device folder it was uploaded against."""
    safe_name = Path(filename).name
    if not safe_name or safe_name != filename:
        raise ValueError("Invalid filename.")
    d = _uploads_dir(project, device)
    d.mkdir(parents=True, exist_ok=True)
    (d / safe_name).write_bytes(content)


def delete_doc(project: str, device: str, filename: str) -> bool:
    safe_name = Path(filename).name
    path = _uploads_dir(project, device) / safe_name
    if not path.is_file():
        return False
    path.unlink()
    return True


def check_docs_for_changes(project: str, requirements_dir: Path, user_id: int = DEFAULT_USER_ID) -> dict:
    """Real change-detection against a local requirements folder (e.g.
    TestOpsRequirements/<project>/) -- mtime+size per file, compared against the last check.
    Updates the stored snapshot to the current state, so the next check is relative to now.

    Deliberately does NOT re-parse anything into knowledge/*.md itself -- that's the same
    ingest-docs pipeline that isn't built yet (write-capable, needs the same "prove it's
    safe" pass audit just got). This only answers "what changed since I last looked",
    honestly, so nothing gets silently missed while that pipeline doesn't exist yet."""
    if not requirements_dir.is_dir():
        return {"exists": False, "new": [], "changed": [], "removed": [], "unchanged_count": 0}

    current = {}
    for f in requirements_dir.rglob("*"):
        if f.is_file():
            rel = str(f.relative_to(requirements_dir))
            stat = f.stat()
            current[rel] = (stat.st_mtime, stat.st_size)

    with _connect() as conn:
        prior_rows = conn.execute(
            "SELECT rel_path, mtime, size FROM doc_snapshots WHERE user_id = ? AND project = ?",
            (user_id, project),
        ).fetchall()
        prior = {r["rel_path"]: (r["mtime"], r["size"]) for r in prior_rows}

        new_files = sorted(set(current) - set(prior))
        removed_files = sorted(set(prior) - set(current))
        changed_files = sorted(
            rel for rel in (set(current) & set(prior))
            if current[rel][1] != prior[rel][1] or abs(current[rel][0] - prior[rel][0]) > 1
        )
        unchanged_count = len(current) - len(new_files) - len(changed_files)

        conn.execute("DELETE FROM doc_snapshots WHERE user_id = ? AND project = ?", (user_id, project))
        conn.executemany(
            "INSERT INTO doc_snapshots (user_id, project, rel_path, mtime, size) VALUES (?, ?, ?, ?, ?)",
            [(user_id, project, rel, mtime, size) for rel, (mtime, size) in current.items()],
        )

    return {
        "exists": True, "new": new_files, "changed": changed_files, "removed": removed_files,
        "unchanged_count": unchanged_count, "total_files": len(current),
    }


def detect_sibling_env_credentials(env_path: Path) -> dict | None:
    """Read-only peek at a sibling repo's .env (system-test-ops' own TESTRAIL_* vars) so the
    console can offer to import real, already-configured credentials instead of asking
    George to retype something that already exists on his machine. Never returns the key
    itself — only enough to show what would be imported; the key is read again, server-side
    only, at actual import time (import_sibling_env_credentials)."""
    if not env_path.is_file():
        return None
    values = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()
    url, user, key = values.get("TESTRAIL_URL"), values.get("TESTRAIL_USER"), values.get("TESTRAIL_API_KEY")
    if not (url and user and key):
        return None
    return {"testrail_url": url, "testrail_user": user}


def import_sibling_env_credentials(env_path: Path, user_id: int = DEFAULT_USER_ID) -> bool:
    if not env_path.is_file():
        return False
    values = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()
    url, user, key = values.get("TESTRAIL_URL"), values.get("TESTRAIL_USER"), values.get("TESTRAIL_API_KEY")
    if not (url and user and key):
        return False
    save_credentials(url, user, key, user_id=user_id)
    return True


def decrypt_api_key(user_id: int = DEFAULT_USER_ID) -> str | None:
    """Server-side only — for the day something actually needs to call TestRail. Never
    call this from a request handler that echoes the result back to the frontend."""
    with _connect() as conn:
        row = conn.execute("SELECT encrypted_api_key FROM credentials WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return None
        try:
            return Fernet(_load_or_create_key()).decrypt(row["encrypted_api_key"]).decode("utf-8")
        except InvalidToken:
            return None  # secret.key was rotated/lost since this was saved — treat as unset
