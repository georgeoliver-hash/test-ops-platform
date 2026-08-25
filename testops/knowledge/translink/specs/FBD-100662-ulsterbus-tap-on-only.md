# FBD-100662 — Ulsterbus Tap On Only (TOO) (distilled)

**Source:** `FBD-100662 Translink Ulsterbus Tap On Only Specification v5.00` (27 Mar 2025, S. James)
(+ migration-plan variant). Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100658 (ABT Audit), FBD-100335 (Rail Substitution), FBD-100340 (Ulsterbus Town Services).

## Scope
- TOO relevant to **ETM only** (POS/TVM not). Customer taps card on boarding; ETM validates → audits to back office. **No inspection** for Ulsterbus TOO.
- ETM **retail mode** (buy tickets by cEMV) retained unchanged.
- Was originally intended as TOTO → no pre-set requirements; **assumed to mirror Metro ETM TOO** logic.
- **Supersedes the old Metro flat-fare rule for Ulsterbus routes:** previously an Ulsterbus tap in the Metro zone charged a Metro flat fare; now Ulsterbus routes use the driver-selected-alighting TOO business rules (Metro routes keep flat fare).

## UX flow (driver-initiated, key difference vs Metro)
1. Customer taps card. 2. ETM runs validation checks; failure → driver feedback + audit. 3. On pass a **FLU screen** shows **Adult** passenger type + valid alighting stages/fares — **locked** (no passenger-type/product/Promo changes), driver may only pick a valid alighting stage on the current route (incl. transfer stages). 4. Customer states alighting stage. 5. Driver selects it. 6. ETM audits to CloudFare, **prints a ticket** (boarding + alighting + fare, plus wording that the fare is for that journey only and may not be the day's total).
- Cancel out before selecting alighting ⇒ **no audit produced**.
- **Annul**: cancels the tap only if it's the most recent transaction, **within 1 minute**, and boarding stage unchanged.
- Some screens must **inhibit taps** so a second card can't interrupt (e.g. half-fare smartpass already tapped while driver choosing alighting).

## Validation checks (ETM)
Pre-read: **Route Attribute** = ABT Type of signed-on route must be **"Tap On Only (Driver Initiated)"** → **Location** (boarding within "Northern Ireland Zone" **and** ≥1 subsequent alighting stop on the route also in that zone) → **Product** (a fare available for the first "ABT Tap On Only" product; device checks some alighting stage returns a valid fare since alighting unknown at read time).
On card (readable? valid scheme Visa/Mastercard?), then audited-with-Declined-Reason checks:
- Card Expiry → **1** (Expired) · ODA → **3** (Declined) · BIN List → **15** (On BIN List) · Deny List → **2** (On Deny List) · Passback → **20** (Passback).
- **Alignment fix:** "On BIN List" (15) and "Passback" (20) are **not currently configured correctly for Metro** — both Metro and Ulsterbus must adopt the new values 15/20.
- All pass ⇒ FLU screen; on alighting selection ⇒ success screen + beep.
- Product note: existing "ABT Tap On Only" product is called "ABT Product"; also used for Metro flat fare — CloudFare rules switch behaviour by boarding/alighting combo.

## Lists
BIN List + full Deny List from CloudFare **≥ once/day**; **delta files every 15 min**. Already supported by retail mode — no PCA change expected.

## Auditing
Near-identical to Metro ETM TOO. **Key difference: alighting location = the driver-selected stage** (not ETM-calculated). Rail-substitution taps differ (below).

## Rail Substitution Services
Routes flagged Vehicle Type "Rail Sub" ⇒ ETM sends Transportation Type "Rail Sub". **Kept OFF (via route ABT Type) until NIR TOTO is implemented.** Back office **splits the single TOO tap into two TOTO taps** (boarding-location tap + alighting-location tap, **same tap time** ⇒ equal boarding/alighting times), then applies rail business rules **ignoring PJT**.

## Ulsterbus Town Services
**No ETM difference** — handled by ABT capping: a journey is capped when boarding **and** alighting are both within the same Ulsterbus Town Service zone. (Detail in FBD-100340.)

## Free bus↔rail transfers
Per CR064 — no ETM change; logic in NIR TOTO back office (FBD-100690).

## Back office
Behaves as Metro TOO: Journey History from device boarding/alighting stops; aggregate per caps; overnight settlement + same debt-recovery; deny-list add/remove same rules; reports same. Ulsterbus has **separate Daily/Weekly/Monthly caps** (different fares). Reports mostly can't distinguish UB vs Metro taps (services not a report field) except cap reports (e.g. Revenue By Business Rule).

## Route Groups + Revenue Apportionment (new)
- **Route Groups** (Admin Settings): named group (e.g. "Bangor (UB)", "Falls (Metro)") holding services; **a route belongs to exactly one group**. Enables revenue apportionment.
- **Revenue Apportionment report** (Operator Portal): Summary (Total Uncapped Revenue; Total Net Revenue = matches Revenue By MID) + per-route-group breakdown (Retail Transactions, Uncapped Revenue, **Taps %** = group uncapped/total uncapped ×100, **Net Revenue Share** = Total Net Revenue × Taps %, Total = Retail + Net Revenue Share). Exportable CSV/XLSX/PDF; rows/columns transposed for >~30 groups. Worked example totals: 7×£4 Bangor + 3×£2 Newtownabbey ⇒ Total Uncapped £34, Net £26; Bangor Taps% 82.35% ⇒ Net Share £21.41.

## Capping Rule creation — two mechanisms (toggle by fare type)
- **Base Amount (Fixed Fare Cap)** — existing: Name, Base Amount, Travelling-in Zones, Transport Mode, Start/End Time, Services.
- **Base Product (Dynamic/Capping-Group Cap)** — new: Name, Product (drives cap value), **Use Rule Groups** checkbox. No zones/services/times on the rule itself — topology comes from the product's rules; **transport-mode & services filters** still added.

## Capping Groups (Ulsterbus is not flat-fare)
"ABT Capping Group" product maps a journey's **reference fare** to a capping group; cap value looked up via the ABT capping-rule product ("UB Daily/Weekly/Monthly Cap"). Same-reference-fare journeys share a group. When a cap is hit, Journey History "Saving Type" shows e.g. **`Ulsterbus Daily Cap [0.35] - £12.50`**.
- Example config: reference fare → daily cap lookup {0.35:£4, 0.4:£4.5, 0.45:£5}; weekly {0.35:£12.5, 0.4:£13.5, 0.45:£15}.
- Multi-day worked example: 0.35-group daily cap £4 saves £2.20/day; weekly £12.50 and 0.45-group weekly £15.00 kick in later in the week. (Use the day-by-day tables in the spec for expected charge/aggregate/saving values — good oracle data for capping tests.)

## Alighting Stop Adjustment (CR122)
Because the driver (not the customer) picks the alighting stop, portals let passenger/operator (anon or registered) **change the alighting stop** of a TOO journey → ABT recalculates fare + affected caps → auto refund/charge. Available alighting stops = after boarding stop, same route as boarding tap. Operator sees new fare before confirm (passenger doesn't). Passenger limit **1/month, 3/calendar year** — **shared with rail TOTO missing-tap corrections**. Change indicators differ passenger vs operator; settled end of day.

## GROUNDING-CRITICAL FACTS — verbatim from v5.00 (cite before writing any annul/correction case)

**Annul is DEVICE-only (ETM driver menu) — v5.00 §5, para 204 (verbatim):**
> "Should a customer wish to cancel the tap that they have just performed then the annul functionality within the existing ETM driver menu will enable the tap to be cancelled providing it is **the most recent transaction on the ETM, within 1 minute** of the tap occurring and **the boarding stage has not changed**."
- ⇒ There is **NO "cancel a tap/journey" action in any portal.** Annul = ETM driver menu only. Cases that annul via a portal, annul an **old/settled** tap, or annul after a later tap are **WRONG** (impossible). Cancelling out of the FLU alighting screen *before* selecting (para 203) produces **no audit**.

**Alighting Stop Adjustment / CR122 — v5.00 §5.6, paras 688–694 — STATUS: PROPOSAL, UX UNDETERMINED (mark `UNCONFIRMED`, do not assert live):**
- para 691: "change request **CR122 has been raised to _propose_** to add a mechanism to change the alighting stop of TOO journeys **via the passenger and operator portals**… ABT recalculates the fare… running totals for any affected caps… a transaction will automatically refund/charge."
- para 693: "**Whilst the full UX for this solution is to be determined**…"; indicator on alighting stops in the **passenger or operator web portal** journey history; selectable stops = **after boarding, same route**; **operator portal (not passenger) shows the new fare before confirm**.
- para 692: passenger limited (**intention 1/month, 3/year**), shared with rail-TOTO missing-tap corrections.
- para 694: revised fare + cap changes shown; passenger-vs-operator change indicators; settled end of day.
- para 690: an ordinary **refund** for a query may be provided via "the normal mechanism in the ABT portal" (separate from the alighting-stop change).
- para 271: "This functionality is **still to be agreed** and will be described in greater detail in later versions."
**Settlement & refund timing (confirmed by George 2026-07-17) — no intraday overcharge:**
- Charging is **overnight-aggregated EndOfDay settlement** (para 266). During the operating day nothing is charged to the card, so **"overcharge" does not exist intraday**.
- A CR122 correction only produces a **refund / extra-charge when it changes an amount the customer was ALREADY charged** — i.e. correcting an **already-settled (prior-day) journey** (para 691). A same-day correction *before* that night's settlement just settles the correct total — **no refund**.
- Any correction refund/charge is itself "**marked for settlement at the end of the day**" (para 694).
- ⇒ Capping-correction cases must set the precondition as **already-settled prior day** if they assert a refund/charge-difference; a same-day scenario asserts only the corrected total at settlement. Fare/cap values are **back-end configurable** — the oracle is "charge matches the configured ABT pricing rule", not a fixed number (gap Q14 answered).

- ⇒ CR122 fare-recalc-in-portal is a **proposal with undetermined UX** — this is why it may not be usable on the live system. Any case depending on it must be `**UNCONFIRMED**` and cite this until George confirms it is actually implemented in the test environment.

## Migration plan (order matters for test env)
Consolidate reference fares → deploy ABT → deploy ETM (Metro+UB, pilot first) → add ABT Type route attribute → set all Metro routes "Tap On Only (Flat Fare)" → set select UB routes "Tap On Only (Driver Initiated)" → distribute topology (Metro, pilot UB, then all UB).

## CR dependencies
CR122 (alighting-stop adjustment) · CR064 (free transfers, in NIR TOTO).

## Suite implications (ABT/BOS suite 30279 + POS/ETM/PV)
- **Confirms & extends** existing ABT Tap-On-Only/capping coverage with the **capping-group (reference-fare→cap lookup)** model and the two-mechanism (Fixed vs Dynamic) capping-rule creation — likely under-covered in suite 30279. The multi-day worked tables are ready-made **oracle values** for cap-aggregation assertions.
- **ETM device cases:** driver-initiated FLU flow (locked passenger type/products), **alighting = driver-selected stage in audit**, cancel-before-select ⇒ no audit, **annul within 1 min / most-recent / same boarding**, tap inhibition on interruptible screens.
- **Declined Reasons:** assert 1/2/3/15/20 in BOS audit; specifically verify the **Metro alignment fix** for 15 (BIN) and 20 (Passback) — a likely contradiction with older Metro cases that expect the old values.
- **Metro-zone regression:** UB route in Metro zone now requires driver alighting selection (no more silent flat fare) — check no old case still asserts flat-fare-only behaviour on UB.
- **Rail sub:** back-office split of one TOO tap into two TOTO taps (equal times), PJT ignored — and that it stays **disabled until NIR TOTO live**.
- **Revenue Apportionment / Route Groups:** new report + one-route-per-group rule; assert Taps%/Net Revenue Share maths.
- **CR122 alighting adjustment:** recalculation + cap re-run + auto refund/charge; **passenger 1/month·3/year shared limit** with rail corrections.
