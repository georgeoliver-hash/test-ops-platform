# GV old-suite audit — `AA - Gate Validator - Acceptance Test` (suite 14973)

Audit-first, **read-only** landscape of the source GV suite, as input to the consolidation into
`**NEW** GV Test Suite` (30286). No TestRail writes, no case authoring. Pulled titles + section
names only (2026-07-13, project **42 — TFTS - System Test**).

- **Source suite:** 14973 — `AA - Gate Validator - Acceptance Test`
- **Size:** **1,184 cases** across **378 sections** (the "1184" in the brief is the case count, not a project id).
- **Target (build later):** 30286 — `**NEW** GV Test Suite` (same project 42).
- **Device:** Axio4 **GV** gate-validator heads (Android), two per lane (**Primary = Entry/unpaid**,
  **Secondary = Exit/paid**) driving a Flowbird TGS SkyLane gate. Project-4 ABT device.

> **CRITICAL CAVEAT (carried through both docs).** The gate **functional** spec **FBD-100348** is a
> factory **acceptance report** of the gate *cabinet*; a large share of its rows are marked
> *"To be validated on integration of Validator."* Requirement grounding for GV functional behaviour
> is therefore **thin**. This structure is built primarily from the **old suite content**; behaviour
> without an issued spec is explicitly flagged **needs-spec** below rather than invented.

---

## 1. Source map — case distribution by top-level section

| Top-level section | Cases | Nature |
|---|---:|---|
| **Gates in Exit Mode** | 264 | Full validation matrix, exit direction |
| **Gates in Entry Mode** | 259 | Full validation matrix, entry direction |
| **Gates in Entry/Exit Mode (B to A)** | 247 | Full validation matrix, bi-directional B→A |
| **Gates in Entry/Exit Mode (A to B)** | 246 | Full validation matrix, bi-directional A→B |
| Fixes/Changes | 75 | Per-build TIBU regression (4.1.0 → 4.2.0) |
| Screens | 28 | HMI/screen-content validation (Project-3) |
| Technician Menu | 26 | Sign-on, location, sys-mgmt, versions, backlight, audio, comms |
| Legacy Support | 13 | POS/legacy top-up → validate on GV |
| Through put | 4 | Primary/Secondary smartcard & barcode throughput |
| Software Distribution | 4 | SW/config/barcode-data file download |
| Light Pictograms | 4 | Passage-permitted / not / infraction / OOS lights |
| Previous TIBU scenarios | 3 | Primary/Secondary state defects |
| Operating Times | 2 | Start-time reconfigure, time sync |
| Daylight Saving Time Changes | 2 | GMT↔BST while disconnected from BOS |
| Settings | 2 | Screen background colour, data mirroring |
| Gate Interface | 1 | Gate sensor sensitivity calibration |
| Emergency Button | 1 | Emergency release button |
| Power Interruption | 1 | Mains fail with user in gate |
| DESFire | 1 | DESFire smartcard validation |
| MIFARE Classic EV1 | 1 | MIFARE smartcard validation |
| **Total** | **1,184** | |

### The dominant structural fact: 86% is a 4× mode clone
**1,016 of 1,184 cases (86%)** live in the four "Gates in … Mode" sections, which are **near-identical
clones** of the same validation matrix, differing only by the gate's operating direction:

- **Entry Mode** (Primary/unpaid side authorises entry)
- **Exit Mode** (Secondary/paid side authorises exit)
- **Entry/Exit Mode (A→B)** and **(B→A)** — bi-directional, one per direction.

These four directions are exactly the **Controlled sub-modes** of FBD-100348 (entry / exit /
bi-directional). Each clone repeats the identical sub-tree:

```
<Mode>
├─ Audio Feedback (1)
├─ iLink Smartcards
│   ├─ Belfast Visitor Pass → Adult|Child → Valid(3)|Invalid(4-5)
│   └─ iLink Zone 1|2|3|4|NW → Adult|Child → Valid(3)|Invalid(4-5)
├─ Employee Smartcards → Staff Pass | Staff Partner | External Staff | Retired Staff → Valid|Invalid
│   └─ ABT → Visa(2) | Mastercard(3) | Declined Taps(4)
├─ Rail (EA) Pupil / Further Education Smartcards → Valid|Invalid
├─ aLink Smartcards → Valid|Invalid
├─ Invalid Smartcards (30)   ← product-family sweep (Metro MJ, Ulsterbus MJ, Daylink, Travelcard,
│                              Town Service, EA, all concessionary SmartPass types, 24+, Ylink)
├─ Multi-Use Barcodes → TVM-produced(11) | HHD-produced(12) | already-validated-on-GV(10)
├─ Passback (2)
└─ NIR Transfers → Belfast Visitor | Adult iLink | Child iLink | aLink | Staff | Rail EA (≈38)
```
The consolidation prize is collapsing this 4× clone into **one shared functional tree executed
against a mode Run Configuration** (the ETM/TVM precedent), with mode-specific leaves only where the
behaviour genuinely diverges (see structure.md).

