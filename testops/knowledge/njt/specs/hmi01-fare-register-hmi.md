# NJT_FRFRP_HMI01 — Fare Register HMI Specification (distilled)

**Source:** `NJT_FRFRP_HMI01 Fare Register HMI specification.pdf` — NJ TRANSIT Fare Register and
Farebox Replacement Project, v4, 9 Jan 2026, Author: Arrive. Text extracted to
`C:\SystemTestOps\njt-requirements\_text\NJT_FRFRP_HMI01 Fare Register HMI specification.pdf.txt`
(~3898 lines). Distilled testable facts only — full PDF (with screenshots/diagrams) held locally at
`C:\SystemTestOps\Specifications\NJT_FRFRP_HMI01 Fare Register HMI specification.pdf`.
Related: `NJT_FRFRP_FS002` (Fare Register Functional Specification — governs which transactions/rider
classes appear and how transaction results are populated; cited throughout as "per NJT_FRFRP_FS002").
Device: **Infigo 4** Fare Register (bus-mounted; NJ TRANSIT Bus System). Citations use the page
numbers printed in the document's own Table of Contents (`NJT_FRFRP_HMI01 p.N`), which line up with
the in-body page-footer markers.

**GAP — diagrams not available in text extract.** Every screen section below originally contains a
screenshot/mock-up image; the plain-text extraction strips all images, leaving only surrounding
prose/tables (Key/Function/Sound-Played tables, notes). **This applies to essentially every screen
listed in this note** — exact layout, field positions, colours, icon shapes and on-screen wording
beyond what is explicitly described in prose are UNCONFIRMED from this note alone. Open the original
PDF at the path above (via the Read tool) if a specific screen's exact visual layout matters for a
case. This single caveat is not repeated under every screen below — assume it applies everywhere
unless a screen's entry says otherwise.

## Physical interface & global conventions (§3–5, p.8–15)

- Physical UI: colour TFT 5.7" RGB primary display, 2×16-char passenger display, numeric keypad, 22
  configurable nav/function keys (L1–L6 left, R1–R6 right), audio output, LED status indicators
  (p.8, FM-2/FM-8/FM-9).
- Key conventions used across nearly all screens (p.9–10): **L1–L6** = rider classification / fare
  strip / menu options; **R1–R6** = transaction type / menu options; **Z** = set alighting zone;
  **S** = sum function (Full Service mode only); **F** = driver menu; **P/N** = previous/next page;
  **⋀/⋁** = scroll boarding zone or list; **ISSUE** = finalise/confirm; **A+<key>** = shift for a
  2nd option on that key (e.g. `A+L6` = Foreign rider class).
- Sounds (p.12): `click.wav` (key press / success key selection), `success.wav` (successful
  transaction), `error.wav` (unsuccessful transaction/key), `producttimeout.wav` (menu timeout /
  auto log-off), `warning.wav` (warning screen shown), `ok.wav` (other confirmations).
- **Status Bar** (top of driver display, present on in-service screens) — 3 sections (p.13–15):
  Time/Day/Date (12hr clock, DD/MM/YY); Status Information (Line ID + zone when in-service, blank
  when not in-service, brief success/error message on transaction); Status Indicators — IVN
  connected/disconnected, OBV connected-in-service/connected-not-in-service/unexpectedly-unavailable
  (fault or disconnected)/maintenance-mode, Farebox OK/fault-or-exact-mode-no-comms/full-service-no-farebox-detected,
  Mode (Exact vs Full Service), Colour-of-the-Day (coloured block + 3-letter abbreviation).
- **GAP** — exact icon glyphs for each status-indicator state are images, not described in text
  (p.14–15); confirm visually if a case needs to assert the icon itself rather than just the
  underlying state.

## 1. Signed Off states (§6, p.16–19)

