# PV mode-execution tagging — Glider / Rail

**Why this doc exists.** PV runs under 2 Configurations: **Glider** and **Rail**. Unlike ETM's
Metro/Ulsterbus split (documentation-only map, no Refs tags), George asked for a queryable
**Refs tag on every case** in suite 30255 so a run can be built by filtering — "avoid re-running
mode-irrelevant cases twice." This doc records the scheme and the per-case rationale; the tags
themselves live in each case's **Refs** field in TestRail (appended, not replacing existing refs).

**Applied:** 2026-07-27, all 184 live cases in suite 30255 (project 42), the 1 pre-existing
condemned case (`C4101005`, `ZZ_DELETE_REVIEW`) excluded. Script:
`tools/tag_pv_modes.py`-equivalent (one-off, run from the session scratchpad; see the changelog for
the exact script and command). Re-audit after tagging: **CLEAN — 0 blocking, 47 advisory**
(pre-existing title-style items, unrelated to this change).

## The four tags

| Tag | Meaning | Run once or twice? |
|---|---|---|
| `MODE-BOTH` | Shared case, steps identical Glider/Rail, but the **outcome could plausibly differ by mode** (fare/product/config-driven behaviour) | Run under **both** Configurations |
| `MODE-GLIDER-ONLY` | Case is genuinely Glider-specific (cEMV/ABT, TOO, FEIG, Pilot List) | **Glider** only |
| `MODE-RAIL-ONLY` | Case is genuinely Rail-specific (NIR transfers, zone, rail-only ABT/legacy behaviour) | **Rail** only |
| `MODE-PRIMARY-ONLY` | Shared **and** genuinely mode-irrelevant (Technician Menu, most Non-Functional, non-fare HMI, comms/hardware) | Run **once** |

## Tally (184 live cases)

| Tag | Count |
|---|---|
| `MODE-BOTH` | 60 |
| `MODE-GLIDER-ONLY` | 36 |
| `MODE-RAIL-ONLY` | 12 |
| `MODE-PRIMARY-ONLY` | 76 |
| **Total** | **184** |

## Grounding — how each section was classified

Classification is grounded in the **live case bodies** (preconditions/steps explicitly say "Glider
PV", "Rail PV", "NIR", "cEMV", etc. — not inferred from section names alone, since the suite has
grown substantially since `coverage-map.md`/`structure.md` were written), cross-checked against
`knowledge/flows/pv-flow-annotations.md` (the Overflow UX annotations, which explicitly call out
"Glider PV only screens" for the cEMV/EMV decline-reason screens, and the "For NIR/Rail PVs this
will state 'Northern Ireland Travel Only'" annotation for the ABT Tag Successful screen).

### `MODE-BOTH` (60)
- **Functional > Smartcard Validation** (33) — every product-family case explicitly says "Run under
  Glider and Rail" in its Expected result (e.g. Concession SmartPass, Half-Fare, Metro Daylink/MJ/
  Travelcard, Ulsterbus MJ, iLink/Belfast Visitor, aLink, yLink/24+, Employee smartcards, EA Pupil/FE,
  inter-device top-up). Same steps, but product/zone/time-band rules are config-driven so the
  outcome could plausibly differ per install.
- **Functional > Validation Outcomes** (4) — shared invalid reasons, passback, offline transaction,
  machine-not-in-service: generic outcomes, config-driven.
- **Functional > Barcodes** (11) — per-product multi-use barcode validation (Adult/Child/3-Day
  Select/1-3 Off Day Return/24+/Ylink/Concession/Half Fare/Day Tracker/Unemployed Day Return) +
  early-morning-expiry display rule. Fare/product-driven, same reasoning as smartcards. *(Inferred —
  these cases don't say "Run under Glider and Rail" explicitly the way the smartcard family does;
  flagged uncertain below.)*
- **Functional > Legacy & Card Tech** (4) — Legacy journey/time-based smartcards, MIFARE/DESFire card
  tech, Passback re-presentation, Operating Times: product/config-driven validation rules.
