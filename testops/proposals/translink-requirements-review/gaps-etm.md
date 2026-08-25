# ETM suite ↔ requirements cross-examination — coverage gaps

**Suite:** `**NEW** ETM-Acceptance Suite` (id 30254), cases dump `reports/tfts-system-test/new-etm-acceptance-suite/2026-07-15/cases.json` (510 cases, 445 non-`ZZ`).
**Specs:** `knowledge/translink/specs/` (distilled FBD notes). **Read-only analysis — no suite/TestRail changes made.**
Last updated: 2026-07-15.

Classification per spec rule: **COVERED** (case cited) / **PARTIAL** / **MISSING** / **STALE-or-WRONG**.
Scope note: the ETM suite owns **device-side** behaviour. Pure back-office rules (ABT tap-matching maths, MERIT
reporting, portal corrections, CSV-import validation) belong to the **ABT/BOS suite 30279** — flagged `[BOS-scope]`
where they are not an ETM-device gap, but listed because the task named the FBD.

---

## Summary

The ETM suite has **strong breadth** on the classic ETM surface — sign-on (driver/supervisor/technician), FLU/ticket
issue, basket mode, the full smartcard product catalogue (concessionary / commercial / staff / education / MJ / top-up),
menus, power/printer/comms non-functional, and a very large HMI screen-validation block. The **gaps are concentrated in
the new ABT / Tap-On / rail / integration work**, which is exactly where the current spec churn lives:

- **Whole capabilities MISSING from the ETM suite:** **Rail Substitution** (FBD-100335/100662/100690), **Shift Board
  sign-on** (FBD-100831, brand-new), **legacy-smartcard transfer decision** (FBD-100271), **RTPI/DAIP** ETM↔Vix
  integration (FBD-100202/100345), the **ETM transfer-audit fields** for Glider-adjacent routes (FBD-100651 CR123), and
  the **device heartbeat** staff-list call-in (FBD-100266).
- **Audit-schema conformance is not asserted** (FBD-100658): no ETM case pins `paymentType=ABT` / `revenue=0`, the
  **`Fare` pounds vs `fareCost` pence** split, product id **7000 (TOO)**, or **`TransportationType="Rail Sub"`**.
- **ABT declined-reason codes are a likely STALE risk** (FBD-100662 "alignment fix": 15=BIN, 20=Passback) — must be
  verified against the ABT-declined case bodies.
- **PARTIAL** where breadth exists but the spec's specific edges do not: capping (no capping-group / max-fare-excluded /
  money-oracle assertions), barcode (validation covered; exact-string errors, result-state distinction, rail £90
  fallback, CR116 expiry-display MISSING), legacy-card format/expiry-boundary edges.

**Grounding caveat (important):** the CLI dump exposes only each case's **title, section, refs and the first `Given`
line** of `custom_steps` (TestRail stored a single-line body for most cases). Detail-level classifications below
(declined codes, audit-field asserts, money oracles) are inferred from title + section + first line and **must be
confirmed against the full case bodies in TestRail** before acting.

---

## Missing

