# Function-granularity audit (cross-suite) — over-consolidation review

**Why.** During the rebuilds we consolidated aggressively (POS, ETM, PV). George's catch (2026-06-11,
running ETM): some **distinct functions** were folded into a single behaviour case or a variation
line, so they aren't separately executable on a run — and a few were dropped entirely. This audit
identifies, per suite, what is **wrongly folded (~)** or **dropped (✗)** versus the old suite, so we
can un-fold the genuinely-distinct functions. Audit-first per `docs/test-practices.md`.

**The rule (the test for "should this be its own case?").** The **old suite is the gospel** for
distinct-function vs data-variation:
- **Distinct function** → its own case. A different *operator action / decision / outcome path*
  (e.g. faulty-card → Charge Full Fare vs Select Card Type vs Issue Ticket; top-up vs top-up-on-expiry).
- **Data variation** → a variation line on one case. Same mechanic, different data (Adult/Child,
  zone, product name where the steps are identical).

Over-folding distinct functions hides coverage and loses bugs; over-splitting variations bloats the
suite. We over-folded; this corrects that without going back to the old duplication.

---

## Status: COMPLETE — full family scan + old-suite grounding done 2026-06-12. Awaiting go on the un-fold list.

---

## CONFIRMED findings

### 1. Faulty-card options — over-folded (POS, ETM); absent (PV, correctly)
Old-suite granularity: **POS-old 28** faulty cases, **ETM-old 14** — distinct functions including
*Charge Full Fare*, *Select Card Type*, *Issue Ticket*, *Faulty Smartpass Receipt*, *Faulty
Dependants Pass Receipt*, *Faulty Fare Paying Smartcard*, *Present a faulty card*.

| Suite | Now | Should be |
|---|---|---|
| POS 30253 | **1** case `Faulty Card — options` (bundles charge-full-fare / select-card-type / issue-ticket) + `Faulty Card — invalid card removal` | Split into per-option cases: Charge Full Fare, Select Card Type, Issue Ticket, Faulty Smartpass Receipt, Faulty Dependants Pass Receipt, Faulty Fare-Paying Smartcard |
| ETM 30254 | **1** case `Smartcard — faulty card handling` (bundles the same) | Same split (per ETM faulty flow) |
| PV 30255 | **0** | Leave — PV is a validator, no faulty-card-issue flow in PV-old (correct) |

### 2. Fare-paying (stored-value) smartcard — DROPPED everywhere (real gap)
`Fare Paying Smartcard` is a real product in **POS-old (4 cases incl. Faulty Fare Paying Smartcard)**
and **ETM-old**. New suites have **zero** coverage — validation (pay a fare / deduct value), top-up
(load value), and faulty handling are all missing on POS and ETM. PV-old: none (validator).
→ **Add** Fare-Paying Smartcard validation + top-up + faulty, on POS and ETM.

### 3. Pass variants — patchy
- POS: has `Dependents Pass`; **no Spouse/Partner pass**.
- ETM: now has Staff / Spouse-Partner / Dependants / Retired / External (just added per-product).
- PV: only `Translink Employee smartcard` — staff-family variants thin (verify if PV-old splits them;
  PV is validate-only so a single employee/staff case may suffice — TBC).

---

## Completed matrix (new suite status · old-suite distinct cases · verdict)
✓ = dedicated runnable case · ~ = only folded into a behaviour body/variation · ✗ = absent. Old = #
distinct cases in the old suite (the gospel). Verdict: **UN-FOLD** / **leave** / **add** / **N/A**.

