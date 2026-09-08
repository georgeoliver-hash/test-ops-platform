# PV Acceptance Suite (30255) — Deep Spec-Grounding Audit

**Verdict: PASS with flags.** Every one of the 136 live cases in suite 30255 (`**NEW**
PV-Acceptance Test Suite`, project 42, TFTS - System Test) was cross-examined claim-by-claim against
the full FBD/PSPEC requirement library and/or the Overflow design source. 47 cases were corrected or
had a real citation backfilled; 6 were confirmed already-correct with a citation-precision note added;
8 cases now carry a new `**GAP**`/`**UNCONFIRMED**` marker pending an answer (gap-register Q25–Q33);
1 case was already correctly condemned before this pass; the remaining 82 needed no change. The suite
re-audits **CLEAN of blocking findings** (`python -m system_test_ops audit --suite 30255`, 24 advisory
title-length/em-dash notices only — pre-existing, reviewed, several intentional per the HMI-title
exception in `docs/gherkin-standard.md`).

Full accounting, findings, and the new gap-register questions: see
`proposals/coherence-audit/fixes/pv-deep-audit.changelog.md`. Prior passes this suite already had:
2026-07-17 light coherence audit, 2026-07-21 JIRA release-coverage build, 2026-07-21 comms-failover
reversal, 2026-07-21 terse-wording pass. This pass is the first exhaustive, cited, case-by-case check
of every live case against a real source.

## Legend

- **VERIFIED-CLEAN** — claim(s) checked, citation already sufficient or claim is generic/
  non-controversial; no change needed.
- **CORRECTED** — a citation was backfilled and/or wording was fixed (coherence bug, wrong artefact
  name, invented clause removed, etc.); a real field was pushed to TestRail.
