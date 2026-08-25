"""Deterministic markdown renderers for the JSON baselines.

These give a human a quick eyeball of the raw data. The richer, consolidated
report (covered/missing verdicts, recommendations) is written by the agents.
"""

from __future__ import annotations

from system_test_ops.models import CasesBaseline, RunHealthReport


def render_cases_baseline(baseline: CasesBaseline) -> str:
    lines = [
        f"# Cases — {baseline.project} / {baseline.suite or 'suite ' + str(baseline.suite_id)}",
        "",
        f"- Generated: {baseline.generated_at.isoformat()}",
        f"- Total cases: {len(baseline.cases)}",
        "",
        "| Case | Title | Section | Linked refs | Has steps |",
        "|---|---|---|---|---|",
    ]
    for c in baseline.cases:
        refs = ", ".join(c.refs) if c.refs else "—"
        steps = "yes" if c.custom_steps else "no"
        section = c.section_path or "—"
        title = c.title.replace("|", "\\|")
        lines.append(f"| {c.cite} | {title} | {section} | {refs} | {steps} |")
    return "\n".join(lines) + "\n"


def _flags(h) -> str:  # noqa: ANN001 - TestHealth
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
    return ", ".join(flags) if flags else "—"


def render_run_health(report: RunHealthReport) -> str:
    flagged = [
        h
        for h in report.cases
        if h.orphaned or h.never_executed or h.always_failing or h.flaky or h.recently_regressed
    ]
    lines = [
        f"# Run health — {report.project} / {report.suite}",
        "",
        f"- Generated: {report.generated_at.isoformat()}",
        f"- Runs considered (last {report.last_n}): {len(report.run_ids)} "
        + (f"(run ids: {', '.join(map(str, report.run_ids))})" if report.run_ids else ""),
        f"- Cases tracked: {len(report.cases)}",
        f"- **Flagged for attention: {len(flagged)}**",
        "",
        "## Flagged cases",
        "",
        "| Case | Title | Exec | Pass | Fail | Block | Last | Flags |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for h in sorted(flagged, key=lambda x: (not x.always_failing, not x.recently_regressed, x.case_id)):
        title = (h.title or "").replace("|", "\\|")
        lines.append(
            f"| {h.cite} | {title} | {h.executed_count} | {h.passed} | {h.failed} | "
            f"{h.blocked} | {h.last_status_label or '—'} | {_flags(h)} |"
        )
    if not flagged:
        lines.append("| — | _no cases flagged across the window_ | | | | | | |")
    return "\n".join(lines) + "\n"
