# PV correctness sense-check — confirmed issues + fixes (2026-08-06)

Combined coverage + correctness pass across both PV flow-maps (Barcode, Technician Menu) against
suite 30255 (186 cases). PV had already been through the most extensive prior work of any device
(release-coverage audit, deep-audit, consolidation-completeness, MODE-ALL re-check) — this pass found
almost nothing new.

## Fixed and live

| Case | Fix |
|---|---|
| C4102167 "Technician Menu — reboot" | Tested a standalone, independently-selectable Reboot menu action; neither flow-map source documents this — the only Rebooting screen either shows is reached via the Location Settings edit chain, already covered by C4101012. Marked `**UNCONFIRMED**`, logged as **gap-register Q64** rather than assumed a duplicate and deleted, since the feature might genuinely exist and just be untranscribed |

## Barcode flow-map: no findings
Extensive, clean coverage confirmed across all 35 paths and all 20 HMI screens. Two prior
cross-board screen-naming patterns (gap-register Q27/Q28 — PV screens legitimately cross-cited
between the Barcode and Glider boards) were checked and correctly NOT re-flagged as new issues.

## Not yet actioned (real coverage gaps, not correctness bugs — logged for a future ADD pass)
- Barcode failure-reason granularity (Service/Time/Location/Passback) untested at the functional
  level — only "Expired" has a dedicated functional trigger; the rest rely on generic "or an invalid
  one" wording.
- Reboot-attempt-to-Loading recovery (single-reader-unavailable, dual-reader/other-fault) has zero
  coverage, functional or screen-level.
- Technician Menu: retry-after-incorrect-PIN loop, abandon-sign-on, abandon-PIN-entry, Sign-Off-cancel,
  Location-Settings-no-change branches, and most of the Network Interfaces sub-screens (Details/
  FecDetails/ChangeIP/Routing Table) are untested at the functional level (screen-validation only).

`coverage_by_flowmap` write-back to both flow-maps' `Covered by` columns — same follow-up as every
other device.
