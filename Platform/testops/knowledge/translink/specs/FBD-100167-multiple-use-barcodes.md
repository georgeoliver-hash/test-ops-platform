# FBD-100167 — Multiple Use Barcodes (distilled)

**Source:** `FBD-100167 Multiple Use Barcode Specification V12.00` (5 Sep 2024, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100317 (Corethree Single/Multi barcode), FBD-100483 (Integrated Barcode API), FBD-100318 (Barcode Product Configuration).

## Scope — which devices print / validate
- **Print** multiple-use barcodes: ETM, HHD (and POS prints, per ticket config).
- **Validate** multiple-use barcodes: ETM, HHD, GV, PV (gates).
- **POS & TVM validate SINGLE-use barcodes only — NOT multiple-use.** (Key scoping rule for suites.)
- Corethree barcodes (mLink mobile, format `02`) are validated by Flowbird devices **offline**, using the **same business rules** as TFTS multi-use barcodes.

## Printing rules (device)
- Barcode appended to the **end** of the ticket, only if enabled per-ticket-type in CloudFare.
- **No barcode** printed when one ticket is issued for **multiple passengers**.
- On print, the **Unique ID is stored on-device for a configurable number of minutes** to guard passback — **ETM & HHD only**, subject to **CR105.1**.

## Encoding (Aztec 2D, AES CBC/PKCS7, non-zero IV; 4-key ring w/ expiry)
- Unencrypted header: Scheme ID (`5720` for Translink), Barcode Format (`01` Flowbird / `02` Corethree), Key Version Code, LRC (XOR integrity, seeded FF). Remainder encrypted.
- Mode enum: **ALL=`FFFF`, BUS=`0001`, RAIL=`0002`**.
- Unique ID = last 6 of device serial + seconds-since-epoch (8 hex) + 2-hex sequence (Corethree uses 11-digit Short ID).
- Start/Expiry `yyMMdd-HHmm` in **UTC**. Expiry defaults: type "Days"+ → **4am** of calculated date; undefined/0 → 4am next day; 3-Day Select → 4am on 3rd day.
- Zone Validity: blank=none; `ALL`=all zones of boarding+alighting; or specific zone numbers. Encoded via Zone Barcode Id bytes, **top bit set marks the last zone** (e.g. `87` = iLink Zone 4 as final). Mapping via TMS-distributed JSON (`Zone Barcode Mapping File`), max 126 zones, ids/numbers immutable once set.
- Boarding/Alighting Location populated only if product setting **"Barcode Location Validation" = Yes**. Bus = PTI Reference (Scheme Id); Rail = Stage Id, space-padded.

## Validation algorithm
**Bus** (Vehicle Type = Bus): passback Unique-ID check → mode Bus/Both → now ≥ Start → now ≤ End → product exists in CloudFare → zone match (if encoded) → **device is between boarding & alighting (inclusive), stops on the signed-on route, boarding ≤ current < alighting**.
**Rail** (Vehicle Type = Train): same temporal/mode/product/zone checks, plus **Rail Location Validation** via new anywhere-to-anywhere line routes + linked-stop loops (e.g. Belfast GVS↔City Hospital↔Botanic↔Lanyon). If location check fails, **fare-fallback: if the product's rule value ≥ £90 (configurable in TMS) treat as valid** (CR105.3; needs weekday-excluding rule assignments). 3-Day ticket: current date must equal Start, an Additional-Dates offset, or End.
- Gates may **share the Unique ID across the gateline** (CR105.2).

## Outcomes, screens & timing
- Success → **green tick** + audio; only step-7 (route/location) fail → **yellow question mark** (shown 3s or until next txn/keypress); other fail → **red cross** + reason.
- Screen shows boarding location, ticket type (Display Description = focus), result, encoded boarding/alighting (or zone).
- **Barcode read to beep ≤ 1 second** (reasonable condition). A new barcode presented during a result screen is processed immediately (no wait for timeout).
- **Expiry display (CR116):** if expiry time is **00:00–04:00**, show the **previous day** as the expiry date and **no time** (e.g. `20240520-0400`→"19/05/2024"; `20240520-0159`→"19/05/24"; `20240520-0401`→"20/05/24 04:01"). Without CR116, only exactly 04:00 rolls back.

## Auditing / back-office
- Success (or step-7-only fail): transaction record (type = barcode **Product ID**) sent to BO immediately, or queued if offline; includes Unique ID, **zero fare**, payment type **`BarcodeUsage`**. Device retains Unique ID for the passback window.
- Failed validation → **event** (with Unique ID + reason) to BO.
- CloudFare: activity-log **filter by Barcode Unique ID**; failed validations viewable in device-activity + alert-management event viewers. Barcode txns flow to **MERIT / Data Warehouse** (but the barcode ID is NOT carried into Merit/DWH). New `BarcodeUsage` payment type accepted into MERIT.

## CR dependencies to track
CR105.1 (passback store, ETM/HHD) · CR105.2 (gateline Unique-ID share) · CR105.3 (rail £90 fare-fallback) · CR116 (midnight–4am expiry rollback) · CR105.

## Suite implications (to action in the barcode re-audit)
- Assert the **device matrix** explicitly: POS/TVM = single-use only; ETM/HHD/GV/PV = multi-use validate; ETM/HHD/POS print.
- Cover the **three result states** (green / yellow-step7 / red) and the **yellow = route-only-fail** distinction — likely missing.
- Cover **passback** (re-present within configured minutes → reject) and **gateline share** (CR105.2).
- Cover **rail £90 fare-fallback** (CR105.3) and **3-Day Select** date logic.
- Assert **audit**: success → `BarcodeUsage` zero-fare txn to CloudFare→MERIT; failure → event with Unique ID; activity-log filter by Unique ID.
- Assert **CR116 expiry display** edge cases (00:00–04:00 rollback) on HHD & GV/PV.
- **No barcode for multi-passenger single ticket**; barcode only if ticket-type configured.
