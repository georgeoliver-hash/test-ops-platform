# FBD-100690 — NIR Tap On Tap Off (TOTO) (distilled)

**Source:** `FBD-100690 Translink NIR Tap On Tap Off Specification v4.00` (25 Nov 2025, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100658 (ABT Audit), FBD-100662 (Ulsterbus TOO), FBD-100716 (Revenue Inspection),
FBD-100720 (ABT Pilot List), FBD-100335 (Rail Substitution), FBD-100340 (Ulsterbus Town Services).

## Scope — which devices do what (rail network)
- **GV & PV** — cEMV validators; customer taps entering/leaving the platform → initiate a TOTO validation to back office.
- **HHD** — revenue inspection on-board train (cEMV inspection taps).
- **ETM** — only bus interactions relevant to rail: **rail substitution services** and **free bus↔rail transfers**.
- **POS & TVM** — not part of TOTO validation.
- All TOTO fare/journey logic lives in the **ABT back office**; devices only tap.

## Device validation checks (PV & GV — identical order)
Pre-read (whether the reader arms at all): **Route Attribute** (ABT Type of first route at device's home location = "Tap On Tap Off"; all NIR routes carry it) → **Location** (boarding location within "Northern Ireland Zone", TMS-configurable) → **Product** (a product named per new TMS field "ABT Tap Product Name" must exist).
On card: readable? valid scheme (Visa/Mastercard, PV also Maestro)? then the checks that each still emit an audit record with a **Declined Reason**:
- **Card Expiry** fail → Declined Reason **1** (Expired)
- **ODA** fail → **3** (Declined)
- **BIN List** fail → **15** (On BIN List)
- **Deny List** fail → **2** (On Deny List)
- **Passback** (re-tap within TMS passback time) → **20** (Passback) — distinct error screen
- All pass → success screen + success beep; **GV opens the gate**.
- **GV exit/bidirectional exception:** if Deny-List check fails but GV is in a mode that lets passengers exit, the gate **still opens** to let them leave, but the screen shows the invalid tap. That tap is audited as **invalid** → cannot be matched → customer likely charged **max fare**; the invalid tap **triggers a debt retry** (may clear them off the deny list).

## Lists (PV & GV)
BIN List + full Deny List downloaded from CloudFare **≥ once/day**; Deny List **delta files every 15 min**. Full deny list max **100,000**, extended to **200,000 with CR106** (+10,000 delta buffer); ordered most-recently-added first. FEIG v2 firmware carries a non-functional PCA app, upgraded remotely to functional.

## Audit differences vs Glider PV TOO
- **Single location object** (tap location only) — no separate boarding/alighting stages (it's tap-on-*tap-off*).
- **Route** audited as the route **reference table**, not a specific NIR route; capping rules use service **"Rail"** for all rail.
- **Product** resolved from TMS "ABT Tap Product Name" → Product ID.
- **GV adds Gate Direction**: "entry" ⇒ Tap On, "exit" ⇒ Tap Off (back office uses this to classify the tap).

## Back-office rail tap matching (the core TOTO algorithm)
Per-boarding/alighting-station **Programmed Journey Time (PJT)**; global **Maximum Journey Time (MJT)**.
- **Step 1** — no tap off within MJT ⇒ **max fare** against the tap on. Else Step 2.
- **Step 2** — final tap off within PJT for first/last combo ⇒ charge **single fare**. Else Step 3.
- **Step 3** — first/last outside PJT: no intermediate taps ⇒ **max fare** but still record boarding+alighting as a complete journey. Intermediate taps ⇒ Step 4.
- **Step 4** — split into legs (tap on→first intermediate off, next on→next off, …); each leg within its PJT ⇒ single fare per leg; any leg outside PJT **or no PJT for that combo** ⇒ **max fare for that leg**.
- **Known Tap Off (e.g. gateline exit) is never treated as a Tap On** for subsequent taps. An inspection tap with no preceding tap on ⇒ following tap treated as a tap off unless it is a known tap on.

## Programmed Journey Time (PJT) config
- Imported CSV per CR135: `Boarding,Alighting,PJTMonSat,PJTSun` (times `H:MM`/`HH:MM`). **Directional** — must enter each direction separately.
- **Absent combination ⇒ journey invalid ⇒ max fare** (anti-fraud: short there-and-back with no PJT = two incomplete journeys).
- Import shows success/row-count or a specific error ("Invalid Format" / "Invalid Field" + field & row); filename shown in Journey Settings; import action tracked in the Audit report. **Separate Sunday PJT** value.

## Maximum Fare
Charged when: missing tap on, missing tap off, time between taps outside PJT, or no PJT for the combo. Value from CloudFare topology; shows as charge type **"Travel (Max Fare)"**, transacted against the **Travel Charge MID**. **Max-fare journeys do NOT count toward capping.**

## Same Location Time (duplicate-tap suppression)
Duplicate tap at the **same location** within the configured Same Location Time is **ignored** for journey/capping/charging (route & transportation type NOT considered — "Rail"/Train == "8001"/Rail Sub). Per **CR134**, when a journey is split into multiple legs within MJT the system **no longer ignores** duplicates and uses them to form legs (worked example: A 12:00, B 12:30, B 12:35, C 13:00 → two valid legs instead of a max fare). UI: icon by From/To stop + "Show More" lists duplicate location/times.
- **Scenario 1:** 2nd tap at A within Same Location Time, then B within MJT ⇒ charged A→B fare.
- **Scenario 2:** 2nd tap at A **outside** Same Location Time ⇒ **max fare** (same-station journey invalid).
- **Scenario 3:** 2nd tap at A within Same Location Time, no further tap within MJT ⇒ **max fare** (correctable via portal).

## Rail Substitution taps (from ETM)
Routes flagged Vehicle Type "Rail Sub"; ETM sends Transportation Type "Rail Sub". Back office produces **synthetic tap-on + tap-off** (boarding time == alighting time) processed as rail taps, **using the ABT TOTO product for MERIT**, **except PJT is not applied**. Fares from the **rail-sub fares triangle** (must align with reference fares so subs and normal rail get same fare/cap group). Route ABT Type only switched to enable this **once NIR TOTO is live**.

## Free bus↔rail transfers at selected stations (CR133/CR064)
Two zone types: **Bus-to-Rail** and **Rail-to-Bus**. If a bus journey and a rail journey occur within **MJT** and the alighting stop of one is in the same free-transfer zone as the boarding stop of the consecutive other ⇒ **bus leg not charged** (rail leg charged normally). **MJT measured boarding-tap to boarding-tap** of the two journeys. Journeys must be **consecutive**. MERIT: rail recorded normally; bus recorded **zero fare with a Full Fare Equivalent**.
- Sc.1–4: various valid orderings, both legs charged when zones don't line up as a transfer.
- **Sc.5 (missing rail tap on):** bus charged, rail = **max fare** (incomplete); customer adds missing tap next day → recalculated, bus no longer charged, difference refunded at end of day.
- **Sc.6 (missing rail tap off):** rail = max fare, bus charged; same-day correction → recalculated, bus no longer charged.

## Revenue Inspection (NIR-specific rules)
Inspection tap (HHD) → **Standard Fare** charged only if: no travel tap within MJT of the journey's original tap **and** (route mismatch) **and** most recent travel tap is **not a tap on**. Route check largely redundant for TOTO (only route is "Rail"). Two inspections within MJT of a non-tapped-on customer ⇒ **one** Standard Fare; two inspections >MJT apart ⇒ **two** Standard Fares.

## Capping
Cap windows: **Daily** 4am→3:59am; **Weekly** Mon 4am→next Mon 3:59am; **Monthly** 1st 4am→last day 3:59am; **3-Day** any 3 days (4am–3:59am) **within one calendar week** (Mon–Sun), consecutive or not, does not span weeks.
- **Zonal caps:** Metro Network Zone (live); iLink Zones 1/2/3/4/NW (nested — Zone2 covers 1&2, Zone3 covers 1-3, Zone4 covers 1-4&NW; Bus & Rail); Ulsterbus Town Services (one per town, Bus); Bus Sunday Rambler (NI Zone, Bus, Sundays); Coleraine Triangle (Bus, peak/off-peak); **Rail Day Tracker** (NI Zone, Rail, **Sunday only**, deployed with NIR TOTO).
- **Capping Groups** (NIR is not flat-fare): "ABT Capping Group" product maps a journey's **reference fare** to a capping group; cap value looked up per product ("NIR Daily/3-Day/Weekly/Monthly Cap"). **NIR Capping Group:** Daily/3-Day/Weekly/Monthly, Base Product, Rail, all services. Same-reference-fare journeys share a group. **CR135.1.8: Glider must be included in the cap.**

## Missing Tap Correction (portal)
Operator or passenger (anon/registered) corrects a "Missing Tap" journey. Available while Journey History shows the taps (**passenger 6 months, operator 13 months**). Correction time **must be within MJT** of the known tap: known Tap On ⇒ after original; known Tap Off ⇒ before original; unspecified Tap ⇒ either side; invalid time ⇒ warning, submit blocked. Location dropdown limited to the original tap's service, cross-border excluded. Operator sees revised fare before confirm; passenger does not. Passenger limit **1/month, 3/calendar year** (shared with UB alighting-stop corrections); operators unlimited. Corrected journeys carry passenger-vs-operator indicators; a correction cannot be subsequently amended. Charges/refunds settled end of day (or settlement amount adjusted if not yet settled).

## PJT Adjustment (operator portal)
"Adjust Journey Times" report lists journeys exceeding PJT (delays not the passenger's fault); staff select rows → adjust → refund. Status: Unprocessed/Pending/Successful/Declined; Mode always "RAIL".

## Journey / Transaction History & MERIT
- Journey History for TOTO appears only **after MJT expires** (taps matched). Shows real tap-off time; "Missing Tap" for absent boarding/alighting; intermediate taps in "Show More"; max fares get a "Penalty Fare" icon; corrected journeys get correction icons.
- Multiple TOTO/TOO journeys in a day aggregate to **one settlement transaction** (max/standard fares & refunds charged individually).
- MERIT sections: TOTO Transactions, Rail Substitutions, Maximum Fares, Standard Fares, Late Taps.

## CR dependencies to track
CR106 (deny list 200k) · CR122 (alighting-stop change) · CR133/CR064 (free transfers) · CR134 (don't ignore duplicates when splitting legs) · CR135 (PJT CSV + Sunday PJT) · Glider-in-cap change (§7.11.1.8).

## Suite implications (ABT/BOS suite 30279 + device suites)
- **This is the authoritative source for the TOTO half of the capping/Tap-On work.** Confirms the ABT max-fare-on-missing-tap and PJT logic; **extends** existing Tap-On-Only cases with the full 4-step tap-matching algorithm and **3-Day cap** window — likely missing from suite 30279.
- **Device (PV/GV):** assert the check order and each **Declined Reason code (1/2/3/15/20)** into the BOS audit; assert **GV gate opens on success** and the **exit-mode deny-list exception** (gate opens, invalid tap audited, debt retry). GV **Gate Direction** entry/exit → Tap On/Off.
- **BOS:** cover Step 1–4 matching (max fare / single fare / split legs), **absent-PJT ⇒ max fare**, **Same Location Time** Scenarios 1–3 and the CR134 leg-splitting example, **max fares excluded from capping**.
- **Transfers & rail sub:** cover free bus↔rail transfer Sc.1–6 including missing-tap recalculation/refund; rail-sub synthetic tap-on/off with **PJT ignored, MJT applied**.
- **Capping:** nested iLink zones, Rail Day Tracker (Sunday/Rail), NIR capping-group reference-fare mapping, Glider included in cap.
- **Missing Tap Correction:** MJT-window validation per known-tap type, passenger 1/month·3/year limit shared with UB, operator-unlimited, no re-amend.
- **Revenue inspection:** Standard-Fare-charged vs not, single-vs-double inspection within/outside MJT.
