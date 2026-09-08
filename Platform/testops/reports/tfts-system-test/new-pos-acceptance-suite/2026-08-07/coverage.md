# Coverage audit — Translink POS — TL_POS_3.0.0

- **Project:** Translink (TestRail project `TFTS - System Test`, id 42)
- **Suite audited:** `**NEW** POS-Acceptance Suite` (TestRail suite id 30253 — the suite this doc's
  `knowledge/projects/translink.md` still calls "GG - POS - Claude Suite"; same id, renamed since
  that note was written — worth a knowledge-file refresh, flagged below, not actioned here)
- **JIRA scope:** fix version `TL_POS_3.0.0`, project key **TIBU** (resolved live — the generic
  `CAFCPOS` "Point Of Sales" project returned zero hits for this fix version; TIBU is correct)
- **Baselines (read-only, generated 2026-08-07):**
  - `cases.json` / `cases.md` — 799 cases in suite 30253
  - `run-health.json` / `run-health.md` — last 6 runs (21978, 21742, 21495, 19352, 19087, 19074), 822 cases tracked
  - `case-drafts.md` — 3 ready-to-paste drafts + 5-question gap register for the remaining gaps
- **Nothing was written to TestRail.** This is a read-only audit; all recommendations below are proposals.

## Verdict

**Not clean.** Of 9 JIRA issues in scope (4 epics as containers + 5 directly-testable stories/bugs),
3 are covered, 3 are partial (one with a **live data conflict** that must be resolved before any case
is pushed), and 2 are missing. Separately, the suite's run history shows the authoring/run cadence is
badly out of sync — 799 of 822 tracked cases (97%) have never appeared in a run — plus a real
regression signal and a cluster of flaky screen-verification cases that predate this fix version.

## Scope table (TL_POS_3.0.0 / project TIBU)

| Issue | Type | Classification | Case(s) | Note |
|---|---|---|---|---|
| TIBU-24900 | Epic | container | — | "Release 3.0.0 TL POS" umbrella; not directly testable. Children not retrievable via MCP (permission error on cloud-id) — **flagged as an unresolved input**, not classified. |
| TIBU-28050 | Epic | container | — | "Bus POS Bug Fixes" umbrella; likely parent of the 3 bug-fix items below, but child linkage unconfirmed for the same MCP reason. |
| TIBU-28051 | Epic | **PARTIAL** (thin basis) | C4103578–4103580 (Refs `FBD-100207`) | CR113 Bus Stop Boarding Stage Grouping. Plausibly covered by the existing Fare-Stage Selection cases, but unconfirmed whether CR113 adds behaviour beyond `FBD-100207`. No case cites TIBU-28051 directly. Routed to gap register (Q5) rather than guessed. |
| TIBU-28211 | Epic | **MISSING** | — | "Ticket Editor Integration with POS." Zero hits anywhere in the 799 cases. No case drafted — only the standalone Ticket Editor tool spec exists locally, not POS-integration acceptance criteria. Routed to gap register (Q4). |
| TIBU-28350 | Story | **PARTIAL → drafted** | C4100034 (existing, Rail) + new draft (Ulsterbus) | Print barcode on a bus ticket. Existing case is generic/Rail; new Ulsterbus-specific case drafted in `case-drafts.md`, restructured post-review so the scan action is the `When`, not smuggled into `Given`. |
| TIBU-24804 | Story | **PARTIAL → drafted, ⚠️ conflicted** | C4099946 (existing, Rail) + new draft (Ulsterbus) | See "Highest-risk finding" below — do not push the new draft's Refs as-is. |
| TIBU-19459 | Bug | **COVERED** | C4100374 | "Bus — products cannot be added to basket." Case explicitly asserts add-to-basket; Refs cite this key. |
| TIBU-19460 | Bug | **COVERED** | C4100374 (same case) | "Bus — products cannot be purchased." Same case asserts the purchase step too. |
| TIBU-19458 | Bug | **COVERED** | C4100375 | "Bus — '*' doesn't show Letters." Case directly asserts the letters-entry regression; Refs cite this key. |
| TIBU-31553 | Bug | **MISSING → drafted** | new draft (Ulsterbus, `@regression`) | "Ulsterbus sign-on stuck on Loading Screen." Zero existing coverage; new case drafted with the unconfirmed screen name marked as commentary (not invented), and the "no documented duration threshold" item correctly re-tagged as an assumed-knowledge note (timeouts here are configurable per `knowledge/projects/translink.md`), not a GAP. |

**Counts: 3 covered · 3 partial · 2 missing · 2 unresolved-container (epics pending JIRA child data).**

## Highest-risk finding — TIBU-24804 mode conflict

