# TVM deep-audit (full citation-grounding pass) — changelog

**Suite:** `**NEW** TVM Test Suite` (30284), project 42, TFTS - System Test. **Mandate:** George's
2026-07-21/22 directive to do the full thing this tool exists for — cross-examine **every** live
case against the actual FBD/spec source, not just internal coherence, following on from the
2026-07-17 coherence audit (16 findings) and today's earlier targeted fixes (34 cases:
barcode/smartcard/Scottish-note) + terse-rewrite pass (9 cases).

**Pulled fresh:** `python -m system_test_ops cases --project 42 --suite 30284` (201 total) plus raw
bodies via `TestRailClient.get_cases(42, 30284)` (preface/preconds/steps/expected/refs, not the
flattened CLI export). **Active (non-`ZZ_DELETE_REVIEW`) case count: 174.**

## Method

For each of the 174 active cases: read title/preface/preconditions/steps/expected in full, listed
every factual claim (capability, screen/message name, config value, workflow step, audit event,
cash rule), and checked whether the case's existing **Refs** citation actually supports that claim
— not just whether a citation was present. Where a citation looked generic/reused across dissimilar
claim types, pulled the real source document via `tools/extract_req.py` (not the distilled
`knowledge/` note) and read it directly. Searched `REQS_DIR` by filename for any better-fitting
source where a citation was missing or wrong. Logged anything neither confirmed nor deniable to
`proposals/coherence-audit/gap-register.md` (Q30–Q34) rather than inventing or silently dropping it.

## What was found and fixed (30 citation corrections, 0 body/behaviour changes)

**No case in this pass needed its title, preface, preconditions, steps or expected result changed —
the wording throughout is accurate to what's tested.** The problem found was entirely in the
**Refs field**: three sections had inherited a plausible-looking FBD number that, read in full,
turns out to document something else.

### 1. EMV & Contactless section (887780) — FBD-100320 mis-cited on 15 of 16 cases (Q30)
FBD-100320 is `TID Management - Embedded & Non-Embedded Payment Devices` — read in full via
`extract_req.py`, it is **entirely** about terminal-ID/transaction-key allocation (serial-number
mapping, NMI Terminal Groups). Zero mentions of PAN, PIN, contactless, or transaction limits
anywhere in the document. It does not support any of: card approval/decline, PIN timeout, Amex/
Diners acceptance, min/max transaction value, contactless tap limit, mobile wallet, PAN masking, or
print-failure voiding a payment — the actual subjects of C4103657–4103670 and C4103672. Checked
FBD-100183 (POS Hardware Spec) as an alternative — it documents the **POS's Miura M020**, not the
**TVM's Ingenico** terminal, so it doesn't apply either. No TVM/Ingenico EMV spec exists anywhere in
`REQS_DIR`. **Fixed:** FBD-100320 removed from these 15 cases' Refs (kept only on **C4103671**, whose
claim — the audit record carries the TVM's TID — genuinely is FBD-100320 territory), replaced with a
pointer to gap-register **Q30**. Case bodies untouched — the claims themselves are standard EMV/PCI
terminal behaviour, not in dispute, just previously mis-cited.

