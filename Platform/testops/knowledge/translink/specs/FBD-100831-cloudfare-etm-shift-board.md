# FBD-100831 — CloudFare & ETM Shift Board (distilled)

**Source:** `FBD-100831 CloudFare and ETM Shift Board Specification v2.00` (8 Jun 2026, S. James / Arrive).
Distilled testable facts only — raw spec held locally, not committed.
Note: **"Shift Boards" = renamed "Running Boards"** (shift = per-driver journeys, not per-bus). Some CloudFare screens still say Running Board pending rename.

## Feature
- ETM predicts and displays a **"Select Journey" list** after the driver enters their **Duty/Shift Number**, so sign-on is semi-automated instead of typing route+journey manually. Managed in CloudFare **Schedule Management module**, distributed via **TMS** (same mechanism as topology).

## Back-office import rules (assert validation)
- **"Import Shift Board Data"** takes a **headerless CSV** with columns: `0 Shift Number` (numeric), `1-3 N/A`, `4 Journey Number` (4 digits), `5 Days of Operation` (**bitmask, Sunday→Saturday** in the CSV, e.g. `0111110` = Mon–Fri), `6 Journey Start Time` (HHMM, ≤4 numeric chars), `7 N/A`, `8 Route Reference` (must match a topology route name).
- Import validation fails (red banner naming bad rows) if: wrong column count, not CSV, Shift Number empty, Days-of-Operation not a 0/1 bitmask, Journey Start Time empty or >4 numeric chars, Route Reference empty. Success → "Upload Complete".
- Import must happen **at the correct operator-hierarchy level**: **Ulsterbus = per-depot** (no inheritance, import at each operating unit); **Metro = once at ETM Metro level, inherited by depots**. Device uses its **ETM Home Location** to decide which level to read.
- **Always import the FULL shift board for a depot** — partial import causes missing data.
- **Publish at Translink level** (devices aren't split by depot in TMS) so all depots' boards are in the output — like topology labels.

## Viewer + versioning + purge
- **Shift Board Viewer** is read-only (no UI edits — re-import to change). Shows Shift, Journey, Journey Start Time (hh:mm), Vehicle Journey Reference (blank unless combined w/ TransXChange), Route, **Valid From/Valid To** (`DD/MM/YY | hh:mm`).
- On import: new/updated entries get **Valid From = 4am local on import day**; superseded entries get **Valid To = 4am local on import day**. Search + per-column filter; page sizes 10/20/50/100.
- **Purge on import:** entries with `Valid To` older than the configured **retention (default 7 days)** are deleted.
- Publish flow: Schedule Version screen → **New Label** (name + associated topology label) → status "Ongoing" → **Publish** (packages DB to TMS, status "Published") / Copy / Delete. TMS **Device Dataset Deployment** adds an optional **"Schedule"** dropdown (labels matching the deployment's topology); **optional** so non-shift-board devices skip it. Activation dates via existing TMS scheduling.

## ETM behaviour (assert filtering + paths)
- ETM downloads shift board like any TMS artifact (manifest diff); reports new **Schedule** version in supervisor/technician menus + Asset Manager. Keeps current board until the new one's **activation date passes** — then next sign-on uses it. Multiple future datasets: must wait for one to activate before scheduling the next.
- Happy-path sign-on: driver number+PIN → safety check (first sign-on of day) → duty number → **Journey List** → route summary → Message of the Day → Word/Colour of the Day.
- **Journey List filtering** (all four must apply): **Home location** of the ETM (duty/journey numbers repeat across depots), **Day of week** (schedule-DB bitmask is **Monday→Sunday**, e.g. `1111100` = Mon–Fri — **differs from the CSV import order**), **Duty Number** (= Shift Number in schedule DB), and **valid route/service** (must exist in DB for the ETM home location).
- Journey List row (left→right): Journey Start Time (shift board), Journey Number (shift board), Service Name (topology), First Boarding Stage (topology, truncated to fit), Direction (topology). **Closest future journey auto-highlighted**; shows 2 previous + 2 next by default; R1–R5 + Enter to select, arrows to scroll.
- **Negative paths:** invalid Duty Number → error screen with retry OR **Manual Override** (uses entered duty, falls to legacy route-entry); journey not listed → **Manual Override** to legacy route-entry.
- **TMS flag** (per CR) enables/disables shift-board sign-on; disabled = legacy manual route/journey entry.

## Suite implications (device/BOS + shift board)
- Assert CSV **import validation** rules and the **two hierarchy patterns** (Ulsterbus per-depot vs Metro inherited); full-board-only import.
- Assert **bitmask day-order flip**: CSV is Sunday→Saturday, schedule DB / ETM filter is Monday→Sunday — a prime regression/bug surface.
- Assert **Valid From/To = 4am local** population and **7-day purge** on re-import.
- Assert ETM Journey List **four-way filter** (home location, day, duty, valid route), **closest-future auto-highlight**, and **both Manual Override negative paths**.
- Assert **activation-date deferral** (device keeps old board until activation) and the **TMS enable/disable flag** toggling to legacy sign-on.
- Newest spec (Arrive-branded, 2026) — likely little/no existing suite coverage; high-priority new coverage area.
