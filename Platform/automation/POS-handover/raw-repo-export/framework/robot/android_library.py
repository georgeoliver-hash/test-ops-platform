"""Robot Framework Library: Android shell, navigation, EventLog, Configuration.

Replaces the pytest `android`, `eventlog`, `configuration`, `pos_strings`, and
`pos_nav` fixtures. TEST-scoped: a fresh `AndroidShell`/`Navigator`/`EventLog`/
`Configuration` is built per test from `DeviceLibrary`'s connected transport
(cheap — these are stateless wrappers over the transport, not connections in
their own right).
"""
from __future__ import annotations

from robot.api.deco import keyword, library
from robot.api.exceptions import SkipExecution
from robot.libraries.BuiltIn import BuiltIn

from framework.android.configuration import Configuration
from framework.android.eventlog import EventLog, EventLogRow
from framework.android.navigator import Navigator
from framework.android.shell import AndroidShell
from framework.android.strings import POSStrings, default as _pos_strings_default
from framework.registry.models import OS


@library(scope="TEST")
class AndroidLibrary:
    def __init__(self):
        self._device_lib = None
        self._shell: AndroidShell | None = None
        self._eventlog: EventLog | None = None
        self._configuration: Configuration | None = None
        self._nav: Navigator | None = None
        self._pos_strings: POSStrings | None = None

    # ─── wiring ──────────────────────────────────────────────────────────────

    @property
    def device_lib(self):
        if self._device_lib is None:
            self._device_lib = BuiltIn().get_library_instance("DeviceLibrary")
        return self._device_lib

    def _require_android(self):
        device = self.device_lib.device
        if device.os != OS.ANDROID:
            raise SkipExecution(f"Device {device.id} is not Android; skipping Android-only test")
        return device

    @property
    def shell(self) -> AndroidShell:
        self._require_android()
        if self._shell is None:
            self._shell = AndroidShell(self.device_lib.transport)
        return self._shell

    @property
    def eventlog(self) -> EventLog:
        self._require_android()
        if self._eventlog is None:
            self._eventlog = EventLog(self.device_lib.transport)
        return self._eventlog

    @property
    def configuration(self) -> Configuration:
        self._require_android()
        if self._configuration is None:
            self._configuration = Configuration(self.device_lib.transport)
        return self._configuration

    @property
    def pos_strings(self) -> POSStrings:
        if self._pos_strings is None:
            try:
                self._pos_strings = _pos_strings_default()
            except FileNotFoundError as e:
                raise SkipExecution(str(e)) from e
        return self._pos_strings

    @property
    def nav(self) -> Navigator:
        device = self._require_android()
        if device.appium_app_package != "com.flowbird.pos":
            raise SkipExecution(f"Device {device.id} is not running com.flowbird.pos")
        if self._nav is None:
            self._nav = Navigator(self.shell, self.pos_strings)
        return self._nav

    # ─── AndroidShell — low-level ────────────────────────────────────────────

    @keyword("Get Android Shell")
    def get_android_shell(self) -> AndroidShell:
        return self.shell

    @keyword("Get Event Log")
    def get_event_log(self) -> EventLog:
        return self.eventlog

    @keyword("Getprop")
    def getprop(self, name: str = ""):
        return self.shell.getprop(name or None)

    @keyword("Package Version")
    def package_version(self, package: str) -> str | None:
        return self.shell.package_version(package)

    @keyword("Is Package Installed")
    def is_package_installed(self, package: str) -> bool:
        return self.shell.is_package_installed(package)

    @keyword("Is Process Running")
    def is_process_running(self, name: str) -> bool:
        return self.shell.is_process_running(name)

    @keyword("File Exists On Device")
    def file_exists_on_device(self, path: str) -> bool:
        return self.shell.file_exists(path)

    @keyword("List Device Directory")
    def list_device_directory(self, path: str) -> list:
        return self.shell.list_dir(path)

    @keyword("Cat Device File")
    def cat_device_file(self, path: str) -> str:
        return self.shell.cat(path)

    @keyword("Tap")
    def tap(self, x: int, y: int) -> None:
        self.shell.tap(x, y)

    @keyword("Swipe")
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self.shell.swipe(x1, y1, x2, y2, duration_ms)

    @keyword("Send Key")
    def send_key(self, keycode) -> None:
        self.shell.key(keycode)

    @keyword("Input Text")
    def input_text(self, text: str) -> None:
        self.shell.text(text)

    @keyword("Take Screenshot")
    def take_screenshot(self, local_path: str) -> None:
        self.shell.screenshot(local_path)

    @keyword("Get UI Dump")
    def get_ui_dump(self) -> str:
        return self.shell.ui_dump()

    @keyword("Tap Text")
    def tap_text(self, text: str, exact: bool = True) -> bool:
        return self.shell.tap_text(text, exact=exact)

    @keyword("Start Activity")
    def start_activity(self, component: str) -> None:
        self.shell.start_activity(component)

    @keyword("Force Stop App")
    def force_stop_app(self, package: str) -> None:
        self.shell.force_stop(package)

    @keyword("Get Current Activity")
    def get_current_activity(self):
        return self.shell.current_activity()

    # ─── Navigator — POS-specific domain helpers ────────────────────────────

    @keyword("Visible Texts")
    def visible_texts(self) -> list:
        return sorted(self.nav.visible_texts())

    @keyword("Wait For Text")
    def wait_for_text(self, text: str, timeout: float = 10.0) -> bool:
        return self.nav.wait_for_text(text, timeout=timeout)

    @keyword("Wait For Any Text")
    def wait_for_any_text(self, *texts: str, timeout: float = 10.0):
        return self.nav.wait_for_any(*texts, timeout=timeout)

    @keyword("Wait For POS Ready")
    def wait_for_pos_ready(self, timeout: float = 30.0) -> bool:
        return self.nav.wait_for_ready(timeout=timeout)

    @keyword("Assert Visible Labels")
    def assert_visible_labels(self, *resources: str, screen: str = "screen") -> None:
        self.nav.assert_visible_labels(resources, screen=screen)

    @keyword("Go Back")
    def go_back(self) -> None:
        self.nav.go_back()

    @keyword("Press Menu Key")
    def press_menu_key(self) -> None:
        self.nav.menu()

    @keyword("Press Esc Key")
    def press_esc_key(self) -> None:
        self.nav.esc()

    @keyword("Press Clear Key")
    def press_clear_key(self) -> None:
        self.nav.clear()

    @keyword("Press Enter Key")
    def press_enter_key(self) -> None:
        self.nav.enter()

    @keyword("Press Up Key")
    def press_up_key(self) -> None:
        self.nav.up()

    @keyword("Press Down Key")
    def press_down_key(self) -> None:
        self.nav.down()

    @keyword("Press Left Key")
    def press_left_key(self) -> None:
        self.nav.left()

    @keyword("Press Right Key")
    def press_right_key(self) -> None:
        self.nav.right()

    @keyword("Press Digits")
    def press_digits(self, number: str) -> None:
        self.nav.press_digits(number)

    @keyword("Reset POS To Launcher")
    def reset_pos_to_launcher(self) -> None:
        self.nav.reset_to_launcher()

    @keyword("Is Signed On")
    def is_signed_on(self) -> bool:
        return self.nav.is_signed_on()

    @keyword("Is On Sign On Screen")
    def is_on_signon_screen(self) -> bool:
        return self.nav.is_on_signon_screen()

    @keyword("Ensure Signed Off")
    def ensure_signed_off(self) -> None:
        self.nav.ensure_signed_off()

    @keyword("Sign On")
    def sign_on(self, operator_id: str, pin: str, timeout: float = 15.0) -> bool:
        return self.nav.sign_on(operator_id, pin, timeout=timeout)

    @keyword("Sign Off")
    def sign_off(self) -> bool:
        return self.nav.sign_off()

    # ─── POSStrings ──────────────────────────────────────────────────────────

    @keyword("Lookup POS String")
    def lookup_pos_string(self, name: str) -> str:
        return self.pos_strings.lookup(name)

    @keyword("Get POS String")
    def get_pos_string(self, name: str, default: str = None):
        return self.pos_strings.get(name, default)

    # ─── Configuration ───────────────────────────────────────────────────────

    @keyword("Get Configuration Value")
    def get_configuration_value(self, path: str):
        return self.configuration.get(path)

    @keyword("Set Configuration Value")
    def set_configuration_value(self, path: str, value: str) -> bool:
        return self.configuration.set(path, value)

    # ─── EventLog ────────────────────────────────────────────────────────────

    @keyword("Latest Event Index")
    def latest_event_index(self, event_type: str):
        return self.eventlog.latest_index(event_type)

    @keyword("Events Since")
    def events_since(self, event_type: str, after_index: int) -> list:
        return self.eventlog.since(event_type, after_index)

    @keyword("Wait For Event")
    def wait_for_event(
        self,
        event_type: str,
        within_seconds: float = 30.0,
        baseline_index: int = None,
        require_payload: bool = False,
    ) -> EventLogRow:
        """Wait for a new `event_type` row. With `require_payload=True`, only
        rows carrying a non-empty JSON payload satisfy the wait — this is the
        RF equivalent of the ad-hoc `predicate=lambda r: bool(r.payload_json)`
        pytest tests used; arbitrary predicates aren't expressible from `.robot`
        syntax, so this flag covers the one concrete case the suite needs."""
        predicate = (lambda r: bool(r.payload_json)) if require_payload else (lambda _r: True)
        return self.eventlog.wait_for(
            event_type,
            predicate=predicate,
            within_seconds=within_seconds,
            baseline_index=baseline_index,
        )

    @keyword("List Event Types")
    def list_event_types(self) -> list:
        return self.eventlog.list_event_types()