### 2. Commissioning / Config-Topology "home location" cluster — FBD-100296 mis-cited on 7 cases (Q31)
FBD-100296 (`Stop, Route & Service Management in CloudFare`) documents TransXChange-sourced routes/
map-points and the ETM route-entry UI — nothing about Device Home Location, operator assignment, or
fares-triangle product availability, the actual subjects of C4103740, 4103746, 4103758, 4103759,
4103760, 4103761, 4103762. Found better sources: **FBD-100383** (TFTS Operator Hierarchy) explicitly
defines Device Home Location per operator; **PSPEC-0014** (CloudFare — Fares and Topology Manager)
§9 "Fare Triangle" documents the fares-triangle concept directly (confirmed present in `REQS_DIR`,
not yet distilled into this repo's `knowledge/`). Neither source states the **joined** rule ("home
location limits which fares-triangle products are sellable") verbatim — that link is inferred, so
it's flagged needs-confirmation rather than asserted as fact. **Fixed:** Refs corrected from
FBD-100296 to FBD-100383 (+ PSPEC-0014 §9 where the case is specifically about triangle
availability), with a pointer to gap-register **Q31**. C4103762 (sub-location 3-digit ID format) has
no matching source in either doc — left as a bare gap pointer, no FBD asserted.

### 3. Commissioning / Config-Deployment cluster — FBD-100385 mis-cited on 7 cases (Q32)
FBD-100385 (`CloudFare Configuration Data Exports`) is explicitly scoped to **portal export
reports only** ("Reports module → Topology submodule") — it does not document the **device-side**
TMS dataset-deployment mechanism actually under test in C4103741–4103745, 4103747, 4103748
(immediate vs future-dated activation, partial-deployment success/failure reporting, coin-vault-
threshold config push, EMV-only-mode toggle). No TMS/dataset/deployment/rollout/activation spec
exists anywhere in `REQS_DIR`. **Fixed:** FBD-100385 removed from these 7 cases' Refs, replaced with
a pointer to gap-register **Q32**. Case bodies untouched — the deployment behaviour described is
plausible/standard TMS practice, just uncited in the available library.

### 4. C4103793 "WAN-to-SIM failover" — flagged as an unresolved conflict, not changed (Q33)
C4103793 asserts the Kiosk TVM fails over WAN→SIM and back. FBD-100359 (SaaS Network Impact)
classifies **Retail Kiosk** as an "Ethernet device" with no cellular-failover path documented (same
"Ethernet-only, no failover" reading that was applied — then reversed on old-suite/TIBU evidence —
for the **PV** earlier this session, Q9/Q23). Time did not allow checking the old suite (10047) or
TIBU for TVM-specific failover evidence the way it was done for the PV, so this is **not** resolved
either way — left unchanged, flagged in Refs, logged as **Q33** for a follow-up check rather than
guessed.

### 5. ~52 hardware/procedural cases with no citation at all — systemic absence of source docs, not fixed (Q34)
Payments-Cash (887777, minus the 2 that do cite FBD-100341), Note Recycler & Change (887778), Coin
Recycler Hopper (887779/887795), most of EMS/TMS Maintenance (887793), all of Alarmboard & Enclosure
(887794), and the hardware-state half of Resilience (887796) — roughly 52 cases — carry no Refs and
describe directly-observable physical/procedural behaviour (coin/note validator acceptance rules,
escrow limits, BNR jam states, alarmboard siren/LED/temperature/UPS/door/speaker/fan tests, TL80
alignment, touchscreen self-test, EMS role access, volume/brightness persistence, degraded/amber
states, cash lockout limits, 98% acceptance / launch-time performance targets). Searched `REQS_DIR`
by filename for every plausible keyword (cash, hardware, printer, alarm, BNR, note acceptor, escrow,
lockout, degraded, AML/laundering/cash-limit/suspicious) — **no FBD/REQ document in the library
covers this layer at all**; it is presumably vendor/OEM (Astreo/Kiosk/TL80) hardware-acceptance
documentation never in scope for this requirements library. **Not marked GAP/UNCONFIRMED in the
case bodies** — these claims are checkable directly on live hardware and are not in dispute the way
a capability-attribution claim (barcode scanner, smartcard reader) is; per `gherkin-standard.md`'s
assumed-competence/unknown-configured-value guidance, the blocking marker is reserved for disputed
*existence* of a behaviour, not "no bespoke citation exists for an observable mechanical fact." This
mirrors the original 2026-07-17 audit's "clean" verdict on this area — that pass checked coherence
only; this pass adds the citation check and records the result as one systemic finding (**Q34**)
rather than 52 duplicate entries.

## What did NOT need a fix

All other citations were spot-checked against their real source and confirmed accurate: FBD-100483
(barcode redemption state machine — already verified line-for-line by the original audit),
FBD-100515 (grouped stops — already verified exact match), FBD-100207 (fare-stage-to-stop — read in
full, confirms TVM Key-Stop-based boarding/alighting exactly as the basket/ticket-issue cases
describe), FBD-100266 (device heartbeat — confirms the 15-minute staff-list mechanism exactly),
FBD-100359 (SaaS network impact — confirms the Ethernet offline→comms-locked-OOS behaviour, aside
from the Q33 WAN/SIM-failover question), FBD-100341 (revenue apportionment — matches the audit-
posting cases), FBD-100336/FBD-100450/FBD-100167/FBD-100317/FBD-100318 (fares export and barcode
format families — consistent with the original audit and today's earlier barcode-cluster fix). The
Smoke-section cases (C4103673–4103679) carry old-suite case IDs (`C18xxxxx`/`C17xxxxx`) and
`REQ-####` numbers as Refs rather than FBD numbers — a legitimate, pre-existing, different citation
style (traces to the old suite's case, verifiable by a human in TestRail history) and out of scope
for `extract_req.py` verification; left as-is.

## Push

```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-deep-audit.rewrite.json --commit
```
Dry-run and commit both reported: `updated: 30  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0`.

## Audit

```
python -m system_test_ops audit --suite 30284
```
**CLEAN** — 174 cases audited, 0 blocking findings, 24 advisory `title-too-long` (identical count to
before this pass — pre-existing, unrelated).

## Totals

| Category | Count |
|---|---:|
| Total active cases reviewed (every case, full body) | 174 |
| Citation corrected (Refs only, no body/behaviour change) | 30 |
| — EMV/Contactless FBD-100320 mis-citation (Q30) | 15 |
| — Home-location/fares-triangle FBD-100296 mis-citation (Q31) | 7 |
| — Config-deployment FBD-100385 mis-citation (Q32) | 7 |
| — Conflict flagged, unchanged (Q33) | 1 |
| Verified clean with an accurate citation (no change needed) | ~91 |
| No citation available, none fabricated — systemic gap (Q34, single grouped finding) | ~52 |
| New gap-register questions raised | 4 (Q30–Q33) + 1 systemic (Q34) |
| Cases not reached | 0 |

**Not touched:** every other TestRail suite; the 27 previously condemned (`ZZ_DELETE_REVIEW`) cases
and the earlier 9 terse-rewrite cases from today's prior passes (out of scope, already handled).

## Follow-up: resolving Q30–Q34 from old suites + JIRA + TFTS Requirements Matrix (2026-07-22)

George's directive: before escalating any gap-register question to him, exhaust every other source —
old suites (one may already test the exact behaviour), UX/hardware docs, JIRA, and a broader spec
re-search — and only leave truly unanswerable questions open. Applied to all 5 TVM questions above.

**Method.** Pulled full case exports for every old TVM suite (`5602`, `6160`, `22270`, `22272`,
`22273`, `22274`, `22275`, `22276`, `22278`, `22279`) via `python -m system_test_ops cases --project
42 --suite <id>`, plus raw bodies for specific case ids via `TestRailClient.get_cases(42, <suite>)`
(preconds/expected, not the flattened CLI export). Searched by keyword per question (EMV/Ingenico/
PAN, home location/fares triangle, deployment/activation/coin-vault/EMV-only, SIM/failover/Teltonika,
cash/coin/alarm/lockout). Also queried JIRA (`searchJiraIssuesUsingJql` + `getJiraIssue`, Atlassian
Rovo MCP) for TVM/Kiosk comms-failover tickets, the same technique that resolved the PV's Q9/Q23
comms-failover saga. Mid-pass, a sibling POS gap-resolution session found `TFTS Requirements
Matrix.xlsx` (`1_Requirements\TFTS Project Delivery Matrices & VCRMs\` in `REQS_DIR`) — a genuine
REQ-id index (Alias/Name/Notes/Status columns, `openpyxl`-readable, full requirement text +
sign-off state) that nobody had searched for by name before — and flagged it as likely relevant here
too. Looked up every REQ id surfaced from the old suites against it.

**Result: all 5 questions resolved from existing evidence — zero required escalation to George.**

- **Q30 (EMV & Contactless, 15 cases)** — RESOLVED. Old suite 6160 + 22276 cite a REQ-#### scheme
  (not FBD) that maps claim-for-claim onto every one of the 15 cases, including **REQ-1515.0/1.1**
  ("Support Chip and PIN on the TVM" / "Device Fitted with EMV Contactless Reader") and **REQ-1630.3**
  ("TVM Payment Channels... Sales payments only, not reversals or refunds") — the governing TVM/
  Ingenico terminal spec, all **S4: Signed-Off** in the Requirements Matrix. C2132852's old-suite
  title even names the terminal: "PAN Not Shown on **Ingenico Device**".
- **Q31 (home-location/fares-triangle joined mechanism, 7 cases)** — RESOLVED. Old suite 6160
  "Configuration Topology" section has 4 cases (C1831895/1899/1903/1904) that directly change home
  location and check resulting product/destination sellability — the joined mechanism, tested as one
  behaviour, even though no single spec states it as one sentence. REQ-2710.0 (S4: Signed-Off)
  confirms Home/Sub Location are one governed field-configuration requirement. Also closed
  C4103762's previously-bare gap (old suite C1831422-425 directly test the 3-digit sub-location
  format).
- **Q32 (config-deployment cluster, 7 cases)** — RESOLVED. Old suite 6160 "TVM / Deploy the
  Software, Configurations & Topology" section (incl. "Failed Deployment"/"Scheduled -
  Pre-Deployment" subsections) covers every named claim — immediate vs future activation
  (C1831885/886), partial-deployment success+failure reporting (C1831403/404), coin-vault threshold
  (C1831883), EMV-only mode (C1831884) — citing REQ-0551.x/0680.0/2727.0/2720.x/0847.5/3294.0, all
  **S4: Signed-Off**.
- **Q33 (C4103793 WAN-to-SIM failover)** — RESOLVED, reversed exactly like the PV Q9/Q23 saga. Old
  suite 6160/22270 hold C1831873/C3544437 ("TVM Comms on SIM - Comms Event Reported to Cloudfare",
  REQ-2746.0 — the same REQ family as the PV's failover) whose expected result states verbatim *"TVM
  continues to operate as normal and report to Cloudfare over SIM when the LAN connection fails"*,
  plus the bidirectional pair C2038470/471. JIRA corroborates directly: **TIBU-13485** (closed)
  describes selling 5 tickets over SIM-only after disconnecting LAN, then reconnecting, with Cloudfare
  expected to log "Sim Only"/"LAN restored" — full functional continuity, not just an event stub.
  **TIBU-15938** (closed) is the matching comms-event defect; **TIBU-4128/4682** confirm the physical
  Teltonika cellular modem. FBD-100359's Ethernet-only classification is stale for the TVM, same as
  it was for the PV — flagged as a candidate FBD update, out of scope to edit here.
- **Q34 (~52 hardware/procedural cases, "no requirement document at all")** — SUBSTANTIALLY RESOLVED.
  The premise was wrong: old suite REQ-#### citations exist for nearly the whole layer (cash/coin/
  banknote REQ-0339.x, currency REQ-1491.0, coin-vault REQ-0847.x, burglary/alarm REQ-2369.x/2785.0,
  device/comms lockout REQ-2690.0/2576.0, cash-collection reports REQ-2720.x, volume/brightness
  REQ-0511.x, ticket-roll REQ-0848.0, audio prompts REQ-0279.x/1687.0, EMS sign-in REQ-2731.0), all
  **S4: Signed-Off** — including **REQ-0339.11/.13**, the literal, verbatim "98% acceptance rate"
  requirement the question said was undocumented. Applied Refs to 36 of the cluster's cases. A
  smaller residual (~16 cases: BNR/BNA jam states, print-failure-returns-cash, the Kiosk alarmboard
  hardware diagnostics, degraded/amber states, mains power failure, screensaver/multi-modal home,
  launch-time performance) genuinely found no REQ/old-suite match even after this pass — left
  uncited, not escalated (low-risk, directly checkable on live hardware, consistent with the original
  "clean" 2026-07-17 coherence verdict).

**Push.**
```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-deep-audit-resolution.rewrite.json --commit
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-deep-audit-q34-resolution.rewrite.json --commit
```
`tvm-deep-audit-resolution.rewrite.json`: `updated: 30  removed(ZZ): 0  fare-reframed: 0  skipped: 0
missing: 0` (Q30/31/32/33, 30 cases). `tvm-deep-audit-q34-resolution.rewrite.json`: `updated: 36
removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0` (Q34, 36 cases). Refs field only — no
case body/behaviour changed in either push (all 5 questions were citation/traceability gaps, not
wording defects).

**Audit.** `python -m system_test_ops audit --suite 30284` — **CLEAN**, 174 cases, 0 blocking
findings, 24 advisory `title-too-long` (unchanged from before this pass).

**Totals.**

| Category | Count |
|---|---:|
| TVM gap-register questions in scope (Q30–Q34) | 5 |
| Resolved from old suites / JIRA / Requirements Matrix (no escalation needed) | 5 |
| Cases with Refs corrected/added this follow-up pass | 66 (30 + 36) |
| Cases left genuinely uncited (residual Q34 tail, low-risk, directly checkable) | ~16 |
| Remaining open for George | 0 |

See `proposals/coherence-audit/gap-register.md` (session "TVM deep-audit (suite 30284...)") for the
full per-question evidence trail.
