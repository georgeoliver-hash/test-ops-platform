# POS mode-execution tagging — suite 30253, 2026-07-27

**Task.** Tag every case in suite 30253 (POS, project 42) with a Refs classification so a tester
running a mode's Configuration knows whether a shared case genuinely needs re-running under that mode
or can be run once under a chosen "primary" mode — per the mode-execution tagging scheme agreed with
George (see `proposals/pos-suite-restructure/mode-coverage.md` for the full reasoning and tally).

**Scope.** Refs-only field update. No preface/preconditions/steps/title changes. 601 cases (all cases
in suite 30253 excluding 100 `ZZ_DELETE_*`/bin-review cases already parked for the engineer's UI
clean-up).

## Method

1. Pulled the full suite live: `TestRailClient.get_cases(42, 30253)` (701 cases, full body incl.
   `refs`) and `TestRailClient.get_sections(42, 30253)` (93 sections) via a scratch script.
2. Built the section-path tree; excluded `ZZ_DELETE_*`-titled cases and the `Delete`/`ZZ - To Delete`
   section trees (100 cases, consistent overlap — confirmed no stray non-`ZZ_DELETE` case was hiding
   in those sections).
3. Cases filed directly under the top-level **NIR (Rail)** / **Ulsterbus** / **Metro** sections got
   the matching single tag automatically — no judgement needed (156 cases: 57 NIR, 45 Ulsterbus (32
   direct + downstream), 3 Metro handled as section defaults; final per-section counts in
   mode-coverage.md).
4. Every other case (Functional-Shared, Non-Functional, Smoke — 601 minus the direct-section ones) was
   read in full (title + preface + preconditions + steps + expected, not just the title) and
   classified against the rubric: does fare/product/payment/config content plausibly vary by mode
   (`MODE-ALL`, or the explicit 2-of-3 mode subset the case text itself names), or is it pure
   UI/menu/auth/hardware mechanics with zero fare dependency (`MODE-PRIMARY-ONLY`)? Screen Validation
   cases got an additional rule: default `MODE-PRIMARY-ONLY` (a render check doesn't depend on mode)
   with per-case override when the screen's own name is mode-specific (`_Metro`, `Ulsterbus …`,
   `Rail-…`, bare `Bus …`).
5. A meaningful subset of shared cases explicitly scope themselves to exactly two of the three modes
   in their own precondition text ("NIR or Ulsterbus mode… Metro is cash-only" / "Metro has no
   smartcard validation" / a bus-only concept like Fare Stage). These got **both** applicable
   single-mode tags together (e.g. `MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY`) rather than being forced into
   `MODE-ALL` (misleading — would send a tester to run it under a mode where the precondition can't be
   met) or `MODE-PRIMARY-ONLY` (would silently drop real per-mode coverage to a single run). This is a
   deliberate, evidence-grounded extension of the 5-tag scheme, flagged prominently in
   `mode-coverage.md` for George's awareness/sign-off.
6. Checked every case's projected new Refs value against TestRail's 250-character field limit (per the
   sibling HHD pass's finding) before writing — **0 of 601 POS cases would exceed 250 chars**, so no
   citation abbreviation was needed here.
7. Wrote the tag(s) via `TestRailWriter.update_case_fields(case_id, {"refs": new_refs})`, appending to
   the existing comma-separated Refs string (never overwriting existing REQ-/TIBU-/FBD- citations).
   Dry-ran a sample of 8 first (spanning cases with no existing refs, single refs, and multi-refs) and
   confirmed the append logic before running for real. `$env:TESTRAIL_WRITE_SUITE_ID=30253` set for
   the whole pass; writer's suite-lock verified every target case's section belongs to 30253.
8. Committed for real: `python scripts_scratch_tag.py --commit` (all 601 rows).

## Tally (see `mode-coverage.md` for the full section-by-section breakdown)

| Tags | Count |
|---|---:|
| `MODE-PRIMARY-ONLY` | 294 |
| `MODE-NIR-ONLY` | 105 |
| `MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY` | 49 |
| `MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY` | 54 |
| `MODE-ULSTERBUS-ONLY` | 46 |
| `MODE-ALL` | 46 |
| `MODE-METRO-ONLY` | 7 |
| **Total** | **601** |

## Judgment calls flagged (not guessed past the evidence — see mode-coverage.md for detail)

18 cases got a real, evidence-based classification that still rests on an inference worth a second
pair of eyes: the Barcode Scanning/Validation family (12 cases, reclassified `MODE-NIR-ONLY` on
consistent Rail-only worked examples, though no case states the exclusion outright), the 3 Fare-Stage
Selection cases (bus-only concept), the Default Boarding Stage case (possible Metro coverage gap), the
generic Customer Display case (kept `MODE-ALL` rather than guessed as the "missing Metro variant"),
and the Ulsterbus-POS-selling-rail Revenue Allocation case.

## Verification

- Independently re-fetched the live suite after commit (`TestRailClient.get_cases(42, 30253)`): 601 of
  701 cases now carry a `MODE-` tag in `refs` (matches exactly: 701 total minus the 100 excluded
  `ZZ_DELETE_*`/bin-review cases). Cross-checked all 601 write results against the classification plan
  — 0 mismatches between the intended `new_refs` and what TestRail returned.
- `python -m system_test_ops audit --suite 30253` after commit: **CLEAN** — 601 cases audited, 0
  blocking findings across every rule, 65 advisory (18 title-no-emdash, 47 title-too-long — pre-existing,
  unrelated to this change). Refs-only edits, as expected, had zero effect on the conformance rules
  (preface/preconds/steps/expected/title all untouched).

## Result

601 cases tagged, 0 skipped (none already carried a MODE- tag going in), 0 refs-length overflow (checked
every case's projected new Refs against TestRail's 250-char limit before writing — see sibling HHD-pass
note above). Old suite 9317 untouched throughout — no client write methods exist for it, and the writer
refused any target outside suite 30253 by construction. Audit result: **CLEAN**.