| Screen | Purpose / entry trigger | Exit / timeout | Elements (as described) | Cite |
|---|---|---|---|---|
| **Low Power Mode** | Entered after a configurable idle period on Screen Saver | Any key → Idle screen (click.wav) | — | p.16 |
| **Screen Saver** | Entered after a configurable idle period on Idle screen with no activity | 10 min inactivity → Low Power; any key → Idle (click.wav) | "PRESS ANY KEY" text, which moves around the screen | p.17 |
| **Idle** | Default state, device signed off | 60s inactivity → Screen Saver; `ISSUE` → Operator Entry screen; all other keys no-op | — | p.18 |
| **Idle — Non Operational** | Device is Out of Service, Locked, blocked, or has a fault | Same timeouts as Idle; `ISSUE` → Operator Entry | Error message overlay on idle screen, reflecting the specific error condition. Four defined error texts (p.19–20): **Communications Lock** → "Communications Locked / Your device has been automatically locked as it has been unable to communicate with the server / Please notify a Supervisor"; **Remote lock or block** → "Out of Service / This device has been remotely put out of service / Please notify a Supervisor"; **Memory Full** → "Out of Service / Memory full, please upload memory to the server / Please notify a Supervisor"; **Other** → "Out of Service / This device has a fault / Please notify a Supervisor" | p.19–20 |

Note: on Fare-Register-Out-of-Service, "Special" users can still sign on (p.20, noted under 7.1).

## 2. Sign-On Process (§7, p.20–32)

