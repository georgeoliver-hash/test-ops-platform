"""judge-failures renders to real commands: placeholders resolve, the optional run id is dropped when blank and kept when given."""
import re

from Platform.webapp import app as _app  # noqa: F401  (points TESTOPS_CLAUDE_ROOT at the sibling system-test-ops)
from Platform.webapp import runner
from model import pipelines
from Platform.webapp.runner import _command_params, _render, _resolve_optional_flags


def _commands(extra):
    p = pipelines.load_pipeline("judge-failures")
    params = {"project": "Translink", "device": "POS", "date": "2026-10-08", **extra}
    return {s.id: _resolve_optional_flags(_render(s.command, _command_params(params)), params) for s in p.steps if s.kind.value == "cli"}


def test_the_pipeline_is_registered_with_its_steps_in_order():
    p = pipelines.load_pipeline("judge-failures")
    assert [s.id for s in p.steps] == ["pull_run", "collect_failures", "judge", "validate", "confirm", "export_tags", "raise_in_sit"]
    assert [i.name for i in p.inputs] == ["project", "device", "run_id"] and not [i for i in p.inputs if i.name == "run_id"][0].required


def test_without_a_run_id_the_newest_run_is_used():
    cmd = _commands({})["pull_run"]
    assert "--run-id" not in cmd and "--project Translink --device POS" in cmd


def test_a_given_run_id_is_passed_through():
    assert "--run-id 37589555395" in _commands({"run_id": "37589555395"})["pull_run"]


def test_every_cli_step_is_fully_rendered():
    for sid, cmd in _commands({}).items():
        assert not re.search(r"\{[\w.]+\}", cmd), (sid, cmd)
        assert cmd.startswith("python -m system_test_ops "), sid


def test_export_never_applies_or_pushes_anything():
    cmd = _commands({})["export_tags"]
    assert "export-severity-tags" in cmd and "--queue" in cmd and "git " not in cmd and "push" not in cmd.replace("export-severity-tags", "")
