# PV Acceptance Suite (30255) — deep, case-by-case spec-grounding audit

Date: 2026-07-21/22. Mandate: George's directive to do "the real thing this tool exists for" —
cross-examine **every** live case in a suite against the actual FBD/PSPEC source documents (not a
lighter coherence/title-agreement pass), fold in the terse-wording standard while touching anything,
and report exactly what was and wasn't reached. Scope: suite **30255** (`**NEW** PV-Acceptance Test
Suite`, project 42, device = Platform Validator) only. No other suite touched.

## What existed before this pass

- **2026-07-17** coherence-audit (`proposals/coherence-audit/pv.findings.md`): a *light* pass —
  title/steps/expected internal agreement + spot capability checks against `knowledge/` notes. Found
  9 issues out of 133 cases. Not an exhaustive per-claim citation check.
- **2026-07-21** JIRA release-coverage build (`proposals/pv-release-coverage/`): grounded a subset of
  cases against specific TL Validators v5.0.0/5.0.1/5.0.3 fix-version tickets — scoped to those
  tickets, not every case.
- **2026-07-21** comms-failover reversal (`proposals/coherence-audit/fixes/pv-failover-restore.*`):
  resolved a real spec/live-system conflict on PV comms failover (gap Q9 → Q23).
- **2026-07-21** terse-wording pass (`proposals/coherence-audit/fixes/pv-terse-rewrite.*`): confirmed
  135/136 cases already clean of inline-citation/bloat; fixed the one remaining case.
- **What had NOT happened**: a systematic walk of every live case verifying every claim against a
  cited source. That is this pass.

## Method

1. Pulled the suite fresh: `python -m system_test_ops cases --project 42 --suite 30255` → **136
   cases** (135 live + 1 already-condemned, `C4101005`, superseded/`ZZ_DELETE_REVIEW`).
2. Pulled full raw case bodies via `TestRailClient.get_cases(42, 30255)` (title, refs,
   `custom_preface`, `custom_preconds`, `custom_steps_seperated`, `custom_expected`).
3. Split the 136 cases into 5 batches by section and dispatched 5 independent audit passes (each
   read `CLAUDE.md`, `docs/gherkin-standard.md`, `docs/test-practices.md`,
   `proposals/coherence-audit/pv.findings.md`, `proposals/coherence-audit/gap-register.md` in full
   first):
   - **Batch 1** (35 cases) — Smartcard Validation, Validation Outcomes, Barcode Validation,
     Barcodes, Rail-specific, Pilot List, Legacy & Card Tech, Legacy Transfer, ABT Audit.
   - **Batch 2** (25 cases) — ABT (Glider), Commissioning, Smoke, Delete (incl. `C4101005`,
     `C4101085`).
   - **Batch 3** (27 cases) — Technician Menu (functional), Non-Functional/PV, Non-Functional/Comms.
   - **Batch 4** (24 cases) — HMI Screen Validation / Technician Menu.
   - **Batch 5** (25 cases) — HMI Screen Validation / Validation Screens.
4. Functional batches (1–3) ground each claim via `tools/extract_req.py` against the full local FBD
   library (`REQS_DIR`), cross-checking `knowledge/translink/specs/*.md` cited-pointer notes against
   the *full* document text (not trusting the distilled note alone), plus Jira cross-checks (via the
   Atlassian MCP) on every cited TIBU ticket. HMI batches (4–5) ground each screen-validation case
   against the Overflow design source — the actual exported screenshot filenames where present, and
   (since the PNGs are gitignored and not present in this clone) the independently-generated
   `knowledge/flows/pv-flow-annotations.md` extract of the same Overflow JSON as a cross-check.
5. All 5 batches wrote a `pv-deep-audit-batchN.rewrite.json` (only cases needing a change) plus a
   full per-case verdict table (`VERIFIED-CLEAN` / `CORRECTED` / `GAP-NEW` / `UNCONFIRMED-NEW` /
   `GAP-EXISTING` / `VERIFIED-CLEAN-ALREADY-CONDEMNED`). No case in any batch was silently skipped.
6. Applied all 5 files via `tools/apply_rewrite.py ... --commit` (dry-run first, sanity-checked
   content) → **47 cases updated**, 6 no-op (already-correct citation, recorded as confirmation
   metadata only, no field to push), 0 missing.
7. Re-ran `python -m system_test_ops audit --suite 30255` → **CLEAN of blocking findings** (135
   cases audited; 24 advisory title-length/em-dash notices only, pre-existing and reviewed —
   several are HMI cases whose titles deliberately mirror exact UI screen names, per the standard's
   documented exception).
8. Appended 9 new questions (Q25–Q33) to `proposals/coherence-audit/gap-register.md` — consolidated
   and renumbered centrally (the parallel batches drafted, but did not append, their own questions,
   to avoid Q-number collisions).

## Results — full accounting

**Total live cases: 136** (135 active + 1 already condemned before this pass).

| Category | Count | Notes |
|---|---:|---|
| Verified-clean, citation already sufficient or claim is generic/uncontroversial — **no change** | 82 | Mostly the 49 HMI screen-validation cases (both batches 100% match against the Overflow annotation extract), the 6 Smoke cases, and a spread of Functional cases whose claims needed no grounding (e.g. generic NFR behaviour) or were already correctly cited from the release-coverage/failover passes and held up under re-verification. |
| Corrected / citation added or wording fixed (real field pushed) | 47 | Refs backfilled with precise paragraph-level citations (the majority), plus genuine wording corrections (coherence bugs, garbled artefact names, invented clauses removed) — see "Significant findings" below. |
| Already correctly cited — confirmed only, no field to push | 6 | `C4103562`, `C4103563`, `C4103564`, `C4103566`, `C4103567`, `C4103565` — Refs already present and verified against the full FBD-100720/100271/100658/100690 text; added citation-precision metadata only (no case-body change needed). |
| Flagged **GAP** or **UNCONFIRMED** (new, this pass) | 8 cases / 9 questions | `C4100989`, `C4102429`, `C4100986`, `C4101090`, `C4101088` (removed an ungroundable clause), `C4101014`, `C4101017`, `C4101091`, `C4102181` — see gap-register **Q25–Q33**. |
| Already condemned, no work (superseded) | 1 | `C4101005` — correctly `ZZ_DELETE_REVIEW`, superseded by `C4103559` per gap Q8. Untouched. |
| **Not reached** | **0** | Every one of the 136 cases was cross-examined; none were silently skipped. |

47 + 6 + 1 + 82 = 136. Audit tool re-run after applying: **CLEAN of blocking findings.**

## Significant findings (a representative sample, not the full list — see the rewrite JSON files and gap-register Q25–Q33 for everything)

1. **`C4101078` "ABT Pilot List management"** — resolved the 2026-07-17 Med finding for real: FBD-100720
   confirms `Enable Registration Mode` and `Enable Pilot List` are **mutually exclusive** TMS dataset
   settings — the old case claimed both applied at once, which is impossible. Fixed the artefact name
   (binary `pilotlist.dat` into the `Pilot List File` field, not a "pilotlist.zip"), and removed a
   garbled export step (the CSV↔binary round-trip is a back-office **Pilot List Converter** tool step,
   not a device/TMS action; the thing that *does* zip-upload to CloudFare Device Logging is the
   *registration* file, a separate flow this case no longer conflates).
2. **`C4101012` "Technician Menu — location settings"** — fixed a genuine self-contradiction: the
   precondition asserted "back-office comms available" while step 3 exercised the comms-*unavailable*
   path. Reworded the precondition to be comms-neutral.
3. **`C4101095` "PV — asset and version reporting"** — the 2026-07-17 pass flagged "SIM ID" as
   possibly invented (PV modelled Ethernet-only elsewhere). This pass found "SIM ID" as a **literal
   named field** in FBD-100263 (paras 187/327/403), and gap-register Q23 already confirms real
   cellular/SIM hardware exists — the case was correct all along; grounded with Refs rather than
   left flagged.
4. **`C4101081` "FEIG card reading"** — cross-surface terminology error: the case called the
   smartcard format "ITSO". Translink's own DESFire card-format spec (FBD-100236) never mentions
   ITSO anywhere. Corrected throughout to "DESFire smartcard".
5. **`C4101088` "cEMV decline reasons"** — removed an ungroundable "card clash" decline condition
   (not in TIBU-22322's canonical 7-condition story, FBD-100651, or FBD-100658) rather than asserting
   it as real; also confirmed (via the full Overflow Technician Menu annotation list, batch 3's
   cross-check) that no cEMV enable/disable *toggle* exists in the Technician Menu, closing the
   2026-07-17 Low finding.
6. **`C4104108` "FEIG update without TID/TK fails safely"** — the existing Refs cited only
   `TIBU-22318` (a general background story). Found the actual matching ticket, `TIBU-24606` (an
   Xray Test issue whose title is an exact match), and added it as the primary citation — a
   wrong-ticket citation, not a fabricated one, but still a defect the earlier pass missed by not
   reading the cited ticket closely enough.
7. **`C4101085` "Comms Failover"** — spot-checking the earlier same-day failover restore found the
   restore had updated title/preface/preconditions/steps but **left the top-level Expected-result
   summary field stale** (pre-restore wording, no mention of the 812 event or fail-back). Corrected
   the Expected field only.
8. **`C4100986`/`C4101090`** — both independently asserted a plausible-but-unconfirmed "exhausted
   product" reject-screen name ("No Journeys Left" / "No Days Left"), neither of which appears in the
   enumerated approved-screen set. Rather than pick one and silently drop the other, both were left
   grounded everywhere else and given the same terse `**GAP**` marker on the screen-name wording only,
   folded into one gap-register question (Q27) since they may be the same underlying unknown.
9. **HMI batches (49 cases total)** — 100% verified against the Overflow annotation source; every
   screen name in every case (title/preface/preconditions) matches exactly, including faithfully
   propagated design quirks (a trailing space in "Passback Days Left", a `/`→`_` filename-safe
   substitution in "ABT deny list/negative list", inconsistent capitalisation in "Network interfaces")
   — confirmed these are genuine copies of the real export names, not drift. **Caveat**: the actual
   PNG files are gitignored and not present in this local clone, so the check is corroboration against
   an independently-generated extract of the same source JSON, not a literal file-existence check —
   flagged for anyone with the original export to do a final `Get-ChildItem` diff.

## New gap-register questions (Q25–Q33)

Full text in `proposals/coherence-audit/gap-register.md`. Summary:
- **Q25** — `C4100989` yLink/24+: genuine time-of-day band, or copy-paste from EA Smartpass?
- **Q26** — `C4102429`: exact "Northern Ireland Travel Only" label text on the rail ABT success screen.
- **Q27** — `C4100986`/`C4101090`: exact exhausted-product reject-screen name.
- **Q28** — `C4101088`: does a "card clash" cEMV decline condition exist?
- **Q29** — `C4101014`: exact itemised Software/Configuration-Version field lists.
- **Q30** — `C4101017`: does a PV Technician Menu "Operating Times" feature exist at all?
- **Q31** — `C4101091`: do backup/mirroring, background-colour, and card-presented-tone Technician
  Menu features exist?
- **Q32** — `C4102181`: exact auto-sign-off timeout mechanics/tone.
- **Q33** — `C4101082` "MERIT 24-hour heartbeat" (TIBU-28386) vs FBD-100266's fixed 15-minute
  CloudFare StaffList heartbeat — same mechanism or a real conflict? (Informational — case left
  as-is, flagged rather than silently reconciled.)

## Loose ends raised, not gaps requiring an answer

- `proposals/pv-release-coverage/pv-release-2.rewrite.json` still contains a stale REFS-only note on
  `C4103568` pre-dating the Q23 failover narrowing. The **live case itself is correct** (verified
  against the applied `pv-failover-restore` wording) — this is just an orphaned proposal-file
  artefact, not a suite defect. No action taken (out of scope — proposal files aren't suite state).
- Possible case overlap between `C4101020` ("PV to BOS — Deny/BIN list download") and `C4101079`
  ("Glider — Deny/BIN list updates") — flagged for a future consolidation pass per
  `docs/test-practices.md`'s fold-don't-duplicate rubric; not resolved in this pass (grounding-only
  scope, not a restructure).

## Files

- `proposals/coherence-audit/fixes/pv-deep-audit-batch1.rewrite.json` … `-batch5.rewrite.json` — the
  applied rewrite proposals (28 + 13 + 12 + 0 + 0 = 53 entries; 47 pushed real field changes, 6
  confirmation-only).
- `proposals/coherence-audit/gap-register.md` — Q25–Q33 appended.
- `reports/translink/pv/2026-07-21/deep-audit.md` — the full 136-row grounding-status table.

## 2026-07-22 addendum — gap-resolution pass (Q24–Q33 exhausted against existing evidence before escalation)

Per George's directive to try hard to close gap-register questions from **existing evidence** (old
suite 10047, `knowledge/flows/pv-flow-annotations.md`, and a broader spec/Jira re-search) before
putting them to him, all 9 PV deep-audit questions (Q25–Q33) plus the carried-over release-coverage
question Q24 (TIBU-30923) were re-investigated. **All 10 were resolved from existing sources — none
needed escalation.**

**Method:** (1) pulled suite 10047 in full (1,144 cases) and keyword-swept it (yLink/24+, "No Journeys
Left"/"No Days Left", card clash, Software/Configuration Versions, Operating Times, backup/mirror,
background colour, audible feedback, auto sign-off/timeouts, MERIT/heartbeat); (2) re-read
`knowledge/flows/pv-flow-annotations.md` (the Overflow UX extract) end to end for the same terms; (3)
re-read FBD-100236 and FBD-100266 in full (not the distilled `knowledge/` notes) for the specific
disputed claims; (4) pulled TIBU-30923 and TIBU-28386 **in full** (description + every comment, not
just the summary/title) via the Atlassian Rovo MCP.

**Resolutions (full text in gap-register.md):**
- **Q24** (TIBU-30923, config+software same-distribution conflict) — the ticket's own QA comment
  (Thomas James, 2026-05-14, "QA PASSED" on PV v1.1.1284.24210) confirms the fix for the **PV** is
  "apply both in one distribution"; the ticket stays open only pending the equivalent **GV** check —
  a GV-scope loose end, not a PV one. No live case existed to reground; flagged as authorable.
- **Q25** (C4100989 yLink/24+ time-of-day) — no time band exists; FBD-100236 para 328 confirms
  date-based (concessionary-period) expiry only, and the old suite's exhaustive yLink coverage has
  zero time-of-day cases (unlike the genuinely time-banded EA Pupil Smartpass/EA Bus FE family).
  Reworded to date-based expiry via the confirmed `1.3.9 Product Expired` screen.
- **Q26** (C4102429 "Northern Ireland Travel Only") — confirmed verbatim in
  `pv-flow-annotations.md`'s Platform Validator-Barcode flow annotation. Marker removed.
- **Q27** (C4100986/C4101090 exhausted-product screens) — both `1.3.11 No Journeys Left` and `1.3.15
  No Days Left` are real, distinct screens per the Overflow screen list; old-suite product-type
  pattern (Multi-Journey → Journeys, Daylink/Travelcard → Days) confirms each case already has the
  right screen. No wording change; markers removed.
- **Q28** (C4101088 card clash) — confirmed as a genuine PV decline condition via the Overflow
  "Platform Validator" flow annotation for screen `1.3.3 Invalid Card` (lists "Card Clash" as 1 of 8
  named causes), independent of TIBU-22322/FBD-100651's silence on it. Restored to the case (also
  fixed a pre-existing inconsistency where the top-level Expected field still asserted it while the
  precondition list had dropped it).
- **Q29** (C4101014 version field lists) — exact fields recovered from old-suite C2667038/C2667047
  (REQ-0513.0): Software Versions = OS(Internal)/BSP/EBoot/Configuration Version/
  DM.applicationSoftwareFile/DM.operatingSystemSoftwareFile/Smartcard Reader Firmware+Application
  Version; Configuration Versions = Configuration Version/DM.furthestAlightingFile/TD.Product/
  TD.Topology/Staff List/Action List. Case corrected to the exact wording.
- **Q30** (C4101017 Operating Times) — confirmed real via old-suite C2224516 (REQ-0594.0); mechanism
  on the old build is a config-file edit (`States.json`), not a Technician Menu screen — existence
  gap closed, mechanism nuance noted instead.
- **Q31** (C4101091 backup/layout/audible) — all three confirmed real: data mirroring (REQ-1685.0/
  .3, old-suite C2224530/C2668492, config-file mechanism), background colour (REQ-0796.0, old-suite
  C2224529/C2668256, config-file mechanism), card-presented tone (REQ-1687.0, old-suite
  C3275577/C3275969, approving/declining tone on valid/invalid presentation).
- **Q32** (C4102181 auto sign-off/timeouts) — exact two-stage 60s/60s mechanics plus tone confirmed
  via old-suite C2667020/C2667023 (REQ-0656.0): sub-menu idle 60s → Technician Menu home; home-screen
  idle a further 60s → auto sign-off with tone, audited in CloudFare.
- **Q33** (C4101082 MERIT heartbeat vs FBD-100266) — **not a conflict**. FBD-100266 (full read) is
  entirely CloudFare/StaffList-scoped with zero MERIT mentions; TIBU-28386's full description
  describes an unrelated mechanism (a silent zero-value preset-product paper transaction to MERIT,
  triggered on in-service transitions + a 24h timer). Two genuinely distinct mechanisms to two
  different back-office systems — case already correctly grounded, FBD-100266 added to Refs with an
  explanatory note so it isn't re-flagged as a conflict later.

**Suite changes applied:** all 10 corrections pushed to suite 30255 via
`tools/apply_rewrite.py --commit` (dry-run verified first): `C4100989`, `C4102429`, `C4100986`,
`C4101090`, `C4101088`, `C4101014`, `C4101017`, `C4101091`, `C4102181`, `C4101082`. Re-ran
`python -m system_test_ops audit --suite 30255` afterwards: **CLEAN of blocking findings** (135 cases,
same 24 pre-existing advisory title notices, 0 new).

**Escalated to George: none.** All 9 PV deep-audit questions plus the carried-over TIBU-30923 question
were resolved from old-suite 10047, the Overflow UX annotations, and full-text spec/Jira re-reads —
no PV gap-register question from this pass required his input.
