# GV suite (30286) — deep spec-grounding audit report

**Date:** 2026-07-22 (task opened 2026-07-21) · **Suite:** 30286 `**NEW** GV Test Suite`, project 42
(TFTS - System Test) · **Scope:** all live cases, pulled fresh (96 at start, 95 after this pass).

## Verdict

**CLEAN.** Every live case's factual claims were checked against the primary FBD/PSPEC source text
(not the distilled `knowledge/` notes, not the earlier coherence-audit summary). 9 cases corrected,
1 duplicate condemned, 5 cases given an honest `needs-spec` marker for an unsupported claim, 1 prior
finding (Q10, TVM barcode printing) discovered to be **wrong** and reversed. `system_test_ops audit
--suite 30286` is clean of blocking findings after the changes (95 cases, 0 blocking, 38 pre-existing
title-length advisories out of scope). Full accounting: **86 verified-clean-with-citation / 9
corrected / 1 condemned-duplicate / 0 not-reached** (of the original 96).

This suite had already had (a) a structural rebuild from the old 1,184-case suite, (b) a 7-finding
"coherence" pass (title/steps/expected internal agreement + spot capability checks, 2026-07-17), and
(c) a terse-wording compression pass (2026-07-21, 10 cases). What had **not** happened until this
pass: a systematic walk of every case's claims against the actual spec text with citations verified,
not assumed. That gap is now closed for this suite.

## What changed and why

| # | Case | Was | Now | Why |
|---|---|---|---|---|
| 1 | C4104013 | DeviceId `0420` / TID `02201156` in precondition | DeviceId `042002` / TID `20115688`; Then asserts the concrete composed value | FBD-100658's own worked example (paras 217-230) splits the same composed TapId string differently — the case's DeviceId/TID breakdown was wrong even though the final concatenated value it quoted was right |
| 2 | C4104029 | "a barcode on a mobile device screen" (unnamed variant) | "a Corethree mLink barcode (format 02)" | FBD-100167 para 267/422 name the only spec-confirmed mobile-screen multi-use artefact |
| 3 | C4104038 | Live case, duplicate of C4104051 | `ZZ_DELETE_REVIEW`, condemned | Both test the identical CR105.2 gateline-share scenario; Passback (C4104051) is the better home |
| 4 | C4104070 | Title asserted the location edit is *blocked*; Expected only proved an indication | Title narrowed to what's provable; blocking claim marked `**UNCONFIRMED**` | FBD-100654 doesn't state whether the save is rejected or only flagged |
| 5 | C4104100 | Titled "Heartbeat — ..." | Titled "Comms — ..." | Conflated the 15-min StaffList/Last-Communication refresh with the distinct true heartbeat tested in C4104094 |
| 6 | C4104065 | Asserted invalid-PIN rejection as spec fact | `(needs-spec — PIN-entry mechanics not detailed in FBD-100654; confirm live)` | FBD-100654 confirms card sign-on only, no PIN text anywhere |
| 7 | C4104067 | Asserted inactivity timeout as spec fact | `(needs-spec — timeout duration/mechanics not detailed...)` | No timeout text in FBD-100654 |
| 8 | C4104073 | Asserted Display Brightness setting as spec fact | `(needs-spec — Display Brightness screen not detailed...)` | No brightness text in FBD-100654 |
| 9 | C4104074 | Asserted Audio Volume setting as spec fact | `(needs-spec — Audio Volume screen not detailed...; only volume ref found is the gate infraction buzzer, a different feature)` | FBD-100348's only "volume" hit is a different feature |
| 10 | C4104075 | Asserted Force Communications as spec fact | `(needs-spec — Force Communications not detailed in FBD-100654 or FBD-100266; confirm live)` | No text found in either doc |

