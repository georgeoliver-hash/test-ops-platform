"""Gaps list + group-gaps: each marker carries its group, other-device gaps leave a POS list, counts per group."""
from __future__ import annotations

import json
import os
import tempfile

os.environ.setdefault("TESTOPS_WEBAPP_DATA_DIR", tempfile.mkdtemp(prefix="testops-webapp-test-"))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import app as app_mod, runner  # noqa: E402

client = TestClient(app_mod.app)
POS_FILE = "knowledge/translink/specs/POS-FS-x.md"


def _marker(line, text="q"):
    return {"file": POS_FILE, "line": line, "kind": "GAP", "text": text}


@pytest.fixture
def env(tmp_path, monkeypatch):
    fixtures = tmp_path / "fx"
    fixtures.mkdir()
    (fixtures / "gaps.json").write_text(json.dumps([_marker(1), _marker(2), _marker(3), _marker(4)]), encoding="utf-8")
    monkeypatch.setattr(app_mod, "FIXTURES", fixtures)
    monkeypatch.setattr(runner, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    d = tmp_path / "reports" / "translink" / "clarify-gaps"
    d.mkdir(parents=True)

    def groups(rows):
        (d / "gap-groups.expanded.json").write_text(json.dumps(rows), encoding="utf-8")
    return groups


def _g(line, cat, devices=("POS",)):
    return {"file": POS_FILE, "line": line, "category": cat, "devices": list(devices), "evidence": "e", "spec_ref": None}


def test_markers_carry_their_group_and_counts_are_reported(env):
    env([_g(1, "screen"), _g(2, "screen"), _g(3, "behaviour")])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert r["grouped"] is True
    assert r["category_counts"] == {"screen": 2, "behaviour": 1, "unclassified": 1}
    assert {m["line"]: m["category"] for m in r["shown"]} == {1: "screen", 2: "screen", 3: "behaviour", 4: None}


def test_a_gap_that_only_concerns_another_device_is_hidden_from_the_pos_list_and_counted(env):
    env([_g(1, "screen"), _g(2, "other-device", ["ETM"]), _g(3, "value", ["ETM", "PV"]), _g(4, "behaviour", ["ALL"])])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert [m["line"] for m in r["shown"]] == [1, 4]
    assert r["hidden_other_device"] == 2 and r["category_counts"] == {"screen": 1, "behaviour": 1}


def test_filtering_by_group_and_no_classification_yet(env):
    env([_g(1, "screen"), _g(2, "behaviour"), _g(3, "behaviour"), _g(4, "conflict")])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "category": "behaviour"}).json()
    assert [m["line"] for m in r["shown"]] == [2, 3] and r["total"] == 2
    assert r["category_counts"]["screen"] == 1  # counts still describe the whole scope, not just the filter


def test_works_unchanged_when_nothing_has_been_grouped_yet(env):
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert r["grouped"] is False and r["hidden_other_device"] == 0 and len(r["shown"]) == 4
