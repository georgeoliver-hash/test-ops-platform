# GV suite (30286) — deep spec-grounding audit, 2026-07-22

Mandate: George's 2026-07-21 directive — the coherence-audit passes done so far (title/steps/
expected internal agreement + spot capability checks) were **not** the full per-case, citation-
grounded cross-examination this tool exists for. This pass does that: every live case's factual
claims checked against the actual FBD/PSPEC source text (not the distilled `knowledge/` notes),
citations verified rather than trusted, and the terse-wording standard re-confirmed while at it (one
combined pass, per instruction, not two).

## Scope

All **96 live cases** in suite 30286 (`**NEW** GV Test Suite`, project 42) pulled fresh via
`system_test_ops cases --project 42 --suite 30286` and raw bodies via
`TestRailClient.get_cases(42, 30286)` (`proposals/coherence-audit/fixes/gv-suite-30286-raw.json`).
Sections: ABT cEMV Taps (887831, 16 cases), Multi-Use Barcode Validation (887832, 20), Passback
(887833, 5), Commissioning & Router (887834, 20), Technician Menu (887835, 12), HMI Screens (887837,
15), Resilience (887838, 11), Smoke (887839, 5). The ~57 pending-integration proposal cases in
`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` were **not** touched —
proposal-only, not live in TestRail, per the task scope.

**Not reached: 0.** Every one of the 96 live cases was read in full and its claims checked against
the governing spec doc(s) in its Refs field, or a targeted search of the wider `REQS_DIR` library
where a claim looked thin. Depth of the check varied by risk: the ABT Tap, Barcode, Passback and
Commissioning/Router clusters (the areas asserting concrete, checkable spec facts) got full
paragraph-level verification via `tools/extract_req.py` and, for one table, direct `python-docx`
table parsing (see below). The HMI Screens and Resilience/pending-integration clusters were spot-
checked against their already-honest `(needs-spec)`/`(pending integration)` markers — those markers
were confirmed accurate (no live-behaviour assertion hiding behind them) rather than re-deriving the
underlying FBD-100348 gate-cabinet rows from scratch (out of scope; FBD-100348 is explicitly a
factory acceptance report per the original restructure caveat, not re-litigated here).

## Method

For each cluster, pulled the actual spec doc(s) via `tools/extract_req.py --entry ... --terms ...` /
`--all` and matched every concrete claim (declined-reason codes, product IDs, screen names, field
compositions, thresholds, config values, cross-device print/validate capability) against the primary
text, not the distilled `knowledge/` notes or the earlier coherence-audit summary. Docs read in full
or targeted: **FBD-100690** (NIR TOTO, ABT Tap section 4.3), **FBD-100658** (ABT Audit Spec, TapId/
DeviceId/CardType/paymentType/revenue fields), **FBD-100167** (Multiple Use Barcodes V12.00, incl.
Table 1 "Device categories"), **FBD-100653** (Gate Router config), **FBD-100654** (Gate System
Commissioning Guide V1.02), **FBD-100348** (Gate Acceptance, targeted terms only — Technician Menu/
buzzer-volume check).

## Findings and corrections applied

Rewrite file: `proposals/coherence-audit/fixes/gv-deep-audit.rewrite.json`. Applied via
`tools/apply_rewrite.py proposals/coherence-audit/fixes/gv-deep-audit.rewrite.json --project 42
--commit` (dry-run first: 9 updated + 1 condemned, 0 missing/skipped — then committed) against
`TESTRAIL_WRITE_SUITE_ID=30286`.

