"""The tool's own routing schema — what runs for a UI action, in what order, and where AI sits.

This is NOT a new format invented here. `testops/.claude/pipelines/*.yaml` already exists as
that source of truth (see `testops/docs/pipelines-schema.md`) — a UI button reads `index.yaml`
to build its menu, then that pipeline's own file for its ordered `steps[]`, each tagged
`kind: cli|agent|human|gate`. This module is the typed, validated Python view of exactly that
data: `route(ui_action)` is the literal function a UI click would call to get back a fully
loaded `Pipeline` — steps, guardrails, kinds — instead of hand-parsing YAML each time.

It also makes queryable, in code, what the AI Boundary Map artifact had to hand-build as a
prose table: `ai_density_report()` returns the same cli/agent/human/gate counts per pipeline
that table listed by hand — now derived from the real files, so it can never silently drift
from them again.

Relationship to `ai_steps.yaml` (Foundation Plan, Phase 2, not built yet): that file will
declare the ~5 genuinely AI-*dependent* judgement points (distil-spec, author-case, ...) with
their deterministic `--no-ai` fallback. This schema is one level up — every step of every
pipeline, `kind: agent` included — `ai_steps.yaml` is expected to be a *subset* annotation on
top of the `kind: agent` steps this module already exposes via `agent_steps()`, not a
competing structure. Wire that link when Phase 2 actually lands.
"""
from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


def _default_root() -> Path:
    override = os.environ.get("TESTOPS_CLAUDE_ROOT")
    if override:
        return Path(override)
    # Eventual merged layout: Platform/model/pipelines.py -> Platform/testops/.claude
    return Path(__file__).resolve().parent.parent / "testops" / ".claude"


CLAUDE_ROOT = _default_root()
PIPELINES_ROOT = CLAUDE_ROOT / "pipelines"


class StepKind(str, Enum):
    cli = "cli"
    agent = "agent"
    human = "human"
    gate = "gate"


class Step(BaseModel):
    """One step of a pipeline. Deliberately permissive (`extra="allow"`): the pipeline files
    are a living format (see e.g. `routing_table`/`exclusion` on audit-flows' `triage` step,
    `parallel`/`classifications` on a couple of others) and rejecting a legitimate field a
    pipeline author added would be worse than not having it typed here yet.

    `kind` is optional because a composite pipeline (e.g. `new-suite-from-docs.yaml`) has steps
    that are just `{id, ref: <other-pipeline-id>}` — "run that whole pipeline inline" — with no
    kind of its own; `is_composite_ref` is how a caller tells the two shapes apart.
    """

    model_config = ConfigDict(extra="allow")

    id: str
    kind: StepKind | None = None
    command: str | None = None
    agent: str | None = None
    note: str | None = None
    produces: Any = None
    reads: Any = None
    loop: str | None = None
    when: str | None = None
    reviewer: str | None = None
    parallel: list[str] | None = None
    guardrails: list[str] = Field(default_factory=list)
    rule: str | None = None
    gate: str | None = None
    must_be: str | None = None
    ref_pipeline: str | None = None
    ref: str | None = None
    action: str | None = None
    actions: list[str] | None = None

    @property
    def is_ai(self) -> bool:
        return self.kind is StepKind.agent

    @property
    def is_composite_ref(self) -> bool:
        """True for a composite pipeline's `{id, ref: <pipeline-id>}` step — no kind of its own."""
        return self.kind is None and self.ref is not None


class PipelineInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    required: bool = False
    default: Any = None
    note: str | None = None


class Trigger(BaseModel):
    ui_action: str
    slash_command: str | None = None


class Pipeline(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    trigger: Trigger
    description: str
    inputs: list[PipelineInput] = Field(default_factory=list)
    preconditions: dict | None = None
    guardrails: list[str] = Field(default_factory=list)
    steps: list[Step] = Field(default_factory=list)
    definition_of_done: str | None = None

    def agent_steps(self) -> list[Step]:
        return [s for s in self.steps if s.kind is StepKind.agent]

    def ai_density(self) -> dict[str, int]:
        """cli/agent/human/gate step counts — what the AI Boundary Map table hand-built.

        Composite-ref steps (`{id, ref: <other-pipeline-id>}`, no kind of their own) are counted
        separately under `composite_ref`, not folded into one of the four real kinds — they
        aren't a step this pipeline does itself, they're "go run that whole other pipeline."
        """
        counts = {k.value: 0 for k in StepKind}
        counts["composite_ref"] = 0
        for s in self.steps:
            if s.is_composite_ref:
                counts["composite_ref"] += 1
            elif s.kind is not None:
                counts[s.kind.value] += 1
        return counts


class Guardrail(BaseModel):
    id: str
    rule: str


class PipelineIndexEntry(BaseModel):
    id: str
    file: str
    ui_action: str
    slash_command: str | None = None


class GuardrailReferenceError(RuntimeError):
    """A pipeline or step names a guardrail id that isn't declared in _shared.yaml."""


def load_shared_guardrails() -> list[Guardrail]:
    path = PIPELINES_ROOT / "_shared.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"No _shared.yaml under {PIPELINES_ROOT}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [Guardrail(**g) for g in data.get("shared_guardrails", [])]


def load_pipeline_index() -> list[PipelineIndexEntry]:
    path = PIPELINES_ROOT / "index.yaml"
    if not path.is_file():
        raise FileNotFoundError(
            f"No index.yaml under {PIPELINES_ROOT}. Set TESTOPS_CLAUDE_ROOT to point at a real "
            f"testops/.claude checkout (the sandbox's own Platform/testops/ copy is stale and "
            f"doesn't have .claude/pipelines/ yet)."
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [PipelineIndexEntry(**e) for e in data.get("pipelines", [])]


def load_pipeline(pipeline_id: str) -> Pipeline:
    index = {e.id: e for e in load_pipeline_index()}
    entry = index.get(pipeline_id)
    if entry is None:
        raise KeyError(f"Unknown pipeline id '{pipeline_id}'. Known: {sorted(index)}")
    path = PIPELINES_ROOT / entry.file
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Pipeline(**data)


def load_all_pipelines() -> list[Pipeline]:
    return [load_pipeline(e.id) for e in load_pipeline_index()]


def route(ui_action: str) -> Pipeline:
    """The literal call a UI button click makes: this ui_action -> the full Pipeline to run."""
    index = load_pipeline_index()
    entry = next((e for e in index if e.ui_action == ui_action), None)
    if entry is None:
        raise KeyError(
            f"No pipeline registered for ui_action '{ui_action}'. Known actions: "
            f"{sorted(e.ui_action for e in index)}"
        )
    return load_pipeline(entry.id)


def validate_guardrail_references() -> list[str]:
    """Every guardrail id any pipeline/step names must exist in _shared.yaml. Returns the list
    of dangling references — empty means clean. Catches the class of bug where a pipeline file
    is edited to reference a guardrail that was renamed or never declared."""
    known = {g.id for g in load_shared_guardrails()}
    problems: list[str] = []
    for p in load_all_pipelines():
        for gid in p.guardrails:
            if gid not in known:
                problems.append(f"{p.id}: unknown guardrail '{gid}'")
        for s in p.steps:
            for gid in s.guardrails:
                if gid not in known:
                    problems.append(f"{p.id}.{s.id}: unknown guardrail '{gid}'")
    return problems


def ai_density_report() -> dict[str, dict[str, int]]:
    """pipeline id -> {cli, agent, human, gate} counts, derived from the real files — the same
    shape as the AI Boundary Map artifact's hand-built "Every pipeline, by AI-density" table."""
    return {p.id: p.ai_density() for p in load_all_pipelines()}
