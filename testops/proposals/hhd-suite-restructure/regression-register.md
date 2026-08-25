# HHD regression register — folding the old defect/TIBU buckets into functional homes

Companion to `structure.md` and `old-suite-audit.md`. The old HHD suite (5446 primary) version-parked
**~340 regression/defect cases** in buckets (Fixes/Changes, Fixes, Barcodes TIBU, Glider Multi-Use TIBU,
CR78 Regression, Full-Battery Regression). Per `docs/gherkin-standard.md` ("Pinning past defects") and
`docs/test-practices.md`, a fixed bug is best caught by **folding an assertion into the functional case
that owns the behaviour** and **linking the defect via Refs (TIBU-#####)** — not by keeping a version
bucket. A **dedicated `@regression` case** is written **only** where the scenario has no functional home.

**READ-ONLY / propose-first.** This register records *where each theme lands*; it does not push. The old
suite is untouched. "Fold" = the new functional case (this YAML or a sibling area YAML) carries the
assertion and cites the TIBU/CR in Refs. Counts are the old-suite section case counts pulled read-only
from 5446 (`get_cases`/`get_sections`, project 42).

---

## 1. Old regression buckets — raw inventory (source: 5446)

| Old bucket / TIBU section | Cases | Theme |
|---|---:|---|
| TIBU-13161 — Barcode encoding HHD/TVM | 33 | Barcode encoding fields, UTC dates, expiry defaults, zones, unique-id, per-type redemption |
| TIBU-13316 — Multi-Use Validation Check Order (Bus/Glider) | 28 | Glider multi-use check-order matrix |
| TIBU-13315 — Multi-Use Validation Check Order (Rail) | 23 | NIR multi-use check-order matrix |
| TIBU-13396 — Successful Multi-use Validation Screens | 14 | Success screen/UX |
| TIBU-3874 — HHD/TVM Barcode Printing | 13 | Barcode printing rules (group, max, concession) |
| TIBU-13329 — Unsuccessful Multi-Use Validation UX | 10 | Failure screen/UX |
| TIBU-13392 — Barcode Location Validation | 9 | Boarding/alighting/linked-stop location checks |
| Full Battery — Regression Tests | 9 | 200-transaction loop bug + battery-removed/power-off/reboot recovery |
| Delete | 9 | Bin — not carried |
| TIBU-2953 — HHD Validation Check | 8 | On-device validation checks |
| TIBU-2944 — Automatic Keyboard Display (manual barcode ref) | 7 | Manual reference-entry keyboard UX |
| TIBU-13320 — Successful Multi-Use Validation Screens | 7 | Success screen/UX |
| TIBU-13390/1 — BO Transactions Bus Barcode Validation | 5 | Glider barcode BarcodeUsage audit + partial |
| TIBU-13386 — Multi-Use and Single-Use Discernment | 5 | Single vs multi routing |
| TIBU-13240 — Barcode Zone Validation | 5 | Zone-encoded validation |
| TIBU-2931 — Mode change / Regression | 4 | NIR↔Glider mode change |
| TIBU-2937 — Barcodes Redeemed Count on waybill | 4 | Waybill barcode counts |
| TIBU-3869 — BO Transaction Rail Barcode Validation | 4 | NIR barcode BarcodeUsage audit |
| Boarding Stage Change | 4 | Fare-stage / boarding change |
| TIBU-13239 — Rail Barcode Validation Product Key | 3 | Product-key topology/hierarchy check |
| TIBU-13395 — Unsuccessful Multi-use Validation Screens | 3 | Failure screen/UX |
| Invalid Products | 3 | Invalid product handling |
| TIBU-13236 — Parsing CoreThree and Flowbird Barcodes | 2 | Barcode parse (AES/TripleDES, format 01/02) |
| TIBU-13244 — BO Event for failed Rail Barcode Validation | 2 | NIR failure event |
| EA Card Hotfix | 2 | EA smartcard fix |
| Defects (574292, 574411) | 3 | Misc device defects |
| Fixes/Changes (V5.0.0…V6.0.1 buckets) | ~71 | Versioned regression parking lot |
| Fixes (versioned buckets) | ~35 | Versioned regression parking lot |
| CR78 HHD Regression + New Functionality | ~40 | Break-mode sign-on, validate/inspect, passback, auditing |
| ABT (Invalid — design changed) | 17 | **Leave** — explicitly invalid |
| **Approx. total regression/defect scope** | **~340** | (overlapping buckets; matches audit §1) |

---

## 2. Fold map — regression theme → functional home (via Refs)

Refs shown are what the receiving functional case should carry. "Home YAML" marks whether the case
lives in **this** proposal (`barcode-inspection-nonfunctional-smoke.cases.yaml`) or a **sibling area
YAML** to be authored (Sales, Smartcards, Sign On, Formats — per `structure.md`).

| Regression theme (Refs) | Functional home (section) | Home YAML | Fold note |
|---|---|---|---|
| TIBU-13236 parse; TIBU-2953 validation check | Single-Use Barcodes (NIR) | **this** | Decrypt/17-comma/type + AES-vs-TripleDES cases carry these Refs. |
| TIBU-2944 manual keyboard | Single-Use Barcodes (NIR) | **this** | Manual 12-digit ref → ShortID case carries the Ref. |
| TIBU-13161 encoding (HHD rows only) | Single-Use Barcodes (NIR) + Ticket Formats | split | Per-type redemption (B/D/E/H/S/U) folds to single-use; encoding/format rows fold to Formats (TVM rows out of HHD scope). |
| TIBU-13386 single/multi discernment | Multi-Use Barcodes | **this** | Device-matrix + routing assertion folds to the multi-use section intro cases. |
| TIBU-13315 (Rail) + TIBU-13316 (Bus/Glider) check order | Multi-Use Barcodes | **this** | The green/yellow/red result cases + passback + date/mode checks carry both Refs (Run Config NIR/Glider). |
| TIBU-13240 zone; TIBU-13392 location; TIBU-13239 product key | Multi-Use Barcodes | **this** | Zone-match, route/location-only-yellow, and product-key checks fold here. |
| TIBU-13320 / TIBU-13396 success screens; TIBU-13329 / TIBU-13395 failure screens | Multi-Use Barcodes | **this** | Green-tick + red-cross-reason cases own the success/failure UX. |
| TIBU-3869 (Rail) + TIBU-13390/1 (Bus) BO txn; TIBU-13244 failed event | Multi-Use Barcodes | **this** | BarcodeUsage zero-fare audit + failure-event cases carry these Refs. |
| TIBU-2937 barcodes-redeemed-on-waybill | Ticket Formats & Receipts / Waybill | sibling | Waybill count folds to the waybill case in the Formats YAML. |
| TIBU-3874 HHD barcode printing | Ticket Formats & Receipts + Multi-Use | sibling | HHD group/max/concession print rules fold to Formats; TVM rows out of scope. |
| TIBU-2931 mode change/regression | Sign On & Session | sibling | NIR↔Glider mode-change assertion folds to the session/topology case. |
| CR78 HHD Regression + New Functionality | Smartcard Inspection (break-mode) + Sign On & Session | split | Break-mode inspection + passback case (**this** YAML) carries CR78; break-mode sign-on folds to Sign On (sibling). |
| Full Battery — Regression Tests | Non-Functional / Resilience / Power & Battery | **this** | Power-loss recovery + battery-replace cases carry the 200-transaction loop-bug Ref. |
| EA Card Hotfix; Invalid Products; Invalid Smartcards; Boarding Stage Change | Smartcards & ABT / Sales — Paper Tickets | sibling | Fold to the smartcard-validation and fares cases (sibling YAMLs). |
| Fixes/Changes (71) + Fixes (35) version buckets | Decompose per feature | split | Each versioned entry re-homed to the feature it defends (barcode/inspection/smartcard/sales/power) and cited by TIBU/CR — **not** re-created as a version bucket. |
| Defects (574292/574411) | Per-feature | split | Re-home each to its owning functional case once the underlying TIBU is read. |

---

## 3. Leave (do NOT carry) — not regression to fold

| Old bucket | Cases | Reason |
|---|---:|---|
| ABT (Invalid — design changed) | 17 | Explicitly marked invalid ("design has changed"). Leave in old suite. |
| Delete | 9 | Marked for bin. Leave. |
| EMV Inspection UX (ET-doc placeholder) | 7 | Referenced another project's doc; superseded by FBD-100716 Revenue Inspection cases (this YAML). Leave. |
| RiD List / RID List Updates (superseded) | — | Superseded by the FBD-100716 RID-lifecycle cases (this YAML). Leave old copies. |

---

## 4. Candidate `@regression` (un-homeable) — residual only

After the fold above, essentially **every** old regression theme lands on a functional behaviour — the
buckets were feature-shaped (barcode/inspection/smartcard/power), so they fold cleanly. The residual set
requiring a **dedicated `@regression` case** is small and provisional (confirm when the raw TIBU text is
read, not just the title):

- **Full-Battery 200-transaction loop bug** (from `Full Battery — Regression Tests`) — if the loop bug is
  a *throughput/stability* defect with no single functional owner beyond the battery-recovery case, keep
  **one** `@regression` case "HHD sustains 200 transactions without the processing loop fault"
  (Refs: the Full-Battery loop-bug ticket) rather than diluting the Power & Battery functional cases.
- Any **Fixes/Changes** entry that, once its TIBU is read, proves to be a **cross-cutting stability fix**
  (memory, crash-on-resume) with no feature home → a single `@regression` case each, cited by ticket.

Everything else = **fold + Ref**, no separate case. Estimate: **≤ 5 dedicated `@regression` cases**
against ~340 old regression rows (~99% folded), consistent with `structure.md` (~15 un-homeable ceiling).

---

## 5. Fold summary (headline)

- **~340** old regression/defect rows → **folded into functional cases via Refs**, organised by
  behaviour not by release version.
- **Barcode TIBU themes (~200 rows)** fold into **Single-Use Barcodes (NIR)** and **Multi-Use Barcodes**
  (this YAML), with encoding/printing/waybill rows to **Ticket Formats** (sibling).
- **CR78 (~40)** splits between **Smartcard Inspection** (this YAML) and **Sign On & Session** (sibling).
- **Full-Battery regression (9)** folds into **Non-Functional / Power & Battery** (this YAML).
- **Fixes/Changes + Fixes (~106)** decomposed per feature; **~26 leave** (ABT-Invalid 17, Delete 9).
- **≤ 5** genuinely un-homeable → candidate `@regression`.