| Case | Finding | Fix |
|---|---|---|
| **C4104013** ABT Tap — TapId composition | **Real grounding error.** The precondition split the spec's own worked-example TapId string at the wrong boundary: case said DeviceId `0420` / Terminal ID `02201156`; FBD-100658's actual field definitions (paras 217-230) give DeviceId `042002` / Terminal ID `20115688` — concatenating `042002` + `20115688` + UNIX ts `1725545715` = `042002201156881725545715`, the exact value the case already quoted. The composed value was right; the "given" breakdown of it was wrong. Also the earlier coherence-audit's "weak expected" note (Then just restates the title) was still open. | Corrected DeviceId/Terminal ID to `042002`/`20115688`; strengthened the `Then` to assert the concrete composed value. |
| **C4104030** Barcode — TVM-produced barcode validates at GV | **Prior finding itself was wrong.** The 2026-07-17 coherence audit (`gv.findings.md`) flagged this Medium: "TVM isn't a multi-use printer per FBD-100167's device matrix." Re-parsing FBD-100167's actual Table 1 ("Device categories") **cell-by-cell via python-docx** (the flattened paragraph-text extraction used by both the earlier audit and my own first read of this table loses the table's column alignment and produces a wrong answer) gives the real matrix: BV (neither), ETM (print+validate), **GV (validate only)**, HHD (print+validate), **POS\* (print only)**, PV (validate only), **TVM\* (print only)**. The `*` footnote refers to the *Validate* column, not Print. TVM does print multi-use barcodes. | **No case change** — C4104030 was correct all along. Gap-register Q10 closed with this citation; the old Medium finding is superseded. |
| **C4104029** Barcode — mobile screen barcode | Low finding (already known): under-specified which barcode variant a "mobile device screen" barcode is. | Named it as the Corethree mLink barcode, format 02 (FBD-100167 para 267, 422) — the only spec-confirmed mobile-screen multi-use artefact. |
| **C4104038** vs **C4104051** | Known duplication (Low, 2026-07-17): both test the identical CR105.2 gateline Unique-ID-share scenario. | Condemned C4104038 (`ZZ_DELETE_REVIEW`), kept C4104051 (better home, Passback section). |
| **C4104070** Location Settings — no-comms | Known coherence gap (Low, 2026-07-17): title asserts the location edit is *blocked* while comms is lost; Expected only ever proved a no-comms *indication*. Deep re-check of FBD-100654 found no text describing whether the save is actually rejected or just flagged. | Retitled to what is actually tested/provable ("a no-comms condition is indicated..."); added an explicit `**UNCONFIRMED**` marker on the blocking claim rather than silently implying it. |
| **C4104100** Heartbeat → Comms rename | Known labelling issue (Low, 2026-07-17): titled "Heartbeat" but tests the 15-min StaffList/Last-Communication refresh, a different mechanism from the true gate↔validator heartbeat correctly tested in C4104094. Refs were already fixed in the earlier terse pass; the title rename was not yet applied. | Renamed to "Comms — the GV updates CloudFare Last Communication at least every 15 minutes via the StaffList refresh." |
| **C4104065, 4104067, 4104073, 4104074, 4104075** Technician Menu (invalid PIN, inactivity timeout, brightness, volume, force comms) | **New finding.** All 12 Technician Menu cases cite FBD-100654 as sole Refs. Full read of that doc (257 paragraphs) confirms Technician **card** sign-on exists (para 250) and the Software-versions tab (para 105) and Location Settings fields (para 253) — but nowhere describes a PIN, an invalid-PIN rejection, an inactivity timeout, a Display Brightness setting, an Audio Volume setting, or a Force Communications action. A targeted check of FBD-100348 found only gate-buzzer volume (a different feature) for "volume." These are standard technician-menu conventions on other Flowbird devices (POS/ETM) but the "never move a capability across device/portal surfaces" rule means that doesn't establish they exist on the GV without a citation. | Added `(needs-spec — ... not detailed in FBD-100654; confirm live)` to the Expected-result of these 5 cases. Behaviour left as-is (plausible, not disputed) — not removed, not invented a fix. Logged **gap-register Q35**. C4104064 (sign-on itself), C4104066 (abandon→idle) and C4104068 (menu navigation) judged low-risk generic UX, not individually reworded, but noted in Q35 for completeness. |

## Everything else — verified clean with citation (no change)

The remaining **86 of 96** cases were checked and their existing Refs found to genuinely support the
claim on primary-source re-read:

