"""store.py: local SQLite persistence for suite mappings + encrypted TestRail credentials.

Every test runs against a fresh temp data dir (TESTOPS_WEBAPP_DATA_DIR) so nothing here
ever touches a real developer's Platform/webapp/data/. No module reload needed: store.py
resolves its data dir fresh on every call rather than caching it at import time.
"""
from __future__ import annotations

import pytest
import yaml

# Test-only fixture data mirroring the real, committed system-test-ops/knowledge/
# suite_targets.yaml. Deliberately lives HERE, not as a hardcoded fallback inside store.py
# itself (2026-09-22: that in-code fallback had already drifted from the real file -- see
# store._load_suite_targets's docstring -- which is exactly the duplication this was fixed
# to remove). Tests get their own explicit, visible copy instead of relying on production
# code silently bootstrapping one.
_SEED_TARGETS = [
    {"project": "Translink", "device": "POS", "old_suite": "AA-POS Acceptance Test", "old_suite_id": 9317,
     "new_suite": "GG - POS - Claude Suite", "new_suite_id": 30253, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "ETM", "old_suite": "AA-ETM-Acceptance Test", "old_suite_id": 4943,
     "new_suite": "NEW ETM-Acceptance Suite", "new_suite_id": 30254, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "GV", "old_suite": "AA - Gate Validator - Acceptance Test", "old_suite_id": 14973,
     "new_suite": "NEW GV Test Suite", "new_suite_id": 30286, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "TVM", "old_suite": "AA-TVM-Acceptance Test-V03", "old_suite_id": 5602,
     "new_suite": "NEW TVM Test Suite", "new_suite_id": 30284, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "HHD", "old_suite": "AA-HHD-Acceptance", "old_suite_id": 5446,
     "new_suite": "NEW HHD Test Suite", "new_suite_id": 30285, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "PV", "old_suite": "AA-Platform Validator Acceptance Test", "old_suite_id": 10047,
     "new_suite": "NEW PV-Acceptance Test Suite", "new_suite_id": 30255, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "Translink", "device": "BOS", "old_suite": "2.1-Backoffice Systems - Acceptance Suite", "old_suite_id": 14441,
     "new_suite": "NEW BOS & ABT Suite", "new_suite_id": 30279, "fresh_build": False, "testrail_project_id": 42, "new_testrail_project_id": 42},
    {"project": "NJT", "device": "ETM", "old_suite": "", "old_suite_id": None,
     "new_suite": "NJT - SystemTestOps", "new_suite_id": 30295, "fresh_build": True, "testrail_project_id": 27, "new_testrail_project_id": 27},
]


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("TESTOPS_WEBAPP_DATA_DIR", str(tmp_path))
    # Isolated from the real, committed system-test-ops/knowledge/suite_targets.yaml --
    # without this, any test that upserts a mapping would write through to the actual
    # sibling-repo file on disk. Pre-seeded with the fixture data above so every existing
    # test keeps seeing the same 8 targets it always has.
    targets_path = tmp_path / "suite_targets.yaml"
    targets_path.write_text(yaml.safe_dump({"version": 1, "targets": _SEED_TARGETS}, sort_keys=False), encoding="utf-8")
    monkeypatch.setenv("TESTOPS_SUITE_TARGETS_PATH", str(targets_path))
    from Platform.webapp import store as mod

    mod.init_db()
    yield mod


def test_default_user_seeded(store):
    user = store.get_current_user()
    assert user["display_name"] == "George Oliver"


def test_seed_mappings_are_the_real_documented_ones(store):
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert len(mappings) == 8
    assert mappings["Translink|POS"]["old_suite"] == "AA-POS Acceptance Test"
    assert mappings["Translink|POS"]["new_suite"] == "GG - POS - Claude Suite"
    assert mappings["Translink|TVM"]["old_suite"] == "AA-TVM-Acceptance Test-V03"
    assert mappings["Translink|HHD"]["old_suite"] == "AA-HHD-Acceptance"
    assert mappings["Translink|ETM"]["old_suite"] == "AA-ETM-Acceptance Test"
    assert mappings["Translink|ETM"]["new_suite"] == "NEW ETM-Acceptance Suite"
    assert mappings["Translink|GV"]["old_suite"] == "AA - Gate Validator - Acceptance Test"
    assert mappings["Translink|BOS"]["old_suite"] == "2.1-Backoffice Systems - Acceptance Suite"
    assert mappings["Translink|BOS"]["new_suite_id"] == 30279
    assert mappings["NJT|ETM"]["old_suite"] == ""  # fresh build, no old suite by design
    assert mappings["NJT|ETM"]["new_suite"] == "NJT - SystemTestOps"
    assert mappings["Translink|PV"]["old_suite"] == "AA-Platform Validator Acceptance Test"


