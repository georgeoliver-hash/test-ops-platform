# Findings — NJT Fare Register / Functional States vs FS002 §3.1 + HMI01 §6 (Signed Off)

Source cases: `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/functional-states.md` (92 cases).
Source spec: `knowledge/njt/specs/fs002-functional-states.md` ("Suite implications") + `knowledge/njt/specs/hmi01-fare-register-hmi.md` (§6, "Signed Off").

## Checkpoint table

| Checkpoint | Status | Case id(s) | Notes |
|---|---|---|---|
| Initialising → Idle only when no errors AND no Driver-access-blocking condition | Covered | C4098825 (full AND condition); C4087100/C4087130/C4087147 (partial, no-errors only, no explicit blocking-condition check) | Positive path fully covered by C4098825. Target state on init failure is an explicit spec GAP — see gap register Q2; do not assume the existing C4098827–C4098830 ("Idle - Non Operational" screen on init w/ comms-lock / fault / OOS-remote / blocked-remote) formally proves the functional-state name, only the screen. |
| Comms Locked reachable only from Idle (never directly from Screen Saver/Low Power/OOS) | Missing | (none) | No case tests the negative — that Comms Locked is NOT entered directly from Screen Saver or Low Power. Drafted. |
| Comms Locked blocks Driver sign-on; only "force comms session" + special-user access available | Covered | C4087159 (sign-on blocked, force-comms only option), C4087160 (special user still works) | — |
| Comms Lock timeout boundaries: 0 (disabled), mid-range, max 99,999 hours | Missing | (none) | No boundary case exists for the timeout config value (spec p.11 gives the explicit 0–99,999hr range). Drafted 3 cases. |
| Successful forced comms session returns Comms Locked to Idle | Covered | C4087161 (Driver-initiated), C4087164 (Supervisor), C4087162 (CloudFare remote force), C4087163 (FR scheduled call) | All four force-comms paths covered. |
| Low Power reachable only via Screen Saver (never directly from Idle) | Missing | (none) | Only the positive Screen Saver→Low Power hop is tested (C4087115/C4087144/C4087155/C4098835/C4098838); no case asserts Idle cannot skip straight to Low Power. Drafted. |
| Low Power: screen/components powered down, but back-office AND RS485 comms maintained | Covered | C4087165, C4098838 | — |
| Low Power exit: any key → Idle, correct Idle Mode screen shown (incl. error variant) | Covered | C4087166, C4087114/C4087140/C4087154, C4098836 (no errors), C4098837 (with errors → Idle Non-Operational), C4087291 (HMI wake logic) | — |
| Screen Saver reachable only from Idle | Partial / GAP-entangled | C4098832 (questionable — see Stale note below) | Positive entry from Idle is well covered (C4087108/C4087133/C4087150/C4098826). The strict negative (not entered from Comms Locked/OOS) is untested and is entangled with the unresolved Operational-State↔Functional-State mapping GAP (fs002 "Scope note") — routed to gap register Q1 rather than drafting a case that could assert the wrong thing. |
| Screen Saver exit: any key → Idle | Covered | C4087111/C4087139/C4087153, C4098833 (no errors), C4098834 (with errors → Idle Non-Operational), C4087294 (HMI wake) | — |
| Inactivity chain Idle → Screen Saver → Low Power occurs in order | Partial | C4087108/etc. (Idle→SS), C4087115/etc. (SS→LP), C4098838 (SS→LP w/ comms check) | Each individual hop is covered by a separate case; no case asserts the full ordered chain in one continuous scenario. Drafted (order only — exact timeout values remain a GAP, not asserted). |
| Out of Service entry via local fault detection | Covered | C4087171, C4099022 | — |
| Out of Service entry via CloudFare remote command | Covered | C4087172, C4099023, C4098829, C4098830 | — |
| OOS entry: clear Driver-facing "cannot be used" indication + sends OOS status to CloudFare (GR-3/FRT-1) | Covered | C4087171/C4087176–C4087178/C4087172, C4099023 | Citing GR-3/FRT-1 lives in the spec, not required in case text per the Gherkin standard's "terse, not bloated" rule. |
| Driver sign-on blocked while OOS; special-user access still works | Partial | C4087175 (special-user access — covered); C4087171/C4087176–C4087178/C4087172 (questionable trigger wording) | The "sign-on blocked" side is only implied: these cases use "When the user attempts to sign on as a Driver" as the trigger for the FR to "enter the Out of Service State", which reads as sign-on-attempt causing OOS entry — inverted vs. spec (fault detection / CloudFare command causes OOS entry; sign-on is then blocked as a consequence). Flagged, not rewritten (existing-case edit is out of scope here — a human resolves via TestRail UI per repo rules). |
| OOS recovery: local fault cleared → Idle | Covered | C4087137, C4087152, C4087173, C4099026 | — |
| OOS recovery: CloudFare forces In Service remotely → device usable again | Covered | C4087174 | — |
| OOS fault example — missing/corrupt software/config | Covered | C4087176 | — |
| OOS fault example — tray-chip unreadable (commissioning-only per Note 1) | Partial | C4087177 | Entry/trigger is covered, but no case flags the "should be commissioning-phase-only; anomalous if reproduced post-commissioning" nuance from Note 1 (p.13). Not a distinct testable device behaviour (it's an operational expectation, not an assertable transition) — recommend annotating C4087177 rather than a new case; not drafted. |
| OOS fault example — essential component not detected/functioning (e.g. printer) | Covered | C4087178 | — |
| OOS fault list is explicitly non-exhaustive — don't assume suite covers all OOS triggers | GAP (logged, no case) | (none) | Not a drafting target — routed to gap register Q4 note only. |
| HMI Low Power Mode screen (visual layout, wake, no-timeout) | Covered | C4087290 (layout), C4087291 (wake), C4087303 (no timeout, stays indefinitely) | — |
| HMI Screen Saver screen (visual + animation, 10-min→Low Power, any-key→Idle) | Covered | C4087293 (layout/animation), C4087294 (wake), C4087304 (auto→Low Power) | — |
| HMI Idle screen (visual layout, ISSUE→Operator Entry, invalid-key no-op, 60s→Screen Saver) | Covered | C4087295, C4087300, C4087301, C4087302 | — |
| HMI Idle — Non Operational: 4 named error texts (Comms Lock / Remote lock-or-block / Memory Full / Other fault) | Partial / Stale content | C4087296 (stale — see below), C4087297, C4087298, C4087299 | Only 3 of 4 defined error variants are addressed, and 2 of those 3 use the wrong/duplicated text. Missing: correctly-texted Memory Full and Other-fault variants. Drafted 2 new cases. |

## Stale / duplicate / questionable findings (flag only — no fix applied; human resolves via TestRail UI)

1. Large-scale duplication across the three legacy "Operation State" trees. The "In Service Operation State", "Out of Service Operation State", and "Locked/Blocked Operation State" sub-trees each hold near-identical copies of the same functional-state transitions (Off→Initialising, Initialising→Off, Initialising→Idle, Idle→Locked, Idle→Screen Saver, Locked→Idle, Screen Saver→Idle, Screen Saver→Low Power, Low Power→Idle), with identical titles-pattern and identical steps text, e.g.:
   - C4087098 / C4087128 / C4087145 (Off → Initialising)
   - C4087099 / C4087129 / C4087146 (Initialising → Off)
   - C4087100 / C4087130 / C4087147 (Initialising → Idle)
   - C4087101 / C4087131 / C4087148 (Idle → Locked)
   - C4087108 / C4087133 / C4087150 (Idle → Screen Saver)
   - C4087110 / C4087135 / C4087151 (Locked → Idle)
   - C4087111 / C4087139 / C4087153 (Screen Saver → Idle)
   - C4087114 / C4087140 / C4087154 (Low Power → Idle)
   - C4087115 / C4087144 / C4087155 (Screen Saver → Low Power)

   These transitions are properties of the FR's functional state machine, which per fs002's Scope note is not clearly proven to vary by Operational State context — organising the identical transition three times under three different Operational-State parents (rather than once under a shared "State Management" section, as the newer Communications lock / Initialisation / Low power mode / Screen Saver / Out of Service subsections already do) looks like straight copy-paste duplication rather than deliberate per-context variation. A human should reconcile this in the TestRail UI (repo rules forbid moving/deleting via API).

2. C4098832 ("Screen Saver — from Idle - Non Operational") asserts Screen Saver is entered directly from the Idle - Non Operational operational state after 60s inactivity. This may conflict with fs002's explicit "Screen Saver only enterable from Idle" rule if Idle-Non-Operational represents a distinct functional state (Comms Locked / Out of Service) rather than the Idle functional state with an overlay — the exact mapping is unresolved (gap register Q1). Flagged as questionable, not rewritten.

3. C4087296 (Idle Non-Operational visual layout, 3 Given blocks for Out of Service/Locked/Blocked) reuses the "Communications Locked" header/sub-text verbatim under the "Locked" and "Blocked" Given blocks instead of the spec's distinct "Remote lock or block" text, and both of those blocks are truncated mid-word ("Please notify a Supe"). This looks like copy-paste and data-entry issues in the existing case rather than a deliberate spec-grounded assertion. Flagged, not corrected here.

## Summary

- Covered: 15 checkpoints
- Partial: 6 checkpoints
- Missing: 3 checkpoints
- GAP (logged only, no case possible): 1 checkpoint
- 8 new cases drafted → functional-states.cases.yaml
- 5 gap-register Q&A entries logged → gap-register-functional-states.md
- 3 stale/duplicate/questionable findings flagged (large-scale legacy-tree duplication; C4098832; C4087296) — no edits made, per repo rule that only a human resolves via the TestRail UI.
