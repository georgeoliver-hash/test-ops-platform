"""Scan a directory of APKs for ContentProvider declarations.

We use providers like `com.parkeon.data.eventLog` and `com.parkeon.data.configuration`
heavily for test assertions, but didn't know which APK in the bundle declares
them. This walks every `*.apk` in a directory tree, dumps each one's full
provider/service/receiver lists with authorities, and aggregates the results.

Usage:
    python tools/scan_apk_providers.py <dir> -o artifacts/bsp_inventory.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def _silence_androguard() -> None:
    from loguru import logger
    logger.remove()


def _provider_authorities(apk: Any, provider_name: str) -> list[str]:
    """Read AndroidManifest.xml binary AXML to find <provider android:authorities=...>."""
    raw_xml = apk.get_android_manifest_xml()
    if raw_xml is None:
        return []
    try:
        if isinstance(raw_xml, (bytes, bytearray)):
            root = ET.fromstring(raw_xml)
        else:
            root = ET.fromstring(ET.tostring(raw_xml))
    except (ET.ParseError, TypeError):
        return []
    out: list[str] = []
    for prov in root.iter("provider"):
        name = prov.get(ANDROID_NS + "name") or ""
        if name == provider_name:
            authorities = prov.get(ANDROID_NS + "authorities") or ""
            if authorities:
                out.extend(a.strip() for a in authorities.split(";") if a.strip())
    return out


def _scan_one(apk_path: Path) -> dict[str, Any]:
    from androguard.core.apk import APK
    apk = APK(str(apk_path))

    providers = []
    for name in apk.get_providers():
        authorities = _provider_authorities(apk, name)
        providers.append({"class": name, "authorities": authorities})

    return {
        "file": apk_path.name,
        "package": apk.get_package(),
        "version_name": apk.get_androidversion_name(),
        "providers": sorted(providers, key=lambda p: p["class"]),
        "services": sorted(apk.get_services()),
        "receivers": sorted(apk.get_receivers()),
        "permissions_declared": sorted(set(apk.get_permissions())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", type=Path, help="Directory to walk for *.apk")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.dir.is_dir():
        print(f"not a directory: {args.dir}", file=sys.stderr)
        return 1

    _silence_androguard()

    apk_paths = sorted(args.dir.rglob("*.apk"))
    if not apk_paths:
        print(f"no .apk files under {args.dir}", file=sys.stderr)
        return 1

    per_apk: list[dict[str, Any]] = []
    for path in apk_paths:
        print(f"  scanning {path.name} ...", file=sys.stderr)
        per_apk.append(_scan_one(path))

    authority_index: dict[str, list[str]] = defaultdict(list)
    for entry in per_apk:
        for prov in entry["providers"]:
            for auth in prov["authorities"]:
                authority_index[auth].append(f"{entry['package']} ({prov['class']})")

    output = {
        "scanned": len(per_apk),
        "authority_index": dict(sorted(authority_index.items())),
        "apks": per_apk,
    }

    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {args.output} — {len(per_apk)} APKs, "
          f"{len(authority_index)} unique provider authorities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