| Screen | Purpose / entry trigger | Exit / next screen | Elements | Cite |
|---|---|---|---|---|
| **Operator Entry** | `ISSUE` pressed from Idle | Valid Operator ID in staff list → PIN Entry; invalid → error tone (error.wav), stays on screen; 60s inactivity → Idle | Operator ID entry box; `0-9` data entry, `C` clears box | p.20 |
| **Operator PIN Entry** | Valid Operator ID confirmed | Valid PIN + role **Driver** → Enter Run screen; role **Supervisor** → Supervisor Menu; role **Administrator** → Administrator Menu; invalid PIN → error shown, stays; 60s inactivity → Idle | PIN entry box | p.21 |
| **Enter Run Screen** | Driver role confirmed at PIN entry | Run 1–4 digits + `ISSUE` → Enter Line screen; >4 digits → error; `C` on empty → Idle; 120s inactivity → Idle | Run number entry | p.23 |
| **Enter Line Screen** | Run accepted | Valid Line + `ISSUE` → Enter Trip screen; unknown Line ID → error; `C` on empty → Enter Run; `⋀/⋁` cycle Line list; 120s inactivity → Idle | Line ID entry, Line list scroll | p.24 |
| **Enter Trip Screen** | Line accepted | Trip 1–3 digits + `ISSUE` → Enter Boarding Zone screen; >3 digits → error; `C` on empty → Enter Line; 120s inactivity → Idle | Trip number entry | p.25 |
| **Enter Boarding Zone Screen** | Trip accepted | Valid zone on selected Line + `ISSUE` → Enter Alighting Zone screen; invalid zone → error; `C` on empty → Enter Trip; `⋀/⋁` cycle zones on the Line; 120s inactivity → Idle | Boarding zone entry, zone scroll | p.26 |
| **Enter Alighting Zone Screen** | Boarding zone accepted | Valid zone + `ISSUE` → Enter Class screen; invalid → error; `C` on empty → Enter Boarding Zone; `⋀/⋁` cycle zones; 120s inactivity → Idle | Alighting zone entry, zone scroll | p.28 |
| **Enter Class Screen** | Alighting zone accepted | `ISSUE` → next screen (spec text for this row is duplicated verbatim from the zone-entry row — **GAP**: the doc's ISSUE bullet under 7.8 literally repeats "If Zone ID is not on selected Line..." rather than describing a class-specific validation; likely a spec authoring error/typo, not a device behaviour — flag to engineer); `C` → Enter Alighting Zone; `⋀/⋁` cycle rider classifications; 120s inactivity → Idle | Rider classification list scroll | p.29 |
| **Enter Transaction Screen** | Class accepted | `ISSUE` → prints start-of-trip receipt, shows Default Display; `C` → Enter Class screen; `⋀/⋁` cycle available transactions; 120s inactivity → Idle | Transaction list scroll | p.31 |
| **Data Validation (error overlay)** | Any invalid value entered on the above entry screens | Cleared on correction | Field displays an "invalid" icon; error message shown in status bar. Two worked examples referenced: Run entry error and Boarding Zone entry error (images not in text extract) | p.32 |

## 3. Default Display & transaction screens (§8, p.33–58)

**Default Display** (p.33) is the driver's normal in-service screen, composed of 3 elements:
- **Fare Strip** (p.33) — `L1-L6` select Rider Classification; keys with 2 options use `A`+key for the
  2nd option (e.g. `A+L6` = Foreign, established at p.36–37).
- **Ticket Details** (p.33–34) — current ticket parameters, price, and (Exact Fare routes only) funds
  entered on the Farebox; the "Farebox:" line is **not shown** on Full Service routes.
- **Transaction List** (p.34) — `R1-R6` select transaction type, paged with `P`/`N`; only transactions
  allowed on the current Line are shown (full list of which is defined in `NJT_FRFRP_FS002`, not this
  doc — **GAP**, cross-reference that spec for the exhaustive transaction-type list per rider class).

| Screen | Purpose / trigger | Exit | Key behaviours worth citing | Cite |
|---|---|---|---|---|
| **Ticket Issue Screen — Exact Mode** | Default display when signed on to an Exact-Fare route | `ISSUE` issues product if sufficient farebox funds registered; insufficient funds → error tone, no issue; invalid product → error tone; `A+ISSUE` issues if ≥1¢ registered (vs. full fare for plain ISSUE) | Rider classes L1–L6 (+A+L6 Foreign); transactions R1 Cash, R2 Monthly Pass (+A+R2 Counterfeit Monthly Pass), R3 MyTix Monthly Pass, R4 Transfer, R5 X-Transfer, R6 MyTix X-Transfer; `Z` updates alighting zone (error tone if zone not on route); `A+1` sends "wheelchair" event to CloudFare; `A+2` sends "non payment" event; `A+3` → Bus Inspection screen; 120-min inactivity → Auto Log-off Warning | p.35–38 |
| **Ticket Issue Screen — Full Service Mode** | Default display when signed on to a Full-Service route | `ISSUE` issues product if valid; invalid → error tone (no farebox-funds check, unlike Exact mode) | Same rider-class/transaction key map as Exact mode; `S` adds a valid product to the "sum" basket (invalid → error tone); 120-min inactivity → Auto Log-off Warning | p.38–41 |
| **Ticket Issue Screen — Full Service Mode, Sum Function** | `S` pressed on a set-up product in Full Service mode | `ISSUE` issues each product in the sum basket in turn | Driver display shows count and total value of summed items (exact layout not in text — GAP); same key map as Full Service | p.41–44 |
| **Barcode Validation Screen** | A multi-use/valid barcode is presented (result populated per `NJT_FRFRP_FS002`) | `C` cancels, returns to Default Display; `ISSUE` accepts and, if more passengers travel on the same ticket, shows next passenger for validation, else returns to Default Display | Timeout: Approval type 00 = 60s auto-accept+return; type 01 = 1s auto-accept+next passenger/return | p.44–45 |
| **PayGo — Waiting for Driver/Automatic** | EMV Transaction message approval mode = 00 or 01 | `C` cancels; `ISSUE` issues product, returns to Default Display | Timeout: type 00 = 60s cancel+return; type 01 = 1s accept+return | p.45–47 |
| **PayGo — Waiting for EMV Validation Information** | EMV approval mode = 02 | `ISSUE` issues, returns to Default Display; `C` cancels | `R1` toggles One Way/CT (only if CT enabled on Line+Rider Class); `L1-L3` change Rider Class (Adult/Senior/Child); `L4` Student (only if enabled on Line); `Z`/`⋀`/`⋁` zone entry/scroll; 60s timeout → cancel+return | p.47–49 |
| **FARE-PAY Stored Value — Waiting for Driver/Automatic** | NJT Card Transaction message approval mode = 00 or 01 | `C` cancels; `ISSUE` issues, returns to Default Display | If offline, "offline" shown instead of SV balance; timeouts as PayGo equivalents | p.49–50 |
| **FARE-PAY Stored Value — Waiting for NJT Card Validation Information** | NJT Card approval mode = 03 | `ISSUE`: sufficient funds/offline → issue+return; insufficient → error shown | `R1` toggles One Way/CT/Transfer (if CT enabled, or discount type 14 with board=alight zone); `L1-L4` rider class (Student only if allowed on Line); zone entry/scroll; "offline" shown if offline; 60s timeout → accept+return | p.50–52 |
| **FARE-PAY Tickets — Waiting for Driver/Automatic** | NJT Card Transaction approval mode = 00 or 01 | `C` cancels; `ISSUE` issues, returns to Default Display | "offline" shown if offline | p.52–53 |
| **FARE-PAY Tickets — Waiting for Zones** | NJT Card approval mode = 02 | `ISSUE`: sufficient funds/offline → issue; insufficient → error | Zone entry/scroll, `Z` key; "offline" shown if offline; 60s timeout → accept+return | p.53–55 |
| **FARE-PAY Tickets — Waiting for Rider Classification and Zones** | NJT Card approval mode = 03 | `ISSUE` issues, returns to Default Display | `L1-L4` rider class (Student only if allowed on Line); zone entry/scroll; "offline" shown if offline; 60s timeout → accept+return | p.55–57 |
| **Transaction Rejected** | A transaction fails validation (reason populated per `NJT_FRFRP_FS002`) | `C` cancels, returns to Default Display | Timeout: type 00 = 60s auto-cancel+return; type 01 = 1s auto-cancel+return | p.57–58 |
| **Bus Inspection** | `A+3` pressed from Ticket Issue screen (Exact or Full Service) | `ISSUE`: 1–6 digit ID → accept, return to Default Display; >6 digits → error; `C` → return to Default Display | 60s inactivity → Default Display | p.58–59 |

## 4. Driver Menu (§9, p.59–80)

| Screen | Purpose / trigger | Exit | Elements | Cite |
|---|---|---|---|---|
| **Driver Menu Page 1** | `F` pressed on Default Display | `C`/`F` → Default Display; `⋁` → Driver Menu Page 2; 60s timeout → Default Display | `L1` End of Trip, `L2` Relief, `L3` Driver Break, `L4` Device Settings, `L5` Paper Status, `L6` Accept Next Bill, `R1` Cancel Ticket (Full Service + eligible ticket only; error if none eligible; no-op in Exact mode), `R2` Full Service = no-op / Exact mode = send Hold to Farebox+return, `R3` Pay Leave, `R4` Driver Totals, `R5` Full Service = no-op / Exact mode = "bill unjam" to Farebox+return, `R6` Full Service = no-op / Exact mode = dump command to Farebox+return | p.59–61 |
| **Driver Menu Page 2** | `⋁` from Page 1 | `⋀` → Page 1; `C`/`F` → Default Display; 60s timeout → Default Display | `L1` Supervisor/Audit reports page | p.61–62 |
| **Confirm End of Trip** | `L1` from Driver Menu | `C` → Default Display; `ISSUE` confirms End of Trip, prints end-of-trip receipt, shows Trip Details screen; 60s timeout → Default Display | — | p.62–63 |
| **Trip Details Screen** | End of Trip confirmed | `F` → Confirm End of Run screen; `ISSUE` on valid data moves to next field / shows Default Display on last field; invalid → error; `C` clears entry or returns to previous prompt (up to Line) if empty; `⋀/⋁` cycle variable list; 120-min timeout → Auto Log-off Warning | Waits for next-trip response from IVN or 1s timeout before showing screen; IVN-suggested details are pre-filled; sign-on flow mirrors initial sign-on minus ability to cancel back to Run number | p.63–65 |
| **Confirm End of Run** | `F` from Trip Details | `C` → Trip Details; `ISSUE` ends the run, prints waybill, returns to Idle screen; 120-min timeout → Auto Log-off Warning | — | p.65–66 |
| **Confirm Relief** | `L2` from Driver Menu | `C` → Driver Menu; `ISSUE` ends run, prints relief receipt, returns to Idle screen; 60s timeout → Driver Menu | — | p.66–67 |
| **Confirm Driver Break** | `L3` from Driver Menu | `C` → Driver Menu; `ISSUE` → Driver Break screen; 60s timeout → Driver Menu | — | p.67–68 |
| **Driver Break** | Confirm Driver Break → `ISSUE` | `R6` → Force Sign off screen; `ISSUE` → Return from Break screen; 120-min timeout signs off driver, shows Idle | — | p.68–69 |
| **Return from Break** | `ISSUE` from Driver Break | `C` → Driver Break; `ISSUE`: correct PIN → Default Display; incorrect PIN → error shown; 60s timeout → Driver Break | PIN entry | p.69–70 |
| **Force Sign off** | `R6` from Driver Break | `C` → Driver Break; `ISSUE` signs off current driver, returns to Idle; 60s timeout → Driver Break | — | p.70–71 |
| **Device Settings (Driver-Menu context)** | `L4` from Driver Menu Page 1 | `C` → Supervisor Menu (**GAP** — text says returns to "Supervisor Menu" even though entered from the Driver Menu; possible spec inconsistency, confirm actual behaviour); 60s timeout → Supervisor Menu | `L1/L2` increment/decrement Farebox brightness, `L4/L5` increment/decrement Farebox volume, `R1/R2` increment/decrement Fare Register brightness, `R4/R5` increment/decrement Fare Register volume, `R6` reset Fare Register to defaults | p.71–73 |
| **Paper Status** | `L5` from Driver Menu | `C` → Driver Menu; 60s timeout → Driver Menu | — (no described content beyond the menu table — GAP on what status text/icon is shown) | p.72 |
| **Accept Next Bill** | `L6` from Driver Menu | `C` → Driver Menu; `R1..R5` send Accept Bill command for $1/$2/$5/$10/$20 respectively and return to Default Display; 60s timeout → Driver Menu | — | p.73–75 |
| **Cancel Ticket** | `R1` from Driver Menu (Full Service, eligible ticket) | `C` → Driver Menu; `ISSUE` cancels ticket, returns to Default Display; 60s timeout → Driver Menu | — | p.75–76 |
| **Pay Leave** | `R3` from Driver Menu | `C` → Driver Menu; `ISSUE` issues ticket, returns to Default Display; 60s timeout → Driver Menu | — | p.76–77 |
| **Driver Totals** | `R4` from Driver Menu | `C` → Driver Menu; 60s timeout → Driver Menu | — (display-only; content not described — GAP) | p.77–78 |
| **Supervisor/Audit Menu** | `L1` from Driver Menu Page 2 | `L1` → Supervisor Report; `R1` → Audit Report; `C` → Driver Menu; 60s timeout → Driver Menu | — | p.78–79 |
| **Supervisor Report** | `L1` from Supervisor/Audit Menu | `ISSUE`: valid number → prints Supervisor report, returns to Default Display; invalid → error; `C` → Driver Menu; 60s timeout → Driver Menu | Numeric entry | p.79–80 |
| **Audit Report** | `R1` from Supervisor/Audit Menu | `ISSUE`: valid number → prints Audit report, returns to Default Display; invalid → error; `C` → Driver Menu; 60s timeout → Driver Menu | Numeric entry | p.80–81 |

## 5. Error and Warning Screens (§10, p.81–83)

| Screen | Purpose / trigger | Exit | Elements | Cite |
|---|---|---|---|---|
| **Full-screen Error/Warning (example: paper jam)** | An error preventing operation, or a warning about an event that may lead to inability to operate | Errors persist until condition resolved; warnings clearable via `C` | Worked example given is a "paper jam" screen (image not in text extract — GAP on exact wording); doc notes "Other errors are shown in the status bar" (i.e., not all errors are full-screen) | p.81–82 |
| **Auto Log off Warning** | 120 minutes of inactivity on an in-service screen (Ticket Issue / Trip Details, per their inactivity-timeout rows) | Any key → Default Display (click.wav); 10s timeout → signs off driver, returns to Idle | `warning.wav` played on screen entry | p.82–83 |

## 6. Supervisor Mode (§11, p.83–91)

| Screen | Purpose / trigger | Exit | Elements | Cite |
|---|---|---|---|---|
| **Supervisor Menu** | Valid PIN + Supervisor role at PIN Entry | `C` → Idle screen; 5-min timeout → Idle | `L1` System Status, `L2` Force Communications, `L3` Historic Trip Reports, `R1` Software Versions, `R2` Serial Numbers, `R3` Device Settings, `R4` sends OBV maintenance-mode request (success.wav) | p.83–85 |
| **System Status** | `L1` from Supervisor Menu | `R6` prints System Status report; `C` → Supervisor Menu; 60s timeout → Supervisor Menu | Colour-coded status: green = OK, yellow = Warning, red = Fault/Not Connected. Cross-references `NJT_FRFRP_FS002` §7.1.6 for the underlying status definitions — **GAP**, not detailed further in this doc | p.84–85 |
| **Software Versions (Supervisor)** | `R1` from Supervisor Menu | `ISSUE` prints report; `C` → Supervisor Menu; `⋀/⋁` page through s/w versions; 60s timeout → Supervisor Menu | — | p.85–86 |
| **Force Communications** | `L2` from Supervisor Menu | `L6` → Supervisor Menu; `R5` refreshes comms info; `R6` forces communications; `C` → Supervisor Menu; 60s timeout → Supervisor Menu | — | p.86–87 |
| **Serial Numbers** | `R2` from Supervisor Menu | `C` → Supervisor Menu; 60s timeout → Supervisor Menu | Display-only; content not described — GAP | p.87–88 |
| **Shift List** | `L3` from Supervisor Menu (Historic Trip Reports) | `L1-L6` → Shift Details for selected shift; `C` → Supervisor Menu; `⋀/⋁` page through shifts; 60s timeout → Supervisor Menu | — | p.88–89 |
| **Shift Details** | Shift selected from Shift List | `ISSUE` prints shift details; `C` → Supervisor Menu; `⋀/⋁` previous/next shift's details; 60s timeout → Supervisor Menu | — | p.89–90 |
| **Device Settings (Supervisor context)** | `R3` from Supervisor Menu | `C` → Supervisor Menu; 60s timeout → Supervisor Menu | Same brightness/volume increment-decrement key map as the Driver-Menu Device Settings screen (`L1/L2` Farebox brightness, `L4/L5` Farebox volume, `R1/R2`/`R4/R5` Fare Register brightness/volume, `R6` reset to defaults) — **GAP**: confirm with engineer whether this is literally the same screen/case as §9.6 or a distinct one requiring its own test case | p.90–91 |

## 7. Administrator Mode (§12, p.92–93)

| Screen | Purpose / trigger | Exit | Elements | Cite |
|---|---|---|---|---|
| **Administrator Menu** | Valid PIN + Administrator role at PIN Entry | `C` → Idle screen; 5-min timeout → Idle | `R1` sends Unlock Farebox message (success.wav); `R2` → Program Farebox Number screen | p.92–93 |
| **Program Farebox Number** | `R2` from Administrator Menu | `ISSUE`: 1–6 digit valid number → sends Program Farebox Number command to Farebox (success.wav); invalid → error; `C` → Administrator Menu (**GAP** — text literally says "Returns to Supervisor Menu" though entered from Administrator Menu; likely spec typo, confirm with engineer); 60s timeout → Administrator Menu | Numeric entry | p.93–94 |

## 8. Ticket / Receipt Formats (§13, p.94–110) — printed outputs, not HMI screens

Listed separately since the suite may hold print-format cases distinct from live-screen cases; not
"screens" in the HMI sense but each is a distinct, named, citable device output:

1. **Fare Receipt** — cash/fare-media transactions; no fare printed if fare media used; special/override/override-transfer fares are driver-entered (p.94).
2. **Transfer Issue** — 2-part ticket (purchase receipt + transfer fare media); No-Charge Transfers print as "Ticket Rx" with no fare (p.94–96).
3. **Round Trip Issue** — 2-part; part 2 shows zones reversed (alight→board) for the return trip; Ticket Rx & 10-trip Rx issues print no fare (p.96–97).
4. **Continue Trip Issue** — 2-part; part 2 shows continue-trip expiry time/date; Ticket Rx & 10-Trip Rx issues print no fare (p.97–98).
5. **Cancel Receipts** — "TICKET NOT VALID FOR ANY TRAVEL" banner top+bottom; echoes the cancelled ticket's number/class/type/fare/line/zone (p.98–99).
6. **Test Ticket** — printed after paper reload; character test string + checkerboard print-head test pattern; "TICKET NOT VALID" footer (p.99–100).
7. **Start of Run** — run/driver/bus number, line, trip, mode (Exact/Full Service), Farebox state (ok/error/NC), issue time/date (p.100–101).
8. **End of Trip Report** — per-trip counts+values by rider class (Adult/Child/Senior/Student/Employee/Family/Foreign) + Dump, subtotal, MyTix sub-breakdown, grand total (p.101–103).
9. **End of Run Report** — same structure as End of Trip Report, at run level (p.102–104).
10. **Relief Report** — combines both Trip- and Run-level breakdowns from #8/#9 on one receipt (p.103–105).
11. **Supervisor and Audit Report** — shared template; header reads "Audit Report" or "Supervisor Report" depending which was selected; "NOT VALID AS A TICKET" banner; same trip-level breakdown as #8 (p.105–106).
12. **Historic Trip Report** — driver number, start/end date+time, run number, seq number, gross/net/void ticket counts and cash (p.106–107).
13. **Bus Inspection Receipt** — badge/driver/bus/run/line/board-zone/time/date; "Ticket Not Valid" banner (p.107–108).
14. **Software Versions (printout)** — bus/tray/FR number/garage ID, print time, OS version, config version, application version, topology/printer-files/product/params versions, staff-list version; "Ticket Not Valid" banner (p.108–109).
15. **System Status Printout** — Printer (OK/Error + tickets-left count), GPS (OK/Error), OBV (OK/Error/NC), Farebox (OK/Error/NC), IVN (OK/NC), Spotter (OK/NC); "Ticket Not Valid" banner (p.109–110).

## Cross-cutting notes / gaps to route to the engineer

- **GAP** — Enter Class Screen (§7.8, p.29): the `ISSUE` row's validation bullets are verbatim
  duplicates of the Enter Alighting Zone Screen's bullets ("If Zone ID is not on selected Line...").
  This reads like a copy-paste error in the spec rather than real class-screen validation logic —
  log to the gap register per this repo's Q&A-loop rule; flag as **POSSIBLE SPEC BUG** if the
  engineer can't clarify intended class-validation behaviour.
- **GAP** — Device Settings and Program Farebox Number screens both describe a `C`/cancel target
  that doesn't match their own stated entry point (Device Settings from Driver Menu says it returns
  to "Supervisor Menu"; Program Farebox Number from Administrator Menu also says "Supervisor Menu").
  Confirm actual return targets before writing pass/fail assertions on those transitions.
