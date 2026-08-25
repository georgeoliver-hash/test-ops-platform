"""Per-test report data model + markdown renderer.

A `TestReport` is built incrementally during a test's lifecycle: the plugin
populates status/duration/traceback, fixtures populate environment + attach
device logs, and tests can add notes or set expected/actual via the
`jira_report` fixture. Rendered to `report.md` at teardown for copy/paste into
a Jira ticket.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Status = Literal["passed", "failed", "skipped", "error", "pending"]


@dataclass
class TestReport:
    nodeid: str
    name: str
    file: str = ""
    status: Status = "pending"
    duration_seconds: float = 0.0
    started_at: str = ""
    finished_at: str = ""
    longrepr: str = ""
    expected: str = ""
    actual: str = ""
    environment: dict[str, str] = field(default_factory=dict)
    attachments: list[Path] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    captured_stdout: str = ""
    captured_stderr: str = ""
    report_dir: Path = field(default_factory=Path)

    def attach(self, path: Path | str) -> None:
        p = Path(path)
        if p.exists() and p not in self.attachments:
            self.attachments.append(p)

    def note(self, text: str) -> None:
        self.notes.append(text)

    def set_expected(self, text: str) -> None:
        self.expected = text

    def set_actual(self, text: str) -> None:
        self.actual = text

    def render_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# {self.name}")
        lines.append("")
        lines.append(f"**Status:** `{self.status}`")
        lines.append(f"**Duration:** {self.duration_seconds:.2f}s")
        if self.started_at:
            lines.append(f"**Started:** {self.started_at}")
        if self.finished_at:
            lines.append(f"**Finished:** {self.finished_at}")
        lines.append("")

        lines.append("## Repro")
        lines.append("")
        lines.append("```")
        lines.append(f'robot --test "{self.name}" {self.file}'.strip())
        lines.append("```")
        lines.append("")

        lines.append("## Environment")
        lines.append("")
        if self.environment:
            for k, v in self.environment.items():
                lines.append(f"- **{k}:** {v}")
        else:
            lines.append("_(no environment captured)_")
        lines.append("")

        if self.expected or self.actual:
            lines.append("## Expected vs Actual")
            lines.append("")
            lines.append(f"**Expected:** {self.expected or '_unspecified_'}")
            lines.append("")
            lines.append(f"**Actual:** {self.actual or '_unspecified_'}")
            lines.append("")

        if self.longrepr:
            heading = "Failure detail" if self.status == "failed" else "Skip / outcome detail"
            lines.append(f"## {heading}")
            lines.append("")
            lines.append("```")
            lines.append(self.longrepr.strip())
            lines.append("```")
            lines.append("")

        if self.notes:
            lines.append("## Notes")
            lines.append("")
            for n in self.notes:
                lines.append(f"- {n}")
            lines.append("")

        if self.attachments:
            lines.append("## Attachments")
            lines.append("")
            for a in self.attachments:
                try:
                    rel = a.relative_to(self.report_dir)
                    target = f"./{rel.as_posix()}"
                except ValueError:
                    target = str(a)
                lines.append(f"- [`{a.name}`]({target})")
            lines.append("")

        if self.captured_stdout.strip():
            lines.append("## Captured stdout")
            lines.append("")
            lines.append("```")
            lines.append(self.captured_stdout.strip())
            lines.append("```")
            lines.append("")

        if self.captured_stderr.strip():
            lines.append("## Captured stderr")
            lines.append("")
            lines.append("```")
            lines.append(self.captured_stderr.strip())
            lines.append("```")
            lines.append("")

        return "\n".join(lines)
