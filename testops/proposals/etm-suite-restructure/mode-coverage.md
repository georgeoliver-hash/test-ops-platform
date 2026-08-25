# ETM operating-mode coverage map

**Why this doc exists.** ETM is structured **test-type-first** (Functional / Non-Functional / HMI /
Regression / Smoke), not mode-first like POS. That is deliberate (see "Why ETM differs from POS"
below) — but it means the suite's *sections* don't tell you which mode a case runs in. Rather than
rely on a side document alone, every case in suite 30254 now carries a **Refs tag** —
`MODE-ALL` / `MODE-METRO-ONLY` / `MODE-ULSTERBUS-ONLY` / `MODE-PRIMARY-ONLY` — so George can filter
directly in TestRail when building a run, without a lookup step. This doc explains the tagging
scheme, gives the full case-by-case tally, and remains the place to update the *logic* when the
suite changes.

> **2026-07-27 rewrite.** This doc previously (2026-06-xx) described the shared/Metro-only/
> Ulsterbus-only split conceptually, before the 2026-07-24 variant-expansion pass took the suite
> from 456 → 516 non-`ZZ` cases (61 new cases from splitting "Data variations" lists into individual
> cases — see `proposals/coherence-audit/fixes/etm-variant-expansion.changelog.md`). Its case lists
> were stale. This rewrite **re-derived the classification fresh against live suite content**
> (`TestRailClient.get_cases(42, 30254)`, full body) — reusing the *logic* below, not the old lists —
> and tagged all 516 live (non-`ZZ`, non-retired) cases via `TestRailWriter.update_case_fields`.

## The 4-tag scheme (George, 2026-07-27)

| Tag | Meaning | Run it |
|---|---|---|
| `MODE-ALL` | Shared case, but the **outcome could plausibly differ by mode** (fare/ticket/product/capping/config-driven behaviour) even though the steps read identically. | Once per mode (Metro **and** Ulsterbus Run Configuration). |
| `MODE-METRO-ONLY` | Mode-specific: the behaviour, product, or zone/transfer mechanic **only exists on Metro**. | Metro configuration only. |
| `MODE-ULSTERBUS-ONLY` | Mode-specific: the behaviour, product, or zone/stage mechanic **only exists on Ulsterbus**. | Ulsterbus configuration only. |
| `MODE-PRIMARY-ONLY` | Shared **and** genuinely mode-irrelevant — Sign On mechanics, menu/hardware/non-functional plumbing, generic UI. | Once, either configuration ("Primary"), never both. |

Tags live in the case's **Refs** field (appended, existing citations preserved) — e.g. a case that
already cited `FBD-100662` now reads `FBD-100662,MODE-ALL`. This is the same mechanism used for
requirement/defect traceability elsewhere in the suite, so it needs no new TestRail field.

## The mode mechanism

ETM modes = **Metro** and **Ulsterbus** (bus device; **no rail/NIR**, unlike POS). Glider = transfer
cases. Modes are an **execution** concern, handled by TestRail **Run Configurations**, not by the
section tree:

- **`MODE-ALL` + `MODE-PRIMARY-ONLY`** cases (the large majority) are authored once. `MODE-ALL`
  runs under **both** Configurations; `MODE-PRIMARY-ONLY` runs under **one** (whichever is
  convenient) since the outcome cannot differ.
- **`MODE-METRO-ONLY` / `MODE-ULSTERBUS-ONLY`** cases run **only** under their own Configuration.

> **Live setup still needed:** create the two Run Configurations (Metro, Ulsterbus) on suite 30254 in
> the TestRail UI if not already done, then build runs by filtering Refs for
> `MODE-ALL,MODE-<mode>-ONLY` (mode-specific) plus `MODE-PRIMARY-ONLY` once per full-suite pass.

## Tally (516 live cases, `ZZ - To Delete` and the one pending-UI-move retired case excluded)

| Tag | Count |
|---|---|
| `MODE-PRIMARY-ONLY` | 294 |
| `MODE-ALL` | 183 |
| `MODE-ULSTERBUS-ONLY` | 25 |
| `MODE-METRO-ONLY` | 14 |
| **Total** | **516** |

Mode-specific cases (`METRO-ONLY` + `ULSTERBUS-ONLY`) are **39 of 516 (~7.6%)** — consistent with the
original "~95% shared" read for ETM (two near-identical bus modes), now precisely counted rather than
estimated, and larger than the ~7-case estimate in the pre-expansion doc because today's variant
expansion created new dedicated per-product/per-zone cases that didn't exist before (Smartcards >
Transfers, Multi-Journey's Metro Travelcard / Town Service Travelcard, several Ticket Issue / Promo
Menu named products, EA Rail SmartPass).