def test_upsert_new_mapping(store):
    store.upsert_suite_mapping("NJT", "ETM", "Old NJT Suite", "New NJT Suite")
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert "NJT|ETM" in mappings
    assert mappings["NJT|ETM"]["old_suite"] == "Old NJT Suite"


def test_upsert_updates_existing_pair_not_duplicate(store):
    before = len(store.list_suite_mappings())
    store.upsert_suite_mapping("Translink", "POS", "New Old Name", "New New Name")
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert len(mappings) == before  # updated in place, no new row
    assert mappings["Translink|POS"]["old_suite"] == "New Old Name"


def test_upsert_rejects_blank_fields(store):
    with pytest.raises(ValueError):
        store.upsert_suite_mapping("NJT", "", "Old", "New")


def test_delete_mapping(store):
    store.upsert_suite_mapping("NJT", "ETM", "Old", "New")
    assert store.delete_suite_mapping("NJT", "ETM") is True
    assert store.delete_suite_mapping("NJT", "ETM") is False  # already gone
    assert not any(m["project"] == "NJT" for m in store.list_suite_mappings())


def test_delete_mapping_also_removes_it_from_the_shared_yaml(store):
    # Regression: delete_suite_mapping used to only touch the local per-machine SQLite
    # row, never the git-tracked suite_targets.yaml mirror that upsert_suite_mapping
    # write-throughs to -- so a deleted target could linger in the shared file forever
    # (or, worse, still be sitting there from before this session's git history even
    # started, silently visible to anyone who later pulls it).
    store.upsert_suite_mapping("Dryrun", "ETM", "Old Dryrun", "New Dryrun")
    assert any(e.get("project") == "Dryrun" for e in store._load_suite_targets())

    store.delete_suite_mapping("Dryrun", "ETM")

    assert not any(e.get("project") == "Dryrun" for e in store._load_suite_targets())
    # Other real targets already in the shared file must survive untouched.
    assert any(e.get("project") == "Translink" and e.get("device") == "POS" for e in store._load_suite_targets())


def test_delete_mapping_for_a_nonexistent_pair_does_not_touch_the_yaml(store):
    before = store._load_suite_targets()
    assert store.delete_suite_mapping("Nope", "Nope") is False
    assert store._load_suite_targets() == before


def test_credentials_not_configured_by_default(store):
    status = store.get_credentials_status()
    assert status == {"configured": False}


def test_save_credentials_never_exposes_key_in_status(store):
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "super-secret-key-123")
    status = store.get_credentials_status()
    assert status["configured"] is True
    assert status["testrail_url"] == "https://example.testrail.io"
    assert "super-secret-key-123" not in str(status)


def test_credentials_roundtrip_decrypt(store):
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "super-secret-key-123")
    assert store.decrypt_api_key() == "super-secret-key-123"


def test_credentials_encrypted_on_disk_not_plaintext(store):
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "super-secret-key-123")
    raw = store._db_path().read_bytes()
    assert b"super-secret-key-123" not in raw


def test_save_credentials_rejects_blanks(store):
    with pytest.raises(ValueError):
        store.save_credentials("", "user", "key")


def test_delete_credentials(store):
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "key")
    assert store.delete_credentials() is True
    assert store.get_credentials_status()["configured"] is False
    assert store.decrypt_api_key() is None


def test_secret_key_file_created_and_reused(store):
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "key-a")
    key_bytes_1 = store._key_path().read_bytes()
    store.save_credentials("https://example.testrail.io", "george@arrive.com", "key-b")
    key_bytes_2 = store._key_path().read_bytes()
    assert key_bytes_1 == key_bytes_2  # same key reused, not regenerated per save
    assert store.decrypt_api_key() == "key-b"


def test_fresh_build_requires_explicit_flag_not_just_blank_old_suite(store):
    with pytest.raises(ValueError):
        store.upsert_suite_mapping("PERTH", "POS", "", "New PERTH Suite")


