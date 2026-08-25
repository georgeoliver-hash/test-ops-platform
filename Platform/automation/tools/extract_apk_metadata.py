"""Extract package metadata from an Android APK for use as Appium selector inputs.

Pulls activities, providers, permissions, services, receivers, and string
resources (the most useful selector input for Xamarin apps where view IDs are
auto-generated).

Usage:
    python tools/extract_apk_metadata.py <apk_path> -o <output.json>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _silence_androguard() -> None:
    from loguru import logger
    logger.remove()


def _extract_strings(apk: Any) -> list[dict[str, str]]:
    arsc = apk.get_android_resources()
    if arsc is None:
        return []
    pkg_names = arsc.get_packages_names()
    if not pkg_names:
        return []
    pkg = pkg_names[0]
    raw_xml = arsc.get_strings_resources()
    if not raw_xml:
        return []
    from lxml import etree
    try:
        if isinstance(raw_xml, bytes):
            root = etree.fromstring(raw_xml)
        else:
            root = etree.fromstring(raw_xml.encode("utf-8"))
    except etree.XMLSyntaxError:
        return []

    seen: set[str] = set()
    results: list[dict[str, str]] = []
    for resources in root.iter("resources"):
        locale = resources.get("locale", "default")
        if locale not in ("default", "", "en"):
            continue
        for s in resources.iter("string"):
            name = s.get("name") or ""
            value = (s.text or "").strip()
            if not name or name in seen:
                continue
            if not value:
                continue
            seen.add(name)
            results.append({"name": name, "value": value})
    results.sort(key=lambda r: r["name"])
    _ = pkg
    return results


def extract(apk_path: Path) -> dict[str, Any]:
    _silence_androguard()
    from androguard.core.apk import APK

    apk = APK(str(apk_path))

    activities = []
    for activity in apk.get_activities():
        filters = apk.get_intent_filters("activity", activity)
        activities.append({
            "name": activity,
            "actions": filters.get("action", []),
            "categories": filters.get("category", []),
        })

    providers = []
    for provider in apk.get_providers():
        providers.append({"name": provider})

    services = list(apk.get_services())
    receivers = list(apk.get_receivers())

    strings = _extract_strings(apk)

    return {
        "package": apk.get_package(),
        "version_name": apk.get_androidversion_name(),
        "version_code": apk.get_androidversion_code(),
        "min_sdk": apk.get_min_sdk_version(),
        "target_sdk": apk.get_target_sdk_version(),
        "main_activity": apk.get_main_activity(),
        "permissions": sorted(apk.get_permissions()),
        "activities": sorted(activities, key=lambda a: a["name"]),
        "providers": sorted(providers, key=lambda p: p["name"]),
        "services": sorted(services),
        "receivers": sorted(receivers),
        "string_count": len(strings),
        "strings": strings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path, help="Path to .apk file")
    parser.add_argument("-o", "--output", type=Path, help="Write JSON here (default stdout)")
    args = parser.parse_args()

    if not args.apk.is_file():
        print(f"not a file: {args.apk}", file=sys.stderr)
        return 1

    metadata = extract(args.apk)
    payload = json.dumps(metadata, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"wrote {args.output} ({len(payload):,} chars, {metadata['string_count']} strings)")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
