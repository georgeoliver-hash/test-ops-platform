# Flow-map coverage pass — Translink ETM, suite 30254

Date: 2026-08-07. Baseline: `reports/tfts-system-test/new-etm-acceptance-suite/2026-08-07/cases.json` (615 cases).
15 flow-maps audited (all `knowledge/flows/translink-etm-*.md` except the raw `full-transcription-v15.0.4.md`).

**NEEDS GEORGE rows left untouched, as required:** `regression-register.md` rows 301937 ("NOT FIXED",
confirm status) and 301828 (blank title) were not edited, resolved, or acted on. One finding below
(driver-menu-options path 22) cross-references 301828 only to note the flow-map's own escalation —
no action taken on the case itself.

## Counts across all 15 flow-maps

| Classification | Count (approx., path-rows) |
|---|---|
| Covered | ~140 |
| Partial | ~55 |
| Missing (zero functional coverage) | ~9 |
| Fragmented | 5 |
| Stale (flow-map doc itself, not the suite) | 6 |
| Escalated / GAP (routed to gap-register, not resolved) | ~10 |

## Per-flow-map summary

| Flow-map | Covered | Partial | Missing | Fragmented | Escalated | Notes |
|---|---|---|---|---|---|---|
| driver-signon | 14 | 9 | 0 | 0 | 2 | MotD/W&C available-vs-unavailable pinned to one case via "or" wording — can't prove both branches run |
| barcode-scanning | 21 | 2 | 4 | 1 | 3 | Happy path (1) fragmented across 2 cases; silent background offline-store branch (15) genuinely untested |
| driver-menu-annulment | 4 | 2 | 2 | 0 | 1 | yLink annulment (path 5) and ABT TOO annulment (path 6) have **zero functional coverage** — screen-validation stubs only |
| driver-menu-options | 18 | 5 | 0 | 0 | 2 | Faulty-reader idempotency/persistence negatives untested; annulled-ticket detail view untested |
| supervisor-menu | 8 | 4 | 0 | 0 | 1 | Paging (Config Versions/Waybill history) only screen-validated, not functionally exercised; "Other Devices" entry point needs engineer Q&A |
| technician | 20 | 10 | 1 | 1 | 1 | Systemic gap: "Go Back" nav edges asserted nowhere across 5 paths; FEC1 IP-change confirm chain fragmented |
| revenue-limit | 3 | 1 | 0 | 0 | 0 | Path 4 (revenue-lock clearing mechanism) already logged in gap-register — do not author blind |
| power-interruption | 3 | 0 | 0 | 0 | 2 | Clean; reachability-of-11.0.0-from-any-screen is the only open question |
| displays-leds-audio | 27 | 1 | 1 | 0 | 3 | **New finding**: PID/Smartcard/Operator case (4100709) was deleted (`ZZ_DELETE_REVIEW`) but flow-map still claims full coverage — real regression in suite completeness |
| flu-ticket-issue | 7 | 1 | 0 | 1 | 1 | Easibus menu (8-way stage split) fragmented — no case walks the whole path |
| flu-abt-emv | 1 | 3 | 0 | 1 | 2 | Passback-clearing behaviour assumed mode-agnostic but never verified on Ulsterbus — money/audit risk |
| flu-basket-mode | 5 | 5 | 0 | 0 | 2 | Payment approval/decline (paths 3/5) only screen-validated, not functionally tested — primary revenue path |
| flu-navigation | 6 | 3 | 0 | 0 | 1 | Speed-only/footprint-only gating branches not isolated from combined condition |
| flu-printer-travel-mode | 3 | 4 | 0 | 0 | 1 | Case 4105058 (path 6) may be wired to wrong precondition — flagged for regrounding, not accepted as covered |
| flu-smartcard | 5 | 8 | 0 | 1 | 0 | Flow-map's own citation for path 9 is wrong (doesn't test what it claims); passback/balance-check logic only screen-validated |
| flu-promo-numeric | 5 | 3 | 0 | 0 | 0 | Direct-issue (non-basket) P&R sub-menu has zero functional coverage; flow-map citation for path 3 is stale/wrong |

## Triage — top findings by action needed

### MISSING → new case (gherkin-author, grounded strictly in flow-map + spec)
1. **yLink/discount-card annulment** (driver-menu-annulment path 5) — no functional case; only screen-validation stub 4100723.
2. **ABT TOO product annulment** (driver-menu-annulment path 6) — no functional case; only screen-validation stub 4100724.
3. **PID/Smartcard/Operator screen state** (displays-leds-audio) — case 4100709 was retired (`ZZ_DELETE_REVIEW`); flow-map claims full coverage. Needs either a restored live case or an engineer confirmation that the state is genuinely retired — **routing to gap-register as a question, not authoring blind**, since the flow-map's basis for "this state exists" wasn't re-verified against current device behaviour.

