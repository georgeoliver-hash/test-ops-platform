from __future__ import annotations

from abc import ABC, abstractmethod


class UIDriver(ABC):
    """Abstract UI driver. Tests use high-level verbs only — never the
    underlying Appium/Playwright client directly.
    """

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def login(self, role: str, username: str, password: str) -> None: ...

    @abstractmethod
    def screenshot(self, path: str) -> None: ...

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.stop()
