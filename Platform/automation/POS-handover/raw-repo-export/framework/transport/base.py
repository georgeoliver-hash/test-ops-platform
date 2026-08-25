from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


class Transport(ABC):
    """Abstract device transport. Implementations: SSHTransportImpl, ADBTransportImpl."""

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def run(self, command: str, timeout: float = 30.0) -> CommandResult: ...

    @abstractmethod
    def push(self, local: str, remote: str) -> None: ...

    @abstractmethod
    def pull(self, remote: str, local: str) -> None: ...

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.disconnect()
