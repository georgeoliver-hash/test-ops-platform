# Findings — NJT OBV "Fare Pay card" cross-examination (Stored Value + Ticket Product Processing)

Source case dump: `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/obv-farepay.md`
(268 cases, read in full). Spec knowledge: FS002 §6.3 distilled note (reproduced in the task brief).
Classification walks the knowledge note's "Suite implications" checklist point by point.

## Checklist classification

### 1. SV vs Ticket top-level split (assert `$F4` Ticket Type Pass `000000` → SV, else → Ticket)
**Missing.** No case in the dump asserts the branch-selection rule itself — cases are already
pre-sorted into "Stored Value Process" vs "Ticket Product Processing" sections, but nothing tests
that the FR makes that routing decision off the `Ticket Type Pass` field value. Drafted
`Fare Pay card — Ticket Type Pass of 000000 routes to the Stored Value flow` and `Fare Pay card —
non-zero Ticket Type Pass routes to the Ticket Product flow`.

### 2. One case per approval mode per product family (7 states × accept/cancel/card-rejected)
**Partial.** SV Waiting for Driver is fully covered (accept online `C4085115`, transfer `C4086334`,
insufficient funds `C4086324`, cancel `C4086332`/`C4086336`, offline `C4086333`/`C4086335`, card
rejected `C4086337`/`C4086338`). SV Automatic is covered for accept/reject (`C4085116`–`C4085121`)
but **has no case asserting the funds-check-skip behaviour** (see #3/#4 below — same gap). SV
Waiting for NJT Card Validation Info (WFCVI) is covered broadly (`C4085127`–`C4085133`, `C4086345`–
`C4086354`) but its insufficient-funds case `C4086349` only exercises the **cancel** sub-path after
rejection — the spec's unique "driver may retry with different zone/rider-class/type" sub-path
(p.65) is **not exercised**. Ticket family (WFD `C4086392`–`C4086399`, Automatic `C4086400`–
`C4086407`, Waiting for zones `C4086408`–`C4086423`, Waiting for Rider Classification and Zones
`C4086424`–`C4086439`) is fully covered for accept/cancel/card-rejected (tickets have no funds
concept, correctly absent). Drafted 2 cases to close the SV Automatic funds-skip gap and the WFCVI
retry-with-different-params gap.

### 3. WFD/Automatic reach the same result; retry-after-insufficient-funds is WFCVI-only
**Confirmed correct, but under-tested on the Automatic side.** WFD's insufficient-funds case
(`C4086324`) correctly shows only cancel, no retry — matches spec. Automatic has **no** insufficient-
funds case at all to confirm the check is skipped there (see #4). Closed by #2/#4's drafts.

### 4. Insufficient-funds check (signed threshold; Automatic skip)
**Missing.** No case tests a **negative threshold** value in the `SV balance − fare ≥ Threshold`
formula (all insufficient-funds cases describe "not enough funds" without exercising a signed
threshold). No case confirms Automatic mode **skips** the check entirely (`C4085116`–`C4085119`
show successful acceptance but never with an insufficient balance to prove the check was bypassed,
unlike `C4086333`/`C4086335` which explicitly says "will not perform the sufficient funds check" for
*offline* WFD — no Automatic equivalent). Drafted 2 cases (Automatic funds-skip; WFD signed
threshold, using the gherkin-standard's "assumed configured value" pattern rather than inventing a
number).

### 5. Online vs Offline per mode
**Covered.** SV: online/offline pairs exist for WFD (`C4085115`/`C4086333`), Automatic
(`C4085116`/`C4085118`), WFCVI (`C4085127`.../`C4086346`...). Ticket: WFD (`C4086392`/`C4086394`),
Automatic (`C4086400`/`C4086402`), Waiting for zones (`C4086420`/`C4086410`), Waiting for Rider
Classification and Zones (`C4086424`/`C4086428`) — and the "offline not expected, forced Adult
Monthly Pass" fallback is explicitly tested for Ticket (`C4086402`, `C4086394`, `C4086407`,
`C4086399`, `C4086415`, `C4086435`).

### 6. Rider classification mapping (incoming 01/02/03/04/05/10; outgoing 1/2/3/4 under mode 03; Employee never sent; Family/Foreign gap)
**Partial.** Incoming OBV→FR mapping fully covered: Adult `C4086355`, Child `C4086356`, Senior
`C4086357`, Disabled `C4086358`, Student `C4086359`, Senior/Disabled `C4086360`. Outgoing FR→OBV
mapping under mode 03 covered: Adult `C4086361`, Child `C4086362`, Senior `C4086363`, Student
`C4086364` (plus a good negative, `C4086365` Student-not-enabled). **No case asserts Employee (5) is
never sent to OBV / never offered as a selectable classification** — drafted one. Family (6) /
Foreign (7) correctly absent (no outgoing mapping documented) — routed to gap register (GAP-1, per
task brief).

### 7. Zone-selection paths (OBV supplies zones vs FR falls back to current zones)
**Covered.** Not tested as standalone display cases, but exercised thoroughly via the Receipt and
Transaction Auditing subareas' OBV-Zones vs No-OBV-Zones pairs — SV: `C4086376`/`C4086377` (receipt),
`C4085151`/`C4086366` (audit One Way), `C4086367`/`C4086368` (audit Transfer), `C4086369`–`C4086372`
(audit Automatic). Ticket: `C4086678`/`C4086679`, `C4086680`/`C4086681` (audit).

### 8. Transaction-type derivation (SV §6.3.1.1/.2) vs driver-toggle (§6.3.1.3), with CT/Transfer gating
**Partial.** Derived OW/Transfer (no driver action) covered for WFD (`C4085115`/`C4086334`) and
Automatic (`C4085116`/`C4085117`). Driver-toggle to CT covered (`C4085130`, `C4085132`). Driver-
toggle to Transfer is asserted as a resulting state (`C4085131`) but not clearly exercised as an
actual R4-toggle interaction (ambiguous — the case body states the TxType outcome without showing
the toggle action). **Missing: a negative case for CT unavailable when 'Enable ISSCTT' is off**, and
**missing: a negative case for Transfer unavailable when discount type ≠ 14 or boarding≠alighting
zone**. Drafted both.

### 9. Fare print/audit rules (SV OW-only vs Ticket never)
**Covered.** SV Receipt shows both "fare shown" (`C4086376`, `C4086381`, `C4086386`, `C4086387`) and
"fare withheld" (`C4086377`, `C4086378`, `C4086379`, `C4086380`, offline variants) paths. Ticket
Receipt (`C4086673`) explicitly states "no fare will be printed"; Ticket Transaction Auditing
(`C4086678`–`C4086683`) explicitly states "no fare value will be audited" in every case.

### 10. Spotter-display ambiguity (`<Class>*CARD` for both SV and Ticket)
**Covered, no defect found.** SV `C4086391` and Ticket `C4085112` both assert the identical
`<Class>*CARD` format; neither wrongly asserts the spotter output distinguishes product type. Minor
note: `C4085112`'s body text says "the EMV transaction performed in the preconditions" rather than
"the NJT Card Ticket Product transaction" — looks like a copy-paste artefact from an unrelated case
family, not a coverage defect (the assertion itself is correct).

### 11. Product-code mapping (§6.1.2) / CT-validity matrix (§4.1.3) — out of range
Correctly not attempted by any case in this area; routed to gap register (GAP-3) per task brief —
these live in sibling notes, not fixable here.

### 12. Payment-type "magnetic vs smart card" for Ticket audit
**Covered as specified, ambiguity is real.** Every Ticket Transaction Auditing case (`C4086678`–
`C4086683`) asserts the literal ambiguous spec value "a payment type of magnetic or smart card pass"
— consistent with the spec text, but the underlying question of how the value is chosen is
unanswered. Routed to gap register (GAP-2) per task brief.

## Product Mapping (55 cases) — sampled, not exhaustive

Spot-checked 10 of 55 across different code ranges and rider classes: `C4086604` (21001, One Way
Adult), `C4086605` (21002, One Way Child), `C4086606` (21103, One Way Off Peak Senior), `C4086609`
(22001, Round Trip Full Adult), `C4086614` (23001, 10 Trip Discount Adult), `C4086618` (24701,
Monthly Adult Intrastate), `C4086620` (14701, Monthly Adult), `C4086631` (84701, Monthly Adult),
`C4086640` (35301, Continuing Trip Adult), `C4086647` (91201, One Way + Transfer Adult).

Result: the ticket-type-code → `Ticket type accepted` field mapping is internally consistent across
the sample (e.g. `21001` → `02 10 01`, `24701` → `02 47 01`, `14701` → `01 47 01` — the field splits
the code into 2-2-2 digit groups matching the stated ticket type prefix). One **data defect** found:
`C4086647` is titled "91201 - One Way + Transfer Adult- Paper" but its body text says "...ticket
type 91201 and the ticket and rider class **'Monthly Student'**" — a copy-paste mismatch between
title and body (the `09 12 01` field value is consistent with the title, so the body prose is wrong,
not the assertion). This is an authoring defect, not a spec ambiguity — flagged here for the suite
owner to fix directly, not routed to the gap register (it doesn't need an engineer's answer, just a
correction). No other mismatches found in the sampled 10. Classification: **Covered** (sampled, not
exhaustive).

## What's missing — summary driving the drafts

8 cases drafted into `obv-farepay.cases.yaml`:
1. SV path selection on `Ticket Type Pass = 000000` (checklist #1)
2. Ticket path selection on non-zero `Ticket Type Pass` (checklist #1)
3. SV Automatic — funds check skipped even when insufficient (checklist #2/#4)
4. SV WFCVI — insufficient funds, driver retries with changed zone/class and succeeds (checklist #2)
5. SV Waiting for Driver — signed/negative threshold still permits acceptance (checklist #4)
6. Rider Classification — Employee never sent to OBV (checklist #6)
7. SV WFCVI — CT not selectable when 'Enable ISSCTT' is off (checklist #8)
8. SV WFCVI — Transfer not selectable when discount-type/zone eligibility fails (checklist #8)

5 gap-register entries logged (4 required by the task brief + 1 discovered during this pass — see
`gap-register-obv-farepay.md`): Family/Foreign outgoing mapping (GAP-1), magnetic-vs-smart-card
payment type (GAP-2), §4.1.3/§6.1.2 out-of-range pointers (GAP-3), pop-up-window terminology
(GAP-4), and a new one discovered here — "Override Required" screen asserted for Ticket Product
Processing cases but not documented in-range for §6.3.2 (GAP-5).