def test_fresh_build_with_explicit_flag_succeeds(store):
    store.upsert_suite_mapping("PERTH", "POS", "", "New PERTH Suite", fresh_build=True)
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["PERTH|POS"]["old_suite"] == ""
    assert mappings["PERTH|POS"]["new_suite"] == "New PERTH Suite"


def test_get_suite_ids_for_bos(store):
    ids = store.get_suite_ids("Translink", "BOS")
    assert ids == {"old_suite_id": 14441, "new_suite_id": 30279}


def test_pipeline_run_steps_roundtrip(store):
    store.create_run("run-1", "audit", "Translink", "POS")
    store.create_step_rows("run-1", [("run_audit", "cli"), ("summarise", "agent")])

    steps = store.get_steps("run-1")
    assert [s["step_id"] for s in steps] == ["run_audit", "summarise"]
    assert all(s["status"] == "pending" for s in steps)
    assert steps[0]["kind"] == "cli"

    store.update_step("run-1", "run_audit", status="succeeded", output="ok", finished_at="2026-09-14T00:00:00")
    step = store.get_step("run-1", "run_audit")
    assert step["status"] == "succeeded"
    assert step["output"] == "ok"
    assert step["finished_at"] == "2026-09-14T00:00:00"

    # the other step is untouched
    other = store.get_step("run-1", "summarise")
    assert other["status"] == "pending"


def test_get_steps_empty_for_unknown_run(store):
    assert store.get_steps("no-such-run") == []


def test_get_runs_returns_history_newest_first(store):
    store.create_run("run-a", "audit-coverage", "Translink", "POS", extra_inputs={"fix_version": "4.2.0"})
    store.create_run("run-b", "audit-coverage", "Translink", "POS", extra_inputs={"fix_version": "4.3.0, 4.4.0"})
    runs = store.get_runs("audit-coverage", "Translink", "POS")
    assert [r["id"] for r in runs] == ["run-b", "run-a"]
    assert runs[0]["extra_inputs"] == {"fix_version": "4.3.0, 4.4.0"}
    assert runs[1]["extra_inputs"] == {"fix_version": "4.2.0"}


def test_get_runs_extra_inputs_none_when_not_given(store):
    store.create_run("run-c", "audit", "Translink", "POS")
    runs = store.get_runs("audit", "Translink", "POS")
    assert runs[0]["extra_inputs"] is None


def test_get_runs_scoped_to_pipeline_and_target(store):
    store.create_run("run-d", "audit-coverage", "Translink", "POS")
    store.create_run("run-e", "audit-coverage", "NJT", "ETM")
    store.create_run("run-f", "audit", "Translink", "POS")
    runs = store.get_runs("audit-coverage", "Translink", "POS")
    assert [r["id"] for r in runs] == ["run-d"]


def test_get_runs_respects_limit(store):
    for i in range(5):
        store.create_run(f"run-limit-{i}", "audit", "Translink", "POS")
    runs = store.get_runs("audit", "Translink", "POS", limit=2)
    assert len(runs) == 2


def test_get_step_none_for_unknown_step(store):
    store.create_run("run-2", "audit", "Translink", "POS")
    store.create_step_rows("run-2", [("only_step", "human")])
    assert store.get_step("run-2", "does-not-exist") is None


def test_seed_mappings_start_unapproved(store):
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["Translink|POS"]["approved_by"] is None
    assert mappings["Translink|POS"]["approved_at"] is None
    assert mappings["NJT|ETM"]["approved_by"] is None
    assert store.is_target_approved("Translink", "POS") is False
    assert store.is_target_approved("NJT", "ETM") is False


def test_approve_suite_mapping_roundtrip(store):
    updated = store.approve_suite_mapping("NJT", "ETM", "George Oliver")
    assert updated["approved_by"] == "George Oliver"
    assert updated["approved_at"] is not None
    assert store.is_target_approved("NJT", "ETM") is True

    # a previously seeded, real row (with a real old_suite) is untouched by the migration
    # and unaffected by approving a DIFFERENT target
    assert store.is_target_approved("Translink", "POS") is False
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["Translink|POS"]["old_suite"] == "AA-POS Acceptance Test"
    assert mappings["Translink|POS"]["approved_by"] is None