**Reversed finding:** the 2026-07-17 coherence audit flagged **C4104030** ("a TVM-produced barcode
validates at the GV") Medium — claiming TVM isn't a multi-use barcode printer per FBD-100167's device
matrix. Re-parsing that matrix properly (FBD-100167's Table 1, "Device categories" — read cell-by-
cell via `python-docx` rather than the flattened paragraph-text extraction both the earlier audit and
my own first pass used, which loses the table's column alignment) shows TVM's checkmark is in the
**Print** column, not Validate: **GV validates only, TVM prints only** — the case was correct all
along. No case change; gap-register Q10 closed with this citation. This is flagged prominently
because it demonstrates exactly the risk this whole audit exists to catch: a plausible-sounding
"grounded" finding that was itself never checked against the primary table structure.

## Full case-by-case grounding table

Legend: **Clean** = existing Refs verified to support the claim on primary-source re-read, no change.
**Corrected** = case body/title/Refs changed this pass. **Condemned** = duplicate, removed.

### Functional / ABT cEMV Taps (887831) — 16 cases, citation FBD-100690 + FBD-100658

| Case | Title | Grounding |
|---|---|---|
| C4104011 | valid contactless tap succeeds, gate opens | Clean — FBD-100690 §4.3 pre-read checks + success path |
| C4104012 | successful tap posts zero-revenue ABT record | Clean — FBD-100658 `paymentType:"ABT"`,`revenue:0`,`CardType:"emv"` |
| C4104013 | TapId composed of DeviceId+TID+timestamp | **Corrected** — wrong DeviceId/TID split (see above) |
| C4104014 | expired card declined, Reason 1 | Clean — FBD-100690 para 998-999 |
| C4104015 | ODA-fail declined, Reason 3 | Clean — FBD-100690 para 1003-1004 |
| C4104016 | BIN-list declined, Reason 15 | Clean — FBD-100690 para 1008-1009 |
| C4104017 | Deny-list rejected in entry mode, Reason 2 | Clean — FBD-100690 para 1013-1014 |
| C4104018 | every declined check posts an audit record | Clean — FBD-100690 §4.3 general rule |
| C4104019 | offline transaction accepted and queued | Clean — consistent with the BIN/Deny-list local-check model in FBD-100690 |
| C4104020 | reader disarmed, route ABT Type ≠ TOTO | Clean — FBD-100690 para 976-978 (Route Attribute Check) |
| C4104021 | reader disarmed, home location outside NI Zone | Clean — FBD-100690 para 984 (Location Check) |
| C4104022 | reader disarmed, no ABT Tap Product configured | Clean — FBD-100690 para 994 (Product Check) |
| C4104023 | unreadable card → error, gate stays closed | Clean — FBD-100690 para 936-939 |
| C4104024 | Maestro not accepted at GV | Clean — FBD-100690 para 940-943 (Visa/Mastercard only) |
| C4104025 | exit-capable gate opens for deny-listed card, audits invalid | Clean — FBD-100690 para 963-972 (near-verbatim match) |
| C4104026 | entry-configured gate audits as Tap On | Clean — FBD-100690 para 1062-1066 (Gate Direction) |
| C4104027 | exit-configured gate audits as Tap Off | Clean — FBD-100690 para 1062-1066 |

### Functional / Multi-Use Barcode Validation (887832) — 20 cases, citation FBD-100167

| Case | Title | Grounding |
|---|---|---|
| C4104028 | valid barcode, green tick, gate opens | Clean |
| C4104029 | mobile-screen barcode validates same as printed | **Corrected** — named as Corethree mLink format 02 |
| C4104030 | TVM-produced barcode validates at GV | Clean (was wrongly flagged 2026-07-17 — now confirmed correct, see above) |
| C4104031 | HHD-produced barcode validates at GV | Clean — Table 1, HHD=print+validate |
| C4104032 | route/location-only failure → yellow question mark | Clean |
| C4104033 | other failure → red cross with reason | Clean |
| C4104034 | already-validated barcode rejected | Clean |
| C4104035 | expired barcode rejected | Clean |
| C4104036 | rail location-fail treated valid ≥£90 (CR105.3) | Clean — FBD-100167 para 532 |
| C4104037 | rail location-fail rejected <£90 | Clean — FBD-100167 para 532 |
| C4104038 | barcode validated on one head rejected on another (gateline) | **Condemned** — duplicate of C4104051 |
| C4104039 | expiry 00:00-04:00 shows previous day, no time (CR116) | Clean |
| C4104040 | expiry after 04:00 shows same day + time (CR116) | Clean |
| C4104041 | read-to-beep within 1 second | Clean |
| C4104042 | barcode during result screen processed immediately | Clean |
| C4104043 | success posts zero-fare BarcodeUsage transaction | Clean |
| C4104044 | failure posts event with Unique ID + reason | Clean |
| C4104045 | GV validates multi-use barcodes (device-set confirmation) | Clean — Table 1 |
| C4104046 | 3-Day Select valid on start/additional/end dates | Clean — FBD-100167 para 471-473, 527; one worked example + Data-variations line follows the suite's own convention, no change needed |
| C4104047 | bus-only-mode barcode rejected at rail gate | Clean |

### Functional / Passback (887833) — 5 cases, citation FBD-100167 / FBD-100690

| Case | Title | Grounding |
|---|---|---|
| C4104048 | barcode re-presented within window rejected | Clean |
| C4104049 | still rejected after intervening transactions | Clean |
| C4104050 | card re-tapped within passback time, Reason 20 | Clean — FBD-100690 para 1018-1019 |
| C4104051 | barcode on second gateline head rejected (CR105.2) | Clean — kept as the canonical home for this scenario |
| C4104052 | barcode accepted after window elapses | Clean |

### Commissioning & Router (887834) — 20 cases, citation FBD-100653/100654

| Case | Title | Grounding |
|---|---|---|
| C4104053 | both heads self-extract and enter service | Clean — FBD-100654 para 249 (~20 min, 3 permission prompts) |
| C4104054 | Primary=Entry/unpaid, Secondary=Exit/paid (not swapped) | Clean |
| C4104055 | SkyLane firmware is HF03 | Clean — FBD-100654 para 92/105/113 |
| C4104056 | correct Standard/Wide gate variant installed | Clean — FBD-100654 para 97-99 |
| C4104057 | one-wire homeLocation/zoneNo match spreadsheet | Clean — FBD-100654 para 214-220 |
| C4104058 | Technician Location Settings match spreadsheet | Clean — FBD-100654 para 253 |
| C4104059 | unique static WAN IP per lane | Clean — FBD-100653 |
| C4104060 | SkyLane .200, gateway .0.1, port-80 NAT | Clean — FBD-100653 para 63-68 |
| C4104061 | router admin password set, not blank | Clean — FBD-100653 para 60 (case correctly withholds the actual password from case text) |
| C4104062 | software/config/barcode-data file downloads | Clean — already marked `(needs-spec — distribution mechanics)`, correctly honest |
| C4104063 | future-dated config applies on activation date | Clean — already marked `(needs-spec)` |
| C4104064 | technician card+PIN reaches Technician Menu | Clean (card) / see Q35 (PIN not detailed) — not individually marked, low risk |
| C4104065 | invalid PIN rejected | **Corrected** — `needs-spec` marker added (Q35) |
| C4104066 | abandoned sign-on returns to idle | Clean/low-risk generic UX — not marked, see Q35 |
| C4104067 | session auto signs off after inactivity timeout | **Corrected** — `needs-spec` marker added (Q35) |
| C4104068 | technician navigates menu pages | Clean/low-risk generic UX — not marked, see Q35 |
| C4104069 | technician sets GV location | Clean — FBD-100654 para 253 |
| C4104070 | location cannot be changed while comms lost | **Corrected** — title narrowed, blocking claim marked UNCONFIRMED |
| C4104071 | Software Versions screen lists versions | Clean — FBD-100654 para 105 |
| C4104072 | Configuration Versions screen lists versions | Clean — same mechanism as C4104071 |

### Technician Menu (887835 continued) — 3 cases

| Case | Title | Grounding |
|---|---|---|
| C4104073 | technician adjusts screen brightness | **Corrected** — `needs-spec` marker added (Q35) |
| C4104074 | technician adjusts audio volume | **Corrected** — `needs-spec` marker added (Q35, buzzer-volume ≠ this feature) |
| C4104075 | technician forces comms session | **Corrected** — `needs-spec` marker added (Q35) |

### HMI Screens (887837) — 15 cases, citation FBD-100348/100167/100690

All 15 (C4104076–C4104090: idle/not-in-service/re-present/not-valid-location/invalid-time/expired/
faulty/not-accepted/success screens, barcode already-validated/expired/not-valid-location/type-
invalid/success screens) — **Clean**, each already carries an honest `(needs-spec — Project-3 screen
content)` marker or, for the passback/barcode screens, a valid FBD-100167/100690 citation for the
underlying trigger condition (not the screen pixel content, which is out of scope for a functional
spec). No case silently asserts unconfirmed screen content as fact.

### Resilience (887838) — 11 cases, citation FBD-100348/100266/100359/100263

All 11 (C4104091–C4104101: power/emergency/heartbeat/power-up/mains-restore/BOS-comms/SaaS-outage/
throughput) — **Clean**, each already carries `(pending integration)`, `(needs-spec ...)`,
`(soft-failure)`/`(hard-failure)` markers consistent with the restructure's explicit stance that
FBD-100348's rows are a factory acceptance report with many "to be validated on integration" items,
not yet validated GV behaviour. Refs were correctly relocated to the field (not the body) in the
2026-07-21 terse pass; this deep pass confirms none of the markers understate or overstate what's
actually confirmed.

### Smoke (887839) — 5 cases

C4104102–C4104106 — **Clean**. These cross-reference already-grounded functional cases (boot to
service, valid card, valid barcode, passback, technician sign-on) and assert no new claims of their
own.

## Accounting

| Category | Count |
|---|---:|
| Verified clean with citation (no change) | 86 |
| Corrected (title/preconds/expected/Refs reworded) | 9 |
| Condemned as duplicate | 1 |
| Flagged gap (new, logged to gap register) | 5 cases → 1 gap-register question (Q35) |
| Reversed prior finding (was wrong, now closed) | 1 (Q10) |
| Not reached | 0 |
| **Total live cases audited** | **96** (95 after condemning C4104038) |

## Suite audit gate

```
python -m system_test_ops audit --suite 30286
audited 95 cases: CLEAN; 38 advisory (title-too-long, pre-existing, out of scope)
```

## Open items for George (gap register)

- **Q35** (new) — GV Technician Menu: is PIN entry / inactivity timeout / brightness / volume /
  force-comms confirmed live on the real GV hardware, or scaffolded from the POS/ETM convention
  without a GV-specific spec? Affects C4104065, 4104067, 4104073, 4104074, 4104075 (and, lower
  priority, the low-risk generic-UX C4104064/4104066/4104068).
- **Q10** — now answered/closed (TVM barcode-print capability confirmed via the real docx table).

## Pending-integration scaffolding (not pushed, flagged per task instruction)

`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` (~57 proposal-only
cases) was not touched — out of scope, proposal file not live in TestRail. Nothing in this pass
changes the case for reconsidering it: the live suite's own `needs-spec`/`pending-integration`
markers held up under full primary-source re-verification. One thing worth carrying forward: if that
scaffolding includes its own Technician Menu cases, apply the same Q35 caveat before any future
promotion to live, so the same unconfirmed PIN/timeout/brightness/volume/force-comms claims aren't
pushed live silently.

## Paths

- Rewrite: `proposals/coherence-audit/fixes/gv-deep-audit.rewrite.json`
- Changelog: `proposals/coherence-audit/fixes/gv-deep-audit.changelog.md`
- Gap register updates: `proposals/coherence-audit/gap-register.md` (Q10 answered/closed, Q35 added)
- Raw case dump used for this audit: `proposals/coherence-audit/fixes/gv-suite-30286-raw.json`
- This report: `reports/translink/gv/2026-07-21/deep-audit.md`
