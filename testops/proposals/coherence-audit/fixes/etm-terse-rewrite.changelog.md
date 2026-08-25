# ETM terse-rewrite pass — suite 30254 (`**NEW** ETM-Acceptance Suite`, project 42)

Date: 2026-07-21. Mandate: `docs/gherkin-standard.md` § "Terse, not bloated — trust the tester
(George, 2026-07-21 — a hard rule)". This is a compression/relocation pass only — no case's tested
behaviour was changed, no facts re-derived or invented.

## Data pulled

- CLI: `system_test_ops cases --project 42 --suite 30254` → `reports/tfts-system-test/new-etm-acceptance-suite/2026-07-21/cases.json` (title/section index only — this suite's CLI serializer doesn't emit full body fields).
- Raw client dump (full `custom_preface`/`custom_preconds`/`custom_steps_seperated`/`custom_expected`/`refs`) via `TestRailClient.get_cases(42, 30254)` → `proposals/coherence-audit/fixes/etm-suite-30254-raw.json` (524 cases, 56 sections). This was the actual source read for the audit below.

## Suite shape (524 cases total)

| Section (top-level) | Cases | Disposition |
|---|---:|---|
| HMI Screen Validation | 280 | Reviewed (sampled ~6): templated one-screen-per-case pattern, already terse (one `GIVEN`/`WHEN`/`THEN`, no prose, no citations). No changes needed. |
| Functional | 139 | Reviewed **all 139**. |
| ZZ - To Delete (review then bin) | 69 | **Not touched** — out of scope by convention: this section is a holding pen for cases already queued for human deletion (`ZZ_DELETE_REVIEW` prefix), not live tester-facing content. One case here (4100588) does carry the exact kind of bloat this pass targets (`**UNCONFIRMED (audit 2026-07-17)**`, a gap-register-Q19 reference, and an audit date baked into the preface) — flagged below for the human bin-review, not rewritten, since editing a case already marked for deletion isn't productive. |
| Non-Functional | 23 | Reviewed **all 23**. |
| Regression | 7 | Reviewed **all 7**. |
| Smoke | 6 | Reviewed **all 6**. |