- **GAP** — several screens (Paper Status, Serial Numbers, Driver Totals) have no described on-screen
  content beyond the entry in the Key/Function table — the doc gives navigation but not payload.
  Confirm displayed fields visually or via `NJT_FRFRP_FS002` before writing content-assertion steps;
  navigation-only assertions are safe to write now.
- **GAP** — exact list of rider classifications and transaction types **allowed per Line** is deferred
  to `NJT_FRFRP_FS002` (not in this document) — needed to know which L/R key combinations are
  testable on a given Line.
- Device Settings appears twice under different entry paths (§9.6 Driver Menu, §11.1.6 Supervisor
  Menu) with an identical key map — confirm with engineer whether TestRail should hold one shared
  case (referencing both entry points) or two, to avoid duplicate coverage.

## Suite implications

The existing TestRail "Fare Register HMI" section holds 388 cases, apparently ~one per screen/HMI
state. Checklist below is every distinct named screen/state this spec defines — use it to find
missing, duplicated, or misattributed cases in that section (388 cases vs. 59 distinct screens below
means most screens likely have several cases each — per rider-class/transaction-key/error-path
variant — which is expected; the check is *coverage of every named screen*, not a 1:1 case count).

**Signed Off (4)**
- [ ] Low Power Mode (p.16)
- [ ] Screen Saver (p.17)
- [ ] Idle (p.18)
- [ ] Idle — Non Operational (4 error variants: Communications Lock / Remote lock-or-block / Memory Full / Other fault) (p.19)

