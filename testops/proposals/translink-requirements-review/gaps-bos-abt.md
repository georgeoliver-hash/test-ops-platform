# Translink BOS & ABT — Coverage Gap Report (suite 30279 vs distilled specs)

**Scope:** the live BOS & ABT suite (`new-bos-abt-suite`, snapshot 2026-07-15, 480 cases incl. 99 ZZ
"Delete" cases; **381 non-ZZ** analysed) cross-examined against the distilled FBD specs in
`knowledge/translink/specs/`. Read-only analysis — no TestRail or suite files modified.

**Method:** case objectives/preconditions were extracted compactly (BDD `GIVEN` bodies + section path)
via the venv Python dump. The 381 live cases carry a **single one-line `custom_steps` objective/GIVEN
only** — there is no expanded When/Then body (unlike the retiring ZZ cases, which do carry rich fare
tables, e.g. old case at cases.json L5444). Coverage is therefore judged at **title + precondition
granularity**; assertion-level verification (numeric decline codes, audit field units, cap arithmetic)
**cannot be confirmed from the JSON**. "Stale/Wrong" findings are limited to what the title/objective
defensibly supports; deeper items are flagged **verify**.

**Suite shape (orientation):** 206 ABT, 110 CloudFare, 50 Merit, 13 Smartrack, 2 Merit Web Reporter.
The ABT block is deep on **annulment/re-tap, duplicate detection, tap-correction (Metro/Ref/Town/Zonal),
Operator & Passenger portal, reports, debt recovery, late taps**. It is almost entirely **TOO/Metro/
Ulsterbus-shaped**: there is **no NIR TOTO tap-matching content at all**.

---

## Summary

The suite is strong on the **Metro/Ulsterbus Tap-On-Only + capping-correction + portal/reports** surface
(annulment re-tap, duplicate detection, iLink zonal caps, reference-fare caps, town-service caps,
tap-correction re-evaluation, journey/transaction history, ~35 operator reports, debt recovery,
card verification, config-export reports, asset reports). Against the distilled requirements there are
**seven high-value holes** and one systemic grounding weakness:

1. **NIR TOTO (FBD-100690) is entirely absent** — no tap-on/tap-off matching (Steps 1–4), no MJT/PJT,
   no **max-fare-on-missing-tap**, no **3-Day cap** window, no Same-Location-Time suppression, no
   free bus↔rail transfer (Sc.1–6), no PJT-adjustment report, no rail missing-tap correction. The
   whole rail half of the ABT programme is uncovered.
2. **ABT audit-schema conformance (FBD-100658) is unasserted** — no per-device case asserting
   `paymentType=ABT` / `revenue=0` / `CardType=emv`, the **`Fare` pounds vs `fareCost` pence** split,
   product ids **7000 (TOO) / 6000 (TOTO) / 5001 (inspection)**, the **`TotoTap` vs `JourneyTap`**
   structure (renamed v1.03), or the **`DeclinedReason` enum incl. 15=BIN / 20=Passback**.
3. **Capping timing constants (FBD-100307/100389) not tested** — no case for **"capping activates next
   business day"** (earliest effect = next business day, never same day), no **04:00→03:59 operating-day
   boundary-crossing** cap test, no **max-fare-excluded-from-capping** rule, no deny-list propagation
   timing (**~30 min**, delta 15 min, 100k/200k cap, 2,500-BIN cap).
4. **CloudFare & ETM Shift Board (FBD-100831) is entirely absent** — no Schedule Management / Shift
   Board import (headerless CSV validation), no **Sun→Sat CSV vs Mon→Sun DB bitmask flip**, no
   4am Valid-From / 7-day purge, no ETM Journey List four-way filter or Manual-Override paths. Newest
   spec (2026), zero coverage.
5. **User-claims first-login gate + operator-hierarchy scoping (FBD-100342/100383) not tested** — no
   **first-login = no claims = no access** gate, and no **operator-tree visibility** case (an operator
   sees own+descendants but not parent/sibling; `CF-Operator-<X>` = no sub-operators vs nested ABT AD
   groups that inherit — the key asymmetry).
