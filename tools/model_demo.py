"""Proves model/ actually holds real data — run after every sit-mirror/ sync.

Usage: python tools/model_demo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.devices import list_mirrored_projects, load_registry  # noqa: E402
from model.functions import find_keyword, load_all_keywords  # noqa: E402


def main() -> None:
    projects = list_mirrored_projects()
    print(f"Mirrored projects: {projects}\n")

    registry = load_registry("Translink")
    print(f"Translink device types ({registry.source_path}):")
    for et in registry.equipment_types:
        print(f"  {et.device_type:5s} ({et.equipment_group_name}): {et.equipment_type_names}")

    pos = registry.get("POS")
    assert pos is not None, "Translink registry should have a POS entry"
    print(f"\nTranslink POS equipment types: {pos.equipment_type_names}")

    keywords = load_all_keywords()
    print(f"\nTotal function keywords parsed: {len(keywords)}")
    by_family: dict[str, int] = {}
    for kw in keywords:
        by_family[kw.device_family] = by_family.get(kw.device_family, 0) + 1
    for family, count in sorted(by_family.items()):
        print(f"  {family:12s}: {count}")

    example_phrase = "the operator is signed off"
    match = find_keyword(example_phrase, keywords)
    print(f"\nResolve '{example_phrase}':")
    if match:
        print(f"  -> FOUND in {match.source_file} (device_family={match.device_family})")
    else:
        print("  -> no existing keyword matches (would need a 'needs-keyword' stub)")


if __name__ == "__main__":
    main()
