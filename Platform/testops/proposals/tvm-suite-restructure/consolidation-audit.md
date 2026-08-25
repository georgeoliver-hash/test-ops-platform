# TVM Suite — Consolidation Audit

- **Project:** `TFTS - System Test` (id 42)
- **Target suite:** `**NEW** TVM Test Suite` — id **30284**
- **Inventory:** `reports/tfts-system-test/new-tvm-test-suite/2026-08-07/cases.json` (436 cases)
- **Lens:** `docs/test-practices.md` → "Structure by flow/risk, not by screen"

436 cases include a **27-case `Delete` section** (rows tagged `ZZ_DELETE_REVIEW -`, old
Smartcards/ABT/Mini-Statement content) that is already flagged for human bin review — **out of
scope**, left untouched. Active cases in scope: **409**.

Fold candidates below are all **variations of one behaviour** (same Given/When/Then shape, only a
payment method / card scheme / component / field name changes) or **steps of one flow**. Distinct
scenarios, branches, mode-specific divergence, and per-screen HMI navigation are left alone per the
consolidation rule.

## High-confidence fold groups (payment-method / scheme / component variation → one case + Examples)

| Area | Before | Fold groups | After | Saved |
|---|---|---|---|---|
| Functional / Barcode Redemption | 35 | 5 groups (booking-ref collect ×6 types, invalid-ref ×4 fields, malformed-ref ×4 reasons, legacy-stage ×3 types, ticket-format ×8 types) | 15 | 20 |
| Functional / Payments - Cash | 44 | 6 groups (sub-value coins ×3, foreign coins ×2, banknote-by-bank ×5, withdrawn notes ×3, jam-cleared ×3, jam-uncleared ×3) | 31 | 13 |
| Functional / Payments - Cash / Note Recycler (Astreo + Kiosk) | 8 | 2 groups (BNR exit-beak by button: Cancel/Back, one per site) | 6 | 2 |
| **Functional / Payments - EMV & Contactless** | **51** | **15 groups** (Chip&PIN-valid-by-scheme ×5, Amex/Diners-accepted ×3, no-PIN ×2, contactless-approved-by-scheme ×5, contactless-fallback-by-scheme ×4, wallet-approved ×3, declined-retry ×2, cancel-at-pinpad ×3, timeout ×3, print-failure-voids ×3, card-removed ×2, magstripe-valid-by-scheme ×4, magstripe-declined ×3, switch-to-card ×2, expired/blocked-rejected ×2) | **20** | **31** |
| Sales - Tickets / Ticket Issue | 50 | 9 groups, one per ticket product, each folding its cash/card/contactless variants ×3 | 32 | 18 |
| Sales - Tickets / Advance & 3-Day | 5 | 1 group (3-day ticket ×3 methods) | 3 | 2 |
| Sales - Tickets / Rail & Cross-Border (Kiosk) | 28 | 3 groups (NI Rail adult single ×3, NI Rail 3-Day Select ×3, XB adult single ×3) | 22 | 6 |
| Non-Functional / Resilience | — | 2 groups (degraded-service-by-component ×4, audio-prompt-by-input ×3) | — | 6 |
| Non-Functional / EMS & TMS Maintenance | — | 1 group (screen brightness inc/dec ×2) | — | 1 |

**Subtotal: ~99 cases saved** (409 → ~310) from the high-confidence groups alone.

Example fold (EMV, the largest group): five near-identical cases —

```
C4103657  Chip & PIN — a valid card completes payment and prints the ticket (Visa Debit)
C4104561  ... (Visa Credit)
C4104562  ... (Mastercard Debit)
C4104563  ... (Mastercard Credit)
C4104564  ... (non-GBP issued card)
```

fold to **one** keeper case `Chip & PIN — a valid card completes payment and prints the ticket`,
with the card scheme pulled into an Examples/data table in the steps, Refs merged
(`REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583`). Same pattern for every
group above — keeper picked as the case with the fullest step body and Refs; absorbed cases retire.

**Left alone (distinct scenarios/branches — do not fold):**
- Payment Cancelled / Change Returned / Timeouts screens (Payments - Cash) — per-screen HMI branches.
- Device Lockout ×4 (Resilience) — each asserts a **different outcome** (goes OOS vs stays In
  Service) depending on sale type, not a mere label variation.
- Alarmboard & Enclosure engineer tests, Cash Collection report types — each exercises distinct
  hardware/report, not a variation of one behaviour.
- Smoke section (9 cases) — deliberately redundant with Functional for smoke-run purposes; never fold.
- Ticket Numbering, Grouped Stops — already one-case-per-distinct-behaviour.

## Needs an aggressiveness call before folding (ambiguous: flow-steps vs per-screen HMI)

Two sections blend genuine screen-validation (leave one-per-screen) with what reads like sequential
navigation through one flow (fold candidate) — judgement call, not obvious:

- **Sales - Tickets / Basket — 34 cases.** ~21 of these are `<Screen> — <action> reaches <Screen>`
  navigation assertions through the Basket → Select Payment Type → Destination Selection → Select
  Tickets chain (rows around C4105303–C4105323), including a duplicated **"Basket - 2025 variant"**
  parallel path. **Full** aggressiveness would fold this into 2–3 flow-level cases (happy path +
  back-navigation) citing each screen in the steps; **obvious-only** would leave navigation as-is
  and fold only the literal duplicate (`Pay Now` vs `Pay Now (Basket - 2025 variant)`, 2→1).
- **Functional / Smartcards & ABT — 29 cases.** Similar pattern — `Home Screen — selecting X opens Y`
  navigation cases (rows C4105346–C4105360) plus behaviour variations (faulty-smartcard-no-update
  ×2 → fold candidate either way).

## Before → after (in-scope, excluding the already-flagged Delete section)

| | Count |
|---|---|
| Active cases today | 409 |
| High-confidence folds | −99 |
| **Subtotal (before Basket/Smartcards decision)** | **~310** |
| Basket, obvious-only (−2) / full (−~18) | 308 / ~292 |
| Smartcards, obvious-only (−1) / full (−~14) | 307 / ~278 |

Coverage is preserved in every fold — no behaviour is dropped, only the duplicated method/scheme/
component axis collapses into one case's Examples/data table.
