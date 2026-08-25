"""Reader for the device's Configuration content provider (com.parkeon.data.configuration).

The Flowbird platform exposes a path-based key/value config tree via an
Android ContentProvider. Sample paths (from artifacts/common.xml in the build):

    /system/debug/mode                         e.g. "INTEGRATION"
    /system/time/timezone                      e.g. "Europe/London"
    /system/network/modem/enable               "0" / "1"
    /system/network/modem/sim/apn              e.g. "everywhere"
    /pknUsbPrinter/printing/speed              e.g. "90"

URI format is not yet confirmed — the provider may key on URI path segments OR
on a `path=` query argument. `get()` tries both; `first_connect.py` records
which format succeeded so we can simplify once known.
"""
from __future__ import annotations

import re

from ..transport.base import Transport

AUTHORITY = "com.parkeon.data.configuration"


class Configuration:
    def __init__(self, transport: Transport):
        self.t = transport

    # ─── reads ──────────────────────────────────────────────────────────────

    def get(self, path: str) -> str | None:
        """Return the string value at `path`, or None if not found.

        Tries URI-segment style first, then falls back to ?path= query style.
        """
        for uri in self._candidate_uris(path):
            value = self._query_one(uri)
            if value is not None:
                return value
        return None

    def get_raw(self, path: str) -> dict[str, str]:
        """Return raw probe results keyed by URI tried — useful for first-connect."""
        out: dict[str, str] = {}
        for uri in self._candidate_uris(path):
            r = self.t.run(f'content query --uri "{uri}"')
            out[uri] = (r.stdout if r.ok else r.stderr).strip()
        return out

    # ─── writes (best-effort, may need root) ────────────────────────────────

    def set(self, path: str, value: str) -> bool:
        """Set `path` to `value`. Returns True if the command exited OK; does
        NOT verify the write took effect (call `get()` afterwards to confirm).
        """
        uri = f"content://{AUTHORITY}{path}"
        cmd = (
            f'content update --uri "{uri}" '
            f'--bind value:s:"{value}"'
        )
        r = self.t.run(cmd)
        return r.ok

    # ─── internals ──────────────────────────────────────────────────────────

    def _candidate_uris(self, path: str) -> list[str]:
        path = path if path.startswith("/") else f"/{path}"
        return [
            f"content://{AUTHORITY}{path}",          # /system/foo as URI segments
            f"content://{AUTHORITY}/?path={path}",   # path as query arg
        ]

    def _query_one(self, uri: str) -> str | None:
        r = self.t.run(f'content query --uri "{uri}"')
        if not r.ok or not r.stdout.strip():
            return None
        for line in r.stdout.splitlines():
            m = re.search(r"\bvalue=([^,]+)$", line.strip())
            if m:
                v = m.group(1).strip()
                return None if v == "NULL" else v
        return None
