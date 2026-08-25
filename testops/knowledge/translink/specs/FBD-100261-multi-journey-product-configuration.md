# FBD-100261 — CloudFare Multi-Journey Product Configuration (distilled)

**Source:** `CloudFare Multi-Journey Product Configuration (FBD-100261) V2.00` (24 Nov 2020, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
POS is the **only device that issues** these smartcard products. Related: FBD-100293 (product groups drive the UI), FBD-100268 (product properties).

## Multi-Journey product types (WTS)
- Three variants: **WTS SmartUse** (validation), **WTS SmartRecharge** (top-up), **WTS SmartCreate** (issue new card).
- Typical config: **one SmartUse** product + **many** SmartRecharge and SmartCreate products (one per top-up/journey amount). This granularity gives per-amount fares, per-amount reporting, and independent location validity / ticket assignment.

## Fare configuration
- Each journey-amount product can have its fare **manually set** or **rule-calculated** from another product. Example: 10-journey = £20, rule "10-journey ÷ 2" → 5-journey = £10. Mix manual (bulk discounts / offers) and rule-based freely. Rules created in the topology **Rules** menu, applied via **Product Assignment**.

## MERIT reporting granularity
- Default: each SmartRecharge/SmartCreate has its own **Reference Id** → reported individually in MERIT.
- New **check box** lets many products **share one Reference Id** (controls whether Product Description + Short Code sync to MERIT). Pattern: one Multi-Journey **reference product** per card product type syncs desc/short-code; all top-up variants link to that Reference Id with the box set to **not** sync — so all top-ups report as one MERIT product.
- To still break down top-up amounts in MERIT, use **Default Alighting Stage**: create a legacy stage per amount (5 Journeys, 10 Journeys, …) and set each product's Default Alighting Stage to it.

## POS issue flows (product-group driven — device UI)
- **Metro Multi-Journey:** present pre-encoded Smartlink → select "Metro Multi-Journey" → select **zone** (Metro Inner / City / Extended) → select **journeys** → pay. Needs **4 new product groups** (1 zone selector of Menu type + 3 zone groups). Journey Selection screen title = **Display Description of the SmartUse product** of the presented card.
- **Ulsterbus Multi-Journey:** present card → select "Ulsterbus Multi-Journey" → select **Card Reference Number** (~50 exist, grouped into **7 ranges of ≤8** because the screen has 8 buttons; naming convention "Card Ref. X – Y") → select **journeys** → pay. Needs **~62 product groups** (1 range selector + 7 range groups + ~54 card-ref groups) + **≥1 lookup table**.
  - Card-ref product-group **naming convention must match device software** (device parses the trailing digits after "Card Ref. " to know which reference to encode/price).
  - Fare needs **both** card reference number **and** journey count. Lookup table keyed by card ref **÷ 100** (e.g. 0.05, 0.1, …) → fare in £. Other journey counts derive from the 10-journey lookup via multiply/divide rules; a **separate lookup table** is only needed where a concession/bulk discount (e.g. 40-journey) breaks the derivation.

## Suite implications
- POS-only issue coverage: **Metro** (zone → journeys) and **Ulsterbus** (range → card ref → journeys) flows, asserting the screen titles come from the SmartUse **Display Description** and product-group names.
- Assert **fare calculation** for Ulsterbus = lookup(card ref ÷ 100) × journey rule, incl. the **concession/bulk exception** needing its own lookup table.
- Assert **MERIT reporting mode**: shared-Reference-Id (all top-ups as one product) vs per-amount breakdown via **Default Alighting Stage** legacy stages.
- Product-group **naming-convention** dependency is a fragile config surface — a rename silently breaks POS card-ref parsing; worth a conformance check (ties to FBD-100293).