6. **DWH freshness + completeness rules (FBD-100356/100387) not tested** — no **≤10-min sync-latency**
   end-to-end, no **completed-journeys-only** DWH filter, no consistency-check-returns-0 integrity smoke,
   no query-time derived-measure recompute (Generated Revenue etc.).
7. **Glider transfer + rail-sub + pilot-list back-office paths thin/absent** — Glider 4-step transfer
   decision (FBD-100651), rail-sub synthetic-tap + PJT-ignored/MJT-applied chain (FBD-100335/100662/
   100690), and the entire **ABT Pilot List** (FBD-100720) registration/enrol/reject-no-audit flow are
   uncovered.

**Grounding weakness:** ABT functional cases are richly grounded with concrete routes/stops/fares
(72b, 10A, ref.60/61, iLink Zone 1–4, £4.00 Metro cap) — good. But the ~35 report cases and CloudFare
config cases are generic ("an operator is signed in… the Reports page is displayed"), asserting only
that a report runs, not its derived values. See final section.

Several cited FBDs are correctly **in scope here** (BOS/portal/Merit) rather than device suites; a few
(product-name usage 100260, product-group 100293, multi-journey config 100261) are largely **POS device
concerns** and are noted as out-of-scope-here where relevant.

---

## Missing

### Capping / operating-day / late-tap timing (FBD-100389, FBD-100307)
- **"Capping activates next business day"** (FBD-100307 §capping; FBD-100307 L25/L37) — **no case**.
  Earliest cap effect is the next business day, never same-day; a newly-configured cap rule and a
  first-travel-day scenario should both assert this. **High priority, explicitly flagged.**
- **04:00→03:59 operating-day boundary crossing** (FBD-100389 def.) — cap-config exists (C4102878
  "Configure the End of the Operational Day and Week") and cap-reached cases exist (C4103473–C4103479),
  but **no case crosses the 04:00 boundary** (tap at 03:59 vs 04:01 fall in different operating days /
  different cap windows). Missing boundary case.
- **Max-fare excluded from capping** (FBD-100690 §Max Fare; FBD-100335) — **no case**. A max-fare
  (missing-tap) journey must NOT count toward the daily/weekly/monthly cap. Not asserted anywhere.
- **3-Day cap window** (FBD-100690 §Capping: any 3 days within one Mon–Sun week, not spanning weeks) —
  **no case**. Suite has Daily/Weekly/Monthly config (C4102869, C4102870) but no 3-Day.

### NIR TOTO tap matching & rail (FBD-100690, FBD-100335)
- **4-step tap-matching algorithm** (Step 1 no-tap-off→max fare; Step 2 within PJT→single; Step 3
  no-intermediates→max but journey recorded; Step 4 split-into-legs) — **no case**.
- **Missing tap-off → Maximum fare** (FBD-100307 §TOTO; FBD-100690 Step 1) — **no case**.
- **Same-Location-Time duplicate suppression** for TOTO (Sc.1–3) and the **CR134 leg-splitting** change
  — **no case** (the Duplicate Detection block C4102816–C4102822 is Metro TOO tap-vs-retail, not TOTO).
- **Free bus↔rail transfers** (CR133/CR064, Sc.1–6 incl. missing-tap recalculation/refund) — **no case**.
- **Rail-substitution synthetic tap-on/off, PJT-ignored / MJT-applied** (FBD-100335; FBD-100662 §Rail Sub;
  FBD-100690 §Rail Sub) — config case exists (C4102991 "Configure an ETM rail substitute route") but the
  **back-office split + PJT-ignored** behaviour is **not asserted**.
- **Rail missing-tap correction** (FBD-100690 §Missing Tap Correction; MJT-window validation, passenger
  6 mo / operator 13 mo) — **no case**. NB the shared **1/month, 3/year** limit *is* covered on the UB
  alighting-stop side (C4103480–C4103484), but not the rail missing-tap side.
- **PJT Adjustment report** ("Adjust Journey Times", FBD-100690) — **no case**.
- **NIR device validation + GV gate behaviour** (FBD-100690 §Device checks): check order, each
  DeclinedReason (1/2/3/15/20), GV gate-opens-on-success, and the **exit-mode deny-list exception**
  (gate opens, tap audited invalid, debt retry) — **no case**.