The task brief said TIBU-24804 is an **Ulsterbus** Operator Menu defect. Two independent local records
disagree: `proposals/coherence-audit/gap-register.md` (Q26) and
`proposals/pos-suite-restructure/bug-regression-register.md` both cite old-suite case **C4078764**,
titled *"TL POS Rail — Operator Menu — Excess Ticket Feature doesn't exist"* — i.e. **Rail**, not
Ulsterbus. The existing suite case `C4099946` ("Excess Ticket — available (rail)") currently carries
`Refs: TIBU-24804`, which — if the repo's own records are right — means **the bug fix is not actually
re-tested where the regression happened**, and the *new* Ulsterbus draft's Refs line has been marked
`**UNCONFIRMED — pending JIRA mode re-check, conflicts with gap-register Q26**` rather than asserted
as fact. **Do not push either case's Refs change until this is resolved with the engineer or a live
JIRA re-read of TIBU-24804's actual description/component.** This is exactly the kind of gap CLAUDE.md
requires routing through the Q&A loop rather than picking a side — logged as Q2 in the gap register.

## ADD / EDIT / REMOVE / REORGANISE recommendations

**ADD** (drafted, ready to review in `case-drafts.md` — standards-keeper review applied, casing fixed,
GAP placement fixed, Given/When/Then restructured):
- Sign On — Ulsterbus reaches the signed-on landing screen without hanging (Refs `TIBU-31553`, `@regression`)
- Excess Ticket — available (Ulsterbus) (Refs `TIBU-24804` **UNCONFIRMED**, blocked on the conflict above)
- Barcode — print barcode (Ulsterbus ticket) (Refs `TIBU-28350`)

**EDIT** (flagged, not yet drafted — needs a human/engineer decision, not a mechanical fix):
- C4099946 — if the Rail/Ulsterbus conflict resolves in favour of "TIBU-24804 is Rail," this case's
  Refs are already correct and the new Ulsterbus draft should NOT cite TIBU-24804. If it resolves the
  other way, C4099946's Refs should be removed (it doesn't catch an Ulsterbus regression).
- 9 flaky "Verify `<X> Screen` Contents" cases (see run-health section) — share one probable root
  cause (a content-verification timing/rendering race); fix once, not per-case.
- C2092782 ("UnSuccessful Cloudfare SignOn - Administrator") — recently-regressed; investigate as a
  real defect before treating as a test-authoring issue, then stabilise (also flaky: 2 pass / 3 fail
  / 6 runs).

**REMOVE** (via TestRail UI — API delete isn't reliable per CLAUDE.md's platform constraints):
- 50 cases explicitly self-titled `ZZ_DELETE_REVIEW — ... (folded)`, confirmed absent from all 6
  windowed runs. Full id list in `run-health.json`/`.md`.

**REORGANISE**:
- The remaining ~749 orphaned cases (Sign On/Off, FLU, Basket, Top Up, Screen Validation, etc.) are
  authored-but-not-yet-run new-suite content — get them into a TestRail run configuration so the next
  `runs --last N` pull actually exercises them. This is expected mid-build-out, not evidence of dead
  cases.

## Run-health summary (last 6 runs: 21978, 21742, 21495, 19352, 19087, 19074)

| Category | Count | Detail |
|---|---|---|
| Always-failing (flagged) | 0 | See note below — 2 cases likely under-counted by the classifier. |
| Never-executed | 0 | — |
| Flaky | 15 | 9 cluster around "Screen Contents" verification (shared likely root cause); 1 genuine regression case also flaky (C2092782). |
| Recently regressed | 1 | C2092782 — investigate as a real defect first. |
| Orphaned | 799 | 50 self-marked for deletion; 749 awaiting inclusion in a run. |

**Detection-blind-spot note:** `C2082948` ("Verify \"Business Intelligence Screen\" Contents") and
`C2092794` ("UnSuccessful Cloudfare SignOn - AD CloudFare User") both show **0 passes** across all
executions but escaped the `always_failing` flag because the classifier
(`system_test_ops/runs/history.py:124`) requires `failed == executed_count` exactly, and these mix in
some `other`-status results. Recommend treating both as de-facto always-failing candidates for
investigation; this is a note on the threshold's blind spot, not a request to change it here.

## Gap register (Q&A loop — route to the engineer)

New file: `proposals/pos-suite-restructure/gap-register.md`, 5 questions logged (Q1–Q5), covering:
TIBU-31553's landing-screen name, the TIBU-24804 Rail/Ulsterbus conflict, whether the barcode family
is really NIR-only, TIBU-28211's missing child-issue data, and whether CR113 (TIBU-28051) needs its
own case beyond `FBD-100207`. None were silently resolved — per CLAUDE.md, a gap nobody can answer is
itself a finding.

## Known input gap for next run

The Atlassian MCP could not retrieve child issues for epics TIBU-24900/28050/28051/28211 (cloud-id
permission error mid-audit). This audit only classified the 9 issues visible via direct fix-version
search; if these epics have additional child stories/bugs, they are **not yet scoped**. Re-run the
epic-children query (or hand the child-issue list directly) before treating epic-level classification
as final.

## Artifacts

- `cases.json` / `cases.md` — case inventory baseline
- `run-health.json` / `run-health.md` / `run-health.jira.txt` — run-history baseline
- `case-drafts.md` — 3 drafted cases (standards-reviewed, blockers fixed) + 5-item gap register pointer
- `proposals/pos-suite-restructure/gap-register.md` — the 5 open questions for the engineer
