"""Function-keyword vocabulary — parsed from SIT's Bindings/*.robot files.

Deliberately NOT a full Robot Framework parser — SIT's Bindings files are always
`*** Settings ***` followed by one `*** Keywords ***` section, one keyword phrase per
zero-indent line, everything else (docs, args, body) indented under it. This reads exactly
that shape and nothing more; anything odd it can't confidently parse is skipped, not guessed.

Root resolution mirrors devices.py — SIT_SCHEMA_ROOT env var, else the sandbox's sit-mirror/,
else (post-merge) the sibling Resources/Devices/ tree directly. See devices.py's docstring.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from pydantic import BaseModel


def _default_root() -> Path:
    override = os.environ.get("SIT_SCHEMA_ROOT")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent.parent / "sit-mirror"


MIRROR_ROOT = _default_root() / "Bindings"

_KEYWORDS_HEADER = re.compile(r"^\*+\s*keywords\s*\*+$", re.IGNORECASE)
_SECTION_HEADER = re.compile(r"^\*+.*\*+$")
_EMBEDDED_ARG = re.compile(r"\$\{[^}]+\}")


class FunctionKeyword(BaseModel):
    """One Given/When/Then phrase bound to a real Robot Framework keyword body."""

    phrase: str  # e.g. "the device software has been started", or with embedded args:
    #                    "an available pos ${role}"
    normalised_key: str  # phrase with ${...} args replaced by a placeholder, for matching
    device_family: str  # e.g. "POS", "ETM", "Common", "Validators", "Axio", "Nexio", "NexioAxio"
    source_file: str  # relative path under sit-mirror/, for provenance


def _normalise(phrase: str) -> str:
    return _EMBEDDED_ARG.sub("<arg>", phrase).strip().lower()


def _parse_file(path: Path, device_family: str, mirror_root: Path) -> list[FunctionKeyword]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    keywords: list[FunctionKeyword] = []
    in_keywords_section = False
    for raw_line in lines:
        stripped = raw_line.strip()
        if _KEYWORDS_HEADER.match(stripped):
            in_keywords_section = True
            continue
        if not in_keywords_section:
            continue
        if _SECTION_HEADER.match(stripped) and not _KEYWORDS_HEADER.match(stripped):
            break  # left the Keywords section (e.g. a trailing *** Comments *** block)
        if not stripped:
            continue
        is_unindented = raw_line == raw_line.lstrip()
        if is_unindented and not stripped.startswith(("#", "[", "...")):
            keywords.append(
                FunctionKeyword(
                    phrase=stripped,
                    normalised_key=_normalise(stripped),
                    device_family=device_family,
                    source_file=str(path.relative_to(mirror_root.parent)),
                )
            )
    return keywords


def load_all_keywords() -> list[FunctionKeyword]:
    """Every function keyword across every mirrored device family's Bindings/*.robot files."""
    if not MIRROR_ROOT.is_dir():
        return []
    all_keywords: list[FunctionKeyword] = []
    for robot_file in sorted(MIRROR_ROOT.glob("*/Bindings/*.robot")):
        device_family = robot_file.parent.parent.name
        all_keywords.extend(_parse_file(robot_file, device_family, MIRROR_ROOT))
    return all_keywords


def find_keyword(phrase: str, keywords: list[FunctionKeyword] | None = None) -> FunctionKeyword | None:
    """Resolve a Gherkin step's phrase to an existing SIT keyword, if one already matches.

    Used by the (future) codegen step: a case step that resolves here can emit a real Robot
    Framework call instead of a `needs-keyword` stub.
    """
    keywords = keywords if keywords is not None else load_all_keywords()
    target = _normalise(phrase)
    return next((k for k in keywords if k.normalised_key == target), None)
