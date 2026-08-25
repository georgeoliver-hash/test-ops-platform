"""Robot Framework Listener v3: per-test report dirs + Jira-ready report.md +
run summary. Replaces the pytest plugin (`framework/reporting/plugin.py`) —
the RF hooks below are the direct analogue of the pytest hooks it used:

    pytest hook                      RF listener hook
    --------------------------       --------------------------------
    pytest_configure                 __init__ / start_suite (top-level only)
    pytest_runtest_makereport        end_test (status/duration/message)
    pytest_runtest_teardown          end_test (writes report.md)
    pytest_sessionfinish             close (writes index.md/html/defects.json)

`TestReport`, `build_defect`, and `render_run_html` are unchanged from the
pytest era — only this glue is new.

Usage: `robot --listener framework.reporting.robot_listener.RobotReportListener ...`

Each test's Teardown is expected to call `Collect Device Logs    ${REPORT_DIR}`
(and, on failure, `Capture UI State On Failure    ${REPORT_DIR}`) — this
listener sets `${REPORT_DIR}` as a test variable in `start_test` so those
keywords (in `DeviceLibrary`) know where to write. `end_test` then picks up
whatever files landed in that directory as attachments.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from robot.libraries.BuiltIn import BuiltIn

from .defect import build_defect
from .html import render_run_html
from .report import TestReport

ROBOT_LISTENER_API_VERSION = 3


def _safe_name(longname: str) -> str:
    safe = longname.replace("/", "__").replace("\\", "__").replace(" ", "_").replace(".", "__")
    if len(safe) > 120:
        digest = hashlib.sha1(longname.encode()).hexdigest()[:8]
        safe = safe[:110] + "_" + digest
    return safe


def _tag_value(tags, prefix: str) -> str:
    values = [t[len(prefix):] for t in tags if t.startswith(prefix)]
    return ",".join(values)


class RobotReportListener:
    def __init__(self, run_reason: str = ""):
        self.run_reason = run_reason or os.getenv("RUN_REASON", "")
        rootdir = Path.cwd()
        now = datetime.now(timezone.utc)
        stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.run_root = rootdir / "artifacts" / "runs" / stamp
        self.run_root.mkdir(parents=True, exist_ok=True)
        self.reports: dict[str, TestReport] = {}
        self._configured_at = now

    # ─── per-test ────────────────────────────────────────────────────────────

    def start_test(self, data, result):
        report_dir = self.run_root / _safe_name(result.longname)
        report_dir.mkdir(parents=True, exist_ok=True)

        report = TestReport(
            nodeid=result.longname,
            name=result.name,
            file=str(getattr(data, "source", "") or ""),
            started_at=now_iso(),
            report_dir=report_dir,
        )
        tags = list(result.tags)
        if project := _tag_value(tags, "project:"):
            report.environment["test_project_marker"] = project
        if device_types := _tag_value(tags, "device_types:"):
            report.environment["device_types"] = device_types
        if feature := _tag_value(tags, "feature:"):
            report.environment["feature"] = feature
        if os.getenv("PROJECT"):
            report.environment["PROJECT"] = os.getenv("PROJECT", "")

        self.reports[result.id] = report
        try:
            BuiltIn().set_test_variable("${REPORT_DIR}", str(report_dir))
        except Exception:
            pass  # e.g. --dryrun, where no test context is active

    def end_test(self, data, result):
        report = self.reports.get(result.id)
        if report is None:
            return
        report.finished_at = now_iso()
        report.duration_seconds = result.elapsedtime / 1000.0
        if result.passed:
            report.status = "passed"
        elif result.skipped:
            report.status = "skipped"
        else:
            report.status = "failed"
        if result.message:
            report.longrepr = result.message

        for f in sorted(report.report_dir.glob("*")):
            if f.is_file() and f.name not in ("report.md", "defect.md"):
                report.attach(f)

        report.report_dir.joinpath("report.md").write_text(
            report.render_markdown(), encoding="utf-8"
        )

    # ─── run summary ─────────────────────────────────────────────────────────

    def close(self):
        if not self.reports:
            return

        counts: dict[str, int] = {"passed": 0, "failed": 0, "skipped": 0}
        for r in self.reports.values():
            counts[r.status] = counts.get(r.status, 0) + 1

        lines: list[str] = ["# Test run summary", ""]
        lines.append(f"- Run directory: `{self.run_root}`")
        lines.append(f"- Total: {len(self.reports)}")
        for k in ("passed", "failed", "skipped"):
            if counts.get(k, 0):
                lines.append(f"- {k}: {counts[k]}")
        lines += ["", "## Tests", "", "| Status | Test | Duration |", "|---|---|---|"]

        def sort_key(r: TestReport):
            order = {"failed": 0, "passed": 1, "skipped": 2}
            return (order.get(r.status, 9), r.nodeid)

        for r in sorted(self.reports.values(), key=sort_key):
            try:
                rel = r.report_dir.relative_to(self.run_root).as_posix()
            except ValueError:
                rel = r.report_dir.as_posix()
            lines.append(f"| {r.status} | [{r.nodeid}](./{rel}/report.md) | {r.duration_seconds:.2f}s |")

        self.run_root.joinpath("index.md").write_text("\n".join(lines), encoding="utf-8")

        run_meta = {
            "date": self._configured_at.strftime("%Y-%m-%d"),
            "time": self._configured_at.strftime("%H:%M:%S"),
            "reason": self.run_reason,
            "project": os.getenv("PROJECT", ""),
            "marker_expr": "",
            "command": "robot " + " ".join(sys.argv[1:]),
            "counts": counts,
        }

        defects_payload = []
        for r in self.reports.values():
            defect = build_defect(r)
            if defect is None:
                continue
            r.report_dir.joinpath("defect.md").write_text(
                defect.render_markdown(), encoding="utf-8"
            )
            entry = defect.to_jira_fields()
            entry["nodeid"] = r.nodeid
            entry["status"] = r.status
            defects_payload.append(entry)

        if defects_payload:
            self.run_root.joinpath("defects.json").write_text(
                json.dumps({"run": run_meta, "defects": defects_payload}, indent=2, default=str),
                encoding="utf-8",
            )

        try:
            html_doc = render_run_html(run_meta, list(self.reports.values()), self.run_root)
            self.run_root.joinpath("index.html").write_text(html_doc, encoding="utf-8")
        except Exception as exc:
            self.run_root.joinpath("index.html.error.txt").write_text(
                f"HTML report generation failed: {exc!r}", encoding="utf-8"
            )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
