---
description: Run the standard-conformance audit on a suite (read-only) and explain any findings. Usage: /audit <project> <suite-id>
argument-hint: <project> <suite-id>
---

Lint a suite against the Gherkin standard. Arguments: `$ARGUMENTS` (`$1` = project, `$2` = suite id;
defaults to `TESTRAIL_WRITE_SUITE_ID` if `$2` omitted).

1. Run `python -m system_test_ops audit --suite $2 --no-gate`.
2. Summarise the per-rule read-out: **blocking** findings (mojibake, missing objective/preconds,
   malformed When/Then, genuine compound THEN, stray tags) must be 0; the two **title** checks
   (length, em-dash) are advisory and often intentional (bare product names / exact screen names).
3. For any blocking finding, name the case ids and the exact fix (e.g. split a compound THEN into
   `**AND**`), and offer to apply it. The full report is at
   `reports/<project>/<suite>/<date>/alignment-audit.md`.

Definition of done for any authoring change: this audit is **CLEAN of blocking**. Read-only.
