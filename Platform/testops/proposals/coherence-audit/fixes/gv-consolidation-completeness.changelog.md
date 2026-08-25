# GV suite (30286) — consolidation-COMPLETENESS audit, 2026-07-23

**Question asked:** did consolidating `AA - Gate Validator - Acceptance Test` (14973, 1,184 cases)
down to the live `**NEW** GV Test Suite` (30286, 96→98 cases) silently drop any genuinely distinct
required coverage — every card/barcode type, decline reason, direction/mode variant — that should
show up somewhere (own case or an explicit "Data variations:" line)? This is a different question
from the two prior GV audits: the 2026-07-17 coherence pass checked internal case coherence, and the
2026-07-22 deep audit checked citation-grounding of what's live. Neither asked "is anything from the
old suite simply not named anywhere any more." This pass does.

**Method.** Pulled old suite 14973 fully (`get_cases(42, 14973)` → 1,184 cases, 378 sections,
`gv-suite-14973-old-raw.json`) and the live new suite 30286 fully (`get_cases(42, 30286)` → 96 cases
pre-fix, `gv-suite-30286-raw.json`), plus re-read the ~57-case
`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` (proposal-only, never
pushed). Grouped the old suite by the existing section landscape (already mapped in
`old-suite-audit.md`/`structure.md`) and checked, family by family, whether every distinct member is
named live, named in the pending-integration file, or genuinely absent from both.

## Priority family: EMS/role sign-on (George's specific concern)

George's worry, verbatim: consolidation might have silently folded a role×method×mode matrix (as
happens on POS with Operator/Supervisor/multiple sign-on methods) down to "one case." **Checked in
full — GV has no such matrix to begin with, and what does exist is fully represented live.**

- The GV has exactly **one role** — Technician (card + 4-digit PIN). There is no Operator/Supervisor/
  Engineer role split like POS; confirmed by reading every old-suite case under `Technician Menu >
  Sign on` (3 cases) and `Technician Menu > Technician Menu Navigation` (3 cases) plus the Project-3
  screen mirrors (3 cases) — all reference the same single "technician smartcard" sign-on method, no
  alternative method (e.g. ID+PIN typed) is ever tested.
- Old suite's distinct sign-on-family behaviours: **Technician Sign On** (valid card+PIN, C2754382),
  **Invalid PIN Entry** (C2754383), **Abandon Sign-On** (card presented, PIN never entered, times out
  back to idle, C2754384), **Auto Sign-Off** (60s idle at the Technician Menu after a successful
  sign-on, C2754318), **Page Timeouts** (30s per-submenu then 60s, C2754319), **Navigation** between
  menus (C2754317).
- Live suite (Technician Menu, section 887835) carries **all of them as distinct cases**: C4104064
  (valid sign-on), C4104065 (invalid PIN), **C4104066 (abandoned sign-on — the incomplete-attempt
  case, distinct from a timeout after a completed sign-on)**, C4104067 (post-sign-on inactivity
  timeout), C4104068 (menu navigation). The abandon-vs-timeout distinction — the exact thing a rushed
  consolidation would most likely blur into one case — is preserved as two separate cases.
- **Verdict: fully covered live, correctly consolidated (26 old cases → the above 5 + Location
  Settings/Software Versions/Configuration Versions/Display Brightness/Audio Volume/Force
  Communications, 7 more — 12 live cases total, no distinct behaviour dropped).**

## Family-by-family accounting

