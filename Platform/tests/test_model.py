"""Regression tests for model/ against the real sit-mirror/ snapshot.

These will need updating (not just re-running) if sit-mirror/ is re-synced and SIT's real data
changes — that's expected and correct; a failing test here after a re-sync is the mirror telling
you something upstream moved, not a bug.
"""
from __future__ import annotations

import pytest

from model.devices import list_mirrored_projects, load_registry
from model.functions import find_keyword, load_all_keywords


def test_translink_is_mirrored():
    assert "Translink" in list_mirrored_projects()


def test_translink_pos_equipment_types():
    registry = load_registry("Translink")
    pos = registry.get("POS")
    assert pos is not None
    assert "POS_Way6" in pos.equipment_type_names


def test_unmirrored_project_raises():
    with pytest.raises(FileNotFoundError):
        load_registry("NoSuchProject")


def test_function_keywords_parsed():
    keywords = load_all_keywords()
    assert len(keywords) > 0
    assert any(k.device_family == "POS" for k in keywords)


def test_resolve_known_keyword():
    match = find_keyword("the operator is signed off")
    assert match is not None
    assert match.device_family == "POS"


def test_resolve_unknown_keyword_returns_none():
    assert find_keyword("this phrase does not exist anywhere in sit") is None
