"""Reader for the device's EventLog content provider (com.parkeon.data.eventLog).

The Flowbird platform exposes every audit-worthy event via an Android
ContentProvider at `content://com.parkeon.data.eventLog/<type>[/<id>]`. Events
have a monotonic `eventIndex` and survive after BOS shipment, so this is the
preferred primitive for assertions — no outbox race like the BOSRecords ledger.

Schema (verified from `EventLogProvider.java` in `com.parkeon.systemstate` v37659):

    CREATE TABLE events (
      eventIndex INTEGER PRIMARY KEY AUTOINCREMENT,
      source     TEXT NOT NULL,
      eventType  TEXT NOT NULL,
      timestamp  INTEGER NOT NULL,
      message    TEXT NOT NULL DEFAULT '',
      payload    TEXT NOT NULL DEFAULT '{}'
    );

The provider is owned by the `EventLogProvider` class, observers go through
`EventLogObserver`, and the client-side constants live in
`com.parkeon.data.events.EventLogConstants`.

Wire-level access from a host: `adb shell content query --uri content://com.parkeon.data.eventLog/<type>`.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Callable

from ..transport.base import Transport

AUTHORITY = "com.parkeon.data.eventLog"

COL_EVENT_INDEX = "eventIndex"
COL_SOURCE = "source"
COL_EVENT_TYPE = "eventType"
COL_TIMESTAMP = "timestamp"
COL_MESSAGE = "message"
COL_PAYLOAD = "payload"

# Event types observed in the static analysis of `2_SystemState` and
# `1_2_ParkeonBspBase` dexes. Not exhaustive — the device emits more at runtime.
KNOWN_EVENT_TYPES: tuple[str, ...] = (
    "state.changed",
    "system.time.change",
    "system.startup.done",
    "alarms.changed",
    "resource.changed",
    "journal.configuration.changed",
    "journal.startup",
    "maintenance.labels.bug_report.collect.done",
    "maintenance.labels.bug_report.generate.done",
)


class EventLogRow(dict):
    """A row from `content query`. Behaves as a dict; typed accessors below
    return None when the column is absent (e.g. older platform builds)."""

    @property
    def event_index(self) -> int | None:
        return _as_int(self.get(COL_EVENT_INDEX))

    @property
    def source(self) -> str | None:
        return self.get(COL_SOURCE)

    @property
    def event_type(self) -> str | None:
        return self.get(COL_EVENT_TYPE)

    @property
    def timestamp(self) -> int | None:
        return _as_int(self.get(COL_TIMESTAMP))

    @property
    def message(self) -> str | None:
        return self.get(COL_MESSAGE)

    @property
    def payload_json(self) -> dict[str, Any] | None:
        raw = self.get(COL_PAYLOAD)
        if not raw or raw == "NULL":
            return None
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None


class EventLog:
    def __init__(self, transport: Transport):
        self.t = transport

    # ─── core query primitive ───────────────────────────────────────────────

    def query(
        self,
        event_type: str,
        *,
        where: str | None = None,
        sort: str | None = None,
    ) -> list[EventLogRow]:
        """Run `content query --uri content://.../<event_type>` and parse rows.

        `where` is passed verbatim to `--where` (e.g. `eventIndex>100`). `sort`
        to `--sort` (e.g. `eventIndex DESC LIMIT 10`).
        """
        uri = f"content://{AUTHORITY}/{event_type}"
        cmd = f'content query --uri {uri}'
        if where:
            cmd += f' --where "{where}"'
        if sort:
            cmd += f' --sort "{sort}"'
        r = self.t.run(cmd)
        if not r.ok:
            return []
        return _parse_content_query_rows(r.stdout)

    def latest(self, event_type: str, *, limit: int = 1) -> list[EventLogRow]:
        return self.query(event_type, sort=f"{COL_EVENT_INDEX} DESC LIMIT {limit}")

    def latest_index(self, event_type: str) -> int | None:
        rows = self.latest(event_type, limit=1)
        return rows[0].event_index if rows else None

    def since(self, event_type: str, after_index: int) -> list[EventLogRow]:
        return self.query(
            event_type,
            where=f"{COL_EVENT_INDEX}>{after_index}",
            sort=f"{COL_EVENT_INDEX} ASC",
        )

    # ─── waiters ────────────────────────────────────────────────────────────

    def wait_for(
        self,
        event_type: str,
        predicate: Callable[[EventLogRow], bool] = lambda _row: True,
        *,
        within_seconds: float = 30.0,
        poll_interval: float = 0.5,
        baseline_index: int | None = None,
    ) -> EventLogRow:
        """Wait for a new event of `event_type` matching `predicate`.

        If `baseline_index` is omitted, captures the current latest_index at
        start so only events that arrive *after* the wait begins are considered.
        """
        if baseline_index is None:
            baseline_index = self.latest_index(event_type) or 0
        deadline = time.monotonic() + within_seconds
        while time.monotonic() < deadline:
            rows = self.since(event_type, baseline_index)
            for row in rows:
                if predicate(row):
                    return row
                idx = row.event_index
                if idx is not None and idx > baseline_index:
                    baseline_index = idx
            time.sleep(poll_interval)
        raise AssertionError(
            f"No new {event_type!r} event matched predicate within {within_seconds}s "
            f"(baseline_index={baseline_index})"
        )

    def list_event_types(self) -> list[str]:
        """Best-effort enumeration via the recent logcat (no public API to list types).

        Reads logcat for EventLogProvider/EventLogObserver lines and harvests
        the event-type segment from URIs like
        `content://com.parkeon.data.eventLog/<type>/<id>`.
        """
        r = self.t.run("logcat -d -s JournalService.EventLogObserver:I -t 500")
        types: set[str] = set()
        for line in r.stdout.splitlines() if r.ok else []:
            m = re.search(rf"{re.escape(AUTHORITY)}/([\w.\-]+)/", line)
            if m:
                types.add(m.group(1))
        return sorted(types)


# ─── helpers ────────────────────────────────────────────────────────────────


_ROW_RE = re.compile(r"^Row:\s*\d+\s+(.*)$")


def _as_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _parse_content_query_rows(stdout: str) -> list[EventLogRow]:
    """Parse `adb shell content query` output.

    Format per row:
        Row: 0 eventIndex=1, source=foo, eventType=state.changed, ...
    """
    rows: list[EventLogRow] = []
    for line in stdout.splitlines():
        m = _ROW_RE.match(line.strip())
        if not m:
            continue
        rows.append(EventLogRow(_parse_row_body(m.group(1))))
    return rows


def _parse_row_body(body: str) -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for chunk in body.split(", "):
        if "=" not in chunk:
            continue
        key, _, value = chunk.partition("=")
        key = key.strip()
        value = value.strip()
        out[key] = None if value == "NULL" else value
    return out
