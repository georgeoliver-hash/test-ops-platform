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


def test_index_lists_all_seventeen_pipelines(pipelines):
    index = pipelines.load_pipeline_index()
    ids = {e.id for e in index}
    assert "onboard-suite" in ids
    assert "audit-flows" in ids
    assert "resolve-gaps" in ids
    assert "write-automation" in ids  # 2026-09-14: new NJT automation-authoring pipeline
    # 2026-09-22: consolidation_sanity_check/traceability_check split out of maintain.yaml
    # into their own standalone, independently-runnable pipelines (George: "what if people
    # wanna do a smaller AI-effective pipeline of checking a different health check?").
    assert "consolidation-check" in ids
    assert "traceability-check" in ids
    # 2026-09-22: write automation straight from docs/JIRA (partial or either one) before
    # any TestRail suite exists -- George: "it might not always be a full doc, jira or
    # story... we want some automation done" at project start.
    assert "draft-automation" in ids
    # 2026-09-22: periodic, read-only doc-change watcher that only ever suggests a next
    # pipeline -- never applies anything itself. George: "does our tool need to
    # automatically read the docs, check our suites... and make these changes" -- answer
    # was suggest, never auto-apply, same human-gate rule every write pipeline follows.
    assert "scheduled-scan" in ids
    # 2026-09-22: select functional area(s) via checkbox (real TestRail sections, per
    # @feature's own mapping in docs/gherkin-standard.md) and create a TestRail run
    # scoped to just those cases -- George: "select EMV, no sign on stuff, run just that."
    assert "targeted-run" in ids
    # 2026-09-25: scoped re-judge of automation tier when the judging RULES change (new
    # automation capability, fresh doc, SIT config update) rather than when new cases simply
    # appear (--missing-only, already covered by the enrich step inside export-automation).
    # Built the same day ObvMessageInjector.py (test-automation-sit) made OBV message-injection
    # testing real, which needed the 2026-09-17 blanket "OBV -> No" cap narrowed -- and the ~97
    # already-enriched OBV cases needed exactly this kind of scoped refresh to pick it up.
    assert "refresh-automation-tier" in ids
    # 2026-09-28: doc-scoped companion to add-feature (which is JIRA/feature-scoped) --
    # cross-examine already-ingested document(s) against an EXISTING suite's live cases and
    # draft build/add/edit updates for review, without a full onboard-suite rebuild. George:
    # "ingest one doc (or multiple) then build, add, edit, resolve... to existing test suite."
    assert "update-suite-from-docs" in ids
    # 2026-09-28: George, "no one will ever know what the question actually is... write it
    # out in plain english... an AI summarize [pass]" -- rewrites GAP/UNCONFIRMED markers
    # into plain English, never answers them (that's still /resolve-gaps' job).
    assert "clarify-gaps" in ids
    # 2026-09-28: real groundwork only -- George is supplying the real template/example
    # report(s) separately; the drafting step's own note says so explicitly rather than
    # inventing a layout in the meantime.
    assert "generate-test-run-report" in ids
    # 2026-10-01: sorts every open gap by what would close it (screen comparison / behaviour run /
    # spec contradiction / exact value / other device), and writes one sheet per group.
    assert "group-gaps" in ids
    # 2026-10-02: links each known defect to the cases that would fail because of it (and lists the
    # defects no test would catch), from local files only -- no TestRail needed.
    assert "link-defects" in ids
    assert "judge-failures" in ids  # 2026-10-08: P1-P5 severity judging of sit failures
    assert len(ids) == 27


def test_clarify_gaps_only_rewords_never_answers(pipelines):
    p = pipelines.load_pipeline("clarify-gaps")
    kinds = {s.id: s.kind.value for s in p.steps}
    assert kinds["collect_markers"] == "cli"
    assert kinds["rewrite_plain_english"] == "agent"
    assert p.trigger.slash_command == "/clarify-gaps"
    rewrite = next(s for s in p.steps if s.id == "rewrite_plain_english")
    assert rewrite.rule == "no_gap_fabrication"
    input_names = {i.name for i in p.inputs}
    assert {"project", "device", "scope"} <= input_names


def test_update_suite_from_docs_is_doc_scoped_and_stops_for_human_review_before_push(pipelines):
    p = pipelines.load_pipeline("update-suite-from-docs")
    kinds = {s.id: s.kind.value for s in p.steps}
    assert kinds["cross_examine"] == "agent"
    assert kinds["human_review"] == "human"
    assert kinds["author_and_push"] == "cli"
    assert kinds["definition_of_done"] == "gate"
    # human_review must come before the push, not after -- this pipeline drafts + stops for
    # review, it never auto-pushes (unlike onboard-suite's per-area loop).
    step_ids = [s.id for s in p.steps]
    assert step_ids.index("human_review") < step_ids.index("author_and_push")
    input_names = {i.name for i in p.inputs}
    assert {"project", "device", "suite_id", "knowledge_files"} <= input_names
    cross_examine = next(s for s in p.steps if s.id == "cross_examine")
    assert "{knowledge_files}" in cross_examine.reads


