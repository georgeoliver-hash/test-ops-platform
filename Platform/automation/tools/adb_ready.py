"""Fast ADB-readiness preflight.

The way6 INF212 device only opens its TCP-5555 adbd window intermittently. This
tool answers, in under a few seconds: *is the device currently reachable right
now, and is the POS app installed?* Use it before kicking off a robot run.

Distinct from `tools/first_connect.py`, which is a one-time deep probe (full
provider/package/process inventory). This is the fast version.

Usage:
    # Check a specific serial
    python -m tools.adb_ready 192.168.3.151:5555

    # Check every ADB device in a project's devices.yaml
    python -m tools.adb_ready --project translink

    # Wait up to 30s for the device to come online (handy when the window flips)
    python -m tools.adb_ready --project translink --wait 30

Exit codes:
    0  every checked device is reachable and the POS app is installed
    1  at least one device failed a check
    2  bad invocation (e.g. neither serial nor --project)
    3  `adb` not on PATH
"""
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass

from framework.android.shell import AndroidShell
from framework.registry.loader import load_project
from framework.registry.models import ADBTransport
from framework.transport.adb import ADBTransportImpl


POS_PACKAGE = "com.flowbird.pos"


@dataclass
class Check:
    label: str
    ok: bool
    detail: str = ""


def check_serial(serial: str, *, wait_seconds: float) -> list[Check]:
    """Run the fast checks for one ADB serial. Order matters — bail early on the
    first hard failure (no adb → no point trying state)."""
    checks: list[Check] = []
    transport = ADBTransportImpl(ADBTransport(serial=serial))

    # `adb connect` for TCP serials; harmless for USB serials.
    if ":" in serial:
        transport._adb("connect", serial, timeout=5)

    if wait_seconds > 0:
        state = transport.wait_until_device(timeout=wait_seconds, poll_interval=1.0)
    else:
        state = transport.get_state()
    checks.append(Check("state==device", state == "device", f"state={state!r}"))
    if state != "device":
        return checks

    # From here on the transport is usable.
    r = transport.run("echo adb_ready_ok", timeout=5)
    checks.append(Check(
        "shell echo",
        r.ok and "adb_ready_ok" in r.stdout,
        f"exit={r.exit_code}",
    ))
    if not (r.ok and "adb_ready_ok" in r.stdout):
        return checks

    sh = AndroidShell(transport)
    installed = sh.is_package_installed(POS_PACKAGE)
    version = sh.package_version(POS_PACKAGE) if installed else None
    checks.append(Check(
        f"{POS_PACKAGE} installed",
        installed,
        f"versionName={version}" if version else "",
    ))
    return checks


def serials_for_project(name: str) -> list[str]:
    proj = load_project(name)
    return [
        d.transport.serial for d in proj.devices
        if isinstance(d.transport, ADBTransport)
    ]


def print_report(serial: str, checks: list[Check]) -> bool:
    all_ok = all(c.ok for c in checks)
    status = "READY" if all_ok else "NOT READY"
    print(f"\n{serial}  [{status}]")
    for c in checks:
        glyph = "OK" if c.ok else "FAIL"
        suffix = f"  ({c.detail})" if c.detail else ""
        print(f"  [{glyph}] {c.label}{suffix}")
    return all_ok


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fast ADB-readiness preflight")
    parser.add_argument("serial", nargs="?", help="adb serial, e.g. 192.168.3.151:5555")
    parser.add_argument("--project", help="check every ADB device in this project's devices.yaml")
    parser.add_argument(
        "--wait",
        type=float,
        default=0.0,
        help="seconds to wait for state==device before declaring failure (default: 0, instant check)",
    )
    args = parser.parse_args(argv[1:])

    if not args.serial and not args.project:
        parser.print_usage(file=sys.stderr)
        print("error: pass a serial, or --project <name>", file=sys.stderr)
        return 2

    if shutil.which("adb") is None:
        print("error: `adb` is not on PATH. Install platform-tools or fix PATH.", file=sys.stderr)
        return 3

    if args.serial:
        serials = [args.serial]
    else:
        try:
            serials = serials_for_project(args.project)
        except FileNotFoundError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not serials:
            print(f"error: project {args.project!r} has no ADB devices in devices.yaml", file=sys.stderr)
            return 2

    all_ok = True
    for serial in serials:
        try:
            checks = check_serial(serial, wait_seconds=args.wait)
        except Exception as e:
            print(f"\n{serial}  [ERROR]\n  {type(e).__name__}: {e}")
            all_ok = False
            continue
        all_ok &= print_report(serial, checks)

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
