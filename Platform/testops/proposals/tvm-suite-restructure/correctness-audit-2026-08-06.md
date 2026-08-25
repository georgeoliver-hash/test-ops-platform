# TVM correctness sense-check — confirmed issues + fixes (2026-08-06)

Combined coverage + correctness pass across all 13 TVM flow-maps against suite 30284 (344 cases).
Only 4 potential issues flagged, 2 confirmed — TVM had already been through a recent MODE-ALL fix
pass (2026-08-03) and the gap-register/refs cross-check discipline held.

## Fixed and live

| Case | Fix |
|---|---|
| C4103796 | "Multi-Modal Home — selecting Bus shows the Bus home" asserted a specific "Bus home screen" name with no source anywhere (flow-map, flow-annotations.md, translink.md) — gap-register already tracks this as a known, non-blocking residual gap. Marked `**UNCONFIRMED**` rather than asserting the exact screen name |
| C4103695 | "3-Day — the ticket is valid across three consecutive days" was wrong and mis-cited: FBD-100336 (its only ref) is an unrelated back-office Fares-List-Export spec with zero mention of "consecutive"; the TVM flow-map's own UI (independent tap-to-select/deselect per date) and FBD-100690 ("any 3 days within one calendar week, consecutive or not") both confirm the product is a free any-3-days pick, not a fixed 3-day block. Corrected the ref to FBD-100690 and rewrote title/preface/steps/expected |

## Not actioned (correctly refuted)
2 flagged issues were refuted on independent re-check and are not listed here — see the verify pass
output for detail if needed.

## Not yet actioned
`coverage_by_flowmap` write-back to the 13 flow-maps' `Covered by` columns — same follow-up as the
other devices. Two coverage escalations worth a human look before that pass: (1) whether the physical
TVM UI still shows a "Smartcard button" affordance on Home/Multi-Modal-Home despite the device having
no smartcard reader (gap-register Q6) — if it does, that's a legitimate small UI case currently
missing; (2) an apparent tension between C4103673 (implying one combined Sales-home screen with
mode-selection built in) and C4103794/C4103796/C4104907 (implying a separate Multi-Modal Home board
before the per-mode home) — worth a live-system confirmation rather than assuming either reading.
