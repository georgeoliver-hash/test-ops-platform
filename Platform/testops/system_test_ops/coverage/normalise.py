"""Normalise raw TestRail case dicts into the CaseRef / CasesBaseline contract.

This produces `cases.json` — the deterministic inventory of a suite. The
coverage-analyst agent pairs these cases with JIRA fix-version scope (which it
pulls via the Atlassian MCP) and sets the covered/partial/missing/stale verdict.
We do NOT do the JIRA matching here because the CLI has no JIRA access.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from system_test_ops.models import CaseRef, CasesBaseline
from system_test_ops.testrail.client import TestRailClient

_JIRA_KEY = re.compile(r"[A-Z][A-Z0-9]+-\d+")


def _epoch_to_dt(val: object) -> datetime | None:
    if val in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(val), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _parse_refs(raw: object) -> list[str]:
    """TestRail 'refs' is a comma/space separated string of references."""
    if not raw:
        return []
    return sorted(set(_JIRA_KEY.findall(str(raw).upper())))


def _extract_steps(case: dict) -> str | None:
    """Best-effort pull of the case's Gherkin / steps body across templates."""
    if case.get("custom_steps"):
        return str(case["custom_steps"])
    separated = case.get("custom_steps_seperated") or case.get("custom_steps_separated")
    if isinstance(separated, list) and separated:
        parts = []
        for step in separated:
            content = (step or {}).get("content") if isinstance(step, dict) else None
            expected = (step or {}).get("expected") if isinstance(step, dict) else None
            if content:
                parts.append(content)
            if expected:
                parts.append(f"-> {expected}")
        if parts:
            return "\n".join(parts)
    # Some teams keep Gherkin in a custom field; surface the first that looks textual.
    for key, val in case.items():
        if key.startswith("custom_") and isinstance(val, str) and any(
            kw in val.lower() for kw in ("given", "when", "then")
        ):
            return val
    return None


def case_from_testrail(case: dict, section_paths: dict[int, str] | None = None) -> CaseRef:
    section_id = case.get("section_id")
    return CaseRef(
        case_id=int(case["id"]),
        title=case.get("title", ""),
        section_id=section_id,
        section_path=(section_paths or {}).get(section_id) if section_id else None,
        refs=_parse_refs(case.get("refs")),
        priority_id=case.get("priority_id"),
        type_id=case.get("type_id"),
        template_id=case.get("template_id"),
        custom_steps=_extract_steps(case),
        updated_on=_epoch_to_dt(case.get("updated_on")),
    )


def _section_path_map(sections: list[dict]) -> dict[int, str]:
    by_id = {int(s["id"]): s for s in sections}
    cache: dict[int, str] = {}

    def path(sid: int) -> str:
        if sid in cache:
            return cache[sid]
        s = by_id.get(sid)
        if not s:
            return ""
        parent = s.get("parent_id")
        prefix = path(int(parent)) + " / " if parent else ""
        cache[sid] = prefix + str(s.get("name", ""))
        return cache[sid]

    return {sid: path(sid) for sid in by_id}


def build_cases_baseline(
    client: TestRailClient,
    *,
    project: str,
    project_id: int,
    suite_id: int | None,
    suite_name: str | None,
) -> CasesBaseline:
    sections = client.get_sections(project_id, suite_id)
    section_paths = _section_path_map(sections)
    raw_cases = client.get_cases(project_id, suite_id)
    cases = [case_from_testrail(c, section_paths) for c in raw_cases]
    return CasesBaseline(
        project=project,
        suite=suite_name,
        suite_id=suite_id,
        generated_at=datetime.now(timezone.utc),
        cases=cases,
    )
