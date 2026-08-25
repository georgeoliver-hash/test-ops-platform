"""First-connect device probe.

Run this the *first* time ADB can reach a device. It captures everything the
framework wants to know (BOSRecords path, EventLog event types, packages,
processes, getprop snapshot, screenshot, on-device DatasetParameters) into a
timestamped report directory.

Why this exists: SEARCH_PATHS and known event types in the framework are
seeded from the SD-card scrape — they may be wrong on a different device or
firmware. This probe surfaces the truth in one shot so we can tune the
framework from real data instead of guessing.

Usage:
    python -m tools.first_connect <adb-serial>
    python -m tools.first_connect 10.0.0.51:5555
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

from framework.android.configuration import Configuration
from framework.android.eventlog import EventLog
from framework.android.shell import AndroidShell
from framework.bos.local_audit import LocalAuditLedger
from framework.registry.models import ADBTransport
from framework.transport.adb import ADBTransportImpl


REPORT_ROOT = Path(__file__).resolve().parent

INTERESTING_PROPS = [
    "ro.product.model",
    "ro.product.device",
    "ro.product.name",
    "ro.product.manufacturer",
    "ro.build.version.release",
    "ro.build.version.sdk",
    "ro.build.fingerprint",
    "ro.serialno",
    "net.hostname",
]

INTERESTING_PACKAGES = [
    "com.flowbird.pos",                              # main UI app
    "com.parkeon.platform",                          # platform daemon
    "com.parkeon.systemstate",                       # systemstate daemon (event source)
    "com.parkeon.base",                              # base resources
    "com.parkeon.updater",                           # software updater
    "com.parkeon.periphs.dallas",                    # one-wire memory chip driver
    "com.parkeon.periphs.pknBixolonUsbSerialLcd",    # Bixolon printer/LCD driver
    "com.parkeon.periphs.pknUsbPrinter",             # USB printer driver
    "com.parkeon.services.ntp",                      # NTP service
    "com.parkeon.services.ledsHub",                  # LED control
    "com.parkeon.bsp.maintenance",                   # maintenance back-end
]

INTERESTING_PROCESSES = [
    "pkn_command_server",
    "com.parkeon.platform",
    "com.parkeon.systemstate",
    "com.flowbird.pos",
    "com.parkeon.updater",
]

CANDIDATE_CONFIG_PATHS = [
    "/sdcard/state/params/DM/DatasetParameters.json",
    "/storage/emulated/0/state/params/DM/DatasetParameters.json",
    "/data/data/com.flowbird.pos/files/state/params/DM/DatasetParameters.json",
    "/sdcard/Android/data/com.flowbird.pos/files/state/params/DM/DatasetParameters.json",
    "/sdcard/pos/backofficeagent.config.json",
    "/sdcard/Android/data/com.flowbird.pos/files/pos/backofficeagent.config.json",
]

# Configuration tree paths from artifacts/common.xml — known to exist in the
# build's default config. Probing them confirms which URI format the provider
# expects (segment-based vs ?path= query arg).
CANDIDATE_CONFIG_TREE_PATHS = [
    "/system/debug/mode",
    "/system/time/timezone",
    "/system/network/modem/enable",
    "/system/network/ethernet/enable",
    "/pknUsbPrinter/printing/speed",
]


def probe(serial: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    transport = ADBTransportImpl(ADBTransport(serial=serial))
    transport.connect()

    report: dict = {
        "serial": serial,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "errors": [],
    }

    try:
        # ─── shell smoke ───
        echo = transport.run("echo first_connect_ok")
        report["echo_ok"] = echo.ok and "first_connect_ok" in echo.stdout
        if not report["echo_ok"]:
            report["errors"].append(f"echo failed: stderr={echo.stderr!r}")
            return report

        sh = AndroidShell(transport)
        elog = EventLog(transport)
        cfg = Configuration(transport)

        # ─── identity ───
        report["props"] = {p: sh.getprop(p) for p in INTERESTING_PROPS}

        # ─── packages ───
        report["packages"] = {}
        for pkg in INTERESTING_PACKAGES:
            installed = sh.is_package_installed(pkg)
            entry: dict = {"installed": installed}
            if installed:
                entry["versionName"] = sh.package_version(pkg)
            report["packages"][pkg] = entry

        # ─── processes ───
        report["processes"] = {p: sh.is_process_running(p) for p in INTERESTING_PROCESSES}

        # ─── audit ledger discovery ───
        ledger = LocalAuditLedger(transport)
        path = ledger.discover()
        report["audit_ledger"] = {
            "path": path,
            "search_paths_tried": LocalAuditLedger.SEARCH_PATHS,
            "record_count": len(ledger.list_records()) if path else 0,
        }
        if path and ledger.list_records():
            newest = ledger.newest_record()
            if newest:
                # Truncate raw to keep the report readable.
                raw = newest.get("_raw")
                if isinstance(raw, str) and len(raw) > 800:
                    newest = {**newest, "_raw": raw[:800] + "...[truncated]"}
                report["audit_ledger"]["newest_record"] = newest

        # ─── EventLog discovery ───
        event_types = elog.list_event_types()
        report["eventlog"] = {
            "discovered_types": event_types,
            "latest_indexes": {t: elog.latest_index(t) for t in event_types},
        }

        # ─── known config files ───
        report["config_files"] = {}
        for candidate in CANDIDATE_CONFIG_PATHS:
            if sh.file_exists(candidate):
                content = sh.cat(candidate)
                try:
                    parsed = json.loads(content)
                except json.JSONDecodeError:
                    parsed = content[:2000]
                report["config_files"][candidate] = parsed

        # ─── Configuration content provider probe ───
        # Records both URI styles' raw responses so we can pick the right one.
        report["configuration_provider"] = {}
        for path in CANDIDATE_CONFIG_TREE_PATHS:
            report["configuration_provider"][path] = {
                "value": cfg.get(path),
                "raw_per_uri": cfg.get_raw(path),
            }

        # ─── screenshot ───
        screenshot_path = out_dir / "screenshot.png"
        try:
            sh.screenshot(str(screenshot_path))
            report["screenshot"] = {
                "path": str(screenshot_path),
                "size_bytes": screenshot_path.stat().st_size if screenshot_path.exists() else 0,
            }
        except Exception as e:
            report["errors"].append(f"screenshot failed: {e}")

        # ─── current activity (where the user/app is right now) ───
        report["current_activity"] = sh.current_activity()

    finally:
        transport.disconnect()
        report["finished_at"] = datetime.now().isoformat(timespec="seconds")

    return report


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python -m tools.first_connect <adb-serial>", file=sys.stderr)
        return 2
    serial = argv[1]
    safe_serial = re.sub(r"[^\w.-]", "_", serial)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = REPORT_ROOT / f"first_connect_{safe_serial}_{timestamp}"

    report = probe(serial, out_dir)

    report_path = out_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    print(f"\nReport: {report_path}")
    print(f"  echo_ok:                {report.get('echo_ok')}")
    print(f"  audit ledger path:      {report.get('audit_ledger', {}).get('path')}")
    print(f"  EventLog types found:   {len(report.get('eventlog', {}).get('discovered_types', []))}")
    print(f"  packages installed:     "
          f"{sum(1 for p in report.get('packages', {}).values() if p.get('installed'))}/"
          f"{len(report.get('packages', {}))}")
    print(f"  processes running:      "
          f"{sum(1 for v in report.get('processes', {}).values() if v)}/"
          f"{len(report.get('processes', {}))}")
    if report.get("errors"):
        print("\nERRORS:")
        for e in report["errors"]:
            print(f"  - {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
