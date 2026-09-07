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
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, project, device)
            )"""
        )
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
            "INSERT OR IGNORE INTO users (id, display_name) VALUES (?, ?)",
            (DEFAULT_USER_ID, "George Oliver"),
        )
        # Seed the one real, documented suite pair (system-test-ops CLAUDE.md's hard rule) —
        # never invent others. INSERT OR IGNORE so re-running init_db doesn't clobber edits.
        conn.execute(
            """INSERT OR IGNORE INTO suite_mappings
               (user_id, project, device, old_suite, new_suite, updated_at)
               VALUES (?, 'Translink', 'POS', 'AA-POS Acceptance Test', 'GG - POS - Claude Suite', datetime('now'))""",
            (DEFAULT_USER_ID,),
        )


def get_current_user(user_id: int = DEFAULT_USER_ID) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT id, display_name FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else {"id": user_id, "display_name": "Unknown"}


def list_suite_mappings(user_id: int = DEFAULT_USER_ID) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT project, device, old_suite, new_suite, updated_at FROM suite_mappings "
            "WHERE user_id = ? ORDER BY project, device",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def upsert_suite_mapping(project: str, device: str, old_suite: str, new_suite: str, user_id: int = DEFAULT_USER_ID) -> None:
    if not (project.strip() and device.strip() and old_suite.strip() and new_suite.strip()):
        raise ValueError("project, device, old_suite, and new_suite are all required — no blanks.")
    with _connect() as conn:
        conn.execute(
            """INSERT INTO suite_mappings (user_id, project, device, old_suite, new_suite, updated_at)
               VALUES (?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(user_id, project, device)
               DO UPDATE SET old_suite = excluded.old_suite, new_suite = excluded.new_suite,
                             updated_at = excluded.updated_at""",
            (user_id, project.strip(), device.strip(), old_suite.strip(), new_suite.strip()),
        )


def delete_suite_mapping(project: str, device: str, user_id: int = DEFAULT_USER_ID) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM suite_mappings WHERE user_id = ? AND project = ? AND device = ?",
            (user_id, project, device),
        )
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
