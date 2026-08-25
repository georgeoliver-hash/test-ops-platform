# Translink POS — Coverage Gap Report (suite vs distilled specs)

**Scope:** the live POS acceptance suite (`new-pos-acceptance-suite`, snapshot 2026-07-15, 603 cases
incl. ZZ; ~590 non-ZZ) cross-examined against the POS-relevant distilled FBD specs in
`knowledge/translink/specs/`. Read-only analysis — no TestRail or suite files modified.

**Method:** case objectives/preconditions were extracted compactly (BDD `GIVEN` bodies + section
path + refs). Full step bodies were not expanded, so "Stale/Wrong" findings are limited to what the
title/objective can defensibly support; items needing the full body to confirm are flagged **verify**.

**Suite shape (orientation):** ~460 of the ~590 non-ZZ cases are `Non-Functional / Screen Validation`
(one case per UI screen — image/label checks). The genuinely behavioural functional set is ~110
cases (Sign On/Session, Operator/Supervisor/Technician/Admin menus, FLU, Basket & Payment,
Top Up & Validation, Issue Card, Barcode, Smartcards, Tickets, NIR, Ulsterbus, Metro) plus ~11
Non-Functional (Printer, Power & Audio, Comms, Stability).

---

## Summary

The suite is strong on the **classic POS retail flow** (sign-on/lockout, FLU by mode, basket, cash &
card payment, annulment, top-up, validation, card issue, receipts, ticket-type catalogue, per-screen
validation). Against the distilled requirements it has **five high-value behavioural holes** and a
systemic grounding weakness:

1. **Refund on POS (FBD-100373) is entirely absent** — 0 cases (grep `efund` = 0). A whole Operator
   Menu feature (cash URN + card PRN/PSP flows, role gating, audit, reporting, finality) is uncovered.
2. **Barcode device-matrix + audit rules (FBD-100167/100317/100318) are unasserted** — only 4 generic
   barcode cases exist; none assert the POS single-use-only / reject-multi-use scoping, the Corethree
   type matrix (Bus=W, Rail=B,U,E,S,D,H), the Ceiling-Limit offline boundary, or the
   event-vs-transaction / `BarcodeUsage` audit split.
3. **Fare-Stage-name display/print + zero-fare block (FBD-100207) not asserted** — stop-selection
   cases exist but none assert the POS shows/prints the **Fare Stage name (not stop name)** or that a
   **zero fare blocks ticket issue**.
4. **Device heartbeat (FBD-100266)** — no case asserts the POS calls CloudFare every **15 min via the
   Staff-List check even when signed out** (grep `eartbeat`/`StaffList`/`15 min` = 0).
5. **MERIT revenue-location allocation (FBD-100341)** — no case asserts a POS transaction's
   route/operating-unit drives the **PM/PR/PU** MERIT allocation (e.g. rail ticket on an Ulsterbus POS
   → NIR/PR, not device-home).

