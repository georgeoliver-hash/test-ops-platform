from __future__ import annotations

import subprocess
import time

from ..registry.models import ADBTransport as ADBConfig
from .base import CommandResult, Transport


class ADBTransportImpl(Transport):
    """Thin wrapper around the `adb` CLI. Assumes adb is on PATH."""

    def __init__(self, config: ADBConfig):
        self.config = config
        self.serial = config.serial

    def connect(self) -> None:
        if ":" in self.serial:
            self._adb("connect", self.serial)
        state = self.get_state()
        if state != "device":
            raise ConnectionError(
                f"ADB device {self.serial} is in state {state!r} (need 'device'). "
                "If state is 'offline' the TCP listener may not be stock adbd."
            )

    def get_state(self) -> str:
        """Return adb's device state: 'device', 'offline', 'unauthorized', 'unknown'."""
        r = self._adb("-s", self.serial, "get-state", timeout=5)
        if r.ok and r.stdout.strip():
            return r.stdout.strip()
        # `get-state` exits 1 with "error: <state>" when not 'device'
        msg = (r.stderr or "").strip().lower()
        for state in ("offline", "unauthorized", "no device", "no such device"):
            if state in msg:
                return state.replace(" ", "_")
        return "unknown"

    def wait_until_device(
        self,
        *,
        timeout: float = 30.0,
        poll_interval: float = 1.0,
    ) -> str:
        """Poll until state becomes 'device' or `timeout` elapses.

        Re-issues `adb connect` for TCP serials on each poll because the way6
        terminal flips its TCP-5555 listener intermittently — a fresh connect
        is what nudges adbd to re-handshake once the window opens.

        Returns the final state. Does NOT raise — callers decide whether to skip
        or fail based on the result.
        """
        deadline = time.monotonic() + timeout
        state = self.get_state()
        while state != "device" and time.monotonic() < deadline:
            if ":" in self.serial:
                self._adb("connect", self.serial, timeout=5)
            time.sleep(poll_interval)
            state = self.get_state()
        return state

    def disconnect(self) -> None:
        if ":" in self.serial:
            self._adb("disconnect", self.serial)

    def run(self, command: str, timeout: float = 30.0) -> CommandResult:
        return self._adb("-s", self.serial, "shell", command, timeout=timeout)

    def push(self, local: str, remote: str) -> None:
        self._adb("-s", self.serial, "push", local, remote)

    def pull(self, remote: str, local: str) -> None:
        self._adb("-s", self.serial, "pull", remote, local)

    def _adb(self, *args: str, timeout: float = 30.0) -> CommandResult:
        try:
            proc = subprocess.run(
                ["adb", *args],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            return CommandResult(-1, "", f"timeout after {e.timeout}s: adb {' '.join(args)}")
        return CommandResult(proc.returncode, proc.stdout, proc.stderr)
