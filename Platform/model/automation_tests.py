"""Real automation-test inventory — a thin parser over test-automation-sit's own .robot files.

Answers "how many tests exist, for what project/device/feature" honestly, from the actual
`*** Test Cases ***` sections and `Force Tags` lines in that repo — not a guess, not a
count of SIT keywords (that's a different axis entirely, see model/functions.py's
docstring: keywords are the technical "how", this is "what automated tests actually
exist"). George's ask, 2026-09-10: "how many tests have been written, and for what
functions" on the Automation console.

Deliberately excludes `POS-handover/raw-repo-export/` — a stale, superseded export copy
sitting alongside the real `projects/` tree, not the live test suite.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from pydantic import BaseModel, Field

_FORCE_TAGS = re.compile(r"^Force Tags\s+(.+)$", re.MULTILINE)
_TAG_TOKEN = re.compile(r"(project|device_types|feature):(\S+)")
_TEST_CASE_NAME = re.compile(r"^(\S[^\n]*)$", re.MULTILINE)
_PER_TEST_TAGS = re.compile(r"^\s*\[Tags\]\s+(.+)$", re.MULTILINE)


def _default_root() -> Path:
    override = os.environ.get("AUTOMATION_TESTS_ROOT")
    if override:
        return Path(override)
    # Sandbox layout: Platform/model/automation_tests.py -> repo root -> sibling checkout
    return Path(__file__).resolve().parent.parent.parent.parent / "test-automation-sit"


ROOT = _default_root()


class AutomationTestCase(BaseModel):
    name: str
    tags: list[str] = Field(default_factory=list)  # per-test [Tags], e.g. "destructive"


class AutomationSuite(BaseModel):
    """One .robot file — a suite of test cases sharing Force Tags."""

    source_file: str  # relative to test-automation-sit/
    project: str | None = None
    device_types: list[str] = Field(default_factory=list)
    feature: str | None = None
    cases: list[AutomationTestCase] = Field(default_factory=list)


def _parse_robot_file(path: Path, root: Path) -> AutomationSuite:
    text = path.read_text(encoding="utf-8")
    project = device_types = feature = None
    force_tags_match = _FORCE_TAGS.search(text)
    if force_tags_match:
        for key, value in _TAG_TOKEN.findall(force_tags_match.group(1)):
            if key == "project":
                project = value
            elif key == "device_types":
                device_types = (device_types or []) + [value]
            elif key == "feature":
                feature = value
    if project is None and device_types is None and feature is None:
        # No suite-level Force Tags -- some real suites (e.g.
        # projects/translink/tests/provisioning/*.robot) declare project/device_types/
        # feature per-test via [Tags] instead. Fall back to the first per-test tag line
        # found, on the assumption (checked true for the real suites this applies to)
        # that every test in the file shares the same project/device/feature even when
        # declared individually rather than once at suite level.
        for match in _PER_TEST_TAGS.finditer(text):
            for key, value in _TAG_TOKEN.findall(match.group(1)):
                if key == "project" and project is None:
                    project = value
                elif key == "device_types":
                    device_types = (device_types or []) + [value] if value not in (device_types or []) else device_types
                elif key == "feature" and feature is None:
                    feature = value
    if project is None:
        # Last resort: the real, documented layout convention itself --
        # projects/<name>/tests/... (CLAUDE.md: "projects/<name>/ -- project-specific
        # tests"). Only reached when the file's own tags never state a project anywhere
        # (e.g. test_etm_device_events.robot only tags `feature:smoke` on every test) --
        # reading the folder name it's actually filed under, not a guess at content.
        try:
            rel_parts = path.relative_to(root / "projects").parts
            if rel_parts and rel_parts[0] != "_common":
                project = rel_parts[0]
        except ValueError:
            pass

    cases: list[AutomationTestCase] = []
    if "*** Test Cases ***" in text:
        body = text.split("*** Test Cases ***", 1)[1]
        # Stop at the next section header, if any.
        for marker in ("*** Keywords ***", "*** Variables ***", "*** Settings ***"):
            if marker in body:
                body = body.split(marker, 1)[0]
        current_name = None
        current_tags: list[str] = []
        for line in body.splitlines():
            if not line.strip():
                continue
            if not line[0].isspace():
                if current_name:
                    cases.append(AutomationTestCase(name=current_name, tags=current_tags))
                current_name = line.strip()
                current_tags = []
            else:
                tag_match = _PER_TEST_TAGS.match(line.strip())
                if tag_match:
                    current_tags.extend(t.strip() for t in tag_match.group(1).split())
        if current_name:
            cases.append(AutomationTestCase(name=current_name, tags=current_tags))

    return AutomationSuite(
        source_file=str(path.relative_to(root)),
        project=project, device_types=device_types or [], feature=feature, cases=cases,
    )


def load_all_suites() -> list[AutomationSuite]:
    """Every real .robot suite under projects/ — not the stale POS-handover export."""
    projects_dir = ROOT / "projects"
    if not projects_dir.is_dir():
        return []
    return [
        _parse_robot_file(p, ROOT)
        for p in sorted(projects_dir.rglob("*.robot"))
    ]


def summarize(suites: list[AutomationSuite]) -> dict:
    """Real counts: total tests, by project, by device_type, by feature."""
    by_project: dict[str, int] = {}
    by_device: dict[str, int] = {}
    by_feature: dict[str, int] = {}
    total = 0
    for suite in suites:
        n = len(suite.cases)
        total += n
        if suite.project:
            by_project[suite.project] = by_project.get(suite.project, 0) + n
        for d in suite.device_types:
            by_device[d] = by_device.get(d, 0) + n
        if suite.feature:
            by_feature[suite.feature] = by_feature.get(suite.feature, 0) + n
    return {
        "total_tests": total, "total_suites": len(suites),
        "by_project": by_project, "by_device_type": by_device, "by_feature": by_feature,
    }
