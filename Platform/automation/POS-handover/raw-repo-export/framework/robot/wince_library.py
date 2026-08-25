"""Robot Framework Library: the WinCE ETM's DeviceEvents store + DM parameters.

Replaces the pytest `etm_events` and `etm_dm_parameters` fixtures.
"""
from __future__ import annotations

from pathlib import Path

from robot.api.deco import keyword, library
from robot.api.exceptions import SkipExecution
from robot.libraries.BuiltIn import BuiltIn

from framework.registry.models import OS
from framework.wince.dm_parameters import load_dm_parameters
from framework.wince.events import (
    DEFAULT_EVENTS_CONFIG,
    DEFAULT_EVENTS_FILE,
    DeviceEvents,
    load_enabled_events,
    parse_ms_date,
)


@library(scope="TEST")
class WinceLibrary:
    def __init__(self):
        self._device_lib = None
        self._events: DeviceEvents | None = None
        self._version_slot: str = "V6"

    @property
    def device_lib(self):
        if self._device_lib is None:
            self._device_lib = BuiltIn().get_library_instance("DeviceLibrary")
        return self._device_lib

    @property
    def events(self) -> DeviceEvents:
        device = self.device_lib.device
        if device.os != OS.WINCE:
            raise SkipExecution("DeviceEvents reader is only implemented for WinCE devices")
        if self._events is None:
            self._events = DeviceEvents.from_transport(
                self.device_lib.transport, version_slot=self._version_slot
            )
        return self._events

    @keyword("Get ETM DM Parameters")
    def get_etm_dm_parameters(self) -> dict:
        try:
            return load_dm_parameters()
        except FileNotFoundError as e:
            raise SkipExecution(str(e)) from e

    @keyword("Reload Device Events")
    def reload_device_events(self, version_slot: str = "") -> None:
        """Force a fresh SFTP pull of DeviceEvents.json (the cached property is
        per-test already, but a long test may want a mid-test refresh). Pass
        `version_slot` to switch the active GFTS version slot (default V6, or
        whatever a prior call set) before pulling."""
        if version_slot:
            self._version_slot = version_slot
        self._events = None
        _ = self.events

    @keyword("Get Device Events")
    def get_device_events(self) -> list:
        """All parsed rows from the current DeviceEvents.json snapshot."""
        return self.events.all()

    @keyword("Latest Device Event")
    def latest_device_event(self, event_id: int = None, component_type: str = None):
        return self.events.latest(event_id=event_id, component_type=component_type)

    @keyword("Device Events Since")
    def device_events_since(self, after) -> list:
        return self.events.since(after)

    @keyword("Device Events By Id")
    def device_events_by_id(self, event_id: int) -> list:
        return self.events.by_id(event_id)

    @keyword("Device Event Ids")
    def device_event_ids(self) -> list:
        return sorted(self.events.event_ids())

    # ─── offline / no-device (cached-snapshot) helpers ──────────────────────
    # These don't touch DeviceLibrary at all — for build-verification suites
    # that assert against a cached `builds/etm/` snapshot with no live device,
    # mirroring the pytest `snapshot_events`/module-scoped fixture tests that
    # never requested `device`/`transport`.

    @keyword("Load Device Events From File")
    def load_device_events_from_file(self, path: str) -> DeviceEvents:
        if not Path(path).exists():
            raise SkipExecution(f"cached DeviceEvents.json not found at {path}")
        return DeviceEvents.from_file(path)

    @keyword("Load Enabled Events From File")
    def load_enabled_events_from_file(self, path: str) -> set:
        if not Path(path).exists():
            raise SkipExecution(f"cached EventsConfig.json not found at {path}")
        return load_enabled_events(path)

    @keyword("Parse MS Date")
    def parse_ms_date_kw(self, raw):
        return parse_ms_date(raw)

    @keyword("Get Default ETM Events Snapshot Path")
    def get_default_etm_events_snapshot_path(self) -> str:
        return str(DEFAULT_EVENTS_FILE)

    @keyword("Get Default ETM Events Config Path")
    def get_default_etm_events_config_path(self) -> str:
        return str(DEFAULT_EVENTS_CONFIG)
