# GV correctness sense-check — confirmed issues + fixes (2026-08-06)

Combined coverage + correctness pass across both GV flow-maps (Gate Validator Flows, Technician Menu)
against suite 30286 (112 cases). GV had already been through a deep spec-grounding audit
(2026-07-22, gap-register Q10/Q35) and the 2026-08-03 MODE-ALL re-check (found clean, no bug) — this
pass found almost nothing new, confirming that prior work held up.

## Fixed and live

| Case | Fix |
|---|---|
| C4104018 | Said "the invalid-tap screen is displayed" for a passback decline (Declined Reason 20); its own cited spec (FBD-100690) and sibling case C4104050 both specify a **distinct** passback error screen, not the generic invalid-tap screen. Corrected to match |

## Flow-map corrected
`translink-gv-gate-validator-flows.md` path 8 listed "Valid AID (Visa/Mastercard/Maestro)" — copied
from the raw Overflow board transcription. **Maestro acceptance is PV-only** per FBD-100690, confirmed
live by case C4104024 ("a Maestro card is not accepted at the GV") — the board transcription appears
to have conflated GV's and PV's accepted-scheme lists. Corrected the diagram edge and path 8's Covered-
by. Path 9 ("invalid AID (Amex etc) → deny list") may be the same conflation — logged as **gap-register
Q63** rather than guessed at, since no case tests it either way.

## Scope note (not new findings)
~40 of the flow-map's 69 gate-validator paths (gate-mode changes, Entry/Exit/Bi-Directional in-service
loops, FullyFree/ClosedMode/EmergencyMode, legacy-smartcard passenger validation, Primary/Secondary/Both
technician routing) have zero coverage in suite 30286 **by design** — `proposals/gv-suite-restructure/
structure.md` explicitly quarantined these as "needs-spec" pending FBD-100348 (gate-mode state machine,
flagged pending-integration) and a per-product legacy-smartcard-acceptance spec. Not re-flagged as
fresh gaps; already tracked as open blockers in that file.

## Not yet actioned
`coverage_by_flowmap` write-back to both flow-maps' `Covered by` columns — same follow-up as the other
devices, once the needs-spec areas are either resolved or explicitly deferred.
