"""Hand gaps to the people who can answer them, and take the answers back.

Export: the `gap-sheet` CLI writes `gap-export.csv` (one row per distinct gap, grouped, with a plain
summary and a single question, and blank Verdict / Answer / Answered by / Evidence columns). Import:
the filled-in CSV comes back, each row is matched to its gap by its stable Gap ID, and every answered row
is saved to the console's gap-answers log (the same log the Gaps screen's click-to-answer uses), so who
answered, what, and when is on record.

Nothing here edits a case or a knowledge note. An answer is recorded; applying it is the Resolve step,
which cites it. A Verdict of "Mismatch" or "Needs a decision" is logged as a conflict / clarification
request, never as a plain answer: the device is evidence, not the verdict.
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
from pathlib import Path

from Platform.webapp import runner, store

VERDICT_TYPES = {"matches spec": "answer", "mismatch": "conflict", "needs a decision": "clarification_request"}
# A drafted sheet (e.g. answers written from the code and the defect list, "Answered by: Claude (draft)")
# uses its own verdicts. Every one of these is imported as a DRAFT: code is evidence of what the build does,
# never a confirmed answer, and a person still has to confirm it. Order matters (longest first).
DRAFT_VERDICTS = {
    "answered from code": ("answer", "[DRAFT from code - not seen on a device] "),
    "answered": ("answer", "[DRAFT - review before use] "),
    "needs confirmation": ("clarification_request", "[DRAFT - needs confirmation] "),
}
# Nothing to record for these: a duplicate is answered on the row it duplicates, a gap that is not about
# this device is not this device's to answer, and "not a gap" is a note that only looked like one.
SKIP_VERDICTS = ("duplicate", "out of scope", "not a gap")


def _dir(project: str) -> Path:
    return runner.SYSTEM_TEST_OPS_ROOT / "reports" / project.lower() / "clarify-gaps"


def export_csv(project: str, device: str | None) -> Path:
    """Regenerate the sheets for this device and return the CSV path. Raises FileNotFoundError with a
    plain message if the grouping has not been run yet."""
    if not (_dir(project) / "gap-groups.json").is_file():
        raise FileNotFoundError("The gaps have not been grouped yet. Run Group gaps (under Checks) first.")
    args = [str(runner._VENV_PYTHON), "-m", "system_test_ops", "gap-sheet", "--project", project.lower()]
    if device:
        args += ["--device", device]
    proc = subprocess.run(args, cwd=str(runner.SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True,
                          timeout=120, encoding="utf-8", errors="replace")
    path = _dir(project) / "gap-export.csv"
    if proc.returncode != 0 or not path.is_file():
        tail = (proc.stderr or proc.stdout or "no output").strip().splitlines()[-1:]
        raise RuntimeError(f"Could not build the export: {tail[0] if tail else 'no output'}")
    return path


def import_csv(project: str, device: str | None, csv_text: str, default_by: str | None) -> dict:
    """Record every answered row of a returned sheet. Returns counts plus per-row problems; a bad row
    never blocks the good ones."""
    inputs_path = _dir(project) / "gap-inputs.json"
    if not inputs_path.is_file():
        raise FileNotFoundError("No gap list for this project yet. Run Group gaps first.")
    by_id = {i["id"]: i for i in json.loads(inputs_path.read_text(encoding="utf-8")) if i.get("id")}
    existing = {(a["gap_ref"], a["answer"]) for a in store.list_gap_answers(project)}
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("﻿")))
    result = {"imported": 0, "blank": 0, "duplicates": 0, "unknown_ids": [], "errors": [], "conflicts": 0, "decisions": 0,
              "skipped_duplicate_or_out_of_scope": 0, "drafts": 0}
    for n, row in enumerate(reader, start=2):  # row 1 is the header
        gid = (row.get("Gap ID") or "").strip()
        answer = (row.get("Answer") or "").strip()
        verdict = (row.get("Verdict") or "").strip()
        notes = (row.get("Evidence or notes") or "").strip()
        if not gid:
            continue
        if not answer and not verdict:
            result["blank"] += 1
            continue
        item = by_id.get(gid)
        vlow = verdict.lower()
        if vlow.startswith(SKIP_VERDICTS):
            result["skipped_duplicate_or_out_of_scope"] += 1
            continue
        if item is None:
            result["unknown_ids"].append(gid)
            continue
        draft = next((v for k, v in DRAFT_VERDICTS.items() if vlow.startswith(k)), None)
        vkey = next((k for k in VERDICT_TYPES if vlow.startswith(k)), None)
        if verdict and vkey is None and draft is None:
            result["errors"].append({"row": n, "gap_id": gid, "reason": f"Verdict '{verdict}' is not one of: Matches spec / Mismatch / Needs a decision."})
            continue
        who = (row.get("Answered by") or "").strip() or (default_by or "").strip()
        if not who:
            result["errors"].append({"row": n, "gap_id": gid, "reason": "No 'Answered by' on the row and no name given for the import."})
            continue
        text = (draft[1] if draft else (f"{verdict}: " if verdict else "")) + (answer or "(verdict only)") + (f" [Evidence: {notes}]" if notes else "")
        # A merged row (the same question asked in several places) lists the other ids it also answers;
        # the one answer is recorded against every id so none is left open.
        also = [x for x in re.split(r"[,; ]+", row.get("Also answers (Gap IDs)") or "") if x.startswith("G-")]
        entry_type = draft[0] if draft else VERDICT_TYPES.get(vkey, "answer")
        for tid in [gid] + also:
            target = by_id.get(tid)
            if target is None:
                if tid != gid:
                    result["unknown_ids"].append(tid)
                continue
            ref = f"{tid} {target['occurrences'][0]}"
            if (ref, text) in existing:
                result["duplicates"] += 1
                continue
            try:
                store.add_gap_answer(project, ref, (row.get("Question to answer") or target.get("plain_english") or target["text"]).strip(),
                                     text, who, device=device, entry_type=entry_type)
            except ValueError as exc:
                result["errors"].append({"row": n, "gap_id": tid, "reason": str(exc)})
                continue
            existing.add((ref, text))
            result["imported"] += 1
            if draft:
                result["drafts"] += 1
            if entry_type == "conflict":
                result["conflicts"] += 1
            elif entry_type == "clarification_request":
                result["decisions"] += 1
    return result
