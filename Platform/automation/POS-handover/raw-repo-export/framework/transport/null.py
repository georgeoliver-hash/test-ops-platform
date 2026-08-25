from __future__ import annotations

from ..registry.models import NullTransport as NullConfig
from .base import CommandResult, Transport


class NullTransportImpl(Transport):
    """No shell target: back-office web portals with no physical device behind
    them (BOS/ABT/CloudFare/Merit). `connect`/`disconnect` are no-ops — there's
    no host to reach at the transport layer, only a URL the UI driver navigates
    to. `run`/`push`/`pull` raise: a portal has no shell or filesystem to touch.
    """

    def __init__(self, config: NullConfig):
        self.config = config

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def run(self, command: str, timeout: float = 30.0) -> CommandResult:
        raise NotImplementedError("no shell transport for a web-portal device")

    def push(self, local: str, remote: str) -> None:
        raise NotImplementedError("no shell transport for a web-portal device")

    def pull(self, remote: str, local: str) -> None:
        raise NotImplementedError("no shell transport for a web-portal device")
