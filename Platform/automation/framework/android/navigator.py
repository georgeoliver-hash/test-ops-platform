"""High-level POS app navigation helper.

Most failing tests had TODO markers like "navigate to the basket-confirm screen
first". The POS app's Xamarin layouts set menu labels at runtime, so we can't
plan navigation purely from static analysis — we have to observe the screen and
react. `Navigator` wraps that pattern.

Scope is deliberately narrow: only the navigation primitives that more than one
test needs. Per-screen helpers grow as tests discover new flows.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from .shell import AndroidShell
from .strings import POSStrings

# ── Android keycodes for the way6 physical keypad (getevent-verified 2026-06-12) ──
# Soft keys — left column (L1 top → L5 bottom, aligned with screen labels)
KEYCODE_L1 = 131   # KEY_F1
KEYCODE_L2 = 132   # KEY_F2
KEYCODE_L3 = 133   # KEY_F3
KEYCODE_L4 = 134   # KEY_F4
KEYCODE_L5 = 135   # KEY_F5
# Soft keys — right column (R1 top → R5 bottom)
KEYCODE_R1 = 136   # KEY_F6
KEYCODE_R2 = 137   # KEY_F7
KEYCODE_R3 = 138   # KEY_F8
KEYCODE_R4 = 139   # KEY_F9
KEYCODE_R5 = 140   # KEY_F10
# Navigation cluster
KEYCODE_UP    = 19    # KEY_UP
KEYCODE_DOWN  = 20    # KEY_DOWN
KEYCODE_LEFT  = 21    # KEY_LEFT
KEYCODE_RIGHT = 22    # KEY_RIGHT
KEYCODE_ENTER = 66    # KEY_ENTER
KEYCODE_BACK  = 4
KEYCODE_HOME  = 3
KEYCODE_ESC   = 111   # KEY_ESC — C/Cancel on some screens
KEYCODE_MENU  = 142   # KEY_F12 — the menu/settings button
# Numeric keypad
KEYCODE_0 = 7
KEYCODE_1 = 8
KEYCODE_2 = 9
KEYCODE_3 = 10
KEYCODE_4 = 11
KEYCODE_5 = 12
KEYCODE_6 = 13
KEYCODE_7 = 14
KEYCODE_8 = 15
KEYCODE_9 = 16
KEYCODE_STAR  = 155   # KEY_KPASTERISK
KEYCODE_PLUS  = 157   # KEY_KPPLUS
KEYCODE_MINUS = 156   # KEY_KPMINUS
KEYCODE_CLEAR = 67    # KEY_BACKSPACE — the C/clear key

_DIGIT_KEYCODES = {str(d): 7 + d for d in range(10)}  # '0'→7 … '9'→16

POS_PACKAGE = "com.flowbird.pos"

# Strings that identify the "Present card / Press Any Key to Continue" idle
# prompt that sits between boot and the actual ID/PIN sign-on form. Any one of
# these texts being visible is enough to recognise the screen.
SIGNON_IDLE_MARKERS: tuple[str, ...] = (
    "Press Any Key to Continue",
    "Present card",
)

# Texts that indicate a transient loading state — navigation should not proceed
# until ALL of these have cleared from the screen.
LOADING_MARKERS: tuple[str, ...] = (
    "Please wait...",
    "Initialising...",
)


@dataclass(frozen=True)
class ScreenProbe:
    """Markers that identify a screen via its visible text. A screen is
    'recognised' when every marker text appears in the current `ui_dump`.
    Markers come from `POSStrings` lookups so the source-of-truth is the APK,
    not duplicated literals here."""

    name: str
    markers: tuple[str, ...]


class Navigator:
    """Driving the POS through screens.

    Use it via the `pos_nav` fixture; tests call `nav.sign_on()`, `nav.go_back()`,
    `nav.wait_for_text()` etc. instead of hand-rolling input + dump loops.
    """

    def __init__(self, android: AndroidShell, pos_strings: POSStrings):
        self.android = android
        self.strings = pos_strings

    # ─── primitives ─────────────────────────────────────────────────────────

    def visible_texts(self) -> set[str]:
        """Set of every non-empty `text` attribute on the current screen."""
        dump = self.android.ui_dump()
        if not dump:
            return set()
        import re
        return {m for m in re.findall(r'text="([^"]+)"', dump) if m}

    def wait_for_text(self, text: str, *, timeout: float = 10.0, poll: float = 0.5) -> bool:
        """Poll until `text` appears on screen, or timeout. Returns whether seen."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if text in self.visible_texts():
                return True
            time.sleep(poll)
        return False

    def wait_for_any(self, *texts: str, timeout: float = 10.0, poll: float = 0.5) -> str | None:
        """Poll until any of `texts` appears. Returns the matching one or None."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            seen = self.visible_texts()
            for t in texts:
                if t in seen:
                    return t
            time.sleep(poll)
        return None

    def is_loading(self) -> bool:
        """True if any loading/busy marker is currently visible."""
        seen = self.visible_texts()
        return any(marker in seen for marker in LOADING_MARKERS)

    def wait_for_ready(self, *, timeout: float = 30.0, poll: float = 0.5) -> bool:
        """Block until no loading markers are visible, or timeout.

        Use after any action that can trigger a 'Please wait...' screen — sign-on,
        basket confirm, mode changes, etc. Timeout is generous (30s default) because
        the POS can take a long time to fetch data from BOS on first load.
        Returns True if the screen cleared, False if timeout was reached.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.is_loading():
                return True
            time.sleep(poll)
        return False

    def screen_matches(self, probe: ScreenProbe) -> bool:
        seen = self.visible_texts()
        return all(m in seen for m in probe.markers)

    def assert_visible_labels(
        self, resources: tuple[str, ...] | list[str], *, screen: str = "screen"
    ) -> None:
        """Assert every `POSStrings` resource name resolves to a visible label.

        On failure the error lists both what was missing AND a snapshot of every
        text that WAS visible — so the report tells you which screen you ended
        up on, not just that you weren't on the expected one.
        """
        seen = self.visible_texts()
        missing: list[tuple[str, str]] = []
        for resource in resources:
            label = self.strings.lookup(resource)
            if label not in seen:
                missing.append((resource, label))
        if not missing:
            return
        sample = sorted(seen)[:30]
        raise AssertionError(
            f"{screen}: missing labels {missing!r}. "
            f"Visible texts on current screen ({len(seen)} total, first 30 sorted): {sample!r}"
        )

    def go_back(self) -> None:
        self.android.key(KEYCODE_BACK)

    # ─── physical keypad helpers ─────────────────────────────────────────────

    def l1(self) -> None: self.android.key(KEYCODE_L1)
    def l2(self) -> None: self.android.key(KEYCODE_L2)
    def l3(self) -> None: self.android.key(KEYCODE_L3)
    def l4(self) -> None: self.android.key(KEYCODE_L4)
    def l5(self) -> None: self.android.key(KEYCODE_L5)

    def r1(self) -> None: self.android.key(KEYCODE_R1)
    def r2(self) -> None: self.android.key(KEYCODE_R2)
    def r3(self) -> None: self.android.key(KEYCODE_R3)
    def r4(self) -> None: self.android.key(KEYCODE_R4)
    def r5(self) -> None: self.android.key(KEYCODE_R5)

    def up(self) -> None:    self.android.key(KEYCODE_UP)
    def down(self) -> None:  self.android.key(KEYCODE_DOWN)
    def left(self) -> None:  self.android.key(KEYCODE_LEFT)
    def right(self) -> None: self.android.key(KEYCODE_RIGHT)
    def enter(self) -> None: self.android.key(KEYCODE_ENTER)
    def esc(self) -> None:   self.android.key(KEYCODE_ESC)
    def menu(self) -> None:  self.android.key(KEYCODE_MENU)
    def clear(self) -> None: self.android.key(KEYCODE_CLEAR)

    def press_digits(self, number: str) -> None:
        """Press each character in `number` as individual keypad digit presses."""
        for ch in number:
            code = _DIGIT_KEYCODES.get(ch)
            if code is None:
                raise ValueError(f"press_digits: non-digit character {ch!r} in {number!r}")
            self.android.key(code)

    def reset_to_launcher(self) -> None:
        """Force-stop the POS app and restart it from the launcher activity.

        Useful when a test needs a known starting state. The app's launcher
        activity is `crc648b5ee79715524b27.MainActivity` (the Xamarin-mangled
        main activity); without a sign-on it lands on the sign-on screen.
        """
        self.android.force_stop(POS_PACKAGE)
        time.sleep(0.5)
        self.android.start_activity(POS_PACKAGE)

    # ─── sign-on / sign-off ────────────────────────────────────────────────

    def is_signed_on(self) -> bool:
        """A signed-on session has 'Sign Off' visible somewhere reachable."""
        try:
            sign_off_label = self.strings.lookup("SignOff.title")
        except KeyError:
            sign_off_label = "Sign Off"
        return sign_off_label in self.visible_texts()

    def is_on_signon_screen(self) -> bool:
        seen = self.visible_texts()
        try:
            id_label = self.strings.lookup("SignOn.id")
            pin_label = self.strings.lookup("SignOn.pin")
        except KeyError:
            return False
        return id_label in seen and pin_label in seen

    def is_on_signon_idle_prompt(self) -> bool:
        """True if we're on the 'Present card / Press Any Key to Continue'
        idle screen that precedes the ID/PIN form."""
        seen = self.visible_texts()
        return any(marker in seen for marker in SIGNON_IDLE_MARKERS)

    def dismiss_signon_idle_prompt(self, *, timeout: float = 10.0) -> bool:
        """Send ENTER to advance past the idle prompt to the ID/PIN form.
        Returns whether the ID/PIN form became visible within `timeout`."""
        self.android.key(KEYCODE_ENTER)
        self.wait_for_ready(timeout=timeout)
        try:
            id_label = self.strings.lookup("SignOn.id")
        except KeyError:
            return False
        return self.wait_for_text(id_label, timeout=timeout)

    def sign_on(self, operator_id: str, pin: str, *, timeout: float = 15.0) -> bool:
        """Enter operator credentials on the sign-on screen and tap Log in.

        Returns whether the InvalidLogin dialog did NOT appear within `timeout`.
        Caller is responsible for asserting whatever post-condition matters
        (e.g. landing on a specific menu, EventLog row).
        """
        id_label = self.strings.lookup("SignOn.id")
        pin_label = self.strings.lookup("SignOn.pin")
        login_label = self.strings.lookup("Login.button_log_in")

        if not self.android.tap_text(id_label):
            return False
        self.android.text(operator_id)
        self.android.key(KEYCODE_ENTER)
        self.android.text(pin)
        self.android.key(KEYCODE_ENTER)

        # Wait for any loading screen to clear before checking for success/failure.
        # Sign-on can trigger a "Please wait..." while fetching operator data from BOS.
        self.wait_for_ready(timeout=timeout)

        failure_label = self.strings.lookup("InvalidLogin.title")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            seen = self.visible_texts()
            if failure_label in seen:
                return False
            if id_label not in seen and pin_label not in seen:
                return True
            time.sleep(0.5)
        return True

    def sign_off(self) -> bool:
        """If 'Sign Off' is reachable, tap it. Returns whether tapped."""
        try:
            label = self.strings.lookup("SignOff.title")
        except KeyError:
            label = "Sign Off"
        return self.android.tap_text(label)

    def ensure_signed_off(self) -> None:
        """End any active session and return to the ID/PIN sign-on screen."""
        for _ in range(5):
            if self.is_on_signon_screen():
                return
            if self.is_on_signon_idle_prompt():
                if self.dismiss_signon_idle_prompt():
                    return
                continue
            if self.is_signed_on():
                self.sign_off()
                time.sleep(1.0)
                continue
            self.go_back()
            time.sleep(0.5)
        self.reset_to_launcher()
        if self.is_on_signon_idle_prompt():
            self.dismiss_signon_idle_prompt()
