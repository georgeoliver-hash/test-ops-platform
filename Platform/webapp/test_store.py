"""store.py: local SQLite persistence for suite mappings + encrypted TestRail credentials.

Every test runs against a fresh temp data dir (TESTOPS_WEBAPP_DATA_DIR) so nothing here
ever touches a real developer's Platform/webapp/data/. No module reload needed: store.py
resolves its data dir fresh on every call rather than caching it at import time.
"""
from __future__ import annotations

import pytest


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("TESTOPS_WEBAPP_DATA_DIR", str(tmp_path))
    from Platform.webapp import store as mod

    mod.init_db()
    yield mod


def test_default_user_seeded(store):
    user = store.get_current_user()
    assert user["display_name"] == "George Oliver"


def test_seed_mappings_are_the_real_documented_ones(store):
    mappings = {m["project"] + "|" + m["device"]: m for m in store.list_suite_mappings()}
    assert len(mappings) == 6
    assert mappings["Translink|POS"]["old_suite"] == "AA-POS Acceptance Test"
    assert mappings["Translink|POS"]["new_suite"] == "GG - POS - Claude Suite"
    assert mappings["Translink|TVM"]["old_suite"] == "AA-TVM-Acceptance Test-V03"
    assert mappings["Translink|HHD"]["old_suite"] == "AA-HHD-Acceptance"
    assert mappings["Translink|ETM"]["old_suite"] == "AA-ETM-Acceptance Test"
    assert mappings["Translink|ETM"]["new_suite"] == "NEW ETM-Acceptance Suite"
    assert mappings["Translink|GV"]["old_suite"] == "AA - Gate Validator - Acceptance Test"
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
