"""Device taxonomy — a thin, validated wrapper over SIT's EquipmentTypes.json files.

This does NOT invent a device model. `EquipmentType` fields map 1:1 onto what
<root>/EquipmentTypes/<Project>/<ver>/EquipmentTypes.json already contains. Loading raises if a
project's file is missing or malformed rather than silently returning an empty registry — a caller
should know immediately if the source is stale or unreachable.

Today (sandbox layout): <root> = sit-mirror/, a one-way synced copy — see docs/sync-policy.md.
After the planned merge into flowbird-group/sit (Platform/ nested alongside Resources/, Tests/,
Tools/): <root> becomes Resources/Common/ConfigSets/ directly — same repo, no mirror needed. Only
`_default_root()` below changes; EquipmentType/ProjectDeviceRegistry and every caller stay identical.
Override anytime with the SIT_SCHEMA_ROOT env var without touching code.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel, Field


def _default_root() -> Path:
    override = os.environ.get("SIT_SCHEMA_ROOT")
    if override:
        return Path(override)
    # Sandbox layout: Platform/model/devices.py -> repo root -> sit-mirror/
    return Path(__file__).resolve().parent.parent.parent / "sit-mirror"


MIRROR_ROOT = _default_root() / "EquipmentTypes"


class EquipmentType(BaseModel):
    """One device-type group for a project/version, e.g. Translink's "POS"."""

    device_type: str  # e.g. "POS", "ETM", "BV" — the top-level key in EquipmentTypes.json
    equipment_group_name: str  # e.g. "Point of Sale"
    equipment_type_names: list[str] = Field(default_factory=list)  # e.g. ["POS_Way6", "Axio_4av"]
    project: str
    config_version: str


class ProjectDeviceRegistry(BaseModel):
    """Every device type declared for one project/version — one EquipmentTypes.json file."""

    project: str
    config_version: str
    source_path: str  # relative path under sit-mirror/, for provenance
    equipment_types: list[EquipmentType] = Field(default_factory=list)

    def get(self, device_type: str) -> EquipmentType | None:
        return next((e for e in self.equipment_types if e.device_type == device_type), None)


def load_registry(project: str, config_version: str = "1") -> ProjectDeviceRegistry:
    """Load one project/version's device registry from the mirrored EquipmentTypes.json."""
    path = MIRROR_ROOT / project / config_version / "EquipmentTypes.json"
    if not path.is_file():
        available = sorted(p.name for p in MIRROR_ROOT.iterdir()) if MIRROR_ROOT.is_dir() else []
        raise FileNotFoundError(
            f"No mirrored EquipmentTypes.json for project={project!r} version={config_version!r} "
            f"at {path}. Available projects in sit-mirror/: {available}. "
            f"Run tools/sync_sit_mirror.py if this looks stale."
        )
    raw = json.loads(path.read_text(encoding="utf-8"))
    equipment_types = [
        EquipmentType(
            device_type=device_type,
            equipment_group_name=body["EquipmentGroupName"],
            equipment_type_names=body["EquipmentTypeNames"],
            project=project,
            config_version=config_version,
        )
        for device_type, body in raw.items()
    ]
    return ProjectDeviceRegistry(
        project=project,
        config_version=config_version,
        source_path=str(path.relative_to(MIRROR_ROOT.parent)),
        equipment_types=equipment_types,
    )


def list_mirrored_projects() -> list[str]:
    """Every project that currently has a mirrored EquipmentTypes.json, for discovery/CLI use."""
    if not MIRROR_ROOT.is_dir():
        return []
    return sorted(p.name for p in MIRROR_ROOT.iterdir() if p.is_dir())