| Family (old suite) | Old cases | Live? | Pending-integration only? | Verdict |
|---|---:|---|---|---|
| 4× mode clone (Entry/Exit/Bi-di A→B/B→A) | 1,016 | Yes — direction is a Run Config; 2 genuine direction-divergent leaves (C4104025 exit deny-list exception, C4104026/4104027 Tap On/Off) authored explicitly | NIR-transfer direction leaf | **Correctly consolidated** — confirmed no third divergent leaf was missed (checked structure.md's own 3-leaf list against the live suite) |
| ABT declined reasons (Deny/BIN/ODA/Expired/Passback) | within the clone | C4104014-4104017/4104050, all 5 codes (1/2/3/15/20) named with FBD-100658 citation | — | **Fully covered live.** Reason `4` (Cancelled) has no GV-specific scenario in the old suite or a spec tie to the gate — not a drop, just an unused enum value not applicable here |
| Multi-Use Barcode products (Adult/Child/3-Day Select/1-3 Off Day Return/24+/Ylink/Concession/Half Fare/Day Tracker/Unemployed Day Return) | within the clone | C4104028 names **every** product as a Data-variations line | — | **Fully covered live** |
| Barcode result states, passback, CR105.2/CR105.3/CR116, TVM/HHD provenance | within the clone + Multi-Use Barcodes(4) | C4104028-4104047 (20 cases) | — | **Fully covered live**, re-verified against FBD-100167 in the 2026-07-22 deep audit |
| Passback (smartcard + barcode + cross-gateline-head) | 2 + within clone | C4104048-4104052 (5 cases) | — | **Fully covered live** |
| Technician Menu / sign-on / role | 26 | 12 live cases (see priority section above) | — | **Fully covered live, no drop** |
| Smartcard product acceptance (iLink/Belfast Visitor/Employee-Staff/Rail-EA/aLink/concessionary sweep/Metro-MJ/Daylink/Travelcard/Town-Service/24+/Ylink, valid+invalid variants, DESFire/MIFARE tech) | ~650 (the 55% bulk) | No — **pending-integration §3**, needs-spec (no issued GV spec for per-product gate acceptance) | Yes — every product family and both card technologies named via Data-variations | **Correctly held as flagged scaffolding**, not silently dropped — shows up in the pending file, just not asserted live (deliberate, George-approved stance, unchanged by this pass) |
| NIR Transfers (product × within/after window × direction) | ~38 ×4 modes | No | Yes — §4, 6 cases, product sweep + explicit direction-dependency case | **Correctly held as flagged scaffolding** |
| Primary/Secondary two-head state machine | Fixes/Changes cluster + Previous TIBU (3) | No | Yes — §5, 12 cases covering the named TIBU ids (14648/14660/14670/14717/16491/18606/18614/18930/19026/19250/23455/18944) | **Correctly held as flagged scaffolding.** A few very old/superseded TIBU ids (14711, 14722, 16779, 18302, 18306, 18309, 18413, 18416, 18310) fold into the same general two-head cluster rather than needing individual cases — consistent with the "fold fixed defects into the behaviour, don't reflex-add per bug" rule |
| Gate Mode & Access Control (Controlled/Free/Locked/Maintenance/Evacuation/OOS), pictograms, buzzer, open/close timing, audio assist | FBD-100348 rows (pending integration in the spec itself) | No | Yes — §1/§2, 18 cases | **Correctly held as flagged scaffolding** — FBD-100348 itself marks these rows "to be validated on integration," so holding back is the spec-honest choice, not a gap |
| Light Pictograms / Emergency Button / Power Interruption / Gate Interface (sensor calibration) | 1+1+1+1 = 4 | Sensor calibration: no; pictograms/emergency/power: yes, in §1/§2 of pending | Gate sensor calibration was **missing from pending too** until this pass | **Fixed** — added `Gate Sensor Calibration (needs-spec)` §8 to the pending-integration file |
| Operating Times (start-time reconfigure, GV time sync) + Daylight Saving (GMT↔BST) | 2 + 1 (Maintenance-menu time sync) + 2 | No | **No — missing from both live and pending until this pass**, despite `old-suite-audit.md` §3b(6) explicitly flagging this cluster as "needs-spec / device-config, carry as scaffolding" | **Fixed** — added `Operating Times & Time Sync (needs-spec)` §6, 4 cases, to the pending-integration file |
| Settings (Main Screen background colour, Data Mirroring) | 2 | No | **No — same oversight** | **Fixed** — added `Device Settings (needs-spec)` §7, 2 cases |
| Legacy Support (POS top-up → GV validation, iLink zones × Adult/Child, Metro Travelcard × Adult/Child, one time-based-product case) | 13 | No | **No — same oversight** | **Fixed** — added `Legacy Support (needs-spec)` §9, 3 cases (equivalence-partitioned: one representative iLink-family case with a Data-variations line for the 10 zone/passenger-type old cases, one time-based-product case, one Metro Travelcard case kept separate because the old suite records the **opposite** outcome — logged as **gap-register Q58**, a genuine cross-case conflict, not silently resolved either way) |
| Through put (Primary/Secondary × smartcard/barcode) | 4 | Yes — C4104101 walks Primary then Secondary with an explicit card-and-barcode burst in one case | — | **Correctly consolidated** |
| Software Distribution (software file / config file / config-future-date / barcode-data file) | 4 | Yes — C4104062 names all three file types, C4104063 covers future-activation | — | **Correctly consolidated** |
| Commissioning (roles, firmware, gate-width, homeLocation/zoneNo, router) | within Technician Menu / new | Yes — 11 cases, C4104053-4104063 | — | **Correctly consolidated/authored**, re-verified against FBD-100653/100654 in the 2026-07-22 deep audit |
| HMI / Screens — smartcard screens (10) | 10 | Yes — all 10, 1:1 | — | **Fully covered live** |
| HMI / Screens — Technician Menu screens (11) | 11 | Folded into the 12 live Technician Menu **functional** cases (each names the relevant screen in its Then) rather than duplicated as separate screen-validation cases | — | **Correctly consolidated** under the established Functional-vs-HMI two-layer model (test-practices.md) — the screen name is still asserted, just inside the functional case rather than a duplicate |
| HMI / Screens — Barcode error/success screens (7) | 7 | **Only 4 of 6 error screens were live** (Already Validated, Has Expired, Not Valid At This Location, Type Invalid) + the Success screen | **No — genuinely missing from both live and pending** (this cluster is spec-grounded, FBD-100167, not needs-spec — so it shouldn't have been left out at all) | **Fixed live** — pushed 2 new cases to suite 30286, HMI Screens section: **C4104111** "Barcode Error Screen — Barcode Not Valid At The Current Time" and **C4104112** "Barcode Error Screen — Barcode Not Valid On This Service" (old suite C3496716/C3496718) |
| Fixes/Changes regression (75) + Previous TIBU (3) | 78 | Folded into the functional/pending-integration case that owns each behaviour, per the fold-not-parking-lot rule | — | **Correctly consolidated** — spot-checked the TIBU ids against both the live suite (CR116 → C4104039/4104040) and the pending file's two-head cluster; no un-homed defect found that needs a dedicated regression case |

## Fixes applied this pass

1. **Live suite 30286** — pushed via `tools/apply_rewrite.py`... no, via
   `python -m system_test_ops push --file proposals/coherence-audit/fixes/gv-consolidation-completeness.cases.yaml --commit`
   (dry-run first, then commit): 2 new HMI Screens cases, **C4104111** and **C4104112** (see table
   above). Both spec-grounded (FBD-100167), matching the pattern of the 4 sibling barcode-error-screen
   cases already live.
2. **Pending-integration scaffolding** (`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml`,
   proposal-only, **not pushed** — same rule as the rest of that file) — appended 4 new sections that
   `old-suite-audit.md`'s own needs-spec list (§3b) always intended but the original authoring pass
   never wrote: §6 Operating Times & Time Sync (4 cases), §7 Device Settings (2 cases), §8 Gate Sensor
   Calibration (1 case), §9 Legacy Support (3 cases). 10 new scaffolding cases total.
3. **Gap register** (`proposals/coherence-audit/gap-register.md`) — logged **Q58**: the Legacy
   Support Metro Travelcard case (old suite) records the opposite outcome (rejected) to the iLink-
   family cases (accepted) for what looks like the identical scenario. Carried forward as an explicit,
   flagged conflict in the new scaffolding case rather than silently picking a side.

## Pending-integration set — status (per task instruction, not pushed)

Nothing in this pass changes the ~57-case (now ~67-case, after the 10 additions above)
pending-integration set's fundamental status: **proposal-only scaffolding, never pushed, held back
because the governing spec (FBD-100348) is itself marked "pending integration on the real hardware"
or because no GV-scoped spec exists at all (per-product smartcard acceptance, NIR transfers, two-head
state machine).** Today's other GV finding (gap-register **Q10**, the TVM-multi-use-barcode
table-parsing correction) does not touch anything in the pending-integration file — Q10 was about a
**live, spec-grounded** case (C4104030) that turned out to already be correct; it has no bearing on
the needs-spec areas. **No pending-integration case is recommended for promotion to live from this
pass** — the one live-vs-pending boundary issue found (the barcode-error screens) was spec-grounded
and has been pushed live directly, not routed through pending-integration.

## Audit result after this pass

`python -m system_test_ops audit --suite 30286` (run automatically by `push --commit`): **CLEAN** —
97 live cases (98 total minus the pre-existing condemned C4104038), 0 blocking findings, 38
title-too-long advisories (pre-existing, unchanged).

## Files touched
- `proposals/coherence-audit/fixes/gv-consolidation-completeness.cases.yaml` (new, pushed live)
- `proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` (extended, proposal-only)
- `proposals/coherence-audit/gap-register.md` (Q58 added)
- `proposals/coherence-audit/fixes/gv-suite-14973-old-raw.json` (new — full old-suite pull, for
  future reference/re-audits)
- `proposals/coherence-audit/fixes/gv-suite-30286-raw.json` (refreshed — now reflects the 98-case
  live suite)
