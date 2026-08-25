"""Readiness preflight for the automation-tests repo.

Answers the day-one question for anyone picking this up: *what's set up, what can
Claude handle, and what do I (the human) still need to do before I can run tests
against a real device?*

    python -m tools.doctor                 # check the default project (translink)
    python -m tools.doctor --project nta    # a different project
    python -m tools.doctor --device         # also probe live device reachability (slower)

Read-only. Never writes or mutates. Informational by default (exit 0); pass
`--gate` to exit non-zero when a human-action item is outstanding (CI / pre-run).

This is the broad environment+stack check. For the fast "is the device's ADB
window open right now?" check used immediately before a robot run, use
`python -m tools.adb_ready --project <name> --wait 30`.

ASCII-only output — Windows consoles default to cp1252 and choke on fancy glyphs.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Status buckets (mirrors the sibling system-test-ops doctor for consistency).
READY = "ready"          # [ok] already in place
CLAUDE = "claude"        # [->] Claude can do this autonomously, no human input
NEEDS_YOU = "you"        # [!!] a human must act (install, secret, network, physical device)
MANUAL = "manual"        # [??] can't be auto-verified here / informational

# Core deps (always needed) and the optional extras keyed by the work they enable.
_CORE_IMPORTS = {"robot": "robotframework", "yaml": "PyYAML", "pydantic": "pydantic",
                 "requests": "requests", "dotenv": "python-dotenv"}
_EXTRA_IMPORTS = {
    "android": {"adbutils": "adbutils", "appium": "Appium-Python-Client"},
    "ssh": {"paramiko": "paramiko"},
    "web": {"playwright": "playwright"},
}

DEFAULT_APPIUM_URL = "http://127.0.0.1:4723"


@dataclass
class Check:
    name: str
    status: str
    detail: str = ""
    fix: str = ""


# --------------------------------------------------------------------------- #
# environment checks
# --------------------------------------------------------------------------- #
def _check_python() -> Check:
    major, minor = sys.version_info[:2]
    ver = f"{major}.{minor}.{sys.version_info[2]}"
    if (major, minor) >= (3, 11):
        return Check("Python 3.11+", READY, detail=f"running {ver}")
    return Check("Python 3.11+", NEEDS_YOU, detail=f"running {ver} - too old",
                 fix="Install Python 3.11+ and recreate the .venv.")


def _check_venv() -> Check:
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return Check("Virtual environment", READY, detail=f"active ({sys.prefix})")
    return Check("Virtual environment", CLAUDE, detail="not running inside a .venv",
                 fix='python -m venv .venv ; .\\.venv\\Scripts\\Activate.ps1 ; pip install -e ".[all]"')


def _check_core_deps() -> Check:
    missing = [label for mod, label in _CORE_IMPORTS.items()
               if importlib.util.find_spec(mod) is None]
    if not missing:
        return Check("Core dependencies", READY, detail="all importable")
    return Check("Core dependencies", CLAUDE, detail="missing: " + ", ".join(missing),
                 fix='pip install -e ".[dev]"  (from the repo root, inside the .venv)')


def _check_extra_deps() -> list[Check]:
    """Report each optional extra (android/ssh/web) as present-or-not. Android is
    the one that matters for the live POS work, so a missing android extra is a
    Claude-can-fix, not just info."""
    out: list[Check] = []
    for extra, mods in _EXTRA_IMPORTS.items():
        missing = [label for mod, label in mods.items()
                   if importlib.util.find_spec(mod) is None]
        if not missing:
            out.append(Check(f"'{extra}' extra", READY, detail="installed"))
        else:
            status = CLAUDE if extra == "android" else MANUAL
            out.append(Check(
                f"'{extra}' extra", status,
                detail="missing: " + ", ".join(missing) +
                       ("" if extra == "android" else " (only needed for this transport)"),
                fix=f'pip install -e ".[{extra}]"' +
                    ("" if extra == "android" else " - only if you test this kind of device"),
            ))
    return out


def _check_adb_on_path() -> Check:
    if shutil.which("adb"):
        return Check("adb on PATH", READY, detail="found")
    return Check("adb on PATH", NEEDS_YOU, detail="not found",
                 fix="Install Android platform-tools and add `adb` to PATH (needed for any ADB device).")


def _check_robot_on_path() -> Check:
    """The `robot` console script (installed alongside the robotframework
    package) — some setups prefer `robot ...` on PATH over `python -m robot`."""
    if shutil.which("robot"):
        return Check("robot on PATH", READY, detail="found")
    if importlib.util.find_spec("robot") is not None:
        return Check("robot on PATH", MANUAL,
                     detail="robotframework importable but no `robot` console script on PATH",
                     fix='Use `python -m robot ...` instead, or add the venv Scripts dir to PATH.')
    return Check("robot on PATH", CLAUDE, detail="robotframework not installed",
                 fix='pip install -e ".[dev]"  (from the repo root, inside the .venv)')


def _check_appium_server() -> Check:
    """GET <APPIUM_URL>/status. Appium replies {value:{ready:true}} when up."""
    url = os.environ.get("APPIUM_URL", DEFAULT_APPIUM_URL).rstrip("/")
    if importlib.util.find_spec("requests") is None:
        return Check("Appium server", MANUAL, detail="skipped - install core deps first")
    try:
        import requests

        resp = requests.get(url + "/status", timeout=4)
        ready = bool((resp.json().get("value") or {}).get("ready"))
        if resp.ok and ready:
            return Check("Appium server", READY, detail=f"up at {url}")
        return Check("Appium server", NEEDS_YOU, detail=f"responded but not ready at {url}",
                     fix="Restart the Appium server: `appium` (UiAutomator2 driver installed).")
    except Exception:  # noqa: BLE001 - connection refused etc. is the common, expected case
        return Check(
            "Appium server", NEEDS_YOU, detail=f"not reachable at {url}",
            fix="Start it in a terminal: `appium` (install once via `npm i -g appium` + "
                "`appium driver install uiautomator2`). Override the URL with APPIUM_URL.",
        )


def _check_node_appium_cli() -> Check:
    if shutil.which("appium"):
        return Check("Appium CLI", READY, detail="on PATH")
    if shutil.which("node") or shutil.which("npm"):
        return Check("Appium CLI", NEEDS_YOU, detail="node present but `appium` not installed",
                     fix="npm i -g appium ; appium driver install uiautomator2")
    return Check("Appium CLI", NEEDS_YOU, detail="node/npm not found",
                 fix="Install Node.js, then: npm i -g appium ; appium driver install uiautomator2")


def _robot_safe_env() -> dict:
    """Robot Framework's console writer passes `PYTHONIOENCODING` straight to
    `str.encode()` as an encoding name. A `codec:errors` value (e.g.
    `utf-8:surrogateescape`, set by some shells/terminal hosts) is a valid
    thing for Python's IO layer to consume but not a valid codec name, so RF
    dies with `LookupError: unknown encoding`. Strip the `:errors` suffix for
    the subprocess only — real environment behaviour is unaffected."""
    env = os.environ.copy()
    value = env.get("PYTHONIOENCODING", "")
    if ":" in value:
        env["PYTHONIOENCODING"] = value.split(":", 1)[0]
    return env


def _check_robot_dryrun(project: str) -> Check:
    """`robot --dryrun` over the project's suites — resolves every keyword and
    tag without touching a device. Catches missing keywords, bad resource
    paths, or import errors before a live run does. Replaces the old pytest
    collection check."""
    suite_dir = REPO_ROOT / "projects" / project / "tests"
    if not suite_dir.exists():
        return Check("Robot dry-run", MANUAL, detail=f"no projects/{project}/tests directory")
    if importlib.util.find_spec("robot") is None:
        return Check("Robot dry-run", CLAUDE, detail="robotframework not installed",
                     fix='pip install -e ".[dev]"  (from the repo root, inside the .venv)')
    try:
        result = subprocess.run(
            [sys.executable, "-m", "robot", "--dryrun", "--variable", f"PROJECT:{project}",
             "--outputdir", str(REPO_ROOT / "artifacts" / "doctor_dryrun"), str(suite_dir)],
            capture_output=True, text=True, timeout=60, cwd=REPO_ROOT,
            env=_robot_safe_env(),
        )
        if result.returncode == 0:
            return Check("Robot dry-run", READY, detail=f"projects/{project}/tests resolves cleanly")
        tail = (result.stdout or result.stderr).strip().splitlines()[-1] if (result.stdout or result.stderr) else ""
        return Check("Robot dry-run", CLAUDE, detail=f"failures found - {tail[:160]}",
                     fix=f"robot --dryrun projects/{project}/tests  (see artifacts/doctor_dryrun/log.html)")
    except subprocess.TimeoutExpired:
        return Check("Robot dry-run", MANUAL, detail="timed out after 60s")
    except Exception as exc:  # noqa: BLE001
        return Check("Robot dry-run", MANUAL, detail=f"could not run - {type(exc).__name__}: {exc}")


def _check_project_registry(project: str) -> tuple[Check, list]:
    """Load and validate the project's devices.yaml via the pydantic model.

    Returns (check, devices) so later checks can reuse the loaded devices.
    """
    try:
        from framework.registry.loader import load_project

        proj = load_project(project)
        return (Check(f"Project registry ({project})", READY,
                      detail=f"loaded, {len(proj.devices)} device(s)"),
                proj.devices)
    except FileNotFoundError:
        return (Check(f"Project registry ({project})", NEEDS_YOU,
                      detail=f"no devices.yaml for '{project}'",
                      fix=f"Create projects/{project}/devices.yaml (copy an existing project's)."),
                [])
    except Exception as exc:  # noqa: BLE001 - surface validation errors, never crash the preflight
        msg = str(exc).splitlines()[0][:160]
        return (Check(f"Project registry ({project})", CLAUDE,
                      detail=f"failed to load: {msg}",
                      fix="devices.yaml or the registry model needs a fix - Claude can sort this."),
                [])


def _check_device_secrets(devices: list) -> list[Check]:
    """For SSH devices, the password env var must be set (it's a secret)."""
    out: list[Check] = []
    for d in devices:
        transport = getattr(d, "transport", None)
        var = getattr(transport, "env_password_var", None)
        if not var:
            continue
        if os.environ.get(var):
            out.append(Check(f"secret {var}", READY, detail=f"set (for {d.id})"))
        else:
            out.append(Check(f"secret {var}", NEEDS_YOU,
                             detail=f"not set - needed for SSH device {d.id}",
                             fix=f"Set the env var {var} to that device's password (secret; don't commit)."))
    return out


def _check_devices_live(devices: list) -> list[Check]:
    """Optional quick reachability snapshot for ADB devices (instant, no wait)."""
    out: list[Check] = []
    try:
        from tools.adb_ready import check_serial
        from framework.registry.models import ADBTransport
    except Exception as exc:  # noqa: BLE001 - missing android extra etc.
        return [Check("Device reachability", MANUAL,
                      detail=f"skipped - {type(exc).__name__} (install the 'android' extra)")]
    if shutil.which("adb") is None:
        return [Check("Device reachability", MANUAL, detail="skipped - adb not on PATH")]
    for d in devices:
        if not isinstance(getattr(d, "transport", None), ADBTransport):
            continue
        serial = d.transport.serial
        try:
            checks = check_serial(serial, wait_seconds=0.0)
            ok = all(c.ok for c in checks)
            detail = "; ".join(f"{c.label}={'ok' if c.ok else 'FAIL'}" for c in checks)
        except Exception as exc:  # noqa: BLE001
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        if ok:
            out.append(Check(f"device {serial}", READY, detail="reachable now"))
        else:
            out.append(Check(f"device {serial}", NEEDS_YOU, detail=detail,
                             fix="The TCP-5555 adbd window flips intermittently. Reconnect "
                                 "(`adb disconnect; adb connect <serial>`) or wait: "
                                 "`python -m tools.adb_ready --project <name> --wait 30`."))
    if not out:
        out.append(Check("Device reachability", MANUAL, detail="no ADB devices in this project"))
    return out


# --------------------------------------------------------------------------- #
# orchestration + rendering
# --------------------------------------------------------------------------- #
def run_checks(project: str = "translink", probe_devices: bool = False) -> list[Check]:
    checks: list[Check] = [_check_python(), _check_venv(), _check_core_deps()]
    checks.extend(_check_extra_deps())
    checks.append(_check_adb_on_path())
    checks.append(_check_robot_on_path())
    checks.append(_check_node_appium_cli())
    checks.append(_check_appium_server())
    reg_check, devices = _check_project_registry(project)
    checks.append(reg_check)
    checks.append(_check_robot_dryrun(project))
    checks.extend(_check_device_secrets(devices))
    if probe_devices:
        checks.extend(_check_devices_live(devices))
    return checks


_GROUPS = [
    (READY, "READY", "[ok]"),
    (CLAUDE, "CLAUDE CAN HANDLE (no input from you)", "[->]"),
    (NEEDS_YOU, "NEEDS YOU", "[!!]"),
    (MANUAL, "CHECK MANUALLY / INFO", "[??]"),
]


def render(checks: list[Check]) -> str:
    lines = ["automation-tests - readiness check", "=" * 34, ""]
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
        lines.append(f"VERDICT: {len(blockers)} item(s) need you before tests can run against a device.")
        if claude_todo:
            lines.append(f"         ({len(claude_todo)} more Claude can set up for you.)")
    elif claude_todo:
        lines.append(f"VERDICT: ready once Claude runs {len(claude_todo)} setup step(s) (no input needed).")
    else:
        lines.append("VERDICT: all green - ready to run tests.")
    return "\n".join(lines) + "\n"


def has_blockers(checks: list[Check]) -> bool:
    return any(c.status == NEEDS_YOU for c in checks)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="Readiness preflight for automation-tests")
    parser.add_argument("--project", default="translink", help="project whose devices.yaml to check (default: translink)")
    parser.add_argument("--device", action="store_true", help="also probe live ADB device reachability (slower)")
    parser.add_argument("--gate", action="store_true", help="exit non-zero if a human-action item is outstanding")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    checks = run_checks(project=args.project, probe_devices=args.device)
    print(render(checks))
    if args.gate and has_blockers(checks):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
