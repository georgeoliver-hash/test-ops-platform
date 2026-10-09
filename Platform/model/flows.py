"""Screen/path model — two real, differently-shaped sources, deliberately NOT joined yet.

  - **ScreenGraph** — a thin, faithful parse of SIT's own automated screenflow discovery output
    (`sit-mirror/ScreenFlow/<Project>/<ver>/<Device>/screenflow_map.jsonc`, plus its `Templates/`
    and `element_queries.json`). Mechanical: every screen and transition SIT actually walked,
    16 distinct transition `Type` values observed in real files (UI_Key, Stages, UI_Click,
    MADT_SignOn, Smartcard_Present, ... — deliberately not narrowed to a closed enum, since new
    types appear as SIT covers more devices). No "candidate scenario" judgement in here at all.

  - **FlowMap** — a parse of testops's hand/AI-transcribed `knowledge/flows/<project>-<device>*.md`
    paths table (`# | Path | Feature | Tags | Covered by`). This is curated: a human decided what
    counts as one candidate scenario, tagged it with a feature, and (once `/audit-flows` has run)
    resolved which TestRail case(s) cover it.

These are NOT reconciled into one join here. The Foundation Plan's Section 06 observation —
"the paths table should not be authored at all, enumerating paths through a graph is a
computation" — is a real future direction, not something to fake today: SIT's screenflow graph is
the exhaustive mechanical transition set, testops's paths table is a curated, feature-tagged,
coverage-annotated subset, and no device today has both built from a *shared* vocabulary of
screen names (spot-check the two against Translink POS below — they don't line up 1:1 as-is).
Building a resolver that walks ScreenGraph and reproduces FlowMap's paths is real, scoped work,
not a one-line join — leave it for the phase that actually needs it.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from pydantic import BaseModel, Field

from model.provenance import Citation


# --------------------------------------------------------------------------- #
# ScreenGraph — mechanical, from SIT's own screenflow discovery output
# --------------------------------------------------------------------------- #
def _default_screenflow_root() -> Path:
    override = os.environ.get("SIT_SCHEMA_ROOT")
    if override:
        return Path(override) / "ScreenFlow"
    # Sandbox layout: Platform/model/flows.py -> repo root -> sit-mirror/ScreenFlow
    return Path(__file__).resolve().parent.parent.parent / "sit-mirror" / "ScreenFlow"


SCREENFLOW_ROOT = _default_screenflow_root()


def _live_sit_configsets() -> Path | None:
    """The real sit checkout's ConfigSets (sit keeps screen flows at ConfigSets/<Project>/<ver>/ScreenFlow/<Device>/).
    George, 2026-10-09: screen flows must come from the source of truth, not a point-in-time mirror -- so a local sit
    checkout (TESTOPS_SIT_ROOT, else the sibling ../sit) wins; sit-mirror/ is only the fallback."""
    root = Path(os.environ.get("TESTOPS_SIT_ROOT") or Path(__file__).resolve().parents[3] / "sit")
    cs = root / "Resources" / "Common" / "ConfigSets"
    return cs if cs.is_dir() else None


LIVE_CONFIGSETS = _live_sit_configsets()


def _graph_dir(project: str, config_version: str, device_type: str) -> Path:
    if LIVE_CONFIGSETS is not None:
        d = LIVE_CONFIGSETS / project / config_version / "ScreenFlow" / device_type
        if (d / "screenflow_map.jsonc").is_file():
            return d
    return SCREENFLOW_ROOT / project / config_version / device_type

_STRING_OR_COMMENT = re.compile(r'"(?:\\.|[^"\\])*"|(//.*)$', re.MULTILINE)


def _strip_jsonc_comments(text: str) -> str:
    """screenflow_map.jsonc allows // line comments — bare json.loads chokes on them.

    Matches a full quoted string OR a trailing // comment at each position, alternation-
    first — a `//` that's actually inside a string value never reaches the comment branch,
    since the string alternative consumes it first. A prior version only matched comments
    that start a line (`^\\s*//`), missing the equally real trailing-comment case (e.g.
    `"StaffPin": "...",  // TODO`) — found via Translink/BV's screenflow_map.jsonc, which
    that shape broke on (json.decoder.JSONDecodeError), 2026-09-09.
    """
    return _STRING_OR_COMMENT.sub(lambda m: "" if m.group(1) else m.group(0), text)


class NavigationAction(BaseModel):
    """One raw action step inside a `Stages` transition — kept verbatim, not reshaped."""

    type: str
    extra: dict = Field(default_factory=dict)  # every other key from the source action, verbatim


class ScreenTransition(BaseModel):
    """One `Navigable_screens` entry: from_screen -> to_screen, however SIT triggers it.

    `type` is one of 16+ real values seen across SIT's screenflow maps (UI_Key, UI_Click,
    Stages, MADT_SignOn, Smartcard_Present, JS_Navigate, ...) — intentionally not a closed enum.
    `keys`/`actions` cover the two most common shapes (UI_Key, Stages); anything else lands
    in `extra` verbatim rather than being silently dropped.
    """

    from_screen: str
    to_screen: str
    type: str
    keys: str | None = None
    actions: list[NavigationAction] = Field(default_factory=list)
    extra: dict = Field(default_factory=dict)


class ScreenTemplate(BaseModel):
    """One screen's element-matching template (`Templates/<Screen>.json`) — kept as-is."""

    screen: str
    attributes: dict = Field(default_factory=dict)
    elements: list[dict] = Field(default_factory=list)  # [{Name, Type, Text?}], raw


