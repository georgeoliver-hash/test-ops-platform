# HHD suite audit — source-suite map, feature landscape, shared-vs-mode cross-tab

Audit-first recon for consolidating the Translink **HHD (driver/inspector handheld)** suites into a new
suite `**NEW** HHD Test Suite` (id 30285, devtype TBD — a build step, not needed for recon). **READ-ONLY:**
no TestRail writes, no case authoring. Titles + section names only were pulled (`get_cases` +
`get_sections`). Governing mindset: `docs/test-practices.md`. Spec grounding: `knowledge/translink/specs/`.

The HHD is a **T1 handheld** paired to a **Miura M020** external card reader (Bluetooth) — a portable,
battery-powered device. It is the only device that performs **cEMV Revenue Inspection**, and it does
**sales + reversals but never refunds** (FBD-100373). This makes several of its feature areas genuinely
distinctive and not shared with POS/ETM/TVM/PV.

---

## 1. Source-suite map (read-only)

| Suite id | Name | Cases | Sections | Role in consolidation |
|---|---:|---:|---|---|
| **5446** | AA-HHD-Acceptance | **1,632** | 310 | **Primary source of truth** — richest, current (V5/V6, CR094, CR78, Revenue Inspection). |
| **13958** | HHD Master | **455** | 80 | **Near-total duplicate** of 5446's NIR core + a `Glider - MAN-FNC-HHD` branch. Mine for anything not already in 5446; otherwise a dedup casualty. |
| **5608** | FAT HHD Glider | **42** | 20 | Compact **FAT smoke/acceptance** for Glider (Operator/Supervisor/Technician happy paths). Good template for the SMOKE layer; folds into functional. |
| **5505** | R1.1-HHD | **151** | 15 | **Older R1.1** (Barcode Reader, Sign On/Off, Validations, Fares, Paper Tickets, UI, CloudFare). Many titles flagged "(To Check)/(Not applicable)/(Failed Review)". **Mine only for non-superseded detail.** |
| | **Raw total** | **2,280** | 425 | Main scope (5446 + 13958) ≈ **2,087**. |

### 5446 top-level landscape (case counts by top section)
| Top section | Cases | Notes |
|---|---:|---|
| **NIR** (rail mode) | 553 | Sign On, Ticket Sales (Card Payments incl. Reference Numbers, Cross-Border, Basket, Group, Visual Inspection), Smartcard (Commercial/Concessionary/Staff/Dependants/Transfers/Mini-Statement), cEMV Validation, Penalty Warning/Fares, Top Ups, Annulment, **Single Use Barcodes (CR094)**, Multiple Use Barcodes, **Inspector Mode**, Ticket Formats, NIR Printer, Operator/Supervisor/Technician, Power Transition, Network Settings, Defects. |
| **Glider R1.1** (bus/Glider mode) | 440 | Parallel tree to NIR: Sign On, Ticket Sales, Smartcard (Metro/Ulsterbus Multi-Journey, Daylink, Travelcard, Town Service, BVP, iLink, EA), cEMV Validations, Top Ups, Annulment, Multiple Use Barcodes, **Old Barcode Redemption**, **Revenue Inspection (RID/cEMV)**, Ticket Formats, Glider Printer, Operator/Supervisor/Technician, Network Settings, Defects. |
| Barcodes | 162 | TIBU-tagged single-use + multi-use barcode defect/regression cases. |
| Smartcard Validations | 100 | "Validate <Product> Smartcard Product" — one case **per product variant** (Senior/Blind/War Pensioner/60+/ROI/Learning-Disability/DLA/…/every iLink/Metro/Ulsterbus product). Product-explosion. |
| Fixes/Changes | 71 | Versioned buckets V5.0.0…V6.0.1 (regression parking lot). |
| Smartcard Inspection | 58 | Visual/colour-change inspection of period passes. |
| Glider Multi-Use Barcodes | 50 | TIBU-tagged Glider barcode cases. |
| ABT (Invalid — design changed) | 37 | **Explicitly marked invalid** ("Tap Queues/Versions/RiD List/End-to-End/EMV Inspection UX"). Leave. |
| Fixes | 35 | More versioned regression buckets. |
| Non-Functional | 26 | Full Battery, Time, Settings, Device Details, Printer, Other. |
| CR78 HHD Regression | 21 | CR78 (break-mode / smartcard inspection) regression. |
| TL HHD CR78 New Functionality | 19 | Break-mode sign-on, validate/inspect smartcard, passback, auditing. |
| CloudFare | 18 | HHD non-functional aspects, device functionality, payment device. |
| Merit | 14 | Back-office reports (NIR Revenue/Analysis/Translink/Ticketing/Stored Procedures). |
| Power Transition & Warnings | 11 | Power Recovery/Save, Replace Battery, Low Battery Warning. |
| Delete | 9 | Bin. |
| Smoke Tests | 4 | Software release/distribution/versions + card-payment sale. |
| OS 8 / Device Security | 4 | OS upgrade + device lock. |

