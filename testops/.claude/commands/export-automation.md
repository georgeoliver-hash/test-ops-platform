---
description: Export the automatable-marked cases as a backlog (JSON + MD) for the automation-tests repo. Usage: /export-automation <project> <suite-id>
argument-hint: <project> <suite-id>
---

Hand the automatable cases to the sibling `automation-tests` repo. Arguments: `$ARGUMENTS`
(`$1` = project, `$2` = suite id; defaults to `TESTRAIL_WRITE_SUITE_ID` if `$2` omitted).

1. Run `python -m system_test_ops export-automation --suite $2`. (Add `--include-manual` to also list
   the cases marked `Automatable: No`.) Read-only — it only reads TestRail.
2. It writes `reports/<project>/<suite>/<date>/automation-backlog.json` (machine-readable handoff) and
   `automation-backlog.md` (human view), ordered High -> Normal -> Low priority.
3. Report the counts (automatable / total, destructive, manual-only) and point at both files.

The backlog is the contract with `automation-tests` (see `docs/automation-handoff.md`):
- each entry carries its TestRail **case id** (`ref`, e.g. `C4099911`) so an automated test maps back;
- `device` + `feature` mirror the pytest markers; `destructive: true` -> `@pytest.mark.destructive`;
- `cross_check` lists the back-office systems (CloudFare / MERIT / SmartTrack) the test must verify;
- `automatable`/`priority` are starting-point judgements the automation engineer may override.

The marker lives in each case's **Expected** as `[Automatable: Yes/No · Cross-check: …]` (set by
`tools/enrich_cases.py`). To re-judge after edits: re-run enrichment, then re-export.
