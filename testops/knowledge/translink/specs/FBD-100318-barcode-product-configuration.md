# FBD-100318 — Barcode Product Configuration (distilled)

**Source:** `Barcode Product Configuration Specification (FBD-100318) V5.00` (16 Feb 2023, C. Kiraz / S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100317 (Corethree single/multi), FBD-100167 (Multiple Use Barcodes).

## Core model
- **Single-use** barcodes = Corethree-generated, validated **online**, audited in CloudFare as an **event**. **Multiple-use** = Corethree/Flowbird-generated, validated **offline** on-device, audited as a **transaction**.
- **Single-use needs NO separate barcode product in CloudFare** (change from before). It links Corethree↔CloudFare↔MERIT purely via **Reference Id (= MERIT class id)**. One CloudFare FLU product (e.g. Cross Border Standard Adult Single, product ID 640) can back multiple single-use barcode types (B/U/E) with no per-type product.
- **Multiple-use** barcodes DO require a new **barcode use product** in CloudFare **and** MERIT, still linked by Reference Id. There are **44** Flowbird barcode-use products, each mapped 1:1 to a main FLU retail product (Adult/Child/yLink/24+/Student/Senior/60Plus/Blind/War/ROI/PartSig/No DL/LearnDis/DLA/PIPS × Single/Return/Day/Weekly/Monthly).

## Barcode-use product config (the fields that MUST be set)
Valid config points for a Translink barcode-use product (everything else = "Not Valid / no need to configure"):
- **Product Description** (unique; naming `Barc - <Product Name>`), **Short Code** (MERIT short desc, ≤10 chars), **Product Type = `BarcodeUse`**.
- Audit: **Count as Passenger = Yes** (multi-use txns count as passenger boardings → drives on-device passenger count + MERIT Route Breakdown), **Merit Synchronization = Yes** (only Flowbird barcode products sync to MERIT).
- Reference: **Reference ID** (= MERIT class id).
- Rule: **Barcode Passback** (passback time; **only valid for multiple-use**; customizable per device).
- Display: **Display Description** (device-friendly, per-device).
- Explicitly **Not Valid**: Product Category, Annul Allowed, Count as Pass, Default fare foregone, Reference Product, MERIT Default Alighting Stage, Additional Transaction Rule, After Use Menu, Barcode Scheme, Barcode Type, Display Fare, Rapid/Sequence/Validation Sequence Id, **Barcode Search String** (not used for Translink).

## Printing a barcode on a Flowbird ticket
- Assign the barcode-use product to the FLU product via the **'Barcode Use'** rule property, **and** set **'Print Barcode' = Yes** on the main product. Otherwise the ticket prints with no barcode.
- Single-use redemption ticket format: device finds the product via **Product Id → Reference Id** in topology and uses that product's assigned ticket layout.

## Auditing / reporting (viewing)
- **Single-use event viewing:** CloudFare Events & Alerts → Event Viewer, OR Estate Management → Activity Log (Activity=Event). Barcode id / Collect Ticket ref is in the **"Message"** field (searchable). Activity Log date range ≤ **5 days**. **Events are NOT synced to MERIT** → not MERIT-reportable.
- **Multiple-use transaction viewing:** Activity Log (Activity=Transactions); barcode id is in the filterable **"Barcode Id"** field; transactions **ARE** synced to MERIT → reportable for product class "Barcode Use".

## Suite implications
- Assert the config contract when auditing back-office setup: multi-use product has **Product Type=BarcodeUse, Count as Passenger=Yes, Merit Sync=Yes, Reference ID set, Barcode Passback set**; single-use products have **no dedicated barcode product** (Reference Id link only).
- Assert **Print Barcode=Yes + Barcode Use rule** is required to get a barcode on a printed ticket (negative case: barcode omitted when unset).
- Assert audit routing matches FBD-100317: single-use → **event, Message-field searchable, NOT in MERIT**; multi-use → **transaction, Barcode Id filterable, IN MERIT** (passenger count).
- Coverage-mapping aid: the **44 FLU↔Barc product** table is the canonical list for "which products can carry a multi-use barcode" — use it to enumerate product-level test data, not as per-row tests.
- Watch the **≤5-day Activity Log range** constraint when a test verifies back-office visibility.
