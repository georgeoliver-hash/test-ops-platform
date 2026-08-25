# Proposal: restructured Translink GV (Gate Validator) suite

Goal: consolidate `AA - Gate Validator - Acceptance Test` (14973, **1,184 cases**) into a cleaner,
**test-type-first** new suite `**NEW** GV Test Suite` (**30286**) — reuse good old cases, collapse the
4× operating-mode clone into mode **Run Configurations**, and fold the per-build regression by
feature. **Read-only / propose-first: this is the blueprint, not authoring.** Evidence:
`old-suite-audit.md` (this folder). Governing mindset: `docs/test-practices.md`.

> **CRITICAL CAVEAT — thin requirement grounding.** The gate functional spec **FBD-100348** is a
> factory **acceptance report** with many rows marked *"To be validated on integration of Validator."*
> So this structure is built primarily from the **old suite**, and every area is tagged
> **`[spec-grounded]`** or **`[needs-spec]`** below. **We do not assert unvalidated gate behaviour** —
> needs-spec areas are carried across as flagged scaffolding, not as validated acceptance criteria.

## Mode decision (the crux — follows the ETM/TVM precedent, not POS)
- The old suite's four top-level sections — **Entry · Exit · Bi-directional A→B · Bi-directional B→A**
  — are **near-identical clones** (1,016 / 1,184 cases; see audit §1). They are the **Controlled
  sub-modes** of FBD-100348 (entry / exit / bi-directional direction).
- **Decision:** structure is **feature/test-type-first**; the **gate direction/mode is a TestRail Run
  Configuration** — shared validation behaviour authored **once**, executed against each
  configuration. Mode-first section trees would recreate the four-way clone and split the shared
  matrix for no benefit (the POS lesson, recorded in `etm-suite-restructure/structure.md`).
- **Mode-specific leaves appear only where behaviour genuinely diverges:**
  1. **Exit / bi-directional — ABT deny-list exception** `[spec-grounded FBD-100690]`: on a failed
     deny-list check in an exit-capable mode the gate **still opens**, the tap is audited **invalid**,
     and a **debt retry** is triggered. (Entry mode rejects.)
  2. **Gate Direction ⇒ Tap classification** `[spec-grounded FBD-100690]`: entry ⇒ Tap-On, exit ⇒
     Tap-Off — audited differently.
  3. **NIR Transfer direction** `[needs-spec]` — any genuinely direction-specific transfer-window
     behaviour (TIBU-22401 territory).
  Everything else (product acceptance, barcode, passback, screens) is **shared across modes**.
- **Mode/head coverage lives in `mode-coverage.md`** (to write): the shared / entry-only / exit-only
  map, the **Primary(Entry/unpaid) vs Secondary(Exit/paid)** head split, and the Run-Configuration spec.

