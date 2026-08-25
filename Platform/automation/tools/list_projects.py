"""List discoverable projects.

Usage:
  python -m tools.list_projects
"""
from __future__ import annotations

from framework.registry.loader import list_projects, load_project


def main() -> int:
    names = list_projects()
    if not names:
        print("(no projects with devices.yaml found)")
        return 0
    for n in names:
        proj = load_project(n)
        print(
            f"{n}: {len(proj.devices)} device(s) — {proj.description or '(no description)'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
