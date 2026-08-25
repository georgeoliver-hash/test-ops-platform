"""Turn a failed/errored TestReport into a JIRA-ready defect raise.

Produces two things from one `TestReport`:

- `render_markdown()` — a copy/paste defect writeup (George's existing file
  workflow: drop it into JIRA by hand, or hand it to a reviewer).
- `to_jira_fields()` — a dict shaped for the Atlassian MCP `createJiraIssue`
  tool (summary / description / labels / priority), so the same defect can be
  pushed straight into JIRA once approved.

Only `failed` and `error` tests become defects; passed/skipped do not.
The JIRA project key is read from `JIRA_PROJECT_KEY` (env) — never hard-coded.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .report import TestReport

# Status -> (JIRA priority, severity word). Errors (setup/teardown blew up)
# are treated as higher urgency than an assertion failure because the test
# couldn't even exercise the behaviour under test.
_PRIORITY = {
    "error": ("High", "Test could not run (setup/teardown error)"),
    "failed": ("Medium", "Assertion failed"),
}

# How much of the traceback to inline in the defect description. The full
# traceback always remains in the per-test report.md / attachments.
_TRACEBACK_MAX_CHARS = 1800


@dataclass
class Defect:
    """A defect raise derived from one failed/errored test."""

    summary: str
    description: str
    labels: list[str] = field(default_factory=list)
    priority: str = "Medium"
    severity: str = ""
    # Evidence files (logcat, screenshot, ui_dump, report.md) — referenced by
    # name in the description; attached to the JIRA issue in a follow-up step
    # (the MCP createJiraIssue call doesn't take attachments inline).
    evidence: list[Path] = field(default_factory=list)

    def to_jira_fields(self, project_key: str | None = None) -> dict:
        """Shape for the Atlassian MCP `createJiraIssue` tool. `project_key`
        falls back to $JIRA_PROJECT_KEY; left blank if neither is set so the
        caller is forced to fill it in rather than post to the wrong project."""
        key = project_key or os.getenv("JIRA_PROJECT_KEY", "")
        return {
            "projectKey": key,
            "issueTypeName": "Bug",
            "summary": self.summary,
            "description": self.description,
            "labels": self.labels,
            "priority": self.priority,
            # surfaced for the caller; not all JIRA projects expose these
            "_evidence_files": [str(p) for p in self.evidence],
        }

    def render_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Defect: {self.summary}")
        lines.append("")
        lines.append(f"- **Priority:** {self.priority}")
        lines.append(f"- **Severity:** {self.severity}")
        if self.labels:
            lines.append(f"- **Labels:** {', '.join(self.labels)}")
        key = os.getenv("JIRA_PROJECT_KEY", "")
        lines.append(f"- **JIRA project:** {key or '_(set JIRA_PROJECT_KEY)_'}")
        lines.append(f"- **Issue type:** Bug")
        lines.append("")
        lines.append(self.description)
        if self.evidence:
            lines.append("")
            lines.append("## Evidence to attach")
            lines.append("")
            for e in self.evidence:
                lines.append(f"- `{e.name}`")
        return "\n".join(lines)


def _short_reason(report: TestReport) -> str:
    """One-line failure reason for the defect summary — the last meaningful
    line of the traceback (usually the assertion / exception message)."""
    if report.actual:
        return report.actual.strip().splitlines()[0][:140]
    if report.longrepr:
        for line in reversed(report.longrepr.strip().splitlines()):
            s = line.strip()
            if s and not s.startswith(("E   ", "^", "~")):
                return s[:140]
        return report.longrepr.strip().splitlines()[-1][:140]
    return "test failed"


def build_defect(report: TestReport) -> Defect | None:
    """Build a Defect from a failed/errored TestReport. Returns None for
    passed/skipped/pending so callers can map-and-filter."""
    if report.status not in _PRIORITY:
        return None
    priority, severity = _PRIORITY[report.status]

    env = report.environment
    device = env.get("device_types") or env.get("device_id") or "device"
    project = env.get("test_project_marker") or env.get("PROJECT") or "common"
    feature = env.get("feature", "")

    summary = f"[{project}/{device}] {report.name} — {_short_reason(report)}"

    # --- description (JIRA wiki-ish markdown; renders fine as plain text too) ---
    d: list[str] = []
    d.append("h2. Summary")
    d.append(f"Automated system test *{report.name}* {report.status} during a run.")
    d.append("")

    d.append("h2. Environment")
    if env:
        for k, v in env.items():
            d.append(f"* *{k}:* {v}")
    else:
        d.append("_(no environment captured)_")
    d.append("")

    d.append("h2. Steps to reproduce")
    d.append("{code}")
    d.append(f'robot --test "{report.name}" {report.file}'.strip())
    d.append("{code}")
    if report.notes:
        d.append("Test notes:")
        for n in report.notes:
            d.append(f"* {n}")
    d.append("")

    d.append("h2. Expected result")
    d.append(report.expected or "_See test assertion (no explicit expected set)._")
    d.append("")
    d.append("h2. Actual result")
    d.append(report.actual or _short_reason(report))
    d.append("")

    if report.longrepr:
        tb = report.longrepr.strip()
        truncated = len(tb) > _TRACEBACK_MAX_CHARS
        if truncated:
            tb = tb[-_TRACEBACK_MAX_CHARS:]
        d.append("h2. Failure detail")
        if truncated:
            d.append("_(tail of traceback — full detail in the attached report.md)_")
        d.append("{code}")
        d.append(tb)
        d.append("{code}")
        d.append("")

    # Evidence: the per-test report.md plus any attached logs/screens.
    evidence: list[Path] = []
    report_md = report.report_dir / "report.md"
    if report_md.exists():
        evidence.append(report_md)
    evidence.extend(a for a in report.attachments if a.exists())
    if evidence:
        d.append("h2. Evidence")
        for e in evidence:
            d.append(f"* {e.name}")
        d.append("")

    labels = ["automated-test", f"project-{project}"]
    if feature:
        labels.append(f"feature-{feature}")

    return Defect(
        summary=summary,
        description="\n".join(d).strip(),
        labels=labels,
        priority=priority,
        severity=severity,
        evidence=evidence,
    )
