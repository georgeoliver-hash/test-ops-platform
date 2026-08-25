# FBD-100260 — CloudFare Product Name Usage (distilled)

**Source:** `CloudFare Product Name Usage (FBD-100260) V2.00` (9 Nov 2020, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.

## The naming fields (CloudFare Products module)
- **Product Description** — main product name, used throughout CloudFare (menus, assignment lists). Also the reporting long name.
- **Short Code** — shortened product name. Also the reporting short name.
- **Default Display Description** — customer-friendly name shown on **all** device screens.
- **Default Sub Product Description** — customer-friendly smartcard product name on device (special cases only).
- **Device Display Description** — per-device override of Default Display Description.
- **Device Sub Product Description** — per-device override of Default Sub Product Description.
- **Reference Id** — links a CloudFare product to a MERIT product reference.

## Reporting (MERIT) name use
- MERIT uses two fields: **Long Description** (50 chars) and **Short Description** (10 chars).
- On CloudFare→MERIT sync, for each product with a **Reference Id** set: CloudFare **Product Description → overwrites MERIT Long Description**, and **Short Code → overwrites MERIT Short Description**.
- Products **without** a Reference Id / not added to CloudFare are **left unchanged in MERIT** (e.g. discontinued products, 3rd-party mobile/barcode tickets). CloudFare never touches them.

## Device display resolution (the core testable logic)
**General rule (all devices, most products):**
1. Use **Device Display Description** if configured;
2. else **Default Display Description** if configured;
3. else **Product Description**.

**Special cases:**
- **Discount/Concession smartcards (WTS SmartUse):** smartcard *name* follows the general rule above. Smartcard *product* uses the **Sub Product** chain: Device Sub Product Description → Default Sub Product Description → Product Description. All variants of one card (e.g. `yLink Single`, `yLink Return`) should share the same Display Description (`yLink`). Name used on Mini Statement; product used when selecting Ticket Type.
- **Multi-Journey smartcards** (types: WTS SmartUse / SmartRecharge / SmartCreate): on **validation**, uses the **SmartUse** product via the general rule. On **top-up / issue**, title = SmartUse product (general rule); the **top-up value amounts** come from each **SmartRecharge** (or **SmartCreate** on issue) product's **Device Display Description** (fallback Default Display Description) — e.g. "5 Journeys", "10 Journeys".
- **Travelcard smartcards** (iLink, DayLink, Metro Travelcard): identical methodology to Multi-Journey; top-up amounts (e.g. "1 Week", "2 Weeks") from SmartRecharge/SmartCreate **Device Display Description** (fallback Default Display Description).
- **ABT products** (types: ABT TopUp / ABT Create): title uses the **Sub Product** chain of one TopUp/Create product (Device Sub Product Description → Default Sub Product Description → Product Description); top-up amounts from each TopUp/Create product's **Device Display Description** (fallback Default Display Description). Assumes all TopUp products share the same Sub Product Description (and all Create products likewise), so which one supplies the title is inconsequential.

## Suite implications (BOS/ABT suite 30279 + device config)
- Highest-value cases are the **3-tier fallback** per product class: configure only Product Description → device shows it; add Default Display → device switches; add Device Display → device switches again. Repeat the same ladder for the **Sub Product** chain (concession + ABT titles).
- **Reporting vs device divergence**: assert MERIT report shows `Product Description`/`Short Code` while the device shows `Device/Default Display Description` for the same product (they are deliberately different).
- **Reference Id gate**: product with no Reference Id must NOT overwrite MERIT; product with one must overwrite Long/Short Description on sync. Verify 50/10-char truncation behaviour.
- Multi-Journey / Travelcard / ABT **top-up screens**: assert amount labels come from SmartRecharge/SmartCreate (or ABT TopUp/Create) Device Display Descriptions, and the title from the SmartUse / Sub Product field — most likely under-covered on POS.