**Structural observations driving consolidation:**
- **NIR and Glider are two parallel copies of the same tree.** Sign On, Sign Off, Supervisor, Technician,
  Annulment, Top Ups, Ticket Formats, Operator Functions, Power Transition all appear **once under NIR and
  again under Glider R1.1**, then a **third time** in 13958 (HHD Master). This is the dominant multiplier.
- **Smartcard is triply exploded:** by product variant (100 "Validate X" cases), by mode (NIR vs Glider),
  and by lifecycle facet (valid / expired / hotlisted / transfer / top-up / inspection), each its own leaf.
- **~256 cases are regression/defect buckets** (Fixes/Changes 71 + Fixes 35 + Barcodes 162 TIBU + Glider
  Multi-Use 50 TIBU + CR78 Regression 21 — with overlap), version-parked rather than pinned to behaviour.
- **~46 cases are already dead** (ABT-Invalid 37 + Delete 9) — leave, do not carry over.
- **~32 back-office cases** (Merit 14 + CloudFare 18) are BOS/MERIT reporting, not HHD device behaviour —
  candidates to exclude to a BOS suite (same call ETM made for its ~26 CloudFare web-admin cases).

---

## 2. Feature-area landscape (grounded in the specs)

| Feature area | HHD behaviour | Spec grounding |
|---|---|---|
| **Sign On & Session** | Operator/Supervisor/Technician sign-on (ID+password, smartcard, duty number), Message/Word-&-Colour of the Day, topology data, device-locked-after-N, break-mode sign-on (CR78). | — |
| **Sales — Paper Tickets** | Sell paper tickets by cash / warrant / **cEMV card** (M020); cross-border (NIR), basket, group tickets, Bus Rambler; visual inspection of paper tickets. | FBD-100373 (HHD = sales + reversals) |
| **Card Payment (M020)** | **Miura M020 external, Bluetooth-paired** reader; **PRN = `H` + last-8-of-IMEI + ticks + 2-digit operator code**; TID/TK via TMS config **after pairing**; Terminal Group **"HHD Retailing"**. | FBD-100320 (device→payment→group matrix; pairing required), FBD-100373 (PRN format) |
| **Smartcards & ABT** | Validate/inspect Metro & Ulsterbus Multi-Journey, Daylink, Travelcard, Town Service, BVP, iLink (adult/child/NW), aLink, yLink, 24+, EA Pupil/Further-Ed (bus & rail), concessionary (Senior/Blind/War Pensioner/60+/ROI/half-fare families), staff + dependants; expired / hotlisted / faulty; transfers (within/after transfer period, by iLink zone). | FBD-100236/100250/100271 (card formats); mode products |
| **Smartcard Top-Ups** | Top up Multi-Journey, Period, Daylink, iLink, Metro Travelcard, BVP; annul unsuccessful top-up. | — |
| **Smartcard Inspection** *(distinctive)* | Visual/colour-change inspection of period-pass smartcards in **Inspector Mode**; adult/child colour changes; concession/half-fare/staff/EA/youth inspections; invalid-smartcard inspection outcomes; CR78 break-mode inspection + passback. | FBD-100651 (inspection enablement by route ABT Type) |
| **Single-Use Barcodes (CR094)** *(distinctive)* | **NIR/rail HHD** redeems single-use Corethree barcodes via the Integrated Barcode REST API: encryption-key lifecycle (once/shift, ≤6 keys, reverse-expiry), AES vs TripleDES selection, 17-comma decrypt check, 200/400/500 state machine + `/logfailure`, offline validation (ceiling limit + per-type dates), offline sweep (15-min, no events), manual 12-digit ref → ShortID, legacy stages, events **1412/1416**. **Glider HHD does NOT do single-use.** | **FBD-100483 (CR094)**, FBD-100317, FBD-100167 |
| **Multi-Use Barcodes** | Both NIR & Glider HHD validate multi-use (mLink/Flowbird) barcodes **offline on-device, audited as a transaction to Merit**; validation check order, zone/location validation, partial validation, success/failure/partial screens, ticket formats. | FBD-100317 (multi-use matrix), FBD-100167 |
| **Revenue Inspection (cEMV / RID)** *(HHD-only)* | HHD is the **only** device doing cEMV inspection. Inspector Mode → M020 tap → M020 integrity (scheme/ODA/expiry → "Card Declined") → ChipDNA online account validation → **RID List** deny check ("Card on RID List") → success/fail with distinct audio tones; events **5008–5013**; RID-list lifecycle (full-on-startup, 15-min delta, full-after-EoD, comms deferral); 30-s no-card timeout; inspection tap **cannot be annulled**. | **FBD-100716**, FBD-100651 (Glider TOO), FBD-100690 (NIR TOTO future), FBD-100320 (Inspection MID override) |
| **Annulment & Reversal** *(no refund)* | Annul ticket / top-up / discount (cash & card), reversal (EMV), annul-unique-reference (PRN), "nothing to annul", sign-off annulment; **HHD performs NO refunds** (assert negative). | **FBD-100373** (HHD = sales + reversals, **no refunds**) |
| **Penalty Warning / Fares** | Issue penalty warning + penalty fare (operator menu / inspection). | FBD-100716 (Standard Fare — BO settled) |
| **Ticket Formats & Receipts / Waybill** | Format catalogue (incl. Format 16 annul/cancel), waybill printing with annulment lines. | — |
| **Operator / Supervisor / Technician functions** | Operator menu (totals, mini-statement, favourites, break mode), printer pairing, supervisor start-duty, technician set-TID/TK + pair + version ticket + home location. | FBD-100320 (technician TID/TK + pairing) |
| **Non-Functional — Power / Battery** *(distinctive)* | **Battery device:** power recovery, power save, replace battery mid-shift, low-battery warning, full-battery regression. | — |
| **Non-Functional — Printer / Network / Comms** | HHD printer (NIR & Glider), printer pairing/NFC, network settings, CloudFare comms, device heartbeat via 15-min staff-list refresh, SaaS offline behaviour. | FBD-100266 (heartbeat), FBD-100359 (SaaS/offline) |
| **Non-Functional — Device Security / OS** | Device lock, OS 8 upgrade. | — |
| **Back-office (candidate EXCLUDE)** | Merit NIR Revenue/Analysis/Translink/Ticketing reports + stored procs; CloudFare device functionality. | Belongs in a BOS/MERIT suite. |