- **Functional > Barcode Validation** (2 of 3) — Multi-Use Barcode valid (green)/invalid (red)
  outcome checks (fare/product-driven, paired with the barcode family above). The third case in this
  section (Single-Use rejection) is `MODE-PRIMARY-ONLY` — see below.
- **Smoke** (3 of 6) — valid smartcard / invalid smartcard / valid barcode: mirrors the `MODE-BOTH`
  mechanism it smoke-tests. *(Inferred by analogy, not stated in the case text — flagged uncertain.)*
- **HMI — ABT deny-list / error-reading-card / hotlisted-card screens** (3) — these three screens
  live in the shared `Platform Validator-Barcode` Overflow flow with no Rail-suffixed variant (unlike
  `ABT Tag successful`, which has an explicit `... - Rail` twin), suggesting they render on both
  configs. *(Genuinely uncertain — flagged below; they pair with Glider-only cEMV decline-reason
  functional cases, so an argument for `MODE-GLIDER-ONLY` exists too.)*

### `MODE-GLIDER-ONLY` (36)
- **Functional > ABT (Glider)** (30) — every case's precondition explicitly states "a Glider PV" /
  "Glider PV on a Tap-On-Only route" (contactless tap validation per scheme, declined/errored tap,
  BIN/Deny/Pilot list handling, cEMV route/location/fare enablement, Glider TOO, Glider transfers,
  ABT end-to-end, Pilot List management, Deny/BIN list updates, FEIG reader software + card reading,
  cEMV route-type enablement, JourneyTap audit, tap audit content, EMV result screens, FEIG
  update-without-TID/TK, all 7 cEMV decline-reason cases, both duplicate-tap cases). Grounded further
  by `pv-flow-annotations.md`'s "Glider PV only screens" annotation on the cEMV decline-condition
  screen (`1.3.3 Invalid Card`) that these cases cite.
- **Functional > Pilot List** (3) — explicitly gated on `Enable Pilot List=True` / "ABT enabled via
  the ABT Type route attribute" / cEMV FEIG tokens — Glider/cEMV-only mechanism.
- **Smoke — ABT contactless tap succeeds** (1) — precondition: "a Glider PV has ABT enabled."
- **HMI — `1_6_1_1 ABT Tag successful`** (1, the base/non-Rail-suffixed screen) — pairs with the
  Rail-suffixed twin (`MODE-RAIL-ONLY` below); this is the Glider-side rendering of that screen.
- **Non-Functional > PV — `PV to BOS — Deny and BIN list download`** (1) — precondition explicitly
  states "the PV has cEMV and back-office comms" and the lists are "applied to the PV FEIG for cEMV
  validation" — cEMV is Glider-only, so this NFR case only has a real outcome on Glider PVs.
  *(Judgment call — flagged uncertain: it sits in the generic Non-Functional > PV section, not the
  Glider-only Functional section, and its sibling `PV to BOS — software and FEIG update via CloudFare
  TMS` was kept `MODE-PRIMARY-ONLY` since it lacks the same explicit cEMV precondition.)*

### `MODE-RAIL-ONLY` (12)
- **Functional > Rail-specific** (8) — NIR transfer validation (iLink, Belfast Visitor, Staff
  Smartpass, aLink, EA Pupil, EA Further Education), Rail zone validation, and the Rail-specific ABT
  tap success case (Northern Ireland travel line) — all explicitly precondition "a Rail (NIR) PV."
- **Functional > ABT Audit — NIR Audit** (1) — precondition: "a NIR PV whose home-location first
  route carries ABT Type 'Tap On Tap Off'... within the Northern Ireland Zone."
- **Functional > Legacy Transfer** (2) — both cases precondition "a PV validating a **legacy rail**
  smartcard" with worked examples at Botanic/Lanyon Place (NIR stations).