| Function | POS new | ETM new | POS-old | ETM-old | Verdict |
|---|---|---|---|---|---|
| Faulty — Charge Full Fare | ✓ | ✓ | 2 | 1 | leave (already dedicated) |
| Faulty — Select Card Type | ✓ | ✓ | 2 | 1 | leave |
| Faulty — Issue Ticket | ✓ | ✓ | yes | yes | leave |
| **Faulty — Smartpass Receipt** | ✗ | ~ | 4 | 2 | **UN-FOLD / add** |
| **Faulty — Dependants Pass Receipt** | ✗ | ✗ | yes (spelt "Dependents") | 1 | **add** |
| **Fare-Paying Smartcard — faulty** | ✗ | ✗ | 4 | 1 | **add** |
| **Fare-Paying Smartcard — validate + top-up** | ✗ | ✗ | yes | yes | **add (the product is dropped entirely)** |
| Top-up — cancel/Back | ✓ | ✓ | — | — | leave |
| Top-up — maximum journeys | ~ | ✓ | yes | yes | leave (POS ~ acceptable) |
| Top-up — expired-journeys removed | ~ | ~ | yes | yes | optional split |
| **Top-up — on expiry** | ✗ | ~ | yes | yes | **add (POS); optional split (ETM)** |
| Mini-statement | ✓ | ✓ | yes | yes | leave |
| Validation — Represent Card | ✗ | ✗ | 0 | 0 | leave (not a distinct old case; folded/HMI) |
| Validation — Unable to Validate | ✗ | ✗ | 0 | 0 | leave |
| Validation — Not Yet Valid | ✗ | ✗ | 0 | 0 | leave |
| Validation — No Journeys/Days Left | ✗ | ✓ | — | yes | leave |
| Validation — Outside Time Band | ✓ | ✓ | yes | yes | leave |
| **Passback (POS)** | ✗ | ✓ | 1 | 85 | **add (POS)** — ETM already covered |
| Card Dump | ✓ | ✗ | 4 | 0 | leave (POS has it; N/A on ETM) |
| Card Clear | ✓ | ✗ | yes | 0 | leave / N/A on ETM |
| Spouse/Partner Pass (POS) | ✗ | ✓ | 0 (POS-old has only Dependents) | yes | leave / N/A on POS |
| Group ticket | ✓ | ✓ | yes | — | leave |
| Excess fare / Open Tickets | ✓ | ✓ | yes | yes | leave |
| Calculate change | ✓ | ~ | yes | — | leave |
| Receipt reprint | ✗ | ✗ | 0 | 0 | leave (not a function in either old suite) |

## Recommended un-fold list (grounded, high-confidence)
**POS (30253):** Fare-Paying Smartcard — validate · top-up · faulty (3); Faulty — Smartpass Receipt (1);
Faulty — Dependants Pass Receipt (1); Passback (1); Top-up on expiry (1). = 7 cases. (No Spouse/Partner
— POS-old has only Dependents.)
**ETM (30254):** Fare-Paying Smartcard — validate · top-up · faulty (3); Faulty — Smartpass Receipt
un-fold from "faulty card handling" (1); Faulty — Dependants Pass Receipt (1). ≈ 5 cases.
**PV (30255):** none — validator; faulty/fare-paying/top-up-at-device don't apply (PV-old has none).

Each un-folded case authored grounded in the old-suite behaviour, with back-office verification steps
baked in (smartcard → CloudFare activity log + MERIT + SmartTrack). Superseded bundle text trimmed;
no old-suite duplication reintroduced (these are distinct functions, not product variations).

## Un-fold plan (after the matrix is agreed)
1. Author per-suite `*-unfold.cases.yaml` re-expanding the agreed distinct functions (grounded in the
   old-suite titles), each with proper Gherkin + back-office verification steps.
2. Mark superseded bundle cases `ZZ_DELETE_REVIEW` for George to bin.
3. Re-audit (CLEAN), re-enrich (priority/estimate/automatable), re-export the automation backlogs.

## Note on PV
PV is a validator (no issue / no faulty-card-issue / no top-up-at-PV). Most of these families don't
apply — PV's lower count is largely correct. PV-specific granularity is already covered by the
per-product validation work + the Overflow-grounded re-check. Confirm only: validation-outcome
screens are each represented.
