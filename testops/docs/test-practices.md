# Test practices — the mindset for every decision

This is the governing rulebook for the whole repo. Every time we look at a flow path, an old case, a
requirement, or a past defect, we ask the same question through a proper test-engineering lens:
**does a test already cover this — and if not, what is the *minimum, well-structured* test that
does?** We are consolidating and optimising, not transcribing flows into cases or writing one test
per bug.

These practices are **device- and project-agnostic**. They apply to POS, TVM, BV, ETM, a new device,
a new project — anything.

## Audit first — non-negotiable

Before changing **anything** in a department suite, complete a full, **evidence-based** audit and
analyse it more than once. Guessing — e.g. assuming a product is shared vs mode-specific — risks
hindering real test results. The audit is not optional and not a one-pass skim:

1. **Old suite** — inventory every section/folder; **cross-tabulate** products/behaviours against
   the dimension that matters (e.g. product × operating mode) to *prove* what is shared vs specific.
   Don't infer from names; count where each thing is actually tested.
2. **Documentation / requirements** — read the specs the cases trace to (e.g. REQ-####).
3. **UX designs** — confirm per-mode/flow differences from the design source (e.g. Overflow).
4. **Re-analyse** — review the audit again before proposing changes; record it (e.g. an
   `old-suite-audit.md`) so decisions are traceable and reviewable.
5. **Run history informs, never gospel.** Use it to prioritise and to justify retiring dead cases —
   but "not run" ≠ "not needed": recently-added cases won't have a run yet. Note: TestRail
   **test-plan runs are NOT returned by `get_runs`** (walk `get_plans`/`get_plan`), so check plans too.
6. **Case-title-level sweep.** The section tree + run data hide behaviours that live only in case
   titles (especially recent additions). Before finalising, read **all** old case titles (set aside
   the obvious matrix, review the rest deduped) so no needed behaviour — for **either operating
   mode** — is dropped. Record the old→new mapping (e.g. a `coverage-map.md`).

Only after the audit is done and confirmed do you propose add/edit/merge/leave changes. If you find
yourself writing "I think X is shared" without a cross-tab to back it, stop and do the audit.

## The "do we need a new test?" decision rubric

Run every candidate (a flow path, a requirement, a defect, an old case) through this in order:

1. **Is the behaviour already exercised by an existing case?**
   → If yes, **do not add a test.** Either it's already covered (link the requirement/defect via
   Refs and move on), or it needs a small **extra step/assertion** added to that case to nail the
   behaviour. Extending beats duplicating.
2. **Is it just another value in a class the case already covers?** (equivalence partitioning)
   → If yes, **no new test** — it's the same partition. Add a boundary value only if the boundary
   itself carries risk (boundary value analysis).
3. **Is it a genuinely distinct behaviour, path, or risk not exercised anywhere?**
   → **Yes → new case**, placed in the functional area that owns the behaviour.
4. **Is it a fixed defect (e.g. a TIBU bug)?**
   → If the scenario is already exercised, **fold a regression assertion** into that case and link
   the defect via Refs. Only write a dedicated `@regression` case when nothing covers the scenario.
   Never create one case per bug as a reflex.
5. **Is it a step *within* a flow you already test?**
   → A sequential flow (sign-on → duty → route → journey → confirm) is **one test walked
   end-to-end** — a step (with a screen check) per stage — **not** one case per screen or per step.
   Fold the steps into the flow test. Split out only a genuinely distinct **scenario/branch** (error
   path, lockout, abandon, an "unavailable" fallback) or a **mode-specific** divergence.