## Proposed section tree
```
**NEW** GV Test Suite (30286)     ← Configurations: Direction{Entry · Exit · Bi-di A→B · Bi-di B→A}
│
├─ SMOKE                                     @mode(all)   thin critical path
│     both heads boot to service → present valid card → success screen + beep → gate opens → passback reject
│
├─ FUNCTIONAL
│   ├─ Gate Mode & Access Control            [spec-grounded FBD-100348 — PENDING INTEGRATION]
│   │     authorise→open ≤650/900ms; no-authorise→stays closed; obstruction blocks + infraction;
│   │     mode matrix (Controlled/Free/Locked/Maintenance/Evacuation/OOS); evacuation priority;
│   │     open-fail 3s⇒OOS; 3-consecutive-close-fail⇒OOS   ← assert as pending-integration, not validated
│   ├─ ABT cEMV Taps                          [spec-grounded FBD-100690]
│   │     Visa/Mastercard/Maestro; Declined Reasons 1(Expired)/2(Deny)/3(ODA)/15(BIN)/20(Passback);
│   │     success⇒gate opens; Offline Transaction
│   │     └─ Exit/Bi-di deny-list exception   @mode(exit,bidi)   gate opens, invalid audit, debt retry
│   ├─ Multi-Use Barcode Validation           [spec-grounded FBD-100167]
│   │     printed + mobile; product sweep (Adult/Child/3-Day Select/1-3 Off Day Return/24+/Ylink/
│   │     Concession/Half Fare/Day Tracker/Unemployed Day Return); TVM- vs HHD-produced; cross-device
│   │     already-validated reject; expired reject; result states green / yellow(step-7-only) / red;
│   │     gateline Unique-ID share (CR105.2); rail £90 fallback (CR105.3); CR116 expiry display
│   ├─ Passback                               [spec-grounded FBD-100167/100690]   re-present within window ⇒ reject
│   ├─ Smartcard Product Validation           [NEEDS-SPEC — cross-ref FBD-100236/100250/100271]
│   │     iLink (Belfast Visitor + Zones 1/2/3/4/NW, Adult/Child); Employee/Staff family;
│   │     Rail-EA Pupil & Further-Ed; aLink; concessionary SmartPass sweep; Metro-MJ/Daylink/
│   │     Travelcard/Town-Service; 24+/Ylink; Valid(new/used/passback) & Invalid(hotlist/expired/
│   │     torn/out-of-zone/before-start); card tech DESFire / MIFARE Classic EV1
│   │     ⚠ carried as FLAGGED scaffolding — no issued GV spec asserts per-product gate acceptance
│   ├─ NIR Transfers                          [NEEDS-SPEC — partial FBD-100690 free-transfer]
│   │     within/after transfer period, per product & direction
│   └─ Legacy Support                         [NEEDS-SPEC / cross-ref]   POS/legacy top-up → validate on GV
│
├─ COMMISSIONING & CONFIG                     [spec-grounded FBD-100653/100654 — field procedure, low auto value]
│   ├─ Technician Menu & Location Settings    sign-on/PIN, navigation/timeout, Home/Stop/Zone/Install-Point/ID,
│   │                                          software+config versions, backlight, audio volume, force comms
│   ├─ Post-commission verification           Primary=Entry/unpaid & Secondary=Exit/paid roles; SkyLane HF03 +
│   │                                          Std/Wide variant; homeLocation/zoneNo; router .200/gw.0.1/port-80 NAT
│   └─ Software / Config Distribution          SW / config / barcode-data file download; future activation date
│
├─ NON-FUNCTIONAL / RESILIENCE
│   ├─ Primary/Secondary Head State Machine   [NEEDS-SPEC — bug-derived; FBD-100348 heartbeat PENDING]
│   │     OOS recovery after power failure; nightly-reboot recovery; Fully-Free handling; remote-command /
│   │     Station-Manager mode changes; tech-signon-on-Secondary side effects; heartbeat-loss⇒major-fault;
│   │     power-up=OOS-until-both-comms; mains-restore=previous-mode
│   ├─ Light Pictograms                       [spec-grounded FBD-100348 PIC — pending integration]
│   │     passage permitted / not permitted / infraction (blinking red) / OOS
│   ├─ Power / Emergency / Evacuation          [spec-grounded FBD-100348 FUN — pending integration]
│   │     mains fail with user in gate; ≤2s power loss no-reboot; Emergency Release Button
│   ├─ Comms / BOS                             [partial FBD-100263/100358]   loss/failover, upload audit, corrupt config
│   ├─ Audio Feedback                          [NEEDS-SPEC]   card-present tone; blind/partial-sight assist messages
│   ├─ Time / DST / Operating Times            [needs-spec]   GMT↔BST offline, start-time reconfigure, time sync
│   └─ Throughput / Performance / Sensor / Settings  [NEEDS-SPEC]   Primary/Secondary throughput, sensor calibration,
│                                              screen background colour, data mirroring
│
├─ HMI / SCREEN VALIDATION                     mirror exact UI screen names (advisory titles)
│     smartcard screens (idle/not-in-service/re-present/not-valid-location/invalid-time/expired/faulty/
│     not-accepted/passback/success); barcode error+success screens [FBD-100167]; technician-menu screens [FBD-100654]
│
└─ REGRESSION
      NOT a parking lot. 75 Fixes/Changes (4.1.0→4.2.0) + 3 Previous TIBU folded into the FUNCTIONAL /
      NON-FUNCTIONAL case that owns the behaviour (linked via Refs incl. TIBU-#####). Dedupe recurring
      ids (18302/16372/18310/18606/18566/14160). Only un-homeable defects live here.
```

