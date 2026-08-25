# Findings — OBV Emergency Mode / Status / Communication Loss / Transaction Timeout

Cross-examines the existing NJT dump (`reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/obv-emergency-status-timeout.md`, 76 cases) against
`knowledge/njt/specs/fs002-obv-emergency-status-timeout.md` (`NJT_FRFRP_FS002` §6.4–6.7), walking that
note's "Suite implications" checklist item by item.

## 1. Emergency Mode (§6.4) — Covered

| Checklist item | Status | Cases |
|---|---|---|
| (a) entry message + accept-other-operator guidance on first bit-set | Covered | C4085169 (legacy), C4098839 (TIBU) |
| (b) clearing entry message via **C key only** | Covered | C4085169, C4098839 |
| (c) exit message on bit-clear | Covered | C4085170, C4098840 |
| (d) clearing exit message via **C key only** | Covered | C4085170, C4098840 |

No draft needed. The "first sees" repeat-entry ambiguity (does a second, later bit-set re-trigger the
entry message?) is the knowledge note's own flagged GAP — per task instruction, not guessed at, only
logged to the gap register (already present as an open question; carried forward, not duplicated).

## 2. OBV Status bar (§6.5) — Partial

- **Bit-pattern-to-scenario mapping** — correctly **not** re-tested here; the source table extraction
  is corrupted per the knowledge note's GAP. Existing legacy cases (C4085171–C4085178, C4086755,
  C4086756) already avoid asserting bit values — they defer to "the symbol displayed matches the
  ... column ... in the table" by cross-reference, which is the safe pattern. No change proposed.
- **Explicit closing rule — Emergency Mode / no-GPS / no-screen-display statuses are excluded from the
  top-line status indicator** (`NJT_FRFRP_FS002 p.79`) — **Missing.** This is a distinct, clean
  behavioural fact (not part of the corrupted bit table) that has no corresponding case in either the
  legacy tree or the TIBU "Status Bar - OBV Status Indicator" tree (C4099533–C4099542, C4099719–
  C4099722 test OK/Error/Maintenance icon logic from fault/in-service/maintenance flags only — none
  test that Emergency Mode / no-GPS / no-screen-display leave the *top-line* indicator unaffected).
  **3 cases drafted** (see cases.yaml) — each states only the clean exclusion fact, citing p.79, with
  no bit-value assertion.
- Whether the legacy per-scenario "status bar shows N/A" cases (C4085176 Emergency Validation mode,
  C4085177 no GPS, C4085178 no screen display) are the *same* display element as this "top-line
  indicator," or a different one, is itself unclear per the knowledge note's second GAP — flagged to
  the gap register rather than assumed either way.

## 3. Communication loss (§6.6) — Covered

Per-transaction-type asymmetry (EMV/SV auto-cancel vs. Barcode/Fare-card remain-waiting) plus the
9-second default detection are all present:

| Type | Behaviour expected (spec) | Case(s) |
|---|---|---|
| Detection | Status bar reflects "not communicating" after configured period | C4086758 |
| Barcode | Remains waiting; driver Issue/C resolves it | C4085636 (accept), C4086757 (cancel) |
| EMV | Auto-cancelled | C4085637 |
| SV (NJT Card Stored Value) | Auto-cancelled | C4085638 |
| Fare card (NJT Card Ticket) | Remains waiting; driver Issue/C resolves it | C4085639 (accept), C4086759 (cancel) |

No gaps found here; no drafts needed.

## 4. Transaction timeout (§6.7) — Covered, with one flagged risk

The enumerated approval-wait states × transaction-type outcomes are present:

| Type | State(s) tested | Outcome per spec | Case(s) |
|---|---|---|---|
| Barcode | waiting for driver | auto-accept + print | C4086760 |
| Barcode | rejected | auto-acknowledge | C4086761 |
| EMV | waiting for driver | auto-cancel | C4086762 |
| EMV | rejected | auto-acknowledge | C4086764 |
| NJT Card Ticket (Fare card) | waiting for driver / waiting for zones / waiting for rider classification and zones | auto-accept + print | C4086768, C4086769, C4086771 |
| NJT Card Ticket | rejected | auto-acknowledge | C4086770 |

No missing state×type combination against the three enumerated states — Barcode/EMV have no
zone/rider-classification wait state in this dump, consistent with those states belonging to the
Fare-card product-selection flow only.

**Flagged risk (not fixed here — existing cases are out of scope to edit):** C4086765–C4086767 test
an **SV (NJT Card Stored Value) transaction-timeout auto-accept path**, but §6.7 of the spec excerpt
only enumerates Barcode, EMV, and Fare card in its auto-accept/auto-reject list — SV is not named. Per
the knowledge note's third GAP, asserting SV *has* (or lacks) a timeout path is exactly what must not
be guessed. These three cases assert real device behaviour (auto-accept) that is currently
**UNCONFIRMED** against the cited spec section. This is logged as a new gap-register question rather
than silently reconciled either way (do not edit C4086765–C4086767 without the engineer's answer).

Also observed, advisory only: the auto-accepted Barcode/Fare-card timeout cases assert the receipt
print unconditionally ("the FR prints the required receipt or fare media"), where §6.7 says printing
is optional ("may also print if configured to"). Not raised as a gap-register question (it's a wording
tightness issue on an existing case, not a missing-behaviour question) — noted for whoever next edits
those cases.

## Summary of drafted cases

3 new cases added to `obv-emergency-status-timeout.cases.yaml`, all under
`Fare Register / OBV Functionality / OBV Status`, covering the p.79 top-line-indicator exclusion rule
for Emergency Mode, no-GPS, and no-screen-display — the one clean, ungrounded-so-far behavioural gap
found in this cross-exam.
