# Alignment audit — GG - POS - Claude Suite (verdict)

Last run: 2026-06-03. Tool: `python tools/audit_suite.py` (read-only conformance linter, reusable
for any suite). Live cases audited: **531** (52 `ZZ_DELETE_DUP` dupes excluded — pending manual bin).

## Headline

The suite is **aligned to `docs/gherkin-standard.md`**. Every substantive rule passes with **0**
findings:

| Rule | Findings |
|------|---------:|
| Residual mojibake | 0 |
| Objective empty / not "This test is to confirm…" | 0 |
| Preconditions empty / no GIVEN | 0 |
| No When→Then step / first step not WHEN / WHEN with no THEN | 0 |
| **Genuine compound THEN (two distinct outcomes on one line)** | **0** |
| Expected empty / restated THEN | 0 |
| Tags written into the case | 0 |

Only two **intentional** categories remain (37 total), reviewed and accepted — see below.

## What this pass fixed

- **Compound-THEN split.** A first pass flagged 356 THEN lines containing "and". Refined detection
  (strip parenthetical/noun-list "and"; require a second *predicate*) isolated **15 genuine**
  two-outcome THENs. All 15 were split into `THEN … / AND …` (e.g. "displayed and printed" →
  "displayed" / "is printed"; "cleared and success is reported" → "cleared" / "success is
  reported"). Applied to live and mirrored into the source YAMLs. The other 341 are valid
  declarative Gherkin (a single observable check that happens to list attributes — e.g. "the screen
  matches the approved design (layout, wording, labels and colours)") and are **correct as written**.
- Earlier in the same recovery: repaired mojibake in 13 specs, re-applied 5 missed splits to the
  real cases, and flagged 52 accidental duplicates `ZZ_DELETE_DUP` for binning.

## Residual findings — reviewed, intentional (not defects)

- **Title over 72 chars (24).** Almost all are `Screen Validation — <exact UI screen name>` cases.
  The title deliberately mirrors the approved-design screen name **1:1** for traceability;
  shortening would break that mapping. Left as-is. (One non-Screen case, `C4099982 Bus FLU — sell a
  ticket: route number, boarding/alighting stages, fare type, basket`, could be trimmed to
  "Bus FLU — sell a ticket" with the detail in steps — optional.)
- **Title without an em-dash separator (13).** Bare product names under a `Tickets` / mode section
  (Single ticket, Day Return ticket, iLink Single, Warrant Return, Family & Friends, Weekly/Monthly
  Season, 3 Day Select, Bus Rambler, Jobseeker Single, Rail Substitution Service, etc.). The parent
  section supplies the feature context, so the bare product name is scannable and unambiguous.
  Left as-is pending a call on whether to prefix them (e.g. "Tickets — sell a Single").

## How to re-check

`python tools/audit_suite.py` (uses `TESTRAIL_WRITE_SUITE_ID` from `.env`; `--suite <id>` for any
other suite). Read-only; writes the full report to `reports/alignment-audit.md`.
