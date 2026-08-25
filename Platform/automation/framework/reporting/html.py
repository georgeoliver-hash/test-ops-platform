"""Self-contained HTML run report.

One `index.html` per run, written at session finish. Contents:

- run header: date, time, *why it was run* (run reason), project, marker
  expression, full run command, and pass/fail/skip/error counts;
- a colour-coded results table (failures first), each row linking to the
  per-test `report.md`;
- a JIRA-style defect block for every failed/errored test, with the evidence
  files listed and linked.

No external dependencies and no network — a single file that opens anywhere.
Kept separate from the markdown renderer so each can evolve independently.
"""
from __future__ import annotations

import html
from pathlib import Path

from .defect import build_defect
from .report import TestReport

_STATUS_COLOUR = {
    "passed": "#1a7f37",
    "failed": "#cf222e",
    "error": "#bc4c00",
    "skipped": "#6e7781",
    "pending": "#6e7781",
}

_CSS = """
:root { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
body { margin: 0; background: #f6f8fa; color: #1f2328; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 24px; }
h1 { font-size: 22px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 28px 0 10px; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; }
.meta { background: #fff; border: 1px solid #d0d7de; border-radius: 8px; padding: 16px 20px; }
.meta dl { display: grid; grid-template-columns: 160px 1fr; gap: 6px 14px; margin: 0; }
.meta dt { color: #57606a; font-weight: 600; }
.meta dd { margin: 0; }
.counts { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0 0; }
.pill { border-radius: 999px; padding: 4px 14px; font-weight: 700; color: #fff; font-size: 14px; }
table { border-collapse: collapse; width: 100%; background: #fff; border: 1px solid #d0d7de; border-radius: 8px; overflow: hidden; }
th, td { text-align: left; padding: 9px 12px; border-bottom: 1px solid #eaeef2; font-size: 14px; }
th { background: #f6f8fa; color: #57606a; }
tr:last-child td { border-bottom: none; }
.badge { display: inline-block; min-width: 64px; text-align: center; border-radius: 6px; padding: 2px 8px; color: #fff; font-weight: 700; font-size: 12px; text-transform: uppercase; }
code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px; overflow-x: auto; font-size: 12.5px; }
.defect { background: #fff; border: 1px solid #d0d7de; border-left: 4px solid #cf222e; border-radius: 8px; padding: 16px 20px; margin: 14px 0; }
.defect h3 { margin: 0 0 10px; font-size: 15px; }
.defect .labels span { background: #ddf4ff; color: #0969da; border-radius: 999px; padding: 2px 10px; font-size: 12px; margin-right: 6px; }
.mono-small { font-size: 12px; color: #57606a; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
"""


def _esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def _counts_pills(counts: dict[str, int]) -> str:
    out = []
    for k in ("passed", "failed", "error", "skipped"):
        n = counts.get(k, 0)
        if n:
            out.append(
                f'<span class="pill" style="background:{_STATUS_COLOUR[k]}">'
                f"{n} {k}</span>"
            )
    return '<div class="counts">' + "".join(out) + "</div>"


def _results_table(reports: list[TestReport], run_root: Path) -> str:
    rows = []
    for r in reports:
        try:
            rel = r.report_dir.relative_to(run_root).as_posix()
            link = f'<a href="./{rel}/report.md">{_esc(r.nodeid)}</a>'
        except ValueError:
            link = _esc(r.nodeid)
        colour = _STATUS_COLOUR.get(r.status, "#6e7781")
        rows.append(
            "<tr>"
            f'<td><span class="badge" style="background:{colour}">{_esc(r.status)}</span></td>'
            f"<td>{link}</td>"
            f"<td>{r.duration_seconds:.2f}s</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Status</th><th>Test</th><th>Duration</th></tr></thead>"
        "<tbody>" + "".join(rows) + "</tbody></table>"
    )


def _defect_block(report: TestReport, run_root: Path) -> str:
    defect = build_defect(report)
    if defect is None:
        return ""
    labels = "".join(f"<span>{_esc(l)}</span>" for l in defect.labels)
    evidence_links = []
    for e in defect.evidence:
        try:
            rel = e.relative_to(run_root).as_posix()
            evidence_links.append(f'<li><a href="./{rel}">{_esc(e.name)}</a></li>')
        except ValueError:
            evidence_links.append(f"<li>{_esc(e.name)}</li>")
    evidence_html = (
        f"<p class='mono-small'>Evidence:</p><ul>{''.join(evidence_links)}</ul>"
        if evidence_links
        else ""
    )
    return (
        '<div class="defect">'
        f"<h3>{_esc(defect.summary)}</h3>"
        f'<p class="labels">{labels}'
        f'<span style="background:#ffebe9;color:#cf222e">priority: {_esc(defect.priority)}</span></p>'
        f"<pre>{_esc(defect.description)}</pre>"
        f"{evidence_html}"
        "</div>"
    )


def render_run_html(run_meta: dict, reports: list[TestReport], run_root: Path) -> str:
    """Build the full run report HTML. `run_meta` carries date/time/reason/
    project/command; `reports` is every TestReport from the session."""

    def order(r: TestReport) -> tuple[int, str]:
        rank = {"failed": 0, "error": 1, "passed": 2, "skipped": 3, "pending": 4}
        return (rank.get(r.status, 9), r.nodeid)

    reports = sorted(reports, key=order)
    counts: dict[str, int] = {}
    for r in reports:
        counts[r.status] = counts.get(r.status, 0) + 1

    failures = [r for r in reports if r.status in ("failed", "error")]

    meta_rows = [
        ("Run date (UTC)", run_meta.get("date", "")),
        ("Run time (UTC)", run_meta.get("time", "")),
        ("Why it was run", run_meta.get("reason") or "_(not specified — pass --run-reason)_"),
        ("Project", run_meta.get("project") or "_(PROJECT not set)_"),
        ("Marker filter", run_meta.get("marker_expr") or "(none)"),
        ("Command", run_meta.get("command", "")),
        ("Total tests", str(len(reports))),
    ]
    dl = "".join(
        f"<dt>{_esc(k)}</dt><dd>{_esc(v)}</dd>" for k, v in meta_rows
    )

    defect_section = ""
    if failures:
        blocks = "".join(_defect_block(r, run_root) for r in failures)
        defect_section = (
            f"<h2>Defect raises ({len(failures)})</h2>"
            "<p class='mono-small'>One JIRA-ready defect per failed/errored test. "
            "Files also written as <code>defect.md</code> beside each test, and "
            "collected in <code>defects.json</code> for pushing via the Atlassian MCP.</p>"
            + blocks
        )

    title = f"Test run — {run_meta.get('date', '')} {run_meta.get('time', '')}"
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{_esc(title)}</title><style>{_CSS}</style></head><body><div class='wrap'>"
        f"<h1>{_esc(title)}</h1>"
        f'<div class="meta"><dl>{dl}</dl>{_counts_pills(counts)}</div>'
        "<h2>Results</h2>"
        f"{_results_table(reports, run_root)}"
        f"{defect_section}"
        "</div></body></html>"
    )