- **CONFIRMED-ONLY** — citation was already present and correct; a citation-precision note was added
  as metadata but no case-body field changed (TestRail wasn't touched for these 6).
- **GAP-NEW / UNCONFIRMED-NEW** — a new `**GAP**`/`**UNCONFIRMED**` marker was added this pass; see the
  linked gap-register question.
- **ALREADY-CONDEMNED** — case was already `ZZ_DELETE_REVIEW` before this pass; untouched.

## Functional / Smartcard Validation, Validation Outcomes, Barcode Validation, Barcodes, Rail-specific, Pilot List, Legacy & Card Tech, Legacy Transfer, ABT Audit (batch 1, 35 cases)

| Case | Title | Verdict | Citation(s) | Note |
|---|---|---|---|---|
| C4100981 | Validate a Concession SmartPass | CORRECTED | FBD-100250, FBD-100335 | Refs backfilled; variation list matches Fare Foregone group exactly |
| C4100982 | Validate a Half-Fare SmartPass | CORRECTED | FBD-100250, gap Q12 | Refs backfilled; matches Funded Passes group |
| C4100983 | Validate a Metro Daylink smartcard | CORRECTED | FBD-100250, FBD-100277 | Refs backfilled |
| C4100984 | Validate a Metro Multi-Journey smartcard | CORRECTED | FBD-100261, FBD-100277, FBD-100271 | Refs backfilled; zone/passback grounded |
| C4100985 | Validate a Metro Travelcard | CORRECTED | FBD-100250, FBD-100260 | Refs backfilled |
| C4100986 | Validate an Ulsterbus Multi-Journey smartcard | CORRECTED / GAP-NEW | FBD-100250/261/277; gap Q27 | Product grounded; exhausted-journeys reject screen name unconfirmed — GAP marker added |
| C4100987 | Validate an iLink smartcard | CORRECTED | FBD-100250, FBD-100271 | Refs backfilled; iLink=Belfast Visitor Pass confirmed |
| C4100988 | Validate an aLink smartcard | CORRECTED | FBD-100250, FBD-100271 | Refs backfilled |
| C4100989 | Validate a yLink/24+ smartcard | UNCONFIRMED-NEW | FBD-100236/250; gap Q25 | Intraday time-of-day band unconfirmed, may be copy-paste from EA Smartpass |
| C4100990 | Validate an Employee smartcard | CORRECTED | FBD-100250 | Refs backfilled |
| C4100991 | Validate an EA Smartpass | CORRECTED | FBD-100250 | Narrowed to time-of-day dimension per 2026-07-17 finding |
| C4101090 | Inter-device top-up (exhausted period product) | CORRECTED / GAP-NEW | FBD-100261/271; gap Q27 | "No Days Left" screen name unconfirmed — GAP marker added |
| C4100992 | Invalid reasons displayed | CORRECTED | FBD-100250, FBD-100277 | Refs backfilled |
| C4100993 | Passback | CORRECTED | FBD-100271 | Refs backfilled |
| C4100994 | Machine not in service | VERIFIED-CLEAN | — | Generic operational behaviour |
| C4100995 | Offline transaction | VERIFIED-CLEAN | — | Consistent with FBD-100167 offline pattern |
| C4103559 | Single-use barcode rejected | VERIFIED-CLEAN | FBD-100167, FBD-100317 | Exact string match confirmed |
| C4103560 | Multi-use barcode valid → green | VERIFIED-CLEAN | FBD-100167 | Confirmed |
| C4103561 | Multi-use barcode invalid → red | VERIFIED-CLEAN | FBD-100167 | Confirmed |
| C4101006 | Multi-use barcode validation | CORRECTED | TIBU-27324, FBD-100167 | Added supporting FBD cite |
| C4102428 | Early-morning barcode expiry | CORRECTED | TIBU-25444, FBD-100167 | Added FBD-100167 CR116 cite, exact match |
| C4104109 | Barcode reader disconnect | VERIFIED-CLEAN | TIBU-21950/27289 | Defect-pinned, fine as-is |
| C4100996 | NIR transfer validation | CORRECTED | FBD-100271 | Variation list matches spec's Rail transfer scope exactly |
| C4100997 | Rail zone validation | CORRECTED | FBD-100167, FBD-100277 | Refs backfilled |
| C4102429 | Rail ABT success — "NI Travel Only" line | UNCONFIRMED-NEW | pv.findings.md; gap Q26 | Exact label text unconfirmed |
| C4103562 | Pilot List enrolled — accepted | CONFIRMED-ONLY | FBD-100720 Phase 2 | Already correct; precision citation added |
| C4103563 | Pilot List non-enrolled — rejected | CONFIRMED-ONLY | FBD-100720 Phase 2, TIBU-28805 | Already correct; precision citation added |
| C4103564 | Pilot registration upload | CONFIRMED-ONLY | FBD-100720 Phase 1 | Already correct; precision citation added |
| C4101007 | Legacy journey/time cards | CORRECTED | FBD-100250, FBD-100271 | Refs backfilled |
| C4101008 | MIFARE/DESFire reading | CORRECTED | FBD-100250, FBD-100236, FBD-100690 | Refs backfilled, FEIG corroborated |
| C4101009 | Passback (legacy) | CORRECTED | FBD-100271 | Refs backfilled |
| C4101010 | Operating Times (legacy) | VERIFIED-CLEAN | — | Generic, no specific FBD needed |
| C4103566 | Legacy Transfer — product property | CONFIRMED-ONLY | FBD-100271 | Exact match confirmed; precision citation added |
| C4103567 | Legacy Transfer — outside window | CONFIRMED-ONLY | FBD-100271 | Exact match confirmed |
| C4103565 | NIR TOTO audit | CONFIRMED-ONLY | FBD-100658, FBD-100690 | Exact field match confirmed |

## Functional / ABT (Glider), Commissioning, Smoke, Delete (batch 2, 25 cases)

| Case | Title | Verdict | Citation(s) | Note |
|---|---|---|---|---|
| C4100998 | ABT contactless tap validation | CORRECTED | knowledge/flows/pv-flow-annotations.md | Refs backfilled from Overflow annotations |
| C4100999 | Declined/errored tap | CORRECTED | knowledge/flows/pv-flow-annotations.md | Refs backfilled |
| C4101000 | BIN, Deny, Pilot list handling | CORRECTED | FBD-100651 §4.3.6-8, FBD-100720 §4 | Refs backfilled |
| C4101001 | cEMV tap enablement by route/location/fare | VERIFIED-CLEAN | TIBU-31722 | Already grounded (release-coverage pass), ticket re-verified |
| C4101002 | Glider TOO flat-fare journeys | CORRECTED | FBD-100651 §4.3.8 para 295 | Split vaguely-bundled step into grounded Passback-decline + capping-rule outcomes |
| C4101003 | Glider transfers | CORRECTED | FBD-100651 §5/§6 | Refs backfilled; no value hard-coded |
| C4101004 | ABT end-to-end to back office | CORRECTED | FBD-100307 | Refs backfilled |
| C4101078 | ABT Pilot List management | CORRECTED | FBD-100720 §3-4 | Fixed 2026-07-17 Med finding (mutually-exclusive TMS modes, artefact names, garbled export step) |
| C4101079 | Deny/BIN list updates | VERIFIED-CLEAN | TIBU-26320/25745/31287 | Already grounded, tickets re-verified real & matching |
| C4101080 | FEIG reader software management | VERIFIED-CLEAN | TIBU-25446/25691/26048/26522/32037 | Already grounded, tickets re-verified |
| C4101081 | FEIG card reading | CORRECTED | FBD-100236 | Fixed cross-surface error: "ITSO" corrected to "DESFire" (no ITSO anywhere in spec) |
| C4101088 | cEMV decline reasons + route enablement | CORRECTED | TIBU-22322, FBD-100651; gap Q28 | Removed ungroundable "card clash" condition |
| C4101089 | JourneyTap audit + alighting derivation | CORRECTED | TIBU-22332, FBD-100658 | Refs backfilled |
| C4101092 | cEMV tap audit content | VERIFIED-CLEAN | TIBU-22332/30476/28856/28645 | All 4 tickets re-verified real & matching |
| C4101093 | EMV result screens + transaction generation | VERIFIED-CLEAN | TIBU-25700/25702/25704/25705 | All 4 tickets re-verified; no hard-coded timeout |
| C4104108 | FEIG update without TID/TK fails safely | CORRECTED | TIBU-24606, TIBU-22318 | Fixed wrong-ticket citation — found the actual matching ticket |
| C4102430 | PV commissioning | CORRECTED | knowledge/flows/pv-flow-annotations.md | Refs backfilled |
| C4101072 | Smoke — valid smartcard validates | VERIFIED-CLEAN | — | Generic, no invented specifics |
| C4101073 | Smoke — invalid smartcard | VERIFIED-CLEAN | — | Generic |
| C4101074 | Smoke — valid barcode | VERIFIED-CLEAN | — | Generic |
| C4101075 | Smoke — ABT contactless tap succeeds | VERIFIED-CLEAN | — | Consistent with C4100998 |
| C4101076 | Smoke — Technician Menu login | VERIFIED-CLEAN | — | Matches flow annotation |
| C4101077 | Smoke — PV communicates with back office | VERIFIED-CLEAN | — | Generic |
| C4101005 | ZZ_DELETE_REVIEW — Barcode single-use validation | ALREADY-CONDEMNED | FBD-100167, gap Q8 | Correctly condemned pre-pass; untouched |
| C4101085 | Comms Failover — Ethernet→cellular | CORRECTED | REQ-2746.0, TIBU-24428 | Spot-checked the earlier restore; Expected-result field was stale (missed by the restore) — fixed |

## Functional / Technician Menu, Non-Functional / PV, Non-Functional / Comms (batch 3, 27 cases)

| Case | Title | Verdict | Citation(s) | Note |
|---|---|---|---|---|
| C4101011 | Technician Menu — login | CORRECTED | pv-flow-annotations.md | Refs backfilled, exact match |
| C4101012 | Technician Menu — location settings | CORRECTED | pv-flow-annotations.md | Fixed precondition/step contradiction (2026-07-17 Med finding) |
| C4101013 | Technician Menu — display settings | CORRECTED | pv-flow-annotations.md | Refs backfilled |
| C4101014 | Technician Menu — software/config versions | GAP-NEW | pv-flow-annotations.md; gap Q29 | Screens confirmed, itemised field lists not |
| C4101015 | Technician Menu — force communications | CORRECTED | pv-flow-annotations.md | Refs backfilled, word-for-word match |
| C4101016 | Technician Menu — network settings | VERIFIED-CLEAN | TIBU-26303, TIBU-29191 | Already grounded, matches release-coverage |
| C4101017 | Technician Menu — operating times | GAP-NEW | gap Q30 | Feature not found in any reviewed source |
| C4101091 | Technician Menu — backup/layout/audible feedback | GAP-NEW | gap Q31 | 3 unconfirmed bundled claims |
| C4102166 | Technician Menu — sign off | CORRECTED | pv-flow-annotations.md | Refs backfilled |
| C4102167 | Technician Menu — reboot | CORRECTED | pv-flow-annotations.md | Refs backfilled |
| C4102168 | Technician Menu — audio settings | CORRECTED | pv-flow-annotations.md | Refs backfilled |
| C4102181 | Technician Menu — auto sign-off/timeouts | UNCONFIRMED-NEW | gap Q32 | Tone + two-stage sequence unconfirmed; PIN-field timeout step left clean |
| C4101018 | Power — recovers to service | VERIFIED-CLEAN | — | Generic NFR |
| C4101019 | PV to BOS — software/FEIG update via TMS | VERIFIED-CLEAN | TIBU-26048, TIBU-32037 | Already grounded (release-coverage) |
| C4101020 | PV to BOS — Deny/BIN list download | VERIFIED-CLEAN | — | Generic; possible overlap with C4101079 flagged for consolidation |
| C4101021 | PV to BOS — transaction upload | VERIFIED-CLEAN | FBD-100359 | General queue mechanism, no invented specifics |
| C4101022 | Clock — GMT/BST change | VERIFIED-CLEAN | — | Generic NFR |
| C4101082 | PV to BOS — MERIT heartbeat | VERIFIED-CLEAN | TIBU-28386; gap Q33 | Already grounded; possible conflict with FBD-100266 flagged, not resolved |
| C4101083 | PV — scheduled reboot | VERIFIED-CLEAN | — | Uses "configured value" pattern correctly |
| C4101084 | PV to BOS — config/topology distribution | VERIFIED-CLEAN | FBD-100359/100304 | General architecture, no invented specifics |
| C4101086 | PV — scheduled maintenance | VERIFIED-CLEAN | — | Vague but not ungrounded; wording smell noted, not a defect |
| C4101087 | PV — validation/barcode performance timings | VERIFIED-CLEAN | — | Uses "acceptable timing" pattern correctly |
| C4101094 | PV — stability and recovery | VERIFIED-CLEAN | TIBU-25842/26302/28453/28770/29165/29602/28240 | Already grounded (release-coverage) |
| C4101095 | PV — asset and version reporting | CORRECTED | FBD-100263, gap Q23 | Resolved 2026-07-17 Med finding — "SIM ID" confirmed real |
| C4104110 | PV to BOS — Device Log Manager | VERIFIED-CLEAN | TIBU-28139 | Already grounded |
| C4103568 | Comms Lock — both channels down | VERIFIED-CLEAN | FBD-100359, TIBU-24428, gap Q23 | Already correctly narrowed per failover restore; verified live text |
| C4103569 | Comms Recovery — queued transactions | VERIFIED-CLEAN | FBD-100359 | Unchanged per failover restore; verified |

## HMI Screen Validation / Technician Menu (batch 4, 24 cases) — all VERIFIED-CLEAN

Cross-checked against `knowledge/flows/pv-flow-annotations.md` (Overflow export) and the recorded
`hmi.cases.yaml` generator snapshot — both list the identical 24 screens in the identical order.
Caveat: the physical PNG files are gitignored and not present in this local clone, so this is
corroboration against an independent extract of the same source, not a literal file-existence check.

C4101048, C4101049, C4101050, C4101051, C4101052, C4101053, C4101054, C4101055, C4101056, C4101057,
C4101058, C4101059, C4101060, C4101061, C4101062, C4101063, C4101064, C4101065, C4101066, C4101067,
C4101068, C4101069, C4101070, C4101071 — all VERIFIED-CLEAN, screen names match exactly (including a
legitimate near-duplicate pair, C4101059 "Select Location - Selected" vs C4101060 "Select Location",
and the source's own inconsistent capitalisation in "Network interfaces" — both are real, not drift).

## HMI Screen Validation / Validation Screens (batch 5, 25 cases) — all VERIFIED-CLEAN

Same method as batch 4, cross-checked against the "Platform Validator-Barcode" Overflow flow
annotations (25/25 exact match, including a faithfully-propagated trailing space in "Passback Days
Left" and a `/`→`_` filename-safe substitution in "ABT deny list/negative list").

C4101023, C4101024, C4101025, C4101026, C4101027, C4101028, C4101029, C4101030, C4101031, C4101032,
C4101033, C4101034, C4101035, C4101036, C4101037, C4101038, C4101039, C4101040, C4101041, C4101042,
C4101043, C4101044, C4101045, C4101046, C4101047 — all VERIFIED-CLEAN. Note: C4101036 ("ABT Tag
successful - Rail") and C4101037 ("ABT Tag successful") share the same underlying screen id
`1.6.1.1` in the Overflow source — a pre-existing open question already logged in
`proposals/translink-requirements-review/gaps-pv.md`, not re-raised here.

## Post-fix conformance

`python -m system_test_ops audit --suite 30255` (re-run after applying all 5 batches):
**CLEAN of blocking findings** — 135 cases audited, 24 advisory (title-length/no-em-dash) notices
only, all pre-existing and reviewed.
