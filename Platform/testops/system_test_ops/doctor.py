"""Environment + connectivity preflight for system-test-ops.

A deterministic readiness check that answers the only question a newcomer has on
day one: *what's already set up, what can Claude handle, and what do I (the
human) still need to do before work can start?*

It is the engine behind the `/start` command, but anyone can run it directly:

    python -m system_test_ops doctor

Read-only. It never writes, mutates, or sends anything. By default it is purely
informational and exits 0; pass `--gate` to exit non-zero when something the
human must fix is still outstanding (handy in CI / pre-commit).

The design philosophy (see docs/test-practices.md): the irreducible human inputs
- secrets, the new TestRail suite, interactive OAuth, network/device access -
can't be automated away, so the win is making them **explicit and front-loaded**
instead of surfacing as surprise blockers mid-build.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Status buckets - these drive how a finding is grouped in the report.
READY = "ready"          # ✓ already in place, nothing to do
CLAUDE = "claude"        # • Claude can do this autonomously, no human input needed
NEEDS_YOU = "you"        # ✗ a human must act (secret, suite creation, network, OAuth)
MANUAL = "manual"        # ? can't be auto-verified here; Claude/you confirm at the Claude-Code layer

# Required Python package imports (module name -> friendly label).
_REQUIRED_IMPORTS = {
    "pydantic": "pydantic",
    "requests": "requests",
    "yaml": "PyYAML",
    "dotenv": "python-dotenv",
}


@dataclass
class Check:
    """One readiness finding."""

    name: str
    status: str
    detail: str = ""
    fix: str = ""


# --------------------------------------------------------------------------- #
# individual checks
# --------------------------------------------------------------------------- #
def _check_python() -> Check:
    major, minor = sys.version_info[:2]
    ver = f"{major}.{minor}.{sys.version_info[2]}"
    if (major, minor) >= (3, 11):
        return Check("Python 3.11+", READY, detail=f"running {ver}")
    return Check(
        "Python 3.11+",
        NEEDS_YOU,
        detail=f"running {ver} - too old",
        fix="Install Python 3.11 or newer and recreate the .venv.",
    )


def _check_venv() -> Check:
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if in_venv:
        return Check("Virtual environment", READY, detail=f"active ({sys.prefix})")
    return Check(
        "Virtual environment",
        CLAUDE,
        detail="not running inside a .venv",
        fix="python -m venv .venv ; .\\.venv\\Scripts\\Activate.ps1 ; pip install -e \".[dev]\"",
    )


def _check_deps() -> Check:
    missing = [
        label
        for mod, label in _REQUIRED_IMPORTS.items()
        if importlib.util.find_spec(mod) is None
    ]
    if not missing:
        return Check("Python dependencies", READY, detail="all importable")
    return Check(
        "Python dependencies",
        CLAUDE,
        detail="missing: " + ", ".join(missing),
        fix='pip install -e ".[dev]"  (from the repo root, inside the .venv)',
    )


def _env_value(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def _check_env_file() -> Check:
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        return Check(".env file", READY, detail=str(env_path))
    example = REPO_ROOT / ".env.example"
    fix = "Copy-Item .env.example .env  then fill in TESTRAIL_* values (see docs/getting-started.md)."
    if not example.exists():
        fix = "Create a .env at the repo root with TESTRAIL_URL / TESTRAIL_USER / TESTRAIL_API_KEY."
    return Check(".env file", NEEDS_YOU, detail="not found", fix=fix)


def _check_testrail_creds() -> list[Check]:
    """Each TestRail credential as its own line so the punch-list is precise."""
    out: list[Check] = []
    # Load .env into the environment first (mirrors the client's behaviour).
    if importlib.util.find_spec("dotenv") is not None:
        from dotenv import load_dotenv

        load_dotenv()

    for var, why, fix in (
        ("TESTRAIL_URL", "TestRail base URL",
         "Set TESTRAIL_URL in .env (e.g. http://testraildb/testrail)."),
        ("TESTRAIL_USER", "TestRail login email",
         "Set TESTRAIL_USER in .env (your login email)."),
        ("TESTRAIL_API_KEY", "TestRail API key / password",
         "Set TESTRAIL_API_KEY in .env (My Settings -> API Keys; or AD password on instances "
         "without API keys)."),
    ):
        if _env_value(var):
            out.append(Check(var, READY, detail="set"))
        else:
            out.append(Check(var, NEEDS_YOU, detail="missing - secret, must be human-supplied", fix=fix))
    return out


def _check_project_id() -> Check:
    if _env_value("TESTRAIL_PROJECT_ID"):
        return Check("TESTRAIL_PROJECT_ID", READY, detail="set")
    return Check(
        "TESTRAIL_PROJECT_ID",
        MANUAL,
        detail="not set (optional - you can pass --project per command)",
        fix="Optional: set TESTRAIL_PROJECT_ID in .env to your project's numeric id "
            "(run `check` to list ids).",
    )


def _check_write_suite() -> Check:
    if _env_value("TESTRAIL_WRITE_SUITE_ID"):
        return Check("TESTRAIL_WRITE_SUITE_ID", READY, detail="set - writes target this suite")
    return Check(
        "TESTRAIL_WRITE_SUITE_ID",
        NEEDS_YOU,
        detail="not set - required before BUILDING a suite (reads/audits work without it)",
        fix="Create the NEW target suite in the TestRail UI (the API can't create suites on this "
            "instance), then set TESTRAIL_WRITE_SUITE_ID to its id. Writes go ONLY there.",
    )


def _check_testrail_reachable() -> Check:
    """Try one lightweight read. Skips cleanly if creds/deps aren't ready yet."""
    if importlib.util.find_spec("requests") is None:
        return Check("TestRail connectivity", MANUAL,
                     detail="skipped - install deps first")
    if not all(_env_value(v) for v in ("TESTRAIL_URL", "TESTRAIL_USER", "TESTRAIL_API_KEY")):
        return Check("TestRail connectivity", MANUAL,
                     detail="skipped - credentials incomplete (see above)")
    try:
        from system_test_ops.testrail.client import TestRailClient

        projects = TestRailClient().get_projects()
        return Check("TestRail connectivity", READY,
                     detail=f"reachable - {len(projects)} project(s) visible")
    except Exception as exc:  # noqa: BLE001 - surface the real reason, never crash the preflight
        msg = str(exc).splitlines()[0][:160] if str(exc) else exc.__class__.__name__
        return Check(
            "TestRail connectivity",
            NEEDS_YOU,
            detail=f"unreachable - {msg}",
            fix="Check you're on the internal network / VPN (this instance is internal-only), and "
                "that TESTRAIL_URL + credentials are correct. Re-run `python -m system_test_ops check`.",
        )