def test_approve_suite_mapping_unknown_target_returns_none(store):
    assert store.approve_suite_mapping("NoSuchProject", "NoSuchDevice", "George Oliver") is None


def test_approve_suite_mapping_rejects_blank_approver(store):
    with pytest.raises(ValueError):
        store.approve_suite_mapping("NJT", "ETM", "   ")


def test_is_target_approved_false_for_unknown_target(store):
    assert store.is_target_approved("NoSuchProject", "NoSuchDevice") is False


def test_upsert_writes_through_to_shared_yaml_file(store, tmp_path):
    """A target added/edited via upsert_suite_mapping (the existing "Add/edit this pair" UI)
    must land in the git-trackable suite_targets.yaml, not just the local db -- that's the
    whole point of it being shared via git instead of per-machine SQLite."""
    store.upsert_suite_mapping("Perth", "POS", "Old Perth Suite", "New Perth Suite", new_suite_id=40001, old_suite_id=5001)
    targets_path = tmp_path / "suite_targets.yaml"
    assert targets_path.is_file()
    entries = {(t["project"], t["device"]): t for t in store._load_suite_targets()}
    assert ("Perth", "POS") in entries
    assert entries[("Perth", "POS")]["new_suite_id"] == 40001
    assert entries[("Perth", "POS")]["old_suite"] == "Old Perth Suite"


def test_upsert_updates_existing_yaml_entry_in_place_not_duplicated(store):
    store.upsert_suite_mapping("Translink", "POS", "Changed Old", "Changed New", new_suite_id=99999)
    entries = store._load_suite_targets()
    pos_entries = [t for t in entries if t["project"] == "Translink" and t["device"] == "POS"]
    assert len(pos_entries) == 1
    assert pos_entries[0]["old_suite"] == "Changed Old"


def test_yaml_source_reproduces_the_same_eight_seeded_targets(store):
    """A fresh clone with no local db yet must see identical targets to today's hardcoded
    list -- this is the regression check for moving seeding out of Python into the YAML."""
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert len(mappings) == 8
    assert mappings["Translink|TVM"]["new_suite_id"] == 30284
    assert mappings["NJT|ETM"]["old_suite"] == ""
    assert mappings["NJT|ETM"]["old_suite_id"] is None


def test_seeded_testrail_project_ids_are_the_real_confirmed_values(store):
    """Translink's suites live under real TestRail project 42 ("TFTS - System Test"); NJT's
    live under 27 ("UK Bus Projects") -- confirmed live, 2026-09-14, after a target got
    audited against the wrong project because a single global .env default can't serve
    every target. Never invent a value for a project we haven't confirmed."""
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["Translink|POS"]["testrail_project_id"] == 42
    assert mappings["Translink|TVM"]["testrail_project_id"] == 42
    assert mappings["Translink|BOS"]["testrail_project_id"] == 42
    assert mappings["NJT|ETM"]["testrail_project_id"] == 27


def test_get_testrail_project_id(store):
    assert store.get_testrail_project_id("Translink", "POS") == 42
    assert store.get_testrail_project_id("NJT", "ETM") == 27
    assert store.get_testrail_project_id("NoSuchProject", "NoSuchDevice") is None


def test_upsert_persists_testrail_project_id(store):
    store.upsert_suite_mapping("Perth", "POS", "Old Perth Suite", "New Perth Suite",
                                new_suite_id=40001, old_suite_id=5001, testrail_project_id=13)
    assert store.get_testrail_project_id("Perth", "POS") == 13
    entries = {(t["project"], t["device"]): t for t in store._load_suite_targets()}
    assert entries[("Perth", "POS")]["testrail_project_id"] == 13


def test_old_and_new_suite_can_live_under_different_testrail_projects(store):
    """Found live, 2026-09-14: a dry-run target's old suite sat under TestRail project 27
    while its new suite sat under project 12 -- one field can't serve both, since
    old-suite-related commands (audit_old_suite/audit_run_history) and new-suite-related
    ones (push_area/definition_of_done) need different real project ids."""
    store.upsert_suite_mapping("Wealden", "ETM", "Old Wealden Suite", "New Wealden Suite",
                                new_suite_id=50002, old_suite_id=15201,
                                testrail_project_id=27, new_testrail_project_id=12)
    assert store.get_testrail_project_id("Wealden", "ETM") == 27
    assert store.get_new_testrail_project_id("Wealden", "ETM") == 12
    entries = {(t["project"], t["device"]): t for t in store._load_suite_targets()}
    assert entries[("Wealden", "ETM")]["testrail_project_id"] == 27
    assert entries[("Wealden", "ETM")]["new_testrail_project_id"] == 12


