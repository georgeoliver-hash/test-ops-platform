"""sit_tree counts tests and tags from .robot files on disk -- suite tags, [Tags] continuation lines, backlog split."""
from Platform.webapp import sit_tree

ROBOT = """*** Settings ***
Test Tags    C=POS    feature=Audit

*** Test Cases ***
First Test
    [Tags]    Smoke    area=Audit    mode=nir
    ...       mode=metro    testrail=C1
    Log    hi

Second Test
    [Tags]    BVT    area=Audit    impl=complete
    Log    there
"""


def test_tree_counts_tests_tags_and_folders(tmp_path):
    flow = tmp_path / "Tests" / "POS" / "Flow" / "Device"
    flow.mkdir(parents=True)
    (flow / "test_a.robot").write_text(ROBOT, encoding="utf-8")
    backlog = tmp_path / "Tests" / "POS" / "_Backlog"
    backlog.mkdir(parents=True)
    (backlog / "test_b.robot").write_text(ROBOT, encoding="utf-8")
    r = sit_tree.tree("Translink", "POS", root=tmp_path)
    assert r["available"] and r["folder"] == "Tests/POS"
    s = r["summary"]
    assert s["total"] == 2 and s["flags"] == {"smoke": 1, "bvt": 1} and s["testrail_linked"] == 1
    assert s["families"]["mode"] == {"nir": 1, "metro": 1} and s["families"]["area"] == {"Audit": 2}
    assert s["families"]["feature"] == {"Audit": 2}
    assert r["backlog"] == 2
    assert [(n["path"], n["total"]) for n in r["nodes"]] == [("Flow", 2), ("Flow/Device", 2)]


def test_missing_checkout_or_folder_says_so(tmp_path):
    assert not sit_tree.tree("X", "POS", root=tmp_path)["available"]
    (tmp_path / "Tests").mkdir()
    r = sit_tree.tree("X", "POS", root=tmp_path)
    assert not r["available"] and "no Tests folder" in r["reason"]


def test_project_device_folder_wins_and_a_bare_device_folder_is_not_guessed(tmp_path):
    for rel in ("Tests/NJT/ETM", "Tests/ETM"):
        d = tmp_path / rel
        d.mkdir(parents=True)
        (d / "t.robot").write_text(ROBOT, encoding="utf-8")
    assert sit_tree.tree("NJT", "ETM", root=tmp_path)["folder"] == "Tests/NJT/ETM"
    assert not sit_tree.tree("Translink", "ETM", root=tmp_path)["available"]