6. **Is the old case obsolete / always-failing-and-invalid / superseded?**
   → **Leave it** (don't carry it over). Cross-check with run history before deciding.

The default answer is **"no new test"** unless step 3 or a true step-4 gap forces one.

## Structure by flow/risk, not by screen (the consolidation lens)

The most common over-fragmentation is **one case per screen or per step**. Apply this lens to every
functional area, on the initial build *and* whenever the suite is touched:

- A **functional** test = one user flow or one risk, walking the screens it touches and asserting
  each as it passes. Test *multiple screens' behaviour inside the flow that uses them*.
- **Every genuinely distinct variant gets its own separate, individually-executable case — never a
  "Data variations:" list substituting for real coverage (George, 2026-07-24, a hard rule,
  superseding the earlier "ride as a data-variation line" guidance below).** If a card scheme,
  smartcard/entitlement type, payment method, or credential (Visa Debit, Visa Credit, Mastercard
  Debit, Mastercard Credit, Maestro, ITSO, a specific concession sub-type, …) can fail independently
  of its siblings, it needs its own case that gets its own pass/fail — "a failure can occur on one
  card and not another; we can't tap one smartcard and say it's all working" (George). A bullet list
  named inside one case's Expected/preconditions is not equivalent to separate, trackable coverage —
  it reads as tested but only one example ever actually gets executed. This applies everywhere this
  pattern shows up: payment schemes, smartcard/ITSO/entitlement types, ticket products — anywhere a
  named list of variants currently substitutes for a set of cases. It mirrors the same logic as the
  Operator-Portal/Passenger-Portal split (duplicate the test into each context, not one case that
  claims to cover both) — same test, once per variant, filed together so the set is obviously
  complete. Genuine **operating-mode** coverage (NIR/Ulsterbus/Metro, Glider/Rail) is unaffected —
  that's still handled via TestRail **Configurations** running the same case, not a data line, per the
  rule below on single-source-of-truth-across-variants; the practice this replaces is only the
  in-body "Data variations: X, Y, Z" list.
- **Author sibling variants adjacent, in one batch, grouped by family (colleague feedback via
  George, 2026-07-24).** When a variant family gets expanded into separate cases (e.g. Visa Debit,
  Visa Credit, Mastercard Debit, Mastercard Credit, Maestro), push them together, in a sensible
  grouped order (same scheme next to each other), so they land adjacent in the TestRail section by
  creation order. **This TestRail instance's API does not support reordering cases after the fact**
  (`display_order` writes are silently accepted but don't take effect — confirmed by direct test) —
  the only fix post-hoc is a manual drag in the UI, same limitation as section/suite moves. Get the
  order right at authoring time; don't rely on being able to tidy it up later.
- A dedicated **per-screen layer** (e.g. an `HMI Screen Validation` section) is the right home for
  "does each screen render to design" — so the functional layer never fragments into a case per
  screen. The two layers are complementary: HMI proves each screen renders; Functional proves the
  flows that use them behave.
- **Consolidation pass (run it when auditing any suite):** per area, list the groups of cases that
  are really *one flow's steps* or *one behaviour's variations*; fold each group into a single flow
  test (enrich its steps); retire the absorbed cases (rename `ZZ_DELETE_REVIEW`, move to a
  `ZZ - To Delete` section, bin via the UI). A good suite **shrinks** as flows are recognised — same
  coverage, fewer and clearer tests.
- **Consolidation must preserve completeness — "shrinks" never means "loses" (George, 2026-07-22, a
  hard rule).** Folding cases together is only correct when every genuinely distinct thing the old
  suite/spec required is still traceable afterward — as its own case, or as a named line in a
  `Data variations:` list. It is **not** correct when a fold silently drops a real card type, decline
  reason, entitlement, role, or mode variant just to make the count smaller. After ANY big
  consolidation (especially the initial build of a new suite from a large old one), run a dedicated
  **consolidation-completeness check**: walk the old suite's cases grouped by family (card/product
  types, decline/error reasons, roles × sign-on methods × operating modes, payment methods), and
  confirm every distinct member is named somewhere in the new suite. Anything genuinely missing gets
  written back in (grounded on the old case's real content + spec, never invented) — this is not
  optional cleanup, it's part of the initial build being *done*, and it's exactly as required after
  onboarding a brand new device as it was for the suites rebuilt so far.

## Core principles for a good test case

- **One behaviour per case.** Title states the observable outcome. If the title needs "and", it's
  probably two cases.
- **Independent & atomic.** A case sets its own preconditions (`Given`) and doesn't depend on another
  case having run first. Reset to a known state.
- **Deterministic & repeatable.** Same inputs → same result. No reliance on timing luck or leftover
  state. Flaky = a defect in the test.
- **Observable, specific expected results.** "Then the X screen shows Y" — never "Then it works".
- **Positive, negative, and boundary coverage** for each behaviour — the happy path *and* the error
  /edge branches (these are where the old suite and most suites are weakest).
- **Right altitude.** Test user-observable behaviour, not implementation detail; don't test the
  framework or the device OS.
- **Clear, consistent structure & naming** (see `gherkin-standard.md`) so any engineer can read any
  suite as if one person wrote it.

## Coverage & traceability

- **Risk-based.** Spend cases where failure hurts most (payment, audit/BOS, lockout, money/top-up),
  not uniformly. Smoke = the thin critical path; functional = breadth; non-functional = resilience.
- **Minimal sufficient set.** Maximise behaviours covered per case; minimise total case count.
  Duplication is a maintenance tax and erodes trust.
- **Traceability via the Refs field, not the title.** Every case links to its requirement(s)
  (`REQ-####`) and any defect(s) it pins (`TIBU-####`). That makes "is requirement X covered?" and
  "is bug Y pinned?" answerable — which is the whole point of the coverage/audit workflow.
- **Single source of truth across variants.** Where behaviour is identical across operating modes /
  configs, write it **once** and run it under TestRail **Configurations** — don't copy a case per
  mode. Fork only at the case that genuinely differs.

## Conformance audit — runs for everyone, all the time

Audit-first (above) is about *what* to cover. The **conformance audit** is about *how every case is
written* — and it is a standing, automated gate, not a one-off cleanup. It belongs to the process,
so any engineer or fresh session inherits it without being told twice.

- **What it is.** `python -m system_test_ops audit [--suite <id>]` lints every case in a suite
  against `gherkin-standard.md`: objective preamble, GIVEN preconditions, a real When→Then with one
  When, no **genuine compound THEN** (two distinct outcomes on one line — a noun list inside one
  observable check is fine), prose Expected, no tags written into the case, and no encoding mojibake.
- **When it runs.** `push --commit` runs it automatically on the target suite and prints a per-rule
  read-out. Run it manually any time. It writes a full report to
  `reports/<project>/<suite>/<date>/alignment-audit.md`.
- **Blocking vs advisory.** Blocking findings (everything except the two title checks) must be **0**
  before a change is considered done / a PR is opened — the command exits non-zero so it can gate a
  PR or CI. The title checks (length, em-dash separator) are **advisory**: sometimes a title is
  deliberately a bare product name or mirrors an exact UI screen name for traceability — review and
  keep those.
- **Definition of done.** A suite you have edited is not done until its audit is **CLEAN of blocking
  findings**. Treat a non-clean audit as unfinished work, same as a failing test.
- **Encoding note.** Never rewrite the `*.cases.yaml` specs with PowerShell `Set-Content`/`Out-File`
  — they re-encode UTF-8 and corrupt punctuation into mojibake, which breaks `push`'s title-match
  and creates duplicates. The audit flags residual mojibake; rerun it after any bulk edit.

## Deep grounding audit — beyond conformance (required for a new suite, not just later cleanup)

The **conformance audit** above checks *how* a case is written (format, wording, no compound-THEN).
It does **not** check whether what the case *claims* is actually true. That's a separate, required
pass, learned the hard way (2026-07-21/22, every Translink suite): a case can be perfectly
well-formatted and still assert a capability that doesn't exist on the real device/portal, cite the
wrong spec document, or carry a citation nobody actually verified. Two real examples from that pass:
a case claimed a customer could "print" Journey History, sourced from a *different customer's*
deployment manual, not Translink's own spec (turned out to be genuinely correct once the right
Translink-specific doc was found — but only checking proved that); 15 TVM payment cases all cited a
spec document that, read in full, turned out to be about something else entirely (terminal-credential
allocation, not EMV/PIN/contactless at all).

- **What it is.** For every case: read its actual claim, check whether its cited source (if any)
  genuinely supports that specific claim (a citation existing is not proof it was checked), and if
  not, search the real spec/old-suite/UX-flow library properly before either regrounding it or
  flagging it `**GAP**`/`**UNCONFIRMED**` (never invent, never silently leave a wrong claim standing).
- **When it runs.** As part of the initial build of any new suite (not deferred to "later") — spec-
  grounding at authoring time is cheaper than finding it wrong after the suite is live. Also re-run
  whenever a suite hasn't had one yet, or after any big consolidation (pairs naturally with the
  consolidation-completeness check above — do them together).
