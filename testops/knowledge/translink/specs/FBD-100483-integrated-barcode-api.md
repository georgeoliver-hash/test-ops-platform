# FBD-100483 — Integrated Barcode API (CR094) (distilled)

**Source:** `FBD-100483 Integrated Barcode API CR Design Specification v7.00` (5 Sep 2024, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Scope: **TVM Collect Tickets** and **NIR HHD single-use barcode redemption** via the new Corethree REST API (CR094). Types **F & W (bus) are OUT of scope** — rail focus. Supersedes the online single-use flow in FBD-100317 for TVM/HHD. Glider HHD does NOT use single-use functionality.

## API shape
- Endpoints (JSON, base `https://translink.corethree.net/tickets`, staging `.nonprod.`): `/encryptionkeys` (GET), `/validate`, `/redeem`, `/print`, `/logfailure` (POST).
- **API key in `x-api-key` header**; keys differ by device type and environment (staging/prod); stored securely on device.
- Status-code driven: **200/206 = success**; **400-family = business error** (show error screen, timeout 3s to Home/sales); **500-family = retry after 3s, max 3 attempts / max 30s**, then fall back (offline list / error). **No response in 30s** = same as exhausted 500.
- Every 400/500 also POSTs `/logfailure` with a specific templated message (assert message text per failure).

## TVM Collect Tickets flow
- Customer enters **Booking Reference** → `/validate`. On success validate three fields against CloudFare (searches **all** products/stages regardless of TVM home location, plus **legacy stages**): **ProductId**→Reference Id, **StartPointId**→Stage Id, **EndPointId**→Stage Id. RouteId is **not** validated. Any fail → "Booking reference entered is invalid" + logfailure.
- Details screen fields per barcode type (B/D/E/H/S/U) govern which of Date-of-use / Outbound / Return dates show.
- Print → `/redeem` then `/print`. Redeem success → event **1412 "Barcode Redemption"**. Redeem 500/timeout → add to **offline redemptions list**, still print, event **1417 "Offline Collect Tickets Redemption"** (Component Type Sales, OneShot).
- TVM shows "Take Your Tickets" regardless of print API result unless the physical print fails.

## HHD (NIR) flow
- **Encryption keys** GET **once per shift** at sign-on (+ retry on any decrypt failure); 500/no-response → retry every 30s until success (does **not** block sign-on — old keys still usable). Store up to ~**6** keys with expiry dates; try keys in **reverse-expiry order** (furthest-future first).
- **Dual encryption during migration:** barcodes are AES (new) or TripleDES (legacy). Determine by encrypted string: **no `|`** = TripleDES; **`|` + `1`** = TripleDES; **`|` + number >1** = AES. VersionNumber `1`=TripleDES, `2+`=AES. Only AES keys decrypt AES, only TripleDES keys decrypt TripleDES.
- **Decrypted barcode = 18 comma-separated fields** (order fixed, commas always present). Success check: **exactly 17 commas** AND BarcodeType ∈ {B,D,E,H,S,U}. Fields incl. BarcodeType, ShortID, BookingReference, ProductID, Route, Value, StartPointID, EndPointID, ValidOnDate, ExpiryDate, In/OutboundDate+Notes, ValidOnDate1/2/3 (dates `YYYYMMddHHmm`). Decrypt fail → "Barcode decryption has failed" (3s timeout).
- Two submit paths: barcode scan (side button) or **manual 12-digit Barcode Reference ID** entry → used as **ShortID** in `/validate`.
- Pre-online check: if ShortID already offline-validated locally → "The ticket has already been used".
- **Offline validation** (API down / 30s timeout / 500 exhausted): reject if `Value` > **Barcode Ceiling Limit** (TMS-configured) → "The ticket value exceeds offline validation limit" (Retry/Cancel). Else time-validity checks by type: B/E none; D = today ∈ {ValidOnDate1/2/3}; H/S = today = OutboundDate or InboundDate; U = today = ValidOnDate. Expired → "The ticket has expired".
- **Validation checks** (all types): ProductId, StartPointId, EndPointId valid (home-location/hierarchy scope + legacy stages), RouteId not null. Per-type date-populated + range checks (see spec table for the exact per-field sub-messages, e.g. "The From Station is invalid").
- Visual inspection screen (Figs 12–15 by type); operator **Valid** → `/redeem`; **Not Valid** → failure screen.
- Redeem success → event **1412 "Barcode Redemption"**; 500/timeout → offline list + event **1416 "Offline Barcode Redemption"**, still print.
- Print retry: attempt 1 then attempt 2 (Reprint=true); operator Print-Check Yes/No; logfailure messages per outcome.
- **Offline redemption sweep** (TVM & HHD): triggered on next online redemption, on app start with internet, and **every 15 min**. Redeem then print each queued ref/ShortID; remove on 400/200/206. **No events sent to CloudFare during the offline sweep.**

## Legacy stages
- New TMS setting **"Legacy Stages file"** (HHD & TVM datasets) imports JSON of non-physical alighting groups (e.g. "Any NIR Station"), looked up by `StageId`→`StageName`. Expect ≤12 configured; system supports up to **50**.

## Suite implications
- Cover the **status-code state machine**: 200/206 vs 400 (business error + 3s timeout) vs 500 (3-retry/30s) vs no-response(30s); assert the exact `/logfailure` message strings and CloudFare **events 1412 / 1416 / 1417**.
- Cover **encryption-key lifecycle**: once-per-shift GET, retry-on-decrypt-fail, reverse-expiry key order, ≤6 keys, sign-on not blocked.
- Cover **AES vs TripleDES selection** by the `|`/version rule (migration path) and the **17-comma / valid-type** decrypt-success check.
- Cover **offline validation** Ceiling-Limit boundary + per-type date checks, and the **offline sweep** triggers (online redemption / app start / 15-min) with **no CloudFare events**.
- Cover **manual 12-digit ref entry → ShortID** path and the "already used" local pre-check.
- Cover **legacy stages** JSON lookup (StartPoint/EndPoint resolving to a legacy StageName) and the ≤50 cap.
- Assert TVM validates all products/stages **regardless of home location**; HHD is scoped to **home-location/hierarchy**. F/W out of scope — do not author bus cases here.
