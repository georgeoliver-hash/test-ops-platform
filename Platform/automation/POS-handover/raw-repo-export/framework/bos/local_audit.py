"""Reader for the on-device audit ledger (Audit/BOSRecords).

The Flowbird BOS agent persists every audit-worthy event locally as a numbered
`.evt` file before shipping it to BOS. **Outbox pattern**: on successful ship
the file is deleted, so files are ephemeral — `expect()` polls aggressively
to catch records before they're shipped.

For more reliable assertions against events that have already shipped, use
`framework.android.eventlog.EventLog` instead — it reads the device's
`content://com.parkeon.data.eventLog` content provider where events persist.

Confirmed format from a real device SD card:
- Path on device: `/sdcard/Android/data/com.flowbird.pos/files/Audit/BOSRecords/`
- Filename: `<8-digit-zero-padded-sequence>.evt` (e.g. `00000252.evt`)
- Content: UTF-8 text fragments — typically a snippet of logcat surrounding the
  event, including a reference to the EventLog event ID.
"""
from __future__ import annotations

import json
import time

from ..transport.base import Transport


class LocalAuditLedger:
    SEARCH_PATHS = [
        "/sdcard/Android/data/com.flowbird.pos/files/Audit/BOSRecords",
        "/storage/emulated/0/Android/data/com.flowbird.pos/files/Audit/BOSRecords",
        "/data/data/com.flowbird.pos/files/Audit/BOSRecords",
        "/data/local/tmp/Audit/BOSRecords",
    ]

    def __init__(self, transport: Transport, path: str | None = None):
        self.t = transport
        self.path = path

    def discover(self) -> str | None:
        for candidate in self.SEARCH_PATHS:
            r = self.t.run(f"[ -d {candidate} ] && echo {candidate}")
            if r.ok and candidate in r.stdout:
                self.path = candidate
                return candidate
        # Fallback: search filesystem (slow, only on first run with an unfamiliar device).
        r = self.t.run("find / -type d -name BOSRecords 2>/dev/null | head -5")
        if r.ok and r.stdout.strip():
            self.path = r.stdout.strip().splitlines()[0]
            return self.path
        return None

    def list_records(self) -> list[str]:
        if not self.path:
            raise RuntimeError("Path not set; call discover() first")
        r = self.t.run(f"ls -1 {self.path} 2>/dev/null")
        return [line for line in r.stdout.splitlines() if line.strip()] if r.ok else []

    def read_record(self, name: str) -> dict | None:
        if not self.path:
            raise RuntimeError("Path not set; call discover() first")
        r = self.t.run(f"cat {self.path}/{name}")
        if not r.ok:
            return None
        try:
            data = json.loads(r.stdout)
            data["_filename"] = name
            return data
        except json.JSONDecodeError:
            return {"_filename": name, "_raw": r.stdout}

    def newest_record(self) -> dict | None:
        if not self.path:
            raise RuntimeError("Path not set; call discover() first")
        r = self.t.run(f"ls -1t {self.path} 2>/dev/null | head -1")
        if not r.ok or not r.stdout.strip():
            return None
        return self.read_record(r.stdout.strip())

    def expect(
        self,
        *,
        event: str,
        within_seconds: float = 30.0,
        poll_interval: float = 0.2,
    ) -> dict:
        """Poll the ledger for a *new* record matching `event` (substring or JSON
        field match). Returns the matching record. Raises AssertionError on timeout.

        Polls aggressively (200 ms default) because the BOS agent ships records
        and deletes the file shortly after creation — sub-second windows.
        """
        if not self.path and not self.discover():
            raise AssertionError("Audit ledger path not found on device")

        before = set(self.list_records())
        deadline = time.monotonic() + within_seconds
        while time.monotonic() < deadline:
            now = set(self.list_records())
            for name in now - before:
                rec = self.read_record(name)
                if rec is None:
                    continue
                if rec.get("event") == event or event in rec.get("_raw", ""):
                    return rec
                if event in json.dumps(rec, default=str):
                    return rec
            time.sleep(poll_interval)
        raise AssertionError(
            f"No new audit record matching {event!r} appeared in {self.path} "
            f"within {within_seconds}s"
        )