## `MODE-PRIMARY-ONLY` — mode-irrelevant, run once (294 cases)

Entire sections tagged `MODE-PRIMARY-ONLY` by default (mechanics/hardware/UI, not fare-outcome-driven):

- **Regression** (7) — all are mechanism/defect-level fixes (sequence ID integrity, Deny/BIN list
  sync, GDPR display, freeze-on-card-removal, menu navigation, performance, print speed), not
  fare-outcome-differentiated by mode.
- **Smoke** (6) — a thin sanity pass across features; run once regardless of mode by design.
- **Functional > Barcode Scanning** (16), **Driver Menu & Options** (14), **Supervisor Menu** (5),
  **Technician Menu** (8), **Location** (2), **Revenue Limit** (2), **Fare Look-Up > Navigation** (2),
  **Sign On & Session** (Driver 13 / Supervisor 5 / Technician 3), **Shift Board** (4 — duty/journey
  scheduling mechanics, no Metro/Ulsterbus signal found in content on re-derivation).
- **Non-Functional** (all 5 subsections, 26 cases) — comms, power, printer/paper, displays/LEDs/audio
  (except one passenger-display case, below), system/performance.
- **HMI Screen Validation**: Barcodes (15), Driver Menu (41), Numeric Entry (6), Power Management (3),
  Printer & Travel Mode (8), Sign On (47), Supervisor Menu (13), Technician Menu (27) — non-fare
  screens per the department convention.
- Within **Fare Look-Up > Sales** (mixed section, see below): 4 of 8 cases are operational mechanics
  (Travel Mode/schedule adherence, passenger count, favourite stages, start-new-journey mid-shift),
  not fare-outcome-driven, so tagged `MODE-PRIMARY-ONLY` even though the section default is `BOTH`.
- Within **HMI > Displays, LEDs & PID** (mixed section, 32 cases): 20 are hardware/generic (COTD
  colour-of-the-day LED codes ×8, CardReader LED codes ×8, generic Info screens ×4) — `PRIMARY-ONLY`.
  The other 12 mirror fare/product content (`PID/FLU/*`, `PID/Smartcard/*`, `PID/ABT/Success`) —
  tagged `MODE-ALL` instead (see below).

## `MODE-ALL` — shared, outcome could differ by mode (183 cases)

Fare/ticket/product/config-driven behaviour, run under both Configurations:

- **Functional > ABT** (12 of 14 — excludes the 2 zone-specific cases below): successful tap+passback
  (all card schemes), declined/error/EMV validation, tap-availability rules, invalid-tap Deny/BIN
  List recording, mobile wallet (Apple/Google/Samsung Pay).
- **Functional > ABT Audit** (2) — audit-field-format assertions (product id, pounds/pence); each
  case is grounded in one mode's worked example for concreteness but the claim itself reads as a
  generic ABT/TOO audit fact. **Flagged uncertain** — see below.
- **Basket Mode** (4), **Fare Look-Up > Sales** (4 of 8 — numeric entry+change, group ticket payment,
  ticket type selection, currency switch).
- **Smartcards**: Commercial (12: DayLink, Belfast Visitor Pass ×3, iLink ×5, aLink, yLink, 24+),
  Concessionary (11), Education (2 of 4 — EA Bus Pupil/FE; EA Rail is Ulsterbus-only, below), Faulty
  (3), Hotlist (1), Staff (5), Top-Up (10 — all variants incl. inter-device), Validation (6 of 8 —
  passback rules, faulty-card handling, fare-paying smartcard, outside-time-band, expired,
  hotlisted; the 2 zone/stage-specific cases are mode-only, below).
- **Ticket Issue** (7 of 19): annulment, Open Tickets excess fare, Day Return, iLink Single, Gateway
  (uncertain, flagged), Warrant Return, ME Rugby Day (uncertain, flagged).
- **Ticket Issue > Promo Menu** (4 of 8): promo-not-available, Family & Friends Day, Park & Ride
  (uncertain, flagged), ME Rugby Day (uncertain, flagged).
- **HMI**: Card Payment & Basket (8), Promo Menu (9), Smartcards (20), Fare Look-Up (50 of 51 — all
  except the Easibus screen, below), and the 12 fare/product-content PID screens noted above.
- **Non-Functional > Displays, LEDs and Audio**: 1 of 3 — Passenger Information Display (mirrors
  live transaction/fare content, so could differ by mode's product set); the other 2 (card-reader
  LED states, audio tones) are hardware mechanics, `PRIMARY-ONLY`.

