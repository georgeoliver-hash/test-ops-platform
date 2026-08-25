# PV suite ↔ requirements cross-examination — coverage gaps

**Suite:** `new-pv-acceptance-test-suite`, cases dump `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-15/cases.json` (122 cases, 0 `ZZ`).
**Specs:** `knowledge/translink/specs/` (distilled FBD notes). **Read-only analysis — no suite/TestRail changes made.**
Last updated: 2026-07-15.

Classification per spec rule: **COVERED** (case cited) / **PARTIAL** / **MISSING** / **STALE-or-WRONG**.
Scope note: the PV is an **unattended validator** — present smartcard / barcode / cEMV → validate; **no sign-on, no ticket
issue, no driver alighting selection**. Pure back-office rules (ABT tap-matching maths, capping, MERIT/portal, PJT/CSV
import) belong to the **ABT/BOS suite 30279** — flagged `[BOS-scope]` where they are not a PV-device gap, but listed
because the task named the FBD.

---

## Summary

The PV suite has **excellent breadth**: the full Translink smartcard catalogue (Concession/Half-Fare SmartPass, Metro
Daylink/Multi-Journey/Travelcard, Ulsterbus MJ, iLink/BVP, aLink, yLink/24+, Employee, EA Pupil/FE), validation
outcomes, both barcode classes, the Glider ABT/cEMV block, a large HMI screen-validation set, the Technician Menu, and a
solid non-functional block (power, comms, DST, heartbeat, updates, asset reporting). Topic coverage is broad and the
device scoping is mostly right (no cEMV-inspection case — correctly HHD-only per FBD-100716; no Integrated-Barcode-API
case — correctly TVM/HHD-only per FBD-100483).

The gaps are concentrated in **assertion depth on the new ABT work and a handful of device-matrix / property-source
correctness risks**:

- **STALE-or-WRONG — single-use barcode:** C4101005 asserts a single-use barcode *validates* on the PV. FBD-100167 §Scope
  and FBD-100317 §matrix are explicit: **PV validates MULTI-use only and must REJECT single-use** with "This Barcode Type
  is not accepted on this device". This is the sharpest correctness finding.
- **NIR/rail TOTO PV depth is thin.** The rail cases (C4100996/C4100997/C4102429) are one-line stubs; the TOTO device
  shape (tap-on vs tap-off, single-location audit, `TotoTap`/`Location` structure, product **6000**, NI-Zone location
  check, Declined Reasons) is not asserted (FBD-100690 / FBD-100658).
- **ABT audit-schema conformance not pinned** (FBD-100658): Glider PV audit cases exist (C4101089/C4101092) but no case
  pins the constant fields (`paymentType=ABT`, `revenue=0`, `CardType=emv`, `passCount=true`, `ticketsIssued=false`), the
  **`Fare` pounds vs `fareCost` pence** split, product **7000 (TOO)** / **6000 (TOTO)**, `TransferRouteType="Directional"`,
  or the PV `gpsCoordinates` block.
- **Pilot list "no-audit-on-reject" not asserted** (FBD-100720): C4101078/C4101000 exist, but the key negative — a
  non-enrolled FEIG token is rejected with **NO audit event** — plus registration-mode enrolment and the once-per-day
  EoD zip upload are not covered.
