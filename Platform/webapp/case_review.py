"""Case Review -- the human half of onboard-suite's repair step.

`system_test_ops repair` fixes what it safely can and writes the rest to
`proposals/<project>-<device>-suite-restructure/repair-plan.json` as `needs_review`. This module
is the console's view of that file: list the cases, save a human's edit to TestRail (through the
`fix-case` CLI, which refuses an edit that still breaks the standard), record a reasoned
"acceptable as-is" waiver, and re-check against live TestRail.

State lives in that one JSON file (an item's `resolution` key), next to the proposal it belongs
to -- no second copy in the console DB to drift. A case is *open* until it has a resolution;
`open_count` is what blocks the build's human_cleanup step from being approved.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from Platform.webapp import runner, store

EDITABLE = ("custom_preface", "custom_preconds", "custom_steps_seperated", "custom_expected")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _rel_dir(project: str, device: str) -> str:
    return f"proposals/{project}-{device}-suite-restructure"


def plan_path(project: str, device: str) -> Path:
    return runner.SYSTEM_TEST_OPS_ROOT / _rel_dir(project, device) / "repair-plan.json"


def _ids(project: str, device: str) -> tuple[int | None, int | None]:
    ids = store.get_suite_ids(project, device) or {}
    pid = store.get_new_testrail_project_id(project, device) or store.get_testrail_project_id(project, device)
    return ids.get("new_suite_id"), pid


def _read(project: str, device: str) -> dict | None:
    path = plan_path(project, device)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write(project: str, device: str, plan: dict) -> None:
    plan_path(project, device).write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")


def load(project: str, device: str) -> dict:
    plan = _read(project, device)
    if plan is None:
        return {"available": False, "items": [], "open": 0, "resolved": 0,
                "reason": "No repair plan yet -- it is written by the build's repair step."}
    items = plan.get("needs_review", [])
    n_open = sum(1 for i in items if not i.get("resolution"))
    return {"available": True, "suite_id": plan.get("suite_id"), "items": items,
            "open": n_open, "resolved": len(items) - n_open}


def open_count(project: str, device: str) -> int:
    return load(project, device)["open"]


def _find(plan: dict, case_id: int, rule: str) -> dict | None:
    return next((i for i in plan.get("needs_review", [])
                 if int(i["case_id"]) == int(case_id) and i["rule"] == rule), None)


def waive(project: str, device: str, case_id: int, rule: str, reason: str, by: str) -> dict:
    if not (reason or "").strip() or not (by or "").strip():
        raise ValueError("A reason and your name are both required to accept a case as-is.")
    plan = _read(project, device)
    item = plan and _find(plan, case_id, rule)
    if not item:
        raise KeyError(f"C{case_id} ({rule}) is not on the review list.")
    item["resolution"] = {"status": "waived", "reason": reason.strip(), "by": by.strip(), "at": _now()}
    _write(project, device, plan)
    store.add_case_review_log(project, device, case_id, item.get("title"), rule, "accepted", by.strip(), reason.strip())
    record_lesson(project, device, case_id, item.get("title"), rule, "accepted", by.strip(), reason.strip())
    return item["resolution"]


def reopen(project: str, device: str, case_id: int, rule: str, by: str = "unknown") -> None:
    plan = _read(project, device)
    item = plan and _find(plan, case_id, rule)
    if not item:
        raise KeyError(f"C{case_id} ({rule}) is not on the review list.")
    item.pop("resolution", None)
    _write(project, device, plan)
    store.add_case_review_log(project, device, case_id, item.get("title"), rule, "reopened", by or "unknown")


LESSONS_HEADER = """# Writing lessons -- {project}