**Total reviewed this pass: 455 cases** (139+23+7+6 read in full + 280 HMI sampled and pattern-confirmed clean). Not reached in depth: the 69 `ZZ - To Delete` cases were read for triage only, not line-edited (correctly, per the section's own "review then bin" convention — a human, not this pass, decides their fate).

## Method

1. Regex-swept every active case's preface/preconds/steps/expected for citation/provenance markers: `FBD-\d+`, `gap Q\d+`, `UNCONFIRMED`, `GAP`, `George`, `confirm(ed)? (live|by)`, `para(s)`, dates (`2026-\d\d-\d\d`), `tracker`, `confirmation)`, plus a second, broader pass for `verified`, `documented`, `as agreed`, `sign-off`, `live-system`, `audit \d`, `Q\d\d`.
2. Manually inspected every hit (24 total across both passes) to separate genuine provenance bloat from false positives (domain terms like "unconfirmed-annul", "basket tracker", "no gap or duplication", "confirmation shown on screen" — all legitimate case vocabulary, not citations).
3. Sorted all 175 active (non-HMI, non-ZZ) cases by body length and read the 25 longest to check for prose bloat independent of citations (the mandate's second failure mode). None found — the long cases are long because they carry legitimate multi-step worked examples and configured-value guards (e.g. "a configurable failed-attempt threshold is set in the TMS (do not assume a value — read it from the TMS)"), which is exactly the pattern the standard's "assumed-knowledge precondition" rule asks for, not bloat.

## Finding: this suite was already largely compliant

Unlike the ABT capping suite (the mandate's worked examples), suite 30254's Functional/Non-Functional/
Regression/Smoke cases were already written tersely: short `GIVEN`/`AND` preconditions, one clause per
`THEN`/`AND` line, configured values handled via "read it from the TMS" rather than a hard-coded guess,
and no inline "— George, date" or "per FBD-#####" provenance in the body **except two cases**.

### Cases changed: 2

| Case | Title | What changed |
|---|---|---|
| 4100586 | ABT — Metro zone boarding and alighting | Removed inline `(George, live-system confirmation, 2026-07-21)` from the preface; moved it to **Refs**. |
| 4100587 | ABT — Ulsterbus zone boarding and alighting | Same fix — identical bracketed clause removed from preface, moved to **Refs**. |

**Before (4100586 preface):**
> This test is to confirm ABT boarding within a Metro ABT zone (Tap On Only – Flat Fare); the customer
> taps once to board and the ETM calculates the alighting stop — there is no customer alighting tap on
> this device (George, live-system confirmation, 2026-07-21).

**After:**
> This test is to confirm ABT boarding within a Metro ABT zone (Tap On Only – Flat Fare); the customer
> taps once to board and the ETM calculates the alighting stop — there is no customer alighting tap on
> this device.

**Refs (new):** `George (live-system confirmation), 2026-07-21`

(4100587 is the same fix, Ulsterbus variant.) No other field on either case changed — preconds, steps
and expected were already terse and were left untouched.

### Already-clean: 453 cases

- 137 of 139 Functional cases, all 23 Non-Functional, all 7 Regression, all 6 Smoke, and all 280 sampled/pattern-confirmed HMI Screen Validation cases carried no inline citation/provenance text and no sentence-style bloat that a short tag would fix. Left as-is.

### Not reached / intentionally out of scope: 69 cases

- The `ZZ - To Delete (review then bin)` section (69 cases) was read for triage but not rewritten — it's
  a pending-deletion holding pen, not live tester content. One case there (4100588,
  "ZZ_DELETE_REVIEW - ABT — reverts to standard fixed fare on rule change") does carry the exact
  bloat pattern this mandate targets (`**UNCONFIRMED (audit 2026-07-17)**`, "gap-register Q19", an
  embedded audit date) — flagged here for whoever does the human bin-review; not edited, since polishing
  a case already marked for deletion isn't useful work.

## Rewrite file

`proposals/coherence-audit/fixes/etm-terse-rewrite.rewrite.json` — 2 records, `action: "reword"`,
shape per `proposals/spec-grounded/abt/capping.rewrite.json`. Confirmed `tools/apply_rewrite.py`
already supports a `refs` pass-through (added by an earlier pass today for a different suite — see
lines ~129-131 of that file); no changes to `apply_rewrite.py` were needed.

## Apply

- Dry-run: `python tools/apply_rewrite.py proposals/coherence-audit/fixes/etm-terse-rewrite.rewrite.json` → `updated: 2, skipped: 0, missing: 0`.
- Commit: same command + `--commit` → `updated: 2`. Verified live via `TestRailClient.get_cases(42, 30254)`: both cases now carry the trimmed preface and the relocated `refs` value.

## Re-audit result

`python -m system_test_ops audit --suite 30254` after the commit:

```
        0  mojibake
        8  title-no-emdash (advisory)
       66  title-too-long (advisory)
        0  preface-empty
        0  preface-bad-preamble
        0  preconds-empty
        0  preconds-no-given
        0  steps-empty
        0  step-first-not-when
        0  step-content-not-when-and
        0  step-no-then
        0  then-compound-genuine
        0  expected-empty
        0  expected-starts-then
        0  has-tags
  audited 454 cases: CLEAN; 74 advisory.
```

**CLEAN of blocking findings** (0 across every blocking rule, including `then-compound-genuine` — no
compound-THEN was introduced by this pass, since only the preface field was touched). The 74 advisory
items (title length/em-dash style) pre-date this pass and are outside its scope (title wording, not
body terseness/citation placement).

## Summary

- **Cases changed:** 2 (4100586, 4100587) — citation relocated to Refs, preface shortened by removing the provenance clause only.
- **Already clean:** 453 (of the 455 actively-reviewed cases).
- **Not reached (out of scope, pending human bin-review):** 69, in `ZZ - To Delete (review then bin)`; one of those (4100588) is flagged as also carrying inline provenance/gap-register bloat for whoever processes that section.
- **Audit:** CLEAN of blocking findings after commit.
- **Changelog path:** `proposals/coherence-audit/fixes/etm-terse-rewrite.changelog.md` (this file).