Plus a **grounding gap**: functional cases are written against generic actors ("an operator is signed
on", "building a fare") with almost no concrete route/operator/stop/product identifiers — falling
short of the new grounding standard (see final section).

Many other cited FBDs are **CloudFare/BOS-only** (fares export 100336/100450, service classification
100377, claims 100342, hierarchy 100383, name usage 100260) and are correctly **out of the POS device
suite** — noted below so they aren't mis-assigned to POS.

---

## Missing (new cases needed)

### Refund on POS — FBD-100373 (highest value; 0 existing cases)
The POS is the only device that refunds, and none of it is covered. New cases needed:
- **Cash refund happy path** — Operator Menu → Issue Refund → Cash Refund, key 23-char **URN** + amount,
  currency auto-format (`2500`→£25.00), refund receipt (customer+operator copy).
- **Cash validation negatives** — URN ≠ 23 chars; refund > original sale value (last-5 digits);
  refund that would drive shift totals negative → **"Cash refund cannot be performed"**; field-clear
  behaviour with `C`.
- **Card refund path** — key **PRN** (alpha entry via L1–L5/R1–R5), PSP called in real time; audit +
  receipt use the **PSP-returned** amount; over-value capped to original; **PSP timeout / no network →
  no refund + error tone**; PSP-declined failure.
- **Role gating** — **Operator can refund; Supervisor / Technician / Administrator cannot** (FBD-100373
  role matrix — explicitly the reverse of intuition).
- **Cross-device / cross-date / cross-company** refunds (POS refunds POS/TVM/HHD cash+card; **ETM
  cash-only**) — tag these **@CR115** so they can be deselected if CR115 slips.
- **Audit-field assertions** — Fare recorded **positive**; Payment Method **1**(cash)/**3**(card);
  reference = URN(cash)/PRN(card); Product type **Open** with **Allow Refund=true**; Ulsterbus →
  **Route Variant Id** present / NIR → **Route Reference Id** present.
- **Finality** (no annul after refund) and **partial refund**; **basket URN = per-ticket value** vs
  **basket PRN = shared** distinction.

### Barcode scoping & audit — FBD-100167 / FBD-100317 / FBD-100318
Existing barcode cases (C4100034 print, C4100035 scan, C4100439 validate-by-reference, C4100440
offline) are generic. Missing high-value cases:
- **POS validates SINGLE-use only; rejects MULTIPLE-use** with **"This Barcode Type is not accepted on
  this device"** (FBD-100167 core scoping rule; FBD-100317 exact string).
- **POS barcode-type matrix**: Bus = **W** only; Rail = **B,U,E,S,D,H**; Barcode or BRID accepted, **not**
  Collect Ticket Code (FBD-100317). Plus **12-digit BRID fallback** path.
- **Offline Ceiling-Limit boundary** — offline single-use accepted only if value ≤ Ceiling Limit;
  above-limit rejected; redemptions **sync back on reconnect** to prevent reuse (FBD-100317/100483).
- **Audit split** — success → **event** (single-use) / **transaction** (multi-use, `BarcodeUsage`
  zero-fare, Merit); failure → event with Unique ID; searchable by Unique ID / Message field
  (FBD-100167/100318).
- **Print config dependency** — barcode printed only if **Print Barcode=Yes + Barcode Use rule** set,
  and **no barcode when one ticket covers multiple passengers** (FBD-100167/100318). C4100034 covers
  "print barcode" but not these negatives.

### Fare-Stage selection behaviour — FBD-100207
- POS **displays and prints the Fare Stage NAME, not the stop name** (screen + printed ticket).
- **Zero-fare stop/stop combination blocks ticket issue** (negative path).
- Selection reachable via **Key Stops (arrow scroll)** or **Fare Stage ID (numeric keypad)** — assert
  the manual Fare-Stage-ID entry path explicitly.

### Device heartbeat — FBD-100266
- POS updates CloudFare **Last Communication at least every 15 min via the Staff-List check, even when
  signed out / no sales** (core heartbeat assertion; period is **fixed, not configurable** — do not
  assert configurability).

### MERIT revenue-location allocation on POS audit — FBD-100341
- Selling a **rail ticket on an Ulsterbus POS** → transaction carries route/operating-unit that
  CloudFare maps to **NIR / PR**, not the device-home location (and vice-versa Ulsterbus-on-Rail → PU).
- **iLink / BVP** integrated-card sales allocate by device/company; **Metro MJ/Travelcard** always →
  Metro, **Ulsterbus MJ/Town-Service** always → Ulsterbus, regardless of selling device.

### Multi-Journey POS issue flows — FBD-100261 (partial today, key flows missing)
- **Ulsterbus Multi-Journey issue**: present card → range selector → **Card Reference Number**
  (7 ranges of ≤8) → journeys → pay; fare = **lookup(card ref ÷ 100) × journey rule**; screen title
  from the SmartUse **Display Description**. Only top-up (C4100392) is covered, not the reference-number
  issue/selection flow.
- **Metro Multi-Journey issue**: zone (Inner/City/Extended) → journeys → pay (C4100391 covers top-up
  only).

---

## Stale / Wrong (cases to fix — cite case id + FBD id)

*Confined to defensible items; full step bodies were not expanded, so each carries a verify note.*

- **C4100440** (`Barcode — offline validations stored until reconnect`) vs **FBD-100317 / FBD-100483** —
  asserts a blanket "barcodes validated while offline are stored and synced" with no **Ceiling-Limit**
  gate and no **"ticket already used"** local pre-check. Per spec, POS offline single-use is only
  permitted **≤ Ceiling Limit** and must reject above it. As written the case **overstates** offline
  capability. **Fix:** add the Ceiling-Limit accept/reject boundary + already-used pre-check, or split
  into two cases. (verify against full body.)
- **C4100439** (`Barcode — validate a ticket by barcode`) vs **FBD-100167 / FBD-100317** — generic
  "validate a ticket by barcode" with no barcode-class scoping. If the body treats POS as validating
  any barcode it **contradicts** the POS = single-use-only rule. **Fix:** constrain to single-use types
  and add the multi-use rejection string. (verify — likely PARTIAL rather than outright wrong.)
- **Fares-export mis-assignment risk** — **FBD-100336 / FBD-100450** are CloudFare BOS export features
  with **no device behaviour**. No POS case should assert them; if any coverage-mapping ties POS cases
  to these FBD/REQ ids (REQ-2661.0), re-home to a BOS/fares-config suite. (No offending POS case found
  in this snapshot — preventive note.)

No further hard contradictions were identifiable from titles/objectives alone. A fuller pass over the
functional step bodies is recommended before finalising the Stale list.

---

## Partial

- **Fare-Stage selection** — **FBD-100207**: C4100376 (`Bus FLU — change boarding stage, alighting
  stage and fare type`), C4100378 (`Default Boarding Stage '*' key`), C4100507 (`Technician — set
  Default Boarding Stage`) cover stage selection mechanics but **omit** the Fare-Stage-name
  display/print and zero-fare-blocks-issue assertions (see Missing).
- **Barcode print** — **FBD-100167 / FBD-100318**: C4100034 (`Barcode — print barcode`) covers the
  positive print but not the config dependency (Print Barcode=Yes + Barcode Use rule) or the
  no-barcode-for-multi-passenger negative.
- **Offline / comms-locked** — **FBD-100359**: **well covered** for device behaviour — C4099924
  (`Sign On — Communication Locked`), C4100362 (`Comms — loss enters Communication Locked`), C4100363
  (`Comms — recovery reconnects and syncs`), C4100364 (`token loss does not force OOS`). POS is an
  **Ethernet** device so the eventual out-of-service state is the correct expectation. Only gap: the
  end-to-end **queued-data-delivered-to-MERIT/SmarTrack-on-restore** BOS audit is implied by C4100363
  but not explicitly asserted.
- **Multi-Journey / Travelcard top-up** — **FBD-100261 / FBD-100260**: C4100391 (Metro MJ), C4100392
  (Ulsterbus MJ), C4100009 (MJ limit), C4100435 (expired MJ clears journeys), C4102561/C4102562 cover
  top-up mechanics; the **issue/selection flows** and **screen-title-from-Display-Description /
  amount-labels-from-SmartRecharge** assertions (FBD-100260) are not covered.
- **Card issue / card format** — **FBD-100236 / FBD-100250**: C4100024 (`Issue from blank`), C4100031
  (`recognised by other devices`), C4100390 (`blank card options` — Adult BVP / iLink Zone 1) cover
  issue mechanics; the **issue-record type per card (130/142/132/133)**, **expiry-date edge cases**
  (academic-year EA, NIR Gate Pass 2099, 1991-offset/16-year wrap), and **PSN Modulus-10 check digit**
  are not asserted. (ABT DESFire validation reject cases — ABT-without-TRK, signature/PSN gate — are
  **validator (GV/PV/HHD) scope**, not POS; note but do not add to POS.)
- **Card payment hardware precondition** — **FBD-100183 / FBD-100320**: C4099994 correctly conditions
  card payment on "a payment card device (PCD) is attached" (good — the M020 is on only ~95 of 160
  consoles). Not asserted: the **Miura M020 wired-pairing** precondition and that **TID/TK arrive via
  TMS at commissioning** (Group POS). Mostly commissioning/BOS, but one pairing-precondition case is
  worth adding.
- **Card Reference File** — **FBD-100277**: the **Ulsterbus MJ operator-chosen reference-number** issue
  path on POS (crib-sheet fare→reference selection) is a POS behaviour not covered; the validation
  lookup (alighting stop in WTS SmartUse audit) is primarily **ETM/PV** scope.

### Out of POS scope (noted so they aren't mis-assigned)
- **FBD-100336 / FBD-100450** (fares export) — CloudFare BOS export; useful only as a **fares oracle**.
- **FBD-100377** (service classification), **FBD-100342** (user claims), **FBD-100383** (operator
  hierarchy), **FBD-100260** (product name usage, reporting side) — CloudFare/portal/KeyCloak; assign to
  the BOS/ABT suite (30279). Exception: the FBD-100373 **refund role-gating** case is a genuine POS
  device case (listed under Missing).
- **FBD-100271** (legacy smartcard transfer) — transfer-vs-journey logic lives on **ETM / Glider PV /
  Rail HHD/GV/PV**, not POS; POS passback is covered by C4102560. Out of POS scope.
- **FBD-100483** (integrated barcode API) — TVM Collect-Tickets + NIR HHD single-use; **F/W out of
  scope, rail-device focus**. Not a POS suite target (POS single-use rules come from FBD-100317).

---

## Grounding note (cases lacking concrete route/operator/stop/product detail)

Against the new grounding standard, the functional layer is systematically **under-grounded**: almost
every case opens with a generic actor/state — "**an operator is signed on**", "**the operator is
building a fare**", "**a smartcard is presented**" — with no concrete **route number**, **operating
company/depot**, **boarding/alighting stop or Fare Stage**, or **named product + ID**. Representative
examples: C4099987/C4099988 (FLU), C4100374/C4100376 (Bus FLU), C4099970 (Rail FLU), C4100419–C4100423
and C4100393–C4100411 (ticket catalogues), C4100413–C4100418 (smartcard concessions), C4100007/C4100009
(top-up), C4100024 (issue from blank).

The distilled specs supply exactly the concrete data these cases should pin to, e.g.:
- **FBD-100341**: route **652 (Ulsterbus)**, operating-unit codes **PM/PR/PU**, depot home (Omagh = OM,
  Botanic = BT).
- **FBD-100318 / FBD-100261**: product **640 (Cross Border Standard Adult Single)**, **44** barcode-use
  products, Ulsterbus MJ card-ref ranges, lookup(card-ref ÷ 100).
- **FBD-100167**: iLink Zone 4 last-zone byte **`87`**, scheme id **`5720`**, mode enums
  ALL/BUS/RAIL = `FFFF`/`0001`/`0002`.
- **FBD-100373**: worked URN `01122400428500078601300`, PRN device prefixes (P/H + serial).
- **FBD-100236**: Operator Number **`0x2057`**, PSN 8-digit + Modulus-10 check.
- **FBD-100383**: named operators/depots for home-location grounding.

**Recommendation:** when authoring/refreshing POS cases in `GG - POS - Claude Suite`, ground each in a
concrete example (a specific route, operating company, boarding/alighting Fare Stage, and named product
+ MERIT reference id) drawn from these specs and the fares oracle (FBD-100336/100450), so the expected
fare, allocation code, and audit fields are assertable rather than generic.