### ABT audit-schema conformance (FBD-100658)
- **Per-device audit conformance** (ETM Metro, ETM Ulsterbus, PV Glider, HHD Glider, GV NIR, PV NIR,
  HHD NIR): constant fields (`paymentType=ABT`, `revenue=0`, `CardType=emv`, `passCount=true`,
  `ticketsIssued=false`) — **no case**.
- **`Fare` (pounds) vs `fareCost` (pence)** unit split — **no case** (spec flags this as an easy bug).
- **Product ids 7000 / 6000 / 5001** in audit — **no case**.
- **`TotoTap`/`Location` (renamed from `JourneyTap` in v1.03) vs TOO `JourneyTap` w/ Boarding/Alighting
  stage** — **no case**. (No live case references either token — so this is a hole, not a stale value.)
- **`DeclinedReason` enum mapping** (0/1/2/3/4/**15**/**20**) asserted into the BOS audit — **no case**.
  Config-side C4102954 "Add new decline reasons" exists but see Stale/Wrong below.
- **Zone arrays carry Zone Numbers (not Ids), bitwise-encoded** (cross-ref FBD-100229; e.g. Zone 2 =
  192) — **no case**.
- **TOO failure Mode 3 (reader not enabled, no passenger response)** vs Mode 2 (declined reason stored)
  (FBD-100307 failure modes) — **no case**; C4102766 covers only "declined ≠ settled-capped".

### Shift Board (FBD-100831) — entire feature
- CloudFare **Import Shift Board Data** headerless-CSV validation (bad column count / empty shift number
  / bad bitmask / bad start time / bad route ref) — **no case**.
- **CSV Sun→Sat vs schedule-DB/ETM Mon→Sun bitmask flip** — **no case** (prime regression surface).
- **Valid-From/To = 4am local** population + **7-day purge on re-import** — **no case**.
- **Ulsterbus per-depot vs Metro inherited** import hierarchy; full-board-only import — **no case**.
- ETM **Journey List four-way filter** (home location / day / duty / valid route), closest-future
  auto-highlight, and **both Manual-Override negative paths** — **no case**.
- **Activation-date deferral** (device keeps old board until activation) + TMS enable/disable flag →
  legacy sign-on — **no case**. (Merit's "Duty Comparison and Driver Shift reports" C4103111 is a
  different thing.)

### User claims & operator hierarchy (FBD-100342, FBD-100383)
- **First-login = no claims = no portal/CloudFare access** gate — **no case** (highest-value permission
  test). C4102857 "Access rights differ by user role" is role-differentiation, not the zero-claims gate.
- **Operator-hierarchy visibility scoping** — **no case** asserting an operator sees own + descendant
  data but NOT parent/sibling (e.g. `Antrim (UB)` cannot see `Bangor (UB)`; a Metro user sees Glider +
  Metro Bus + Falls…), and the **`CF-Operator-<X>` no-sub-operators vs nested-ABT-AD-group inheritance**
  asymmetry.
