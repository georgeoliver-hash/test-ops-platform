# PV coverage audit — TIBU fixVersions "TL Validators v5.0.0" / "v5.0.1" / "v5.0.3"

**Target suite:** 30255 (`**NEW** PV-Acceptance Test Suite`, project 42 `TFTS - System Test`).
**Date:** 2026-07-21. **Verdict: mostly covered going in; 12 EDITs + 3 ADDs landed this session to
close the gaps found; audit CLEAN of blocking findings after push.**

Baselines (read-only, deterministic):
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/cases.json` / `.md` — live PV
  suite state (136 cases after this session's push; 134 live, 2 pre-existing `ZZ_DELETE_REVIEW`
  condemned earlier today per `proposals/coherence-audit/fixes/pv.changelog.md`).
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/run-health.json` / `.md` — see
  Run-health section below.
- `reports/tfts-system-test/aa-platform-validator-acceptance-test/2026-07-21/cases.json` / `.md` —
  **old suite 10047 baseline**, pulled per George's mid-task instruction, used to cross-check every
  candidate "Missing" item before authoring anything new.
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/jira-scope-summary.json` — the
  55 JIRA issues in scope, normalised from the raw JQL result (208K chars, over the tool's token cap
  — parsed with the venv Python per the documented gotcha, not dumped raw into context).
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/alignment-audit.md` — the
  post-push conformance audit (CLEAN, 0 blocking, 23 advisory).

## JIRA scope pull

`project = TIBU AND fixVersion in ("TL Validators v5.0.0", "TL Validators v5.0.1", "TL Validators
v5.0.3") ORDER BY fixVersion, issuetype, key` against cloudId `flowbird.atlassian.net`. All three
fixVersion names resolved exactly (no variant needed). **55 issues** returned, no pagination:

| fixVersion | Issues |
|---|---|
| TL Validators v5.0.0 | 53 (incl. 4 that also carry a second fixVersion: TIBU-30923 also v6.0.0; TIBU-24260/25444/26053/26054 also v3.1.3) |
| TL Validators v5.0.1 | 1 — TIBU-31722 |
| TL Validators v5.0.3 | 1 — TIBU-32037 |