---

## 3. HHD-distinctive coverage areas (the reason HHD is not "just another device")

1. **Revenue Inspection (cEMV / RID List) — HHD-ONLY.** No other device type performs cEMV inspection
   (FBD-100716 §"scope"). The whole RID-list lifecycle, M020 integrity-check failures (scheme/ODA/expired
   → "Card Declined"), online account-validation, "Card on RID List", distinct audio tones, events
   **5008–5013**, 30-s timeout, and **inspection-tap-cannot-be-annulled** are unique to HHD. Assert other
   device types do **not** offer it.
2. **Integrated Barcode API / CR094 single-use redemption (NIR/rail HHD).** The FBD-100483 REST state
   machine (encryption keys, AES/TripleDES, 17-comma decrypt, 200/400/500 + `/logfailure`, offline
   validation + 15-min sweep, manual ref → ShortID, legacy stages, events 1412/1416). **Glider HHD is
   explicitly excluded** from single-use — a genuine NIR-vs-Glider divergence.
3. **Sales + reversals, NO refund.** FBD-100373 REQ-1630.0: HHD sells and reverses but **cannot refund**;
   refunds happen only on POS (of an HHD-originated sale, gated by CR115). Assert the negative and the
   annulment-vs-reversal distinction with the HHD PRN (`H`+IMEI) format.
4. **Inspection Tap-On checks + Smartcard visual inspection.** Inspector Mode: cEMV inspection is enabled
   by the signed-on route's ABT Type ("Tap On Only (Flat Fare)" for Glider) per FBD-100651; plus the
   period-pass **visual/colour-change smartcard inspection** (adult/child colour changes, concession,
   half-fare, staff, EA, youth, invalid), and CR78 break-mode inspection + passback.
5. **M020 external paired payment device.** Unlike ETM/PV/GV/BV (embedded Feig), HHD (with POS) uses an
   **external Miura M020, paired over Bluetooth**, Terminal Group **"HHD Retailing"**, PRN keyed on IMEI
   (FBD-100320). Pairing, TID/TK-after-pairing, and payment-device-swap-keeps-TID/TK are HHD-specific.
6. **Portable / battery-powered.** Power recovery, power save, replace-battery-mid-shift, low-battery
   warning — non-functional coverage no fixed device needs.

---

## 4. Shared-vs-mode cross-tab

HHD's two operating modes in the old suite are **NIR (rail)** and **Glider (bus / Metro network)**.
Metro and Ulsterbus appear as **product sets within the bus/Glider branch** (Metro/Ulsterbus
Multi-Journey, Daylink, Travelcard, Town Service), not as separate device trees. Following the department
convention recorded in `etm-suite-restructure/structure.md` (choose structure by degree of divergence, but
handle modes via **Run Configurations** with shared behaviour authored once), the shared core is authored
**once** and only the proven divergences get named per-mode leaves.