---

## 2. Feature-area landscape

**Smartcard product validation (largest area, ~55% of cases).** Per-product acceptance of Translink
stored-product / concessionary smartcards at the gate: iLink (Belfast Visitor Pass + Zones 1/2/3/4/NW,
Adult & Child), Metro Multi-Journey (City/Inner/Extended), Ulsterbus MJ, Daylink, Metro Travelcard,
Ulsterbus Town Service, Employee/Staff family (Staff, Partner, External, Retired), Rail EA Pupil &
Further-Education, aLink, and the full concessionary SmartPass sweep (Senior, ROI Senior, 60+, War
Pensioner, Blind, DLA Half Fare, No Driving Licence, Partially Sighted, PIPS, Learning Disability,
Dependents), plus 24+ and Ylink. Each product carries Valid (new / previously-used / passback) and
Invalid (hotlisted / expired / torn / out-of-zone / before-start) variants. **DESFire** and **MIFARE
Classic EV1** are the card-technology validation cases.

**ABT cEMV taps.** Contactless bank-card taps at the gate — Visa Debit/Credit, Mastercard
Debit/Credit, Maestro, Declined Taps (Deny List / Negative List / Expired / BIN List), and an Offline
Transaction case. Small but the spec-grounded core of Project-4.

**Multi-Use Barcode validation.** Printed and mobile-screen barcodes, per product (Adult, Child,
3-Day Select, 1/3 Off Day Return, 24+, Ylink, Concession, Half Fare, Day Tracker, Unemployed Day
Return); source device TVM-produced vs HHD-produced; cross-device "already validated on a GV then
re-presented on HHD"; expired and already-validated rejection.

**NIR Transfers.** Smartcard validated "within / after transfer period" across iLink/Belfast
Visitor/aLink/Staff/Rail-EA — transfer-window behaviour at the gate.

**Gate mechanics & pictograms.** Light Pictograms (passage permitted / not permitted / infraction /
OOS), Emergency Release Button, Power Interruption (user in gate), Gate Sensor calibration, Through
put (Primary/Secondary × smartcard/barcode).

**Device / operational.** Technician Menu (Sign-on, Navigation, Location Settings, System Management
→ BOS Comms + Power Management, Software/Config Versions, Screen Backlight, Audio Volume, Force
Comms, Maintenance-mode time sync), Software Distribution, Operating Times, Daylight Saving,
Settings (screen colour, data mirroring), Legacy Support (POS top-up → GV validate).

**HMI / Screens.** 28 screen-content cases (Project-3): smartcard screens (idle, not-in-service,
re-present, not-valid-at-location, invalid-time, product-expired, faulty-card, not-accepted,
passback, success), barcode error/success screens, Technician-menu screens.

**Regression (Fixes/Changes + Previous TIBU, 78 cases).** Per-build TIBU defects 4.1.0 → 4.2.0. The
**dominant theme is the Primary/Secondary two-head state machine**: OOS recovery after power failure,
nightly-reboot OOS, Fully-Free mode handling, remote-command/Station-Manager mode changes,
tech-signon-on-secondary side effects, barcode-reader dropout/spamming, audit-data quarantine,
CloudFare status spamming. A second cluster is barcode throughput/quick-succession and the CR116
midnight-4am expiry display.

---

## 3. Spec-grounded vs needs-spec (the honest map)

### 3a. Spec-grounded — behaviour tied to an issued, distilled spec

| Feature area | Spec | Grounding notes |
|---|---|---|
| **Multi-Use Barcode validation** | **FBD-100167** | GV explicitly validates multi-use barcodes. Result states (green tick / yellow step-7-only / red + reason), passback reject, **gateline Unique-ID share (CR105.2)**, **rail £90 fare-fallback (CR105.3)**, **CR116 midnight-4am expiry display**, `BarcodeUsage` zero-fare audit. Old barcode + barcode-error-screen cases map cleanly here. |
| **ABT cEMV taps + declined reasons + gate-opens-on-success** | **FBD-100690** | Check order + **Declined Reason codes 1/2/3/15/20**, success ⇒ **GV opens gate**, **exit/bi-di deny-list exception** (gate opens to let out, tap audited invalid, debt retry), **Gate Direction** entry⇒Tap-On / exit⇒Tap-Off. Grounds the ABT Visa/MC/Declined cases + the exit-mode nuance. |
| **Gate mode matrix, pictograms, open/close timing, emergency/evacuation, heartbeat/BIST, power-fail** | **FBD-100348** | Modes (Controlled entry/exit/bi-di, Free, Locked, Maintenance, Evacuation, OOS), pictogram states, authorise→open ≤650/900ms, open-fail 3s⇒OOS, 3-consecutive-close-fail⇒OOS, evacuation priority, power-up=OOS-until-both-validators, mains-restore=previous-mode. **BUT flagged pending integration — see caveat.** Grounds Light Pictograms, Emergency Button, Power Interruption, Through put *by reference*. |
| **Commissioning / location / router config** | **FBD-100653, FBD-100654** | Primary=Entry/unpaid & Secondary=Exit/paid roles, SkyLane HF03 firmware + Std/Wide variant, one-wire homeLocation/zoneNo, Technician **Location Settings** (Home/Stop/Zone/Install-Point/ID), router static WAN + port-80 NAT. Grounds Technician Menu / Location Settings + post-commission verification. Mostly **field procedure, low automated-test value**. |
| **Device status / activity to CloudFare** | **FBD-100263 / FBD-100358** | Asset-tracking + activity/shift log. Grounds the "gateValidatorState / device status to CloudFare" behaviour behind several TIBU items (e.g. 16455, 18306, 18309). |