- **HMI — `1_6_1_1 ABT Tag successful - Rail`** (1) — the explicit Rail-suffixed screen variant,
  grounded in the Overflow annotation ("For NIR/Rail PVs this will state 'Northern Ireland Travel
  Only'").

### `MODE-PRIMARY-ONLY` (76)
- **Functional > Technician Menu** (12) — login, location settings, display, software/configuration
  versions, force communications, network settings, operating times, backup/layout/audible feedback,
  sign off, reboot, audio settings, auto sign-off/timeouts. No Glider/Rail divergence anywhere in the
  case bodies — pure technician mechanics, identical either way.
- **Non-Functional > PV** (12 of 13) — power recovery, PV-BOS software/FEIG update, transaction
  upload, GMT/BST clock change, MERIT heartbeat, scheduled reboot, config/topology distribution,
  scheduled maintenance, performance timings, stability/recovery, asset/version reporting, Device Log
  Manager. Comms/hardware/maintenance mechanics — no mode-dependent outcome.
- **Non-Functional > Comms** (3) — Ethernet↔cellular failover, comms lock (sustained dual-channel
  loss), comms recovery. Confirmed **not** mode-specific: `proposals/coherence-audit/fixes/
  pv-failover-restore.changelog.md` records that the old suite's failover case existed for **both**
  the NIR route (`C2700890`) and the Glider route (`C3275939`) with identical behaviour.
- **HMI Screen Validation > Validation Screens** (20 of 25) — Loading, Present SmartCard/Barcode
  variants, Machine Not In Service, Represent Card, Unable to Validate, Not Valid At This Location,
  Invalid Time Of Day, Product Expired, Passback (Journeys/Days Left, No Entry), Tag successful
  (base), all 6 Barcode Validation outcome screens. Generic, non-fare-differentiated renders.
- **HMI Screen Validation > Technician Menu** (24) — all technician-menu screens, generic.
- **Smoke — Technician Menu login / PV communicates with the back office** (2) — generic
  technician/comms mechanics.
- **Functional > Commissioning** (1) — uncommissioned-until-location-programmed: a generic
  provisioning mechanic.
- **Functional > Barcode Validation — Single-Use rejection** (1) — the case states the PV rejects
  single-use barcodes categorically ("the PV validates multiple-use barcodes only... single-use is
  validated by POS and TVM, never the PV") — a fixed device capability, not a per-mode rule.
- **Functional > Barcodes — reader disconnect banner/event** (1) — a hardware-fault scenario
  (barcode/smartcard reader disconnected), unaffected by Glider/Rail.

## Flagged uncertain (judgment calls worth a second look)

1. **Barcode family "inferred MODE-BOTH"** (11 multi-use product cases + early-morning expiry, plus
   the 2 Barcode Validation green/red outcome cases and 4 Legacy & Card Tech cases, 17 total) — none
   of these cases say "Run under Glider and Rail" the way the Smartcard Validation family does. Tagged
   `MODE-BOTH` by analogy (fare/product-driven), but it is possible some or all barcode products are
   only ever used on one mode in practice — worth confirming with George/the fares team.
2. **Smoke smartcard/barcode cases "inferred MODE-BOTH"** (3) — same reasoning/caveat as above.
3. **HMI ABT deny-list / error-reading-card / hotlisted-card screens** (3, `C4101038`/`39`/`40`) —
   tagged `MODE-BOTH` because they have no Rail-suffixed variant in the Overflow flow (unlike ABT Tag
   successful), but they pair functionally with the Glider-only cEMV decline-reason cases. A case
   could be made for `MODE-GLIDER-ONLY` instead — needs a look at whether Rail PVs can actually
   present these three outcomes.
4. **`PV to BOS — Deny and BIN list download`** (`C4101020`) tagged `MODE-GLIDER-ONLY` on its explicit
   "PV has cEMV" precondition, while its sibling **`PV to BOS — software and FEIG update via CloudFare
   TMS`** (`C4101019`) was left `MODE-PRIMARY-ONLY` since FEIG firmware plausibly exists as hardware
   on all PVs even though cEMV validation itself is Glider-only. The split between these two very
   similar-looking NFR cases is a judgment call — worth confirming whether Rail PVs carry a FEIG
   reader at all.

## Keeping this accurate
Re-tag any new case at authoring time (don't defer to a later sweep) — append the appropriate
`MODE-*` value to its Refs field per the rules above. If a case moves from generic to genuinely
mode-specific (or vice versa) as the suite evolves, update its tag and this doc's tally together.
