"""Resolve symbolic resource names to UI text for `com.flowbird.pos`.

The POS app is Xamarin/Mono, so view-IDs are auto-generated and useless as
selectors — but string-resource names are stable across releases. Tests should
target UI by `POSStrings.lookup("Login.button_log_in")` instead of hardcoding
`"Log in"`, so a future label change only updates the metadata JSON.

The metadata file is produced by `tools/extract_apk_metadata.py` from
`com.flowbird.pos`'s APK and lives in `artifacts/pos_apk_metadata.json`.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from functools import cache
from pathlib import Path

_DEFAULT_METADATA_PATH = (
    Path(__file__).resolve().parents[2] / "artifacts" / "pos_apk_metadata.json"
)


class StringNotFound(KeyError):
    """Raised when a lookup name has no entry in the metadata."""


class POSStrings:
    def __init__(self, metadata_path: Path | None = None):
        path = metadata_path or _DEFAULT_METADATA_PATH
        if not path.is_file():
            raise FileNotFoundError(
                f"POS metadata not found at {path}. Run "
                "`python tools/extract_apk_metadata.py <apk> -o artifacts/pos_apk_metadata.json`."
            )
        data = json.loads(path.read_text(encoding="utf-8"))
        self._by_name: dict[str, str] = {s["name"]: s["value"] for s in data["strings"]}
        self.package: str = data["package"]
        self.version_name: str = data["version_name"]

    def lookup(self, name: str) -> str:
        try:
            return self._by_name[name]
        except KeyError as e:
            raise StringNotFound(name) from e

    def get(self, name: str, default: str | None = None) -> str | None:
        return self._by_name.get(name, default)

    def find(self, *, name_contains: str = "", value_contains: str = "") -> list[tuple[str, str]]:
        nc = name_contains.lower()
        vc = value_contains.lower()
        results: list[tuple[str, str]] = []
        for n, v in self._by_name.items():
            if nc and nc not in n.lower():
                continue
            if vc and vc not in v.lower():
                continue
            results.append((n, v))
        results.sort()
        return results

    def names(self) -> Iterable[str]:
        return self._by_name.keys()

    def __len__(self) -> int:
        return len(self._by_name)

    def __contains__(self, name: object) -> bool:
        return name in self._by_name


@cache
def default() -> POSStrings:
    return POSStrings()
