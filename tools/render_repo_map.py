"""Repo Map: file -> purpose -> line count, across system-test-ops + test-ops-platform.

Deterministic, no AI: "purpose" is pulled mechanically — a Python file's module docstring
first line, or a .claude/agents|commands .md file's frontmatter `description:`. Nothing is
summarised or invented. Re-run any time the repos change; it's a few hundred file reads,
not a model call. Doesn't touch sit-mirror/ (data, not scripts) or flowbird-group/sit
(not ours to inventory).

Usage:
    python tools/render_repo_map.py --system-test-ops ../system-test-ops --out repo-map.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

_DOCSTRING_FIRST_LINE = re.compile(r'^\s*(?:"""|\'\'\')\s*(.+?)\s*(?:"""|\'\'\')?\s*$')
_FRONTMATTER_DESC = re.compile(r"^description:\s*(.+)$", re.M)


def _py_purpose(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "(unreadable)"
    for line in text.splitlines():
        if not line.strip():
            continue
        m = _DOCSTRING_FIRST_LINE.match(line)
        return m.group(1) if m else "(no module docstring)"
    return "(empty file)"


def _md_purpose(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "(unreadable)"
    m = _FRONTMATTER_DESC.search(text[:2000])
    return m.group(1).strip() if m else "(no description: frontmatter)"


def _rows_for_py(root: Path, glob: str) -> list[tuple[str, str, int]]:
    rows = []
    for path in sorted(root.glob(glob)):
        if path.is_file() and path.suffix == ".py":
            loc = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
            rows.append((str(path.relative_to(root.parent)), _py_purpose(path), loc))
    return rows


def _rows_for_md(root: Path, glob: str) -> list[tuple[str, str, int]]:
    rows = []
    for path in sorted(root.glob(glob)):
        if path.is_file() and path.suffix == ".md":
            loc = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
            rows.append((str(path.relative_to(root.parent)), _md_purpose(path), loc))
    return rows


def build_sections(system_test_ops_root: Path, platform_root: Path) -> list[tuple[str, list[tuple[str, str, int]]]]:
    sections = []
    sto = system_test_ops_root
    sections.append(("system-test-ops — deterministic core (system_test_ops/)",
                      _rows_for_py(sto, "system_test_ops/**/*.py")))
    sections.append(("system-test-ops — scripts (tools/)", _rows_for_py(sto, "tools/*.py")))
    sections.append(("system-test-ops — agents (.claude/agents/)", _rows_for_md(sto, ".claude/agents/*.md")))
    sections.append(("system-test-ops — commands (.claude/commands/)", _rows_for_md(sto, ".claude/commands/*.md")))
    sections.append(("test-ops-platform — model/ schema", _rows_for_py(platform_root, "Platform/model/*.py")))
    sections.append(("test-ops-platform — scripts (tools/)", _rows_for_py(platform_root, "tools/*.py")))
    return sections


def render_markdown(sections: list[tuple[str, list[tuple[str, str, int]]]]) -> str:
    lines = [
        "# Repo Map",
        "",
        "Generated mechanically — a Python file's purpose is its module docstring's first line, "
        "an agent/command file's purpose is its `description:` frontmatter. Nothing summarised, "
        "nothing invented. Re-run `tools/render_repo_map.py` any time; it's file reads, not AI.",
        "",
    ]
    for title, rows in sections:
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_(none found)_")
            lines.append("")
            continue
        lines.append("| File | Purpose | Lines |")
        lines.append("|---|---|---|")
        for path, purpose, loc in rows:
            purpose = purpose.replace("|", "\\|")
            lines.append(f"| `{path}` | {purpose} | {loc} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system-test-ops", required=True, help="Path to a system-test-ops checkout")
    parser.add_argument("--platform", default=".", help="Path to this test-ops-platform checkout (default: cwd)")
    parser.add_argument("--out", default="repo-map.md", help="Output Markdown path")
    args = parser.parse_args()

    sections = build_sections(Path(args.system_test_ops).resolve(), Path(args.platform).resolve())
    content = render_markdown(sections)
    out_path = Path(args.out)
    out_path.write_text(content, encoding="utf-8")
    total = sum(len(rows) for _, rows in sections)
    print(f"Repo Map: {total} file(s) across {len(sections)} section(s) -> {out_path}")


if __name__ == "__main__":
    main()