### 3b. NEEDS-SPEC — behaviour with no issued functional spec in the GV set

These carry the **largest** share of the old suite and must be flagged, not asserted as validated
gate behaviour:

1. **Per-product smartcard validation at the gate** *(the ~55% bulk).* No GV-listed spec defines
   product-by-product acceptance of iLink / Belfast Visitor / Employee-Staff / Rail-EA / aLink /
   concessionary SmartPass / Metro-MJ / Daylink / Travelcard / Town-Service / 24+ / Ylink at a GV
   head. FBD-100348 is cabinet acceptance; FBD-100690 covers **cEMV taps only**, not stored-product
   smartcards. Likely lives in ABT/smartcard specs (DESFire **FBD-100236**, preprinted **FBD-100250**,
   legacy transfer **FBD-100271**, product config) — **but their applicability to the GV head is not
   asserted anywhere available.** → **needs-spec / cross-ref before authoring product cases.**
2. **NIR Transfers (transfer-period logic at the gate).** FBD-100690 covers ABT free bus↔rail
   transfers, but the **stored-product iLink transfer-window** behaviour at the GV is not clearly
   specced — and TIBU-22401 shows it was still defective/under-development. → **needs-spec.**
3. **Primary/Secondary two-head state machine** *(dominant regression theme).* FBD-100348 gives the
   mode model + power-up=OOS-until-both-comms + mains-restore-previous-mode + heartbeat-loss⇒major-fault,
   but the **inter-head interaction detail** (independent Primary vs Secondary state, tech-signon on
   Secondary forcing OOS, nightly-reboot recovery, Fully-Free handling, Station-Manager mode-change
   propagation) is **entirely bug-derived**. The governing FBD-100348 rows are the *"pending
   integration"* ones. → **needs-spec (pending integration).**
4. **Audio feedback / audible-assistance messages** (Blind / Partial-Sight). Bug-derived only
   (TIBU-16372, 14246). → **needs-spec.**
5. **Software/config distribution to GV & BOS-comms-loss behaviour.** Partially covered by
   FBD-100263/100358 + FBD-100348 heartbeat, but the distribution mechanics for the GV are not
   specced. → **cross-ref ETM analog; partial.**
6. **Throughput, gate-sensor calibration, screen backlight, Settings (background colour, data
   mirroring), Operating Times.** No functional spec. → **needs-spec / device-config.**

### 3c. Duplication & data-quality notes (for the reorg, not for authoring)
- **4× mode clone (1,016 cases)** is the primary consolidation target — collapse to a mode Run
  Configuration; keep mode-specific leaves only for the FBD-100690 **exit-mode deny-list exception**
  and any genuinely direction-specific transfer behaviour.
- **75 Fixes/Changes** (per-build TIBU) should **fold into the functional case that owns the
  behaviour** via Refs (the ETM/TVM regression rule), not survive as a parking lot; only un-homeable
  defects remain. Several TIBU ids **recur across builds** (e.g. 18302, 16372, 18310, 18606, 18566,
  14160) — dedupe on fold.
- Title typos in source ("Chilld", "Samrtacard", "Syncronisation", "Commnication") — do not carry
  forward; not blocking to this audit.

---

## 4. What this means for 30286
- Author **shared behaviour once**; drive the four gate directions by **TestRail Run Configuration**,
  not by four cloned trees (collapses 86% of the suite).
- **Only build spec-grounded functional assertions** for barcode (FBD-100167), ABT taps (FBD-100690),
  and — *as reference/pending-integration* — the gate mode/pictogram/timing matrix (FBD-100348).
- **Quarantine needs-spec areas** (smartcard product acceptance, NIR transfers, two-head state
  machine, audio assist) behind an explicit **needs-spec** marker in the structure so the suite never
  asserts unvalidated gate behaviour. Carry the old cases across as scaffolding but flagged.
- Fold the 78 regression cases into functional homes via Refs (TIBU-#####).

Proposed structure + consolidated count: see `structure.md` (this folder).
