---
description: Cross-reference a device's flow-map inventory against its live TestRail suite, fill in every "Covered by" column, and route findings to ADD/EDIT/CONDEMN/DEFER/ESCALATE. Usage: /audit-flows <project> <device> <suite-id>
argument-hint: <project> <device> <suite-id>
---

Run a **flow-map coverage pass** — the flow-data equivalent of `/audit-coverage`, but scoped to this
repo's own `knowledge/flows/` transcriptions instead of a JIRA fix version, so it can run without one.
Arguments: `$ARGUMENTS` (`$1` = project, `$2` = device, `$3` = suite id).

**If `$1`, `$2`, or `$3` is missing, stop and ask before doing anything else** — per `CLAUDE.md`'s
hard rule on confirming an ambiguous target. Ask which project, which device, and which suite id.

**Then, before pulling any baseline, check the flow-maps actually exist — don't discover this
mid-process.** `Glob knowledge/flows/$1-$2-*.md` (excluding `*-full-transcription-*.md`) as the very
first action, before step 1 below:
- **Files exist** → proceed normally.
- **Zero files match** → stop and say so plainly: this project/device has no structured flow-maps
  yet. Ask how the user wants to proceed — do they have a raw UX export ready to transcribe first
  (today this only has a built ingestion path for **Overflow** exports via the Chrome-extension
  transcription process used for every existing device; a different source like Figma has no
  ingestion tooling yet and would need that built first), or would they rather run `/audit-coverage`
  instead for now (grounds against a JIRA release, doesn't need flow-maps at all)? Don't guess which
  they'd prefer.

Act as **test-lead** (`.claude/agents/test-lead.md`). Load `CLAUDE.md` and
`docs/test-practices.md` first, plus `proposals/<device>-suite-restructure/regression-register.md`
and `mode-coverage.md` if they exist for this device — you need both before touching any case.

1. **Baseline.** `python -m system_test_ops cases --project $1 --suite $3` → note the `cases.json`
   path. Read-only; never re-fetch by hand.
2. **Inventory the flow-maps.** Reuse the Glob result from the pre-check above — each matched file is
   one flow-map to audit.
3. **Dispatch coverage-analyst once per flow-map, in parallel.** Give each dispatch the `cases.json`
   path and exactly one flow-map file. `coverage-analyst` already reads a flow map's `Paths` table as
   a coverage checklist (see `.claude/agents/coverage-analyst.md`) and returns
   covered/partial/missing/stale/**fragmented** per path, citing case ids:
   - **fragmented** — the path is only "covered" by several scattered near-duplicate cases, none of
     which reads as the whole path end-to-end. This is distinct from **stale**: nothing is wrong with
     the individual cases, they're just not organised around this path. Don't ask gherkin-author to
     author over a fragmented path — defer it (see step 4).
4. **Triage the combined results.** For each path finding:

   | Finding | Action | Who |
   |---|---|---|
   | missing | ADD a new case, grounded only in this path's screen states / notes | gherkin-author |
   | partial | ADD the missing edge/branch only — don't duplicate what's already covered | gherkin-author |
   | stale | EDIT (if correctable) or CONDEMN — rename `ZZ_DELETE_REVIEW - <title> (superseded)` if it was built on now-disproven behaviour | gherkin-author |
   | fragmented | DEFER — append a row to `proposals/<device>-suite-restructure/consolidation-audit.md` (create it if absent) naming the path and the scattered case ids; do not author on top of it | test-lead (log only) |
   | flow-map row is `TODO`/`GAP`/`UNCONFIRMED` | ESCALATE — append to `proposals/coherence-audit/gap-register.md`; never guess the missing detail | route through `/resolve-gaps` afterwards |
   | covered | none — just record the real case id(s) | — |

   Before touching **any** case, check this device's `regression-register.md` for open
   **NEEDS GEORGE** rows (rows whose Disposition is literally `NEEDS GEORGE`, however many there are
   — don't assume a fixed count). Never silently edit, resolve, or drop one of those rows or the case
   it points at; if a finding touches the same case, flag it in the report instead of acting on it.

5. **Write real case ids back into the flow-maps.** For every path now classified, edit that
   flow-map's `Covered by` cell with the real TestRail case id(s), or an explicit `GAP — see
   proposals/coherence-audit/gap-register.md` / `DEFERRED — see consolidation-audit.md` note if it isn't a clean case-id yet.
   **test-lead does this write**, not coverage-analyst — keeps the read-only/write split intact.
6. **Author + push.** Dispatch **gherkin-author** for every ADD/EDIT/CONDEMN item, grounded strictly
   in the flow-map's screen states and notes (never invent a screen name, decision, or audit event
   not present there). Every new/edited case must carry this device's existing tagging scheme in the
   *same* push — don't leave tagging as a follow-up. Then dispatch **standards-keeper** to review the
   drafts. A human runs the actual `push --commit`.
7. **Conformance gate.** After any push, `python -m system_test_ops audit --suite $3` must be CLEAN
   of blocking findings before calling the pass done (same rule as every other authoring command).

## What you produce
Write `reports/$1/$3/<date>/flow-coverage.md`:
- One row per flow-map path: path text → classification → case id(s) or gap/defer pointer.
- Counts: covered / partial / missing / stale / fragmented / escalated.
- The ADD/EDIT/CONDEMN list actually pushed (or queued for a human `--commit`).
- Any `consolidation-audit.md` / `proposals/coherence-audit/gap-register.md` rows this run added.
- An explicit note confirming `regression-register.md`'s NEEDS GEORGE rows were left untouched.

Finish by printing the report path and a one-line summary (path counts by classification + whether
the suite audit is CLEAN).
