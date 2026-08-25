# FBD-100515 — Grouped Stops on TVM (distilled)

**Source:** `FBD-100515 Grouped Stops on TVM CR Design Specification V1.00` (25 Jan 2024, S. James).
Distilled testable facts only — raw spec held locally, not committed.

## Scope / feature
- **TVM only** (plus CloudFare topology config). Lets a customer at a TVM see alighting stops from a
  **group** of boarding stops, not just the single farestage the TVM sits at.
- A **group** = several farestages combined into one "combined boarding stop". **Buses OR rail
  stations only — never mixed** in one group.
- If a TVM's farestage belongs to a group, the TVM **defaults to the group** as its boarding stage.

## CloudFare topology config (testable)
- Grouping is driven by a new **"Area"** free-text field on a **Map Point** (Topology & Fares →
  Drawing Tools → Map Point Settings). **Map points sharing the same Area string are linked** into a
  group. The Area name is the group's display name.
- A boarding stop **can belong to multiple groups/areas** (per requirements) — but the mechanism is a
  single free-text Area per map point, so multi-group is via shared naming.
- **Visualise groups:** searchable **single-select** Area dropdown on the Map Point Functions Menu;
  starts populating after **3 characters**; selecting filters the map to that Area's points; a Clear
  button restores all.
- **Import/Export:** Map Point CSV export/import includes the **Area** column; import assigns new
  Areas and **unassigns** Areas removed from the CSV.
- Group name is **displayed on the TVM screen** and **printed on the customer's ticket**.

## TVM boarding/alighting logic (revised)
- Operating units considered: **TVM Railway (NIR)**, **TVM Metro (Metro)**, **TVM Ulsterbus (UB)**
  (bus-only TVM = Metro+UB; rail-only = NIR).
- **Boarding list:** build list across operating units → for any stop with an Area, **add the Area
  name** to the boarding list → de-duplicate by stage name (keep first, duplicates tracked in a
  "Duplicate Boarding Stops List").
- **Alighting list:** expand chosen boarding stop to all stops in its Area (+ any duplicates) →
  gather valid-fare alighting stops across operating units → add Area names for alighting stops
  (**except** where the Area name equals the chosen boarding stop's name) → de-duplicate.
- **Product availability:** expand both chosen boarding and alighting selections to all stops in their
  Areas → find routes containing any boarding/alighting combination → a product is offered if a fare
  exists for **any** combination; **error screen if no products have valid fares**.
- **Fare selection when multiple combinations exist:** filter to the **lowest non-zero fare**; if
  still multiple, **pick the first combination** in the list. That combination's boarding/alighting/
  route is what prints on the ticket.
- **Key gotcha:** selection is **purely cheapest-fare** — **no preference for the TVM's physical
  location**, so the printed boarding stop may not be the one nearest the TVM.

## Suite implications (TVM)
- Assert grouping is **config-driven by the "Area" map-point field**; same Area string → grouped;
  bus/rail must not be mixed in a group.
- Assert a grouped TVM **defaults to the group** and shows **alighting stops from all boarding stops
  in the group**.
- Assert the **group name shows on screen AND prints on the ticket**.
- Assert **cheapest-non-zero fare** selection and the **first-combination tie-break**; explicitly
  cover the **"nearest stop not necessarily chosen"** behaviour so it is not logged as a defect.
- Assert **no-valid-fare → error screen**.
- Cover CloudFare-side: Area dropdown **3-char** trigger + single-select + Clear; **CSV
  import/export** assign/unassign of Areas.
