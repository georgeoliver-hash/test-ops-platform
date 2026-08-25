from __future__ import annotations

from pathlib import Path

import yaml

from .models import Project

PROJECTS_ROOT = Path(__file__).resolve().parents[2] / "projects"


def load_project(name: str) -> Project:
    path = PROJECTS_ROOT / name / "devices.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No registry for project '{name}' at {path}")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Project.model_validate(data)


def list_projects() -> list[str]:
    if not PROJECTS_ROOT.exists():
        return []
    return sorted(
        p.name for p in PROJECTS_ROOT.iterdir()
        if p.is_dir()
        and not p.name.startswith("_")
        and (p / "devices.yaml").exists()
    )


def load_all_projects() -> list[Project]:
    return [load_project(n) for n in list_projects()]
