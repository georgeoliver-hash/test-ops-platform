# PV (Platform Validator) Overflow design assets

Drop the **PV Overflow images here**, one subfolder per flow — same workflow as the ETM build.
Images anywhere under `knowledge/flows/**` are gitignored (png/webp/jpg/jpeg/zip); the committed,
derived text is the annotations file.

## How to add assets
1. **Flow-data JSON:** grab it from the browser Network tab on the PV Overflow share link (the share
   page itself is a JS shell WebFetch can't read), and save it as
   `knowledge/flows/PVoverflow_data.json`.
2. **Images:** export each flow from Overflow as a zip of screen PNGs (name the zip with the flow at
   the end, e.g. `PV-... - Sign On.zip`) **or** drop the already-extracted `... - <Flow>` folder —
   into `knowledge/flows/` or straight into this `pv/` folder.
3. Then Claude runs:
   - `python tools/extract_overflow_annotations.py knowledge/flows/PVoverflow_data.json knowledge/flows/pv-flow-annotations.md`
   - `python tools/organise_flow_zips.py --device pv`  (tidies zips/folders into `knowledge/flows/pv/<flow-slug>/`, dedupes Overflow `(1)` copies, quarantines stray screenshots)

## Naming
Keep the flow name at the **end** of each zip/folder name so the slug comes out right. Screen PNGs
keep their Overflow caption names so HMI screen-validation cases can cite the exact filename in the
case preface (TestRail's API here can't attach images).

> Once the JSON + images are in, Claude runs `/onboard-suite <project> pv 10047 <new-suite-id>` —
> audit-first: old-suite inventory + run-history + flow annotations + product×(whatever dimension
> matters) cross-tab, then builds area-by-area, conformance-clean. PV scope/modes confirmed with you
> first (PV is a different device — don't assume it mirrors ETM/POS; the audit proves it).