- **The gap-register Q&A loop is mandatory, not optional, for anything that can't be grounded.** See
  CLAUDE.md's "gaps trigger a Q&A loop" rule and `.claude/commands/resolve-gaps.md`. Before putting a
  question to the engineer, **exhaust every existing source first** (old suite, spec library, UX/
  Overflow flow annotations, a broader/deeper re-search, JIRA ticket full history not just the
  preamble) — a large share of "unconfirmed" questions turn out to be answerable from evidence that's
  already sitting in the repo/library and nobody had searched for by the right name yet (e.g. a REQ-id
  index spreadsheet that resolved dozens of questions once someone found it). Only genuinely
  unanswerable-from-any-document questions should reach the engineer.
- **Section/folder structure drift is part of this too.** A big consolidation often creates new
  sections at different times without checking the existing tree — leading to inconsistent nesting
  (a family's cases split between a top-level section and a nested one). Check the live section tree
  against the suite's own `structure.md` as part of this pass. This TestRail instance's API can create
  a section in the right place but cannot move/re-parent an existing one — so the fix is: create the
  correctly-nested section, migrate the case content into it, and flag the old one's cases
  `ZZ_DELETE_REVIEW` for the engineer's normal UI bin-cleanup. Never ask the engineer to manually
  drag-and-move cases as the primary mechanism.

## Test-ops team practices

- **Version control is the team contract.** The suite design, standards, knowledge, flows, and
  registers live in this repo; changes go through review (PR), so every project converges on the
  same conventions.
- **Read-only / propose-first against TestRail.** We analyse and propose; a human applies. Old suites
  are never edited or deleted from — we copy out into the new suite.
- **Peer review every change** against the standard (`standards-keeper`) before it lands.
- **Maintain, don't just add.** Periodically run the run-history review to retire always-failing/
  dead cases and catch flakes — the suite should shrink as often as it grows.
- **Regression discipline.** Every fixed defect ends up pinned by a case (folded or dedicated) and
  linked via Refs, so it can't silently return.
- **Evidence over assertion.** Every coverage/health claim cites a case id, run id, requirement, or
  defect. No uncited verdicts.

## How the agents apply this
- `coverage-analyst` uses the rubric to classify covered / partial / missing / stale and to avoid
  proposing duplicates.
- `run-historian` flags dead/flaky/always-failing cases so we retire rather than carry them.
- `gherkin-author` writes to `gherkin-standard.md` and only drafts what the rubric says is genuinely
  needed.
- `standards-keeper` enforces structure, consistency, and traceability at review time, and **runs
  the conformance audit** (`system_test_ops audit`) on the target suite as part of every review —
  reporting blocking findings and confirming the suite is clean before a change lands.
