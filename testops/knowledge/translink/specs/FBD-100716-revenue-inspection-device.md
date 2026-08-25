# FBD-100716 — Revenue Inspection Device (RID / cEMV Inspection) (distilled)

**Source:** `FBD-100716 Translink Revenue Inspection Specification V5.00` (28 Apr 2025, S. James).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100658 (ABT Audit), FBD-100651 (Glider Tap On Only).

## Scope / device
- **Delivered on the T1 HHD + Miura M020 + CloudFare ABT back office.** No dedicated RID hardware;
  **inspection is HHD-only** (PV/GV/ETM/BV/TVM do not perform cEMV inspection).
- Purpose: inspect **contactless EMV (cEMV)** bank cards on **Tap-On-Only (Glider)** and future
  **Tap-On-Tap-Off (NIR)** networks and charge a penalty ("**Standard Fare**") if the customer had no
  valid tap-on. **Online-only** (no offline inspection). **No BIN blocking list on HHD.**
- Terminology: **RID List** = HHD-local deny list of **FEIG tokens** (payment cards) blocked for
  travel. Max **100,000 tokens** (CR106 may raise to **200,000**).

## HHD local RID List lifecycle (testable timings)
- On startup: request **full RID list** from ABT; store with timestamp. If comms are down, request is
  deferred until comms restored.
- **Every 15 minutes**: if the stored list's timestamp is **before the most recent End-of-Day**
  (configurable via TMS) → request a **full** list; otherwise request a **delta** (adds/removals).
- Delta with no changes → wait another 15 min. Apply adds/removals to the local list.

## Inspection flow on device (M020 → HHD)
1. HHD in Sales Mode; inspector triggers **Inspection Mode** (earmarked: oval soft key) → M020 wakes
   / connects (Bluetooth; may show "connecting" screens).
2. Customer taps card. **M020 card integrity checks**: accepted **scheme** (Visa/Mastercard/Maestro),
   **offline data authentication (ODA)**, **not expired**. Fail → failure screen, message **"Card
   Declined"**.
3. **ChipDNA online Account Validation** to NMI (→ acquirer Elavon). NMI **tokenises** the card with
   the same algorithm/keys as FEIG devices; returns **Auth Result, PAR, Card Reference, Card Hash +
   FEIG token**. (Auth Result is not acted on — validation is only to obtain token + do local deny
   check.) Device offline → **"Failed to connect please try again"**.
4. **RID List check**: FEIG token on RID list → **"Card on RID List"** failure. Not on list →
   **Success** screen. Success/failure screens carry **distinct audio tones**.
5. Inspection tap generated (FEIG Token, PAR, Card Reference, Card Hash, direction, boarding location,
   route, timestamp) → sent to CloudFare → forwarded to ABT.
- **Inspection Mode UX:** after each inspection HHD **auto-returns to inspection mode** (keeps M020
  awake); short timeout returns to inspection mode from result screens; **no card presented within
  30 s** → timeout back to Sales screen. **An inspection tap cannot be annulled** (refund only via BO).

## Device events (for MERIT / bonus reporting) — must be emitted per inspection
- **5008** cEMV Inspection Success
- **5009** Failure – On RID List
- **5010** Failure – Card Expired
- **5011** Failure – Failed ODA
- **5012** Failure – Invalid Scheme
- **5013** Failure – Other
- Events **must include the client shift id** to be usable by MERIT.

## Back-office (ABT / CloudFare / MERIT) rules
- On inspection tap, ABT links by **FEIG token** to existing media; if none, **creates a new customer
  account** from the token (so charging can occur).
- **No penalty** if a matching **travel tap** exists (same transport mode, same route, within
  **Maximum Journey Time (MJT)**, tap before inspection). MJT is configured **per operator via ABT
  route groups** (single Glider group, single NIR group).
- If no valid tap-on: on auth failure → **add FEIG token to both Deny List and RID List** (propagated
  to all devices at normal cadence). **Standard Fare** charged at **End-of-Day settlement** after the
  configurable **Standard Fare Delay** (delay counts **from expected settlement time**, e.g.
  inspect 10:00 D1, settle 04:00 D2, 2-day delay → charged at 04:00 D4). Late matching tap within the
  window flips the inspection to success (no charge).
- **Standard Fare** value = global (not per mode); configured via a **product → rule assignment** in
  CloudFare, with the product name set in ABT settings. Not included in capping.
- **Multiple inspections / same journey:** never charge Standard Fare twice — success within MJT of an
  already-successful travel tap = success; repeated failures outside MJT with no travel tap = another
  Standard Fare (see spec §5.3 for the full matrix).
- **Late tap after Standard Fare charged:** ABT recalculates and **auto-refunds the difference**.
- **Deny/RID interaction:** a FEIG token added to the deny list via a valid PV tap (later auth fail)
  is added to the RID list **only after the original tap's MJT expires** (so the customer can finish
  their journey without a false "On RID List"). Deny-list removal must also remove from RID list.
- **Inspection MID:** Standard Fare settled under a distinct **Inspection MID** (separate from travel
  taps); appears separately in **Revenue By MID**. Debt recovery = automatic + tap-initiated (no
  cardholder-initiated) against the CNP MID.
- **Journey/Transaction History**: failed inspections add rows with penalty icons, file number, empty
  alighting (TOO); successful-linked inspections add an inspection icon to the aggregated fare.
- **MERIT**: failed inspections have no boarding/alighting stage → ABT sends **default (legacy) stage**
  locations; product = Standard Fare product.

## Reports
- **Revenue Inspection report** (Operator Portal): summary (Total inspections, Total incomplete
  journeys, Standard fares issued count+value, Max fares — TOTO only) + per-tap detail; date filters;
  export **CSV/XLSX/PDF**; includes inspections with no linked account.
- **Tickets By Operator (MERIT)** and **Revenue Inspectors (CloudFare)** reports gain cEMV inspection
  counts from events 5008–5013 (new columns "Qty Valid / Not Valid cEMV Inspections").

## CR dependencies
- **CR106** — RID list max token count 100k → 200k.

## Suite implications (HHD / ABT-BOS)
- Scope RID/inspection cases to **HHD only**; assert other device types do **not** offer cEMV
  inspection.
- Cover the **three M020 card-integrity failures** (scheme / ODA / expired → "Card Declined"),
  **offline** ("Failed to connect"), **On RID List** ("Card on RID List"), and **Success** — each with
  the correct **event code (5008–5013)** and distinct audio tone.
- Cover **RID list lifecycle**: full-on-startup, **15-min** delta, **full-after-End-of-Day**, comms
  outage deferral.
- Cover **Inspection Mode UX**: auto-return to inspection mode, **30 s no-card timeout**, cannot annul.
- Cover BO matching: **MJT** match = no charge; no tap → **Standard Fare** after **Standard Fare Delay**
  from settlement; **late tap → auto-refund**; **multiple-inspection** no-double-charge matrix.
- Cover **Deny/RID propagation** incl. the **MJT-delayed RID add** and deny-removal→RID-removal.
- Cover **Inspection MID** separation and the **Revenue Inspection report** export.
- **Note dependency on FBD-100651 (Glider TOO) and FBD-100658 (ABT Audit)** for exact matching rules
  — do not invent TOTO/NIR behaviour (largely future scope).
