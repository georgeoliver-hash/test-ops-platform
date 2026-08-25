from __future__ import annotations

import time
from datetime import datetime, timezone

from .client import BOSClient


class AuditAssertion:
    def __init__(self, client: BOSClient):
        self.client = client

    def expect(
        self,
        *,
        event: str,
        device_id: str,
        within_seconds: float = 30.0,
        poll_interval: float = 1.0,
    ) -> dict:
        """Poll BOS until an audit event of the given kind appears for the device.

        Raises AssertionError on timeout.
        """
        deadline = time.monotonic() + within_seconds
        since = datetime.now(timezone.utc).isoformat()
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                events = self.client.get_audit_events(
                    device_id=device_id, event=event, since_iso=since
                )
                if events:
                    return events[0]
            except NotImplementedError:
                raise
            except Exception as e:
                last_error = e
            time.sleep(poll_interval)
        raise AssertionError(
            f"BOS did not record audit event '{event}' for device '{device_id}' "
            f"within {within_seconds}s. Last error: {last_error}"
        )
