# ABT + BOS conformance gate — first pass, 2026-08-06

**Discovery.** While preparing to run the flow-map correctness process on ABT/BOS, found that neither
suite (30279 ABT, 30287 BOS) had ever been through `python -m system_test_ops audit` — the standard
conformance gate that POS/ETM go through on every push. All the July 2026 coherence-audit work on
these suites was **content grounding** (spec-correctness), a different dimension from **format
compliance** (the house Gherkin standard). The two were never reconciled for these two suites.

**Result before fix:** ABT 45 blocking findings / BOS 48 blocking findings (out of 297 and 191 cases
respectively) — almost entirely `preface-bad-preamble` (objective doesn't start with "This test is to
confirm"), plus a handful of genuine compound-THEN.

## preface-bad-preamble (86 cases: 40 ABT + 46 BOS)
Root cause: every `**UNCONFIRMED**`-marked case (mostly the "Report" and "[UNCONFIRMED]"-titled
cases from the reporting-catalogue sweep) put the UNCONFIRMED marker at the START of the objective
field instead of after a compliant lead sentence — same house-style requirement ETM's cases follow
(see `correctness-fixes-2026-08-05.cases.yaml` for the pattern used there too). Fixed mechanically:
prepended `This test is to confirm the behaviour of "<title>".` before the existing preface text on
all 86 cases via `TestRailWriter.update_case_fields` (partial-field patch, preconds/steps/expected
untouched). One case (C4102855, "Debt Recovery...") needed manual wording cleanup after the mechanical
pass produced an awkward mid-sentence capitalisation.

## then-compound-genuine (6 cases: 4 ABT + 2 BOS)
C4102818, C4102822, C4102865, C4103488 (ABT); C4104259, C4104322 (BOS) — each had a THEN line
asserting two distinct outcomes joined by "and" instead of a separate AND line. Split by hand (steps
were too varied to template) — see `custom_steps_seperated` on each case for the corrected form.

**Verified:** both suites now audit CLEAN (0 blocking; 236 ABT / 67 BOS advisory titles, same
pre-existing title-length/em-dash items every other suite carries — not actioned, same as elsewhere).

**Lesson for the department standard:** any suite that goes through spec-grounding/content work should
ALSO run `python -m system_test_ops audit` before being called done — content-correctness and
format-conformance are independent checks and neither substitutes for the other.
