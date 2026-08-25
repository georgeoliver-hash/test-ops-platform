# ABT/BOS back-office — gap register (Q&A loop for the engineer)

Per CLAUDE.md, a GAP/UNCONFIRMED marker is a **question**, not an end state. Each item below is put to
the engineer; the answer is cited back into the case (now grounded) and into `knowledge/`. A gap nobody
can answer is itself a finding — flagged **POSSIBLE SPEC/DESIGN BUG** and raised to Jira.

## P1 — POSSIBLE SPEC / IMPLEMENTATION CONFLICT (raise to Jira if unresolved)

### G1 — "All taps incl invalid" in the operator's customer-portal view (C4102867)
- **The conflict:** the confirmed fact says Journey History shows **valid journeys only** and there is
  **no portal view of "all taps including invalid"**. But two sources say the opposite, verbatim:
  - **PSPEC-0015 §3.3.6:** *"All taps will be visible even if the taps are not valid for the journey i.e.
    operators must be able to see, in their view of the customer portal, all valid and invalid taps
    (i.e. expired, pass back, deny list, etc.) made by the customer."*
  - **REQ-3498.0 (TFTS Requirements Matrix):** *"As a Transport Operator I want all taps (both EMV Media
    taps and ABT Smartcards taps) to be visible even if the tap is not valid for a journey, so that I
    can review potential issues. i.e. Expired, passback, deny list etc."*
- **Consequence:** the old case C4102867 was **not invented** — it is a faithful transcription of a real
  requirement. The rewrite honours the confirmed live behaviour (Journey History = valid only; invalid
  taps via Declined Taps report + Activity Log + audit), but the requirement must be reconciled.
- **Question for George / product:** is REQ-3498 satisfied by the Declined Taps report + Activity Log
  failed-validations view (requirement met via a different surface — the rewrite stands as-is), **or** is
  a combined operator "all taps incl invalid" view genuinely missing (an **unmet requirement / defect**
  to raise)? Answer decides whether C4102867 is final or a defect ticket is opened.
- **Also:** task-supplied citation "FBD-100662 para 264" does not resolve to a verbatim valid-only
  statement in v5.00; para 108 is the anchor used. Confirm or correct the paragraph.

## P2 — Portal status-label inconsistency (Debt Recovery)

### G2 — Recovered-card status label: "Active" vs "ACCEPTED" (C4102850, C4102851, C4102853, C4102854)
- FBD-100307 grounds deny-list **membership** and travel permitted/denied, **not** a portal status string.
  The suite uses **two different literals for the same recovered state**: C4102850/C4102853 say "Active";
  C4102854 said "ACCEPTED"; blocked state written as "Blocked".
- **Question:** what is the single correct Operator-Portal status label for (a) blocked/deny-listed and
  (b) recovered/re-enabled? Standardise all four cases once confirmed.
- **Related:** confirm the account/card **linkage model** ("linked cards on the same account both
  blocked/recovered together" — C4102850/C4102851) and where "expected number of authorisation requests"
  is displayed.

## P3 — Terminology / scheme scope

### G3 — "Visa MIT" terminology (C4102852)
FBD-100307 para 309 says "automated debt recovery per card-scheme rules"; "Visa MIT (merchant-initiated)"
is not in the cited spec. Confirm whether the test env specifically exercises the Visa MIT rail or keep
the case scheme-agnostic.

### G4 — Maestro pre-authorisation (C4102939, C4102940)
PSPEC-0015 §Initial Card Requests names only **"Mastercard"** for the daily / post-deny-removal pre-auth.
The originals said "MasterCard or Maestro". Confirm whether Maestro (a Mastercard-family scheme) follows
the same pre-auth rule before asserting it. Cases narrowed to Mastercard pending the answer.

### G5 — Issuer Liability figure (C4102937)
PSPEC-0015 states the UK Issuer Liability threshold is "now £10.00" (as of the spec date). Confirm the
current value configured in the test env before using £10.00 as the oracle.

## P4 — UI affordances not named in a spec (confirm on the live system)

| Ref | Case | Item to confirm |
|-----|------|-----------------|
| G6 | C4103031 | Exact live page/tab label — original "All Activities page" vs FBD-100358's "Activity Log". |
| G7 | C4103034 | Whether the Activity Log Barcode-ID filter exposes the four states "validated / printed / failed / invalid" (FBD-100358 grounds the filter + Transaction/Annulment applicability, not those four states). |
| G8 | C4102864 | Operator aftercare action set — is "cancel a query" an operator action? PSPEC-0015 §6.2.6 grounds view/manage/comment. |
| G9 | C4102866 | Existence of "Authorise All" / "Reject All" bulk buttons on the Authorisations page. |
| G10 | C4102931, C4102932 | Whether the Passenger Web Portal offers a **print** affordance for Journey/Transaction History. |
| G11 | C4102935 | Whether card replacement applies to issued ABT smartcards only (a cEMV bank card is the passenger's own, not operator-replaceable). |
| G12 | C4102868 | Exact live name of the quarantine surface (a "Quarantined Data" section exists in the suite); confirm the "journey tap service" component naming. |

## P5 — Scope / test-strategy note (not a behaviour)

### G13 — C4102855 is a QA-scope note, not a functional test
It defines the manual-vs-dev-test boundary (open-payment-bs service logs verified by automated dev tests,
not manual QA). Decide whether it belongs in the suite or in test-plan documentation, and confirm the
automated dev-test coverage for open-payment-bs actually exists.