| Spec | Rule not covered | Notes |
|------|------------------|-------|
| **FBD-100335 / 100662 / 100690** | **Rail Substitution on ETM** — no case anywhere mentions rail-sub. Missing: Manual-Override sign-on to an ad-hoc "Rail Sub" route, GPS boarding-stop auto-advance with widened tolerances, no-schedule-adherence, cross-mode smartcard validation on a rail-sub bus, and the device sending **`TransportationType="Rail Sub"`** taps (back office splits one TOO tap → two TOTO, PJT ignored / MJT applied). | Emphasised. Entirely absent. `08.0.6 - New Trip - Select New Route` (4100728) is a legacy new-trip screen, not rail-sub. |
| **FBD-100831** | **Shift Board sign-on (NEW)** — no case for Duty/Shift-Number → predicted **Journey List** selection, the four-way Journey-List filter (home location / day-of-week / duty / valid route), closest-future auto-highlight, both **Manual Override** negative paths, activation-date deferral, or the TMS enable/disable flag. Existing sign-on is legacy manual route+journey entry only (screens `01.3.0 Select Duty` 4100856, `01.5.0 Journey Selection` 4100867; functional 4100510-4100513). | Emphasised, 2026 spec, likely **zero** coverage. CSV-import validation + Sun→Sat/Mon→Sun bitmask flip are `[BOS-scope]`. |
| **FBD-100271** | **Legacy-smartcard transfer decision on ETM** — no case asserts transfer-vs-journey using the **ROUTE `Transfer Time`** property (the ETM-specific source), the Metro-Transfer-Zone membership check, direction-of-travel enable, the window boundary (`LastValidated + TransferTime`), **passback-prioritised-over-transfer**, or the **WTS SmartTransfer vs WTS SmartUse** audit split. MJ cases 4100579/4100580 are *zone/boarding-stage* validation, not transfer. `02.0.4.2 FLU - Transfer Journeys` (4100764) is only a screen-validation case. | Emphasised (property-source). |
| **FBD-100651 (CR123)** | **ETM transfer-audit fields** — Metro/Ulsterbus ETMs near Glider routes must audit **`TransferRouteType`** (None / Directional / Non-Directional, derived from Metro Transfer Zone + Transfer Time + Directional-Transfer attr) and **`RouteDirection`**. No case asserts these fields. | Glider itself is PV/HHD (out of ETM scope), but the audit-field emission is an ETM duty. |
| **FBD-100690** | **Free bus↔rail transfers** originating on the ETM (bus leg zero-fared when consecutive within MJT of a rail journey in a paired transfer zone). No ETM case. | Emphasised. Charging maths `[BOS-scope]`; the ETM contributes the bus tap. |
| **FBD-100658** | **ETM ABT audit-schema conformance** — no case pins constant fields (`paymentType=ABT`, `revenue=0`, `CardType=emv`, `passCount=true`, `ticketsIssued=false`), the **`Fare` (pounds) vs `fareCost` (pence)** unit split, product id **7000** (TOO travel), or the `JourneyTap`/`BoardingStage`/`AlightingStage` structure. | Emphasised (pounds vs pence; Rail Sub type). `TotoTap` rename is TOTO-only ⇒ N/A to ETM. |
| **FBD-100266** | **Device heartbeat** — no case asserts the ETM performs the **15-min Staff-List Refresh call-in even when signed off / no sales**, updating CloudFare "Last Communication". Smoke 4100943 ("ETM communicates with the back office") is generic. | Dashboard-tile/`StaffList` reporting is `[BOS-scope]`; the periodic call-in is the ETM-side assertion. |
| **FBD-100202 / 100345** | **RTPI/DAIP (ETM↔Vix)** — no case for DAIP Log On/Off + SVID, Journey/Start/End messages, Position Update (every-4th-ack, GPS-null sentinels), stop depart/arrive events, state-gating matrix, retry semantics, NAT/session binding. | Emphasised as likely absent; needs a stubbed RTPI server. Confirm suite scope (register B6). |
| **FBD-100690 / 100389 / 100307** | **Max-fare-excluded-from-capping** — no ETM/capping case asserts a max-fare journey does not count toward a cap, nor the 4-step TOTO matching / late-tap (14-day) boundaries. | Emphasised. Primarily `[BOS-scope]` (suite 30279); no ETM-visible assertion exists either. |
| **FBD-100377** | **Service Classification** (route Service Code → Merit DWH; "first-reached tag wins" integrity risk). | `[BOS-scope]` — config/reporting, not an ETM-device case. Listed for completeness. |

---

## Stale-or-Wrong