- **Transfer property-source** (FBD-100271): no case asserts the PV uses the **PRODUCT `Transfer Time`** property
  (vs the ETM's ROUTE property), nor the **WTS SmartTransfer vs WTS SmartUse** audit split or passback-over-transfer priority.
- **SaaS comms-lock OOS** (FBD-100359): C4101085/C4100995 cover offline+failover, but the specific end-state — a sustained
  Translink-network outage drives the Ethernet PV into a **communication-locked, out-of-service** state — is not asserted,
  and C4101085's "secondary failover channel" wording needs verifying against the PV's Ethernet topology.
- **CR116 early-morning expiry IS covered** — C4102428 is a dedicated case (good; verify the 00:00–04:00 rollback edges in body).

---

## Missing

| Spec | Rule not covered | Notes |
|------|------------------|-------|
| **FBD-100720** | **Pilot registration mode + EoD upload** — no case for `Enable Registration Mode=True` tapping enrolling a card's FEIG token into the on-device registration file, nor the **once-per-day-at-End-of-Day** zip upload to CloudFare Device Logging (not real-time). C4101078 covers pilot *validation* only. | Emphasised. Phase-1 of the pilot flow is absent. |
| **FBD-100720** | **Pilot list no-audit-on-reject** — the key negative assertion (non-enrolled token → standard rejection screen **and NO auditing event**) is not asserted anywhere. C4101078/C4101000 name the pilot list but stubs don't pin the no-audit rule. | Emphasised. "Easy to get wrong" per spec. |
| **FBD-100658** | **NIR/rail TOTO PV audit-schema conformance** — no case pins the TOTO tap structure (`TotoTap`/`Location`, single location, no boarding/alighting stages), product **6000**, `RouteType=0`, or `gpsCoordinates`. Rail cases C4100996/C4100997/C4102429 are stubs. | Emphasised. Glider TOO audit is partly covered (C4101089/C4101092); NIR TOTO audit is not. |
| **FBD-100271** | **Legacy MJ / rail smartcard transfer decision on PV** — no case asserts transfer-vs-journey using the **PRODUCT `Transfer Time`** property, the window boundary (`LastValidated+TransferTime`), PV always-directional check, Vehicle Type=Train (rail cards), **passback prioritised over transfer**, or the **WTS SmartTransfer vs WTS SmartUse** audit split + TRN increment. MJ card cases (C4100984/C4100986) are zone/validity only; C4100996 "NIR transfer" is a stub. | Emphasised (property-source). |
| **FBD-100359** | **Communication-locked out-of-service state** — no case asserts that after a *sustained* Translink-network outage the (Ethernet) PV goes offline and then enters the **comms-locked OOS** state. C4101085 covers resilience/failover generically; C4100995 covers offline-then-reconcile. | Emphasised. The terminal OOS state is the missing edge. |
| **FBD-100167** | **Three barcode result states** — the green-tick vs **yellow question-mark (route/location step-7-only fail)** vs red-cross distinction is not asserted; the yellow "valid but wrong route" state has no case (barcode fail screens C4101043–47 are red/other fails). Also **no barcode on a multi-passenger single ticket** (n/a to PV validation but worth confirming out of scope). | Emphasised. Result-state taxonomy. |
| **FBD-100307** | **TOO failure-mode distinction** — Mode 3 (topology/fare reject ⇒ **card reader not even enabled**, no passenger response) vs Mode 2 (card-level decline ⇒ txn + declined reason stored) vs Mode 1 (unreadable). C4101001 (enablement) and C4100999 (declined) touch these but no case asserts the **reader-disabled / no-response** behaviour distinctly. | Emphasised distinction; primarily device-visible on PV. |

---

## Stale-or-Wrong

| Spec | Contradiction to verify | Case(s) |
|------|-------------------------|---------|
| **FBD-100167 §Scope / FBD-100317 §matrix** | **PV does NOT validate single-use barcodes.** C4101005 title + stub state a single-use barcode "validates when valid and is rejected … when invalid" — implying a success path on the PV. Spec: PV/GV validate **multi-use only**; single-use on PV must reject with **"This Barcode Type is not accepted on this device"**. Either retitle/rescope this case to a **rejection** case, or delete (multi-use is already C4101006). | **C4101005** |
| **FBD-100266** | **"MERIT heartbeat" naming.** C4101082 is titled "PV to BOS — MERIT heartbeat". The delivered heartbeat is the **15-min Staff-List Refresh call-in to CloudFare** (Comms Monitor / Asset Manager / `StaffList` message), *not* a MERIT mechanism, and fires even when signed-out/no-sales. Verify the body targets the CloudFare StaffList cadence, not MERIT; the 15-min period is fixed (not Translink-configurable). | **C4101082** |
| **FBD-100359** | **"Secondary failover channel" for an Ethernet PV.** C4101085 asserts the PV "uses the secondary failover channel". Per FBD-100359 the PV is an **Ethernet** device routed through the Translink network (it is the **cellular** devices that are outage-independent). Confirm the PV actually has a secondary channel; if not, this expectation is wrong and should become the comms-lock-OOS path instead. | **C4101085** |
| **housekeeping** | **Duplicate screen id 1_6_1_1.** C4101036 ("ABT Tag successful - Rail") and C4101037 ("ABT Tag successful") both carry screen id `1_6_1_1`. Confirm these are genuinely two distinct HMI states (rail vs bus variant) and not a copy artefact; likewise C4101059/C4101060 both `11_01_10 Select Location`. | C4101036/C4101037; C4101059/C4101060 |

---

## Partial

| Spec | Covered by | What's missing in-body |
|------|-----------|------------------------|
| **FBD-100167 (CR116)** | **C4102428** (early-morning expiry displays previous day) — dedicated case ✓ | Assert the exact rollback edges: 00:00–04:00 → show **previous day, no time**; `…0400`→prev day; `…0401`→same day + time. Verify body encodes the boundary examples. |
| **FBD-100167 / 100317** | **C4101006** (barcode multi-use validation), HMI success/fail screens C4101042–47 | Validation-algorithm order (passback→mode→start→end→product→zone→route/location), Aztec/Corethree format `02`, offline-same-business-rules, "read-to-beep ≤1s" (touched by C4101087 timings). |
| **FBD-100651** (Glider TOO PV) | C4101001 (cEMV enablement by route/location/fare), C4101002 (TOO flat-fare), C4101088 (decline reasons + route-type), C4101089 (JourneyTap + alighting derivation), C4101003 (transfers), C4100998/C4101075 (contactless tap) | Assert the **check order** (ABT Type "Tap On Only (Flat Fare)" → Metro Network Zone → fare for first ABT product), **synthetic alighting via Furthest Alighting Point file `ProductSearchKey="ABT"`**, route audited as **"GLIDER"**, and Declined Reasons **1/2/3/15/20** into the audit. Stubs don't pin these. |
| **FBD-100690** (NIR TOTO PV) | C4100996 (NIR transfer), C4100997 (rail zone), C4102429 (ABT tap success shows NI travel line), C4101036 (ABT Tag successful - Rail screen) | Tap-on vs tap-off behaviour, check order (ABT Type "Tap On Tap Off" → NI Zone → "ABT Tap Product Name"), Declined Reasons, and that PV only taps (all fare/journey logic is BOS `[BOS-scope]`). |
| **FBD-100658** (ABT audit) | C4101089, C4101092 (tap audit content: JourneyTap, stop/stage, direction, payment method) | Pin constant fields (`paymentType=ABT`, `revenue=0`, `CardType=emv`, `passCount=true`, `ticketsIssued=false`), **`Fare` pounds vs `fareCost` pence**, product **7000**, `TapId` format, `TransferRouteType="Directional"` (PV), `gpsCoordinates` present. |
| **FBD-100720** (pilot list) | C4101078 (pilot list mgmt+validation), C4101000 (BIN/Deny/Pilot handling) | Enrolled token → normal success+audit; **non-enrolled → reject + NO audit** (see Missing); ABT-Type-enabled topology precondition. |
| **FBD-100359** (SaaS offline) | C4100995 (offline transaction + reconcile), C4101085 (comms resilience/failover), C4101021 (txn upload) | Comms-locked OOS end-state (see Missing); queued-then-delivered-via-RabbitMQ-on-restore end-to-end; KeyCloak/DNS switchover no-recommission. |
| **FBD-100266** (heartbeat) | C4101082 (MERIT heartbeat) | 15-min StaffList call-in even signed-out/no-sales; resets Hours-Since-Last-Comms to 0 (naming caveat in Stale-or-Wrong). |
| **FBD-100307** (deny/BIN cadence) | C4101020 (Deny/BIN download), C4101079 (Deny/BIN updates), C4101000 | Assert **full ≥ once/day + delta every 15 min**, 100k→200k (CR106) deny cap, ~30-min propagation to a new token. |
| **FBD-100236 / 100250 / 100277** (card tech/format) | C4101007 (legacy smartcard), C4101008 (MIFARE/DESFire), C4101090 (inter-device top-up) | DESFire ABT card format fields, preprinted-smartcard format, card-reference-file usage — not asserted in stubs; grounding for these three FBDs not deeply reviewed here (see note). |
| **FBD-100296** (stop/route) | C4102430 (commissioning — location programmed), C4101012/C4101055 (location settings) | PV "Metro Network Zone" / "Northern Ireland Zone" location membership drives ABT enablement (cross-links FBD-100651/100690); ETM sign-on/GPS rules are ETM-scope, N/A to PV. |

---

## Grounding note

- **Dump depth is the dominant caveat.** The CLI dump exposes each case's **title, section, refs, and `custom_steps`** —
  but in this suite `custom_steps` is a **single `Given` line (or one summary sentence) for every one of the 122 cases**;
  there is **no stored When/Then body**. So every classification above is inferred from title + section + that one line.
  A "COVERED"/"PARTIAL" here means *a dedicated case targets the rule*; it does **not** confirm the assertions are written.
  All detail-level findings (audit-field pins, Declined-Reason codes, CR116 edges, no-audit-on-reject) **must be verified
  against the full case bodies in TestRail** before acting — and most cases will need their When/Then authored regardless.
- **Cross-suite scope:** ABT tap-matching, capping, MERIT/portal, PJT/CSV import from FBD-100690/100662/100651/100389/100307
  are `[BOS-scope]` (suite 30279); this PV report keeps only the PV-device-visible slice.
- **Correctly out of PV scope (no gap):** cEMV revenue inspection (FBD-100716 — HHD-only) and the Integrated Barcode API
  single-use flow (FBD-100483 — TVM/HHD-only). The suite correctly has no PV cases for these; do not add any.
- **Specs read for this pass:** FBD-100167, 100317, 100483, 100651, 100662, 100690, 100658, 100720, 100359, 100266,
  100307, 100389, 100716, 100271, 100296. FBD-100236 / 100250 / 100277 / 100318 (card formats / barcode product config)
  were not opened in full — the card-tech PARTIAL rows above are provisional pending those notes.
