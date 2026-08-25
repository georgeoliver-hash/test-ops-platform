"""Generate a markdown catalog of POS app screens (layouts) and their strings.

Filters out AndroidX/Material support-library layouts (the `abc_*`, `mtrl_*`,
`material_*` ones) and renders only the application-specific layouts. For each
layout we list every string resource it references plus the display value, so
test authors can see at a glance which screen contains which UI text.

Usage:
    python tools/generate_screens_doc.py \\
        --layouts artifacts/pos_apk_layouts.json \\
        --strings artifacts/pos_apk_metadata.json \\
        -o docs/screens.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LIBRARY_PREFIXES = ("abc_", "mtrl_", "material_", "design_", "notification_",
                    "preference_", "select_dialog_", "support_simple_")


def is_app_layout(filename: str) -> bool:
    name = filename.removeprefix("res/layout/").removeprefix("res/layout-")
    if "/" in name:
        name = name.split("/", 1)[1]
    return not name.startswith(LIBRARY_PREFIXES)


def short_name(filename: str) -> str:
    return filename.removeprefix("res/").replace("\\", "/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layouts", type=Path, required=True)
    parser.add_argument("--strings", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    layouts_doc = json.loads(args.layouts.read_text(encoding="utf-8"))
    strings_doc = json.loads(args.strings.read_text(encoding="utf-8"))
    string_lookup = {s["name"]: s["value"] for s in strings_doc["strings"]}

    layouts = layouts_doc["layouts"]
    app_layouts = sorted(f for f in layouts if is_app_layout(f))

    lines: list[str] = []
    lines.append(f"# POS app screen catalog — `{layouts_doc['package']}` v{layouts_doc['version_name']}")
    lines.append("")
    lines.append("Generated from static APK analysis. Each entry lists the layout filename and "
                 "every `@string/...` resource referenced inside it. Layouts that set their text "
                 "purely from Xamarin/C# code (a lot of them) won't show string entries here — "
                 "you'll see them at runtime via `uiautomator dump`.")
    lines.append("")
    lines.append(f"- Total layouts in APK: **{layouts_doc['layout_count']}**")
    lines.append(f"- Application layouts (excludes androidx/material): **{len(app_layouts)}**")
    lines.append(f"- Layouts with at least one `@string` reference: "
                 f"**{sum(1 for f in app_layouts if any(_strings_in_rows(layouts[f])))}**")
    lines.append("")

    for filename in app_layouts:
        rows = layouts[filename]
        if isinstance(rows, list) and len(rows) == 1 and "_error" in rows[0]:
            continue
        string_refs = sorted(set(_strings_in_rows(rows)))
        view_count = len(rows)
        lines.append(f"## `{short_name(filename)}`")
        lines.append("")
        lines.append(f"- Views: {view_count}")
        if string_refs:
            lines.append("- Strings referenced:")
            lines.append("")
            lines.append("  | Resource | Text |")
            lines.append("  | --- | --- |")
            for name in string_refs:
                value = string_lookup.get(name, "_(not in strings index)_")
                lines.append(f"  | `{name}` | {_escape_md(value)} |")
        else:
            lines.append("- _No `@string` refs in layout — text is set programmatically._")
        lines.append("")

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.output} — {len(app_layouts)} app layouts catalogued")
    return 0


def _strings_in_rows(rows: list) -> list[str]:
    out: list[str] = []
    for row in rows:
        for attr in ("text", "hint", "content_description"):
            ref = row.get(attr) if isinstance(row, dict) else None
            if isinstance(ref, dict) and ref.get("kind") == "string_ref":
                out.append(ref["name"])
    return out


def _escape_md(value: str) -> str:
    return re.sub(r"([|\n\r])", lambda m: "\\|" if m.group(1) == "|" else " ", value)


if __name__ == "__main__":
    sys.exit(main())