| Behaviour | Shared (author once) | NIR-Rail only | Glider / Bus only | Evidence |
|---|:--:|:--:|:--:|---|
| Sign On / Off, Supervisor, Technician, break-mode | ✔ | | | 5446 NIR + Glider trees identical |
| Card payment via M020, PRN, pairing, TID/TK | ✔ | | | FBD-100320 |
| Paper-ticket sale (cash/warrant/card), basket, group | ✔ | | | both trees |
| **Cross-border tickets** | | ✔ | | NIR-only section 579830 |
| **Card-payment reference-number stations** (Yorkgate/Antrim/Coleraine…) | | ✔ | | NIR station list |
| Smartcard validation (representative products) | ✔ | | | both trees, product set differs by config |
| Metro/Ulsterbus Multi-Journey, Daylink, Travelcard, Town Service, yLink | | | ✔ | Glider R1.1 tree |
| iLink / BVP / EA / concessionary / staff / half-fare | ✔ | | | present in both trees |
| Top-ups (Multi-Journey/Period/Daylink/iLink/Travelcard/BVP) | ✔ | | | both trees |
| Annulment & reversal (cash/card/unique-ref) — **no refund** | ✔ | | | FBD-100373 |
| **Single-Use Barcodes (CR094)** | | ✔ | | FBD-100483 — Glider excluded |
| **Old Barcode Redemption (BRS)** | | | ✔ | Glider R1.1 only (563621) |
| Multi-Use Barcodes (validate offline → Merit txn) | ✔ | | | FBD-100317 — both validate |
| **cEMV Revenue Inspection (RID)** | | | ✔ (Glider TOO now) | FBD-100716/100651; NIR TOTO future |
| Smartcard visual/colour-change inspection | ✔ | | | both trees |
| Penalty warning / penalty fare | ✔ | | | both trees |
| Ticket formats & receipts, waybill | ✔ | | | both trees (rail formats land on NIR config) |
| NIR Printer vs Glider Printer | ✔ (one printer area) | | | two copies today → merge |
| Power / battery, network, comms, heartbeat, device security | ✔ | | | non-functional, mode-agnostic |

**Proven divergences (get a named per-mode leaf, everything else = Run Configuration):**
- **NIR only:** Cross-Border tickets · Card-payment reference-number station set · **Single-Use Barcodes (CR094)**.
- **Glider/Bus only:** Metro/Ulsterbus product family (Multi-Journey/Daylink/Travelcard/Town Service) ·
  **Old Barcode Redemption (BRS)** · **cEMV Revenue Inspection** (Glider TOO live; NIR TOTO is future scope
  per FBD-100690 — tag as future, do not author full NIR inspection now).

**Conflicts / cautions to resolve before authoring:**
- **Single-use flow version drift:** FBD-100483 (CR094, v7 2024) supersedes the online single-use steps in
  FBD-100317 for HHD — author to CR094, not the legacy Corethree flow.
- **ABT (Invalid) 37 cases** are marked "design has changed" — leave, don't carry.
- **13958 HHD Master (455)** is a duplicate master — mine only for non-superseded detail, then dedup.
- **Merit/CloudFare back-office (~32)** — decide EXCLUDE-to-BOS-suite (ETM precedent) vs keep the
  HHD-device-impacting subset (payment device, device functionality) only.

---

## 5. What to carry, merge, or leave (summary)

- **Carry (deduped, shared-once):** the NIR/Glider common core — Sign On/Off, Supervisor, Technician,
  Sales, Card payment, Smartcards, Top-ups, Annulment/Reversal, Multi-Use Barcodes, Inspection, Penalty,
  Formats, Power/Battery, Printer, Network/Comms.
- **Carry with named mode leaves:** Cross-Border + Single-Use Barcodes + reference-number stations (NIR);
  Metro/Ulsterbus products + Old Barcode Redemption + cEMV Revenue Inspection (Glider).
- **Fold into functional via Refs:** Fixes/Changes (71) + Fixes (35) + Barcodes TIBU (162) + Glider
  Multi-Use TIBU (50) + CR78 Regression (21) — pinned to the behaviour they defend, not version buckets.
- **Leave (do not carry):** ABT-Invalid (37), Delete (9), R1.1 "(Not applicable)/(Failed Review)" cases,
  duplicate HHD Master cases already represented in 5446.
- **Decide (EXCLUDE candidate):** Merit (14) + CloudFare back-office (18) → BOS/MERIT suite.