Append-only ledger of how a person corrected or knowingly accepted a case the build would not
guess at (written by the console's Case Review screen). Read it during health checks and syncs:
if the same correction shows up twice or more, propose it as a rule for `docs/gherkin-standard.md`
(propose only -- the standards-keeper owns that file).

"""


def _flat(fields: dict) -> str:
    """One-line, truncated rendering of the edited fields, for the ledger."""
    parts = []
    for key, val in fields.items():
        if key == "custom_steps_seperated":
            val = " | ".join(f"{(r.get('content') or '').strip()} -> {(r.get('expected') or '').strip()}"
                             for r in (val or []) if isinstance(r, dict)) or "(no steps)"
        parts.append(f"{key.replace('custom_', '')}: {str(val or '').strip()}")
    text = " ; ".join(parts).replace("\n", " / ")
    return text if len(text) <= 420 else text[:417] + "..."


def lessons_path(project: str) -> Path:
    return runner.SYSTEM_TEST_OPS_ROOT / "knowledge" / project.lower() / "writing-lessons.md"


def record_lesson(project: str, device: str, case_id: int, title: str | None, rule: str,
                  action: str, by: str, reason: str | None = None,
                  before: dict | None = None, after: dict | None = None) -> None:
    """Append one decision to the repo's writing-lessons ledger. Never raises: the decision
    itself is already saved, and a ledger write failing must not undo or hide it."""
    try:
        path = lessons_path(project)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(LESSONS_HEADER.format(project=project), encoding="utf-8")
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        line = f"- {day} | {device} | C{case_id} {title or ''} | {rule} | **{action}** by {by}"
        if reason:
            line += f" -- {reason}"
        if before is not None and after is not None:
            line += f"\n  - before: {_flat(before)}\n  - after: {_flat(after)}"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def _cli(args: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(runner._VENV_PYTHON), "-m", "system_test_ops", *args],
        cwd=str(runner.SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True,
        timeout=timeout, encoding="utf-8", errors="replace",
    )


def fix(project: str, device: str, case_id: int, rule: str, fields: dict, by: str) -> dict:
    """Save a human's edit through `fix-case`. Returns {"ok": bool, "error"?, "remaining"?}."""
    bad = sorted(set(fields) - set(EDITABLE))
    if bad or not fields:
        raise ValueError(f"Editable fields are {list(EDITABLE)}.")
    if not (by or "").strip():
        raise ValueError("Your name is required so the fix is attributed.")
    plan = _read(project, device)
    item = plan and _find(plan, case_id, rule)
    if not item:
        raise KeyError(f"C{case_id} ({rule}) is not on the review list.")
    suite_id, pid = _ids(project, device)
    if suite_id is None or pid is None:
        return {"ok": False, "error": "No suite / TestRail project configured for this target."}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump(fields, fh, ensure_ascii=False)
        edit_file = fh.name
    try:
        proc = _cli(["fix-case", "--suite", str(suite_id), "--project", str(pid),
                     "--case", str(case_id), "--file", edit_file, "--commit"])
    except (subprocess.TimeoutExpired, OSError) as exc:
        return {"ok": False, "error": f"Could not run the save: {exc}"}
    finally:
        Path(edit_file).unlink(missing_ok=True)
    line = next((l for l in reversed((proc.stdout or "").splitlines()) if l.startswith("RESULT ")), None)
    if line is None:
        tail = (proc.stderr or proc.stdout or "no output").strip().splitlines()[-1:]
        return {"ok": False, "error": f"Save failed: {tail[0] if tail else 'no output'}"}
    result = json.loads(line[len("RESULT "):])
    if result.get("ok"):
        before = {k: (item.get("case") or {}).get(k) for k in fields}
        item["case"] = {**(item.get("case") or {}), **fields}
        item["resolution"] = {"status": "fixed", "by": by.strip(), "at": _now()}
        _write(project, device, plan)
        store.add_case_review_log(project, device, case_id, item.get("title"), rule, "fixed", by.strip())
        record_lesson(project, device, case_id, item.get("title"), rule, "fixed", by.strip(), before=before, after=fields)
    return result


def recheck(project: str, device: str) -> dict:
    """Re-run `repair` as a dry-run against live TestRail: items fixed directly in TestRail
    drop off, new ones appear, existing waivers carry over. Writes nothing to TestRail."""
    suite_id, pid = _ids(project, device)
    if suite_id is None or pid is None:
        return {"ok": False, "error": "No suite / TestRail project configured for this target."}
    try:
        proc = _cli(["repair", "--suite", str(suite_id), "--project", str(pid), "--out", _rel_dir(project, device)])
    except (subprocess.TimeoutExpired, OSError) as exc:
        return {"ok": False, "error": f"Could not re-check: {exc}"}
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-1:]
        return {"ok": False, "error": tail[0] if tail else "Re-check failed."}
    return {"ok": True, **load(project, device)}


def log(project: str, device: str) -> dict:
    """The decision log plus counts, for the Log tab: today (UTC date) and all time."""
    entries = store.list_case_review_log(project, device)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def count(rows):
        return {a: sum(1 for e in rows if e["action"] == a) for a in store.CASE_REVIEW_ACTIONS}
    return {"entries": entries, "today": count([e for e in entries if e["created_at"].startswith(today)]),
            "all_time": count(entries)}
