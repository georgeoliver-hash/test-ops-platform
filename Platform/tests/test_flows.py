"""Regression tests for model/flows.py against real data — SIT's mirrored screenflow output
AND testops's hand-transcribed flow maps. Two real, differently-shaped sources, checked
separately (see flows.py's module docstring for why they aren't joined yet).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from model.flows import _strip_jsonc_comments, available_screen_graphs, load_flow_map, load_screen_graph

TESTOPS_KNOWLEDGE_FLOWS = (
    Path(__file__).resolve().parent.parent / "testops" / "knowledge" / "flows"
)


def test_translink_pos_has_a_screen_graph():
    assert "POS" in available_screen_graphs("Translink")


def test_translink_pos_screen_graph_parses_real_transitions():
    graph = load_screen_graph("Translink", "POS")
    assert "Idle" in graph.screens
    assert "SignOn" in graph.screens
    # Idle -> SignOn via a UI_Key/Enter transition, per the real screenflow_map.jsonc
    idle_transitions = graph.transitions_from("Idle")
    assert any(t.to_screen == "SignOn" for t in idle_transitions)
    signon_to_motd = next(
        (t for t in graph.transitions_from("SignOn") if t.to_screen == "MessageOfTheDay"), None
    )
    assert signon_to_motd is not None
    assert signon_to_motd.type == "Stages"
    assert len(signon_to_motd.actions) >= 1


def test_unmirrored_device_raises_not_silently_empty():
    with pytest.raises(FileNotFoundError):
        load_screen_graph("Translink", "NoSuchDevice")


def test_njt_etm_has_a_screen_graph():
    assert "ETM" in available_screen_graphs("NJT")


def test_translink_pos_basket_payment_flow_map_parses_real_paths():
    path = TESTOPS_KNOWLEDGE_FLOWS / "translink-pos-basket-payment.md"
    if not path.is_file():
        pytest.skip(f"sandbox testops/ copy doesn't have {path.name} — expected if it's stale")
    flow_map = load_flow_map(path)
    assert len(flow_map.paths) >= 15
    first = flow_map.paths[0]
    assert first.path_id == 1
    assert first.feature == "basket-bus"
    assert 4099989 in first.covered_by


def test_flow_map_with_no_paths_table_returns_empty_not_an_error(tmp_path):
    f = tmp_path / "no-table.md"
    f.write_text("# Flow: nothing here\n\nJust prose, no table.\n", encoding="utf-8")
    flow_map = load_flow_map(f)
    assert flow_map.paths == []


def test_uncovered_paths_are_the_ones_with_no_case_ids(tmp_path):
    f = tmp_path / "mini.md"
    f.write_text(
        "# Flow: mini\n\n"
        "## Paths (each path = one candidate scenario)\n"
        "| # | Path | Feature | Tags | Covered by |\n"
        "|---|------|---------|------|------------|\n"
        "| 1 | A -> B | auth | — | 100 |\n"
        "| 2 | A -> C | auth | @destructive | ? |\n\n"
        "## Notes\n",
        encoding="utf-8",
    )
    flow_map = load_flow_map(f)
    assert len(flow_map.paths) == 2
    assert flow_map.paths[0].covered_by == [100]
    uncovered = flow_map.uncovered()
    assert len(uncovered) == 1
    assert uncovered[0].path_id == 2
    assert uncovered[0].covered_by_raw == "?"


def test_strip_jsonc_comments_handles_trailing_inline_comments():
    # Real shape from Translink/BV's screenflow_map.jsonc, 2026-09-09: a prior version of
    # this stripper only matched comments that START a line, missing this trailing case.
    raw = '{\n  "StaffPin": "[StaffPin]1234",  // TODO\n  "Other": "value"\n}'
    stripped = _strip_jsonc_comments(raw)
    import json
    parsed = json.loads(stripped)
    assert parsed == {"StaffPin": "[StaffPin]1234", "Other": "value"}


def test_strip_jsonc_comments_does_not_eat_slashes_inside_strings():
    raw = '{\n  "Url": "http://example.com"  // a real comment\n}'
    stripped = _strip_jsonc_comments(raw)
    import json
    parsed = json.loads(stripped)
    assert parsed == {"Url": "http://example.com"}


def test_translink_bv_screen_graph_parses():
    graph = load_screen_graph("Translink", "BV")
    assert len(graph.screens) > 0
    assert len(graph.transitions) > 0