**Sign-On Process (10)**
- [ ] Operator Entry (p.20)
- [ ] Operator PIN Entry (p.21)
- [ ] Enter Run Screen (p.23)
- [ ] Enter Line Screen (p.24)
- [ ] Enter Trip Screen (p.25)
- [ ] Enter Boarding Zone Screen (p.26)
- [ ] Enter Alighting Zone Screen (p.28)
- [ ] Enter Class Screen (p.29)
- [ ] Enter Transaction Screen (p.31)
- [ ] Data Validation error overlay (p.32)

**Default Display / transaction screens (12)**
- [ ] Ticket Issue Screen — Exact Mode (p.35)
- [ ] Ticket Issue Screen — Full Service Mode (p.38)
- [ ] Ticket Issue Screen — Full Service Mode, Sum Function (p.41)
- [ ] Barcode Validation Screen (p.44)
- [ ] PayGo — Waiting for Driver/Automatic (p.45)
- [ ] PayGo — Waiting for EMV Validation Information (p.47)
- [ ] FARE-PAY Stored Value — Waiting for Driver/Automatic (p.49)
- [ ] FARE-PAY Stored Value — Waiting for NJT Card Validation Information (p.50)
- [ ] FARE-PAY Tickets — Waiting for Driver/Automatic (p.52)
- [ ] FARE-PAY Tickets — Waiting for Zones (p.53)
- [ ] FARE-PAY Tickets — Waiting for Rider Classification and Zones (p.55)
- [ ] Transaction Rejected (p.57)
- [ ] Bus Inspection (p.58)

