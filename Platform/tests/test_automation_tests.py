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
    """`total_tests` is WRITTEN tests only -- `[Setup] Skip GAP` placeholders never enter
    the dataset (dropped in load_all_suites), so this straight equality still holds."""
    suites = load_all_suites()
    summary = summarize(suites)
    assert summary["total_tests"] == sum(len(s.cases) for s in suites)
    assert summary["total_suites"] == len(suites)
    assert sum(summary["by_project"].values()) == summary["total_tests"]


def test_gap_stub_tests_are_dropped_entirely_not_counted_as_written(tmp_path, monkeypatch):
    """Found live 2026-09-23: 459 of NJT's reported 460 "tests written" were
    `[Setup] Skip GAP: ...` placeholders that automate nothing. They're dropped from the
    dataset entirely -- not counted, not listed -- until genuinely written."""
    from model import automation_tests as at

    proj = tmp_path / "projects" / "fakeproj" / "tests"
    proj.mkdir(parents=True)
    (proj / "test_stub.robot").write_text(
        "*** Settings ***\n"
        "Force Tags    project:fakeproj    device_types:ETM    feature:comms\n\n"
        "*** Test Cases ***\n"
        "A stubbed case\n"
        "    [Tags]    testrailid=C1\n"
        "    [Setup]    Skip    GAP: no device library yet\n"
        "    Case Is Not Yet Automatable\n",
        encoding="utf-8",
    )
    (proj / "test_real.robot").write_text(
        "*** Settings ***\n"
        "Force Tags    project:fakeproj    device_types:ETM    feature:comms\n\n"
        "*** Test Cases ***\n"
        "A real case\n"
        "    [Tags]    testrailid=C2\n"
        "    Given the device is at idle\n"
        "    Then something real happens\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(at, "ROOT", tmp_path)
    summary = at.summarize(at.load_all_suites())

    assert summary["total_tests"] == 1     # only the real one
    assert summary["total_suites"] == 1    # the all-stub suite is dropped entirely
    assert summary["by_project"]["fakeproj"] == 1
    assert summary["by_feature"]["comms"] == 1
    # the stub never reaches the dataset at all
    suites = at.load_all_suites()
    assert all(not c.is_gap_stub for s in suites for c in s.cases)
    assert not any("test_stub.robot" in s.source_file for s in suites)