class ScreenGraph(BaseModel):
    """One device's mechanical screen-transition graph, straight from SIT's own discovery output."""

    project: str
    config_version: str
    device_type: str
    source_path: str  # relative path under sit-mirror/, for provenance
    presets: dict = Field(default_factory=dict)
    screens: list[str] = Field(default_factory=list)  # screen names, file order preserved
    transitions: list[ScreenTransition] = Field(default_factory=list)
    templates: dict[str, ScreenTemplate] = Field(default_factory=dict)  # screen -> template
    element_map: dict[str, dict] = Field(default_factory=dict)  # logical name -> {Name, Type}

    def transitions_from(self, screen: str) -> list[ScreenTransition]:
        return [t for t in self.transitions if t.from_screen == screen]

    def citation(self) -> Citation:
        return Citation(source_kind="sit_screenflow", source_ref=self.source_path)


def available_screen_graphs(project: str, config_version: str = "1") -> list[str]:
    """Device types that actually have a screenflow_map.jsonc for this project/version — not
    every device does, so callers should check this (or catch the FileNotFoundError below)
    rather than assume."""
    found = set()
    for root in ([LIVE_CONFIGSETS / project / config_version / "ScreenFlow"] if LIVE_CONFIGSETS is not None else []) + [SCREENFLOW_ROOT / project / config_version]:
        if root.is_dir():
            found |= {p.name for p in root.iterdir() if (p / "screenflow_map.jsonc").is_file()}
    return sorted(found)


def load_screen_graph(project: str, device_type: str, config_version: str = "1") -> ScreenGraph:
    """Parse one device's screenflow_map.jsonc (+ Templates/, + element_queries.json if present).

    Raises FileNotFoundError if this project/device/version has no screenflow map — a missing
    screen graph is a real, nameable gap (most devices don't have one yet), not something to
    silently return empty for. Check `available_screen_graphs()` first if the caller needs to
    branch on availability rather than fail.
    """
    base = _graph_dir(project, config_version, device_type)
    map_path = base / "screenflow_map.jsonc"
    if not map_path.is_file():
        available = available_screen_graphs(project, config_version)
        raise FileNotFoundError(
            f"No screenflow_map.jsonc for {project}/{config_version}/{device_type} under "
            f"{SCREENFLOW_ROOT}. Devices with one for this project/version: {available or '(none)'}"
        )
    data = json.loads(_strip_jsonc_comments(map_path.read_text(encoding="utf-8")))

    screens: list[str] = []
    transitions: list[ScreenTransition] = []
    for screen_name, screen in (data.get("Screens") or {}).items():
        screens.append(screen_name)
        for target, nav in (screen.get("Navigable_screens") or {}).items():
            nav = dict(nav)
            nav_type = nav.pop("Type", "")
            keys = nav.pop("Keys", None)
            raw_actions = nav.pop("Actions", None) or []
            actions = [
                NavigationAction(type=a.get("Type", ""), extra={k: v for k, v in a.items() if k != "Type"})
                for a in raw_actions
            ]
            transitions.append(
                ScreenTransition(
                    from_screen=screen_name, to_screen=target, type=nav_type,
                    keys=keys, actions=actions, extra=nav,  # whatever's left, verbatim
                )
            )

    templates: dict[str, ScreenTemplate] = {}
    templates_dir = base / "Templates"
    if templates_dir.is_dir():
        for tpl_file in templates_dir.glob("*.json"):
            tpl = json.loads(tpl_file.read_text(encoding="utf-8"))
            templates[tpl_file.stem] = ScreenTemplate(
                screen=tpl_file.stem,
                attributes=tpl.get("Attributes", {}),
                elements=tpl.get("Elements", []),
            )

    element_map: dict[str, dict] = {}
    eq_path = base / "element_queries.json"
    if eq_path.is_file():
        raw = json.loads(eq_path.read_text(encoding="utf-8"))
        element_map = {k: v for k, v in raw.items() if not k.startswith("_")}

    return ScreenGraph(
        project=project, config_version=config_version, device_type=device_type,
        source_path=(("sit/" + str(map_path.relative_to(LIVE_CONFIGSETS.parents[2])).replace("\\", "/"))
                     if LIVE_CONFIGSETS is not None and LIVE_CONFIGSETS in map_path.parents
                     else str(map_path.relative_to(SCREENFLOW_ROOT.parent))),
        presets=data.get("Presets", {}), screens=screens, transitions=transitions,
        templates=templates, element_map=element_map,
    )