- **Config inheritance** (product/rule at Translink/Metro level visible at child depots; "specific to
  NIR" not visible to Ulsterbus) — **no case**.

### DWH / Merit integration (FBD-100356, FBD-100387, FBD-100300, FBD-100377)
- **Source→DWH sync-latency window** (≤ configured interval, default 10 min) end-to-end — **no case**.
- **Completed-journeys-only** DWH rule (open/tap-on-without-tap-off ABT journey absent until complete;
  `ABT Tap On Only` product filter scopes ABT rows) (FBD-100387) — **no case**.
- **Consistency-check returns 0** integrity smoke + incremental/clean-only extraction + exception rows
  as "unknown dimension keys" + purge cutoff (FBD-100356) — **no case**.
- **Query-time derived measures** (Generated Revenue, Product/Journey Count, Pass Revenue) recompute vs
  fixture (FBD-100356) — **no case**.
- **Route in/out consolidation** (FBD-100300: inbound reversed, dedup by Stage Number, +1000 offset,
  PTI Stop Reference dropped) — **no case**.
- **Service-classification data integrity** (FBD-100377: no-tag → `Unclassified`; mixed-tag service →
  only the **first-reached tag** syncs to DWH — the silent-misclassification risk) — **no case**.

### Glider TOO transfer / same-location (FBD-100651)
- **4-step Glider transfer decision** (~90-min transfer time, previous-tap-was-charged, Non-Directional
  short-circuit, same-RouteDirection rule; transfer ⇒ zero charge + **distinct MERIT transfer product**)
  — **no case**.
- **Glider PV ↔ Metro ETM same-location suppression** + **annulment reversal re-check** — **no case**.
- **PV Glider synthetic alighting** from Furthest-Alighting-Point file (`ProductSearchKey:"ABT"`), route
  audited as `"GLIDER"` — **no case** (device-level; ties to audit conformance above).
- **Revenue-inspection direction-check toggle** (on/off via ABT DB) — **no case** (report exists:
  C4102900/C4102913, logic does not).

### ABT Pilot List (FBD-100720) — entire feature
- Registration mode (enrol FEIG token), once/day EoD zip upload, pilot-list ON: enrolled → normal
  success+audit, **non-enrolled → standard reject with NO audit event** — **no case** (device config;
  the no-audit-on-reject negative is the key assertion).

### Fares-engine routing (FBD-100698)
- **RouteType 0 → AreaFare vs RouteType 1 → RoutePointToPointFares** fare-routing branch — **no case**.
- **Max Fare / Standard Fare now flow to MERIT** (product-id based, Reference=0, v0.04 change) — **no
  case**. (Capping-rule product loading *is* partly covered — C4102955.)

### Other flagged items
- **Model 1 / KFT deferred-settlement** txn sent to MERIT even if payment later fails (FBD-100307) —
  **no case**.
- **MERIT payment-method OpenPayment (TOO) vs Card (Model 1)** + "refunds/debt-recovery never reach
  MERIT" (FBD-100307) — **no case** (refund workflow itself is covered — C4102863/C4102907/C4102933).

---

## Stale-or-Wrong

The 381 live cases have shallow one-line bodies and do **not** assert numeric decline codes, audit
field names, or old fare values, so there is **no live case contradicting the new spec values** that I
can cite. The genuine stale content (rich fare tables, old regression guards) is confined to the 99
**ZZ "Delete" cases**, which are already flagged for removal and out of scope. Two items to flag:

- **C4102954 "Add new decline reasons"** (ABT / Configuration & Setup) — its GIVEN enumerates only
  *"expired, authenticity-failed, BIN-listed and Deny-listed"* cards and **omits Passback**. Given
  FBD-100658/100662 make **20=Passback** and **15=BIN** the realigned Metro+Ulsterbus values, a
  decline-reason case that omits Passback is **incomplete / likely stale** — should be extended to the
  full enum (0/1/2/3/4/15/20) and explicitly verify the **Metro alignment fix** (15=BIN, 20=Passback).
  **verify** against the full body before editing.
- **Metro "flat fare" regression risk (FBD-100662)** — spec warns Ulsterbus-route taps in the Metro
  zone must now use driver-initiated alighting selection, not the old silent Metro flat fare. No live
  non-ZZ case asserts the old flat-fare-only behaviour on UB (the flat-fare cases are Metro-proper), so
  **no stale case cited** — but confirm none of the ZZ cases being *promoted* into the suite carry it.

*(No case found asserting old decline values 15/20 differently, no `JourneyTap`-for-TOTO reference, no
pence/pounds contradiction — because the audit layer is simply untested, not miswritten.)*

---

## Partial

- **Daily capping (FBD-100389 S2)** — C4103473–C4103479 cover Metro cap reached, ref-fare cap, both-caps,
  interleaved independence, two ref-bands independent, single-tap-no-cap, single-taps-full. **Good.**
  Missing the 04:00 boundary and next-business-day activation (see Missing).
- **Late taps (FBD-100389 S3, FBD-100307)** — C4102941 (≤14d processed), C4102942 (>14d rejected),
  C4102943 (caps applied retrospectively), C4102944 (dup late taps disregarded), C4103485–C4103488
  (blocked-ETM held taps, intraday late tap capped, late-tap-after-settlement reconciled, late-tap +
  annulment). **Strong.** But the **travel-date (MERIT/ABT-journey) vs settlement-date (ABT Transaction)
  split** and the on-portal **`Late Tap` flag** are not explicitly asserted — **verify** C4103487.
- **Deny/BIN list (FBD-100307, FBD-100690)** — lifecycle covered: C4102945 (added on auth fail), C4102946
  (blocks travel), C4102947/C4102853 (removed on recovery), C4102892 (Deny List Report). **Timing/
  capacity not asserted**: full ≥once/day, **delta 15 min**, **~30-min propagation**, 100k→200k (CR106),
  2,500-BIN cap.
- **Debt recovery (FBD-100307)** — C4102850–C4102855, C4102852 (Visa MIT), C4102947 (any channel).
  Covers recoverable/unrecoverable/deny-removal well. **15-min tap-initiated re-auth timing** and the
  explicit three-trigger taxonomy (web/automated/tap) are **verify**.
- **Card verification (FBD-100307)** — C4102937 (guaranteed to Issuer Liability Threshold), C4102938
  (AVR first-use Visa), C4102939 (pre-auth first-use MC/Maestro), C4102940 (pre-auth after deny removal).
  **Strong — effectively covered.**
- **Ulsterbus TOO capping-group model (FBD-100662)** — reference-fare caps covered (C4102781–C4102783,
  C4103474, C4103477); base-product/capping-group config covered (C4102872, C4102876, C4102877, C4102955).
  The **Fixed-vs-Dynamic two-mechanism rule creation** and **"Saving Type" label** are **verify/partial**.
- **UB alighting-stop adjustment (FBD-100662 CR122)** — Update Stop List (C4102839–C4102849), Journey
  History onward-stops (C4102833–C4102838), Correction Limits **1/month·3/year** (C4103480–C4103484).
  **Strong** on the UB side; note the limit is **shared** with rail (rail side missing).
- **Town-service cap (FBD-100340)** — C4102788–C4102790 (within-town holds cap, outside higher charges,
  outside lower refunds). Covers the correction path; the **cap-eligibility matrix** (both-in-zone caps /
  board-in-alight-out / board-out-alight-in / two-different-town-zones) is only partly represented.
- **Zonal cap (FBD-100229 capping side)** — C4102768–C4102780 (iLink Zone 1/2/4, £6/£11/£19, mixed-mode)
  **strong for ABT capping**. But the **iLink smartcard validity matrix** (card zone × travel zone),
  **bitwise encoding** (Zone 2 = 192), and **Cross-Border multi-currency** dependency are **missing**
  (device-side validity). Zone CRUD covered (C4102982, C4102953).
- **Revenue Apportionment / Route Groups (FBD-100662/100651)** — report exists (C4102910), plus
  C4102911 (Revenue by Business Rule). **Taps% / Net Revenue Share arithmetic** and one-route-per-group
  rule not asserted; transfers-excluded-from-uncapped not asserted.
- **Activity Log & Shift Viewer (FBD-100358)** — C4103031–C4103035 (filter, paging, txn/event/staff
  views, barcode-ID filter, failed validations). **Partial**: no explicit **annulment display** (summary
  £0.00, expanded original fare, negative annul row), no **net-of-annulment shift/journey cash total**,
  no **Corethree single-use → Event (not MERIT)** rule, no **7-day cap / at-least-one-filter** validation,
  no **24-month Device Status purge**, no Shift Viewer per-driver case.
- **Operator Totals / StaffCash API (FBD-100276)** — C4102973 (returns staff cash for date range),
  C4102974 (invalid requests + BST/GMT). **Present.** **Net-of-annulment `CashTotal`**, alt-currency
  conversion, ended+processed-only, `ShiftId`+`DeviceSerialNumber` uniqueness are **verify**.
- **Config-export reports (FBD-100385)** — all five covered at report-existence level: Rules List
  (C4103071), Concise Area & Reference Fare (C4103072), Route List (C4103073, carries Service
  Classification col), Product to Ticket (C4103074), Product List (C4103075). **Column order / hierarchy
  scoping / CSV comma-quoting / Product-List device-type-filter** behaviour not asserted — **partial**.
- **Asset tracking reports (FBD-100263)** — Depot Location (C4103063), Devices Last Seen (C4103064),
  Software Versions (C4103065), Staff Activity (C4103066), Engineer Visits (C4103067), Revenue
  Inspector's (C4103068). **Good at report level.** Device-location convention, 31-day cap, Lost/Stolen &
  Decommissioned categories, same-day-move-both, concurrent-shift fraud flag are **verify/partial**.
- **Stop/route/service mgmt (FBD-100296)** — route CRUD (C4102986), service code/operator (C4102987),
  ABT flat fare (C4102988), transfers+time (C4102989), fares triangle (C4102990), rail-sub route
  (C4102991), map-point import (C4102979), route data import (C4102980), Station Manager (C4103088–90).
  **Strong config coverage.** ETM sign-on prefix-match + **GPS boarding-stop auto-advance**,
  delete-service-cascade, delete-stop-blocked-while-on-route are **missing/device-side**.
- **Product configuration (FBD-100268/100260/100293/100261)** — Products block C4102992–C4103006 covers
  ABT/Open/FLU/Preset/Reference/Excess/Smartcard/Barcode products, alighting stage, per-device annulments,
  passback period, keyboard buttons, FLU product group, assignment expiry. **Broad config coverage.**
  **Product-name 3-tier display fallback** (Device>Default>Product Description), **Reference Id →
  MERIT Long/Short sync**, product-group naming-convention resolution (`Default ETM Metro` etc.), and
  Multi-Journey POS issue flows are **not asserted here** (several are POS-device concerns, out of scope
  for suite 30279).
- **Revenue reallocation (FBD-100334 — STUB)** — Revenue Apportionment report (C4102910), Merit
  Concessionary reports (Revenue Foregone C4103125, Fare Foregone C4103128). Per the spec's own caveat
  (V0.01 is an unfilled template), **do not author detailed reallocation cases** (generation factor /
  journey factor / pass-revenue date-effective) until a completed spec exists — log as "needs checking".
- **Merit reporting (FBD-100347/100356/100306)** — ~35 Merit report cases (C4103100–C4103142) + Merit Web
  Reporter (C4103143/C4103144) + stored procedures (C4103138–C4103140). **Report-existence coverage is
  broad**, but the reports assert only that they run (generic GIVEN "with audit data processed"), not
  derived values (headway early/late buckets, >1-early/>5-late thresholds, Missing-Data both-way
  detection, Operational-Date basis). Merit Web **auth gate / depot restriction** not asserted.

### End-to-End skew (note)
The E2E block covers **ETM Metro TOO + retail** (C4102948/C4102949), **HHD Glider TOO + retail**
(C4102950/C4102951), **HHD Rail retail** (C4102952) — but **no PV Glider TOO**, **no GV/PV NIR TOTO**,
and **no Ulsterbus ETM TOO** end-to-end. The e2e set is Metro/Glider-HHD-shaped and omits the two
device classes (NIR validators, UB ETM) that carry the most untested audit/matching logic.

---

## Grounding note

- **ABT functional cases are well grounded** — concrete routes/stops/fares (72b Moygashel Busby Shop →
  Armagh, ref.60 £7.20 / ref.61 £8.20, 10A Casement Park → City Hall £2.30, Metro £4.00 cap, iLink Zone
  1–4 £6/£11/£19, Bangor town £2.50). These are good oracle values and match the spec worked examples
  (FBD-100662 multi-day tables, FBD-100340 town matrix, FBD-100389 S1–S3).
- **Report and CloudFare-config cases are weakly grounded** — the ~35 report cases and many CloudFare
  cases use generic actors ("an operator is signed in… the Reports page is displayed", "with audit data
  processed") and assert only that the report/screen loads, not its computed content. This is the main
  quality gap on the BOS side.
- **Assertion-level limits** — because each live case carries only a one-line objective (no When/Then),
  every "Stale/Wrong" call had to be conservative and several capping/audit/timing checks are marked
  **verify** rather than confirmed. Items depending on numeric audit codes, fare-unit split, or cap
  arithmetic could not be validated from the cases.json snapshot and need the full TestRail body (or new
  cases written to the Gherkin standard) to close out.
- **Spec provenance** — findings cite the distilled notes in `knowledge/translink/specs/`; the "next
  business day" and TOO-failure-mode constants come from **FBD-100307** (referenced by 100389/100658),
  which is a legitimate part of this cluster even though not in the original FBD list for this task.
