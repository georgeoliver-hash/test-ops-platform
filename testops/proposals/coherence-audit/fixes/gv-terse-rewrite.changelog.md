# GV suite (30286) — terse-not-bloated compression pass, 2026-07-21

Mandate: `docs/gherkin-standard.md` § "Terse, not bloated — trust the tester" (George, 2026-07-21).
Every citation/date/confirmation-attribution baked into Given/When/Then or Expected-result text must
move to the Refs field; full sentences must shrink to short tags. Compression only — no re-authoring,
no re-derivation, no new invention.

## Scope covered

All **96 live cases** in suite 30286 (`**NEW** GV Test Suite`, project 42, sections 887831–887839:
ABT cEMV Taps, Multi-Use Barcode Validation, Passback, Commissioning & Router, Technician Menu, HMI
Screens, Resilience, Smoke) were pulled via `TestRailClient.get_cases(42, 30286)` (raw
`custom_preface` / `custom_preconds` / `custom_steps_seperated` / `custom_expected` / `refs`) and read
in full. **Not reached: 0** — every live case was classified. The ~57 pending-integration cases in
`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` were left untouched, as
instructed (proposal file, not TestRail).

## Classification

| Class | Count | Notes |
|---|---:|---|
| Already clean | 86 | Given/When/Then already terse; refs already hold the FBD/TIBU citations; Expected-result prose is the allowed short summary, no bare citations/attributions in body |
| Needed citation relocation | 10 | An FBD-##### or TIBU-##### reference (or a "Folds …"/"per FBD-…" note) was written directly into a precondition or the Expected-result prose, rather than living only in Refs |
| Needed sentence-to-tag compression | 0 | No case in this suite had the ABT-suite-style bloated full-sentence Given/And/Then prose (e.g. "the tester has confirmed…"); GV bodies were already short clause-per-line |

No case needed re-authoring, re-derivation, or invented content. This suite was already in
noticeably better shape than the ABT capping suite that motivated the mandate — consistent with the
GV coherence audit (`proposals/coherence-audit/gv.findings.md`), which found it "largely clean and
well-grounded."

## The 10 cases changed

Rewrite file: `proposals/coherence-audit/fixes/gv-terse-rewrite.rewrite.json`. Applied via
`tools/apply_rewrite.py proposals/coherence-audit/fixes/gv-terse-rewrite.rewrite.json --project 42
--commit` (dry-run first, then commit) against `TESTRAIL_WRITE_SUITE_ID=30286`.

| Case | Before (citation baked in body) | After (relocated) |
|---|---|---|
| **C4104053** Commissioning — both GV heads boot into service | Precond: "a lane commissioned **per FBD-100654** with the primary app zip…" | Precond: "a lane commissioned with the primary app zip…" — FBD-100654 was already in Refs, so the inline citation was simply dropped as redundant |
| **C4104091** Power — gate stays open, user in aisle | Expected: "…the gate remains open. **(pending integration — FBD-100348 FUN.)**" | Expected: "…the gate remains open. (pending integration)" — Refs updated to the more specific `FBD-100348 FUN` |
| **C4104092** Power — ≤2s power loss, no reboot | Expected: "…without a reboot. **(Folds TIBU-14160.)**" | Expected: "…without a reboot." — TIBU-14160 already in Refs, citation dropped from body |
| **C4104093** Emergency Release Button | Expected: "…without a reboot. **(pending integration; folds TIBU-16813/18635.)**" | Expected: "…without a reboot. (pending integration)" — both TIBU ids already in Refs |
| **C4104094** Heartbeat — loss raises major fault | Expected: "…raises a major fault. **(pending integration — FBD-100348 INT.)**" | Expected: "…raises a major fault. (pending integration)" — Refs updated to `FBD-100348 INT,FBD-100266` |
| **C4104097** BOS Comms — keeps validating offline | Expected: "…queues its audit data locally. **(Soft-failure principle, FBD-100359.)**" | Expected: "…queues its audit data locally. (soft-failure)" — FBD-100359 already in Refs |
| **C4104098** BOS Comms — queued data uploads on restore | Expected: "…Last Communication updates. **(Folds TIBU-16455/17104/18566.)**" | Expected: "…Last Communication updates." — Refs **extended** to add TIBU-16455/17104/18566 (these were not previously listed — relocated, not dropped) |
| **C4104099** SaaS — sustained outage → comms-locked OOS | Expected: "…Out of Service state. **(FBD-100359 hard-failure.)**" | Expected: "…Out of Service state. (hard-failure)" — FBD-100359 already in Refs |
| **C4104100** Heartbeat — 15-min Last-Communication update | Expected: "…even with no validations. **(Folds TIBU-18310 spamming theme.)**" | Expected: "…even with no validations." — Refs extended to add TIBU-18310 |
| **C4104101** Throughput — heads sustain back-to-back validations | Expected: "…blocking valid taps. **(needs-spec throughput; folds TIBU-18597/21005/16221 quick-succession theme.)**" | Expected: "…blocking valid taps. (needs-spec throughput)" — Refs extended to add TIBU-16221 (18597/21005 already present) |

No citation was deleted anywhere — every FBD/TIBU id that was in the body prose is either already in
that case's Refs field or was added to it in this pass.

## Audit result

`python -m system_test_ops audit --suite 30286` after commit: **CLEAN** — 0 blocking findings across
all 96 cases (mojibake 0, preface/preconds/steps/expected structural checks 0, compound-THEN 0,
stray-tags 0). 39 `title-too-long` advisories remain (pre-existing, out of scope for this pass — a
title-length concern, not a body-terseness one).

## Not touched

- The ~57 pending-integration proposal cases in `proposals/gv-suite-restructure/*.cases.yaml` (not
  live TestRail cases — out of scope per the task).
- Any other suite (10-2 project scope enforced by `TESTRAIL_WRITE_SUITE_ID=30286`).
- The 39 advisory `title-too-long` findings — titles were not shortened in this pass since the mandate
  is scoped to body text/citations, not titles; flagging here for a separate pass if wanted.