- **ABT cEMV Taps (15 of 16 cases, all but C4104013):** FBD-100690 §4.3 (Route Attribute / Location /
  Product pre-read checks, para 974-994), Declined Reason codes 1/2/3/15/20 (para 996-1019), the
  exit/bi-di deny-list-exception behaviour (para 963-972, matches C4104025 near-verbatim), Gate
  Direction → Tap On/Tap Off (para 1062-1066, matches C4104026/4104027), Visa/Mastercard-only /
  Maestro-excluded (para 940-943, matches C4104024). FBD-100658 confirms `paymentType":"ABT"`,
  `revenue:0`, `CardType:"emv"` (matches C4104012).
- **Multi-Use Barcode Validation (19 of 20, all but C4104029/4104030 above):** FBD-100167 confirms
  Scheme ID/format/mode fields (§5.1), the £90 rail location-check fallback (CR105.3, para 532),
  CR105.2 gateline Unique-ID share, CR116 midnight-4am expiry display, the 3-Day Select Start/
  Additional-Dates-offset/End validity rule (para 471-473, 527 — confirms C4104046's underlying claim
  is correct; the case's one worked precondition + a "Data variations" line for the other two dates
  follows this suite's own established convention for data variations, e.g. C4104028, so **no case
  change made** — the earlier Medium finding's "add steps for all 3 dates" suggestion is superseded
  by that convention, not applied).