## Spec-grounded vs needs-spec — the split at a glance
| Area | Grounding | Build stance |
|---|---|---|
| ABT cEMV Taps (+ exit deny-list exception) | **FBD-100690** `[grounded]` | Author validated assertions |
| Multi-Use Barcode Validation + Passback | **FBD-100167** `[grounded]` | Author validated assertions |
| Gate Mode & Access Control, Pictograms, Power/Emergency | **FBD-100348** `[grounded but PENDING INTEGRATION]` | Author as **pending-integration** — do not mark validated |
| Commissioning / Location / Distribution | **FBD-100653/100654** `[grounded]` | Author, but note field-procedure / low auto value |
| Comms / device status to CloudFare | **FBD-100263/100358** `[partial]` | Author cautiously; cross-ref ETM |
| **Smartcard Product Validation (~55%)** | **none in GV set** `[needs-spec]` | **Carry as flagged scaffolding; do NOT assert gate acceptance until spec sourced** |
| **NIR Transfers** | partial `[needs-spec]` | Flagged; confirm transfer-window rule |
| **Primary/Secondary head state machine** | bug-derived `[needs-spec]` | Flagged; governing FBD-100348 rows are pending-integration |
| **Audio Feedback / Throughput / Sensor / Settings / DST** | none `[needs-spec]` | Flagged device-config/exploratory |

## Estimated consolidated case count
Old raw = **1,184**, inflated by three multipliers the new suite removes: **(a)** the 4× operating-mode
clone (1,016 cases → one shared tree + mode Run Configs + ~3 divergent leaves); **(b)** per-product
permutation explosion in the smartcard sweep; **(c)** 78 per-build regression cases folded into
functional homes via Refs.

| New area | Est. cases | Grounding | How it collapses the old total |
|---|---:|---|---|
| Smoke | ~6 | mixed | one critical path, both heads |
| Gate Mode & Access Control | ~15 | grounded (pending) | new/consolidated from FBD-100348 rows |
| ABT cEMV Taps (+ exit leaf) | ~15 | grounded | dedupe across 4 modes; +declined-reason matrix |
| Multi-Use Barcode Validation | ~25 | grounded | one product sweep (was ×4 modes ×TVM/HHD) |
| Passback | ~4 | grounded | one section (was ×4 modes) |
| Smartcard Product Validation | ~55 | **needs-spec** | parametrise product×Adult/Child; representative concessions, not every SmartPass ×4 modes |
| NIR Transfers | ~12 | needs-spec | one section (was ×4 modes ×~38) |
| Legacy Support | ~6 | needs-spec | representative zones, not all |
| Technician Menu & Location | ~15 | grounded | de-cloned |
| Commissioning verification + Distribution | ~12 | grounded | field-procedure checks |
| Primary/Secondary Head State Machine | ~20 | needs-spec | consolidate the regression cluster into behaviour cases |
| Pictograms / Power / Emergency / Evac | ~10 | grounded (pending) | |
| Comms / BOS | ~8 | partial | |
| Audio / Time-DST / Throughput / Sensor / Settings | ~12 | needs-spec | |
| HMI / Screen Validation | ~28 | mixed | carry Screens 1:1 (advisory titles) |
| Regression (un-homeable only) | ~10 | — | remaining ~68 folded via Refs |
| **Total** | **≈ 250–300 (~270)** | | **~77% reduction vs 1,184 raw** |

## Suites
- **Source (old, read-only):** 14973 `AA - Gate Validator - Acceptance Test`. Never modified/deleted from.
- **Target (new):** 30286 `**NEW** GV Test Suite` — everything built here. Copy-out only.

## Push defaults for this suite
```yaml
suite_id: 30286
# Run discover-fields against project 42 + a sample GV case to confirm the real block before authoring:
# python -m system_test_ops discover-fields --project 42 --sample-case <gv_case_id>
defaults:
  template_id: 1
  custom_devtypes: [ <GV — confirm via discover-fields> ]
  custom_revstatus: 2
  custom_autoconfirmation: false
```

## Gated on (before any authoring)
1. George's sign-off on this section tree and the **direction = Run Configuration** decision.
2. **Resolve the needs-spec list** — above all, **source a spec for per-product smartcard acceptance
   at the GV** (the ~55% bulk). Until then those cases stay **flagged scaffolding**, not validated.
3. Confirm FBD-100348 items are treated as **pending-integration** (not validated acceptance).
4. `mode-coverage.md` written (shared / entry-only / exit-only map + Primary/Secondary head split +
   Run-Configuration spec).
5. `discover-fields` run against project 42 to fix the real `defaults:` block (GV devtype id).