Excluded from per-issue classification (containers/artifacts, not testable behaviour): **TIBU-21910**
(epic, "Release 5.0.0 TL Validators"), **TIBU-24660** (Test Execution — a QA run record, not a
requirement/bug). **TIBU-22305** (epic, "Glider Tap On Only for PV") and **TIBU-28094** (epic, "NIR
TOTO on PV") are covered via their child stories (noted, not double-counted).

## Old-suite cross-check (per George's mid-task instruction)

Suite 30255 was built via an aggressive ~1,144→~115 consolidation
(`proposals/pv-suite-restructure/build-complete.md`), so before authoring anything "Missing", every
candidate was searched against the **old suite (10047, read-only, 1,144 cases)** by title/preface/
steps keyword match. This changed the outcome materially — **6 of the 9 "Missing" candidates turned
out to already have real, populated cases in 10047** that were never migrated forward:

| JIRA issue | Old-suite case (10047) | Disposition |
|---|---|---|
| TIBU-22318 (TID/TK from device group) | **C4073875** "FEIG Update Fails if Device Group Lacks TID/TK, but PV App Software Still Updates" (full GIVEN/WHEN/THEN) | Migrated as new case **C4104108** (content taken from C4073875, not invented) |
| TIBU-27289 (barcode reader dropout, no event) | **C4091911** "TIBU-27289 - No event for barcode reader dropouts" (full content, event 941) | Migrated into new case **C4104109** |
| TIBU-22250/TIBU-21950 (banner area) | **C4060881** "TIBU-22250: banner does not fully disappear" (full content) | Migrated into new case **C4104109** alongside TIBU-27289 (same functional area — one case, not three near-duplicates) |
| TIBU-27324 (audible beep pattern) | **C4091912** "TIBU-27324 - Audible Beep..." (full expected beep-per-product table) | Table migrated verbatim into EDIT of **C4101006** |
| TIBU-26303 (missing Network Interface screen) | **C4091908** "TIBU-26303 - ..." (full GIVEN/WHEN/THEN, confirms both Ethernet + Cellular interfaces shown) | Content migrated into EDIT of **C4101016** |
| TIBU-25446 (FEIG manifest spam) | **C4091897** (full content, SD-card log-pull method) | Grounded the EDIT of **C4101080** |
| TIBU-26048 / TIBU-26522 (FEIG update via TMS / EMV detection after update) | **C4091905** / **C4091910** (full content) | Grounded the EDIT of **C4101080** |
| TIBU-24428 (comms spamming) | **C4069405** / **C4091894** (full content — fix target: "stays on ethernet, does NOT fail over to cellular") | Ref-only addition to **C4103568** (see conflict note below) |
| TIBU-28139 (remote logging) | C4091913 — **empty stub, no content** | No old-suite content to migrate; new case **C4104110** grounded directly on the JIRA ticket's own repro steps instead |

Also surfaced (not one of the 55 JIRA issues, but material to a decision made **earlier in this same
session**): **C2700890** / **C3275939**, "Secondary Communication Failover Method" (Refs `REQ-2746.0`,
old cases from 2022/2024), explicitly test the PV **continuing to operate via cellular** when
Ethernet fails. This appears to conflict with today's earlier condemnation of C4101085 (based on
FBD-100359 + George's live confirmation, gap Q9, "Ethernet-only, no failover"). See **Escalation**
below — logged as gap-register **Q23**, not resolved unilaterally.

## Scope table — all 55 issues classified

Legend: **Covered** = an existing case already exercises it (cited); **Covered (edit)** = it now
does, after this session's fold; **Added** = a brand-new case now covers it; **GAP** = flagged to
the gap register, no case authored (no invention).

| Key | Type | Summary | Verdict | Case(s) |
|---|---|---|---|---|
| TIBU-21910 | Epic | Release 5.0.0 TL Validators | N/A (container) | — |
| TIBU-24660 | Test Execution | [PV] Glider TOO - QA Run | N/A (artifact) | — |
| TIBU-22305 | Epic | Glider Tap On Only for PV | Covered via children | C4101002, C4101092, C4101093 |
| TIBU-28094 | Epic | NIR TOTO on PV | Covered via children | C4103565 (via TIBU-28098) |
| TIBU-22311 | Tech Story | Port Open Payment from Edinburgh Trams | Covered | C4101080, C4101079/C4101020, C4100998/C4100999, C4101004/C4103565 |
| TIBU-22312 | Tech Story | Port pilot list functionality from SRUP | Covered | C4101078, C4103562, C4103563, C4103564 |
| TIBU-24196 | Tech Story | Implement TOO for Glider PV | Covered | C4101002, C4101092 |
| TIBU-28453 | Tech Story | Recover PV that fails to boot | Covered | C4101094 |
| TIBU-22316 | Story | Update PV FEIG software via back office | Covered | C4101080, C4101019 |
| TIBU-22317 | Story | Deny/BIN list download + apply, EOD + retry + delta | Covered | C4101079, C4101020 |
| TIBU-22318 | Story | Remote FEIG upgrade incl. TID/TK from device group | **Added** (old-suite migration) | **C4104108** |
| TIBU-22319 | Story | cEMV enablement (route/location/fare/tech-menu) | Covered | C4101001, C4101088 |
| TIBU-22322 | Story | cEMV taps rejected in the right cases (incl. passback) | **Covered (edit)** — passback case was missing | C4101088 (edited) |
| TIBU-22323 | Story | Success screen shown + times out | Covered | C4100998, C4101093 |
| TIBU-28098 | Story | TOTO tap audit correctness | Covered | C4103565 |
| TIBU-28386 | Story | MERIT heartbeat every 24h + on in-service entry | **Covered (edit)** — trigger broadened | C4101082 (edited) |
| TIBU-30476 | Story | Audit stop id as well as stage id | Covered | C4101092 |
| TIBU-21950 | Bug | Banners don't match UI spec | **Added** (old-suite-grounded) | **C4104109** |
| TIBU-24428 | Bug | PrimaryCommsChannelFailed spamming | Covered (ref added) — see Q23 | C4103568 (ref added) |
| TIBU-25446 | Bug | FEIG manifest spam every 1s | **Covered (edit)** | C4101080 (edited) |
| TIBU-25548 | Bug | SIM ID not sent to CF | Covered | C4101095 |
| TIBU-25691 | Bug | EMV taps disabled for Glider PV | **Covered (edit)** | C4101080 (edited) |
| TIBU-25700/25702/25704/25705 | Bug | EMV result screens / transaction generation | Covered | C4101093 |
| TIBU-25745 | Bug | BIN list download fails | Covered | C4101079 |
| TIBU-25842 | Bug | Frozen on white Flowbird screen | Covered | C4101094 |
| TIBU-26048 | Bug | FEIG update via TMS fails | **Covered (edit)** | C4101080 (edited), C4101019 (ref) |
| TIBU-26053 | Bug | PCA version not displayed | Covered | C4101095 |
| TIBU-26054 | Bug | FEIG Device ID not in Asset Manager | Covered | C4101095 |
| TIBU-26303 | Bug | Missing Network Interface screen | **Covered (edit, old-suite-grounded)** | C4101016 (edited) |
| TIBU-26320 | Bug | Deny list download fails | Covered | C4101079 |
| TIBU-26522 | Bug | FEIG update → fails to detect EMV cards | **Covered (edit)** | C4101080 (edited) |
| TIBU-26531 | Bug | Duplicate FEIG versions in Asset Manager | **Covered (edit)** | C4101095 (edited) |
| TIBU-27289 | Bug | No event for barcode reader dropout | **Added** (old-suite migration) | **C4104109** |
| TIBU-27324 | Bug | Audible beep pattern wrong for MUB | **Covered (edit, old-suite-grounded)** | C4101006 (edited) |
| TIBU-28139 | Bug | Remote logging (Device Log Manager) not working | **Added** | **C4104110** |
| TIBU-28240 | Bug | Frozen on black screen after reboot | **Covered (edit)** | C4101094 (edited) |
| TIBU-28645 | Bug | Payment method wrong (OpenPayments not ABT) | Covered | C4101092 |
| TIBU-28649 | Bug | Deny/BIN list URLs wrong per environment | Covered (config-value issue, not case-level) | C4101020/C4101079 |
| TIBU-28770 | Bug | Transaction Service stops responding | Covered | C4101094 |
| TIBU-28805 | Bug | Pilot-list decline incorrectly creates audit | Covered (ref added) — already exact match | C4103563 |
| TIBU-28856 | Bug | Direction audited OUT not IN | Covered | C4101092 |
| TIBU-29165 | Bug | Stuck, not downloading distributions | Covered | C4101094 |
| TIBU-29191 | Bug | SIM shows "connected" when physically removed | **Covered (edit)** — status-reporting only, see Q23 | C4101016 (edited) |
| TIBU-29602 | Bug | Deployments via TMS broken | Covered | C4101094 |
| TIBU-30923 | Bug | Config+software can't apply in the same distribution | **GAP** — Q24 | — |
| TIBU-31287 | Bug | 200,000-entry Deny list causes PollSocket exception | **Covered (edit)** | C4101079 (edited) |
| TIBU-31705 | Bug | Technician screen speed slow on sub-menus | **GAP** — see below | — |
| TIBU-31722 | Bug (v5.0.1) | Glider Metro ABT not enabling despite correct zone config | **Covered (edit)** | C4101001 (edited) |
| TIBU-32037 | Bug (v5.0.3) | Watchdog interrupts FEIG PCA/FW update | **Covered (edit)** | C4101080 (edited) |
| TIBU-24260 | Bug | Version page missing Application version | Covered | C4101095 |
| TIBU-25444 | Bug | Barcode expiry (NIR) UTC/local conversion | Covered (ref added) — already exact match | C4102428 |

**TIBU-31705 note:** flagged in earlier analysis for an ADD (Technician Menu screen-transition
performance) but **not authored this session** — on reflection it needs its own non-functional
performance case rather than a forced fold into C4101087 (which is validation/barcode timing, a
different risk area), and per the minimal-sufficient-set principle a genuinely new case should not
be rushed without checking whether a performance/timing convention already exists elsewhere in the
suite for Technician Menu specifically. Recording this as a **follow-up ADD**, not a gap — the
*behaviour* is known (sub-menu navigation should be fast), it just wasn't included in this push;
flag for the next authoring pass.

## Tally

- **55** JIRA issues in scope (53 v5.0.0 / 1 v5.0.1 / 1 v5.0.3, some counted once despite 2 fixVersions).
- **4** excluded as non-testable containers/artifacts (2 epics whose children are counted, 1 pure
  epic, 1 Test Execution record).
- **Covered outright** (no case change needed): 27
- **Covered after this session's edit** (fold/broaden into an existing case): 15
- **Added** (new case, 2 of 3 grounded on real old-suite content): 3 — **C4104108, C4104109, C4104110**
- **GAP** (flagged, no invention): 2 — TIBU-30923 (Q24), TIBU-31705 (follow-up ADD, not this push)
- **Stale:** none reclassified this session (the two pre-existing condemnations, C4101005/C4101085,
  were already actioned earlier today per `proposals/coherence-audit/fixes/pv.changelog.md` and are
  accounted for, not re-touched).

## ADD / EDIT / REORGANISE actions taken

**ADD (3 new cases, pushed via `proposals/pv-release-coverage/pv-release.cases.yaml`):**
- **C4104108** "FEIG — update without TID/TK fails safely, PV app software still updates" (Functional
  / ABT (Glider)) — migrated from old-suite C4073875. Refs: TIBU-22318.
- **C4104109** "PV — barcode/smartcard reader disconnect shows the correct banner and raises an
  event" (Functional / Barcodes) — migrated from old-suite C4091911 + C4060881. Refs: TIBU-21950,
  TIBU-27289.
- **C4104110** "PV to BOS — Device Log Manager retrieves device logs on request" (Non-Functional /
  PV) — grounded directly on the TIBU-28139 ticket's repro steps (no old-suite content existed).
  Refs: TIBU-28139.

**EDIT (12 fold/broaden + 1 ref-only, via `proposals/pv-release-coverage/pv-release.rewrite.json` and
`pv-release-2.rewrite.json`, applied with `tools/apply_rewrite.py --commit`):**

| Case | Change | Pins |
|---|---|---|
| C4101079 | Added 200,000-entry Deny-list scale step | TIBU-31287 |
| C4101001 | Added Glider Metro zone-enablement regression step | TIBU-31722 |
| C4101080 | Added 3 steps: watchdog/manifest-stall on update, EMV-detection-after-update, manifest-poll frequency | TIBU-25446, TIBU-25691, TIBU-26048, TIBU-26522, TIBU-32037 |
| C4101095 | Added duplicate-FEIG-version-in-Asset-Manager step | TIBU-26531 |
| C4101094 | Broadened freeze step to include black-screen variant | TIBU-28240 |
| C4101082 | Broadened heartbeat trigger beyond technician sign-out | TIBU-28386 |
| C4101088 | Added ABT Passback decline scenario | TIBU-22322 |
| C4101016 | Added Network Interfaces display + SIM-removed status steps | TIBU-26303, TIBU-29191 |
| C4101006 | Added exact beep-per-product table (migrated from old-suite C4091912) | TIBU-27324 |
| C4102428 | Ref-only | TIBU-25444 |
| C4103563 | Ref-only | TIBU-28805 |
| C4101019 | Ref-only | TIBU-26048, TIBU-32037 |
| C4103568 | Ref-only | TIBU-24428 |

**REORGANISE:** none — no misplaced cases found; all edits landed in the section that already owned
the behaviour.

**Tooling note:** `tools/apply_rewrite.py` didn't support a refs-only update (only
preface/preconds/steps), so it was extended with a small, backward-compatible `refs` pass-through
(the writer's `update_case_fields` already supported it) to avoid inventing step content just to
carry a citation.

## Escalations (gaps logged, not invented) — `proposals/coherence-audit/gap-register.md`

- **Q23 — comms-failover conflict.** Old-suite `REQ-2746.0` cases (C2700890, C3275939, "Secondary
  Communication Failover Method") explicitly test the PV **failing over to cellular** when Ethernet
  drops — apparently contradicting this same session's earlier condemnation of C4101085 (built on
  FBD-100359 + George's live confirmation that the PV is **Ethernet-only, no failover**). Additional
  evidence (TIBU-24428's own fix target: "stays on ethernet, does not fail over"; TIBU-29191 and
  C4091908 both confirming a Cellular interface is still shown on the Technician Menu) suggests a
  working theory — **REQ-2746.0 may be an obsolete/superseded requirement from an earlier PV
  hardware/config generation** — but this is not confirmed. **Not resolved unilaterally**: C4101085
  stays condemned per Q9, no new "failover" case was authored, and TIBU-29191 was folded into
  C4101016 as a status-reporting assertion only (not a failover assertion). Flagged as
  **POSSIBLE DESIGN/SPEC BUG** per the hard rule — two apparently-authoritative sources disagree.
- **Q24 — TIBU-30923.** No FBD/REQ found and no old-suite case; the ticket describes an observed
  limitation (config + software can't apply in the same distribution) with no stated fix/expected
  behaviour. Cannot author a case without inventing which behaviour is correct (fixed vs.
  accepted-permanent two-step procedure) — logged as a question, no case authored.

## Run-health (run-historian lens)

`run-health.json` covers the last 6 runs (of the last 10 requested; only 6 exist) against project 42.
Nearly all of the 133 pre-existing PV cases show **0 executions — "orphaned"**, which is expected and
**not a finding**: the suite was built/iterated through 2026-06 to 2026-07-21 and hasn't had a full
regression run yet (per `test-practices.md`, "not run" ≠ "not needed" for recently-added cases). The
3 new cases (C4104108–10) will show the same until the next run.

The **~15 "flaky"/"recently-regressed" rows** in `run-health.md` (e.g. C2092782 "UnSuccessful
Cloudfare SignOn - Administrator", C2082941–50 "Verify ... Screen Contents", C2131388, C2132847/8)
do **not** appear on the PV suite's own case list (`cases.md`) at all — they look like **BOS/CloudFare
web-admin cases from a different suite** in project 42 that the run-history join picked up (case ids
in the low-2M range vs. the PV suite's 4.1M range). This is flagged as a probable **cross-suite
artifact** in the run-health tooling, not a PV finding — worth the run-historian double-checking the
`runs` command's suite-scoping, but out of scope to fix in this coverage session.

## Files

- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/cases.json` / `.md` (post-push)
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/run-health.json` / `.md`
- `reports/tfts-system-test/aa-platform-validator-acceptance-test/2026-07-21/cases.json` / `.md` (old suite 10047 baseline)
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/jira-scope-summary.json`
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/jira-descriptions.md`
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/case-bodies.json` (new-suite case bodies pulled for grounding)
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/old-suite-case-bodies.json` / `old-suite-case-bodies2.json` (old-suite case bodies pulled for grounding)
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/alignment-audit.md` (post-push conformance audit — CLEAN)
- `proposals/pv-release-coverage/pv-release.cases.yaml` (3 ADDs)
- `proposals/pv-release-coverage/pv-release.rewrite.json`, `pv-release-2.rewrite.json` (13 EDITs)
- `proposals/coherence-audit/gap-register.md` (Q23, Q24 appended)
