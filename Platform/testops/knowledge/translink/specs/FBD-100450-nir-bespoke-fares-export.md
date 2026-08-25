# FBD-100450 — NIR Bespoke Fares Export (distilled)

**Source:** `FBD-100450 NIR Bespoke Fares Export Specification V1.00` (29 Jul 2022, S. James).
(Note: the file's internal header mislabels the doc number as FBD-100336; the folder/spec id is **FBD-100450**.)
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Complements FBD-100336 — this is the **NIR-specific, pre-formatted** rail-fares export. **CloudFare / web-tool back-office feature** — no device behaviour.

## Delivery mechanism
- A **separate simple website** (not the main Export Fares button) linked to CloudFare's external interfaces.
- **Windows-credential login.** User chooses **XLSX or CSV**, and scope of boarding/alighting combinations:
  - **All NIR** combinations, or
  - **NI-only** combinations (**station number ≤ 61**; cross-border stations up to **96** are the "all" case).
- User selects which **products** to include; product list box supports **drag-to-reorder** and per-product **X** to remove. Fares always calculated at the **generate-time date/time**.

## XLSX format
- Default products included (CSV default = none). Additional products append as **columns to the right**.
- Table title per boarding station: **`FARES FROM <BOARDING STATION NAME> STATION`** (station name in capitals).
- Default columns (left→right): Alighting Station **Number**, Alighting Station **Name**, then fares for the NIR products, each via a **named rule**:
  - Adult Single (`STD Adult Single`), Adult Day Return (`STD Ad Day Rtn Fare`), 1/3-Off Adult Day Return (`STD 1/3Off Ad DRtnV`), Adult Weekly Season (`STD Adult Wkly S'son`), Adult Monthly Season (`STD Adult Mthly Sson`), yLink Single (`STD Student Single`), yLink Day Rtn (`yLink Day Return`), yLink Weekly (`STD Stu Wkly S'son`), yLink Monthly (`yLink Monthly`).
- **Additional-product column titles** derived from the product's **Product Category** attribute:
  - Row 1 = **Passenger Type** (blank if unconfigured).
  - Row 2 = **Travel Type** (falls back to **Product Description** if unconfigured).
  - Fares use whichever rule is assigned at the **NIR level** of the CloudFare operator hierarchy.

## CSV format (eCommerce)
- Columns: **`From`** (boarding **stage number**), **`To`** (alighting stage number), then one column **per selected product named by its Product Description** (no default products).
- Product-column fare = the rule assigned at the **NIR level** for that product.
- **One row per boarding/alighting combination** in scope (NI-only ≤61, or all incl. cross-border ≤96), **sorted ascending by boarding then alighting** station number.

## Suite implications (ABT-BOS / fares-config suite, not POS device)
- **Back-office export** — assign to a BOS/fares-config coverage area, not the POS device suite.
- Testable rules: **station-number scope boundary** (NI-only ≤61 vs cross-border ≤96); **XLSX default product set + named-rule mapping**; **additional-product column-title derivation** (Passenger Type / Travel Type→Product Description fallback); **CSV From/To ordering and sort**; **Windows-credential auth gate**; fares taken at **generate time**.
- Useful as a **rail-fares oracle** for validating NIR fare calculation on devices, and pairs with FBD-100336 (which excludes NIR/Glider — they use Reference Tables). Verify the doc-number mislabel doesn't cause a traceability mismatch.
