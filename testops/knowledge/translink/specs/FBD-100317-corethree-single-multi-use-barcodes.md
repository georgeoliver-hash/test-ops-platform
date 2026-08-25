# FBD-100317 — Corethree Single & Multi Use Barcode Validation (distilled)

**Source:** `Corethree Single and Multi Use Barcode Specification (FBD-100317) V5.00` (10 Jan 2022, C. Kiraz).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100167 (Multiple Use Barcodes), FBD-100483 (Integrated Barcode API — the current TVM/HHD single-use flow supersedes the online-Corethree steps here), FBD-100318 (Barcode Product Config).

## Device × barcode matrix (the core scoping rule)
- **Single-use** (Corethree-generated, validated **online** against Corethree; audited as an **event**):
  - **ETM** — offline against downloaded lists, types **F** (Manifest) + **W** (Walk-up) only; prints; Barcode or BRID.
  - **POS** — online; **Bus = W only**, **Rail = B,U,E,S,D,H**; prints; Barcode or BRID (NOT Collect Ticket Code).
  - **Rail HHD** — online; types **B,U,E,S,D,H**; prints; Barcode or BRID.
  - **TVM** — online; **Collect Ticket Code only** (NOT barcode/BRID scan); Bus = W, Rail = B,U,E,S,D,H; prints.
  - **Glider HHD, PV, GV, BV** — do **NOT** validate single-use (error screen).
- **Multiple-use** (mLink/Flowbird, validated **offline** on-device; audited as a **transaction**): **ETM, Glider HHD, Rail HHD, PV, GV** validate. **POS, TVM, BV** do **NOT**.
- **Mode independence:** TVM & POS do **not** need a specific mode — a Rail barcode redeems on a POS in bus mode and vice-versa (if a Collect Ticket Code exists).

## Single-use barcode types (Corethree)
`B` no date; `U` date-of-use; `E` expiry date; `S` outward+return dates; `D` 3-Day Select (3 dates); `H` inbound within 1 calendar month of outbound; `F` Manifest (ETM only); `W` Walk-up (ETM/POS/TVM). For `F`/`W` the device reads **Product ID** to pick correct ticket layout + dates. `U`/`E` validity date is device-calculated from issue date.
- **BRID** = 12-digit fallback if barcode unreadable/damaged (operator decision). First 2 digits = source: `12`=Being (→Merit), `13`=MMT (→Merit), `99`=Test (not to Merit).

## Validation flow rules (single-use)
- Device pre-checks **offline first** (barcode type, current date, boarding/alighting station) before contacting Corethree; fails these → error immediately.
- **Offline single-use** allowed only if ticket value ≤ **Ceiling Limit** (BOS-configured); above limit cannot validate offline. Offline redemptions must **sync back to Corethree** on reconnect to prevent reuse.
- **Manifest/Walk-up files** pulled from MMT/Being via REST API, refreshed **every 5 min**, covering redeemed+unredeemed barcodes for **−24h/+24h** of the driver's route. A route uses Manifest **or** Walk-up, never both. ETM barcode reader is permanently on during sign-on. Comms failure → retry with configured "retry times".
- Manifest validation exceptions (ETM): red = not on file / wrong route (charge full fare); **amber** = valid barcode wrong journey or wrong boarding stage (shows journey details, operator may **Proceed/Cancel**). Proceed → event `PassUse-Audited by operator`, status→Redeemed, synced MMT/Being→Corethree. Success (normal) → `PassUse`, expected-boarding count decrements by 1.

## Error message content (assert exact strings)
- Wrong device / wrong barcode class (POS multi-use, POS type-F, PV/GV/ETM single-use, Glider HHD non-multi-use): **"This Barcode Type is not accepted on this device"**.
- ETM not-on-file / wrong route: **"This Barcode is not valid – Charge Full Fare"** (red).
- ETM wrong journey: **"This is a valid Barcode but is not valid for the current journey – Check seating capacity"** (amber).
- ETM wrong boarding stage: **"This is a valid Barcode but is not valid at this location – Check seating capacity"** (amber).
- Manifest Collect Ticket Code presented to TVM → TVM error (should never happen operationally); TVM has no interaction.

## Auditing / back-office
- Single-use = **event** (traceable in CloudFare Activity Log + Events & Alerts); Collect Ticket Code shown in event **"Message"** field; **not** synced to Merit.
- Multiple-use = **transaction** recorded in Merit against the assigned multi-use product; traceable in CloudFare + Merit.
- All success + failure records retained for reporting; Flowbird-produced barcodes flow through the same mechanisms as the rest of the estate.

## Suite implications
- Assert the full **device × single/multi × barcode-type matrix** above — this is the primary coverage backbone (POS Rail=B,U,E,S,D,H / Bus=W; ETM=F,W; TVM=Collect-Code only; PV/GV/BV reject single-use; POS/TVM reject multi-use).
- Cover **offline Ceiling Limit** accept/reject boundary and the **sync-back-on-reconnect** anti-reuse behaviour.
- Cover Manifest/Walk-up **5-min refresh**, ±24h window, one-file-per-route, and the retry mechanism.
- Cover the **red vs amber** exception outcomes and operator **Proceed/Cancel** → `PassUse-Audited by operator` audit.
- Assert **exact error strings** (esp. "This Barcode Type is not accepted on this device").
- Assert audit split: single-use → **event** (not Merit); multi-use → **transaction** (Merit). BRID fallback path (12-digit).
- **Note version drift:** FBD-100483 (V7, 2024) redefines the TVM/HHD single-use online API — cross-check which flow the current build implements before authoring TVM/HHD single-use cases.