## `MODE-METRO-ONLY` — Metro-specific (14 cases)

| Case | Area | Why Metro-only |
|---|---|---|
| ABT — Metro zone boarding and alighting | ABT | Zone-based fare derivation (Tap On Only – Flat Fare) |
| Metro Multi-Journey — zone validation (City / Inner / Extended) ×3 | Smartcards / Multi-Journey | Validates by **zone**, wrong-zone rejection |
| Metro Travelcard — validation | Smartcards / Multi-Journey | Named Metro product |
| Smartcard — invalid card presented (wrong zone, Metro) | Smartcards / Validation | Zone mechanic |
| Transfer — ETM decides transfer vs journey from ROUTE Transfer Time | Smartcards / Transfers | Explicitly Metro Transfer Zone / Metro Multi-Journey mechanic (FBD-100271) |
| Transfer — a stop outside the Metro Transfer Zone is charged as a journey | Smartcards / Transfers | as above |
| Transfer — passback is prioritised over the transfer window | Smartcards / Transfers | as above |
| Transfer — a transfer audits WTS SmartTransfer while a journey audits WTS SmartUse | Smartcards / Transfers | as above |
| Ticket Issue — issue a single ticket (Metro Single) | Ticket Issue | Named Metro product (see flagged content note below) |
| Promo Menu — issue a promo product (Metro Day / Metro Evening / Metro Family Day) ×3 | Promo Menu | Named Metro products |

**New finding vs the pre-expansion doc:** the entire **Smartcards > Transfers** family (4 cases, added
in the 2026-07-24 expansion from FBD-100271) is Metro-only — the old doc filed "direction/transfer-
period rules" generically under Shared because these dedicated cases didn't exist yet. Likewise
**Metro Travelcard** and **Town Service Travelcard** (below) are now their own dedicated cases, still
mode-homed the same way the old doc predicted for the *behaviour* but not previously tagged as
individual cases.

## `MODE-ULSTERBUS-ONLY` — Ulsterbus-specific (25 cases)

| Case | Area | Why Ulsterbus-only |
|---|---|---|
| ABT — Ulsterbus zone boarding and alighting | ABT | Driver-selected alighting stage (Tap On Only – Driver Initiated) |
| Capping — cap reached / journeys without reaching cap / multiple services and modes ×3 | Capping | Capping is an Ulsterbus concept |
| Rail Substitution — all 4 cases | Rail Substitution | Rail-sub bus service only runs under Ulsterbus |
| EA Rail SmartPass — validation (Pupil / Further Education) ×2 | Smartcards / Education | Grounded in a rail-substitution service, Ulsterbus-only mechanism |
| Ulsterbus Multi-Journey — boarding-stage validation | Smartcards / Multi-Journey | Validates by **boarding stage**, not zone |
| Town Service Travelcard — validation | Smartcards / Multi-Journey | Named Ulsterbus town-service product |
| Smartcard — invalid card presented (invalid boarding stage, Ulsterbus) | Smartcards / Validation | Stage mechanic |
| Ticket Issue — issue a single ticket (Month Return / Jobseeker) ×2 | Ticket Issue | Ulsterbus-only products (`knowledge/projects/translink.md`) |
| Ticket Issue — Easibus stage selection (Red/Orange/Yellow/Green/White/Buggy/Wheelchair/Other) ×8 | Ticket Issue | Easibus is an Ulsterbus rural service brand (FBD-100377) |
| Promo Menu — issue a promo product (Bus Rambler) | Promo Menu | Ulsterbus-only product (`knowledge/projects/translink.md`) |
| Screen Validation — 02.0.5 \| Easibus | HMI / Fare Look-Up | Easibus screen only renders on Ulsterbus |

## Flagged uncertain cases (for engineer confirmation)

Grounded classification could not fully resolve these from the sources searched (old suite, specs,
`knowledge/`); each was given the **safe conservative default** (`MODE-ALL`, so it is never
under-tested — worst case it runs once too often) rather than guessed mode-only:

1. **Ticket Issue — Gateway** (`C4104443`) and **ME Rugby Day** (`C4104449`, also in Promo Menu
   `C4104476`) — not in the known Metro/Ulsterbus/NIR product-ownership list
   (`knowledge/projects/translink.md`). Tagged `MODE-ALL`; confirm which mode(s) actually sell these.
2. **Promo Menu — Park & Ride** (`C4104474`) — FBD-100377 lists "Park & Ride" as a service
   classification, not clearly tied to one mode. Tagged `MODE-ALL`; confirm.