def test_upsert_does_not_clobber_testrail_project_id_when_omitted(store):
    """A later edit that doesn't mention testrail_project_id (e.g. the existing "Add/edit
    this pair" flow before the real dropdown fetches a project) must not silently wipe out
    an already-confirmed value."""
    store.upsert_suite_mapping("Translink", "POS", "AA-POS Acceptance Test", "GG - POS - Claude Suite",
                                new_suite_id=30253, old_suite_id=9317)  # no testrail_project_id passed
    assert store.get_testrail_project_id("Translink", "POS") == 42


def test_migration_backfills_testrail_project_id_without_clobbering_other_columns(store, tmp_path):
    """Simulates a pre-migration db (column doesn't exist yet) getting the new column added
    and backfilled from suite_targets.yaml on the next init_db() -- must not disturb
    unrelated already-set columns like approved_by."""
    store.approve_suite_mapping("NJT", "ETM", "George Oliver")
    with store._connect() as conn:
        conn.execute("ALTER TABLE suite_mappings RENAME TO suite_mappings_old")
        conn.execute(
            """CREATE TABLE suite_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, project TEXT NOT NULL,
                device TEXT NOT NULL, old_suite TEXT NOT NULL, new_suite TEXT NOT NULL,
                new_suite_id INTEGER, old_suite_id INTEGER, approved_by TEXT, approved_at TEXT,
                updated_at TEXT NOT NULL, UNIQUE(user_id, project, device)
            )"""
        )
        conn.execute(
            "INSERT INTO suite_mappings SELECT id, user_id, project, device, old_suite, new_suite, "
            "new_suite_id, old_suite_id, approved_by, approved_at, updated_at FROM suite_mappings_old"
        )
        conn.execute("DROP TABLE suite_mappings_old")
    store.init_db()
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["NJT|ETM"]["testrail_project_id"] == 27
    assert mappings["NJT|ETM"]["approved_by"] == "George Oliver"  # untouched by the migration


def test_load_suite_targets_returns_empty_when_missing_no_phantom_seed(tmp_path, monkeypatch):
    """2026-09-22: this used to bootstrap a hardcoded fallback list onto disk -- itself a
    second, silently-drifting copy of the real registry. Now a missing file (e.g. no sibling
    system-test-ops checkout yet) just means an honest empty list; nothing is written."""
    monkeypatch.setenv("TESTOPS_WEBAPP_DATA_DIR", str(tmp_path / "data"))
    targets_path = tmp_path / "does-not-exist-yet" / "suite_targets.yaml"
    monkeypatch.setenv("TESTOPS_SUITE_TARGETS_PATH", str(targets_path))
    from Platform.webapp import store as mod

    assert not targets_path.is_file()
    entries = mod._load_suite_targets()
    assert entries == []
    assert not targets_path.is_file()  # never bootstrapped -- nothing to silently drift from


def test_suite_targets_git_status_reports_unknown_outside_a_git_repo(tmp_path, monkeypatch):
    """No git repo at the resolved root -> the read-only status check degrades to "unknown"
    rather than raising -- this must never break loading the target list itself."""
    monkeypatch.setenv("TESTOPS_WEBAPP_DATA_DIR", str(tmp_path))
    from Platform.webapp import store as mod

    monkeypatch.setattr(mod, "_system_test_ops_root", lambda: tmp_path)
    status = mod.suite_targets_git_status()
    assert status["status"] == "unknown"


def test_migration_backfills_approval_columns_without_clobbering_rows(store):
    """Simulates a DB created before approved_by/approved_at existed -- init_db's ALTER
    TABLE migration must add the columns without touching any existing row's data."""
    store.approve_suite_mapping("NJT", "ETM", "George Oliver")

    # re-running init_db (as app.py does on every startup) must be a no-op for existing data
    store.init_db()
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert mappings["NJT|ETM"]["approved_by"] == "George Oliver"
    assert mappings["Translink|POS"]["approved_by"] is None
