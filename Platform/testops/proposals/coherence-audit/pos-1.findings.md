# POS Coherence & Grounding Audit — Part 1 (cases 0–264)

**Scope:** `suite_POS.json` array indices 0–264 (265 cases). Grounded against
`knowledge/translink/specs/FBD-*.md` (Android POS / way6). Report-only — no cases edited.

**Summary: 11 problems of 265 cases — 0 High, 3 Med, 8 Low.**
The suite is largely coherent and well-grounded; the refund block (125–136) in particular ties
cleanly to FBD-100373. The 71 Screen-Validation cases (idx 194–264) are coherent by design (titles
mirror exact UI screen names, advisory per CLAUDE.md) and are **not** flagged. Most findings are the
same systemic smell rather than broken scenarios: **back-office assertion steps ("CloudFare activity
log", "transaction appears in MERIT", "SmartTrack record") bolted onto scenarios that produce no
transaction** (UI views, cancellations, availability checks, diagnostic reads). No case was found as
broken as the daily-cap-vs-cancellation example.

---

## Findings

**C4100414 (idx 115) + C4100417 (idx 118)** | Med | grounding/both |
Titles/steps sell a "**Youth** smartcard" applying a "youth entitlement" and a "**Concession**
smartcard" applying a "concession entitlement". Neither "Youth" nor "Concession" is a Translink
entitlement card type. FBD-100250's Funded group is `Partially Sighted, No DL, Learning Disability,
DLA, yLink, PIPS, 24 Plus`; the grounded entitlement enum used elsewhere in this very suite (idx 94
C4100427) is `Senior/Blind/War Pensioner/yLink/24+/Half-Fare/Dependants`. "Youth" duplicates/conflates
with **yLink** (idx 116 C4100415, immediately adjacent); "Concession" is a vague catch-all matching no
named product. **Action:** re-ground each to a real card type (Youth → yLink, or confirm intended
concession product), or delete as duplicate of idx 94/116. Needs-confirmation on the exact card names.

**C4103544 (idx 136)** | Med | coherence |
Cross-device refund. The action (STEP1) is "refund a **TVM** sale on a Bus POS", but EXP1 welds on a
second, unrelated rule: *"AND an ETM sale is refundable only when it was originally paid by cash"*. The
ETM-cash-only rule is real (FBD-100373) but is **not exercised by this step's action** — two distinct
assertions fused into one expected. **Action:** split the ETM-cash-only assertion into its own step
(or its own case); keep EXP1 to the TVM-on-POS outcome actually performed.

**C4099960 (idx 36)** | Med | grounding |
Technician card-reader diagnostic ("Please Present Smartcard to Test"). Steps 3–4 assert *"the
transaction appears in MERIT"* and *"the updated smartcard record appears in SmartTrack"*. A reader
**health-check read** is not a sale/issue/validation and writes nothing to the card, so it should not
produce a MERIT financial transaction or a mutated SmartTrack record. **Action:** re-ground the
expected to a diagnostic/event outcome (device event only), or confirm the test-read is genuinely
posted to MERIT/SmartTrack. Needs-confirmation.

**C4099912 (idx 4)** | Low | both |
Sign-On screen field-entry / 'C'-key test. (a) Preconditions carry a stray boilerplate line
*"AND example: Operator → the Operator menu"* irrelevant to a Sign-On-screen field test (same
copy-paste artifact recurs in idx 5–7). (b) EXP5 asserts a BOS/CloudFare activity-log event for a pure
keypad/clear-key UI check that performs no sign-on and no transaction. **Action:** drop the stray
example line; drop or re-scope the activity-log step (a UI-only field test emits no BOS event).

**C4099937 (idx 16)** | Low | coherence |
"Cancel Soft Reset" — operator presses Cancel and *no reset is performed*, yet EXP2 asserts the event
"is recorded in the CloudFare activity log". A cancelled no-op is unlikely to raise an audit event.
**Action:** drop the activity-log step or confirm a cancel is audited. Needs-confirmation.

**C4100023 (idx 100)** | Low | both |
"Faulty Card — invalid card removal": action is the POS *detecting a card lifted off the reader*, but
EXP3 asserts *"the transaction appears in MERIT"*. A removal-detection is not a transaction.
**Action:** remove the MERIT step; keep to the on-device detection outcome.

**C4099946 (idx 163)** | Low | both |
"Excess Ticket — available (rail)": the only action is opening the Operator menu to confirm the
feature **is listed**, yet EXP2/EXP3 assert a CloudFare event and a MERIT transaction. Merely seeing a
menu entry sells nothing. **Action:** drop the CloudFare/MERIT steps (menu-presence check has no
transaction).

**C4100432 (idx 58)** | Low | grounding (needs-confirmation) |
Basket caps at **9 tickets**. The "9" is not stated in the specs reviewed. Scenario is internally
coherent. **Action:** confirm the cap value against the product/basket spec; otherwise fine.

**C4100430 (idx 80)** | Low | grounding (needs-confirmation) |
Group ticket passenger count **"up to the maximum of 100"**. The 100 cap is not found in the specs.
Coherent otherwise. **Action:** confirm the group maximum.

**C4100434 (idx 60)** | Low | grounding (needs-confirmation) |
"Bus basket is single-route" (second-route ticket rejected, multiple stages on the same route
accepted). Plausible and coherent, but the single-route basket rule is not stated in the reviewed
specs. **Action:** confirm against basket/product rules.

**C4099936 (idx 15)** | Low | grounding (needs-confirmation) |
Operator Options must show *no 'Report Faulty Payment Device' option*. This specific negative
(that such an option exists and belongs to another role/feature) is not grounded in the reviewed
specs. **Action:** confirm the option's real home before asserting its absence here.

---

## Systemic observation (not counted above)

The dominant smell across the audited half is **boilerplate back-office assertion steps appended to
non-transactional scenarios**. Findings idx 4, 16, 100, 163 are the clearest instances, but the same
"WHEN the CloudFare activity log is checked / reviewed in MERIT → transaction appears in MERIT" tail
recurs on UI-view, cancel, and availability cases throughout. A single pass to strip the
transaction-in-MERIT / SmartTrack tail from any case whose action issues/writes nothing would improve
coherence suite-wide more than the individual edits above. Recommend handling as one cleanup rule
rather than case-by-case.
