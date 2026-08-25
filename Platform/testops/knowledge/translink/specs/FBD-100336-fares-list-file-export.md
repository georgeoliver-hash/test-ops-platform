# FBD-100336 — Fares List File Export (distilled)

**Source:** `FBD-100336 Fares File Export Specification V5.00` (29 Jul 2022, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100377 (Service Classification Config & Reporting). Requirement: REQ-2661.0. **CloudFare back-office feature** — no device behaviour.

## What it does
- Enhances CloudFare's **"Export Fares"** button to export fares lists from the **currently loaded Topology & Fares Management dataset** in **CSV or XLSX** (tabs toggle format). A prior dataset must be loaded before exporting to get its fares.
- Legacy behaviour retained separately: raw **XML** export of the selected operator/service/route triangles (whole-operator export → zip of per-service XML).

## Export-menu parameters (selection rules)
- **Route Display Box** (right): lists selected routes/reference tables (service name + route name). **Select All Routes** adds everything at/inherited-by the current hierarchy level; **Deselect All**, or hover-cross per row, removes. Rows are **reorderable**, and that order is the order they appear in a **single-file** export.
- **Service Groups** (multi-select, searchable, alphabetical): selecting appends all not-already-listed services/routes in that group; re-selecting removes them (unless still captured by another selected group). If a route from a group is removed by other means, **the service group is deselected**. Distinct from "Service Classification" (School/Goldline). Configured in Settings → Topology, assigned to routes via Edit Route Attributes.
- **Services** / **Routes** / **Reference Tables** (multi-select, searchable): selecting appends; re-selecting removes + unticks. Removing a route by another means deselects its parent service.
- **Product / Reference Fares** (single-select, searchable): default **"Reference Fares"**. Selecting a product exports fares per that **product's rule assignments at the configured date/time** instead of reference fares. **Selecting any product forces "Include Route Attributes" OFF and disabled.**
- **Area / Zone Overlays** (single-select): **None** (default) / **Area Overlay** / **Zone Overlay** — colour-codes triangle cells with a legend.
- **Date / Time** (calendar, default = now): used to calculate the fare for that date/time against current topology data.
- **Include Route Attributes** (toggle, default ON): includes route attributes header + **key-stop and timing-point info** per row. Forced OFF when a product is selected.
- **Single File Export** (toggle, default OFF): OFF = one file per route; ON = all routes in one file in Route-Display-Box order.
- **Export** button disabled unless ≥1 route/reference table selected; **Export keeps the menu open with params retained**; **Close** resets params to defaults.
- Guidance: **avoid large bulk exports** (fare calc time).

## Output / filename rules
- **Single File ON:**
  - Single route/ref table → one CSV/XLSX, one worksheet, filename = route/ref-table name (e.g. `1A_1A (OUT)`, `Glider`). CSV worksheet name = filename; XLSX worksheet name = route/ref-table name.
  - Multiple routes → one file, one worksheet, lists stacked vertically separated by one blank line; filename = timestamp (`Fares Export 2021-10-15 09:00:00`).
- **Single File OFF:**
  - Single route/ref table → as above (one file).
  - Multiple, **CSV** → **zip** (named by timestamp) containing one CSV per route.
  - Multiple, **XLSX** → **zip** containing one XLSX **per service**, each with a worksheet per route (ref table = single worksheet named after the table).
- **Filename suffixes (append in this order):** product name (`_Adult Single`) when product fares selected; then `_Areas` or `_Zones` when an overlay is selected. Example `1A_1A (OUT)_Adult Single_Areas`.

## Content rules
- **Product fare export:** cells contain product fares (from current rules); title/route name includes the product name instead of "Reference Fares".
- **Area overlay:** cells coloured by the area configured for that boarding/alighting combination; legend on the right.
- **Zone overlay:** coloured by the **boarding stop's zone(s)** (per column); a stop in two zones colours the column with both; legend names each zone. (Based on **boarding stop only** — clarified in V2.00.)
- **Reference table export:** a fares square, stage IDs down the side and across the top, reference/product fares in cells; title `<Ref Table Name> Reference Table – <Product Name>`.
- Data fields per REQ-2661.0: fares for all ticket classes plus topology (route name/number, direction, stop name/number, stop GPS, zone).
- Format availability by phase: BRT (A), Metro (B), Ulsterbus (C), NIR (D).

## Suite implications (mostly ABT-BOS / config suite, not POS device)
- This is a **CloudFare export feature** — belongs to a **BOS/fares-config suite**, not the POS device suite. Note it in coverage so it isn't mistakenly assigned to POS.
- Testable rules worth cases: **product-selected → Route Attributes forced off**; **single-file vs multi-file file/zip structure** (CSV zip-of-CSV vs XLSX zip-per-service); **filename suffix ordering** (product then Area/Zone); **zone overlay keyed on boarding stop only**; **Export disabled with no selection**; **Close resets, Export retains** params; **service-group/route selection-coupling** (removing a route deselects its group/service).
- The **fares produced here are the reference for validating on-device fare calculation** (POS/ETM/TVM) at a given date/time and product — useful as a fares oracle for device fare-assertion cases.
