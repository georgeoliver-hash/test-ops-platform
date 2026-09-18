"""Regression tests for model/automation_tests.py against the real test-automation-sit checkout."""
from __future__ import annotations

from model.automation_tests import load_all_suites, summarize


def test_loads_real_suites():
    suites = load_all_suites()
    assert len(suites) > 0
    assert all(s.source_file for s in suites)


def test_excludes_stale_pos_handover_export():
    suites = load_all_suites()
    assert not any("POS-handover" in s.source_file for s in suites)


def test_translink_signon_suite_has_real_tags_and_cases():
    suites = load_all_suites()
    signon = next(s for s in suites if s.source_file.endswith("test_operator_signon.robot"))
    assert signon.project == "translink"
    assert "POS" in signon.device_types
    assert signon.feature == "auth"
    names = {c.name for c in signon.cases}
    assert "Signon Screen Shows Id And Pin Labels" in names
    destructive_case = next(c for c in signon.cases if c.name == "Invalid Signon Shows Failure Dialog")
    assert "destructive" in destructive_case.tags


def test_provisioning_suites_fall_back_to_per_test_or_path_tags():
    # Real gap found 2026-09-10: 3 translink provisioning suites declare project/device
    # per-test via [Tags] instead of suite-level Force Tags, and one of those (
    # test_etm_device_events.robot) never states a project anywhere at all -- only the
    # directory it's filed under (projects/translink/...) says so.
    suites = load_all_suites()
    by_name = {s.source_file.split("\\")[-1].split("/")[-1]: s for s in suites}
    assert by_name["test_dataset_parameters.robot"].project == "translink"
    assert by_name["test_etm_dm_parameters.robot"].project == "translink"
    assert by_name["test_etm_device_events.robot"].project == "translink"


def test_excludes_njt_reference_material_copied_from_sit():
    # Real bug found 2026-09-18: projects/njt/reference/ holds verbatim copies of sit's own
    # Farebox test files (grounding material, never move/delete from sit -- see that
    # folder's own README) -- these are sit's real tests, not ones written in this repo, so
    # counting them here inflated NJT's dashboard numbers by 16 phantom suites the day the
    # reference folder was expanded with more of them.
    suites = load_all_suites()
    assert not any("reference" in s.source_file.replace("\\", "/").split("/") for s in suites)


def test_summarize_totals_match_sum_of_suites():
    suites = load_all_suites()
    summary = summarize(suites)
    assert summary["total_tests"] == sum(len(s.cases) for s in suites)
    assert summary["total_suites"] == len(suites)
    assert sum(summary["by_project"].values()) == summary["total_tests"]
