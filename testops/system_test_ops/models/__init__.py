"""Pydantic data models shared across the deterministic core.

These are the contract between the CLI (which produces them as JSON) and the
agents (which consume the JSON). Keep them project-agnostic.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# TestRail-side inventory
# --------------------------------------------------------------------------- #
class CaseRef(BaseModel):
    """A single TestRail test case (the unit the suite is made of)."""

    case_id: int
    title: str
    section_id: int | None = None
    section_path: str | None = None
    refs: list[str] = Field(default_factory=list)  # JIRA keys linked in the case's Refs field
    priority_id: int | None = None
    type_id: int | None = None
    template_id: int | None = None
    custom_steps: str | None = None  # raw Gherkin / steps body if present
    updated_on: datetime | None = None

    @property
    def cite(self) -> str:
        return f"C{self.case_id}"


# --------------------------------------------------------------------------- #
# Run history
# --------------------------------------------------------------------------- #
class RunResult(BaseModel):
    """One case's outcome within one TestRail run."""

    run_id: int
    run_name: str | None = None
    case_id: int
    status_id: int | None = None  # TestRail status (1=passed,2=blocked,3=untested,4=retest,5=failed,...)
    status_label: str | None = None
    executed_on: datetime | None = None


class TestHealth(BaseModel):
    """Aggregated health for one case across the last N runs."""

    case_id: int
    title: str | None = None
    runs_considered: int = 0
    executed_count: int = 0
    passed: int = 0
    failed: int = 0
    blocked: int = 0
    other: int = 0
    last_status_label: str | None = None
    last_executed_on: datetime | None = None
    run_ids: list[int] = Field(default_factory=list)  # evidence

    # Deterministic flags (thresholds applied in runs/history.py)
    always_failing: bool = False
    never_executed: bool = False
    flaky: bool = False
    recently_regressed: bool = False
    orphaned: bool = False  # not present in any of the last N runs

    @property
    def cite(self) -> str:
        return f"C{self.case_id}"


class RunHealthReport(BaseModel):
    """The JSON baseline the run-historian agent consumes."""

    project: str
    suite: str
    suite_id: int | None = None
    last_n: int
    generated_at: datetime
    run_ids: list[int] = Field(default_factory=list)
    cases: list[TestHealth] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Coverage
# --------------------------------------------------------------------------- #
class ScopeItem(BaseModel):
    """One unit of release scope pulled from a JIRA fix version."""

    issue_key: str
    issue_type: str | None = None  # Story / Bug / Task ...
    summary: str = ""
    status: str | None = None


class CoverageStatus(str, Enum):
    covered = "covered"
    partial = "partial"
    missing = "missing"
    stale = "stale"


class CoverageItem(BaseModel):
    """A scope item paired with the cases that (might) cover it.

    The CLI fills issue_key + candidate_case_ids deterministically (by Refs
    match / keyword overlap). The coverage-analyst agent sets `status` and
    `rationale` — that's the judgment layer.
    """

    issue_key: str
    summary: str = ""
    issue_type: str | None = None
    candidate_case_ids: list[int] = Field(default_factory=list)
    status: CoverageStatus | None = None  # set by the agent
    rationale: str | None = None  # set by the agent


class CasesBaseline(BaseModel):
    """The JSON baseline the coverage-analyst agent consumes (cases.json)."""

    project: str
    suite: str | None = None
    suite_id: int | None = None
    generated_at: datetime
    cases: list[CaseRef] = Field(default_factory=list)
