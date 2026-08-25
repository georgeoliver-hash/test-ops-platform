"""Robot Framework Library: device resolution, connection, and log capture.

Replaces the pytest `device`/`transport`/`ui` fixtures and the root conftest's
`pytest_generate_tests` device parametrization.

Scope note: this library is **SUITE**-scoped, not TEST-scoped like the other
libraries in `framework/robot/`. The old `transport` fixture reconnected on
every test, but a live device connection is expensive and these suites are
already one-physical-unit-per-file, so `Connect To Device` (Suite Setup)
connects once and `Disconnect From Device` (Suite Teardown) closes it once.
Per-test isolation — clearing the log window before each test, pulling
logs/screenshots after — still happens at Test Setup/Teardown via `Clear
Device Logs` / `Collect Device Logs`, matching the granularity the old
`transport` fixture's setup/teardown gave each test.

Device selection: no dynamic parametrization (RF has no direct equivalent of
`metafunc.parametrize`). A suite targets exactly one device, named by the
`${DEVICE_ID}` variable (`--variable DEVICE_ID:translink-pos-01` or the
`DEVICE_ID` env var) or, if unset, the first device in the project's
`devices.yaml` whose type is in the suite's `${DEVICE_TYPES}` variable
(comma-separated, set in each suite's `*** Variables ***` table — the RF
analogue of the old `@pytest.mark.device_types(...)` marker).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from robot.api import logger
from robot.api.deco import keyword, library
from robot.api.exceptions import SkipExecution

from framework.android.shell import AndroidShell
from framework.registry.loader import load_project
from framework.registry.models import (
    ADBTransport,
    Device,
    NullTransport,
    OS,
    Project,
    SSHTransport,
    UIKind,
)
from framework.transport.adb import ADBTransportImpl
from framework.transport.base import Transport
from framework.transport.null import NullTransportImpl
from framework.transport.ssh import SSHTransportImpl
from framework.ui.android import AndroidUIDriver
from framework.ui.base import UIDriver
from framework.ui.web import WebUIDriver


def _make_transport(device: Device) -> Transport:
    if isinstance(device.transport, SSHTransport):
        return SSHTransportImpl(device.transport)
    if isinstance(device.transport, ADBTransport):
        return ADBTransportImpl(device.transport)
    if isinstance(device.transport, NullTransport):
        return NullTransportImpl(device.transport)
    raise ValueError(f"Unknown transport for device {device.id}")


def _make_ui(device: Device) -> UIDriver | None:
    if device.ui == UIKind.ANDROID_APP:
        return AndroidUIDriver(device)
    if device.ui == UIKind.WEB:
        return WebUIDriver(device)
    return None


@library(scope="SUITE")
class DeviceLibrary:
    """`Connect To Device` / `Disconnect From Device` (Suite Setup/Teardown)
    plus per-test log capture (Test Setup/Teardown). Other `framework/robot/`
    libraries (AndroidLibrary, BOSLibrary, WinceLibrary) pull the connected
    device/transport from this library via
    `BuiltIn().get_library_instance('DeviceLibrary')`.
    """

    def __init__(self):
        self.project: Project | None = None
        self.device: Device | None = None
        self.transport: Transport | None = None
        self.ui: UIDriver | None = None

    # ─── connection lifecycle ───────────────────────────────────────────────

    @keyword("Resolve Device")
    def resolve_device(self, device_id: str = "") -> Device:
        """Load the project registry and pick the device object for this suite
        — no transport connection. Use as Suite Setup for suites that only
        read `Get Connected Device`'s metadata (e.g. a registry-vs-build-file
        version comparison) without ever touching the device, mirroring how
        the pytest `device` fixture alone (without `transport`/`android`) never
        connected anything."""
        project_name = os.getenv("PROJECT", "")
        try:
            from robot.libraries.BuiltIn import BuiltIn

            project_name = BuiltIn().get_variable_value("${PROJECT}", project_name)
        except Exception:
            pass
        if not project_name:
            raise RuntimeError(
                "PROJECT not set — pass --variable PROJECT:<name> or set the PROJECT env var"
            )
        self.project = load_project(project_name)

        resolved_id = device_id or self._variable("DEVICE_ID", os.getenv("DEVICE_ID", ""))
        device_types = self._suite_device_types()
        self.device = self._resolve_device(resolved_id, device_types)
        return self.device

    @keyword("Connect To Device")
    def connect_to_device(self, device_id: str = "") -> None:
        """`Resolve Device` plus an actual transport connection. Use as Suite
        Setup for suites that drive or read from the live device."""
        self.resolve_device(device_id)

        self.transport = _make_transport(self.device)
        try:
            self.transport.connect()
        except Exception as e:
            raise SkipExecution(f"Cannot connect to {self.device.id}: {e}") from e

        logger.info(
            f"Connected to {self.device.id} "
            f"(type={self.device.type.value}, os={self.device.os.value})"
        )
        self.clear_device_logs()

    @keyword("Disconnect From Device")
    def disconnect_from_device(self) -> None:
        if self.transport is not None:
            self.transport.disconnect()

    @keyword("Start Device UI")
    def start_device_ui(self) -> UIDriver:
        """Start the device's UI driver (Appium for android_app, Playwright for
        web). Raises SkipExecution if the device has no UI surface or the
        driver fails to start (Appium down, portal unreachable, etc.) —
        mirrors the old `ui` fixture."""
        drv = _make_ui(self.device)
        if drv is None:
            raise SkipExecution(f"Device {self.device.id} has no UI surface")
        try:
            drv.start()
        except Exception as e:
            raise SkipExecution(str(e)) from e
        self.ui = drv
        return drv

    @keyword("Stop Device UI")
    def stop_device_ui(self) -> None:
        if self.ui is not None:
            self.ui.stop()
            self.ui = None

    # ─── accessors for other framework/robot libraries ──────────────────────

    @keyword("Get Connected Device")
    def get_connected_device(self) -> Device:
        return self.device

    @keyword("Get Transport")
    def get_transport(self) -> Transport:
        return self.transport

    @keyword("Get Project")
    def get_project(self) -> Project:
        return self.project

    @keyword("Get Device Metadata Value")
    def get_device_metadata_value(self, key: str, default=None):
        return self.device.metadata.get(key, default)

    @keyword("Get Device Build Version")
    def get_device_build_version(self):
        return self.device.build.version if self.device.build else None

    @keyword("Get Device UI")
    def get_device_ui(self) -> UIDriver:
        return self.ui

    # ─── raw transport access ────────────────────────────────────────────────

    @keyword("Run On Device")
    def run_on_device(self, command: str, timeout: float = 30.0):
        return self.transport.run(command, timeout=timeout)

    @keyword("Push To Device")
    def push_to_device(self, local: str, remote: str) -> None:
        self.transport.push(local, remote)

    @keyword("Pull From Device")
    def pull_from_device(self, remote: str, local: str) -> None:
        self.transport.pull(remote, local)

    # ─── per-test log capture ────────────────────────────────────────────────

    @keyword("Clear Device Logs")
    def clear_device_logs(self) -> None:
        """Clear the device's rolling log buffer so the teardown pull captures
        only the current test's window. Best effort; never raises."""
        try:
            if isinstance(self.device.transport, ADBTransport):
                self.transport.run("logcat -c", timeout=10)
        except Exception:
            pass

    @keyword("Collect Device Logs")
    def collect_device_logs(self, report_dir: str) -> list:
        """Pull a recent slice of device logs into `report_dir`. Returns the
        list of files written (possibly empty). Best effort; never raises."""
        out_dir = Path(report_dir)
        written: list[str] = []
        try:
            if isinstance(self.device.transport, ADBTransport):
                result = self.transport.run("logcat -d -v threadtime -t 500", timeout=15)
                target = out_dir / "logcat.txt"
                target.write_text(result.stdout or "(empty)", encoding="utf-8")
                written.append(str(target))
            elif isinstance(self.device.transport, SSHTransport):
                if self.device.os == OS.WINCE:
                    return written
                result = self.transport.run("journalctl -n 500 --no-pager", timeout=15)
                if result.exit_code != 0:
                    result = self.transport.run("dmesg | tail -n 500", timeout=15)
                target = out_dir / "journal.txt"
                target.write_text(result.stdout or "(empty)", encoding="utf-8")
                written.append(str(target))
        except Exception as e:
            logger.warn(f"device log collection failed: {e}")
        return written

    @keyword("Capture UI State On Failure")
    def capture_ui_state_on_failure(self, report_dir: str) -> list:
        """On Android, dump `uiautomator dump` + `screencap` into `report_dir`
        so a failure report shows what screen the device was on. Call from
        Test Teardown guarded by `Run Keyword If Test Failed`. Best effort."""
        out_dir = Path(report_dir)
        written: list[str] = []
        if not isinstance(self.device.transport, ADBTransport):
            return written
        try:
            shell = AndroidShell(self.transport)
            dump = shell.ui_dump()
            if dump:
                target = out_dir / "ui_dump.xml"
                target.write_text(dump, encoding="utf-8")
                written.append(str(target))
                visible = sorted({m for m in re.findall(r'text="([^"]+)"', dump) if m})
                if visible:
                    logger.info("Visible texts at failure: " + ", ".join(repr(v) for v in visible))
            png = out_dir / "screen.png"
            shell.screenshot(str(png))
            if png.exists() and png.stat().st_size > 0:
                written.append(str(png))
        except Exception as e:
            logger.warn(f"UI state capture failed: {e}")
        return written

    # ─── internals ───────────────────────────────────────────────────────────

    def _variable(self, name: str, default: str = "") -> str:
        try:
            from robot.libraries.BuiltIn import BuiltIn

            return BuiltIn().get_variable_value("${" + name + "}", default)
        except Exception:
            return default

    def _suite_device_types(self) -> set[str]:
        raw = self._variable("DEVICE_TYPES", "")
        return {t.strip().upper() for t in raw.split(",") if t.strip()}

    def _resolve_device(self, device_id: str, device_types: set[str]) -> Device:
        if device_id:
            for d in self.project.devices:
                if d.id == device_id:
                    return d
            raise RuntimeError(f"No device '{device_id}' in project '{self.project.project}'")
        matching = [
            d for d in self.project.devices
            if not device_types or d.type.value in device_types
        ]
        if not matching:
            raise SkipExecution(
                f"No device in project '{self.project.project}' matches "
                f"device_types {device_types or '(any)'}"
            )
        return matching[0]
