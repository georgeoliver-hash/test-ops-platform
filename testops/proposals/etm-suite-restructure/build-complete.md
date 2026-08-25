# ETM suite restructure — BUILD COMPLETE (2026-06-08)

Target: **`**NEW** ETM-Acceptance Suite`** (id 30254), project TFTS - System Test (42), device
`custom_devtypes [25]`. Source (read-only): `AA-ETM-Acceptance Test` (4943, 936 cases).
Audit: **CLEAN — 0 blocking, 69 advisory** (all intentional screen-name title lengths/separators).

## Final shape — 406 active cases (+65 retired for binning)
After the suite-wide consolidation pass (consolidation-audit.md): sequential flow-step and
pure-variation functional cases folded into their parent flow test. Functional 120 → 90.
| Section | Cases | Notes |
|---|---|---|
| HMI Screen Validation | 280 | One per unique Overflow screen (per-screen layer, kept by design). |
| Functional | 90 | Flow-based + consolidated: Sign On & Session, Fare Look-Up (Navigation/Sales), Ticket Issue + Basket Mode + Promo, Smartcards & ABT + Capping, Driver/Supervisor/Technician menus, Barcode, Location, Revenue Limit. |
| Non-Functional | 23 | Power, Printer/Paper, Displays-LEDs-Audio, Comms (ETM↔BOS), Time, System/Performance. |
| Regression | 7 | Defects with no functional home; the other ~32 fold into owning cases (register). |
| Smoke | 6 | Thin critical path. |

Consolidated from ~900 old ETM-device cases (e.g. 337 smartcard/ABT → 28; ~130 ticket → 17), grounded
in the Overflow flow annotations (16 flows / 196 notes / 365 screens) + screen images, mode-aware
(Metro + Ulsterbus via TestRail **Run Configurations**; tags stay repo-side only).

## Scope decisions (George)
- ETM device only. **Excluded:** ~26 CloudFare/BOS web-admin cases (different system) and all BV
  (Bus Validator) cases. **Kept:** ETM↔BOS interaction (config/software distribution to ETM, audit
  upload, comms-lock, BOS-connection-lost) and ETM-manages-a-paired-device ("Other devices").
- Two-layer model: **HMI = per-screen** validation; **Functional = flow-based** (sequential flow
  steps live as steps inside one flow test, not separate cases — e.g. sign-on/route/journey folded
  into "Driver Sign On — Manual, first use").

## George — remaining TestRail UI actions (API cannot move/delete on this instance)
1. **Bin the 65 retired cases** (all prefixed for easy sorting; target section
   **`ZZ - To Delete (review then bin)`** exists — drag them in or just multi-select by prefix and delete):
   - **35 × `ZZ_DELETE_REVIEW`** — superseded by consolidation (5 sign-on step-cases + 30 folded flow-step/variation cases).
   - **30 × `ZZ_DELETE_DUP`** — created-in-error duplicates from an em-dash encoding slip during the bin step (recovered via `tools/fix_consolidation.py`; the real cases were retired correctly).
2. **Set up Run Configurations** on the suite: **Metro** and **Ulsterbus**. A mode run = the shared
   Functional cases + that mode's specifics (Metro MJ zones/Travelcard/ABT zones; Ulsterbus MJ/Town
   Service/Capping/ABT zones).
3. **Two defects need your input** (`regression-register.md`): **301937** ("NOT FIXED" — confirm
   current status) and **301828** (blank title in the old suite — needs detail) before authoring.

## Optional follow-up (I can do on request)
- Apply the **~32 fold Refs** from `regression-register.md` onto their owning live cases (adds the
  defect-id traceability in TestRail without new cases).
- Wire the HMI cases' `attach` to the exact repo image filenames (currently the Overflow link +
  screen name carry the design reference; attachments 404 on this instance anyway).

## Files (proposals/etm-suite-restructure/)
old-suite-audit.md, run-history-audit.md, smartcards-abt-crosstab.md, structure.md,
regression-register.md, build-complete.md (this), and the pushed specs: signon, navigation-flu,
basket-ticket-issue, smartcards-abt, menus, barcode-location-revenue, nonfunctional, hmi (generated),
smoke, regression, consolidate-bin. Generators: tools/extract_overflow_annotations.py,
tools/gen_hmi_cases.py, tools/organise_flow_zips.py.