### PARTIAL → extend existing case (gherkin-author edits, not new cases, per rubric step 1/5)
Highest-risk cluster (money/audit-adjacent, prioritize these):
- flu-basket-mode paths 3/5 — bank-card approval/decline only screen-validated; extend 4100677/4100680/4100678's sibling functional case (or add explicit assertions to 4100562) with real approval/decline logic.
- flu-abt-emv path 4 — extend a passback case to run under Ulsterbus mode explicitly (currently untested there).
- flu-smartcard paths 3/4/8 — DayLink passback/no-journeys-left/top-up-failure: extend from screen-only to functional assertions.
- driver-menu-annulment paths 3/4 — top-up annulment "present smartcard" step and incorrect-card re-prompt behaviour.
- technician — "Go Back" edges (paths 2, 15, 18, 20, 32): add one assertion line each to the existing cases (4100614, 4100616, 4105038 etc.) rather than new cases.
- driver-signon paths 19/20/21 — split the ambiguous "or"-worded case (4100510) so MotD-available and MotD-unavailable are each deterministically exercised, or add a second explicit case for the unavailable branch.
- supervisor-menu paths 3/4/5 — fold paging (Config Versions/Waybill) and print-success assertions into 4102177/4100610.
- driver-menu-options paths 2/9/10 — faulty-reader idempotency negative assertions, annulled-ticket detail view.
- barcode-scanning path 6 — disambiguate which Retry (main vs mLink) routes to which check in case 4105048.
- flu-navigation paths 2/3/6 — isolate speed-only/footprint-only branches and configured-tier-skip logic in 4100535/4100533.
- flu-ticket-issue path 5 — isolate C-key/60s-timeout abort from the expanded toggle-group list specifically.
- flu-promo-numeric paths 1/5 — assert the 3s banner-clear transition and the optional-receipt-print/cancel branch.
- flu-printer-travel-mode paths 3/4/5/7 — annul-branch outcome, paper-low exclusivity, jam-screen persistence, speed-threshold precondition.

### FRAGMENTED → defer to consolidation-audit.md (do not author over)
- barcode-scanning path 1 (happy path split 4100622/4100628)
- flu-abt-emv path 1 (Metro auto-return split 4100586/4100783/4100940)
- flu-ticket-issue path 9 (Easibus, 8 near-duplicate cases)
- technician path 16 (FEC1 IP-change confirm chain split 4100616/4105038)
- flu-smartcard path 5 (DayLink hotlist split across Validation/Hotlist sections)

### STALE flow-map documentation (not suite gaps — doc fix only, no case action)
- driver-signon: Notes/unknowns section calls paths 9/13/14/15/18/22 "missing" — all now covered by 4105049–4105053 (cases added since the 2026-08-05 pass). Text is stale.
- barcode-scanning: 2026-08-05 risk note ("path 2 + Retry/Cancel cluster unverified") is resolved by cases 4105044–4105048.
- driver-menu-options: Notes section still calls path 22 (scheduling-disabled route entry) missing/screen-only; case 4105054 now covers it functionally.
- technician: no equivalent stale note found beyond the flow map's own already-correct GAP flags.
- supervisor-menu: "Soft Reboot lands on Idle not On Break" — flow-map's own note (line 88-90) claims this distinction is unasserted; case 4100613 (updated 2026-08-07) already asserts it.
- flu-printer-travel-mode: path 2 listed as "missing" in Notes; case 4105058 covers it.
- flu-abt-emv: path 5 (Ulsterbus driver-abandon) listed missing; case 4105055 (added same day as baseline) covers it.

**Action:** these doc corrections are cheap — recommend a follow-up pass update the seven flow-maps' prose Notes sections so future `/audit-flows` runs don't re-flag resolved items. Not done in this pass (out of scope of "classify against baseline"; doing it now risks conflating "I verified this" with "I re-audited the whole file").

### ESCALATED → gap-register (already logged by flow-map, or new this pass)
- revenue-limit path 4 (lock-clearing mechanism) — already logged, reconfirmed still open.
- flu-abt-emv path 4 — Ulsterbus passback assumption, new escalation (was an "open question" in the flow-map, now confirmed genuinely untested).
- driver-menu-annulment path 9 (>1 min annulment window) — already logged.
- driver-menu-options — defect 301828 relevance question (ties to NEEDS GEORGE row, not touched) + Driver Break race-condition GAP.
- technician path 13 (Decommissioning, pending design) — already logged, reconfirmed.
- flu-ticket-issue — Basket Mode / Numeric Input entry points off FLU Home, un-transcribed (no flow-map file exists yet for these).
- barcode-scanning paths 26/27 — ticket-variant paging (12.5.3/12.5.4), blocked on unconfirmed source wiring + provisional post-R2.0 design status.
- power-interruption — reachability of 11.0.0 from arbitrary screens, unconfirmed.
- **New this pass**: PID/Smartcard/Operator retirement (displays-leds-audio) — is the screen state genuinely retired, or was the case wrongly binned?

## What was NOT done in this pass (checkpoint before proceeding)

Per the command spec, the remaining steps are:
5. Write real case ids back into all 15 flow-maps' `Covered by` cells (including correcting several
   wrong/stale citations found above: supervisor-menu, flu-smartcard path 9, flu-promo-numeric path 3).
6. Dispatch gherkin-author once per ADD/EDIT/CONDEMN item above (~9 new-case items, ~25+ extend-existing
   items) with this device's tagging scheme (`MODE-*` Refs tags per `mode-coverage.md`), then
   standards-keeper to review the drafts.
7. Re-run `python -m system_test_ops audit --suite 30254` after any push.

Given the volume (40+ discrete authoring items across 15 files), I'm checking in before generating that
many drafts/edits. Confirm scope before I proceed — e.g. prioritize the money/audit-adjacent cluster
first (basket-mode payment approval/decline, ABT Ulsterbus passback, annulment gaps) versus doing the
full sweep in one pass.