def test_consolidate_execute_folds_references_a_real_produced_file_not_a_placeholder(pipelines):
    """Found live, 2026-09-28 (George ran /consolidate for real on Translink/POS):
    `execute_folds` failed every time -- its command hardcoded the literal, never-
    substituted placeholder `<folded>.cases.yaml` as the push target, and no earlier step
    in this pipeline ever actually authored a real `.cases.yaml` from the confirmed fold
    groups (find_fold_groups only ever wrote the audit/proposal .md). Fixed: a real
    author_folds step (gherkin-author) now authors the staging file, and execute_folds
    pushes that same real path -- not a placeholder."""
    p = pipelines.load_pipeline("consolidate")
    step_ids = [s.id for s in p.steps]
    assert "author_folds" in step_ids
    assert step_ids.index("confirm_aggressiveness") < step_ids.index("author_folds") < step_ids.index("execute_folds")
    author_folds = next(s for s in p.steps if s.id == "author_folds")
    execute_folds = next(s for s in p.steps if s.id == "execute_folds")
    assert "<folded>" not in execute_folds.command
    assert author_folds.produces in execute_folds.command
    # Also fixed alongside: find_fold_groups' own produces path was missing the real
    # {project}- prefix every other pipeline's proposals/ path uses (onboard-suite,
    # add-feature, ...) -- it would have written to proposals/POS-suite-restructure/...
    # instead of proposals/Translink-POS-suite-restructure/..., exactly what the live run
    # actually did.
    find_fold_groups = next(s for s in p.steps if s.id == "find_fold_groups")
    assert find_fold_groups.produces.startswith("proposals/{project}-{device}-suite-restructure/")
    # author_folds now reads ONLY the proposals a person ticked (Review & decide writes approved-folds.json),
    # not the whole audit -- so nothing unticked can be authored.
    assert any('approved-folds.json' in r for r in author_folds.reads)


def test_fold_defect_regression_register_path_matches_real_naming_convention(pipelines):
    """Same missing-{project}-prefix bug as consolidate's find_fold_groups, found by the
    same sweep: proposals/{device}-suite-restructure/... instead of the real convention
    every other pipeline uses."""
    p = pipelines.load_pipeline("fold-defect")
    record_decision = next(s for s in p.steps if s.id == "record_decision")
    assert record_decision.produces.startswith("proposals/{project}-{device}-suite-restructure/")


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
    assert report["onboard-suite"]["cli"] == 7
    assert report["audit"]["cli"] == 1 and report["audit"]["agent"] == 1


def test_missing_root_raises_a_clear_error(monkeypatch):
    monkeypatch.setenv("TESTOPS_CLAUDE_ROOT", str(Path("/definitely/does/not/exist")))
    from model import pipelines as mod

    with pytest.raises(FileNotFoundError, match="stale"):
        mod.load_pipeline_index()


def test_group_gaps_classifies_and_never_answers(pipelines):
    """The device is evidence, not gospel: group-gaps sorts gaps by what closes them and records a
    verdict column for a person -- it must never resolve a gap or write a case."""
    p = pipelines.load_pipeline("group-gaps")
    ids = [s.id for s in p.steps]
    assert ids == ["collect_markers", "gap_inputs", "classify_gaps", "gap_sheet"]
    classify = next(s for s in p.steps if s.id == "classify_gaps")
    assert "never answer" in classify.note.lower()
    for cat in ("screen", "behaviour", "conflict", "value", "other-device", "unclear"):
        assert f'"{cat}"' in classify.note
    sheet = next(s for s in p.steps if s.id == "gap_sheet")
    assert "Mismatch" in sheet.note and "--commit" not in (sheet.command or "")


def test_link_defects_works_offline_and_writes_nothing_to_testrail(pipelines):
    p = pipelines.load_pipeline("link-defects")
    assert [s.id for s in p.steps] == ["defect_inputs", "link_defects", "defect_report"]
    link = next(s for s in p.steps if s.id == "link_defects")
    assert "never" in link.note.lower() and "do not link" in link.note.lower() and "CANNOT RUN CODE" in link.note
    for s in p.steps:
        assert "--commit" not in (s.command or "") and "push" not in (s.command or "")
