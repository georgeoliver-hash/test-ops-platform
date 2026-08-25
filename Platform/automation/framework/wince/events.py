r"""Reader for the ETM's SRSService event store (`DeviceEvents.json`).

This is the WinCE analogue of the Android `EventLog` (framework/android/eventlog.py),
but the access model is different in two important ways:

1. **No shell.** The ETM's only transport is a Rebex SFTP file server (no
   `exec_command`), so we *pull the file* and parse it locally rather than
   running a `content query`. The query/filter API below operates on the
   parsed rows, so it works identically whether the rows came from a live
   pull or a cached `builds/etm/` snapshot.

2. **No monotonic row index.** `DeviceEvents.json` is a flat JSON array where
   each row's `Id` is an *event-type code* (102 = printer print started,
   1307 = power restore, 50001 = open-payment, …) drawn from the
   `EventsConfig.json::EnabledEvents` catalogue — NOT a per-row primary key.
   Multiple rows can share an `Id`. So "latest" and "since" baseline on
   `EventDate`, not on an index.

On the live device the active copy lives under the running version slot, e.g.
`\SD Memory\GFTS\V6\Code\SRSService\Data\DeviceEvents.json` (the GFTS log line
"Configuration Service running at '...\\V6\\Code\\SRSService'" names the slot).

Row shape (keys seen in the snapshot):
    Id, EventDate, ApplicationVersion, FirmwareVersion, EquipmentState,
    EventSense, EventSubType, Message, MessageLevel, EventComponentType,
    EventComponentNumber, JourneyId, GpsLocation, LocationId

`EventDate` is Microsoft JSON date format: `/Date(1780310162000)/` or with a
trailing timezone offset `/Date(1780310162000+0000)/` — milliseconds since the
Unix epoch.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from ..transport.base import Transport

# Cached-build snapshot defaults — the active version slot is V6 per the GFTS
# log ("Configuration Service running at '...\\V6\\Code\\SRSService'"). Offline
# build-verification tests read these without a live device.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRS_V6 = _REPO_ROOT / "builds" / "etm" / "GFTS" / "V6" / "Code" / "SRSService"
DEFAULT_EVENTS_FILE = _SRS_V6 / "Data" / "DeviceEvents.json"
DEFAULT_EVENTS_CONFIG = _SRS_V6 / "Configuration" / "EventsConfig.json"

# Microsoft JSON date: /Date(<ms>[<+/-hhmm>])/
_MS_DATE_RE = re.compile(r"/Date\((-?\d+)(?:([+-]\d{4}))?\)/")

# Column names as they appear in DeviceEvents.json.
COL_ID = "Id"
COL_EVENT_DATE = "EventDate"
COL_EQUIPMENT_STATE = "EquipmentState"
COL_EVENT_SENSE = "EventSense"
COL_COMPONENT_TYPE = "EventComponentType"
COL_MESSAGE = "Message"
COL_MESSAGE_LEVEL = "MessageLevel"
COL_JOURNEY_ID = "JourneyId"

# Default remote path on the device, parameterised by the active version slot.
def srs_data_path(version_slot: str = "V6", filename: str = "DeviceEvents.json") -> str:
    r"""Build the SD-card path to an SRSService data file for a version slot.

    e.g. srs_data_path("V6") -> '\SD Memory\GFTS\V6\Code\SRSService\Data\DeviceEvents.json'
    """
    return rf"\SD Memory\GFTS\{version_slot}\Code\SRSService\Data\{filename}"


def parse_ms_date(raw: str | None) -> datetime | None:
    """Parse a Microsoft JSON `/Date(ms)/` string into a UTC `datetime`.

    Returns None for null/empty/unparseable values. The optional `+hhmm`
    offset only labels the displayed zone; the millisecond value is already
    epoch-relative, so we anchor everything to UTC.
    """
    if not raw:
        return None
    m = _MS_DATE_RE.search(raw)
    if not m:
        return None
    try:
        ms = int(m.group(1))
    except ValueError:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)


def _as_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


class DeviceEventRow(dict):
    """One event from `DeviceEvents.json`. Behaves as a dict; typed accessors
    return None when a field is absent or unparseable."""

    @property
    def id(self) -> int | None:
        """Event-TYPE code (matches an entry in EventsConfig EnabledEvents)."""
        return _as_int(self.get(COL_ID))

    @property
    def event_date(self) -> datetime | None:
        return parse_ms_date(self.get(COL_EVENT_DATE))

    @property
    def equipment_state(self) -> str | None:
        return self.get(COL_EQUIPMENT_STATE)

    @property
    def event_sense(self) -> int | None:
        return _as_int(self.get(COL_EVENT_SENSE))

    @property
    def component_type(self) -> str | None:
        return self.get(COL_COMPONENT_TYPE)

    @property
    def message(self) -> str | None:
        return self.get(COL_MESSAGE)

    @property
    def message_level(self) -> str | None:
        return self.get(COL_MESSAGE_LEVEL)

    @property
    def journey_id(self) -> str | None:
        return self.get(COL_JOURNEY_ID)


class DeviceEvents:
    r"""A parsed `DeviceEvents.json`, with filter/lookup helpers.

    Construct from whichever source you have:
      * `DeviceEvents.from_transport(transport, remote_path)` — live device (SFTP pull)
      * `DeviceEvents.from_file(path)` — cached `builds/etm/` snapshot or a prior pull
      * `DeviceEvents.from_text(text)` — already-read JSON text
    """

    def __init__(self, rows: list[DeviceEventRow]):
        self.rows = rows

    # ─── constructors ────────────────────────────────────────────────────────

    @classmethod
    def from_text(cls, text: str) -> "DeviceEvents":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("DeviceEvents.json must be a JSON array")
        return cls([DeviceEventRow(r) for r in data if isinstance(r, dict)])

    @classmethod
    def from_file(cls, path: str | Path) -> "DeviceEvents":
        # utf-8-sig: these are Windows-authored files and some carry a BOM.
        return cls.from_text(Path(path).read_text(encoding="utf-8-sig"))

    @classmethod
    def from_transport(
        cls,
        transport: Transport,
        remote_path: str | None = None,
        *,
        version_slot: str = "V6",
        scratch_dir: str | Path | None = None,
    ) -> "DeviceEvents":
        """Pull `DeviceEvents.json` over SFTP and parse it.

        `remote_path` defaults to the active version slot's SRSService data dir.
        Uses `transport.pull` (file copy) — NOT `transport.run`, which the ETM
        SFTP-only server does not support.
        """
        remote = remote_path or srs_data_path(version_slot)
        import tempfile

        tmpdir = Path(scratch_dir) if scratch_dir else Path(tempfile.gettempdir())
        local = tmpdir / "DeviceEvents.json"
        transport.pull(remote, str(local))
        return cls.from_file(local)

    # ─── queries (operate on parsed rows) ─────────────────────────────────────

    def all(self) -> list[DeviceEventRow]:
        return list(self.rows)

    def by_id(self, event_id: int) -> list[DeviceEventRow]:
        return [r for r in self.rows if r.id == event_id]

    def by_component(self, component_type: str) -> list[DeviceEventRow]:
        return [r for r in self.rows if r.component_type == component_type]

    def latest(
        self,
        *,
        event_id: int | None = None,
        component_type: str | None = None,
    ) -> DeviceEventRow | None:
        """The most recent matching row by `EventDate`. Rows without a parseable
        date sort last (never chosen as latest unless they're the only match)."""
        rows = self.rows
        if event_id is not None:
            rows = [r for r in rows if r.id == event_id]
        if component_type is not None:
            rows = [r for r in rows if r.component_type == component_type]
        if not rows:
            return None
        return max(rows, key=lambda r: (r.event_date is not None, r.event_date or _MIN_DT))

    def since(self, after: datetime) -> list[DeviceEventRow]:
        """Rows whose EventDate is strictly after `after`, oldest first."""
        out = [r for r in self.rows if r.event_date and r.event_date > after]
        return sorted(out, key=lambda r: r.event_date)  # type: ignore[arg-type,return-value]

    def event_ids(self) -> set[int]:
        """Distinct event-type codes present in the store."""
        return {r.id for r in self.rows if r.id is not None}

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[DeviceEventRow]:
        return iter(self.rows)


_MIN_DT = datetime.min.replace(tzinfo=timezone.utc)


def load_enabled_events(path: str | Path) -> set[int]:
    """Return the `EnabledEvents` catalogue from an `EventsConfig.json`.

    This is the set of event-type codes the SRSService is configured to emit;
    a row in DeviceEvents whose `Id` is not in this set signals config/build
    drift between the events store and its configuration.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    enabled = data.get("EnabledEvents", []) if isinstance(data, dict) else []
    return {int(x) for x in enabled}
