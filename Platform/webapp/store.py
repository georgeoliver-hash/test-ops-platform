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
from contextlib import contextmanager
from pathlib import Path

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
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, project, device)
            )"""
        )
        # Migration for DBs created before new_suite_id existed (2026-09-08) -- needed to
        # actually run a pipeline against a suite (the CLI takes a numeric --suite id, not a
        # name); pre-existing rows just get it backfilled below via the same INSERT OR IGNORE
        # seed keys, or stay NULL until edited if they're a custom row George added by hand.
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(suite_mappings)").fetchall()}
        if "new_suite_id" not in cols:
            conn.execute("ALTER TABLE suite_mappings ADD COLUMN new_suite_id INTEGER")
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
        conn.execute(
            "INSERT OR IGNORE INTO users (id, display_name) VALUES (?, ?)",
            (DEFAULT_USER_ID, "George Oliver"),
        )
        # Seed every real, documented old/new pair found in system-test-ops — never invent
        # others. TVM and HHD confirmed by George directly on 2026-09-08 (both had multiple
        # "old" suites feeding the new one; he named the one real Acceptance suite to treat
        # as the reference for each). NJT FR: new suite 30295 is real and in heavy use
        # (proposals/njt-fr-suite-restructure/*.cases.yaml), but George is getting the old
        # suite from Gareth — deliberately left unseeded until confirmed, not guessed.
        # INSERT OR IGNORE so re-running init_db doesn't clobber George's own edits.
        seed_pairs = [
            # (project, device, old_suite, new_suite, new_suite_id) -- cite: system-test-ops CLAUDE.md
            ("Translink", "POS", "AA-POS Acceptance Test", "GG - POS - Claude Suite", 30253),
            # cite: knowledge/devices/etm.md:89 + proposals/etm-suite-restructure/*
            ("Translink", "ETM", "AA-ETM-Acceptance Test", "NEW ETM-Acceptance Suite", 30254),
            # cite: proposals/gv-suite-restructure/old-suite-audit.md:7
            ("Translink", "GV", "AA - Gate Validator - Acceptance Test", "NEW GV Test Suite", 30286),
            # cite: proposals/tvm-suite-restructure/old-suite-audit.md:14 (id 5602) + George, 2026-09-08
            ("Translink", "TVM", "AA-TVM-Acceptance Test-V03", "NEW TVM Test Suite", 30284),
            # cite: proposals/hhd-suite-restructure/old-suite-audit.md:19 (id 5446) + George, 2026-09-08
            ("Translink", "HHD", "AA-HHD-Acceptance", "NEW HHD Test Suite", 30285),
            # cite: proposals/pv-suite-restructure/build-complete.md:3, pv-mode-tagging.changelog.md:81
            ("Translink", "PV", "AA-Platform Validator Acceptance Test", "NEW PV-Acceptance Test Suite", 30255),
        ]
        for project, device, old_suite, new_suite, new_suite_id in seed_pairs:
            conn.execute(
                """INSERT OR IGNORE INTO suite_mappings
                   (user_id, project, device, old_suite, new_suite, new_suite_id, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
                (DEFAULT_USER_ID, project, device, old_suite, new_suite, new_suite_id),
            )
            # Backfill for rows created before new_suite_id existed (this session, pre-migration)
            conn.execute(
                """UPDATE suite_mappings SET new_suite_id = ?
                   WHERE user_id = ? AND project = ? AND device = ? AND new_suite_id IS NULL""",
                (new_suite_id, DEFAULT_USER_ID, project, device),
            )


def get_current_user(user_id: int = DEFAULT_USER_ID) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT id, display_name FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else {"id": user_id, "display_name": "Unknown"}


def list_suite_mappings(user_id: int = DEFAULT_USER_ID) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT project, device, old_suite, new_suite, new_suite_id, updated_at FROM suite_mappings "
            "WHERE user_id = ? ORDER BY project, device",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_new_suite_id(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> int | None:
    """The numeric TestRail suite id to actually run a pipeline against — the CLI's --suite
    flag needs a real id, not the display name stored in new_suite."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT new_suite_id FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        ).fetchone()
        return row["new_suite_id"] if row else None


def upsert_suite_mapping(project: str, device: str, old_suite: str, new_suite: str, new_suite_id: int | None = None, user_id: int = DEFAULT_USER_ID) -> None:
    if not (project.strip() and device.strip() and old_suite.strip() and new_suite.strip()):
        raise ValueError("project, device, old_suite, and new_suite are all required — no blanks.")
    with _connect() as conn:
        conn.execute(
            """INSERT INTO suite_mappings (user_id, project, device, old_suite, new_suite, new_suite_id, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(user_id, project, device)
               DO UPDATE SET old_suite = excluded.old_suite, new_suite = excluded.new_suite,
                             new_suite_id = COALESCE(excluded.new_suite_id, suite_mappings.new_suite_id),
                             updated_at = excluded.updated_at""",
            (user_id, project.strip(), device.strip(), old_suite.strip(), new_suite.strip(), new_suite_id),
        )


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
