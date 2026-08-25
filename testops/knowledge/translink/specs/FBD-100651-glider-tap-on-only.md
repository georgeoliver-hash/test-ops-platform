# FBD-100651 — Glider Tap On Only (TOO) (distilled)

**Source:** `FBD-100651 Translink Glider Tap On Only Specification v5.00` (23 Apr 2025, S. James)
(+ `Glider Transfer Scenarios v3.00`). Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100658 (ABT Audit), FBD-100716 (Revenue Inspection), FBD-100720 (ABT Pilot List).

## Scope
- TOO relevant to **PV** (customer taps before boarding) and **HHD** (inspection). TVM not.
- Back office aggregates PV taps → end-of-day fare + caps; HHD inspection taps → Standard-Fare decision.
- Was originally intended as TOTO; **assumed to mirror Metro ETM TOO**.

## PV validation checks
Pre-read: **Route Attribute** = ABT Type of first route at the **"Glider (Metro)"** home location must be **"Tap On Only (Flat Fare)"** (all Glider routes carry it; any other value ⇒ taps rejected; future "Tap On Tap Off" triggers NIR TOTO instead) → **Location** (boarding within **"Metro Network Zone"**, all Glider stops expected inside) → **Fare** (a fare available for the first "ABT Tap On Only" product, Translink's single "ABT Product").
On card (readable? valid scheme Visa/Mastercard/Maestro?), then audited-with-Declined-Reason checks:
- Card Expiry → **1** · ODA → **3** · BIN List → **15** · Deny List → **2** · Passback → **20**.
- All pass ⇒ success screen + beep. (Flat-fare TOO — **no alighting selection on the PV**.)

## Lists
BIN + full Deny List from CloudFare **≥ once/day**; **delta every 15 min**. FEIG v2 firmware → non-functional PCA, upgraded remotely.

## PV auditing (differences vs Metro ETM TOO)
- **Alighting Stage:** no alighting selection, so audit a synthetic one — PV searches the **Furthest Alighting Point file** for an entry matching its boarding stop + direction + **`ProductSearchKey: "ABT"`**, uses `FurthestAlightingStopID` as the audited alighting location.
- **Route:** point-to-point via reference table; **audits "GLIDER" as the route** to MERIT; capping rules use service **"GLIDER"**.
- **Transfers (CR123):** two new audit fields — **`TransferRouteType` = "Directional"** and **`RouteDirection`** = configured boarding-stop direction.
- **Pilot Mode** used for live-environment testing of Glider TOO.

## ETM transfer auditing (CR123)
ETM not used on Glider, but Metro/Ulsterbus ETMs near Glider routes must audit transfer fields:
- **`TransferRouteType`**: **"None"** if boarding stop not in Metro Transfer Zone, or route "Transfer Time" attr = 0, or alighting not in Metro Network Zone. **"Directional"** if boarding in Metro Transfer Zone + alighting in Metro Network Zone + Transfer Time ≠ 0 + "Directional Transfer" attr set. **"Non-Directional"** = same but Directional Transfer attr **not** set.
- **`RouteDirection`** = direction of signed-on route.

## HHD (inspection)
Enable cEMV inspection via ABT Type of signed-on route: **"Tap On Only (Flat Fare)"** ⇒ inspection button enabled, flat-fare audit; anything else ⇒ disabled (future "Tap On Tap Off" enables NIR mode, not yet). New audit field **`RouteDirection`** = signed-on route direction. No pilot mode (use live test devices).

## Back office — Route Groups & Revenue Apportionment
- **Route Groups** carry name + services **and a per-group Maximum Journey Time + Same Location Time** ⇒ MJT/Same-Location configurable **per operator/depot** (Glider/Falls(Metro)/NIR).
- **Revenue Apportionment report** as in FBD-100662 — **transfers do NOT contribute** to Uncapped Revenue / Taps %.

## Same Location taps
Glider PV tap then Metro ETM tap at the same halt: replicate TOTO duplicate-suppression for TOO — a subsequent same-location tap within a **configurable time window** is **ignored** for journey/capping/charging; UI icon by From/To + "Show More" lists them. **Annulled TOO tap** ⇒ system re-checks and reverses any duplicates previously marked against that location.

## Glider Transfers (CR123) — decision flow
For each new tap (Metro/UB ETM or Glider PV):
1. **`TransferRouteType` ≠ "None"?** (else transfers disabled for this tap → charge normally).
2. **Previous transfer-applicable tap found?** — same media; time diff ≤ configured **transfer time (~90 min)**; previous tap **was charged** (not itself a transfer); previous `TransferRouteType` ≠ "None". (else charge normally).
3. **Either tap `TransferRouteType` = "Non-Directional"?** ⇒ mark new tap a transfer.
4. Else **same `RouteDirection`** (both Inbound or both Outbound)? ⇒ transfer.
- Transfer ⇒ **no charge**, journey marked with transfer icon; **still sent to MERIT but with a distinct transfer product** (new CloudFare product), not the standard ABT product.

## Revenue Inspection (Glider-specific)
Standard Fare charged when: no travel tap within **MJT (~90 min initially)**; travel-tap route ≠ inspection route (catches ETM-tapped-but-not-Glider-PV); **and** (toggleable) travel tap **different direction** from inspection (catches direction change without re-tap). Direction check **on/off via ABT DB setting** — if off, passing the route check alone = successful inspection. Otherwise no charge, journey history marked inspected.

## Journey Summary report (CR123 update)
Row per date × transport type ("Bus" now, "Train" future). Columns: Date, Transport Type, **Total Number of Journeys**, **Total Number of Transfers**, **Total Value (£)**. Retail excluded; Standard Fare (and future Max Fare) included; **late taps** update the counts/value for the **date the journey occurred**. Export CSV/XLSX/PDF.

## Migration plan
Metro+UB TOO already live. Order: CloudFare → ABT → ETM (pilot then estate) → PV (pilot mode off, ABT not yet enabled) → PV estate → enable pilot mode + ABT-enabled topology on pilot PVs → HHD live-test → HHD estate → disable pilot / enable ABT on all Glider PVs.

## CR dependencies
CR123 (Glider↔Metro/UB transfers, transfer audit fields, Journey Summary update).

## Suite implications (ABT/BOS suite 30279 + PV/ETM/HHD)
- **PV device cases:** ABT-Type gate ("Tap On Only (Flat Fare)" enables; other values reject), Metro Network Zone location, **synthetic alighting from Furthest Alighting Point file (`ProductSearchKey:"ABT"`)**, route audited as **"GLIDER"**, transfer fields `TransferRouteType`/`RouteDirection` in audit. Declined Reasons 1/2/3/15/20.
- **Transfer logic (BOS):** the 4-step Glider Transfer decision — assert **~90-min transfer time**, previous-tap-was-charged rule, Non-Directional short-circuit, same-direction rule; transfer ⇒ **zero charge + distinct MERIT transfer product** (not standard ABT product). This is a distinct, likely-uncovered path vs the NIR free-transfer logic — don't conflate them.
- **Same Location:** duplicate suppression for TOO across Glider PV ↔ Metro ETM, plus **annulment reversal** re-check.
- **Per-operator MJT/Same-Location via Route Groups** — assert Glider vs Metro vs NIR can differ.
- **Revenue inspection:** direction-check **toggle** on/off behaviour; route/direction/MJT gating of Standard Fare.
- **Reports:** Journey Summary transfers column + late-tap dating; Revenue Apportionment excludes transfers from uncapped revenue.
- Cross-check: Glider PV audit is **Tap-On-Only single flat-fare** vs NIR PV **Tap-On-Tap-Off** (single location, "Rail" route) — same hardware, different audit shape; ensure device suites keep these separate.
