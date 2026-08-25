"""High-level Android operations on top of an ADB Transport.

Tests use these wrappers instead of raw `transport.run("adb shell ...")` so that
intent stays readable and we can swap implementation (e.g. promote tap() to
UIAutomator/Appium) without rewriting tests.
"""
from __future__ import annotations

import re
from xml.etree import ElementTree as ET

from ..transport.base import Transport


class AndroidShell:
    def __init__(self, transport: Transport):
        self.t = transport

    # ─── inventory ──────────────────────────────────────────────────────────

    def getprop(self, name: str | None = None) -> str | dict[str, str]:
        if name:
            r = self.t.run(f"getprop {name}")
            return r.stdout.strip() if r.ok else ""
        r = self.t.run("getprop")
        if not r.ok:
            return {}
        props: dict[str, str] = {}
        for line in r.stdout.splitlines():
            m = re.match(r"\[([^]]+)\]:\s*\[(.*)\]", line)
            if m:
                props[m.group(1)] = m.group(2)
        return props

    def package_version(self, package: str) -> str | None:
        r = self.t.run(f"dumpsys package {package} | grep versionName")
        if not r.ok:
            return None
        m = re.search(r"versionName=(\S+)", r.stdout)
        return m.group(1) if m else None

    def is_package_installed(self, package: str) -> bool:
        r = self.t.run(f"pm list packages {package}")
        return r.ok and f"package:{package}" in r.stdout

    def is_process_running(self, name: str) -> bool:
        r = self.t.run(f"pidof {name}")
        if r.ok and r.stdout.strip():
            return True
        # `pidof` is missing on some stock Android builds; fall back to ps.
        r = self.t.run(f"ps -A 2>/dev/null | grep {name} | grep -v grep")
        if r.ok and r.stdout.strip():
            return True
        r = self.t.run(f"ps | grep {name} | grep -v grep")
        return r.ok and bool(r.stdout.strip())

    # ─── filesystem ─────────────────────────────────────────────────────────

    def list_dir(self, path: str) -> list[str]:
        r = self.t.run(f"ls -1 {path}")
        if not r.ok:
            return []
        return [line for line in r.stdout.splitlines() if line.strip()]

    def file_exists(self, path: str) -> bool:
        r = self.t.run(f"[ -e {path} ] && echo yes || echo no")
        return r.ok and "yes" in r.stdout

    def cat(self, path: str) -> str:
        r = self.t.run(f"cat {path}")
        return r.stdout if r.ok else ""

    # ─── UI driving (raw, no Appium) ────────────────────────────────────────

    def tap(self, x: int, y: int) -> None:
        self.t.run(f"input tap {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self.t.run(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

    def key(self, keycode: int | str) -> None:
        self.t.run(f"input keyevent {keycode}")

    def text(self, s: str) -> None:
        # `input text` doesn't handle spaces or special chars well; %s encodes spaces.
        self.t.run(f"input text '{s.replace(' ', '%s')}'")

    # `/data/local/tmp` is the universal-Android shell-writable scratch dir.
    # `/sdcard` is missing on some older builds (e.g. Android 5.1 on way6).
    _SCRATCH_DIR = "/data/local/tmp"

    def screenshot(self, local_path: str) -> None:
        remote = f"{self._SCRATCH_DIR}/__test_screencap.png"
        self.t.run(f"screencap -p {remote}")
        self.t.pull(remote, local_path)
        self.t.run(f"rm {remote}")

    def ui_dump(self) -> str:
        remote = f"{self._SCRATCH_DIR}/__test_ui_dump.xml"
        self.t.run(f"uiautomator dump {remote}")
        r = self.t.run(f"cat {remote}")
        self.t.run(f"rm {remote}")
        return r.stdout if r.ok else ""

    def find_by_text(self, text: str, *, exact: bool = True) -> tuple[int, int] | None:
        """Return the centre (x, y) of the first node whose @text matches, or None.

        Set `exact=False` for substring match. Reads a fresh `uiautomator dump`,
        so callers don't need to interleave dump calls themselves.
        """
        dump = self.ui_dump()
        if not dump:
            return None
        try:
            root = ET.fromstring(dump)
        except ET.ParseError:
            return None
        for node in root.iter("node"):
            node_text = node.get("text", "")
            if exact:
                if node_text != text:
                    continue
            else:
                if text not in node_text:
                    continue
            bounds = node.get("bounds", "")
            m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
            if not m:
                continue
            x1, y1, x2, y2 = (int(v) for v in m.groups())
            return ((x1 + x2) // 2, (y1 + y2) // 2)
        return None

    def tap_text(self, text: str, *, exact: bool = True) -> bool:
        """Tap the centre of the first node whose @text matches. Returns whether a tap was issued."""
        centre = self.find_by_text(text, exact=exact)
        if centre is None:
            return False
        self.tap(*centre)
        return True

    # ─── app control ────────────────────────────────────────────────────────

    def start_activity(self, component: str) -> None:
        """`component` may be 'package/.Activity' or just 'package' (uses LAUNCHER intent)."""
        if "/" in component:
            self.t.run(f"am start -n {component}")
        else:
            self.t.run(f"monkey -p {component} -c android.intent.category.LAUNCHER 1")

    def force_stop(self, package: str) -> None:
        self.t.run(f"am force-stop {package}")

    def current_activity(self) -> str | None:
        r = self.t.run("dumpsys activity activities | grep mResumedActivity")
        if not r.ok:
            return None
        m = re.search(r"\b([\w.]+/[\w.$]+)\b", r.stdout)
        return m.group(1) if m else None
