# Deep audit — suite 30279 (`**NEW** BOS & ABT Suite`), 2026-07-22

## Verdict

**Full coverage achieved of all 391 in-scope live cases** (496 total minus the 105 already-condemned
`ZZ_DELETE_REVIEW` cases in the `Delete` section, out of scope per the brief). 165 cases corrected/
grounded, 226 verified clean, 13 new gap-register questions logged (Q25-Q37), 2 existing gaps
(Q3/Q14/Q21) applied to close out stale markers. Audit blocking-count **unchanged at 89** (no
regressions from 165 field changes across 6 commits). The flagged Passenger Web Portal print/download
question is **resolved**: "print" was correct all along.

## The headline finding: Journey/Transaction History "print" vs "download"

C4102931/C4102932 claimed customers can "print" their Journey/Transaction History. Authored
2026-06-24, never grounded in any of the six prior spec-grounded rewrite passes on this suite. George
suspected "download" was correct and asked for it to be resolved against Translink-specific sources,
explicitly not guessed either way if nothing definitive turned up.

**Resolved: "print" is correct.** `PSPEC-0015 - Product Specification - CloudFare - ABT v4.2.1.pdf`
— the base CloudFare ABT product spec, filed in the Translink requirements library alongside the
Translink Cloudfare manual (not the Laval manual, which is for a different deployment and was
correctly excluded) — Figure 51 "web/mobile app portal functionality for customer" explicitly lists:

> **"View (and print) Transaction History"** (para 13555)
> **"View (and print) Journey History"** (para 13714)

for both Anonymous and Registered accounts. No wording change was needed on either case — only the
missing Refs citation (both had none before). A separate "download in Excel/CSV" feature does exist
in the same spec (para 15374) but applies to **Transaction** data specifically, for expense purposes —
an addition, not a replacement for print. George's "download" suspicion is not supported by any source
found and was not applied. Logged as gap-register **Q27, ANSWERED**.

Grounding the rest of the never-audited Passenger Web Portal section surfaced one further open
question: C4102927's "journeys in the previous seven days" sign-on precondition conflates sign-on
eligibility with a different, confirmed fact (the 7-day figure governs the post-sign-on *history view
window*, not sign-on itself) — marked `**UNCONFIRMED**`, logged **Q26**, linked from its sibling
C4102928.

## George's spot-check: C4102766

Fixed a backwards WHEN (attempt-before-open, reordered) and surfaced a genuine unconfirmed premise —
FBD-100662 §5.6 never states whether a CR122 correction option is even exposed for a **declined**
journey. Marked the attempt `**UNCONFIRMED**` (Q25); the asserted safety outcome is kept either way.
Its 33 CR122-capping siblings were swept for the same risk and are all clean (every one performs a
real correction on a settled journey).

## Coverage by section

See `proposals/coherence-audit/fixes/abt-deep-audit.changelog.md` for the full section-by-section
table (391 cases, 0 not-reached) and the complete list of new gap-register questions (Q25-Q37).
Summary:

| Area | Cases | Corrected | Clean |
|---|---|---|---|
| Passenger Web Portal + Tap Correction (this session, direct) | 44 | 9 | 35 |
| Annulment/Duplicate/Journey History/Late Taps/Update Stop/Debt Recovery | 70 | 43 | 27 |
| Operator Web Portal + remaining ABT Functional | 102 | 48 | 54 |
| CloudFare (all sub-sections) | 110 | 29 | 81 |
| Merit / Merit Web Reporter / Smartrack | 65 | 34 | 31 |
| **Total** | **391** | **163** | **228** |

(163 corrected + 1 flagged-but-not-pushed C4102880 + 1 count reconciliation note: the passenger-portal
follow-up batch of 3 cases is included in the 44 above.)

## Audit result

`python -m system_test_ops audit --suite 30279 --no-gate`:

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before this pass | 391 | 89 | 208 |
| After this pass | 391 | **89 (unchanged)** | 208 |

The 89 blocking findings are the suite's pre-existing, unrelated backlog (`preface-bad-preamble` ×82,
`then-compound-genuine` ×7) — explicitly out of scope for this task per the brief; not hunted down.

## Out of scope, disclosed

The `Delete` section (105 cases, all `ZZ_DELETE_REVIEW`-prefixed by an earlier pass) was not audited —
these are condemned cases awaiting a human bin action in the TestRail UI (the API here cannot delete
or move cases). This is a deliberate exclusion, not a silent gap.

## Full detail

See `proposals/coherence-audit/fixes/abt-deep-audit.changelog.md` for: the complete section table, all
six rewrite-file paths and their applied counts, the full text of gap-register questions Q25-Q37, and
the reconciliation of existing gaps (Q3/Q14/Q21) applied during this pass.