def _check_git() -> Check:
    if shutil.which("git"):
        return Check("git", READY, detail="on PATH")
    return Check(
        "git",
        MANUAL,
        detail="not on PATH (optional - needed only for the clone/PR workflow)",
        fix="Optional: install git if you want the version-control/PR workflow.",
    )


def _check_atlassian_mcp() -> Check:
    # The MCP connection lives at the Claude Code layer; a plain Python process can't see it.
    return Check(
        "Atlassian (JIRA) MCP",
        MANUAL,
        detail="can't be auto-checked here - verify in Claude Code",
        fix="Run /mcp in Claude Code and connect the Atlassian (Rovo) server. Needed only for "
            "coverage / feature / defect work (not for a pure restructure).",
    )


# --------------------------------------------------------------------------- #
# orchestration + rendering
# --------------------------------------------------------------------------- #
def run_checks() -> list[Check]:
    """Run every readiness check, in report order."""
    checks: list[Check] = [
        _check_python(),
        _check_venv(),
        _check_deps(),
        _check_env_file(),
    ]
    checks.extend(_check_testrail_creds())
    checks.append(_check_project_id())
    checks.append(_check_write_suite())
    checks.append(_check_testrail_reachable())
    checks.append(_check_git())
    checks.append(_check_atlassian_mcp())
    return checks


# ASCII markers only - this repo has been bitten repeatedly by cp1252 consoles
# mangling unicode glyphs; keep the readiness report safe in any terminal.
_GROUPS = [
    (READY, "READY", "[ok]"),
    (CLAUDE, "CLAUDE CAN HANDLE (no input from you)", "[->]"),
    (NEEDS_YOU, "NEEDS YOU", "[!!]"),
    (MANUAL, "CHECK MANUALLY", "[??]"),
]


def render(checks: list[Check]) -> str:
    """Human-readable readiness report, grouped by who-does-what."""
    lines = ["system-test-ops - readiness check", "=" * 33, ""]
    for status, heading, glyph in _GROUPS:
        group = [c for c in checks if c.status == status]
        if not group:
            continue
        lines.append(heading)
        for c in group:
            detail = f" - {c.detail}" if c.detail else ""
            lines.append(f"  {glyph} {c.name}{detail}")
            if c.fix and status in (NEEDS_YOU, CLAUDE, MANUAL):
                lines.append(f"      -> {c.fix}")
        lines.append("")

    blockers = [c for c in checks if c.status == NEEDS_YOU]
    claude_todo = [c for c in checks if c.status == CLAUDE]
    if blockers:
        lines.append(f"VERDICT: {len(blockers)} item(s) need you before a build can start.")
        if claude_todo:
            lines.append(f"         ({len(claude_todo)} more Claude can set up for you once those are in.)")
    elif claude_todo:
        lines.append(f"VERDICT: ready once Claude runs {len(claude_todo)} setup step(s) for you "
                     "(no input needed).")
    else:
        lines.append("VERDICT: all green - ready to work.")
    return "\n".join(lines) + "\n"


def has_blockers(checks: list[Check]) -> bool:
    return any(c.status == NEEDS_YOU for c in checks)