| Spec | Contradiction to verify | Case(s) |
|------|-------------------------|---------|
| **FBD-100662 / 100651 / 100690** | **ABT Declined-Reason codes.** Spec mandates the "alignment fix" values **15 = On BIN List** and **20 = Passback** for both Metro and Ulsterbus; older Metro cases may still assert the pre-fix values. If case 4100583 (or the audit case) asserts legacy BIN/passback codes, it is **wrong**. Cannot confirm from the dump (body truncated) — **verify the full body**. | **4100583** "ABT — declined, error and EMV validation failures"; **4100591** "ABT — invalid taps recorded in back office". (Register B2.) |
| **FBD-100662** | **UB-in-Metro-zone flat fare superseded.** Ulsterbus routes now use driver-selected-alighting TOO rules; only Metro routes keep the flat fare. Any case still asserting a silent Metro flat fare on a UB route/zone would be stale. 4100586/4100587 appear to split Metro-zone vs Ulsterbus-zone correctly, but confirm 4100588 ("reverts to standard fixed fare on rule change") is not encoding the old UB flat-fare path. | **4100586**, **4100587**, **4100588** — verify. |
| **FBD-100335** | **NI-Railways smartcard products retired into ABT.** Rail business rules moved to ABT; existing rail-valid cards (iLink, concessions, yLink, 24+, staff) still honoured. Flag any ETM case asserting NIR-smartcard-*specific* on-device logic as stale. No such case seen; EA Rail SmartPass (4102550) as an honoured card is fine. | (none confirmed) |

*No hard contradiction could be proven from titles alone — all three items are "verify against full body". None are confirmed-wrong yet.*

---

## Partial

| Spec | What's covered | What's missing within the rule |
|------|----------------|--------------------------------|
| **FBD-100307** (TOO failure modes) | 4100583 (card-level rejects / EMV failures ≈ Mode 2), 4100585 (tap availability rules ≈ Mode 3 topology reject). | Explicit **three-mode distinction** — Mode 1 (card unreadable, *no response*) vs Mode 2 (declined-reason stored) vs Mode 3 (**reader not even enabled**). Timing constants (14-day, ~30-min deny propagation, 2,500-BIN) are `[BOS-scope]`. |
| **FBD-100662** (UB TOO / capping-group) | 4100587 (UB zone boarding + driver-selected alighting), 4100585 (pre-read route/location/product checks), capping 4100592-4100594. | Capping-group **reference-fare→cap lookup** model + two-mechanism (Fixed vs Dynamic) rule creation not asserted; **driver-initiated FLU locked** (no passenger-type/product/Promo change) not an explicit assertion; **cancel-before-alighting ⇒ no audit**; **ABT-tap annul (within 1 min / most-recent / same boarding)** — only HMI screen `08.0.4.2 - Annulment - ABT TOO` (4100724) exists, no functional case. |
| **FBD-100389** (capping money oracles) | 4100592 (cap reached), 4100593 (no cap), 4100594 (multi-service/mode). | Per-tap **charge-amount** + **daily-aggregate** oracles (S2), 04:00-03:59 operating-day boundary, **late-tap** path (S3, Late-Tap flag, >14-day expiry), Full-Fare-Equivalent stays uncapped. Mostly `[BOS-scope]`, but no ETM capping case pins the numbers. |
| **FBD-100167 / 100317 / 100318** (barcode) | Barcode Scanning section: 4100622 (online pass/fail), 4100624 (offline incl. **over-ceiling-limit** reject ✓), 4100625 (multiple-use), 4100626 (mLink), 4100627 (BRID reference entry), 4100628 (print + print error); + 15 HMI barcode screens (4100658-4100672). | **Exact error strings** ("This Barcode Type is not accepted on this device"); the **green / yellow-step7-only / red** result-state distinction as behaviour (screens exist, logic not asserted); **rail £90 fare-fallback** (CR105.3); **3-Day Select** date logic; **CR116** 00:00-04:00 expiry-display rollback; **passback** re-present reject + gateline Unique-ID share; **audit split** single-use=event(not MERIT) vs multi-use=transaction. |
| **FBD-100250** (Mifare pre-printed cards) | Full product-validation catalogue: concessionary 4102537-4102543, commercial 4102551-4102556, staff 4102544-4102548, education 4102549/4102550, MJ 4100579/4100580/4102557/4102558, faulty 4102568-4102570, hotlist 4100581, validation/passback 4100567-4100571/4102566; MIFARE card-type validation 4100655. | **Format/checksum rejection** (LRC / Smart-Card CRC / Customer-CRC; primary-vs-backup sector mismatch); **expiry-date boundary** edges (**1991-offset / 16-year wrap**, academic-year EA start 1 Sep/expire 30 Jun, birthday-anchored concessions, NIR Gate Pass fixed 2099); **zone-bitmap** accept/reject for iLink/aLink. |
| **FBD-100277** (Card Reference File) | 4100580 (Ulsterbus MJ boarding-stage validation) touches the alighting derivation. | The **lookup algorithm** end-to-end (furthest-down-column selection, upward-iteration fallback, **no-match ⇒ no alighting**, circular-route); **ConfigurationVersion-increment gating** (stale-config trap); `Card Reference ID Location` honoured. Operator-chosen UB-MJ reference is POS-issue `[BOS/POS-scope]`. |
| **FBD-100359** (SaaS offline/failover) | 4100647 (comms lock / interruption / restore), 4100648 (ETM keeps operating + queues when BOS lost), 4100649 (config download), 4100651 (upload audit on restore). | **KeyCloak auth** (vs ADFS) + **DNS-based server switchover no re-commission**; explicit **queue→RabbitMQ→deliver-on-restore no-data-loss** end-to-end audit assertion. ETM is cellular, so the "Ethernet devices comms-lock OOS" rule is not ETM-specific. |
| **FBD-100296** (stop/route/sign-on/GPS) | Sign-on route entry + 4100523 (correct topology & fares for the route), GPS cases 4100629/4100632. | **Prefix-match route filtering** + blank-entry full list + Route-Selection column layout as explicit asserts; **GPS auto boarding-stop advance** incl. Lookahead=0; boarding stop does not update at non-key stops. |
| **FBD-100716** (revenue inspection) | 4100607 (Inspector — report & smartcard check) = the *smartcard* inspection path. | The spec's assertable ETM rule is a **negative**: ETM does **not** perform **cEMV** inspection (HHD-only). No case pins that boundary. Bulk of spec is HHD/`[BOS-scope]`. |

