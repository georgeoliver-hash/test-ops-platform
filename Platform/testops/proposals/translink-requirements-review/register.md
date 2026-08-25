# Translink requirements review — running register

Living log of **questions, blockers, findings and housekeeping** from the requirements ingestion +
suite cross-examination. Walk this at the end. Updated as work proceeds.
Last updated: 2026-07-15.

---

## A. Blockers — specs incomplete / can't author around (need a real spec or team input)
| # | Item | Impact | Source |
|---|---|---|---|
| A1 | **BV (Bus Validator) comms protocol is an empty v0.01 stub** (headers only, no requirements) | A **BV device suite cannot be built** until an issued spec exists | FBD-100391 |
| A2 | **Gates: functional behaviour "to be validated on integration"** (authorise/open, fault handling, modes, pictograms, buzzer) not yet evidenced; only factory-acceptance exists | A **GV/gate suite** can't be meaningfully authored yet | FBD-100348 |
| A3 | **Gate close-fail ambiguity:** OOS after "2 attempts" (FUN-0016) vs "3 consecutive" (FUN-0018) | Can't assert the exact threshold | FBD-100348 |
| A4 | **FBD-100334 Revenue Reallocation w/ ABT Capping** = unfilled template (only REQ list real) | Reallocation cases need completed spec / MERIT confirmation | FBD-100334 |
| A5 | **FBD-100333 Transfer Stop Implementation** = v0.03 template stub | Transfer-point config + paper-ticket reallocation (REQ-2121.2/.3) unspecified | FBD-100333 |

## B. Questions to resolve with George / the team
| # | Question | Why it matters |
|---|---|---|
| B1 | **Which barcode single-use flow ships** — the old online-Corethree call, or the new REST API (CR094)? | Determines whether TVM/HHD single-use barcode cases need re-authoring to the API state machine |
| B2 | **Declined-Reason codes** — do existing Metro cases assert the pre-"alignment-fix" values? The spec now says 15=BIN, 20=Passback | Possible **contradiction** — existing cases may be wrong |
| B3 | **CR status** — which of these are accepted/shipped: CR094, CR105.1/.2/.3, CR115, CR116, CR122, CR123, CR134? | Cases gated on unshipped CRs must be marked/deselected, not asserted as live |
| B4 | **Doc-number mismatches** — FBD-100353 is a near-duplicate of FBD-100320 (authored to 100320 V5.03); gate config docs' internal ids (FBD-100522/100523) don't match their folder ids (100653/100654); FBD-100450 header mislabels itself as FBD-100336 | Traceability/citation accuracy |
| B5 | **Which devices need a suite** beyond POS/ETM/PV/ABT-BOS/TVM — HHD? BV (blocked)? GV/gates (blocked)? | Scope of "a suite per device" |
| B6 | **RTPI/DAIP (FBD-100202/100345)** — ETM↔Vix protocol; in scope for a system-test suite or out? | Scoping the ETM suite |

## C. Findings — coverage gaps (master list, drives the re-audit)
Grouped from the 59 distilled spec notes' "Suite implications". To be confirmed against live suites in the cross-examination.

**Barcode / cards**
- Single-use flow may test the OLD model, not the CR094 REST API (see B1).
- Device "wrong barcode class" rejections (exact string "This Barcode Type is not accepted on this device") — POS rejects multi-use; PV/GV/ETM reject single-use; TVM rejects Manifest — likely gaps.
- Three result states (green / yellow step-7-only / red) + CR116 midnight–04:00 expiry-display rollback.
- Offline: ceiling-limit accept/reject boundary; offline-redemption sweep sends NO CloudFare events; Card Reference File ignored unless ConfigurationVersion increments.
- Rail £90 fare-fallback (CR105.3); gateline Unique-ID sharing (CR105.2); passback store (CR105.1).
- Legacy-card date edges: 1991-offset year wrap (16-yr), academic-year EA, birthday concessions, NIR Gate Pass fixed 2099.
- Transfer property-source: ETM uses route Transfer Time; PV/GV/Rail-HHD use product Transfer Time; Metro Transfer Zone (id > 256); passback prioritised over transfer.

**ABT / capping / Tap-On**
- NIR TOTO 4-step tap-matching; absent tap-off ⇒ max fare; max-fare journeys EXCLUDED from capping.
- Capping vs 04:00–03:59 operating day; 14-day late-tap vs expired boundary; "late tap = last tap of its day" retro-charge; capping rules activate NEXT business day.
- Capping-group (reference-fare → cap) model + 3-day cap window (UB + NIR).
- Two distinct transfer mechanisms (Glider↔Metro/UB ~90-min CR123 vs NIR free bus↔rail) — don't merge.
- Correction limits (1/month, 3/year, shared UB alighting + rail missing-tap; operators unlimited) — partially added to ABT already; verify vs spec.
- Zone encoding: bitwise Zone Number (256 multiples); audit Zone arrays must carry Zone *Numbers* not Ids; rail/bus split by transport mode, not zones.