**Driver Menu (18)**
- [ ] Driver Menu Page 1 (p.59)
- [ ] Driver Menu Page 2 (p.61)
- [ ] Confirm End of Trip (p.62)
- [ ] Trip Details Screen (p.63)
- [ ] Confirm End of Run (p.65)
- [ ] Confirm Relief (p.66)
- [ ] Confirm Driver Break (p.67)
- [ ] Driver Break (p.68)
- [ ] Return from Break (p.69)
- [ ] Force Sign off (p.70)
- [ ] Device Settings — Driver Menu context (p.71)
- [ ] Paper Status (p.72)
- [ ] Accept Next Bill (p.73)
- [ ] Cancel Ticket (p.75)
- [ ] Pay Leave (p.76)
- [ ] Driver Totals (p.77)
- [ ] Supervisor/Audit Menu (p.78)
- [ ] Supervisor Report (from Driver Menu) (p.79)
- [ ] Audit Report (from Driver Menu) (p.80)

**Error/Warning (2)**
- [ ] Full-screen Error/Warning (e.g. paper jam) (p.81)
- [ ] Auto Log off Warning (p.82)

**Supervisor Mode (8)**
- [ ] Supervisor Menu (p.83)
- [ ] System Status (p.84)
- [ ] Software Versions — Supervisor context (p.85)
- [ ] Force Communications (p.86)
- [ ] Serial Numbers (p.87)
- [ ] Shift List (p.88)
- [ ] Shift Details (p.89)
- [ ] Device Settings — Supervisor context (p.90)

