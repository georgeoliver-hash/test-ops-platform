"""Regression tests for model/pipelines.py against the REAL .claude/pipelines/*.yaml.

The sandbox's own Platform/testops/ copy is stale (frozen June, predates the pipelines/ split)
so these point TESTOPS_CLAUDE_ROOT at the live system-test-ops checkout via a fixture — the
same "point at a real checkout" pattern sync_sit_mirror.py uses for sit-mirror/.

No module reload needed: pipelines.py resolves its root fresh on every call rather than
caching it at import time, specifically so one test file's env var doesn't leak into another
caller sharing the cached module (see _default_root()'s docstring for the bug this replaced).
"""
from __future__ import annotations

from pathlib import Path

import pytest

LIVE_CLAUDE_ROOT = (
    Path(__file__).resolve().parent.parent.parent.parent / "system-test-ops" / ".claude"
)


@pytest.fixture()
def pipelines(monkeypatch):
    if not LIVE_CLAUDE_ROOT.is_dir():
        pytest.skip(f"live system-test-ops checkout not found at {LIVE_CLAUDE_ROOT}")
    monkeypatch.setenv("TESTOPS_CLAUDE_ROOT", str(LIVE_CLAUDE_ROOT))
    from model import pipelines as mod

    yield mod


def test_index_lists_all_fourteen_pipelines(pipelines):
    index = pipelines.load_pipeline_index()
    ids = {e.id for e in index}
    assert "onboard-suite" in ids
    assert "audit-flows" in ids
    assert "resolve-gaps" in ids
    assert len(ids) == 14


def test_route_by_ui_action_matches_slash_command(pipelines):
    p = pipelines.route("audit_coverage")
    assert p.id == "audit-coverage"
    assert p.trigger.slash_command == "/audit-coverage"


def test_unknown_ui_action_raises_with_known_actions_listed(pipelines):
    with pytest.raises(KeyError, match="Known actions"):
        pipelines.route("does_not_exist")


def test_onboard_suite_has_expected_step_kinds_and_agent_fanout(pipelines):
    p = pipelines.load_pipeline("onboard-suite")
    kinds = {s.id: s.kind.value for s in p.steps}
    assert kinds["author_area"] == "agent"
    assert kinds["push_area"] == "cli"
    assert kinds["definition_of_done"] == "gate"
    author_step = next(s for s in p.steps if s.id == "author_area")
    assert author_step.loop == "one per functional area"


def test_audit_flows_triage_step_keeps_its_routing_table_via_extra_allow(pipelines):
    p = pipelines.load_pipeline("audit-flows")
    triage = next(s for s in p.steps if s.id == "triage")
    # routing_table isn't a typed field on Step — extra="allow" must still preserve it.
    assert "missing" in triage.model_extra["routing_table"]
    assert triage.model_extra["routing_table"]["missing"]["action"] == "ADD"


def test_shared_guardrails_load_and_all_references_resolve(pipelines):
    guardrails = pipelines.load_shared_guardrails()
    ids = {g.id for g in guardrails}
    assert "no_gap_fabrication" in ids
    problems = pipelines.validate_guardrail_references()
    assert problems == []


def test_ai_density_report_matches_known_onboard_suite_shape(pipelines):
    report = pipelines.ai_density_report()
    assert report["onboard-suite"]["agent"] == 5
    assert report["onboard-suite"]["cli"] == 5
    assert report["audit"]["cli"] == 1 and report["audit"]["agent"] == 1


def test_missing_root_raises_a_clear_error(monkeypatch):
    monkeypatch.setenv("TESTOPS_CLAUDE_ROOT", str(Path("/definitely/does/not/exist")))
    from model import pipelines as mod

    with pytest.raises(FileNotFoundError, match="stale"):
        mod.load_pipeline_index()
