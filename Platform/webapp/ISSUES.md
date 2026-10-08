# Test-Ops Console — issues & feedback (v8)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`
- `archive/ISSUES-2026-09-28-resolved.md`
- `archive/ISSUES-2026-09-28-b-resolved.md`
- `archive/ISSUES-2026-10-08-resolved.md` (v7: everything up to 2026-10-08)

**How to use:** just drop raw bullet points under "Testing notes" below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## To test today (built since v7, none of it eyeballed by you yet)

- **Automation → Coverage** — Robot tests tied to TestRail cases, and which sections have a linked functional test. Draft numbers; most
  sections read ZERO until mapping rows are approved (see below).
- **Automation → Runs → Judge failures** — pulls a finished sit run, groups failures, AI judges P1–P5, you confirm, writes a
  `severity=P<n>` tag patch for sit. Has a **run picker** (default: newest finished run with Robot results). The AI step has never run.
- **Automation → Live runs → Schedule & manual run** — when the pipeline runs by itself (read from sit's workflow), and a guarded
  "Start run now" (preview first; needs the tick box; uses the lab device). Please don't start one unless you mean to.
- **Hand-offs** (Test-Ops sidebar) — the author → review → approve → automate → run → report queue; approve/reject as yourself.
- **Status page** no longer gets overwritten by a view you open while it is loading.
- **Change target** edit/add pair is a second pop-up (checked in tests, not by eye).
- Sidebar icon rail: icons were missing for Overview, Coverage and Hand-offs — fixed.

## Known open (not bugs in what is built; things that need a person, data or hosting)

- **Hosting / logins** for company-wide use — needs IT's answer on who owns internal hosting; then SSO, per-user secrets, Postgres,
  shared uploads. Also gates the runner → console live push (`tops-live-push-mode` branch in sit is held for this).
- **Mapping approvals** — `system-test-ops/proposals/Translink-POS-suite-restructure/robot-case-mapping-DRAFT.csv`: fill `approved_case_id`
  for the rows you agree with (only 7 tests link to a case today), then re-run the two tools; Coverage updates.
- **Judge failures**: P2–P4 wording in `system-test-ops/knowledge/severity-rubric.md` is my proposal; a tag is a snapshot of one run's
  judgement (the patch replaces an existing `severity=` tag but never removes it from a test that now passes).
- **Lab database** ("TDS server unavailable") fails every sit suite setup, so no test body has run on a device.
- **Ingest-docs** has not been run on the real POS docs through the console; 246 marker cases still need device checks / Translink
  answers; 47 gap answers are "needs a decision".
- **Coverage**: no Refresh button (re-running the two tools needs TestRail from wherever the console is hosted).
- **Schedule**: shown, not editable — changing it is a PR to sit's workflow file.
- **Stale-render guard** covers the Status page only; other slow views could in principle land on top of one opened early.
- **e2e**: no pipeline-run test yet (a run writes into the real system-test-ops; needs a throw-away copy of it).
- **ZZ_DELETE_REVIEW** binning in TestRail — yours (needs delete rights).
- **Open question**: scheduled checks — against a centralised doc location, or just internal uploads?
- **Naming/IA umbrella** — review remaining pipeline/option names against their real scope.

---

## Testing notes (George)

-