**Audit / back-office**
- Record renames: JourneyTap→TotoTap; new HHD CardDetails block; TransportationType "Rail Sub"; pounds (Fare) vs pence (fareCost).
- `BarcodeUsage` zero-fare txn path CloudFare→MERIT; failed validation = event (not txn); single-use redemption logs as Event not MERIT transaction.
- Deny-list 100k cap / ~30-min propagation / 15-min tap-removal; BIN 2,500 cap; 3 re-auth triggers.
- Net-of-annulment cash totals with EUR converted-in but native retained (Operator Totals API + Activity Log).
- DWH freshness (~10-min SSIS incremental, clean-only) + consistency-check = 0; ABT open journeys excluded until completed; pre-calculated report values (headway/adherence) are a regression surface.

**POS / device**
- Refund: Operator-role-ONLY; cash-URN validation triad (≠23 chars / > original / shift-negative); card PRN + PSP failure modes; basket URN per-ticket vs PRN shared; CR115 cross-device.
- Fare-stage selection/display (Key Stops vs Fare Stage ID; zero-fare combo blocks issue; Fare Stage NAME on screen/ticket).
- Peripheral-optional: ~95/160 POS have M020 payment terminal, 80 have Bixolon display → card/display cases need hardware preconditions.
- TVM grouped stops: printed boarding stop = lowest non-zero fare, first-combination tie-break, ignores physical location (false-defect trap — needs explicit positive case).
- Revenue Inspection (HHD): events 5008–5013 authorable now; ABT-matching edge cases defer to FBD-100651/100658.

**Config / portal / ops**
- User claims: first-login-no-claims = denied all; CF-Operator-X sees that operator only vs ABT nested groups inherit children.
- Operator-hierarchy scoping (own + descendants, not parent/sibling) governs exports AND claims.
- Pilot list: non-enrolled FEIG token rejected with NO audit event; EOD upload (not real-time).
- Product-name 3-tier display fallback (Device Display → Default → Description) + Sub Product chain.
- SaaS offline: Ethernet devices comms-lock OOS on network loss; cellular keep working; RabbitMQ queue-and-deliver-on-restore.
- Shift Board (FBD-100831, 2026, brand new): CSV import validation, Sun→Sat vs Mon→Sun bitmask flip, 4am valid-from/to + 7-day purge — likely zero coverage.
- Service Classification "first-reached tag wins" on mixed-classification services = silent Merit misclassification risk.

## D. Housekeeping / process
| # | Item | Status |
|---|---|---|
| D1 | Push distilled specs + ingest tool + command (`cb2344c`) to GitHub | **Pending — George: GitHub Desktop → Push** |
| D2 | Push overview/standard/register updates | Pending (batch with next commit) |
| D3 | ZZ_DELETE cases across suites awaiting UI bin | Pending — George (do after re-write) |
| D4 | Raw docs stay LOCAL in dev/translink-requirements (never committed) | Enforced |
| D5 | Work Google account SSO-blocks the Drive MCP; Confluence MCP write admin-blocked; JIRA write admin-blocked | Known limits |
| D6 | TestRail moved to IP 10.120.54.19 (was `testraildb`); AD password rotated | Resolved in .env |
| D7 | Diagrams: images ARE readable on demand (Read tool); only Visio binaries + scanned-PDF pages not | Note |

## E. Program status (tasks)
1. Distil requirements ✅ done (59 notes, committed cb2344c)
2. Cross-examine suites vs requirements — **in progress**
3. Suite per device (TVM/HHD/BV/GV) — pending (George creates targets; BV/GV blocked per A1/A2)
4. JIRA coverage audits — pending (George feeds epics/sprints/fix+affected versions)
5. Strengthen writing standard — ✅ done (concrete-grounding rule added to gherkin-standard.md)
6. Re-write & re-audit every suite — pending (blocked by 2 + 5; **checkpoint with George before starting**)
7. Push all + colleague trial — pending

---

## F. Cross-examination results (2026-07-15) — per suite
Full detail in `gaps-pos.md`, `gaps-etm.md`, `gaps-pv.md`, `gaps-bos-abt.md`.

**Recurring caveat (must fix before re-write):** the `cases` JSON dump exposed mainly titles + the
first `Given` line — **not the When/Then bodies** — so all verdicts are **title/section-level and
provisional**. Before Phase 6 I must **pull full case bodies** (steps + expected) so nothing is
mis-flagged as missing when it's actually present. *(Suspected cause: the `cases` command JSON
doesn't serialise `custom_steps_seperated` — verify/extend the CLI.)*

**POS (30253)** — biggest single gap: **Refund on POS 100% missing** (whole feature: cash URN + card
PRN/PSP flows, Operator-only role gating, positive-Fare audit, CR115). Barcode scoping/audit
unasserted (single-use-only + reject-multi-use string + `BarcodeUsage` split). Fare-Stage display
partial (name-not-stop, zero-fare blocks issue). Heartbeat missing. MERIT revenue-location allocation
missing. Stale to verify: C4100440 (offline-barcode overstates vs Ceiling-Limit), C4100439 (needs
single-use scoping).

