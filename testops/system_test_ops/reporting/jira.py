"""Jira-flavoured renderer (Jira wiki markup) for pasting into a ticket comment.

Mirrors the spirit of automation-tests' Jira-ready reports: same data, a format
that pastes cleanly into Jira rather than a Markdown viewer.
"""

from __future__ import annotations

from system_test_ops.models import RunHealthReport


def render_run_health_jira(report: RunHealthReport) -> str:
    flagged = [
        h
        for h in report.cases
        if h.orphaned or h.never_executed or h.always_failing or h.flaky or h.recently_regressed
    ]
    lines = [
        f"h2. Run health — {report.project} / {report.suite}",
        f"Runs considered: last {report.last_n} "
        + (f"(ids: {', '.join(map(str, report.run_ids))})" if report.run_ids else "(none found)"),
        f"Flagged for attention: *{len(flagged)}*",
        "",
        "|| Case || Title || Exec || Pass || Fail || Last || Flags ||",
    ]
    for h in flagged:
        title = (h.title or "").replace("|", "\\|")
        flags = []
        if h.orphaned:
            flags.append("orphaned")
        if h.never_executed:
            flags.append("never-executed")
        if h.always_failing:
            flags.append("always-failing")
        if h.flaky:
            flags.append("flaky")
        if h.recently_regressed:
            flags.append("recently-regressed")
        lines.append(
            f"| C{h.case_id} | {title} | {h.executed_count} | {h.passed} | {h.failed} | "
            f"{h.last_status_label or '-'} | {', '.join(flags) or '-'} |"
        )
    return "\n".join(lines) + "\n"
