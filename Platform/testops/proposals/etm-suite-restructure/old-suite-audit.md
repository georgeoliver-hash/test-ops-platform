# ETM suite — old-suite audit (evidence base)

**Audit-first.** Before authoring any ETM case we record the actual shape of the source suite. This
is the structural recon done 2026-06-04; the product×mode cross-tab and annotation coverage come
once the requirements + Overflow flow-data JSON are in.

## Suites
- **Source (old, read-only):** `AA-ETM-Acceptance Test` — **id 4943**. Never modified or deleted.
- **Target (new):** `**NEW** ETM-Acceptance Suite` — **id 30254**. Everything is built here.
- Other ETM suites in project 42 (possible cross-reference, NOT the source): `2.1-ETM-Acceptance
  Test - V01` (14322), `R:2 - MAN -FNC - ETM` (9164), `**WIP - R:2 - MAN -SMK - ETM` (10149),
  `Translink ETM EMBEDDED QA Smoke` (19505), `R1.1-AUT-SMK-ETM Way 6S 3947` (10045),
  `ETM - Manual Basic Functional Tests` (3931), `Translink ETM - Basic Functional Tests` (3932).

## Scale
- **936 cases across 146 sections.** (POS old suite was ~2193 cases; ETM is smaller but deeper on
  smartcard/ABT product matrices.)

## Top-level section breakdown (case counts)
- **Driver Operations** — the bulk. Sub-areas:
  - Sign on (19), FLU (11), Flash Passes (5), Paper Management (3), Power Interrupt (5).
  - **Driver Menu and Options** (~30): Annulments, Barcode Reference Entry, Currency change over,
    Driver Sign-Off, Driver break, Driver options (Display Settings, Driver Totals, Last Ticket
    Issued, Messages, Other devices, Paper Status, Reboot Card Reader, Report Faulty Reader, Soft
    Reboot, Word & Colour), Inspector, Open Tickets, Start New Journey.
  - **Barcodes** (~22): Single-Use Online/Offline, Multiple Use, mLink, Legacy, Printing.
  - **Location Management**: GPS (8), Manual Stage Selection (1).
  - **Ticket Issue** (~130): Day Return, Easibus, Gateway Single, Jobseeker Single, ME Rugby Day,
    Metro Single, Month Return, iLink Single, Warrant Return, Change Receipts, Printer-interrupt
    during issue, **Promo Menu** (Bus Rambler, Family & Friends Day, Metro Day/Evening/Family Day,
    Park & Ride Day).
  - **Smartcards and ABT** (~330 — the largest matrix):
    - **ABT** tap: Visa, Mastercard, Mobile Wallet, Declined Taps, **TOO Metro** (+ Metro Tap
      Annulment), **TOO Ulsterbus** (+ Capping Groups, Ulsterbus Tap Annulment).
    - **Smartcards**: Hot Listed; Concessionary (EA Smartpass Bus/Rail Pupil & Further Education,
      Free Smartpass, Half Fare Smartpass, Staff Pass); Commercial (Daylink, Belfast Visitor Pass,
      **Multi-Journey** — Metro City/Inner/Extended Zone + **Inter-Device** variants, Ulsterbus MJ +
      Inter-Device, Metro MJ, Ulsterbus MJ; **Travelcard** — Metro, Ulsterbus Town Service; iLink
      Zones 1–4 + NW; aLink; yLink).
- **HMI / Screens** (screen-validation, ~210): 1.0 Sign On (33), 2.0 FLU (35), 3.0 Promo Menu (8),
  4.0 Numeric Entry (6), 5.0 Daylink (4), 6.0 Smartcards (14), 7.0 Printer Errors & Events (6),
  8.0 Driver Menu (35), 9.0 Supervisor Menu (13), 10.0 Technician Menu (23), 11.0 Power Management
  (3), 12.0 Barcodes (15) — plus **HMI / Ticket Layouts (40)**.