**ETM (30254)** — **Rail Substitution 0 coverage** (Manual-Override sign-on, GPS auto-advance,
`TransportationType="Rail Sub"`). **Shift Board sign-on missing** (new 2026 spec). Legacy transfer
decision missing (ETM route Transfer Time). ABT audit conformance not pinned. RTPI/DAIP + heartbeat
missing. Stale to verify: C4100583 / C4100591 (Declined-Reason vs 15=BIN/20=Passback).

**PV (30255)** — **STALE/WRONG C4101005** (asserts single-use *validates*; spec = multi-use-only,
reject single-use). Mislabels: C4101082 (heartbeat is CloudFare StaffList, not MERIT), C4101085
(secondary-failover questionable — PV is Ethernet). Missing: pilot no-audit-on-reject, TOTO audit
conformance, legacy transfer (product Transfer Time), comms-lock OOS, three barcode result states.
Good: CR116 expiry covered (C4102428); device scoping largely right.

**BOS & ABT (30279)** — **NIR TOTO entirely absent** (whole rail half of ABT: 4-step matching,
MJT/PJT, max-fare-on-missing-tap, 3-Day cap, Same-Location-Time, free bus↔rail transfers, missing-tap
correction, GV gate/deny-exit). ABT audit-schema conformance unasserted. Capping timing constants
untested (next-business-day activation, 04:00 boundary, max-fare-excluded-from-capping, deny/BIN
timing). Shift Board 0 coverage. User-claims first-login gate + operator-hierarchy scoping absent.
DWH freshness/completeness untested. Stale: C4102954 "Add new decline reasons" omits Passback —
extend + verify. Strong: Metro/UB tap-correction, iLink/ref/town capping, late-tap, debt recovery.

**Cross-cutting themes for the re-write (Phase 6):**
1. Requirement-grounded NEW coverage: NIR TOTO (ETM+ABT), POS Refund, Shift Board (ETM+ABT),
   pilot-list, heartbeat, SaaS comms-lock, DWH freshness.
2. Audit-schema conformance pass across device suites (paymentType/revenue, pounds-vs-pence, product
   ids, TotoTap rename, DeclinedReason enum incl. Metro fix).
3. Fix confirmed stale/contradicting cases (PV C4101005; ABT C4102954; verify POS/ETM flagged ones
   against full bodies).
4. Grounding pass: functional cases are systematically generic ("an operator is signed on") — apply
   the new concrete-grounding standard (real route/operator/stop/product) across all suites.
5. Reporting/config cases assert "screen/report loads" not computed values — add value oracles.

## G. Phase 6 progress (re-write)
- **Prerequisite fixed:** confirmed TestRail `get_cases` DOES return full bodies (custom_preconds/
  steps_seperated/expected/preface) — the `cases` CLI just projected them out. Full bodies available
  for safe re-analysis before editing existing cases.
- **PILOT DONE — POS `Functional / Refund`** (FBD-100373): 12 requirement-grounded cases
  C4103533–544, audit CLEAN, enriched. Whole feature was previously absent. Concrete worked examples
  (URN `01122400428500078601300`, PRN, £ amounts) per the new grounding standard; cross-device case
  tagged CR115. This is the pattern for the rest.
- **ADDITIVE COVERAGE COMPLETE (all 4 suites, audit-CLEAN, enriched) — 66 new cases:**
  - POS 30253: Refund 12 (C4103533–544) + barcode/fare-stage/heartbeat/allocation 13 (C4103570–582)
  - ETM 30254: Rail Sub / Shift Board / transfers / ABT audit 14 (C4103545–558)
  - PV 30255: barcode-reject / pilot / TOTO audit / comms-lock 11 (C4103559–569)
  - BOS-ABT 30279: NIR TOTO / capping timing / Shift Board / access-claims 16 (C4103583–598)
  Files: each suite's `requirements-additions.cases.yaml` (+ POS `refund.cases.yaml`).

### H. Existing cases flagged for George (verify / ZZ_DELETE) — NOT edited (parked on B1/B2/B3)
| Case | Suite | Issue | Action |
|---|---|---|---|
| C4101005 | PV | Asserts single-use *validates*; spec = reject single-use | **ZZ_DELETE / superseded** by new PV barcode-reject case |
| C4100439 | POS | Generic "validate by barcode", no single-use scoping | Verify vs body → supersede by new barcode cases |
| C4100440 | POS | Offline barcode overstates capability (no Ceiling-Limit gate) | Verify vs body → supersede |
| C4102954 | BOS-ABT | "Add new decline reasons" omits **Passback**; needs full enum incl. 15=BIN/20=Passback (Metro fix) | Extend + verify (B2) |
| C4100583 / C4100591 | ETM | ABT declined/invalid-tap cases may assert pre-alignment codes | Verify vs body (B2) |
| C4103487 | BOS-ABT | Late-tap-after-settlement: travel-date-vs-settlement + "Late Tap" flag not asserted | Verify/extend |

**Still parked for the end-review (need answers before editing existing cases):** B1 barcode flow
(old vs CR094), B2 Declined-Reason values, B3 CR statuses. Also: NIR TOTO exact fares/PJT values are
structural-only in the new cases — harden with FBD-100450 NIR bespoke-fares export when available.
