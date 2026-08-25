"""Inventory the builds/ tree and print a summary of artifacts found.

Usage:
  python -m tools.scan_builds
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDS = ROOT / "builds"


def main() -> int:
    if not BUILDS.exists():
        print(f"No builds dir at {BUILDS}", file=sys.stderr)
        return 1
    for sd in sorted(BUILDS.iterdir()):
        if not sd.is_dir():
            continue
        print(f"\n[{sd.name}]")
        for entry in sorted(sd.iterdir()):
            kind = "DIR " if entry.is_dir() else "FILE"
            size = "" if entry.is_dir() else f"  {entry.stat().st_size:>10} B"
            print(f"  {kind}  {entry.name}{size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
