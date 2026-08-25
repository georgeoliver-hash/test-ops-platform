"""Extract layout-XML structure from an Android APK.

Each entry in `res/layout*/*.xml` is binary AXML; we decode it via androguard
and record, per view, the tag, id, and any user-visible text/hint/description
references. The resulting JSON lets a test author work backward from a string
("Login.button_log_in") to the layouts that reference it ("login_screen.xml")
to the navigation flow that reaches that screen.

Usage:
    python tools/extract_apk_layouts.py <apk> -o artifacts/pos_apk_layouts.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"
APP_NS_RE = re.compile(r"^\{http://schemas\.android\.com/apk/res-auto\}")

INTERESTING_ATTRS = {
    "id": ANDROID_NS + "id",
    "text": ANDROID_NS + "text",
    "hint": ANDROID_NS + "hint",
    "content_description": ANDROID_NS + "contentDescription",
    "tag": ANDROID_NS + "tag",
    "src": ANDROID_NS + "src",
}


def _silence_androguard() -> None:
    from loguru import logger
    logger.remove()


_RAW_REF_RE = re.compile(r"^[@?](0x)?([0-9A-Fa-f]{6,8})$")


class Resolver:
    """Resolves raw resource numbers (e.g. '@7F040014') back to type/name pairs."""

    def __init__(self, arsc: Any, package: str):
        self._arsc = arsc
        self._pkg = package
        self._cache: dict[int, tuple[str, str] | None] = {}

    def lookup(self, rid: int) -> tuple[str, str] | None:
        if rid in self._cache:
            return self._cache[rid]
        try:
            entry = self._arsc.get_id(self._pkg, rid)
        except Exception:
            entry = None
        if entry and len(entry) >= 2 and entry[0] and entry[1]:
            result = (entry[0], entry[1])
        else:
            result = None
        self._cache[rid] = result
        return result


def _parse_raw_ref(value: str) -> int | None:
    m = _RAW_REF_RE.match(value)
    if not m:
        return None
    try:
        return int(m.group(2), 16)
    except ValueError:
        return None


def _strip_id_ref(value: str, resolver: Resolver | None) -> str:
    if value.startswith("@+id/") or value.startswith("@id/"):
        return value.split("/", 1)[1]
    if value.startswith("@android:id/"):
        return "android:" + value.split("/", 1)[1]
    if resolver is not None:
        rid = _parse_raw_ref(value)
        if rid is not None:
            entry = resolver.lookup(rid)
            if entry and entry[0] == "id":
                return entry[1]
    return value


def _classify_text(value: str, resolver: Resolver | None) -> dict[str, str]:
    if value.startswith("@string/"):
        return {"kind": "string_ref", "name": value.removeprefix("@string/")}
    if resolver is not None and (value.startswith("@") or value.startswith("?")):
        rid = _parse_raw_ref(value)
        if rid is not None:
            entry = resolver.lookup(rid)
            if entry:
                rtype, rname = entry
                if rtype == "string":
                    return {"kind": "string_ref", "name": rname}
                return {"kind": "ref", "type": rtype, "name": rname}
    if value.startswith("@") and "/" in value:
        return {"kind": "ref", "value": value}
    return {"kind": "literal", "value": value}


def _summarise_view(elem: ET.Element, resolver: Resolver | None) -> dict[str, Any]:
    summary: dict[str, Any] = {"tag": elem.tag}
    raw_id = elem.get(INTERESTING_ATTRS["id"])
    if raw_id:
        summary["id"] = _strip_id_ref(raw_id, resolver)
    for attr_name in ("text", "hint", "content_description", "tag", "src"):
        raw = elem.get(INTERESTING_ATTRS[attr_name])
        if raw:
            summary[attr_name] = _classify_text(raw, resolver)
    return summary


def _walk(elem: ET.Element, *, resolver: Resolver | None, depth: int = 0) -> list[dict[str, Any]]:
    rows = [{"depth": depth, **_summarise_view(elem, resolver)}]
    for child in elem:
        rows.extend(_walk(child, resolver=resolver, depth=depth + 1))
    return rows


def extract(apk_path: Path) -> dict[str, Any]:
    _silence_androguard()
    from androguard.core import axml
    from androguard.core.apk import APK

    apk = APK(str(apk_path))
    arsc = apk.get_android_resources()
    pkg_names = arsc.get_packages_names() if arsc is not None else []
    resolver = Resolver(arsc, pkg_names[0]) if (arsc is not None and pkg_names) else None

    layouts: dict[str, list[dict[str, Any]]] = {}
    string_index: dict[str, list[str]] = {}

    for filename in apk.get_files():
        if not filename.startswith("res/layout"):
            continue
        if not filename.endswith(".xml"):
            continue
        try:
            raw = apk.get_file(filename)
            printer = axml.AXMLPrinter(raw)
            xml_text = printer.get_xml()
        except Exception as e:
            layouts[filename] = [{"_error": f"{type(e).__name__}: {e}"}]
            continue
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            layouts[filename] = [{"_error": f"ParseError: {e}"}]
            continue

        rows = _walk(root, resolver=resolver)
        layouts[filename] = rows

        for row in rows:
            for attr in ("text", "hint", "content_description"):
                ref = row.get(attr)
                if isinstance(ref, dict) and ref.get("kind") == "string_ref":
                    name = ref["name"]
                    string_index.setdefault(name, [])
                    if filename not in string_index[name]:
                        string_index[name].append(filename)

    return {
        "package": apk.get_package(),
        "version_name": apk.get_androidversion_name(),
        "layout_count": len(layouts),
        "layouts": layouts,
        "string_to_layouts": {k: sorted(v) for k, v in sorted(string_index.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.apk.is_file():
        print(f"not a file: {args.apk}", file=sys.stderr)
        return 1

    metadata = extract(args.apk)
    args.output.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    indexed = sum(1 for v in metadata["layouts"].values() if not (len(v) == 1 and "_error" in v[0]))
    print(
        f"wrote {args.output} — {metadata['layout_count']} layouts ({indexed} indexed), "
        f"{len(metadata['string_to_layouts'])} strings cross-referenced"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
