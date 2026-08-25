---
description: Review the last N TestRail runs of a suite and recommend add/edit/remove/reorganise. Usage: /review-runs <project> <suite> [--last N]
argument-hint: <project> <suite> [--last N]
---

Review run history. Arguments: `$ARGUMENTS`
(positional: `$1` = project, `$2` = suite; optional `--last N`, default 10).

**If `$1` or `$2` is missing, stop and ask before doing anything else** — per `CLAUDE.md`'s hard rule
on confirming an ambiguous target: which project/device, and which suite?

Act as the **test-lead** agent (`.claude/agents/test-lead.md`). Follow its run-history playbook:

1. Read `CLAUDE.md`, `knowledge/projects/$1.md`, and `knowledge/devices/*.md` for the suite.
2. Produce the deterministic baseline (read-only):
   `python -m system_test_ops runs --project $1 --suite $2 --last <N>`
   If the CLI errors on credentials, stop and point the user at `docs/getting-started.md`.
3. Dispatch **run-historian** with the `run-health.json` path.
4. For any gap it implies (e.g. an unstable area with no reliable happy-path case), dispatch
   **gherkin-author** to draft, then **standards-keeper** to review.
5. Consolidate into `reports/$1/$2/<date>/run-health.md`: a health summary, the flagged-cases table
   (always-failing / never-run / flaky / regressed / orphaned), and a ranked
   ADD/EDIT/REMOVE/REORGANISE/INVESTIGATE list — each citing run ids and linking any drafts.

Finish by printing the report path and the top 3 actions. Read-only against TestRail — propose,
don't write.
