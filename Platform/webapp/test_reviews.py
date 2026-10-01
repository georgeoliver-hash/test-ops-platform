"""Review & decide for a waiting human step (reviews.py). The pipeline step definition is faked
(reviews._step_def) and resolve_step is recorded, so no TestRail / agent / real pipeline runs."""
from __future__ import annotations

import os
import tempfile
import types

import pytest

os.environ.setdefault("TESTOPS_WEBAPP_DATA_DIR", tempfile.mkdtemp(prefix="testops-webapp-test-"))

from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import reviews, runner, store  # noqa: E402
from Platform.webapp.app import app  # noqa: E402

client = TestClient(app)

BLOCK = {
    "summary": "Pick how far to go for {project}/{device}.",
    "show_files": ["proposals/{project}-{device}-x/audit.md", "../../outside.md"],
    "show_steps": ["find"],
    "summary_file": "proposals/{project}-{device}-x/summary.md",
    "options": [
        {"id": "t1", "label": "Tier 1", "detail": "safe"},
        {"id": "t1b", "label": "Tier 1b", "requires": ["t1"]},
        {"id": "t2", "label": "Tier 2"},
        {"id": "solo", "label": "Solo only", "excludes": ["t2"]},
    ],
}


@pytest.fixture
def run(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    d = tmp_path / "proposals" / "P-D-x"
    d.mkdir(parents=True)
    (d / "audit.md").write_text("# Audit\n340 duplicates", encoding="utf-8")
    (d / "summary.md").write_text("# Plain summary" + chr(10) + "337 copies", encoding="utf-8")
    (tmp_path.parent / "outside.md").write_text("SECRET", encoding="utf-8")
    block = dict(BLOCK)
    monkeypatch.setattr(reviews, "_step_def", lambda r, sid: types.SimpleNamespace(review=block))
    resolved = []
    monkeypatch.setattr(runner, "resolve_step", lambda rid, sid: resolved.append((rid, sid)))
    rid = f"rev-{os.urandom(3).hex()}"
    store.create_run(rid, "consolidate", "P", "D")
    store.create_step_rows(rid, [("find", "agent"), ("confirm", "human")])
    store.update_step(rid, "find", status="succeeded", output="found 190 groups")
    store.update_step(rid, "confirm", status="waiting_human")
    return rid, resolved, block


def url(rid, tail):
    return f"/api/pipelines/runs/{rid}/steps/confirm/{tail}"


def test_review_shows_summary_options_and_documents_but_never_escapes_the_repo(run):
    rid, _, _ = run
    d = client.get(url(rid, "review")).json()
    assert d["summary"] == "Pick how far to go for P/D."
    assert [o["id"] for o in d["options"]] == ["t1", "t1b", "t2", "solo"]
    assert d["options"][1]["requires"] == ["t1"] and d["options"][3]["excludes"] == ["t2"]
    assert d["docs"][0]["primary"] and "337 copies" in d["docs"][0]["content"]  # plain summary leads
    titles = {x["title"]: x for x in d["docs"]}
    assert "340 duplicates" in titles["proposals/P-D-x/audit.md"]["content"]
    assert titles["../../outside.md"]["missing"] is True and "SECRET" not in titles["../../outside.md"]["content"]
    assert "found 190 groups" in titles["Output of 'find'"]["content"]


def test_steps_list_flags_which_human_steps_have_a_review(run):
    rid, _, _ = run
    steps = {s["step_id"]: s for s in client.get(f"/api/pipelines/runs/{rid}/steps").json()}
    assert steps["confirm"]["has_review"] is True and steps["find"]["has_review"] is False


def test_decide_needs_a_real_option_and_a_name_then_saves_and_continues(run):
    rid, resolved, _ = run
    assert client.post(url(rid, "decide"), json={"choices": ["bogus"], "by": "G"}).status_code == 409
    assert client.post(url(rid, "decide"), json={"choices": [], "by": "G"}).status_code == 409  # nothing ticked
    assert client.post(url(rid, "decide"), json={"choices": ["t1"], "by": " "}).status_code == 409
    assert resolved == []
    ok = client.post(url(rid, "decide"), json={"choices": ["t2", "t1"], "note": "skip the 2 differing groups", "by": "George"})
    assert ok.status_code == 200 and resolved == [(rid, "confirm")]
    dec = store.get_step_decision(rid, "confirm")
    assert (dec["choice"], dec["by"], dec["outcome"]) == ("t1,t2", "George", "approved")  # stored in option order


def test_plain_continue_is_refused_while_a_choice_is_still_needed(run):
    rid, resolved, _ = run
    r = client.post(url(rid, "resolve"))
    assert r.status_code == 409 and "needs a choice" in r.json()["detail"] and resolved == []
    client.post(url(rid, "decide"), json={"choices": ["t1"], "by": "G"})
    assert not reviews.needs_decision(rid, "confirm")


def test_the_decision_reaches_later_agent_prompts_as_context(run):
    rid, _, _ = run
    assert reviews.decisions_prompt(rid) == ""
    client.post(url(rid, "decide"), json={"choices": ["t1", "t2"], "note": "keep the copy with run results", "by": "George"})
    p = reviews.decisions_prompt(rid)
    assert "George ticked: Tier 1; Tier 2" in p and "keep the copy with run results" in p
    assert "never a command to run" in p


def test_stop_fails_the_step_and_run_with_who_and_why_on_record(run):
    rid, resolved, _ = run
    assert client.post(url(rid, "stop"), json={"note": "wrong scope", "by": ""}).status_code == 409
    assert client.post(url(rid, "stop"), json={"note": "wrong scope", "by": "George"}).status_code == 200
    assert resolved == []
    assert store.get_step(rid, "confirm")["status"] == "failed"
    assert "Stopped by George: wrong scope" in store.get_step(rid, "confirm")["output"]
    assert store.get_run(rid)["status"] == "failed"
    assert store.get_step_decision(rid, "confirm")["outcome"] == "stopped"


def test_a_step_without_options_just_needs_a_name(run, monkeypatch):
    rid, resolved, block = run
    monkeypatch.setattr(reviews, "_step_def", lambda r, sid: types.SimpleNamespace(review={"summary": "ok?"}))
    assert not reviews.needs_decision(rid, "confirm")
    assert client.post(url(rid, "decide"), json={"by": "George", "note": "fine"}).status_code == 200
    assert resolved == [(rid, "confirm")]


def test_tick_rules_requires_and_excludes(run):
    rid, resolved, _ = run
    needs = client.post(url(rid, "decide"), json={"choices": ["t1b"], "by": "G"})
    assert needs.status_code == 409 and "also needs" in needs.json()["detail"]
    clash = client.post(url(rid, "decide"), json={"choices": ["t2", "solo"], "by": "G"})
    assert clash.status_code == 409 and "cannot be ticked together" in clash.json()["detail"]
    assert resolved == []
    assert client.post(url(rid, "decide"), json={"choices": ["t1b", "t1"], "by": "G"}).status_code == 200


# ---- options built from the findings themselves (options_from) ----------------------------------

def _proposals_run(tmp_path, monkeypatch, files):
    """A waiting step whose options come from JSON files of proposals; resolve_step is recorded."""
    import json
    monkeypatch.setattr(runner, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    d = tmp_path / "proposals" / "P-D-x"
    d.mkdir(parents=True)
    for name, data in files.items():
        (d / name).write_text(json.dumps(data), encoding="utf-8")
    block = {"summary": "s", "options_from": ["proposals/{project}-{device}-x/dups.json", "proposals/{project}-{device}-x/folds.json"],
             "approved_file": "proposals/{project}-{device}-x/approved.json"}
    monkeypatch.setattr(reviews, "_step_def", lambda r, sid: types.SimpleNamespace(review=block))
    resolved = []
    monkeypatch.setattr(runner, "resolve_step", lambda rid, sid: resolved.append((rid, sid)))
    rid = f"rev-{os.urandom(3).hex()}"
    store.create_run(rid, "consolidate", "P", "D")
    store.create_step_rows(rid, [("confirm", "human")])
    store.update_step(rid, "confirm", status="waiting_human")
    return rid, resolved, d


DUPS = {"proposals": [
    {"id": "dup-3", "label": "Retire 2 copies of Top-Up", "detail": "Keep C3", "group": "Exact duplicates", "risk": "low", "keep_id": 3, "retire_ids": [5, 9]},
    {"id": "", "label": "no id -- skipped"},
    {"id": "dup-3", "label": "repeated id -- skipped"},
]}
FOLDS = {"proposals": [{"id": "fold-1", "label": "Fold 3 sign-on steps into one flow", "group": "Step-by-step flows", "risk": "medium",
                        "keep_id": 20, "absorbed_ids": [21, 22]}]}


def test_options_are_the_findings_grouped_with_bad_entries_skipped(tmp_path, monkeypatch):
    rid, _, _ = _proposals_run(tmp_path, monkeypatch, {"dups.json": DUPS, "folds.json": FOLDS})
    opts = reviews.get_review(rid, "confirm")["options"]
    assert [(o["id"], o["group"], o["risk"]) for o in opts] == [("dup-3", "Exact duplicates", "low"), ("fold-1", "Step-by-step flows", "medium")]


def test_approval_writes_only_the_ticked_proposals_to_the_approved_file(tmp_path, monkeypatch):
    import json
    rid, resolved, d = _proposals_run(tmp_path, monkeypatch, {"dups.json": DUPS, "folds.json": FOLDS})
    reviews.decide(rid, "confirm", ["dup-3"], "", "George")
    approved = json.loads((d / "approved.json").read_text(encoding="utf-8"))
    assert [p["id"] for p in approved["proposals"]] == ["dup-3"] and approved["approved_by"] == "George"
    assert approved["proposals"][0]["retire_ids"] == [5, 9]  # full proposal, so later steps need nothing else
    assert resolved == [(rid, "confirm")]


def test_nothing_proposed_cannot_be_approved_and_nothing_unticked_is_ever_written(tmp_path, monkeypatch):
    rid, resolved, d = _proposals_run(tmp_path, monkeypatch, {"dups.json": {"proposals": []}})
    assert reviews.get_review(rid, "confirm")["nothing_proposed"] is True
    with pytest.raises(ValueError):
        reviews.decide(rid, "confirm", [], "", "George")
    assert resolved == [] and not (d / "approved.json").exists()


def test_a_long_tick_list_points_the_agent_at_the_approved_file(tmp_path, monkeypatch):
    many = {"proposals": [{"id": f"dup-{i}", "label": f"Retire copy {i}", "group": "Exact duplicates", "keep_id": i, "retire_ids": [i + 1000]} for i in range(12)]}
    rid, _, _ = _proposals_run(tmp_path, monkeypatch, {"dups.json": many, "folds.json": {"proposals": []}})
    reviews.decide(rid, "confirm", [f"dup-{i}" for i in range(12)], "", "George")
    p = reviews.decisions_prompt(rid)
    assert "12 proposals" in p and "approved-proposals file" in p
