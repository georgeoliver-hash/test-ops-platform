# Proposal: restructured Translink ETM suite

Goal: take `AA-ETM-Acceptance Test` (4943) and rebuild it into a cleaner, test-type-first new suite
`**NEW** ETM-Acceptance Suite` (30254) — reuse good old cases, write new ones for the gaps the
Overflow flows expose, and handle Metro/Ulsterbus without duplication. Read-only / propose-first.

**Status: CONFIRMED — building.** Overflow flow-data mined (16 flows / 196 notes / 365 screens),
run-history audited, scope + modes confirmed by George 2026-06-05. Building area-by-area as
`<area>.cases.yaml` → `push --commit` (auto-audit gates each push); George does UI moves/bins.

## Scope (George 2026-06-05)
- **ETM device only (~897 cases).**
- **EXCLUDE** the ~26 CloudFare/BOS **web-admin** cases (Dashboard/Reports/Settings/ABT/Schedule/
  Estate/BI/Menu/Events screen-content, CloudFare sign-on, Staff/Asset Manager, Rules/Products/
  Tickets/Route admin) — different system, belongs in a BOS suite. The only run-history in the old
  suite is these; see `run-history-audit.md`.
- **KEEP ETM↔BOS interaction** that *impacts the ETM* (software/config distribution **to the ETM**,
  audit/data upload, commissioning, comms-lock, "ETM in Working State when BOS Connection Lost") —
  these are ETM device behaviour (old "System Management / BOS Comms"). → Non-Functional / Comms.
- **EXCLUDE BV (Bus Validator)** entirely — it's a separate device type with its own suite. KEEP only
  ETM "Other devices" cases where the **ETM manages a paired BV** (ETM is the actor). Drop the 3
  `For Removal? … Bus Validator` cases and the BV HMI screens (8.9.x).

## Operating modes (George 2026-06-05: confirmed; structure rationale revisited 2026-06-11)
- Modes: **Metro · Ulsterbus** (bus device; **no NIR/rail**, unlike POS). Glider = transfer cases.
- Mechanism: **shared cases authored once**, executed against each mode via TestRail **Run
  Configurations** (Metro / Ulsterbus). Mode-specific cases only where steps genuinely differ
  (zone-vs-boarding-stage validation, ABT zones, Capping) and are named by mode.
- **Structure is feature/test-type-first, NOT mode-first like POS — deliberately.** Department
  convention (recorded 2026-06-11): pick suite structure by **degree of mode divergence**. Many
  modes / heavy divergence incl. rail (POS: NIR/Ulsterbus/Metro, mode-first sections) vs few modes /
  near-identical (ETM: 2 bus modes ~95% shared, feature-first + Run Configurations). Same execution
  mechanism either way; only the organisation differs, matched to the device. ETM has only ~7
  mode-specific cases — mode-first sections would create two near-empty trees and split the shared
  95% for no benefit.
- **Mode coverage is documented in `mode-coverage.md`** (the shared / Metro-only / Ulsterbus-only
  map) — that is ETM's equivalent of POS's mode sections, giving the same visibility without the
  duplication. It is also the spec for setting up the Run Configurations.

## Proposed section tree (derived from 11 Overflow flows + old suite + test-type-first)
```
**NEW** ETM-Acceptance Suite            ← Configurations: Metro · Ulsterbus
│
├─ SMOKE                                @mode(all)   thin critical path
│     driver sign on → FLU → issue ticket → print → sign off
│
├─ FUNCTIONAL
│   ├─ Sign On & Session                @mode(all)   [Driver Sign On flow] (Driver/Supervisor/Technician)
│   ├─ Navigation                       @mode(all)   [Navigation flow] — menu traversal / back / idle
│   ├─ Fare Look-Up (FLU)               @mode(all)   [FLU flow]
│   ├─ Basket Mode                      @mode(all)   [Basket Mode flow]
│   ├─ Ticket Issue                                   per-product; shared vs Metro/Ulsterbus per audit
│   │     incl. Promo Menu, Change Receipts, printer-interrupt-during-issue
│   ├─ Smartcards & ABT                               LARGE matrix; shared vs mode per audit
│   │     ABT tap (Visa/MC/Wallet/declined), Concessionary, Commercial (MJ/Travelcard/iLink/…),
│   │     Hotlisted, Inter-Device, Tap Annulment, Capping Groups
│   ├─ Driver Menu & Options            @mode(all)   [Driver Menu/Options flow] (annulments, totals,
│   │     messages, other devices, paper status, reboots, Word & Colour, breaks, open tickets)
│   ├─ Supervisor                       @mode(all)   [Supervisor flow]
│   ├─ Technician                       @mode(all)   [Technician flow]
│   ├─ Barcode Scanning                 @mode(all)   [Barcode flow] (single online/offline, multiple,
│   │     mLink, legacy, printing, reference entry)
│   ├─ Location                         @mode(all)   GPS / Manual Stage Selection
│   └─ Revenue Limit                    @mode(all)   [Revenue Limit flow] — confirm rule from annotations
│
├─ NON-FUNCTIONAL / RESILIENCE          @mode(all)
│   ├─ Power Interruption                            [Power Interruption flow]
│   ├─ Display LEDs & Audio Tones                    [LEDs/Audio flow] — likely new coverage
│   ├─ Paper / Printer Management                    paper status, firmware update, printer interrupts
│   ├─ Comms / CloudFare (loss + commissioning)      System Mgmt / BOS Comms
│   ├─ Time Change (GMT/BST), Power Saving Mode
│   └─ Timing / Performance                          from Exploratory / Timing Tests
│
├─ HMI / SCREEN VALIDATION                           mirror exact UI screen names (advisory titles)
│     1.0 Sign On … 12.0 Barcodes + Ticket Layouts — carry Overflow link + image filename in preface
│
└─ REGRESSION
      ETM "Regression Defects" (41) folded into the FUNCTIONAL case that owns the behaviour
      (linked via Refs); only un-homeable defects live here.
```

## Governing mindset
All add/edit/merge/fold/leave decisions follow **`docs/test-practices.md`** — risk-based, minimal
sufficient coverage, no duplication, one behaviour per case, traceability via Refs. The product×mode
cross-tab is mandatory before authoring Smartcards/ABT and Ticket Issue (the POS lesson: guessing
shared-vs-mode produced wrong duplicates).

## Old → new mapping
Per-area `<area>.cases.yaml` built into 30254 via `push` (idempotent, new-suite-only). Old suite
untouched; "leave" = simply not carried over. UI moves/bins done by George (API can't move/delete on
this instance).

## Push defaults for this suite
```yaml
suite_id: 30254
defaults:
  template_id: 1
  custom_autoconfirmation: false
  custom_devtypes: [25]
  custom_revstatus: 2
```

## Gated on (before any authoring)
1. Overflow flow-data JSON (Network-tab export) → mine 11 flows' annotations.
2. Requirements / REQ docs.
3. George's confirmation of: mode model (Metro+Ulsterbus, no rail), the shared-vs-mode product split,
   and scope of Navigation / Display-LEDs-&-Audio / Revenue Limit.
4. George's sign-off on this section tree.
```
