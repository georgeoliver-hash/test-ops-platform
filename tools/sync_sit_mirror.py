"""Refresh sit-mirror/ from a local flowbird-group/sit checkout.

One-way mirror only: this script READS from a local `sit` clone and WRITES into
`sit-mirror/` in this repo. It never writes back to the `sit` checkout, and this
repo never opens a PR against flowbird-group/sit on its own — see
docs/sync-policy.md for the full rule.

Usage:
    python tools/sync_sit_mirror.py --sit-path ../sit

Mirrors exactly three things (the schema this platform reuses, not the whole repo):
  - Resources/Common/ConfigSets/<Project>/<ver>/EquipmentTypes.json          (device taxonomy)
  - Resources/Devices/**/Bindings/*.robot                                    (function keywords)
  - Resources/Common/ConfigSets/<Project>/<ver>/ScreenFlow/<Device>/**       (screen graphs,
    screenflow_map.jsonc + Templates/*.json + element_queries.json) — added when model/flows.py
    needed a real source to parse instead of a guessed schema. Same directory tree the
    EquipmentTypes.json glob already walks, so this isn't a scope creep, just the sibling data.

Writes sit-mirror/_sync_manifest.json recording the source commit hash + date, so a
stale mirror is always detectable rather than silently out of date.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

MIRROR_ROOT = Path(__file__).resolve().parent.parent / "sit-mirror"


def _git_head_info(sit_path: Path) -> dict:
    commit = subprocess.run(
        ["git", "-C", str(sit_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    commit_date = subprocess.run(
        ["git", "-C", str(sit_path), "log", "-1", "--format=%cI"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    remote = subprocess.run(
        ["git", "-C", str(sit_path), "remote", "get-url", "origin"],
        capture_output=True, text=True,
    ).stdout.strip() or "unknown"
    return {"commit": commit, "commit_date": commit_date, "remote": remote}


def sync_equipment_types(sit_path: Path) -> list[str]:
    src_root = sit_path / "Resources" / "Common" / "ConfigSets"
    dst_root = MIRROR_ROOT / "EquipmentTypes"
    written: list[str] = []
    if not src_root.is_dir():
        return written
    for equip_file in src_root.glob("*/*/EquipmentTypes.json"):
        project, version = equip_file.parent.parent.name, equip_file.parent.name
        dst = dst_root / project / version / "EquipmentTypes.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(equip_file, dst)
        written.append(str(dst.relative_to(MIRROR_ROOT)))
    return written


def sync_bindings(sit_path: Path) -> list[str]:
    src_root = sit_path / "Resources" / "Devices"
    dst_root = MIRROR_ROOT / "Bindings"
    written: list[str] = []
    if not src_root.is_dir():
        return written
    for binding_file in src_root.glob("**/Bindings/*.robot"):
        rel = binding_file.relative_to(src_root)
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(binding_file, dst)
        written.append(str(dst.relative_to(MIRROR_ROOT)))
    return written


def sync_screenflows(sit_path: Path) -> list[str]:
    """Mirror every ScreenFlow/<Device>/ dir verbatim: screenflow_map.jsonc, Templates/*.json,
    element_queries.json — whatever exists (not every project/device has one yet)."""
    src_root = sit_path / "Resources" / "Common" / "ConfigSets"
    dst_root = MIRROR_ROOT / "ScreenFlow"
    written: list[str] = []
    if not src_root.is_dir():
        return written
    for screenflow_dir in src_root.glob("*/*/ScreenFlow/*"):
        if not screenflow_dir.is_dir():
            continue
        project, config_version, _screenflow, device = screenflow_dir.relative_to(src_root).parts
        for f in screenflow_dir.rglob("*"):
            if not f.is_file():
                continue
            dst = dst_root / project / config_version / device / f.relative_to(screenflow_dir)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
            written.append(str(dst.relative_to(MIRROR_ROOT)))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sit-path", required=True, help="Path to a local flowbird-group/sit checkout")
    args = parser.parse_args()

    sit_path = Path(args.sit_path).resolve()
    if not sit_path.is_dir():
        raise SystemExit(f"--sit-path does not exist: {sit_path}")

    equip_written = sync_equipment_types(sit_path)
    bindings_written = sync_bindings(sit_path)
    screenflow_written = sync_screenflows(sit_path)

    manifest = {
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(sit_path),
        **_git_head_info(sit_path),
        "equipment_types_files": len(equip_written),
        "bindings_files": len(bindings_written),
        "screenflow_files": len(screenflow_written),
        "note": (
            "One-way mirror. Regenerate by re-running this script against a fresh "
            "sit checkout — never hand-edit files under sit-mirror/."
        ),
    }
    (MIRROR_ROOT / "_sync_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    print(f"EquipmentTypes.json files mirrored: {len(equip_written)}")
    print(f"Bindings/*.robot files mirrored:    {len(bindings_written)}")
    print(f"ScreenFlow files mirrored:           {len(screenflow_written)}")
    print(f"Source commit: {manifest['commit'][:12]} ({manifest['commit_date']})")
    print(f"Manifest written to {MIRROR_ROOT / '_sync_manifest.json'}")


if __name__ == "__main__":
    main()