# --------------------------------------------------------------------------- #
# FlowMap — curated, from testops's knowledge/flows/*.md paths table
# --------------------------------------------------------------------------- #
_PATHS_HEADER = re.compile(r"^\|\s*#\s*\|\s*Path\s*\|\s*Feature\s*\|\s*Tags\s*\|\s*Covered by\s*\|", re.M)
_TABLE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", re.M
)
_CASE_ID = re.compile(r"\d+")


class FlowPath(BaseModel):
    """One row of a knowledge/flows/*.md paths table — a human-curated candidate scenario."""

    path_id: int
    description: str
    feature: str | None = None
    tags: str | None = None
    covered_by: list[int] = Field(default_factory=list)  # empty if the cell is "?" or a gap marker
    covered_by_raw: str = ""  # verbatim cell text — "?" / "4099989" / "GAP: ..." never discarded
    source_path: str

    def citation(self) -> Citation:
        return Citation(source_kind="flow_map", source_ref=f"{self.source_path}#path-{self.path_id}")


class FlowMap(BaseModel):
    """One device's curated flow map — every path testops's transcription pass identified."""

    source_path: str
    paths: list[FlowPath] = Field(default_factory=list)

    def uncovered(self) -> list[FlowPath]:
        return [p for p in self.paths if not p.covered_by]


def load_flow_map(path: Path) -> FlowMap:
    """Parse the `## Paths` table out of one knowledge/flows/<project>-<device>*.md file.

    Per knowledge/flows/README.md's template, the table is always `| # | Path | Feature | Tags |
    Covered by |` — this parses exactly that shape and nothing else (the Mermaid diagram and
    Screen states/Notes sections are for a human/agent to read, not modelled here).
    """
    text = path.read_text(encoding="utf-8")
    if not _PATHS_HEADER.search(text):
        return FlowMap(source_path=str(path), paths=[])
    # Only the Paths section — stop at the next "## " heading so Screen states/Notes rows
    # (which are bullet lists, not tables, but be defensive) never get mistaken for path rows.
    after_header = text[_PATHS_HEADER.search(text).end():]
    next_heading = re.search(r"^## ", after_header, re.M)
    table_text = after_header[: next_heading.start()] if next_heading else after_header

    paths: list[FlowPath] = []
    for m in _TABLE_ROW.finditer(table_text):
        path_id, description, feature, tags, covered_raw = m.groups()
        if description.strip().startswith("-") or set(description.strip()) <= {"-", " "}:
            continue  # markdown's |---|---|---| separator row
        paths.append(
            FlowPath(
                path_id=int(path_id),
                description=description,
                feature=feature or None,
                tags=tags or None,
                covered_by=[int(n) for n in _CASE_ID.findall(covered_raw)],
                covered_by_raw=covered_raw,
                source_path=str(path),
            )
        )
    return FlowMap(source_path=str(path), paths=paths)