**Administrator Mode (2)**
- [ ] Administrator Menu (p.92)
- [ ] Program Farebox Number (p.93)

**Ticket/Receipt formats (15) — check whether the suite treats these as HMI cases at all**
- [ ] Fare Receipt (p.94)
- [ ] Transfer Issue (p.94)
- [ ] Round Trip Issue (p.96)
- [ ] Continue Trip Issue (p.97)
- [ ] Cancel Receipts (p.98)
- [ ] Test Ticket (p.99)
- [ ] Start of Run (p.100)
- [ ] End of Trip Report (p.101)
- [ ] End of Run Report (p.102)
- [ ] Relief Report (p.103)
- [ ] Supervisor and Audit Report (p.105)
- [ ] Historic Trip Report (p.106)
- [ ] Bus Inspection Receipt (p.107)
- [ ] Software Versions printout (p.108)
- [ ] System Status Printout (p.109)

**Total: 56 live HMI screens/states + 15 printed ticket/receipt formats = 71 distinct named
items to reconcile against the 388-case section.** Also assert, per the cross-cutting gaps above:
the Enter Class Screen validation-logic mismatch, the two ambiguous "return to Supervisor Menu" exits,
and whether the two Device Settings screens (Driver-Menu vs Supervisor-Menu entry) are one case or two
in the suite.