- **Passback (5 of 5):** FBD-100690 Declined Reason 20 (Passback), FBD-100167 CR105.2.
- **Commissioning & Router (20 of 20):** FBD-100654 confirms HF03 firmware (para 92/105/113),
  Standard/Wide firmware variants (para 97-99), one-wire homeLocation/zoneNo programming (para
  214-220), Location Settings fields (para 253), the ~20-minute self-extract + 3 Android permission
  prompts (para 249, matches C4104053 closely). FBD-100653 confirms the static-WAN-per-lane model,
  SkyLane at `192.168.0.200` with a port-80 NAT rule (para 63-68), and the router admin password
  change-from-blank procedure (para 60) — C4104061 correctly avoids stating the actual password in
  the case text (gherkin-standard's "no hard-coded secrets" rule).
- **Technician Menu (7 of 12, the software/location/comms cluster):** C4104058, C4104069 (Location
  Settings fields, para 253), C4104071 (Software Versions "tab", para 105), C4104072 (Configuration
  Versions, same mechanism), C4104064/4104066/4104068 (card sign-on / abandon / navigate — judged
  low-risk generic UX per Q35, not marked).
- **HMI Screens (15 of 15):** all already carry an honest `(needs-spec — Project-3 screen content)` or
  equivalent marker in their Expected text (or none needed, e.g. the passback/barcode screens cite
  FBD-100167/100690 correctly) — confirmed none silently assert unconfirmed screen content as fact.
- **Resilience (11 of 11):** all already carry `(pending integration)`, `(needs-spec ...)`, `(soft-
  failure)`/`(hard-failure)` markers matching the restructure's explicit "FBD-100348 rows are pending
  integration, don't assert as validated" stance; refs already relocated correctly in the 2026-07-21
  terse pass.
- **Smoke (5 of 5):** cross-references already-grounded functional cases; no new claims of its own.

## Audit result

`python -m system_test_ops audit --suite 30286` after commit: **CLEAN** — 95 cases (96 minus the
condemned C4104038), 0 blocking findings (mojibake 0, preface/preconds/steps/expected structural
checks 0, compound-THEN 0, stray-tags 0). 38 `title-too-long` advisories remain (pre-existing, out of
scope for a grounding pass).

## Gap register

- **Q10** (GV C4104030, TVM barcode print) — was open/needs-checking, now **ANSWERED** and closed:
  the earlier finding was itself wrong (table-extraction error); no case change needed.
- **Q35** (GV Technician Menu PIN/timeout/brightness/volume/force-comms) — logged 2026-07-22, then
  **resolved the same day from existing evidence, before escalation to George** (per his directive to
  exhaust old-suite/UX-doc/deeper-spec sources first — see addendum below).

## Addendum 2026-07-22 — Q35 resolved (old suite + a previously-unchecked GV requirements doc)

George's directive: before bringing a GAP/UNCONFIRMED question to him, exhaust every other source —
the old suite (as happened for Q10 above), any UX documentation, and a broader/deeper spec re-search.

**Old suite 14973 already tests all 5 behaviours**, on real GV hardware, full step tables (pulled via
`TestRailClient.get_cases(42, 14973)`, filtered to Technician-titled cases):

| New-suite case | Old-suite case(s) | Old Refs |
|---|---|---|
| C4104065 (invalid PIN) | C2754383 "Technician - Invalid PIN Entry" | REQ-0050.0, REQ-0050.2 |
| C4104067 (inactivity timeout) | C2754318/C2754319 "Navigation - Auto Sign-Off"/"Page Timeouts", C3251520 "Auto Sign off **" | REQ-0656.0 |
| C4104073 (Display Brightness) | C2754308/C2754309/C2754310, C3251526 "Display Brightness" | REQ-0511.0, REQ-0511.1 |
| C4104074 (Audio Volume) | C2754311, C3251527 "Audio Volume" | REQ-0511.0, REQ-0511.1 |
| C4104075 (Force Comms) | C2754326 "Communications - Force Communications", C3251528 "Force Comms" | REQ-0348.0, REQ-0521.0, REQ-0661.0 |

**A GV-specific requirements doc had not yet been checked**: `GV VCRM Requirements Extract.xlsx`
(`REQS_DIR`, same folder as FBD-100654/FBD-100348). Re-searching it for the old suite's REQ numbers
via `tools/extract_req.py --entry "GV VCRM Requirements Extract.xlsx" --terms ...` confirms each
genuinely applies to GV, with one correction: the old suite's own REQ-0656.0 citation for the
inactivity-timeout cases turned out to be **mis-cited** — REQ-0656.0 ("navigate menu functions using
the touch screen") applies only to HHD/PV in `VCRM (Latest).xlsx`, not GV. A better, GV-scoped
requirement exists for the exact behaviour: **REQ-3129.0/REQ-3129.1** — "As an engineer I need the
device to exit engineering mode after a configurable period of user inactivity ... even if I forget
to sign out." REQ-0050.2, REQ-0511.0/0511.1, and REQ-0348.0 were all confirmed genuinely GV-scoped
as cited (REQ-0050.2's tracker note even says "Include tests for valid and invalid PIN entry
attempts" — a direct instruction to test C4104065's exact scenario).

**Applied**: `proposals/coherence-audit/fixes/gv-technician-menu-q35-resolution.rewrite.json` via
`tools/apply_rewrite.py --project 42 --commit` (dry-run: 5 updated/0 missing/0 skipped, then
committed) against `TESTRAIL_WRITE_SUITE_ID=30286`. Removed the `(needs-spec — ... confirm live)`
markers from all 5 cases' Expected text and replaced Refs with `FBD-100654,REQ-####` (C4104075 also
keeps `FBD-100266`). Re-audit `python -m system_test_ops audit --suite 30286`: **CLEAN**, 95 cases, 0
blocking findings (38 title-too-long advisories, pre-existing, unchanged).

**Not escalated to George** — resolved the same way Q10 was, by re-mining a source that hadn't been
fully searched yet (the GV-specific VCRM extract, distinct from FBD-100654/FBD-100348). Gap register
`gap-register.md` Q35 updated with the full answer + sources.

## Pending-integration scaffolding — should it be reconsidered?

Per the task's instruction to flag (not push) this: nothing in this deep pass changes the
restructure's original stance on the ~57 pending-integration cases in
`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml`. If anything it
reinforces it — the live suite's own `(needs-spec)`/`(pending integration)` markers held up under a
full primary-source re-check (nothing found that would let any of those areas be asserted as
validated). The one thing worth carrying into that scaffolding review: the **Technician Menu**
scaffolding (if any exists there) should get the same `Q35` caveat applied before being considered
for promotion to live, so the same unconfirmed PIN/timeout/brightness/volume/force-comms claims
aren't pushed live without the same marker.
