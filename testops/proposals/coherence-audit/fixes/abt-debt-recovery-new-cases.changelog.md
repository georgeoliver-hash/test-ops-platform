# ABT suite (30279) — debt-recovery cases from George's domain knowledge, 2026-07-24

**Scenario source:** George described this directly, not from a spec search (confirmed 2026-07-24):
a card taps £5.00, the payment fails and the card goes onto the Deny List. Two recovery paths, each
needing Visa AND Mastercard coverage:
1. **Automated recovery** — a later automated recovery cycle recovers a DIFFERENT amount than the
   original tap (George's example: £4.49, not £5.00) — recovery succeeds, card comes off the Deny
   List.
2. **Manual retry** — instead of waiting for automated recovery, the debt is manually retried via a
   portal — both the Operator Portal and the Passenger Portal.

Practical setup (George): the tester has DB access to adjust the original tap's timestamp and
recovery amount directly to reach the scenario — stated as the GIVEN in every case, rather than a
real-time wait.

## Existing-coverage check (done first, per docs/test-practices.md rubric)

Read the live suite (`TestRailClient.get_sections`/`get_cases`/`get_case`, project 42, suite 30279)
before authoring anything:

- **Section confirmed:** `ABT / Debt Recovery` is section id `887585` (direct child of `ABT`,
  887557) — matches `proposals/bos-abt-suite-restructure/structure.md`'s planned tree. Not nested
  under a "Functional" parent.
- **C4102852** ("Debt Recovery — automated Visa recovery clears a recoverable issuer-liability
  debt") and **C4104540** (Mastercard sibling, created in the earlier 2026-07-23 card-variant
  sweep) already test "automated recovery clears a recoverable debt, card returns to Active" —
  but generically, with no concrete worked example and no different-amount detail. **Extended in
  place** with George's £5.00 -> £4.49 example and the DB-access setup, rather than duplicated.
  (A third sibling, C4104541 Maestro, exists but is out of scope — George's task named Visa and
  Mastercard only.)
- **C4102934** ("Account Functions — retry a declined payment", section `ABT / Passenger Web
  Portal / Account Functions`, id 887597) already tests passenger-side manual retry
  (PSPEC-0015 §4.9.3 Customer Online Debt Recovery), but scheme-neutral and with no worked example.
  **Extended in place** for Visa (retitled `(Visa)`, following the same scheme-neutral-to-named-
  siblings pattern the automated-recovery family already uses); a **new** Mastercard sibling added.
- **No Operator Portal equivalent existed anywhere in the suite.** Checked `ABT / Operator Web
  Portal / Customer Services` (887590, the operator-side analogue of Account Functions) and swept
  the whole suite for "operator" + "retry" + "debt" — nothing. The only place operator-initiated
  retry was even named was inside C4102947's "four recovery triggers" summary line, with no
  standalone case. Genuinely new: 2 cases added (Visa, Mastercard), grounded in PSPEC-0015 §4.9.3
  (para ~11826-11837): "This process can also be initiated by the operator's customer service
  portal/agents on behalf of the customer... The operator agent can trigger the debt recovery
  process by clicking retry in the Operator portal."

## Result: 3 extended, 3 new (not 6 fresh duplicates)

| Path | Scheme | Action | Case |
|---|---|---|---|
| Automated recovery | Visa | **Extended** | C4102852 — retitled "...clears a debt at a different amount" |
| Automated recovery | Mastercard | **Extended** | C4104540 — retitled "...clears a debt at a different amount" |
| Manual retry — Passenger Portal | Visa | **Extended** | C4102934 — retitled "...retry a declined payment (Visa)" |
| Manual retry — Passenger Portal | Mastercard | **New** | C4104888 — "...retry a declined payment (Mastercard)" |
| Manual retry — Operator Portal | Visa | **New** | C4104889 — "Customer Services — operator retries a customer's declined payment (Visa)" |
| Manual retry — Operator Portal | Mastercard | **New** | C4104890 — "Customer Services — operator retries a customer's declined payment (Mastercard)" |

Every case's GIVEN states the £5.00 tap / deny-list setup and the DB-access practical detail; refs
cite `George (domain knowledge), 2026-07-24` for the scenario plus the relevant PSPEC-0015 section
for the mechanism (§4.9.1/Automatic Debt Recovery cadence already cited on the automated cases;
§4.9.3/Customer Online Debt Recovery, including the operator-triggered-retry paragraph, for the
manual-retry cases). No citation/date text was put in the case body (terse rule) — it lives only in
the Refs field.

## Push

`proposals/coherence-audit/fixes/abt-debt-recovery-new-cases.cases.yaml` ->
`python -m system_test_ops push --file proposals/coherence-audit/fixes/abt-debt-recovery-new-cases.cases.yaml --update`
(dry-run: 3 would-update, 3 dry-run-create, all in the correct sections) then `--commit`:
3 cases updated (C4102852, C4104540, C4102934), 3 cases created (C4104888, C4104889, C4104890).
No other suite touched; no old-suite cases touched.

## Re-audit

`push --commit` auto-runs the suite audit: **296 cases audited, 45 BLOCKING, 234 advisory** —
identical pre-existing blocking count to the baseline before this change (unrelated
`preface-bad-preamble` UNCONFIRMED-report findings and `then-compound-genuine` findings on other,
untouched cases). None of the 6 touched case ids (C4102852, C4104540, C4102934, C4104888, C4104889,
C4104890) appear under either blocking rule — 3 of the 6 appear only under the pre-existing advisory
`title-too-long` check (bracketed scheme suffixes push them over 72 chars, same pattern already
accepted on the sibling automated-recovery/card-verification cases). **This change added zero net
blocking findings.**

## Files touched

- `proposals/coherence-audit/fixes/abt-debt-recovery-new-cases.cases.yaml` (new, pushed live)
- `proposals/coherence-audit/fixes/abt-debt-recovery-new-cases.changelog.md` (new, this file)
- No changes to any other suite; no old-suite cases touched.