3. **ABT Audit — both cases** (`C4103557`, `C4103558`) — each is grounded in one mode's worked example
   (Ulsterbus route 72b / Metro route 10A respectively) but the audited-field claim itself (product id
   7000 for TOO taps; Fare-in-pounds/fareCost-in-pence format) reads as generic ABT auditing, not
   mode-specific. Tagged `MODE-ALL`; flag if either claim is actually mode-restricted.
4. **EA Bus SmartPass — Pupil / Further Education** (`C4102549`, `C4104511`) — grounded in an
   Ulsterbus route 72b worked example, but EA Bus (school) passes aren't obviously Ulsterbus-only the
   way EA **Rail** (rail-substitution) passes are. Tagged `MODE-ALL`; confirm.
5. ~~**Ticket Issue — issue a single ticket (Metro Single)** (`C4100550`) — content inconsistency~~
   **FIXED 2026-07-28**: preconditions corrected to a genuine Metro route 10A / Metro Single worked
   example. See this same finding's broader pattern below (item 8).
8. **`MODE-ALL` cases hard-coding a single operator's route — FIXED 2026-08-03.** The `C4100550`
   inconsistency above turned out to be one instance of a systemic bug: 62 of 183 `MODE-ALL` cases
   named one operator's route in their precondition (e.g. "signed on to Ulsterbus route 72b"), which
   is wrong under whichever Configuration doesn't match — confirmed as the majority cause of Invalid-
   Test marks in the live `ETM - OS v8.0.6356` run. All 62 fixed to generic wording ("a valid route").
   Full list and rationale: `proposals/etm-suite-restructure/mode-all-route-hardcoding.changelog.md`.
   New standing rule added to `docs/gherkin-standard.md`.
6. **Smartcards > Transfers family** (`C4103553`–`C4103556`) — tagged `MODE-METRO-ONLY` on strong
   textual evidence (explicit "Metro Transfer Zone" / "Metro Multi-Journey card" / "Metro route 10A"
   throughout), but this is a new read not present in the pre-expansion doc. Confirm there is no
   equivalent Ulsterbus transfer-zone scheme these cases should also cover.
7. **Ticket Issue — printer/power interrupt during print recovers** (`C4100557`) — tagged
   `MODE-PRIMARY-ONLY` (recovery mechanism, not fare-outcome) rather than `MODE-ALL`; a reasonable
   alternate read exists if print-recovery behaviour is believed to differ by mode.

## Why ETM differs from POS (and why that's correct, not an accident)

| | POS | ETM |
|---|---|---|
| Modes | **3** — NIR (rail), Ulsterbus, Metro | **2** — Metro, Ulsterbus (both bus) |
| Divergence | Heavy — rail tickets, Metro cash-only + no-validation, mode-specific products | Light — 39 of 516 cases (~7.6%) are mode-specific; ~92% shared/primary |
| Old suite | Triplicated **per mode** (NIR 513 / Metro 334 / Ulsterbus 317) | Feature-organised |
| Chosen structure | **Mode-first sections** (Functional - Shared / NIR / Ulsterbus / Metro) | **Feature/test-type-first** + Run Configurations + Refs tags |

**The department convention:** choose structure by **degree of mode divergence**.
- Many modes / heavy divergence (incl. rail) → **mode-first sections** so a tester runs `Shared + one
  mode` and the structure mirrors the divergence (POS).
- Few modes / near-identical → **feature-first + Run Configurations**, with a **Refs tag on every
  case** giving the same shared/mode-only visibility without duplicating the section tree (ETM).

Forcing ETM into POS-style mode-first sections would create two near-empty mode trees and split the
shared ~92% for almost no benefit. Forcing POS into feature-first would bury its heavy rail/Metro
divergence. Same execution mechanism (Run Configurations) either way — only the organisation differs,
matched to the device.

## Keeping this accurate

- **Regenerate the tally and tables above whenever cases are added/removed** in Smartcards/ABT/
  Capping/Ticket Issue/Promo Menu/HMI Fare Look-Up (the areas where mode-specificity actually lives).
- **New cases must be tagged at authoring time** — add the `MODE-*` Refs tag in the same push that
  creates the case, using this doc's logic (fare/product/config-driven and shared → `BOTH`; provably
  Metro-only or Ulsterbus-only by product/zone/stage/service → the mode-only tag; pure
  mechanics/hardware/UI → `PRIMARY-ONLY`).
- If a new mode-specific behaviour is added, name it here and update the relevant table.
- The classification script and full per-case log used for the 2026-07-27 re-derivation:
  `proposals/coherence-audit/fixes/etm-mode-tagging.changelog.md`.
