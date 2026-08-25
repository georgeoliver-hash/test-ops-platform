---
description: Periodic suite maintenance — run-history health (retire dead/flaky), conformance audit, and a consolidation sanity check. Usage: /maintain <project> <suite-id>
argument-hint: <project> <suite-id>
---

Routine upkeep so the suite stays lean and trustworthy. Arguments: `$ARGUMENTS` (`$1` = project,
`$2` = suite id). Act as **test-lead**; "Maintain, don't just add" (`docs/test-practices.md`).

**If `$1` or `$2` is missing, stop and ask before doing anything else** — per `CLAUDE.md`'s hard rule
on confirming an ambiguous target: which project/device, and which suite?

1. **Run-health:** `python -m system_test_ops runs --project $1 --suite $2 --last 10` (dispatch
   **run-historian**). Flag always-failing (candidate invalid), never-executed, flaky, recently-
   regressed, orphaned. Propose retirements (`ZZ_DELETE_REVIEW`) and flake fixes — the suite should
   shrink as often as it grows.
2. **Conformance:** `python -m system_test_ops audit --suite $2`. Any blocking finding is unfinished
   work — fix and re-push.
3. **Consolidation sanity check:** skim functional areas for any new over-fragmentation that crept in
   (steps/variations split into separate cases); if found, run `/consolidate`.
4. **Traceability:** confirm recent defects are pinned via Refs (`/fold-defect`) and recent stories
   covered (`/add-feature`).
5. Report a short health verdict (counts, retirements proposed, audit status) with case/run-id
   citations. Read-only against TestRail — propose; a human applies via the UI / a `--commit` push.