- **Supervisor Operations** (14): Sign on, Sign off, Supervisor Functions.
- **Technician Operations** (16): Sign on, Technician Functions.
- **System Management** (~30): BOS Comms (+ Commissioning & Software Distribution, Upload), GMT/BST
  Time Change, Power Saving Mode, Printer Management (Paper Management, Power Interrupt, Printer
  Firmware Update).
- **Regression Defects (41)** — the ETM bug backlog (ETM analogue of the POS `Confirmation Tests` /
  TIBU register). Fold each into the functional case that owns the behaviour; link via Refs.
- **Exploratory Tests / Timing Tests (17)**, **Glider Transfers (3)**, **Invalid Cards? (~22)**,
  **Non-Functional testing (2)**, **Delete (3)** — staging/edge buckets to triage.

## Overflow flows George listed → old-suite home (for coverage mapping)
| Overflow flow (new ETM Overflow) | Old-suite section(s) | Notes |
|---|---|---|
| Driver Sign On | Driver Operations / Sign on; HMI / 1.0 Sign On | Long flow (see device brief). |
| FLU | Driver Operations / FLU; HMI / 2.0 FLU | |
| Navigation | (cross-cutting — menu traversal) | New explicit area? confirm. |
| Basket Mode | Ticket Issue + (basket) | ETM "basket" scope to confirm vs POS. |
| Driver Menu / Options | Driver Menu and Options; HMI / 8.0 Driver Menu | |
| Supervisor | Supervisor Operations; HMI / 9.0 Supervisor Menu | |
| Technician | Technician Operations; HMI / 10.0 Technician Menu | |
| Display LEDs and Audio Tones | (not an obvious old section) | likely new coverage — confirm. |
| Barcode Scanning | Driver Operations / Barcodes; HMI / 12.0 Barcodes | |
| Power Interruption | Power Interrupt; System Mgmt / Power; HMI / 11.0 | |
| Revenue Limit | (not an obvious old section) | likely new coverage — confirm rule from annotations. |

**Gaps the Overflow list implies (to confirm):** *Navigation*, *Display LEDs & Audio Tones*, and
*Revenue Limit* don't map cleanly to a dedicated old section — candidate new coverage. The old suite
has large areas the Overflow list doesn't mention (Smartcards/ABT matrix, Ticket Issue, System
Management, Timing/Exploratory) — those stay in scope and come from the old suite + requirements.

## Mode reality (preliminary — MUST be cross-tabbed before authoring)
- ETM is a **bus device: Metro + Ulsterbus** products (no rail/NIR mode, unlike POS). Glider appears
  as a transfer case.
- Mode-specific evidence so far: Multi-Journey zoning (Metro City/Inner/Extended) vs Ulsterbus MJ /
  Town Service Travelcard; TOO Metro vs TOO Ulsterbus tap flows; ticket products. **Do the product ×
  mode cross-tab (like POS `old-suite-audit.md`) to PROVE shared-vs-Metro-vs-Ulsterbus — do not
  guess from names.**

## Push defaults (confirmed live, sample C1519256)
`template_id: 1`, `custom_devtypes: [25]`, `custom_revstatus: 2`, `custom_autoconfirmation: false`.
The "REQUIRED" qualproc/bdcreqdocs/automation_script are None on real cases → don't set. (Full note
in `knowledge/devices/etm.md`.)

## Inputs still needed from George (audit-first prerequisites)
1. **Overflow flow-data JSON** for the new ETM Overflow (`overflow.io/s/NDLGF6NF`). Share link is a
   JS shell — WebFetch can't read it. Grab it from the browser **Network tab** (same trick as POS →
   `overflow_data.json`); drop it in `knowledge/flows/`. Then 11 flows' annotations are mineable.
2. **Requirements / REQ docs** (the old suite refs `REQ-####` / `B*.*.*` requirement ids) — to judge
   stale-vs-current and ground preconditions.
3. **Confirm the mode model:** Metro + Ulsterbus only (no rail), and the shared-vs-mode product split.
4. **Confirm scope of the 3 likely-new areas:** Navigation, Display LEDs & Audio Tones, Revenue Limit.