**Effectively out of ETM device scope** (listed by the task but device-validation lives on other suites): **FBD-100236**
(DESFire ABT card = GV/PV/HHD rail validators, not ETM). No ETM gap.

---

## Grounding note

- **Data source fidelity:** classifications are grounded in the live suite dump (title / section_path / refs / first
  `Given` line) and the distilled FBD notes in `knowledge/translink/specs/`. The dump does **not** contain full
  Given/When/Then bodies (TestRail stored one-line `custom_steps` for most cases), so any assertion-level judgement
  (declined-reason codes, audit-field content, capping money values) is **provisional** and must be confirmed against
  the full case body in TestRail before authoring/editing. The **Stale-or-Wrong** items in particular are "verify",
  not "confirmed wrong".
- **Scope discipline:** several named FBDs (100307 timings, 100389 money, 100377, most of 100716, CSV-import in 100831,
  portal corrections in 100662/100690) are **ABT/BOS-suite (30254 vs 30279) responsibilities**, marked `[BOS-scope]`.
  They are real gaps for the *programme* but should be authored on the BOS/ABT suite, not the ETM suite — see the
  sibling `proposals/bos-abt-suite-restructure/`.
- **Cross-reference:** this ETM pass refines the master gap list in `proposals/translink-requirements-review/register.md`
  §C. Open questions that gate these gaps: **B2** (declined codes), **B3** (CR status: CR105.x/CR116/CR122/CR123/CR134),
  **B6** (RTPI/DAIP suite scope). ZZ-To-Delete section (65 cases) excluded from this analysis.
- **No writes performed** — TestRail and all suite `.cases.yaml` files untouched.
