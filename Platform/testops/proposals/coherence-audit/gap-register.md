# Gap Register & Q&A — Translink suites

**Purpose.** Every gap the audit found is a **question**, not a silent marker. Answer each and the case gets grounded + cited. Any question **nobody** can answer is flagged **POSSIBLE DESIGN/SPEC BUG** — the tests have exposed a hole in the requirement or the system, which is a finding worth raising to the design owners.

**How to use.** Fill in the `A:` line for each. `source:` = where the answer came from (a spec section, the live system, a colleague, "confirmed from experience"). If you can't answer, leave `A:` blank and set `→ ESCALATE`. I then re-ground the affected cases (cite the answer) or mark them `**UNCONFIRMED**`, and raise the escalations.

**Q-numbers are scoped to their session/device header block, NOT globally unique.** This file grew from many parallel audit sessions across suites, each numbering its own questions Q1, Q2, ... from wherever it started — so "Q25" appears under several different session headers below, each meaning something completely different. **Never reference a question by number alone** — always say which session/suite it's under, or better, cite the **case id** (e.g. C4102766), which is the real unique key every question is anchored to. When answering or discussing a question, quote the case id and/or session header, not just "Q25".

Legend for category: **SURFACE** (does this device/portal do this action?) · **LIVE?** (specified in a CR/FBD but is it actually built/usable?) · **VALUE** (exact fare/threshold/enum) · **CONFLICT** (two cases disagree — which is right?) · **BUG?** (if unanswerable, likely a design/spec hole).

---

## A. Portal capabilities (the big one — blocks the whole ABT correction/annul area)

**Q1 · SURFACE/LIVE? · affects ~30 ABT cases (C4102757–C4102790, C4102825/826, correction family)** — ANSWERED 2026-07-21, REVERSED 2026-07-22, **REVERSED AGAIN 2026-07-23 (back to the original answer)**
Can an operator actually **change a journey's alighting stop and have the fare recalculate** (with auto refund/charge) in the **Operator Portal**?
A (George, 2026-07-21, pass 1): **Yes, live.**
A (George, 2026-07-22, pass 2, REVERSED): **No — the Operator Portal does NOT have this function.**
**A (George, 2026-07-23, pass 3, REVERSED AGAIN):** **"Just seen that you can edit alighting stage on both Passenger Portal and on the ABT Operator Portal."** Confirmed live on BOTH portals. Pass 1 was right all along; pass 2 was wrong.
source: George (live-system confirmation, all three passes — the third, most-recently-verified, is authoritative). ⇒ **ACTION NEEDED (again)**: the 61 cases reworded 2026-07-22/23 to "Passenger Portal only" (per pass 2) must be corrected a third time to state the correction mechanism is confirmed live on **both** the Operator Portal and Passenger Portal — cite FBD-100662 §5.6 for the mechanism, live confirmation in Refs only (not inline body text, per the terse rule). Note the spec's real UX distinction between the two portals still applies regardless of which pass this is: the Operator Portal shows the recalculated fare **before** confirming; the Passenger Portal does not (FBD-100662 para 693) — that's a genuine difference in mechanics, not something either reversal changes. In progress via the ABT tidy-up pass as of this entry.

**Q2 · SURFACE/LIVE? · affects the same CR122 family** — ANSWERED 2026-07-22, folded into Q1's 2026-07-23 answer
Same for the **Passenger web portal**?
A (George, 2026-07-21, pass 1): **Don't know / needs checking.**
A (George, 2026-07-22, pass 2): **"It looks like it is a thing on passenger portal yes"** — tentative.
**A (George, 2026-07-23, pass 3):** Confirmed alongside Q1 — both portals have it. No longer just "looks like", now directly confirmed.
source: George (live-system confirmation, both passes). ⇒ Passenger-portal correction cases (incl. the 5 "Correction Limits" cases C4103480–4103484) can be grounded as confirmed-live rather than left `UNCONFIRMED` on the liveness question — the only remaining open point is exact UX mechanics (Q21b), not whether the feature exists at all.

**Q3 · SURFACE · affects the whole 35-case annul/cancel section**
Does **any "cancel a journey / cancel a tap" action exist in either portal**?
A (from source): **No.** The only tap-cancellation is the **ETM driver-menu annul** — most-recent tap, within 1 minute, boarding stage unchanged (para 204). No portal cancel exists. ⇒ the condemned "cancel-in-portal" cases were correctly condemned.
source: FBD-100662 v5.00 para 204 (verbatim in the note).

**Q4 · SURFACE/BUG? · C4102830** — ANSWERED
Is there **any back-office way to void or refund an already-settled journey**?
A (George, 2026-07-21): **Yes** — on ABT you can refund a processed payment from the **Transaction History**, and that refund must then be **authorised** (an approval step, not instant).
source: George (live-system confirmation). ⇒ C4102830 as written ("cancel a charged journey") is still wrong — reground it on the real mechanism: refund a processed payment from Transaction History, requiring authorisation. Not a "cancel the journey" action.

---

## B. Device capabilities (surface confusion found by the audit)

**Q5 · SURFACE · TVM C4103628, C4103729, C4103677, barcode-collection cases** — ANSWERED
Does the real **TVM have a barcode scanner**, or is it **Collect-Ticket-Code entry only** (specs say no scanner)?
A (George, 2026-07-21): **Collect-Ticket-Code only, no scanner.** Confirms the spec.
source: George (live-system confirmation) + FBD-100317. ⇒ Correct all cases assuming a scan/present-barcode action at the TVM to Collect-Ticket-Code entry.

**Q6 · SURFACE · TVM C4103599, C4103617, ~30 "TVM Smartcards & ABT" + Mini-Statement cases** — ANSWERED
Does the real **TVM have a smartcard reader/writer**, and can it **issue/read** smartcards? (FBD-100261/100236 say issue is **POS-only** / Card-Bureau.)
A (George, 2026-07-21): **No, POS/Card-Bureau only.** Confirms the spec.
source: George (live-system confirmation) + FBD-100261/100236. ⇒ The ~30 "TVM Smartcards & ABT" cases assuming issue/read on the TVM are wrong — condemn or correct.

**Q7 · SURFACE · ETM C4100586, C4100587 (High)** — ANSWERED
On Metro / Ulsterbus **ETM (tap-on-only)**, is there **ever a customer tap-off**? (Specs: alighting is ETM-calculated / driver-selected — no customer tap-off.)
A (George, 2026-07-21): **No customer tap-off, TOO only.** Confirms the spec.
source: George (live-system confirmation). ⇒ Correct C4100586/C4100587 to TOO/driver-selected alighting mechanics.

**Q8 · SURFACE · PV C4101005 vs C4103559 (CONFLICT)** — ANSWERED
Does the **PV validate single-use barcodes**, or **multi-use only** (FBD-100167 says multi-use only)?
A (George, 2026-07-21): **Multi-use only.** Confirms the spec; C4103559 is right, C4101005 is wrong.
source: George (live-system confirmation) + FBD-100167. ⇒ Condemn/correct C4101005.

**Q9 · SURFACE · PV C4101085 vs C4103568 (CONFLICT)** — ANSWERED, then REVERSED same day (see Q23)
Does the **PV have comms failover**, or is it **Ethernet-only, no failover** (offline → out-of-service)?
A (George, 2026-07-21, first pass): **Ethernet-only, no failover.** Confirms the spec; C4103568 is right, C4101085 is wrong. ⇒ C4101085 condemned (`ZZ_DELETE_REVIEW`).
**REVERSED (George, 2026-07-21, second pass, later same session — see Q23):** a subsequent coverage-audit pass found the old suite (10047) holds real, populated `REQ-2746.0` cases (C2700890, C3275939) that explicitly test the PV failing over to cellular — directly contradicting this answer. George's ruling: **"if there is an old test case with it, then yes for now assume it has failover."** ⇒ **C4101085 restored** and reworded to ground the failover mechanism precisely on REQ-2746.0 + TIBU-24428's full ticket history (which, read past its initial bug-report preamble, confirms a working, QA-passed, bidirectional Ethernet⇌cellular failover with a named audit event, PrimaryCommsChannelFailed/812 set-clear). **C4103568 narrowed** (not reversed) to the correct trigger — sustained loss of BOTH Ethernet AND cellular together, not Ethernet alone — since a single-channel Ethernet failure now correctly fails over per C4101085. See `proposals/coherence-audit/fixes/pv-failover-restore.rewrite.json` / `.changelog.md`.
source: George (live-system confirmation, both passes); REQ-2746.0 (old suite 10047); TIBU-24428 (full ticket, not just its initial bug description); FBD-100359. ⇒ Superseded by Q23.

**Q10 · SURFACE · GV C4104030** — ANSWERED (2026-07-22, GV deep audit)
Can a **TVM-produced multi-use barcode** be validated at the **GV**? (TVM isn't a multi-use printer per spec.)
A: **Yes.** The earlier finding that "TVM isn't a multi-use printer" was itself wrong — it came from a flattened text extraction of FBD-100167's Table 1 ("Device categories") that lost the table's column alignment. Re-parsing the actual docx table (python-docx, cell-by-cell) gives the real Print/Validate matrix: **BV** (neither), **ETM** (print + validate), **GV** (validate only), **HHD** (print + validate), **POS\*** (print only), **PV** (validate only), **TVM\*** (**print only**). The `*` footnote ("POS and TVM will validate Single Use barcodes but not multiple use") refers to the *Validate* column being empty for POS/TVM, not the *Print* column — TVM's checkmark is in Print. So a TVM-produced multi-use barcode validating at the GV (C4104030) is a fully grounded, ordinary cross-device scenario, no different from the already-accepted HHD-produced case (C4104031).
source: FBD-100167 V12.00, Table 1 "Device categories" (Background section, docx table index 2), parsed cell-by-cell via python-docx to recover the Print/Validate column each device's tick belongs to (the flattened paragraph-text extraction used in both the original coherence pass and my own first read of this table lost the column mapping and produced the wrong answer twice before the table was parsed properly). ⇒ **No change needed to C4104030** — it was correct all along. The earlier gv.findings.md Medium finding on this case is superseded/closed.

**Q11 · SURFACE/BUG? · ETM C4100946** — ANSWERED
Does this **ETM have a customer-facing passenger display** peripheral (for the GDPR display case)?
A (George, 2026-07-21): **Yes, it has one.**
source: George (live-system confirmation). ⇒ C4100946 is grounded as correct — clear any doubt/gap marker on it.

---

## C. Products / entitlements

**Q12 · VALUE · POS C4100414, C4100417** — ANSWERED
Are **"Youth"** and **"Concession"** real smartcard entitlement types? (Known enum: Senior / Blind / War Pensioner / yLink / 24+ / Half-Fare / Dependants — "Youth" looks like yLink.)
A (George, 2026-07-21): **No — duplicates.** "Youth" = yLink, "Concession" = Half-Fare.
source: George. ⇒ Condemn/merge C4100414 (Youth) into the yLink case and C4100417 (Concession) into the Half-Fare case.

**Q13 · LIVE? · ETM C4102566/C4102567; POS idx 88/97/101** — ANSWERED
Is a **fare-paying / stored-value (e-purse) smartcard** a real current Translink product, or is PAYG only via cEMV contactless?
A (George, 2026-07-21): **Yes, real product.**
source: George (live-system confirmation). ⇒ Keep the ETM/POS fare-paying-smartcard cases as grounded; no change needed.

---

## D. Fare / cap values (grounding for the capping suite)

**Q14 · VALUE · ABT capping family (C4102757–C4102822, many)** — ANSWERED
The concrete values (Metro cap £4.00 / single £2.30; iLink £6/£11/£19; Ulsterbus ref.60 £7.20 / ref.61 £8.20) come from the **UB-TOO tracker**, not the committed FBD specs.
A (George 2026-07-17): fares/caps are **back-end configurable** (may change; ~90% stable). The point is **not** to assert a fixed number — the test must verify the **charge matches the configured ABT pricing rule**. ⇒ Treat the values as **examples per current config**, not gospel; oracle = the ABT pricing setup. Reframe the fare-value `UNCONFIRMED` markers to "example per current ABT pricing config; verify charge matches the configured rule" (runnable, not blocked).
source: George; back-end pricing configuration is the source of truth.

**Q15 · VALUE · TVM C4103641 (BUG?)** — ANSWERED
Should a **Scottish banknote be rejected** as "foreign/not sterling"? (Scottish notes are sterling — the expected outcome may itself be wrong.)
A (George, 2026-07-21): **Case is wrong — should be accepted.** Scottish notes are sterling; the TVM should accept them like any other GBP note.
source: George. ⇒ Fix the expected outcome on C4103641 to "accepted", not "rejected as foreign."

---

## E. Cross-case contradictions (which case is correct?)

**Q16 · CONFLICT · HHD C4103831 vs C4103883** — same expired Adult iLink at top-up → one refuses, one reactivates. Which is right? — ANSWERED (resolved from old suite, 2026-07-22)
A: **Reactivation is correct.** Old suite 5446 (C1688835, C2682243, C2682255, C2682256, C2682242/2682244/2682247/2682248) and dedup suite 13958 (C2598643) all model the same consistent flow for an expired iLink/Belfast Visitor Pass at top-up: the device shows an informational "Product/Pass Expired" screen (or, in the primary suite's later revision, no blocking screen at all), then proceeds through the ordinary Top-Up flow (period/amount select → payment → re-present card) to completion — "the Top up is issued... the smartcard is validated". None of the ~9 old-suite cases across two suites model an outright refusal. C4103831's "top-up is refused" is unsupported and stale; C4103883's "expired smartcard is topped up and reactivated" matches the old-suite evidence exactly.
source: TestRail suite 5446 (primary) C1688835, C2682243, C2682242, C2682244, C2682247, C2682248, C2682255, C2682256; suite 13958 (dedup) C2598643 — all titled "Top Up(s) - Adult/Child iLink/Belfast Visitor Pass - Expired". ⇒ **C4103831 condemned** (`ZZ_DELETE_REVIEW`, wrong/stale model). **C4103883 kept as the grounded case**, re-cited `FBD-100261,gap-register Q16 (resolved)`.

**Q17 · CONFLICT · HHD C4103835 vs C4103982** — expired-card inspection: audit `DeclinedReason=1` vs M020 "Card Declined" before any tap. Which? — ANSWERED (resolved from spec cross-reference, 2026-07-22)
A: **Not a real conflict — both are correct, describing the same event from two different audit layers.** `knowledge/translink/specs/FBD-100658-abt-audit-specification.md` documents the `DeclinedReason` enum: `1` = **Card Expired**. `knowledge/translink/specs/FBD-100716-revenue-inspection-device.md` documents event **5010** = **"Failure – Card Expired"**, raised by the same M020 card-integrity check that displays message **"Card Declined"**. C4103835 asserts the CloudFare/BOS **audit-record** view (`DeclinedReason=1`) of an expired-card inspection tap; C4103982 asserts the **on-device event/message** view (`Card Declined` + event 5010) of the identical tap. They are two facets of one decline, not competing models.
source: FBD-100658 (`DeclinedReason` enum, `1`=Card Expired); FBD-100716 (event 5010 = Failure – Card Expired, M020 "Card Declined" message) — both already indexed in `knowledge/`. ⇒ **Both cases kept, no behaviour change** — Refs updated on each to cross-reference the other and note the resolution; CONFLICT marker removed from both prefaces.

**Q18 · CONFLICT · POS C4100360 vs C4100436** — power/suspend sign-off destination (break mode skipped or not?). Which? — ANSWERED
A (George, 2026-07-21): **Break mode is used.**
source: George (live-system confirmation). ⇒ Read both live cases to determine which already models break-mode-used; keep that one, correct/condemn the other.

**Q19 · CONFLICT · ETM C4100588** — UB journey "reverts to fixed fare"; FBD-100662 makes flat-fare Metro-only now. Still valid? — ANSWERED
A (George, 2026-07-21): **No — spec is right, flat-fare is Metro-only now.**
source: George (live-system confirmation) + FBD-100662. ⇒ C4100588 is stale — condemn or correct it to remove the UB-fixed-fare-revert claim.

---

## F.5 Alighting-stop correction / "Update Stop list" family (31 ABT cases)

**Q21 · LIVE?/INVENTED · C4102757, 760–767, 784–785, 827, 833–849, C4103480–482 (31 cases)**
This whole family depends on **CR122 alighting-stop correction**, which FBD-100662 v5.00 §5.6 (paras 691–693) calls a **proposal with "full UX to be determined"**. Two things to confirm:
(a) Is CR122 **actually implemented/usable** in the test environment (operator + passenger portal)?
(b) The cases use a screen called **"Update Stop list"** and stop-list **filter rules** ("only fare > 0 stops shown", "No options", operator-match, hide zero/negative/transfer) — **none of which are in the spec** (spec says only "stops after the boarding stop on the same route"). Do these UI rules actually exist, or were they invented?
The 1/month·3/year correction **limit** (C4103480–482) *is* grounded (para 692). Everything else here → `UNCONFIRMED` until (a)+(b) confirmed.
A:
source: FBD-100662 v5.00 §5.6 paras 691–693 (proposal / UX TBD); "Update Stop" = 0 hits across all 1,197 requirement docs.

---

## F.6 Do invalid/declined taps display in the Operator Portal?

**Q22 · SURFACE/INVENTED · C4102867 "View all taps including taps not valid for a journey" (Customer Services)**
Verified from source + confirmed by George (2026-07-17): declined/invalid taps are **audit data** — `DeclinedReason` on the audit payload (FBD-100658), "stored… for historic reporting" (FBD-100307 para 460) — and surface in the **device/BOS Activity Log** (FBD-100358). The **operator/passenger portal Journey History shows journeys = valid taps with boarding/alighting** (FBD-100662 para 264). There is **no spec basis** for the portal showing invalid/declined taps to the operator. George: "it might store them in the database or logs but not visually on the portal."
⇒ **C4102867 is ungrounded** — correct it (operator views the customer's *journeys* over a date range; declined taps are verified via the Activity Log / audit, not this portal view) or remove. Marked `UNCONFIRMED` in-suite pending the Customer-Services section rewrite.
A (CORRECTED 2026-07-17 after reading full specs): **C4102867 is NOT invented.** REQ-3498.0 and PSPEC-0015 §3.3.6 REQUIRE operators to see all valid **and invalid** taps in the customer-portal view. This **conflicts** with George's confirmed live behaviour (declined taps not shown on portal). ⇒ **P1 POSSIBLE SPEC/IMPLEMENTATION CONFLICT** — either the requirement is met via the Declined Taps report + Activity Log + stored audit, or the combined portal view is genuinely missing (a defect). Escalate to product; do NOT silently delete the case. (My earlier "invented" call was wrong — it came from the distilled note, not the full spec. Citation fixes: "historic reporting" = FBD-100307 **para 367**; Journey-History anchor = FBD-100662 **para 108**.)
source: REQ-3498.0, PSPEC-0015 §3.3.6 (require valid+invalid view); FBD-100307 para 367, FBD-100662 para 108; + George's live-behaviour confirmation (the conflict).

---

## F. Feature-gating / rail-sub

**Q20 · LIVE? · ETM C4103547/C4103548; ABT rail-sub cases** — ANSWERED
Rail-substitution ABT is **gated off until NIR TOTO is live**. Is NIR TOTO live in the test environment, or should these be marked out-of-scope/UNCONFIRMED?
A (George, 2026-07-21): **No, not live yet.**
source: George (live-system confirmation). ⇒ Rail-sub ABT cases stay correctly gated/out-of-scope — no change needed, the existing gating was right.

---

---

## Session 2026-07-21 — Q1/Q2/Q4-Q9/Q11-Q13/Q15/Q18-Q20 answered by George
Answers recorded inline above. Also: George clarified the general convention for **configurable
values** (thresholds/windows/limits, e.g. a passback window) — don't hard-code a guessed number and
don't block on `**UNCONFIRMED**` either; add an assumed-knowledge precondition instead (e.g. `**GIVEN**
the tester knows the currently configured passback window`). Generalises the existing fare/cap
reframe (Q14) to any configurable value. Now baked into `docs/gherkin-standard.md` ("Unknown
*configured value*" rule). Remaining open: Q2 (passenger-portal CR122), Q10 (GV/TVM multi-use
barcode), Q16/Q17 (HHD conflicts), Q21b (Update Stop list UI specifics) — still need checking.

## Already actioned in the live suite (2026-07-17)
- **32 ABT annul/cancel cases condemned** (`ZZ_DELETE_REVIEW`) — rebuild plan in `annul-rebuild-plan.md`.
- **13 High/CONFLICT cases stamped in-suite** with `UNCONFIRMED`/`CONFLICT` markers pointing here: C4100586, C4100587, C4100588 (ETM); C4101005, C4101085 (PV); C4103628, C4103641 (TVM); C4103831, C4103883, C4103835, C4103982 (HHD); C4100360, C4100436 (POS). Answering Q5–Q9, Q15–Q19 lets me remove the marker + ground the case, or escalate it.

## Session 2026-07-21 (PV release-coverage audit, TL Validators v5.0.0/v5.0.1/v5.0.3) — new questions

**Q23 · CONFLICT/BUG? · PV comms failover — REQ-2746.0 vs FBD-100359/C4103568/TIBU-24428** — ANSWERED
Old suite (10047) has **C2700890** and **C3275939** ("Secondary Communication Failover Method",
Refs `REQ-2746.0`, created 2022/2024) that explicitly test the PV **continuing to operate on
cellular** when Ethernet fails, "as normal". This appears to directly conflict with **today's own
earlier decision in this same session**: C4101085 ("PV to BOS — communications resilience and
failover") was condemned as wrong, on the basis of FBD-100359 (Ethernet devices have no secondary/
failover channel) + George's live-system confirmation (gap Q9, "Ethernet-only, no failover").
Additional evidence pulled this session:
- **TIBU-24428** (`PrimaryCommsChannelFailed` event spamming, fixed) — the OLD suite's own
  regression case for this bug (**C4069405** / **C4091894**) states the **target/fixed** behaviour
  as: *"the PV continues to communicate over ethernet AND does not fail over to cellular"* — i.e.
  the fix itself confirms **no failover** is correct, consistent with FBD-100359/Q9.
- **TIBU-29191** (SIM remains "connected" when physically removed, still open/System Test) and
  **C4091908** (old suite, TIBU-26303 fix-check) both show the Technician Menu Network Settings
  screen displaying **both an Ethernet and a Cellular interface** on the PV — i.e. the hardware
  clearly still has a cellular/SIM component, it's just not used as a comms failover path per the
  current confirmed behaviour.
A (George, 2026-07-21, later same session): **"If there is an old test case with it, then yes for
now assume it has failover."** ⇒ Treat the PV as having a real Ethernet(primary)⇄cellular(secondary)
failover path, grounded on REQ-2746.0's old-suite case content (C2700890, C3275939) — this reverses
the earlier same-session Q9 answer/condemnation of C4101085.

**Follow-up check on the "working theory" above (this session, before applying George's ruling):**
re-read TIBU-24428 **in full** (not just the bug-report preamble the earlier pass quoted) via the
Jira issue's complete comment history. The line quoted as evidence FOR "no failover" — *"the PV
should continue to communicate over ethernet AND not fail over to cellular"* — turns out to be the
**initial bug report's own description of the spamming defect** (a *spurious* failover flapping on
a perfectly healthy Ethernet link), not a statement that failover doesn't exist as a mechanism. The
ticket's own final, QA-passed builds say otherwise: build 1.1.1151.27197 (Thomas James, 2026-01-30,
"QA PASSED") — *"PrimaryCommsChannelFailed Event 812 (Set) raised when disconnecting ethernet...
device then failed over to cellular connection... 812 (Clear) raised after reconnecting"* — and
build 1.0.9603.23768 (Thomas James, 2026-04-20, "QA PASSED") which tests and passes a full
bidirectional matrix (Ethernet+cellular → disconnect Ethernet → fails to cellular → reconnect →
fails back; cellular-only → connect Ethernet → fails over to Ethernet; etc.). So **TIBU-24428, read
in full, corroborates REQ-2746.0** rather than contradicting it — there is no residual conflict
between the two JIRA/old-suite sources; the only earlier "conflict" was FBD-100359 (which lists the
PV under Ethernet-only devices, no cellular failover described) vs. REQ-2746.0/TIBU-24428 (which
show the PV does have a working cellular failover). That gap in FBD-100359's device classification
is not resolved here (confidential source doc, out of scope) — flagged as a candidate FBD-100359
update for the requirements owner.

**Resolution applied to the suite (`proposals/coherence-audit/fixes/pv-failover-restore.rewrite.json`
+ `.changelog.md`):**
- **C4101085 restored** (title un-prefixed from `ZZ_DELETE_REVIEW`) and fully reworded to ground the
  failover mechanism on REQ-2746.0 (continues to operate on cellular, transaction identifiable in
  the back office) + TIBU-24428 (the named PrimaryCommsChannelFailed/812 set-clear event, the
  Ethernet⇌cellular bidirectional behaviour) — not the old suite's generic pre-condemnation wording.
- **C4103568 narrowed, not reversed**: its "sustained network outage drives the PV out of service"
  premise is correct but was written as if any Ethernet/Translink-network outage alone triggers it;
  narrowed to the correct, more specific trigger confirmed by TIBU-24428's own QA matrix — a
  sustained loss of **both** Ethernet and cellular together. A single-channel Ethernet failure now
  correctly fails over (per restored C4101085) rather than driving the PV out of service.
- **C4103569** ("transactions queued during an outage are delivered on restore") needed no change —
  it already describes the both-channels-down/total-outage recovery case, which stays valid either way.
- TIBU-29191 stays folded into C4101016 as a status-reporting assertion only (unchanged) — that was
  never dependent on the failover question.
source: REQ-2746.0 (old suite 10047, C2700890, C3275939); TIBU-24428 (full ticket, all 17 comments,
not just the bug-report preamble); FBD-100359; gap-register Q9 (reversed); George's directive,
2026-07-21.

**Q24 · VALUE/LIVE? · TIBU-30923 (PV/GV, "Devices cannot apply brand new configuration settings at
the same time as a software update")** — status QA TEST, no described fix/expected behaviour in the
ticket, only the observed limitation (a new TMS parameter unknown to current software isn't applied
until a second distribution, when software adding support for it is deployed in the same
distribution as the new parameter).
A: Don't know / needs checking — is the **intended fix** "apply both in one distribution" (i.e. this
is being fixed for v5.0.0/5.0.1/5.0.3), or is "deploy config then redeploy software" an **accepted
permanent two-step procedure**? A case can't be authored without knowing which behaviour to assert.
source: TIBU-30923 description only (no FBD/REQ found, no old-suite case). ⇒ Left as a **GAP** in
`proposals/pv-release-coverage/coverage.md` — no case authored pending George's answer.
**A (resolved from full Jira ticket, 2026-07-22):** re-read TIBU-30923 in full via the Atlassian MCP
(not just the description quoted above) — it carries a QA test-coverage comment from Thomas James,
2026-05-14: *"Tested on PV v1.1.1284.24210. **QA PASSED**. This was tested by deploying an old version
of application software which doesn't include functionality such as Multi-Use Barcodes and EMV. Then
updating to v1.1.1284.24210 which has Multi-Use Barcodes and EMV functionality to then validate that
once deployed to the device the new functionality is working as the configuration need for those
features has been applied via the dataset."* So **for the PV specifically, the intended fix is
confirmed as "apply both in one distribution"** — the ticket is only still open (status `QA TEST`,
not closed) because the equivalent check hasn't been run on **GV** yet (a second Thomas James comment,
2026-07-20: "Note this still needs to be tested on GV") — that's a GV-scope loose end, not a PV one.
source: TIBU-30923 full ticket (description + both comments), pulled via the Atlassian Rovo MCP,
2026-07-22. ⇒ No live PV case currently exists to reground (none was authored pending this answer,
per the original note) — flagging here that a case **can now be authored** in suite 30255 asserting:
"a new TMS config parameter unknown to the current software is correctly applied as soon as software
adding support for it is deployed in the same distribution" (QA-passed on PV v1.1.1284.24210). Not
authored in this pass (scope was resolving the gap-register question, not net-new coverage) —
candidate for a future `/add-feature` or release-coverage pass.

## Session 2026-07-21/22 — TVM deep-audit (suite 30284, full-suite citation re-verification)

**Q30 · GROUNDING/BUG? · TVM Payments — EMV & Contactless section (887780), 15 cases
(C4103657–4103670, C4103672, excl. C4103671)** — systemic mis-citation found
Every case in the section cites **FBD-100320** as its sole/primary Refs. Read the full FBD-100320
doc (`TID Management - Embedded & Non-Embedded Payment Devices V5.03`) directly via
`tools/extract_req.py` — it is **entirely** about TID/TK terminal-credential allocation
(serial-number mapping, NMI Terminal Groups, deallocate-before-reallocate). Zero mentions of PAN,
PIN, contactless, transaction limit, or mask anywhere in the document. It does **not** cover any of
the actual claims under test: card approval/decline, PIN timeout, Amex/Diners acceptance,
min/max transaction value, contactless tap limit, mobile wallet, PAN masking on receipt/back office,
print-failure voiding a card payment. Checked the only other TVM-adjacent hardware doc,
**FBD-100183 (POS Hardware Spec)** — it documents the **Miura M020** (the **POS** payment terminal),
not the TVM's **Ingenico** terminal, so it doesn't apply either. Searched `REQS_DIR` for
EMV/Ingenico/PIN/contactless/P2PE-specific specs — **none exist in the library**.
Is there a governing TVM/Ingenico payment-terminal integration spec (or PCI/EMV certification
doc) held elsewhere that should replace FBD-100320 as these 15 cases' citation? If not, are these
claims accepted as standard EMV/PCI terminal behaviour needing live confirmation rather than a
bespoke Translink citation?
A (resolved from old suite, 2026-07-22): **Yes — a governing citation exists, it's just not an FBD
document.** Old suite 6160 ("R:2 - MAN - FNC - TVM", EMV Payments section) and 22276 ("TVM Astreo —
Cash and EMV Cards") contain ~90 near-identical EMV/Contactless/Chip&PIN/mobile-wallet cases citing
a **REQ-#### requirement scheme** (not FBD) — e.g. REQ-0097/0295/0340/1488/1489/1490/1515/1591/1630/
1722/2519/2583 — that map claim-for-claim onto the 15 new-suite cases: Amex/Diners acceptance
(C1831439/440/669), contactless-limit fallback (C1831356-396), mobile wallet (Apple/Google/Samsung
Pay cases), declined-card retry/cancel (REQ-1409/1515/1591), print-failure-voids-payment
(REQ-1515/1591/0847), expired/blocked card (C2041433/2041437, REQ-1519), and — most tellingly —
**PAN masking, which names the terminal explicitly**: C2132851 "PAN Not Shown on Card Receipt",
C2132852 "**PAN Not Shown on Ingenico Device**", C2132853 "PAN Not Shown in Cloudfare" (REQ-1723/
1630). This confirms both the terminal identity (Ingenico) and that PAN-masking is a real, tested,
cited requirement. The one case with no old-suite REQ either (C4103658, "no PIN entered") is a
pre-existing gap in the old suite too, not a new problem.
**Upgraded same session:** a sibling POS gap-resolution pass found `TFTS Requirements Matrix.xlsx`
(`1_Requirements\TFTS Project Delivery Matrices & VCRMs\` in `REQS_DIR`) — a genuine REQ-id index
with full requirement text + sign-off status, readable via `openpyxl` (not previously searched for
by name; `extract_req.py --find` only matches filenames, and nobody had tried this one). Looked up
every REQ id used above — **all Signed-Off (S4)** — and it directly names the TVM's terminal and
behaviour: **REQ-1515.0** "Support Chip and PIN on the TVM" (contact/contactless/mag-stripe
integrated PCD), **REQ-1515.1** "Device Fitted with EMV Contactless Reader", **REQ-1630.3** "TVM
Payment Channels" ("The TVM payment terminal shall accept Sales payments only and not reversals or
refunds"), **REQ-1723.0** "Mask Account Data on reporting displays", **REQ-1722.0** "Mask account
data on tickets", **REQ-1519.0** "Fraud Checks" (PAN valid/not expired/frequency/limit — grounds
expired-or-blocked-card rejection), **REQ-1409.x/1591.x** (passenger advisement on payment/EMV
decline). This *is* the "governing TVM EMV terminal spec" the question asked for — it was never
missing, just held in a spreadsheet, not an FBD document. The `extract_req.py` REQ-id→text gap
(POS Q25) is now closed for these ids specifically (verified directly via openpyxl this session);
extending `extract_req.py` itself to index this workbook is a good fast-follow, not a blocker.
source: old suite 6160 (EMV Payments / EMV Regression / Edge Case Tests) + 22276 (TVM Astreo — Cash
and EMV Cards); `TFTS Requirements Matrix.xlsx` "Description" sheet (Alias/Name/Notes/Status columns,
read via openpyxl), all cited REQ ids confirmed **S4: Signed-Off**; case-by-case REQ mapping in
`tvm-deep-audit-resolution.rewrite.json`. ⇒ Refs on all 15 cases (+ C4103672) updated from the Q30
gap-pointer to the matched, now-verified REQ-#### citations, pushed to suite 30284, 2026-07-22. No
case body/behaviour changed — same as the original pass, only Refs.

**Q31 · GROUNDING · TVM Commissioning/Config-Topology — "home location sets selling operator /
fares triangle" cluster, 7 cases (C4103740, 4103746, 4103758, 4103759, 4103760, 4103761, 4103762)**
— systemic mis-citation found
All 7 cite **FBD-100296** (Stop, Route & Service Management in CloudFare). Read the full distilled
note + doc scope: FBD-100296 is about **TransXChange-sourced routes/map-points and ETM route-entry
UI** — nothing about Device Home Location, operator assignment, or fare-triangle product
availability. The better-matching doc for "home location" is **FBD-100383 (TFTS Operator
Hierarchy)** — it explicitly defines **Device Home Location** per operator (e.g. "Metro TVM
Devices") and the visibility/config-inheritance model. The "fares triangle" concept itself (why a
destination outside the triangle has no product) is documented in **PSPEC-0014 (CloudFare — Fares
and Topology Manager) §9 Fare Triangle** — confirmed present via `extract_req.py`, not yet in this
repo's `knowledge/`. Neither doc explicitly states "**home location** limits **which fare-triangle
products** are sellable" as one joined rule — that linkage is inferred, not read verbatim in either
source.
Is the home-location → sellable-products-via-fares-triangle mechanism documented as one linked rule
anywhere, or is this an assumed/observed integration between two separately-documented concepts?
A (resolved from old suite, 2026-07-22): **Yes — the joined mechanism is real and old-suite-tested,
even though no single spec states it as one sentence.** Old suite 6160 ("Configuration Topology"
section) has four cases that directly demonstrate the join: **C1831895** "New Location set as Home -
Locations within Fares Triangle Available with **Correct** Operator", **C1831903** "...**not**
available with **Different** Operator", **C1831899** "Home location - Amend Boarding Location to
another in Fares Triangle", **C1831904** "Select to Travel to Location not within Fares Triangle".
C1831895's precondition is literally "TVM home location has been amended to the location in EMS
where TVM is expected to be", and C1831903's is "EMS Home location is amended to different home
location, AND TVM has rebooted after amendment" — i.e. the old suite's own test design changes home
location and then checks which destinations/products become (un)sellable, which is exactly the
"joined rule" this question asked about. Home Location itself is REQ-2710.0 (C1831732/733).
Also resolves **C4103762** (sub-location 3-digit ID format, previously a bare gap pointer): old
suite C1831422-425 ("Sub Location - Amend to 2 Digits / Input Text for Sub Location ID / Add Symbols
/ Amend to Another Valid 3 Digit ID", all REQ-2710.0) directly test the 3-digit format claim.
**Upgraded same session** (per the `TFTS Requirements Matrix.xlsx` find, see Q30 above): REQ-2710.0
is **S4: Signed-Off**, titled "As an Engineer, I need to be able to modify the configuration of a
device in the field", and its description explicitly lists "Default Boarding Location, Home
Location, Sub Location, Brightness..." as the covered fields — directly confirming Home Location
and Sub Location are one governed requirement family, not a guess.
source: old suite 6160, section "Configuration Topology" (C1831895, C1831899, C1831903, C1831904)
and "Location Settings / Home Location" + "Sub Location" (C1831732, C1831733, C1831420-425), all
REQ-2710.0 (verified **S4: Signed-Off** in `TFTS Requirements Matrix.xlsx`); FBD-100383 (Device Home
Location); PSPEC-0014 §9 (Fare Triangle). ⇒ Refs on all 7 cases updated to add REQ-2710.0 and the
old-suite pointer (`tvm-deep-audit-resolution.rewrite.json`), pushed to suite 30284, 2026-07-22. No
case body/behaviour changed.

**Q32 · GROUNDING · TVM Commissioning/Config-Deployment cluster, 7 cases (C4103741–4103745,
4103747, 4103748)** — no source document found
All cite **FBD-100385** (CloudFare Configuration Data Exports). Read the full distilled note: that
spec's scope is explicitly **portal/config-export reports only** ("Reports module → Topology
submodule") — it does not document the **device-side** TMS dataset-deployment mechanism these cases
actually test (immediate vs future-dated activation, partial-deployment success/failure reporting,
a coin-vault-threshold config push, EMV-only-mode toggle). Searched `REQS_DIR` for
TMS/dataset/deployment/rollout/activation/software-named documents — **none exist**.
Is there a TMS/device-deployment spec (distinct from the CloudFare export-report spec) held
elsewhere that should ground this cluster?
A (resolved from old suite + TFTS Requirements Matrix, 2026-07-22): **Yes.** Old suite 6160 has a
whole "TVM / Deploy the Software, Configurations & Topology" section (with "Failed Deployment" and
"Scheduled - Pre-Deployment" subsections) covering every claim in this cluster: **C1831885** "New
Complete Dataset available - Scheduled For **Immediate** Activation from Cloudfare", **C1831886**
"...Scheduled For **Future** Activation from Cloudfare", **C1831403/404** "Print/View Software
Versions Report - After Some software has Successfully Updated and others have Failed to Install"
(partial-deployment success+failure reporting), **C1831883** "Configure TVM **Coin Vault
Threshold**", **C1831884** "Configure **EMV only Mode** for TVM" (exact match for every named claim
in the question — immediate/future activation, partial-deployment reporting, coin-vault threshold,
EMV-only toggle). Verified the REQ ids these old cases cite against `TFTS Requirements Matrix.xlsx`
— all **S4: Signed-Off**: **REQ-0551.5** "Date Software Configuration data" (advance-date
scheduling), **REQ-0551.6** "Distribute software configuration data" (manual/automatic trigger),
**REQ-0680.0** "Device Stores Downloaded Files With **Future Date of Activation**" (names TVM
explicitly), **REQ-2727.0** "TVM...Check and Download Configuration Updates from the Back Office",
**REQ-2720.0/2720.2** (Engineer prints/reviews config/report data logs from a device),
**REQ-0847.5** "Configure TVM Coin Vault Thresholds", **REQ-3294.0** "...configured to operate in a
'EMV Card Only' payment mode". This is the "TMS/device-deployment spec" the question asked for — it
exists, just as a REQ-numbered requirement set (in the spreadsheet, not an FBD doc), not previously
searched for by name.
source: old suite 6160 ("TVM / Deploy the Software, Configurations & Topology", incl. "Failed
Deployment"/"Scheduled - Pre-Deployment" subsections) + 22275/22270 (Astreo/Kiosk EMS&TMS mirror
sections, C3546221/222/250-253); `TFTS Requirements Matrix.xlsx` "Description" sheet (all cited REQ
ids confirmed S4: Signed-Off). ⇒ Refs on all 7 cases updated from the Q32 gap-pointer to the matched
REQ-#### citations (`tvm-deep-audit-resolution.rewrite.json`), pushed to suite 30284, 2026-07-22. No
case body/behaviour changed — the deployment behaviour described was already accurate, only
uncited.

**Q33 · CONFLICT/BUG? · TVM C4103793 "WAN-to-SIM failover" vs FBD-100359's Ethernet-device
classification** — same pattern as the PV Q9/Q23 saga, not yet resolved
C4103793 asserts a Kiosk TVM fails over from WAN to a SIM/cellular connection and reports the event,
then reverts to WAN on recovery. FBD-100359 (SaaS Network Impact) explicitly lists **Retail Kiosk**
under **"Ethernet devices… assumed routed through the Translink network"**, with the documented
failure mode being **offline → comms-locked Out of Service** — no cellular-failover path is
described for Ethernet devices, mirroring the exact "no failover" reading that was initially applied
(then reversed on old-suite/TIBU evidence) for the **PV** in Q9/Q23. Unlike the PV case, no old-suite
(`10047`) case or TIBU ticket was checked for TVM-specific WAN/SIM failover evidence in this pass —
time did not allow it.
Does the Kiosk TVM have a genuine WAN(Ethernet)↔SIM(cellular) failover path (as the PV turned out to
have), or is FBD-100359's Ethernet-only classification correct for the TVM specifically (unlike the
PV)?
A (resolved from old suite + JIRA, 2026-07-22): **Yes — genuine, bidirectional failover, exactly
like the PV.** Old suite 6160 and 22270 (Kiosk EMS&TMS) both carry **C1831873** / **C3544437** "TVM
Comms on SIM - Comms Event Reported to Cloudfare" (Refs REQ-2399.0/2399.1/2450.0/2589.0/2741.0/
**2746.0** — the same REQ-2746.0 family used for the PV's failover, Q23), whose precondition is
"LAN is disconnected from TVM so TVM is running on SIM for comms" and whose **expected result is
verbatim**: *"TVM continues to operate as normal and report to Cloudfare over SIM when the LAN
connection fails"* + *"Events and transactions are correctly reported to Cloudfare over both SIM and
LAN connection."* Old suite 6160 also has the bidirectional pair **C2038470** "Kiosk - Comms WAN
Failure - Fallback to SIM - Event Raised" and **C2038471** "Kiosk - Comms over SIM Returns to WAN"
(REQ-0847.6, REQ-2746.0). Searched JIRA (`searchJiraIssuesUsingJql`, same technique as the PV
Q9/Q23 resolution) and found direct, closed-bug confirmation: **TIBU-13485** ("TVM: Tickets
purchased with Sim only and LAN Connection do not have any Cloudfare Activity...") describes an
explicit repro — *disconnect LAN, complete a card purchase of 5 tickets over SIM, reconnect LAN,
complete another purchase* — with the **expected** result being Cloudfare shows "Sim Only" and "LAN
restored" messages; this is functional continuity (ticket sales keep working), not just an event
log. **TIBU-15938** (closed) is the matching "comms event not reported" defect for the same
disconnect/reconnect scenario. **TIBU-4128**/**TIBU-4682** confirm the physical hardware — the
Kiosk TVM's cellular modem is a named **Teltonika** modem, tracked via activity events (code
1900/1901). Also confirmed **REQ-2746.0** itself in `TFTS Requirements Matrix.xlsx`: "As an
Administrator I need to configure the **secondary communication failover method**, so that my
device can continue to communicate and exchange data in the event of a failure of the primary
method" — **S4: Signed-Off**, applies across device types (same requirement family used for the
PV). ⇒ This reverses the "Ethernet-only, no failover" reading, exactly as happened for the PV in
Q9/Q23 — **FBD-100359's Ethernet-device classification is stale for the TVM too**, same gap as
flagged for the PV, candidate FBD update for the requirements owner (out of scope to edit here,
confidential doc).
source: old suite 6160 (C2038470, C2038471, C1831873) + 22270 (C3544437), all REQ-2746.0 family;
TIBU-13485 (closed, full description read), TIBU-15938 (closed, full description read), TIBU-4128,
TIBU-4682 (Teltonika modem), pulled via Atlassian Rovo MCP 2026-07-22; `TFTS Requirements
Matrix.xlsx` (REQ-2746.0 confirmed S4: Signed-Off); PV Q9/Q23 precedent. ⇒ Refs on C4103793 updated
from the Q33 conflict-pointer to the confirmed citation (`tvm-deep-audit-resolution.rewrite.json`),
pushed to suite 30284, 2026-07-22. No case body/behaviour changed — C4103793 was already correct.

**Q34 · GROUNDING (systemic, not case-specific) · ~52 TVM hardware/procedural cases across
Payments-Cash (887777, minus C4103649/4103653), Note Recycler & Change (887778), Coin Recycler
Hopper (887779/887795), EMS/TMS misc (887793, minus the FBD-100266/100296(now 100383)/100385-cited
ones), Alarmboard & Enclosure (887794), and the hardware-state half of Resilience (887796, minus the
comms-cited cases)** — no requirement document exists for this layer at all
These cases carry **no Refs** and describe directly-observable physical/procedural device behaviour:
coin/banknote validator acceptance-and-rejection rules, escrow limits, BNR/Astreo note-recycler jam
states, coin-recycler hopper replace/reload, Kiosk alarmboard siren/LED/temperature/UPS/door/speaker/
fan tests, TL80 printer alignment, touchscreen self-test, EMS role access, volume/brightness
persistence, ticket-roll-length correction, degraded/amber states, low-change vouchers, cash lockout
limits, and the 98% cash-acceptance / launch-time performance targets. Searched `REQS_DIR` by
filename for every plausible keyword (cash, hardware\*, printer, alarm, BNR, note acceptor, escrow,
lockout, degraded, AML/laundering/cash-limit/suspicious/revenue-protection) — **no FBD/REQ document
in the library covers TVM physical hardware or EMS-maintenance procedures**; this is presumably
vendor/OEM (Astreo/Kiosk/TL80) hardware-acceptance documentation that was never in scope for this
requirements library. The original 2026-07-17 coherence audit already called this whole area
"clean" — but that pass checked internal coherence only, not citation-to-source, which is what this
pass adds.
Is there an OEM/vendor hardware-acceptance spec (Astreo, Kiosk, TL80, alarmboard) that should be
added to `REQS_DIR` for future citation on this cluster, or is direct live-hardware observability
(a tester can verify "does this coin get accepted" without a business spec) the accepted evidence
standard for this layer, as the "clean" 2026-07-17 verdict implicitly assumed?
A (substantially resolved from old suite + TFTS Requirements Matrix, 2026-07-22): **The premise was
wrong — a governing REQ-numbered spec covers most of this layer; it was never "no requirement
document at all", just not an FBD document and not previously searched for.** Old suite 6160/22270/
22275 cite REQ-#### for nearly every category in this cluster (cash/coin/banknote validation
REQ-0339.x, Bank-of-England/other-currency-issuer acceptance REQ-1491.0, coin-vault threshold
REQ-0847.5/0847.7, burglary/alarm REQ-2369.x/2785.0, device revenue-lockout REQ-2690.0, comms-lockout
REQ-2576.0, cash-collection/hopper reports REQ-2720.x, volume/brightness persistence REQ-0511.x,
ticket-roll-length REQ-0848.0, audio speech prompts REQ-0279.x/1687.0, engineer/EMS sign-in
REQ-2731.0). Verified every one of these against `TFTS Requirements Matrix.xlsx` (`1_Requirements\
TFTS Project Delivery Matrices & VCRMs\`, an `openpyxl`-readable REQ-id index with full text +
sign-off status — not previously searched for by name; a sibling POS gap-resolution pass found it
independently the same session) — **all Signed-Off (S4)**, and several are exact, TVM-specific,
verbatim matches for claims this question said had zero documentation: **REQ-0339.11** "Acceptance
of Valid Coinage by TVM" — *"The TVM shall accept coins with an acceptance rate of **98%** of valid
tender coins upon insertion"* — and **REQ-0339.13** (identical for banknotes) are the literal "98%
cash-acceptance target" the question called undocumented. Applied this to 36 of the cluster's cases
(cash/coin/banknote validation, escrow return, change/vouchers, coin-recycler-hopper reports, EMS
sign-in, ticket-roll-length, volume/brightness, audio prompts, device lockout, the 98% acceptance
case). **Genuinely still uncited** (no REQ or old-suite match found for these specific claims even
after this pass): BNR/BNA note-recycler jam/error states (C4103650-4103652), print-failure-returns-
cash (C4103648, C4103784), the Kiosk alarmboard hardware diagnostics (siren/LED/temperature/UPS/
door/speaker/fan/TL80-alignment/touchscreen/on-screen-keyboard, C4103768-4103777), degraded/amber
states (C4103780/4103781), mains power failure (C4103785), screensaver/multi-modal home
(C4103794/4103796), and launch-time performance (C4103798) — these remain a smaller, genuine
residual gap (plausibly OEM/vendor Astreo/Kiosk/TL80 documentation outside this requirements
library, or simply not yet matched to a REQ id), not blocking, still directly checkable on live
hardware.
source: old suite 6160/22270/22275 (per-category REQ citations, see case-by-case mapping in
`tvm-deep-audit-q34-resolution.rewrite.json`); `TFTS Requirements Matrix.xlsx` "Description" sheet
(all cited REQ ids confirmed S4: Signed-Off, read via openpyxl 2026-07-22). ⇒ Refs added (previously
none) on 36 cases across Payments-Cash, EMS & TMS Maintenance, and Resilience
(`tvm-deep-audit-q34-resolution.rewrite.json`, pushed to suite 30284, 2026-07-22); the smaller
residual list above stays uncited, genuinely open, not escalated further (low-risk, directly
checkable, consistent with the original "clean" 2026-07-17 coherence verdict). No case
body/behaviour changed.

## Session 2026-07-22 (ETM deep spec-grounding audit, suite 30254) — new questions

**Q25 · LIVE?/VALUE · ETM C4100945 "Regression — Deny/BIN list download and update"** — ANSWERED
Case claims the ETM is "configured for Open Payments" with a "Deny/BIN list" and that a "FEIG" reader
performs concurrent comms during a list update (defects 301106, 302090). Searched the requirements
library for "FEIG" and "Open Payments" — no hits. Only a design-options doc (`Deny List Tile
Options.docx`) confirms a deny/negative-list concept generally (devices download a list, CloudFare
tracks the version) but not the FEIG hardware or "Open Payments" configuration terms this case uses.
A (resolved from old suite 4943, 2026-07-22): **Confirmed — same terminology, same defects, in the
old suite's own tests.** `TestRailClient.get_cases(42, 4943)` search for "feig"/"open payment"/"bin
list"/"deny list" turns up **C2547104** ("302090 - Open Payments Service - Deny or BIN List Updates
while FEIG is doing Comms Call") — tied to the **exact same defect number (302090)** this live case
cites — plus **C2536476**/**C2543245** ("301106 - Deny List is not Downloaded to Device" / "Deny List
Downloads Daily") — tied to the **exact same defect number (301106)**. The old suite's own section is
literally titled "Open Payments Service" for this defect pair, and all three cases use "FEIG"
(the reader hardware) and "Deny/BIN list downloaded from the BOS" exactly as C4100945 does. Old-suite
test evidence for the identical defect numbers counts as grounding per George's directive (exhaust
old-suite before escalating).
source: old suite 4943, C2547104, C2536476, C2543245 (pulled via `TestRailClient.get_cases(42, 4943)`,
2026-07-22). ⇒ **GAP marker removed** from C4100945's preface; reworded via
`proposals/coherence-audit/fixes/etm-gap-resolution.rewrite.json`, pushed to suite 30254, re-audit
CLEAN.

**Q26 · SURFACE/HOW · ETM C4100545 "FLU — currency switch to Euro and back"** — ANSWERED
Case claims the **alighting-stage key** is the control that toggles the FLU sale currency between
Pounds and Euro. The Euro currency state itself is real (screen `07_0_4 Main Screen - Currency is
Euro` exists), but no FBD/spec documents a currency control or an alighting-stage-key overload
(searched "currency", "Euro" — no hits in the requirements library).
A (resolved from Overflow UX flow annotations + old suite 4943, 2026-07-22): **Confirmed — the
Alighting Stage key is the currency toggle, two independent sources agree verbatim.**
`knowledge/flows/etm-flow-annotations.md` (current Overflow design export, both the 'FLU' and 'FLU
2.0 Navigation' boards) states: "The user can select an alighting stage. To change the currency, they
can press the alighting stage key again, this will change the currency to €. To change back to £, the
user can press the alighting stage key for a third time to toggle it back." Independently, **old
suite 4943's C2471550** ("7.0.4 Main Screen - Currency is Euro") — a real prior test of the same
screen — confirms the identical mechanism verbatim in its own preface (drafted against an earlier
Overflow board of the same screen, pre-R2.1). Two independent sources (current UX design + old-suite
test) agree exactly on the mechanism.
source: `knowledge/flows/etm-flow-annotations.md` (Overflow export, "FLU"/"FLU 2.0 Navigation" boards);
old suite 4943, C2471550 (pulled via `TestRailClient.get_cases(42, 4943)`, 2026-07-22). ⇒ **GAP marker
removed**; case now asserts the Alighting Stage key (press twice → Euro, a third time → back to
Pounds) as fact, via
`proposals/coherence-audit/fixes/etm-gap-resolution.rewrite.json`, pushed to suite 30254, re-audit
CLEAN.

## Session 2026-07-21/22 — POS deep-audit pass, suite 30253 (full citation-grounded sweep)

**Q25 · VALUE/traceability · POS C4099912, C4099913 (Sign On, REQ-0050/0056/0276/2821/3013)** — ANSWERED
`tools/extract_req.py --find` matches on document **filenames** only; there is no local REQ-id→document index, so `REQ-####` refs already on many POS cases can't be independently re-verified against real spec text with current tooling (unlike `FBD-#####` refs, which resolve to a real doc). Is there a REQ-id index/mapping we should be using, or do these REQ ids come from a system outside `REQS_DIR`?
A (resolved from broader spec re-search, 2026-07-22): **The tooling-limitation premise was wrong — a real REQ-id index does exist locally.** `REQS_DIR\1_Requirements\TFTS Project Delivery Matrices & VCRMs\TFTS Requirements Matrix.xlsx` (and its sibling `EXCEL VERSION TFTS Project Delivery Matrix.xlsx`) is a full REQ-id catalogue with description, device applicability, test/acceptance status per REQ. `extract_req.py --entry "TFTS Requirements Matrix" --terms "REQ-0050"` etc. resolves all five REQ ids on C4099912/C4099913 to matching, on-topic requirement text (REQ-0050.0 sign-on auth, REQ-0056.0/1 message of the day, REQ-0276.0 colour/word of the day, REQ-2821.0 PIN masking, REQ-3013.0 single integrated POS) — the earlier "no index" claim came from only searching filenames matching `FBD-`/doc-name patterns, not searching for "matrix"/"REQ" itself. ⇒ Both cases confirmed correctly grounded; no case-body change needed (Refs were already right). Tooling note for future audits: search `--find "matrix"` or `--find "REQ"` before concluding a REQ id is unverifiable.
source: `REQS_DIR\1_Requirements\TFTS Project Delivery Matrices & VCRMs\TFTS Requirements Matrix.xlsx` (broader spec re-search, 2026-07-22).

**Q26 · LIVE?/traceability · POS C4099946 (NIR Operator — Excess Ticket)** — ANSWERED
Case asserts "Excess Ticket is rail-only, available in the Operator menu", backed only by a TIBU bug-fix pin (TIBU-24804) — no FBD found by filename/content search across the local requirements library. Is there an FBD backing this, or is it a live-system-only fact only ever pinned by the TIBU ticket?
A (resolved from old-suite evidence, 2026-07-22): Old suite 9317 has a real, populated regression case for this exact defect: **C4078764** "TIBU-24804: TL POS Rail- Operator Menu- Excess Ticket Feature doesnt exist" (section `Confirmation Tests`), whose description is the literal TIBU-24804 bug report — signed on to Rail, pressed 'P', Expected: Excess Ticket option present, Actual: missing. The Excess Tickets feature itself is also tested pre-regression under old suite section **"NIR > NIR Operator > NIR Operator Menu"** (C4069393/4069394/4069397 — the section confirms an NIR/rail home, even though one case's precondition text has a copy-paste "set to Metro" artefact from a sibling smartcard case, not a genuine Metro-mode claim). ⇒ TIBU-24804 is not a bare bug-tracker reference — it is grounded in a real, populated old-suite case matching the live case's exact claim. No wording change needed to C4099946 (already correct); confirmed via old suite, not just a TIBU pin.
source: TestRail suite 9317, C4078764 (regression case, `Confirmation Tests` section), C4069393/4069394/4069397 (`NIR Operator Menu` section) — old-suite pull, 2026-07-22.

**Q27 · LIVE? · POS C4103581 (Comms & Status — Heartbeat)** — ANSWERED
FBD-100266 V3.00 frames the StaffList-reuse heartbeat mechanism (CloudFare "StaffList" message type, Hours-Since-Last-Communication reset to zero) as a **proposed** solution ("if we were to implement this... successful demonstration of this functionality"), not an asserted-shipped fact. Is Method 2 confirmed live on the current CloudFare build, or still just the documented proposal?
A (resolved from broader spec re-search, 2026-07-22): **Yes, confirmed delivered.** Re-reading FBD-100266 V3.00 past the paragraphs originally cited: its own Summary (para 174-175) states "The use of Method 2 has now been agreed with Translink subject to agreement of the heartbeat reporting solution in CloudFare" — a decision, not a floated idea — and para 165-168 verbatim matches the case's exact mechanism (StaffList message type, Hours Since Last Communication reset to zero, flows into Asset Manager). Independently, `TFTS Requirements Matrix.xlsx`'s REQ-0602.4 (the CloudFare dashboard-tile requirement, explicitly "Subject to the agreed functionality described in the Device Heartbeat Functionality and Reporting version 3.00 document") carries status **"Accepted by customer"**, and its linked design-query tracker log ("R1.1 - Device Heartbeat Requirements") states outright: *"15/02 TM: ... The function has been designed, developed and delivered"* — the only later exception noted is device-specific to the **ETM** ("04/03 TM: ETMs currently don't do heartbeat function... to be discussed if this is acceptable"), which does not apply to this POS case. Old suite 9317 has zero heartbeat/StaffList cases, so this is resolved by the requirements-matrix/design-query evidence, not old-suite. ⇒ **UNCONFIRMED marker removed** from C4103581; Refs tightened to FBD-100266 para 148/165-168/174-175 + REQ-0602.4.
source: FBD-100266 V3.00 paras 165-168, 174-175 (Summary); `TFTS Requirements Matrix.xlsx` REQ-0602.4 + its "R1.1 - Device Heartbeat Requirements" design-query log — broader spec re-search, 2026-07-22. Applied: `proposals/coherence-audit/fixes/pos-gap-resolution.rewrite.json`.

**Q28 · VALUE · POS C4100427 (Validation — Funded-group entitlement smartcards)** — ANSWERED
Is "Half-Fare" the actual CloudFare/on-screen umbrella ticket-type name applied to the Funded-group sub-types (Partially Sighted, Learning Disability, No Driving Licence, DLA), or are these distinct standalone entitlement types that only coincidentally share a fare rate? (Relevant to the already-closed Q12 Youth/Concession=yLink/Half-Fare dedup — this checks whether the same umbrella logic extends correctly to the Funded group.)
A (resolved from old-suite evidence, 2026-07-22): **Yes, confirmed.** Old suite 9317 holds 5 (×3 duplicated) real, populated cases explicitly titled "**X Half Fare Smartcard**" for this exact cluster: C4072936/45 (NDL = No Driving Licence), C4072937/41/47 (Partially Sighted), C4072938/42/48 (LD = Learning Disability), C4072939/43/49 (PIPS), C4072940/44/50 (**DLA**) — all sharing the identical precondition/step template ("The User Presents the Half Fare Card to the POS" → ticket type changes to Half Fare). This confirms "Half-Fare" is the applied umbrella name across the whole Funded sub-group, including DLA (previously hedged in the case as merely "also an entitlement card" rather than confirmed under the same umbrella). ⇒ Preface tightened from equivocal to confirmed wording; no behavioural change.
source: TestRail suite 9317, C4072936-40 (+ duplicates C4072941-50), all titled "X Half Fare Smartcard" — old-suite pull, 2026-07-22. Applied: `proposals/coherence-audit/fixes/pos-gap-resolution.rewrite.json`.

**Q29 · SURFACE · POS C4100363 (Non-Functional / Comms — "recovery reconnects and syncs")** — ANSWERED
No FBD or Overflow flow-doc text found describing the reconnect-and-sync-outstanding-transactions behaviour on CloudFare recovery (its mirror case, C4100362 "loss enters Communication Locked", is TIBU-pinned; this one has no ref at all). Is this behaviour documented anywhere, or is it an assumed inverse of C4100362 that's never been separately specified/tested?
A (resolved from broader spec re-search, 2026-07-22): **Yes — REQ-2589.0** in `TFTS Requirements Matrix.xlsx` (applies to POS (All) among other devices; status "Requirement customer signed off"): *"As an Operator I want my device to resume sending after communications interruption, so that I can prevent data loss. GIVEN the device has stored the details of the data interruption WHEN the device communication is interrupted THEN the device will initiate a communication session and resume sending."* This directly grounds the case's claim. Old suite 9317 has no mirror case for the reconnect/resync direction (only power-interruption resume-printing cases — a different mechanism, ticket-print recovery not comms-session recovery), so this is resolved via the requirements-matrix search, not old-suite evidence. ⇒ Refs added: REQ-2589.0.
source: `TFTS Requirements Matrix.xlsx` REQ-2589.0 — broader spec re-search, 2026-07-22. Applied: `proposals/coherence-audit/fixes/pos-gap-resolution.rewrite.json`.

**Consolidation note (not a gap, no Q assigned):** batch_A flagged C4099953 (Technician — Device Settings) and C4099966 (Administrator — Device Settings), and similarly C4099957/C4099967 (Network Settings), as near-identical Home Location/Boarding Location/Mounting Point/Tray Identifier checks duplicated per-role, unlike Sign On/Sign Off/Versions which use one case run per role. Left untouched (out of scope for a citation-grounding pass per `docs/test-practices.md`'s consolidation lens) — candidate for a future `/consolidate` pass, not raised as a Q since it's a structure question, not a fact in doubt.

## Session 2026-07-22 — GV deep spec-grounding audit (suite 30286, full 96-case citation re-verification)

**Q35 · SURFACE/HOW (systemic) · GV Technician Menu cluster, 5 cases (C4104065, C4104067, C4104073,
C4104074, C4104075) — sole citation FBD-100654 doesn't support the specific claim** — ANSWERED
2026-07-22 (resolved from existing evidence, before escalation)
Every case in the GV Technician Menu section cites **FBD-100654** (TFTS Gate System Commissioning
Guide) as its only Refs. Read the full doc (257 paragraphs) plus a targeted search of FBD-100348
(Gate Acceptance) for PIN/timeout/brightness/volume/force-comms terms: FBD-100654 confirms a
**Technician card sign-on exists** ("use a Technician card to login as a Technician", para 250) and
mentions a "Software" tab showing the installed version (para 105, grounds C4104071) and the
Location Settings fields (para 253, grounds C4104058/4104069) — but **nowhere** describes: a PIN
step or invalid-PIN rejection (C4104065), an inactivity auto-signoff timeout (C4104067), a Display
Brightness setting (C4104073), an Audio Volume setting for the validation tone (C4104074), or a
Force Communications action (C4104075). FBD-100348's only "volume" mention is the gate infraction
buzzer (para 352) — a different feature. These are standard technician-menu conventions on other
Flowbird devices (POS/ETM), but per the hard "never move a capability across device/portal surfaces"
rule, that doesn't establish they exist on the **GV** specifically without a citation.
Is GV Technician Menu PIN entry / inactivity timeout / brightness / volume / force-comms confirmed
live on the real GV hardware (carried from the same convention as POS/ETM), or were these scaffolded
from another device/the old suite without a GV-specific spec ever being written?
A (resolved from old suite 14973 + a GV-specific requirements doc not previously checked,
2026-07-22): **Yes, all five are genuine, GV-specific, already-tested behaviours** — not carried
over from another device without basis.
1. **Old suite 14973 already tests every one of the 5**, on real GV hardware, with full step
   tables: PIN entry — **C2754383** "Technician - Invalid PIN Entry" (refs REQ-0050.0/REQ-0050.2);
   inactivity timeout — **C2754318/C2754319/C3251520** "Technician - Navigation - Auto Sign-Off" /
   "Page Timeouts" / "Auto Sign off **" (60s-idle → tone → BOS-audit-log sequence, refs REQ-0656.0);
   Display Brightness — **C2754308/C2754309/C2754310/C3251526** (incremental adjust, refs
   REQ-0511.0/REQ-0511.1); Audio Volume — **C2754311/C3251527** (refs REQ-0511.0/REQ-0511.1); Force
   Communications — **C2754326/C3251528** "Call Now" → BOS session (refs REQ-0348.0).
2. **A GV-specific requirements doc exists that neither the earlier coherence pass nor this session's
   first read had checked**: `GV VCRM Requirements Extract.xlsx` (in `REQS_DIR`, alongside
   FBD-100654/FBD-100348). Re-searching it for the old suite's cited REQ numbers confirms each is
   genuinely GV-scoped: **REQ-0050.2** ("the device shall allow authentication and sign-on via
   Smartcard and a 4 digit PIN", Applies to: ...GV..., tracker note: *"Include tests for valid and
   invalid PIN entry attempts"* — a direct GV-specific instruction to test exactly C4104065's
   scenario); **REQ-3129.0/REQ-3129.1** (GV-scoped: *"the device to exit engineering mode after a
   configurable period of user inactivity ... even if I forget to sign out"* — a better, GV-specific
   citation for C4104067 than the old suite's own REQ-0656.0, which turned out to be mis-cited: it
   applies only to HHD/PV in `VCRM (Latest).xlsx`, not GV); **REQ-0511.0/REQ-0511.1** ("the device
   shall allow for settings to be adjusted including Brightness [and] Volume", Applies to: ...GV...)
   for C4104073/C4104074; **REQ-0348.0** ("the device shall be capable of receiving an instruction
   from the back office that will manually force the device to communicate", Applies to: ...GV...)
   for C4104075.
source: `TestRailClient.get_cases(42, 14973)` (old GV suite, full case bodies for the Technician
cluster); `GV VCRM Requirements Extract.xlsx` and `VCRM (Latest).xlsx` in `REQS_DIR`
(`tools/extract_req.py --entry "GV VCRM Requirements Extract.xlsx" --terms ...`), 2026-07-22. ⇒
Replaced the `(needs-spec — ... confirm live)` markers with proper Refs citations on all 5 cases
(`proposals/coherence-audit/fixes/gv-technician-menu-q35-resolution.rewrite.json`, applied via
`tools/apply_rewrite.py --commit` against suite 30286). Re-audit: CLEAN, 0 blocking findings. Did
**not** need to escalate to George — resolved the same way Q10 was (re-searching a spec source not
yet fully mined), per the "exhaust every other source first" directive. C4104064 (sign-on with
card+PIN), C4104066 (abandon→idle) and C4104068 (menu navigation) remain unchanged (already judged
low-risk generic UX, not reworded, per the original Q35 note).

**Q10 note:** see the ANSWERED update above (2026-07-22) — the earlier "TVM isn't a multi-use
printer" claim (C4104030, gv.findings.md) was itself wrong, from a flattened-text table-extraction
error; the real docx table (parsed cell-by-cell) shows TVM prints multi-use barcodes fine. No case
change needed; the gap is closed, not open.

## Session 2026-07-22 (ABT deep audit, suite 30279, full 496-case sweep — Passenger Portal print/download
resolution + finishing the terse-wording sweep) — Q-numbers below are scoped to this session (this
register restarts numbering per session/device; see e.g. the ETM/POS/GV sessions above for the same
convention). Cross-reference by case id, not by number, across sessions.

**Q25 · SURFACE · C4102766 (Metro cap, "a declined journey is not treated as a settled capped tap") — 2026-07-22 deep audit**
Can a CR122 alighting-stop correction even be *attempted* on a journey that was **declined at the reader** (deny-listed, Declined Reason 2)? The case's WHEN assumes the operator can attempt the correction and it's handled gracefully, but FBD-100662 §5.6 (paras 688-694, read in full) only describes the correction indicator appearing on bus journeys' alighting stops generally ("all bus journeys within the journey history") — it never distinguishes declined/deny-listed journeys from settled ones, so whether the correction UI is even exposed for a declined journey is unstated.
A: Don't know / needs checking — is the correction option offered at all for a declined journey (and this case is right to test "attempt it, it's handled safely"), or does a declined journey never expose that indicator (making the real test "no correction option is shown for a declined journey")?
source: FBD-100662 §5.6 paras 688-694 (full read, this session); TODEV-24096 (title/summary only, no ticket-body access from this tool). ⇒ Case reworded to mark the *attempt* premise `**UNCONFIRMED**` (not the outcome, which stays asserted either way) pending this answer; see `proposals/coherence-audit/fixes/abt-deep-audit-passenger-portal.rewrite.json`. Also swept its 33 sibling cases in the same CR122 capping batch (C4102757-4102790 excl. C4102766) for the same "mechanical CR122 stamp" risk George flagged — all 33 genuinely perform/hold a correction on a settled journey, so the precondition is relevant in every other case; C4102766 was the only mismatch.
**A (partially resolved via Rovo/Jira, 2026-07-22, then re-scoped 2026-07-23 after the Q1 reversal — see below):** Read **TODEV-24096** in full via the Atlassian Rovo MCP (not just title/summary) — it is about the *Settled* case specifically ("Metro Daily Cap Is Removed After Updating Stop Location on a Settled Tap"), and its own bug analysis explicitly guards `Settled == true` and warns "do not conflate with `Declined == true`" — confirming Settled and Declined are handled as genuinely distinct states in the correction code, but not directly stating what happens if a correction is *attempted* on a Declined journey. A closely related ticket, **TODEV-24061** ("Audit Record Loss on Annulled Tap Modification"), is more directly on point for a *non-settled* journey state: its Expected Result states a cancelled/annulled tap should have "no link against the alighting stop (so that the user cannot change the stop)", and the final retest (comment 1127375, PASSED) confirms this was fixed so **the correction option is not offered at all once a journey is cancelled**. This is strong converging evidence (not a 100%-identical state — cancelled/annulled ≠ declined/deny-listed — but the same underlying design principle: the correction UI guards on journey state and is not exposed for a journey that isn't a normal settled one) that the *existence* question is answerable by analogy: the correction option is designed to NOT appear for a non-normally-settled journey. The case's own asserted outcome ("still handled as declined, not a settled capped journey, no cap charge") stays correct either way. **Now re-scoped 2026-07-23**: since the Operator Portal correction capability was reversed today (Q1) — the correction (if attempted) would be via the **Passenger Portal**, not the Operator Portal as originally written; case reworded accordingly (see `abt-cr122-operator-to-passenger.rewrite.json`). The underlying declined-vs-settled question is unchanged by that reversal and remains the residual open point.
source: TODEV-24096 (full ticket incl. all comments, via Atlassian Rovo MCP); TODEV-24061 (full ticket, the cancelled/annulled-tap correction-blocking fix, comments 1116655/1126092/1126096/1127089/1127375) — 2026-07-22/23. ⇒ Left `**UNCONFIRMED**` on the *attempt* premise (the analogy is strong but not identical-state proof); reworded to Passenger Portal per the Q1 reversal.

**A (George, 2026-07-23, new domain fact — narrows the question):** the FIRST declined tap/payment (the one that triggers the decline — e.g. the tap that causes a card to become deny-listed) DOES show in Journey History as a declined entry, and is correctly not counted toward caps. But once a card is ACTUALLY in a denied/deny-listed state, any SUBSEQUENT taps on that already-denied card do NOT appear in Journey History at all. ⇒ **C4102766's own precondition is now suspect**: it uses "the card in a deny-listed state, Declined Reason 2" as its example of a journey "shown in Journey History as declined" — that's ambiguous/possibly wrong. It must be a FIRST-decline example (the triggering tap), not a subsequent-tap-on-an-already-denied-card example (which per George would not be visible at all, contradicting the case's own premise). Case needs rewording to use an unambiguous first-decline scenario. This also sharpens (doesn't fully answer) the original question: the correction-availability question only makes sense for a journey that's actually visible in Journey History, i.e. the first-decline case — a card already on the deny list wouldn't have a visible journey to attempt correcting in the first place.
source: George (live-system confirmation), 2026-07-23.

**Q26 · VALUE/SURFACE · C4102927 ("Passenger Portal — sign on to an anonymous account") — 2026-07-22 deep audit**
The case's precondition claims an anonymous account can only sign on if its card "has completed journeys in the previous seven days." No source found ties **sign-on eligibility** to a 7-day recency window. PSPEC-0015 (CloudFare ABT Product Spec v4.2.1) §6.1.1.1 describes anonymous cEMV login as simple card-details entry (no recency check mentioned), and the only "7 days" figure found (Fig.51 footnote *) governs the **view window** for an anonymous account's Journey/Transaction History *after* sign-on, not a sign-on gate.
A: Don't know / needs checking — is "journeys in the previous 7 days" really a sign-on precondition (e.g. an anti-fraud/anonymous-linking rule not described in PSPEC-0015), or is this case's precondition a conflation of the (confirmed) 7-day *history view* limit with sign-on itself?
source: PSPEC-0015 Fig.51 (footnote *), §6.1.1.1-6.1.1.2 (this session). ⇒ Marked `**UNCONFIRMED**` in the case rather than silently keeping or changing it; see `proposals/coherence-audit/fixes/abt-deep-audit-passenger-portal.rewrite.json`.
**A (resolved from old suite 14441, 2026-07-22): Confirmed — "journeys in the previous seven days" IS a real, distinct sign-on precondition, not a conflation.** Old suite 14441 holds three real, populated, REQ-3561-tagged cases for exactly this: **C2665782** ("Sign-On — ... a card that has performed any number of journeys in the previous seven days ... THEN the user will be signed on"), **C2665784** ("Sign-On — No Journeys" — "Given a user attempts to sign in ... where no Journeys have taken place in the previous seven days / Then the Passenger Portal will prevent the user from signing on"), and **C2665785** (mobile-wallet variant, same seven-day gate). All three predate and are independent of PSPEC-0015's Fig.51 view-window figure — the old suite treats the seven-day check as a sign-on gate in its own right, not a conflation with the history-view limit.
source: TestRail suite 14441, C2665782/C2665784/C2665785 (`ABT / Passenger Web Portal / Anonymous Account`, REQ-3561) — old-suite pull, 2026-07-22. ⇒ `**UNCONFIRMED**` marker removed from C4102927/C4102928; Refs updated to REQ-3561 + the three old-suite case ids (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed 2026-07-22).

**Q27 · PRINT vs DOWNLOAD · C4102931/C4102932 ("Account Functions — view and print Journey/Transaction History") — 2026-07-22 deep audit, the case that triggered this whole task** — ANSWERED
Authored 2026-06-24, never grounded in any of the six prior spec-grounded passes. George suspected "print" should read "download" and asked for it to be resolved against Translink-specific sources, not guessed either way. The only source initially found (`Manuel Portail usager - Laval.docx`) is for a **different deployment** (Laval, Quebec) and confirms nothing about Translink.
A: **"Print" is correct as currently written.** `PSPEC-0015 - Product Specification - CloudFare - ABT v4.2.1.pdf` (the base CloudFare ABT product spec, filed in the Translink requirements library alongside the Translink Cloudfare manual — not the Laval manual) Figure 51 "web/mobile app portal functionality for customer" explicitly lists **"View (and print) Transaction History"** and **"View (and print) Journey History"** as functions available to Anonymous and Registered accounts alike.
source: PSPEC-0015 paras 13555, 13714 (Figure 51 table, page 145). A separate "download in Excel/CSV" feature also exists (para 15374) but is for **Transaction** data specifically, for expense purposes — an additional feature, not a replacement for print, and not currently claimed by either case. ⇒ No wording change to C4102931/C4102932 — only the missing Refs citation added. George's suspicion of "download" is **not** supported by any source found; do not apply it.

**Q28 · SURFACE/VALUE (batch) · Merit Web report-name mismatches, ~24 cases across Analysis Reports,
Concessionary Reports, Revenue Performance Reports, Distance Reports** (e.g. C4103102-4103107,
4103112, 4103114, 4103119, 4103120, 4103125, 4103134, 4103135, 4103108, 4103110, 4103113, 4103136,
4103137)
None of these report names (Origin/Destination, Bus Loading by Route/Journey, Route/Stage, Journey
Analysis, Stage Timeband, Patronage Timeband, Bus Serviceability Final Defects, Route Purchase,
Outstanding Duties, Stage List, Revenue/Revenue by Stop, POS Revenue, GPS/GPS Stage Change Failure,
Tickets By Operator, NIR Revenue Performance, Revenue Foregone, Origin/Destination Distance, Route
Distance Analysis) appear in `FBD-100306`'s 18-report Merit Web catalogue or `FBD-100341`/`FBD-100347`
(the closest adjacent specs). Are these legacy Merit-5 report names that no longer exist in the new
Merit Web viewer, renamed reports we haven't matched, or reports that do exist but simply predate/
postdate the reviewed FBD versions?
A: Don't know / needs checking.
source: FBD-100306 (18-report catalogue, full read), FBD-100341, FBD-100347 — this session.
⇒ All ~24 cases carry (or now carry, terse-form) an individual `**UNCONFIRMED**` marker; not blocked,
not deleted. `Distance Reports` (C4103136/4103137) had been missed by an earlier catalogue-check pass
and is now marked consistent with its siblings.
**A (resolved from old suite 14441 + `TFTS Requirements Matrix.xlsx`, 2026-07-22): These are real, REQ-traceable reports — the premise that no spec covers them was wrong; they simply belong to the legacy Merit-5 catalogue, not the CloudFare-generation FBD library this pass searched first.** Old suite 14441 has a populated `Merit / Analysis Reports`, `Merit / Concessionary Report`, `Merit / Distance Reports`, `Merit / NIR Revenue Reports` and `Merit / Translink Reports` tree with matching titles and real `REQ-####` tags for nearly every one of them (e.g. Origin/Destination = C2700374/REQ-1212.11-12, Bus Loading = C2700324/REQ-1212.10, NIR Revenue Performance = C2691812/REQ-1212+, Outstanding Duties = C2665834/REQ-1212/2255, Stage List = C2697921/REQ-1993). Independently, `TFTS Requirements Matrix.xlsx` (an REQ-id delivery-status index not previously searched for by name — see the sibling POS/TVM passes' Q25/Q34 for the same discovery) confirms the **REQ-1212 family status as "Test | Cloudfare | Deployed"** — i.e. these are live, delivered CloudFare-generation reports, not dead Merit-5-only legacy names. A handful (BRT, Glider, Concessionary Class Summary excl. ENTCS, Fare Foregone, Ticketing-timebands, Route Distance Analysis) still have no old-suite or REQ match and remain genuinely open.
source: TestRail suite 14441 (Merit sections, REQ-1212/1993/2005/2012/1967/1989/2000/2323/2327/2330/2334/2255/2388 family); `TFTS Requirements Matrix.xlsx` (REQ-1212 family, "Deployed" status) — 2026-07-22. ⇒ Refs added citing the matching old-suite case + REQ id on 18 of the ~24 cases (`abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json`, pushed); the ~6 still-unmatched report names left as-is, genuinely open.

**Q29 · SURFACE (batch) · No Smartrack or Merit-sync spec found at all in the local library** — Merit
`Synchronisation & Tools` (C4103141, C4103142), all of `Smartrack` (C4103159 Access, C4103160-4103162
Card Data, C4103163-4103164 Import & Export, C4103165-4103171 Reports)
An extensive search of `REQS_DIR` turned up zero FBD/PSPEC documents naming Smartrack or a Merit
staff/client-tool sync mechanism — Smartrack's cases already carried a pre-existing `[UNCONFIRMED]`
title tag with no body citation possible, and Merit sync has none at all. Is there a separate
Smartrack/Merit-sync spec that hasn't been added to the local requirements library yet, or is this
functionality genuinely undocumented (verified only by direct live-system observation, per the
"assumed-competence" pattern used elsewhere for undocumented-but-real mechanical facts)?
A: Don't know / needs checking.
source: `tools/extract_req.py --find "Smartrack"` / `--find "sync"` — no hits, this session.
⇒ Left `**GAP**`/`**UNCONFIRMED**` markers in place/added for consistency; no invention.
**A (resolved from old suite 14441, 2026-07-22): Smartrack is real, REQ-traceable, and every one of the 7 report names this question named has a matching old-suite case.** Old suite 14441's `Smartrack` section (REQ-0535, REQ-3516, REQ-1895, REQ-2455, REQ-2375 family) has populated cases for exactly this cluster: Action List (`Reports - Active Action List`, C2665900/2665901/2665902), Liability/Scheme Liability (C2724075/2724076/2665886), Default Payment (C2724087), Delivery (C2724091/2724101), Refund (C2724104), Decommission Card (C2665885), POS Revenue Analysis (C2665887) — plus `SmarTrack - Administrator Access` (C2665878) and `SmarTrack - User Access` (C2665892) grounding the whole page, not just its reports. `REQS_DIR` genuinely has no FBD/PSPEC for Smartrack (confirmed absent, not just unsearched) — it is documented only in the old suite/REQ system, a different, older requirements track than the FBD library this pass searched.
source: TestRail suite 14441, `Smartrack` section (C2665878-2665902, C2724075-2724104) — old-suite pull, 2026-07-22. ⇒ Refs added (previously none) on all 7 report cases + `Access`/`Card Data`/`Import & Export` cases citing the matching old-suite case id + REQ-2375 (`abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json`, pushed).

**Q30 · VALUE · Merit C4103099 ("Route Revenue Editor")**
Case asserts the editor covers "pass revenue" and a "generation factor" (confirmed, FBD-100341) AND
"rail and BRT mileage and journey allocation" (not named anywhere in FBD-100341 or the adjacent Merit
specs). Is the rail/BRT mileage-allocation function part of the same Route Revenue Editor screen, or
a different/non-existent function this case incorrectly folded in?
A: Don't know / needs checking.
source: FBD-100341 (pass revenue/generation factor confirmed; rail/BRT mileage allocation absent) —
this session. ⇒ Marked `**GAP**` on the rail/BRT clause only; pass-revenue/generation-factor content
left as grounded.
**A (resolved from old suite 14441, 2026-07-22): Confirmed real — rail and BRT mileage/journey allocation are genuine, distinct sub-functions of the same Route Revenue Editor, just not named in FBD-100341.** Old suite 14441 has four dedicated cases under `Merit / Administration` alongside the Pass Revenue/Generation Factor cases already confirmed: **C2665863** "Route Revenue Editor - Rail Mileage Allocation" (REQ-2066), **C2665864** "Route Revenue Editor - Rail Journey Allocation" (REQ-2066), **C2841019** "Route Revenue Editor - BRT Mileage Allocation" (REQ-3285), **C2841020** "Route Revenue Editor - BRT Journey Allocation" (REQ-3285) — same section, same editor, sibling cases to the already-grounded Pass Revenue (C2665861) and Generation Factor (C2665862).
source: TestRail suite 14441, `Merit / Administration` (C2665861-2665864, C2841019-2841020) — old-suite pull, 2026-07-22. ⇒ `**GAP**` marker removed from C4103099; Refs updated to FBD-100341 + REQ-2066/REQ-2137/REQ-2753/REQ-3285 + the 6 old-suite case ids (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed).

**Q31 · SURFACE/LIVE? (batch) · CloudFare screens described only in specs, liveness/detail
unconfirmed** — spread across `CloudFare / Topology & Fares / Route Management` (6 cases, all
corrected this pass), `Products` (4 of 15 cases), `Dashboard` (4 of 4 cases), and scattered `Reports`/
`Asset Manager`/`Ticket Editor`/`Rules`/`Setup & Import` cases (~15 more)
Multiple CloudFare screens/fields (the route fares-triangle editor, an "ABT flat fare" toggle, rail
substitution-service config, specific ETM-assignment fields, Product buttons/expiry behaviour, Fares
rule creation flow, and the Dashboard's exact tile set) are named in FBD-100296/100260/100261/100268/
100335 etc. as intended functionality, but this pass did not independently re-verify each one live —
only that the FBD text supports the described screen/field existing as specified. Are all of these
confirmed live on the current CloudFare build, or do any remain proposed-only (CR-written, not yet
shipped)?
A: Don't know / needs checking.
source: FBD-100296, FBD-100260, FBD-100261, FBD-100268, FBD-100335 (existence-in-spec confirmed;
live-system confirmation not independently re-obtained this pass, carried as inherited from earlier
grounding work).
⇒ Existing `**UNCONFIRMED**`/citation markers relocated to Refs and tersened per the terse mandate;
no marker was removed or its substance weakened. Treat as still-open pending a live spot-check.

**Q32 · CONFLICT · CloudFare C4102996 ("...a Preset product is configured")**
The case title says "Preset product" but `custom_expected` still reads "a preset reverse FLU
product" — a title/body naming mismatch that predates this pass (not introduced by it). Which is the
correct term — is "reverse FLU" a distinct product sub-type from a generic "Preset" product, or was
the title tightened at some point without updating the expected-result text (or vice versa)?
A: Don't know / needs checking.
source: live case body, `full_cases.json` pull, 2026-07-22. ⇒ Left as-is (not silently retitled by an
agent — a rename call needs a human decision); flagged here rather than fixed unilaterally.
**A (resolved from old suite 14441, 2026-07-22): Not a mismatch — "Preset" and "reverse FLU" are the SAME product, just abbreviated differently in the title vs. the expected-result text.** Old suite 14441 has **C2717262** "Topology & Fares Management - Products - Configure **Preset Reverse Fares Lookup Product**" (REQ-0516/1592/1862) — "FLU" = **F**ares **L**ookup **U**p, so "Preset Reverse FLU Product" and "a Preset product" are both partial references to the one, real, REQ-traceable product name "Preset Reverse Fares Lookup (Up) Product." No rename decision needed — both the title and the expected-result text were describing the same thing; the fix is to make the title match the full real name.
source: TestRail suite 14441, C2717262 (`Cloudfare / Topology & Fares Management / Products`, REQ-0516/REQ-1592/REQ-1862) — old-suite pull, 2026-07-22. ⇒ C4102996 retitled "Product — a Preset Reverse FLU product is configured" (same case id, not a duplicate); Refs updated (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed).

**Q33 · VALUE/traceability · CloudFare C4102987 ("Route Management") terminology drift**
Case title/expected-result use "service code" and "operator" but `FBD-100296`'s actual named route
attributes are "Add to a Service" and "Public Route Code" — is the case's wording an acceptable plain-
language paraphrase, or should it be tightened to the FBD's exact field names for traceability?
A: Don't know / needs checking.
source: FBD-100296 (full read, this session) vs. live case body. ⇒ Left as-is pending a wording-
tightening decision; not unilaterally renamed.
**A (resolved from old suite 14441, 2026-07-22): The case's own wording ("service code") is confirmed correct — it matches the historical/live screen term, not a paraphrase drift.** Old suite 14441 has **C2840946** "Topology & Fares Management - Route Management - **Service Code**" (REQ-3291) — i.e. "Service Code" (not "Public Route Code") is the real, REQ-tagged, on-screen term the old suite itself tests. FBD-100296's "Add to a Service"/"Public Route Code" wording may be a later or coexisting field name, but it does not make the case's "service code" wrong — it is independently grounded.
source: TestRail suite 14441, C2840946 (`Cloudfare / Topology & Fares Management / Route Management`, REQ-3291) — old-suite pull, 2026-07-22. ⇒ No wording change; Refs updated to add REQ-3291 + the old-suite case id alongside FBD-100296 (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed).

**Q34 · VALUE · ABT Operator Web Portal, C4102882 ("Administrator Settings — minimum fare for an
e-Purse smartcard")**
Case claims an admin-configurable **"minimum fare"** for an ePurse smartcard. PSPEC-0015 only names a
**"Minimum ePurse balance"** setting — a balance floor (the point at which a top-up/negative-list
action triggers), not a fare floor. Is "minimum fare" a real, separate setting this case correctly
names, or a mislabelling of the confirmed "Minimum ePurse balance" control?
A: Don't know / needs checking.
source: PSPEC-0015 (Minimum ePurse balance confirmed; no "minimum fare" setting found) — this session.
⇒ Marked `**GAP**` rather than assuming the case's terminology is right.
**A (resolved from old suite 14441 + `TFTS Requirements Matrix.xlsx`, 2026-07-22): Confirmed real and correctly named — "minimum fare" is a genuine, distinct, signed-off requirement, not a mislabelling of "Minimum ePurse balance."** Old suite 14441 has **C2925129** "Administrator can configure **a minimum fare** a customer can have on their e-Purse smartcard" (REQ-3192) alongside the separately-tested **C2925128** "negative balance limit" (also REQ-3192) — two distinct settings under one requirement grouping. `TFTS Requirements Matrix.xlsx` confirms **REQ-3192.1**, verbatim: *"As an administrator I want to configure the **minimum fare** a customer can have on their ABT smartcard, so that if a customer does not have the minimum fare... they cannot tag on"* — status **Signed-Off**. "Minimum ePurse balance" (PSPEC-0015) and "minimum fare" (REQ-3192.1) are two separate, both-real settings, not one mislabelled as the other.
source: TestRail suite 14441, C2925128/C2925129 (`ABT / Operator Web Portal / Administrator Settings Management`, REQ-3192); `TFTS Requirements Matrix.xlsx` REQ-3192.1 (Signed-Off) — 2026-07-22. ⇒ `**GAP**` marker removed from C4102882; Refs updated to REQ-3192.1 + C2925129 (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed).

**Q35 · SURFACE · ABT Operator Web Portal, C4102881 ("Administrator Settings — online debt-recovery
retry attempts")**
Case ties a configurable retry-attempt count to "online" debt recovery generically, but PSPEC-0015
§4.9 distinguishes **Automatic** (back-office-driven, scheme-rule cadence) from **Customer Online**
(customer-portal-initiated, "N attempts per customer per year, operator-configurable") debt recovery
— only the Customer Online channel is described as having a configurable attempt count. Does this
case's "online" mean Customer Online specifically (in which case it's correctly grounded), or is it
conflating the two channels?
A: Don't know / needs checking.
source: PSPEC-0015 §4.9 (this session, cross-referenced with the Q29-Q on debt recovery answered
earlier in this same session's Passenger Portal work). ⇒ Left flagged for confirmation, not reworded
blind.
**A (resolved from old suite 14441 + `TFTS Requirements Matrix.xlsx`, 2026-07-22): Confirmed — "online" means Customer Online specifically, correctly distinguished from tap-initiated, not a channel conflation.** Old suite 14441 has two separately-tested, adjacent cases: **C2665809** "Administrator can configure the max number of customer **online** debt recovery retry attempts" (REQ-3399) and **C2665810** "...customer **tap initiated** debt recovery retry attempts" (REQ-3400) — two distinct, REQ-tagged settings. `TFTS Requirements Matrix.xlsx` confirms **REQ-3399.0** status **"Test | ABT | Deployed"** — live and delivered, not merely proposed.
source: TestRail suite 14441, C2665809/C2665810 (`ABT / Operator Web Portal / Administrator Settings Management`, REQ-3399/REQ-3400); `TFTS Requirements Matrix.xlsx` REQ-3399.0 (Deployed) — 2026-07-22. ⇒ Refs updated to REQ-3399/REQ-3400 + the two old-suite case ids (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed); no wording change needed.

**Q36 · VALUE · ABT Operator Web Portal, C4102880 ("Administrator Settings — maximum journey
duration")**
No paragraph in PSPEC-0015 or the reviewed FBDs names an admin-configurable "maximum journey
duration" setting distinct from the NIR Maximum Journey Time (MJT, FBD-100690) or the ABT "maximum
late data period" (the adjacent case, C4102879). Is this the same control as the NIR MJT (applied
suite-wide, not NIR-only as its FBD implies), a separate ABT-wide setting, or a duplicate/near-
duplicate of C4102879 under a different name?
A: Don't know / needs checking.
source: FBD-100690 (NIR MJT), adjacent case C4102879 — this session. ⇒ Left uncited (no plausible
citation added; would be a guess) — this is the one case in the whole 2026-07-22 pass with literally
no content change pushed, since nothing could be grounded or safely reworded without more information.
**A (resolved from old suite 14441 + `TFTS Requirements Matrix.xlsx`, 2026-07-22): Confirmed real and distinct — not the NIR MJT, not a duplicate of the maximum-late-data-period case.** Old suite 14441 has **C2665808** "Administrator can configure the **maximum journey duration**" (REQ-3414) — "so that a maximum fare can be applied" — as its own separate case, adjacent to but distinct from **C2665807** "...maximum late data period" (REQ-3396, matching C4102879). `TFTS Requirements Matrix.xlsx` confirms **REQ-3414.0**, verbatim: *"As an Administrator I want to configure the maximum journey duration, so that a maximum fare can be applied"* — Signed-Off (delivery status shown as "In Development" in one matrix row, so treat as a real, distinct, signed-off requirement whose full live deployment isn't independently reconfirmed here).
source: TestRail suite 14441, C2665807/C2665808 (`ABT / Operator Web Portal / Administrator Settings Management`, REQ-3396/REQ-3414); `TFTS Requirements Matrix.xlsx` REQ-3414.0 (Signed-Off; delivery status "In Development" in one row) — 2026-07-22. ⇒ Refs added (previously none) citing REQ-3414 + C2665808 (`abt-deep-audit-single-case-resolutions.rewrite.json`, pushed); no wording change.

**Q37 · LIVE? (batch) · ABT Operator Web Portal / Reports, all 35 cases (C4102883-4102917)**
Every case in this section was previously uncited (Refs: none on all 35) and asserts a named ABT/BOS
report exists in the Operator Web Portal, sourced only from FBD-100387 (ABT Reporting via Merit DWH)
and adjacent specs (FBD-100341, FBD-100716, FBD-100358). The specs confirm these report **concepts**
(revenue, pay-in reconciliation, NIR revenue performance, revenue-foregone, etc.) exist as DWH/back-
office data, but this pass did not re-verify that each is exposed as a **named report screen in the
Operator Web Portal** specifically, only that the underlying data/concept is documented somewhere.
Are all 35 confirmed live as named portal reports, or do some only exist as DWH queries/Merit reports
without an Operator Web Portal-native equivalent?
A: Don't know / needs checking.
source: FBD-100387, FBD-100341, FBD-100716, FBD-100358 (concept-level confirmation; portal-surface
confirmation not independently re-obtained this pass). ⇒ All 35 cases now carry `**UNCONFIRMED**` +
Refs citations (previously none); genuinely new markers, not previously flagged in this suite.
**A (resolved from old suite 14441, 2026-07-22): Confirmed — all 35 are (or map directly to) real, historically portal-native, previously-executed reports, not just DWH/back-office concepts.** Old suite 14441 has a populated `ABT / Operator Web Portal / Reports Management` section with a matching "Operator can run a(n) X Report" case for every one of the 35 names in this batch — including the specific ones this question worried might be DWH-only or invented (**Fare Band** = C4066700, **PSP Technical Errors** = C4066699, **Retail Debt** = C2880099, **Revenue by Business Rule** = C2813978, **Revenue Apportionment** = C4073109, **Journeys by Card Scheme** = C2813971, **Journeys by Service/Route** = C2813974) — every one carrying "Has steps: yes" in the old suite, i.e. these were actually executed as portal-native tests historically, not merely queried from a DWH. Several also carry real REQ ids (Action List REQ-3436, Debt REQ-3435, EMV Summary REQ-2662/3491, Revenue by MID REQ-3440, Revenue Inspection REQ-3437, Tap Reconciliation REQ-2662, Transaction REQ-3457/3492), independently confirmed Signed-Off/Deployed in `TFTS Requirements Matrix.xlsx` for the ones checked (e.g. REQ-3436 Action List Report, Signed-Off).
source: TestRail suite 14441, `ABT / Operator Web Portal / Reports Management` (35 matching cases, case ids in `abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json`); `TFTS Requirements Matrix.xlsx` (REQ-3436 etc., Signed-Off) — 2026-07-22. ⇒ `[UNCONFIRMED]` title prefix removed from all 35 cases; Refs updated to add the matching old-suite case id (+ REQ id where one exists) alongside the existing FBD-100387 citation (`abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json`, pushed).

## Session 2026-07-22/23 — ABT gap-resolution follow-up (Q21b, and the Q1 CR122 Operator→Passenger reversal)

**Q21 part (b) · Update Stop list UI filter rules (the ~22 Journey History / Alighting-Stop-Correction cases, C4102825-4102849)** — PARTIALLY RESOLVED
Re-read **TODEV-23500** ("Trying to update an alighting stage in Journey History errors when confirming the new Stop", full ticket incl. Jarvis root-cause analysis, via Atlassian Rovo MCP) — this **confirms the mechanism is real and live**: an "Update stop" dialog on Journey History with a dropdown populated from the fares-engine topology (`GetTooLocations`, keyed on `BoardingStageId`), a genuine "No options" empty-state (seen as the literal bug symptom before the fix), fixed and smoke-tested in ABT 1.2.228.4/1.2.230.1 (2026-03-27). This resolves the screen-name/mechanism-existence part of Q21b. **Still unresolved**: the specific business-rule filters this suite's cases assert (fare>0 filter, zero/negative/transfer-stop exclusion, operator-match rule, exact stop counts) are not described anywhere in this ticket or FBD-100662 — genuinely open, not further resolvable from any source checked.
source: TODEV-23500 (full ticket, Atlassian Rovo MCP, 2026-07-22/23). ⇒ No case wording changed by this finding alone (the existing `**UNCONFIRMED**` markers on the granular filter rules stay, correctly scoped); informs the Q1-reversal fix below (confirms the screen exists to be reworded to Passenger Portal, rather than being invented).

**⚠️ SUPERSEDED 2026-07-23 — see the updated Q1/Q2 answer near the top of this file.** George confirmed a THIRD time that the correction function exists on **both** the Operator Portal and Passenger Portal — the "Passenger Portal only" conclusion this whole section documents is now itself wrong. The 61-case fix described below needs re-applying a third time (in progress via the ABT tidy-up pass). Left the historical record below intact rather than rewritten, so the sequence of what was believed/done at each point stays traceable.

**Q1 · SURFACE/LIVE? — REVERSED AGAIN, 2026-07-22/23: Operator Portal does NOT have CR122 correction; Passenger Portal does**
George's 2026-07-21 "yes, live" answer for the Operator Portal (which had unblocked 37 cases via `abt-bos.rewrite.json`) was itself wrong. **Corrected 2026-07-22/23: the Operator Portal has NO alighting/boarding-stage or fare correction function at all; the Passenger Portal does** ("it looks like it is a thing on passenger portal yes" — tentative but positive, treated as the working answer per Q2 above). FBD-100662 para 693 (re-read in full) shows the two portals were never meant to be interchangeable even under the original CR122 proposal: *"On the operator portal (not the passenger portal) the new fare will be displayed to the operator before it is confirmed"* — i.e. only the operator portal was ever specified to preview the fare before confirming; that nuance had to be checked, not blindly dropped, when regrounding to Passenger Portal.
**Full sweep performed** (not just the known ~42-case list): grepped title/preface/preconditions/steps/expected/Refs of **all 496 live cases** in suite 30279 for "correct/adjust the alighting/fare", "CR122", "recalculate the fare", "Update Stop" (case-insensitive). **96 matches, but only 61 are live, in-scope cases** — the other 35 are already-condemned `ZZ_DELETE_REVIEW` duplicates (out of scope, pending human deletion). The 61 live matches are exactly: the 34 Metro/Zonal/Reference/Uncapped/Town-Service capping-correction cases (C4102757-C4102790, incl. C4102766), the 22 Journey-History/Alighting-Stop-Correction cases (C4102825-C4102849 excl. gaps), and the 5 Correction-Limits cases (C4103480-C4103484). **Nothing outside the known correction family referenced this capability** — no stray mentions in Reports, Customer Services, Refund, or Debt Recovery sections.
**Fixes applied** (`proposals/coherence-audit/fixes/abt-cr122-operator-to-passenger.rewrite.json`, 61 cases, pushed + committed):
- The 34 capping-correction cases + C4102766: "ABT Operator Portal"/"in the Operator Portal you correct" → "ABT Passenger Portal"/"in the Passenger Portal you correct" (mechanically safe — none of these 34 ever asserted the operator-fare-preview behaviour, so the swap doesn't strand a now-false claim). Added a citation note per case: "CR122 ... confirmed live on the ABT Passenger Portal — the Operator Portal does NOT have this function (George, 2026-07-22/23)".
- The 22 Journey-History/Alighting-Stop-Correction cases: same portal-venue swap ("ABT Operator Web Portal" → "ABT Passenger Web Portal"). The pre-existing granular `**UNCONFIRMED**` markers on screen mechanics/filter rules (Q21b) were left untouched — those remain open regardless of which portal. **C4102842 special-cased**: its precondition/step asserted "on the operator portal the new fare is shown before confirmation" — per FBD-100662 para 693 this is an **operator-portal-specific** behaviour that does NOT carry over to the Passenger Portal, so this clause was corrected (not just relabelled) to "on the Passenger Portal the new fare is NOT shown before confirmation ... the fare is recalculated ... after confirming." C4102838's "the journey's operator is Ulsterbus" (the network operator who ran the route — an unrelated, orthogonal fact) was left as-is; only the portal-venue text was swapped.
- The 5 Correction-Limits cases (C4103480-C4103484): these were **already correctly Passenger-Portal-scoped** (never wrongly attributed to the Operator Portal) — only the "does this feature exist at all" liveness hedges were removed (existence now confirmed for the Passenger Portal); the narrower Q21b UX-mechanics hedges (exact refusal-message wording, explicit monthly-reset statement) were kept.
- **Section-placement check** (per George's follow-up): all 61 cases' sections (`Metro Daily Cap`, `Zonal Cap`, `Reference Fare Cap`, `Uncapped & Single Taps`, `Town Service Cap`, `Journey History`, `Update Stop List`, `Correction Limits`) are generically named — none is section-named "Operator Web Portal" or "Passenger Web Portal" specifically, so there is **no case-placement (wrong-section) issue** arising from the Operator-vs-Passenger confusion. Nothing to list for George to move in the TestRail UI.
- **The separate 47-case `proposals/spec-grounded/abt/correction.rewrite.json` proposal** (already applied live 2026-07-21, see its changelog) was checked for the same assumption: it left every CR122 case `**UNCONFIRMED**` (pre-Q1-answer caution), including C4102842's citation of "operator-portal fare-preview (para 693)" as a **spec** reference only, never asserting it as confirmed-live behaviour — so it introduced no live Operator-vs-Passenger contradiction. No further fix needed there beyond the C4102842 correction already made above.
source: George (live-system confirmation, 2026-07-22/23, reversing 2026-07-21); FBD-100662 para 693 (full re-read); full 496-case keyword sweep, 2026-07-22/23. ⇒ 61 cases fixed and committed to suite 30279; re-audit `--no-gate` unchanged at 89 blocking / 208 advisory (no new blocking findings; none of the 61 ids appear in any blocking or advisory finding).

## Session 2026-07-22 — PV deep-audit (every live case in suite 30255 cross-examined against full specs)

New questions surfaced by walking all 135 live cases (+1 already-condemned) claim-by-claim against
the full FBD library / Overflow design source (see
`proposals/coherence-audit/fixes/pv-deep-audit.changelog.md` for the full accounting).

**Q25 · VALUE · PV C4100989 "yLink/24+ smartcard" ("Invalid Time Of Day" reject)**
Does yLink/24+ have a genuine intraday time-of-day validity band, or was "Invalid Time Of Day" copied
from the EA Smartpass sibling case (C4100991)? FBD-100236/100250 only document date-based expiry (end
of concessionary period) for yLink/24+, no time band.
A: source: — ⇒ Marked **UNCONFIRMED** in C4100989 pending answer.
**A (resolved from spec + old suite, 2026-07-22):** No genuine time-of-day band. FBD-100236 para 328
(re-read directly, not the distilled note) states explicitly: *"For yLink and 24+ cards, the expiry
date is expected to be set to the end of the concessionary period"* — date-based expiry only, no
intraday window. Corroborated by the old suite (10047): its yLink coverage is exhaustive (hotlist,
passback, days-left, zone-mismatch — 50 yLink-title hits) yet contains **zero** yLink/24+
time-of-day cases, whereas the genuinely time-banded products (EA Pupil Smartpass, EA Bus Further
Education — a different product family) do have real Mon-Fri/weekend/school-holiday cases in the old
suite. This confirms "Invalid Time Of Day" was carried over in error from the EA Smartpass sibling
(C4100991). ⇒ C4100989 reworded to assert date-based (concessionary-period) expiry, rejecting via the
PV's own confirmed `1.3.9 Product Expired` screen, not a time-of-day check.
source: FBD-100236 para 328 (full read); old-suite 10047 keyword sweep (yLink/24+/"Invalid Time Of
Day"/"time of day", 2026-07-22).

**Q26 · VALUE · PV C4102429 "NI Travel Only" rail ABT success-screen label**
Does the Rail/NIR PV ABT success screen literally show "Northern Ireland Travel Only"? A rail ABT
success screen design exists (C4101036) but the exact string isn't confirmed in specs reviewed
(carried over from the 2026-07-17 light pass, still open).
A: source: — ⇒ Marked **UNCONFIRMED** in C4102429.
**A (resolved from Overflow UX annotations, 2026-07-22):** Confirmed verbatim. The independently
generated `knowledge/flows/pv-flow-annotations.md` extract of the same Overflow source carries this
annotation under the **Platform Validator-Barcode** flow: *"'1.6.1.1 ABT Tag successful' screen can
display an additional line of text. / For NIR/Rail PVs this will state 'Northern Ireland Travel
Only'."* — an exact match to the case's existing wording. ⇒ `**UNCONFIRMED**` marker removed from
C4102429; Refs updated to cite the annotation file directly.
source: `knowledge/flows/pv-flow-annotations.md`, "Platform Validator-Barcode" flow annotation.

**Q27 · SURFACE · PV C4100986 "Ulsterbus Multi-Journey" vs C4101090 "Inter-device top-up" (exhausted-product reject screen name)**
What is the exact approved screen name for an exhausted multi-journey/period product on the PV?
Neither "No Journeys Left" (C4100986) nor "No Days Left" (C4101090) appears in the enumerated
approved-screen set (C4101023–C4101071) — may be one screen with two guessed names, or two genuinely
different conditions.
A: source: — ⇒ Both marked **GAP** on the exact reject-screen wording only (rest of each case is grounded).
**A (resolved from Overflow UX annotations + old suite, 2026-07-22):** Two genuinely different
conditions, both real — not a guessed duplicate. `knowledge/flows/pv-flow-annotations.md`'s
"Platform Validator" flow screen list enumerates **both** `1.3.11 No Journeys Left` and `1.3.15 No
Days Left` as distinct screens. The old suite (10047) shows the same product-type split: Multi-Journey
products test "used all available Journeys" (matching "No Journeys Left"), while Daylink/day-based
products test "used all available days" (matching "No Days Left"). C4100986 tests an Ulsterbus
**Multi-Journey** product ⇒ "No Journeys Left" is correct. C4101090 tests a Metro **Travelcard**
(day-based) ⇒ "No Days Left" is correct. ⇒ Both `**GAP**` markers removed; each case cited to the
Overflow screen list, no wording change needed.
source: `knowledge/flows/pv-flow-annotations.md` ("Platform Validator" flow screen list); old-suite
10047 keyword sweep on "No Journeys Left"/"No Days Left", 2026-07-22.

**Q28 · SURFACE · PV C4101088 "card clash" cEMV decline condition**
TIBU-22322 (the canonical 7-condition cEMV decline story), FBD-100651, and FBD-100658 do not mention
"card clash" (multiple EMV cards presented simultaneously) as a PV decline condition/reason. Is this
a real, distinct decline condition (and its DeclinedReason code/screen), or invented/carried over from
a generic template?
A: source: — ⇒ Removed from C4101088 pending confirmation (not asserted as a decline condition).
**A (resolved from Overflow UX annotations, 2026-07-22):** Real and distinct. The independently
generated `knowledge/flows/pv-flow-annotations.md` extract carries this annotation under the
**"Platform Validator"** flow (the PV's own cEMV/smartcard flow, not the barcode-specific one),
immediately following the screen list that includes `1.3.3 Invalid Card`: *"Cases in which this
screen will be displayed / 1) Unsupported cEMV card e.g. AMEX / 2) Card Clash / 3) Expired cEMV card /
4) BIN on cEMV card invalid / 5) AID check invalid / 6) ODA check not ok / 7) Deny list / 8) Negative
list"* — an Overflow UX design-source confirmation, independent of TIBU-22322/FBD-100651/658's
silence on the term. (The case's own top-level Expected field had in fact never had "card clash"
removed from it despite the precondition's decline-condition list dropping it — a partial-removal
inconsistency this resolves.) ⇒ "card clash" restored to C4101088's decline-condition list, cited to
the Overflow annotation alongside the existing TIBU-22322/FBD-100651 Refs.
source: `knowledge/flows/pv-flow-annotations.md`, "Platform Validator" flow annotation (screen `1.3.3
Invalid Card`).

**Q29 · VALUE · PV C4101014 "Technician Menu — software/config versions"**
Do the exact itemised field lists (OS/BSP/EBoot software versions; Configuration Version/Furthest
Alighting file/TD.Product/TD.Topology/Staff List config versions) match the live PV Technician Menu?
The screens themselves are confirmed (Overflow annotations) but the itemised field lists aren't.
A: source: — ⇒ GAP markers added on the itemised lists only.
**A (resolved from old suite, 2026-07-22):** Exact field lists found and confirmed. Old-suite (10047)
cases C2667038/C3275920 ("A user checks that all Software Versions are Present on the Software
Versions Screen", REQ-0513.0) give the Software Versions field list: **OS (Internal), BSP, EBoot,
Configuration Version, DM.applicationSoftwareFile, DM.operatingSystemSoftwareFile, Smartcard Reader
Firmware Version, Smartcard Reader Application Version**. Old-suite cases C2667047/C3275921 ("...
Configuration Versions Screen", REQ-0513.0) give the Configuration Versions field list:
**Configuration Version, DM.furthestAlightingFile, TD.Product, TD.Topology, Staff List, Action
List**. Both lists extend (not contradict) C4101014's existing guesses — adding Smartcard Reader
Firmware/Application Version and Action List, which the case had missed. ⇒ `**GAP**` markers removed;
C4101014's field lists corrected to the exact old-suite/REQ-0513.0 wording.
source: old-suite 10047 C2667038, C2667047, C3275920, C3275921 (REQ-0513.0), 2026-07-22.
**Addendum (REQ-index cross-check, 2026-07-22):** per a sibling POS pass's finding that
`REQS_DIR\1_Requirements\TFTS Project Delivery Matrices & VCRMs\TFTS Requirements Matrix.xlsx` is a
genuine REQ-id catalogue with delivery/sign-off status, checked REQ-0513.0 there directly: "The
system shall display an on-screen list of the software versions of fares and configuration data
within the device" — applies to PV, status **S4: Signed-Off** ("Accepted by customer"). Independently
corroborates the old-suite evidence above; no change to the resolution.

**Q30 · SURFACE · PV C4101017 "Technician Menu — Operating Times"**
Does a PV "Operating Times" schedule feature exist in the Technician Menu at all? Not found in the
Overflow flow annotations (24-screen Technician Menu list) or FBD-100304.
A: source: — ⇒ Marked **GAP**; feature existence itself is in question, not just the mechanism.
**A (resolved from old suite, 2026-07-22):** Real feature, confirmed. Old-suite (10047) case C2224516
("Operating Times - An Engineer reconfigures the Start Time", REQ-0594.0): *"verify that when the
non-operational periods start time is configured, then the platform validator correctly enters the
out of service state"* — the PV goes out of service at the configured start time and back into
service at the configured end time. Note the mechanism found is a **config-file edit**
(`StateService\Configuration\States.json`) by an engineer, not confirmed as an on-device Technician
Menu screen (which is why it doesn't appear in the Overflow Technician Menu screen list) — the
feature's existence is grounded, but whether the current build exposes it via a Technician Menu
screen vs. a back-office/config-file route remains to double-check live. ⇒ `**GAP**` on existence
removed (feature confirmed real, REQ-0594.0); a narrower note on the configuration entry-point
mechanism added instead.
source: old-suite 10047 C2224516 (REQ-0594.0), 2026-07-22.
**Addendum (REQ-index cross-check, 2026-07-22):** REQ-0594.0 in the TFTS Requirements Matrix reads
"The device shall be capable of receiving traffic operation time data and shall set traffic operation
start and end times" — applies to PV, status **S4: Signed-Off** ("Requirement customer signed off").
This is the requirement-text confirmation that "Operating Times" = the traffic-operation start/end
time feature (matching the old-suite case's start-time behaviour); independently corroborates, no
change to the resolution.

**Q31 · SURFACE · PV C4101091 "Technician Menu — backup/layout/audible feedback"**
Do PV Technician Menu screens for (a) data-mirroring/backup enable, (b) main-screen background colour,
and (c) a distinct card-presented tone actually exist? None of the three found in the Overflow
annotations or reviewed specs.
A: source: — ⇒ Marked **GAP** on all three bundled claims.
**A (resolved from old suite, 2026-07-22):** All three real, confirmed. (a) Data mirroring/backup:
old-suite cases C2224530/C2668492 (REQ-1685.0/REQ-1685.3) — configured by editing
`BOSAgentService\Configuration\BackOfficeAgentConfig.json` (mirroring enabled + a mirror path) then
restarting the Sales App. (b) Main-screen background colour: old-suite cases C2224529/C2668256
(REQ-0796.0) — set by editing `UIService\Layouts\homescreenlayout.scn` (BackColour R/G/B values) then
signing off from the Technician Menu. (c) Distinct card-presented tone: old-suite cases
C3275577/C3275969 (REQ-1687.0) — a valid card presentation plays an approving tone, an invalid
presentation a declining tone. All three are real requirements-backed behaviours, but (a) and (b) are
**config-file edits**, not Technician Menu on-screen toggles, on the old build — which is why neither
appears in the Overflow Technician Menu screen list — so the *mechanism* (not the *existence*) still
wants a live check on the current build. ⇒ `**GAP**` on existence removed for all three; mechanism
caveat added for (a)/(b).
source: old-suite 10047 C2224530/C2668492 (REQ-1685.0/1685.3), C2224529/C2668256 (REQ-0796.0),
C3275577/C3275969 (REQ-1687.0), 2026-07-22.
**Addendum (REQ-index cross-check, 2026-07-22):** all three REQ ids confirmed in the TFTS
Requirements Matrix, all PV-applicable, all **S4: Signed-Off**. Notably REQ-0796.0's exact text
refines (b): *"The device screen layout shall be configurable by Parkeon, as requested by Translink
once per annum"* — i.e. this is a **supplier (Parkeon)-executed, once-a-year change process**, not a
Translink-technician self-service control, which is consistent with the old-suite mechanism (a direct
`homescreenlayout.scn` file edit) rather than an on-screen colour picker. REQ-1685.0: "The Device
shall backup all transaction data within the storage device and SD Memory... Applies to: ...PV
(All)...". REQ-1687.0: "The device shall be capable of providing audible feedback in response to
agreed trigger events... Applies to: ...PV...". No change to the resolution; strengthens it.

**Q32 · VALUE · PV C4102181 "Technician Menu — auto sign-off / timeouts"**
What are the exact auto-sign-off timeout mechanics and tone on the PV Technician Menu? Only a
narrower PIN-field timeout is confirmed in the Overflow annotations; the tone and a two-stage
timeout sequence are not.
A: source: — ⇒ Marked **UNCONFIRMED** on the tone/two-stage-sequence clauses only; the confirmed
PIN-field timeout step is left clean.
**A (resolved from old suite, 2026-07-22):** Exact mechanics confirmed — a genuine two-stage sequence
with a tone. Old-suite (10047) cases C2667020/C3275916 ("Technician - Navigation - Auto Sign-Off",
REQ-0656.0): *"the platform validator auto signs off from the 'Technician Menu' when it is idle"*
after **60 seconds** of inactivity, *"signalised by a tone"*, and the sign-off is audited in the
CloudFare activity log. Old-suite cases C2667023/C3275917 ("Technician - Navigation - Page Timeouts",
same REQ) give the full two-stage sequence: a sub-menu page (Location Settings, Network Settings,
Software/Configuration Versions, Force Communications, Tests and Diagnostics, Display Brightness,
Audio Volume) times out to the Technician Menu **home screen after 60 seconds**, then a **further 60
seconds** of inactivity on the home screen triggers the auto sign-off with the tone. ⇒
`**UNCONFIRMED**` marker removed; C4102181 reworded with the exact 60s/60s mechanics, tone, and
CloudFare-audit assertion.
source: old-suite 10047 C2667020, C2667023, C3275916, C3275917 (REQ-0656.0), 2026-07-22.
**Addendum (REQ-index cross-check, 2026-07-22):** REQ-0656.0 in the TFTS Requirements Matrix reads
"The Translink Engineer, Translink Operator and Translink Supervisor shall be able to navigate menu
functions using the t[ouchscreen]..." — applies to HHD/PV, status **S4: Signed-Off** ("Accepted by
customer" evidence, though noted "Partially Complete with Bugs" on test-evidence completeness).
Independently corroborates the menu-navigation/timeout behaviour family; no change to the resolution.

**Q33 · CONFLICT · PV C4101082 "PV to BOS — MERIT heartbeat" (TIBU-28386) vs FBD-100266**
Is the "MERIT 24-hour heartbeat" (TIBU-28386, cited in C4101082) a distinct mechanism from
FBD-100266's fixed, non-configurable **15-minute** StaffList-based CloudFare heartbeat, or the same
mechanism described inconsistently across two sources?
A: source: — ⇒ Left as-is (case already correctly cites TIBU-28386, no hard-coded value changed);
flagged here rather than silently reconciled, since I can't tell which source is stale without an
answer.
**A (resolved from full spec read + full Jira ticket, 2026-07-22): NOT a conflict — two genuinely
distinct mechanisms to two different back-office systems.** Re-read FBD-100266 in full for every
MERIT/heartbeat/StaffList mention: the document is **entirely scoped to CloudFare's own Comms
Monitor/StaffList mechanism** ("The scope of this document is limited to the Device Heartbeat
mechanism used by devices and how this can be used for reporting in CloudFare only") — it contains
**zero mentions of MERIT anywhere**. Separately, pulled TIBU-28386's full description (not just the
title) via the Atlassian MCP: it specifies the MERIT heartbeat as a **silent, zero-value "preset
product" paper-ticket transaction** — audited via the normal CloudFare audit-queue pipeline through to
MERIT, not the StaffList/Comms-Monitor path — triggered whenever the PV/GV enters an in-service state
(reboot, technician sign-out, returning from auto-out-of-service) **and** by a 24-hour timer as a
backstop. This is mechanically unrelated to FBD-100266's 15-minute StaffList call-in (a lightweight
comms-monitor ping with no transaction record). Ticket status: "Ready for Release", QA PASSED (Thomas
James, 2026-02-24, tested on PV v1.1.1192.29108 — heartbeat-on-sign-in/out and forced-out-of-service
all confirmed triggering). ⇒ No conflict to reconcile; C4101082 was already correctly grounded on
TIBU-28386 — added FBD-100266 to Refs alongside a short note explaining why the two are compatible,
not contradictory, so a future auditor doesn't re-raise this as a conflict.
source: FBD-100266 V3.00 (full read, all heartbeat/StaffList paragraphs); TIBU-28386 full ticket
(description + QA comment), pulled via the Atlassian Rovo MCP, 2026-07-22.

_Also raised (informational, not gap-register questions — see changelog for detail): a stale
`pv-release-2.rewrite.json` REFS-ONLY note on C4103568 pre-dating the Q23 failover narrowing (the
live case itself is correct, just a loose end in an old proposal file); a possible case-overlap
between C4101020 (PV→BOS Deny/BIN list download) and C4101079 (Glider Deny/BIN list updates) flagged
for a future consolidation pass, not resolved here; the two batches auditing the HMI Screen
Validation sections could not stat the actual PNG files (gitignored, not present in this clone) and
instead corroborated every screen name against the independently-generated
`knowledge/flows/pv-flow-annotations.md` extract — treat as strong but not 100%-identical grounding
to a literal file-existence check._

**Q58 · LIVE? · HHD C4103881** — Does Multi-Journey top-up enforce a maximum journey count at all
(the literal "45" figure is unconfirmed AND unsupported — but more fundamentally, no spec confirms
any cap-enforcement behaviour exists, not just its value)?
A: — source: FBD-100261 (no cap-enforcement content found). ⇒ Reworded to an assumed-knowledge-value
precondition ("the configured maximum") per the standard's config-value pattern; underlying
enforcement behaviour itself flagged **GAP**, not just the number.
**A (resolved from old suite, 2026-07-22):** **Cap-enforcement is real, and the actual maximum is 50
journeys** (not 45 — 45 is a boundary test value, not the cap itself). Old suite 5446: **C2678902**
"Top Ups - Adult Metro Multi-Journey Smartcard Top-up - Journeys Exceed 45" and **C2678944** (same for
Ulsterbus) — preface states outright: *"Verifies the maximum number of journeys that can be on the
smartcard at any time is **50 journeys**"*; scenario: card already has >45 journeys → "a top-up is not
processed... no top up products are available" → device shows "Top Up - No products available"
screen. This is a genuine, old-suite-tested enforcement behaviour, just at 50 not 45. ⇒ C4103881
reworded: "45-journey maximum" → "the configured maximum (50 journeys per prior test evidence)";
`**GAP**` on enforcement-existence removed (existence confirmed); cited to `FBD-100261,gap-register Q58
(resolved)`.
source: TestRail suite 5446, C2678902, C2678944 ("...Journeys Exceed 45", REQ-0001.0/0001.2/0060.0/
0873.0/0873.3/0881.0/0881.4/1448.0/1912.0/2145.0/2778.0).

**Q59 · SURFACE · HHD C4103882** — Are expired journeys removed from a Multi-Journey smartcard product
before a new top-up is applied?
A: — source: — ⇒ **GAP**; no textual support anywhere in FBD-100261 or elsewhere searched.
**A (resolved from old suite, 2026-07-22):** **Yes, fully confirmed, with a dedicated receipt.** Old
suite 5446: **C2678904/C2678905** (Adult/Child Metro Multi-Journey) and **C2678946/C2678947** (Adult/
Child Ulsterbus Multi-Journey), all titled "...Smartcard Top-up - Expired Journeys Removed..." —
"Verifies if there are journeys already on the card which are past their expiry date at the time of a
top-up, these journeys shall be removed as part of the top-up process"; Then: "the Journeys are added
to the smartcard... the expired journeys are removed... the transaction is audited accordingly." A
dedicated ticket format exists for this specifically: **C2725362**/dedup-suite **C2598962** "Ticket
Format Number 13C – Smartcard Top-up Expiry Receipt" — "This ticket receipt is only printed when
expired journeys have been removed from a Multi-journey smartcard at the point where the customer is
performing a top-up... IN ADDITION TO their receipt for their multi-journey top-up." Dedup suite 13958
**C2599018** further confirms the "Top Up - Select Amount" screen shows a "Number of Expired Journeys"
field and a "Card Balance" of "0 Journeys" when fully expired. ⇒ `**GAP**` removed from C4103882's
Refs; cited to the REQ series (`REQ-0001.0/0873.0/0873.3/0878.0/0878.3/0881.0/0881.4/0887.0/0887.4`)
plus `gap-register Q59 (resolved)`.
source: TestRail suite 5446, C2678904, C2678905, C2678946, C2678947, C2725362; suite 13958, C2598962,
C2599018.

**Q60 · LIVE? · HHD C4103890** — For a failed-print top-up on HHD, can the transaction be annulled and
cash handed back to the passenger (by analogy to ETM's annul-on-failed-print pattern)? FBD-100373
explicitly scopes HHD to "sales+reversals, no refunds" — citing it for this case risks implying the
POS URN-based Refund workflow, which the same spec says doesn't apply to HHD.
A: — source: FBD-100373 (excludes HHD from refunds; doesn't confirm or deny an annul-and-hand-back
mechanism). ⇒ Dropped the misleading FBD-100373 citation; flagged the underlying reversal mechanism
**UNCONFIRMED** for HHD specifically.

_Answered questions get cited back into the affected cases + `knowledge/`. Unanswered → escalated as possible design/spec findings. Add rows as new gaps surface._

---

## Session 2026-07-22 — HHD deep-grounding audit (suite 30285, Q34–Q57)

Full per-case citation-grounded walk of all 211 live HHD cases (not just coherence/wording — every
factual claim checked against the actual FBD/REQ source, per George's directive). Full accounting in
`proposals/coherence-audit/fixes/hhd-deep-audit.changelog.md`. 24 new questions raised.

**Resolution pass, 2026-07-22 (see `proposals/coherence-audit/fixes/hhd-deep-audit.changelog.md` for
the full accounting and `hhd-gap-resolution.changelog.md` for this specific pass):** before escalating
this backlog to George, re-checked every open HHD question (this session's Q34-Q57, the earlier
standalone Q58-Q60, and the original Q16/Q17 conflicts) against the 4 old suites (5446/13958/5608/5505)
and a broader/deeper `REQS_DIR` re-search — critically including `TFTS Requirements Matrix.xlsx`
(1_Requirements/TFTS Project Delivery Matrices & VCRMs), a REQ-id index/description sheet that had
never been searched by name before this pass and turned out to hold detailed HHD-specific requirement
text for most of this backlog. **Resolved: Q16, Q17, Q35, Q38, Q40, Q41, Q42, Q44 (the 9-case Penalty
Warning & Fares section — confirmed real, NOT invented), Q46 (partially), Q47 (partially), Q48, Q51,
Q55, Q56, Q58, Q59.** Strengthened-but-still-open: Q49, Q52 (new contradicting hardware evidence, not
yet condemned). Still open, no source found: Q34, Q36, Q37, Q39 (partially — 10/11 cases grounded),
Q43, Q45 (partially — 7/8 cases grounded), Q50, Q53, Q54, Q57, Q60. Cases affected: 39 updated via
`hhd-gap-resolution.rewrite.json` (`apply_rewrite.py --commit`), 3 condemned (`ZZ_DELETE_REVIEW`:
C4103831, C4103977, C4103995). Suite re-audited CLEAN after the pass (208 cases; 43 pre-existing
advisory title-length findings, no blocking findings).

**Q34 · LIVE? · HHD C4103814** — Does HHD card payment (M020) resume automatically once comms are
restored after an outage, with no extra operator steps?
A: — source: — ⇒ Marked **UNCONFIRMED** in-case; no spec (FBD-100320/353/373/183) covers post-outage
resume behaviour.

**Q35 · VALUE · HHD C4103815** — Is the PAN masked on a printed HHD card-sale receipt/ticket?
A: — source: — ⇒ `MaskedPan` in FBD-100658 is an ABT-tap audit field, not the printed-receipt context;
no ticket-layout doc confirms PAN masking on the printed card-sale receipt. Marked **GAP**.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** **Yes — real, PCI DSS-mandated.**
`TFTS Requirements Matrix.xlsx` "Description" sheet: **REQ-1722.0** "Mask account data on tickets" —
"The device payment terminals shall ensure only the last 4 digits of the PAN on payment receipts are
visible to ensure compliance with PCI DSS requirements" (Applies to: HHD (All), POS (All), TVM (All)).
**REQ-1723.0** mirrors this for reporting/on-device displays. ⇒ **GAP** removed from C4103815; cited
`REQ-1722.0,REQ-1723.0` alongside FBD-100658.
source: `TFTS Requirements Matrix.xlsx` (1_Requirements/TFTS Project Delivery Matrices & VCRMs),
"Description" sheet, REQ-1722.0/REQ-1723.0.

**Q36 · LIVE? · HHD C4103817 / C4103819** — Does a card sale complete normally while the M020 is on
charge (cradled)?
A: — source: — ⇒ No document mentions charging state as a factor in payment availability. **GAP**.

**Q37 · SURFACE · HHD C4103818 / C4103819** — Does a "reference-number station" card-payment keying
mechanism exist for HHD at named NIR halts (Yorkgate etc.), and if so what is it? (Not to be confused
with the smartcard product-reference mechanism in FBD-100261/277, a different thing.)
A: — source: — ⇒ Location examples grounded (FBD-100383 confirms the halts); the keying mechanism
itself is **GAP**.

**Q38 · CONFLICT · HHD C4103829 / C4103830 vs C4103832** — Can the HHD top up (SmartRecharge) an
existing smartcard, or is smartcard issue+recharge POS-only per FBD-100261 §5 ("only used by the POS
device as this is the only device that will issue these smartcard products")? C4103832 in the same
suite already correctly cites this doc for "HHD does not issue smartcards" — C4103829/830 contradict
it for top-up specifically.
A: — source: FBD-100261 §5. ⇒ Flagged, not resolved — needs a live-system/engineer call on whether
top-up is a genuine HHD capability the doc under-describes, or whether the two cases are wrong.
**A (resolved from `Smartcard Use Matrix.xlsx`, 2026-07-22):** **No real conflict — both are correct.**
Read the xlsx cell-by-cell (openpyxl, not the flattened text dump) on its "Smartcard Topups" sheet:
columns are `HHD` → `Glider` (col E) / `NIR` (col F). Row `iLink`: **E11=Yes, F11=Yes** — the HHD
**does** top up iLink in both modes. FBD-100261 §5's "only used by the POS device as this is the only
device that will issue these smartcard products" is scoped to that section's **issue** process
(WTS SmartCreate — encoding a brand-new Metro/Ulsterbus Multi-Journey card, per §5's own worked
examples "present a **pre-encoded** Smartlink smartcard... issue it to the customer"), not top-up
(WTS SmartRecharge) in general — §2 of the same doc lists SmartUse/SmartRecharge/SmartCreate as three
separate product types with no device restriction stated for SmartRecharge. C4103832 ("issuing a new
smartcard is not available on the HHD") and C4103829/C4103830 (HHD iLink top-up) are both correct —
they test different capabilities (issue vs recharge), not contradictory claims about the same one.
⇒ **GAP** removed from C4103829/C4103830; refs corrected to `FBD-100261,Smartcard Use Matrix.xlsx`.
No change needed to C4103832.
source: `Smartcard Use Matrix.xlsx` (Useful Documents), "Smartcard Topups" sheet, row `iLink`
(cols E/F = HHD Glider/NIR, both `Yes`); FBD-100261 V2.00 §2 (product-type definitions) and §5
(issue-process scope, paras 76-77).

**Q39 · SURFACE · HHD C4103847, 4103848, 4103849, 4103851, 4103863, 4103864, 4103871, 4103872,
4103875, 4103876, 4103877** — Does FBD-100207's boarding/alighting stage-selection UI model (documented
explicitly for ETM/POS/TVM, never HHD) also govern the HHD, or does HHD use a different/undocumented
mechanism?
A: — source: FBD-100207 (0 "HHD"/"Handheld" hits across the whole doc). ⇒ Kept as best-available
analogy citation; flagged rather than asserted as confirmed.
**A (substantially resolved from TFTS Requirements Matrix, 2026-07-22):** HHD **does** have its own
documented boarding/alighting selection mechanism — a separate REQ series from FBD-100207's ETM/POS/
TVM model, not the same source but a real HHD-specific one. **REQ-0113.3** "Input Stage ID": "The
device shall allow the Translink operator to manually enter the boarding and alighting station or
halt ID" (HHD/ETM/POS). **REQ-0142.0**: "As a NIR Operator I need the HHD to provide a **numeric
selection facility** of the boarding and alighting stations on the ticket issue screen" (HHD (NIR)).
Dozens of smartcard-validation REQs (REQ-0837.2/0837.6, REQ-0840.2/0840.6, REQ-0841.2/0841.6, etc.)
also explicitly state "the device shall allow the Translink Operator to select the boarding
station"/"alighting station" (NIR) or "boarding halt"/"alighting halt" (BRT) for the HHD by name. This
directly matches C4103851's own "Data variations: stage selection {menu, manual character entry}" —
REQ-0142.0 = the menu/numeric-selection variant, REQ-0113.3 = the manual-entry variant. ⇒
`**UNCONFIRMED**` removed from C4103851, re-cited to `FBD-100207,FBD-100336,REQ-0113.3,REQ-0142.0`.
The other 10 cases in this group (C4103847/848/849/863/864/871/872/875/876/877) had no inline marker
(FBD-100207 was one of several Refs, not asserted alone) — added `REQ-0113.3` alongside their existing
Refs for a firmer citation.
source: `TFTS Requirements Matrix.xlsx`, "Description" sheet, REQ-0113.3, REQ-0142.0, REQ-0837.2,
REQ-0837.6 (representative sample of the boarding/alighting-select REQ series).

**Q40 · LIVE? · HHD C4103838** — Does annulling an HHD iLink top-up reverse the value already written
to the smartcard, or only cancel the back-office/payment record?
A: — source: — ⇒ **GAP**; a real reconciliation-risk question, not just a wording issue.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** **Yes — the smartcard write is reversed,
not just the back-office record.** `TFTS Requirements Matrix.xlsx` REQ-2836.0 "As a Transport Operator,
I need my device to be capable of annulling both a smartcard product issue and a smartcard product
top-up" (HHD/ETM/POS): constraint — **"The device will restore the smartcard product on which the
issue/top-up was performed to its state prior to the issue/top-up."** Consistent with REQ-0300.0
("Annul Ticket" constraint: "For top-up annulment the smartcard shall be present and shall not have
been used for travel since the top-up") and the old suite's C2645308 ("Annulment - Adult iLink - Top
Up After Expiry - Cash": the expired top-up ticket, once validated, is **not** able to be annulled —
consistent with "must not have been used since"). ⇒ `**UNCONFIRMED**` removed from C4103838; cited
`FBD-100373,REQ-2836.0`.
source: `TFTS Requirements Matrix.xlsx`, REQ-2836.0, REQ-0300.0; TestRail suite 5446 C2645308.

**Q41 · SURFACE · HHD C4103850** — Does the HHD ticket-sales screen have a configured default
passenger/ticket-type pre-selection?
A: — source: — ⇒ **GAP**; possible POS-behaviour carried over to HHD without confirmation.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** **Yes, real.** REQ-0235.0 "As an Operator
or Driver I need the device to have a default ticket type, so that I can save time when issuing the
most common tickets" (HHD (All), ETM (All)) — constraints: "When status/boarding/alighting stage has
changed the HHD will revert to the default ticket type"; "When the HHD has been inactive for 1 minute
for a BRT Operator the HHD will revert to the default ticket type." ⇒ **GAP** removed from C4103850;
cited `REQ-0235.0`.
source: `TFTS Requirements Matrix.xlsx`, REQ-0235.0.

**Q42 · SURFACE · HHD C4103855** — Does a distinct "advance ticket" product exist on HHD, or is this
the same product as "3 Day Select" (C4103858) under a different name?
A: — source: — ⇒ **GAP**; no "Advance" product found in the Product-to-Ticket Mapping xlsx or either
ticket-layout doc for any device.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** Neither guess was right — it's an
**attribute**, not a product. **REQ-3094.0** "As an operator I need the device to have an option to
advance date paper tickets" (POS (Ulsterbus), POS (NIR), **HHD (NIR)**): "The device shall identify
which ticket types can be advance dated... Only configured ticket types can be advance dated." Also
**REQ-0142.6** (legacy) and **REQ-0446.0** ("Configure Products" — "Advance date"/"Advance date
period" are per-product config flags). So "advance" is a **date attribute applied to an eligible,
already-existing ticket type** at issue time — not a standalone "advance product" to select, and not
the same thing as "3 Day Select" (a distinct product). ⇒ C4103855 retitled/reworded from "issue the
advance ticket... showing the advance product" to applying an advance date to a configured
advance-dateable ticket type; cited `REQ-0142.6,REQ-0446.0,REQ-3094.0`.
source: `TFTS Requirements Matrix.xlsx`, REQ-3094.0, REQ-0142.6, REQ-0446.0.

**Q43 · CONFLICT · HHD C4103870** — Is "Visual Inspection" an on-device HHD recall screen (Operator
looks up a previously issued ticket's stored details on the HHD), or a manual paper check with no
device feature involved? The case as written asserts "on the HHD" but no source describes such a
screen.
A: — source: — ⇒ **GAP**; case may be over-asserting a device capability.

**Q44 · SURFACE/BUG? · HHD C4103893, 4103894, 4103895, 4103896, 4103897, 4103898, 4103899, 4103900,
4103921 (whole "Penalty Warning & Fares" section)** — Is there a manual, operator-menu-driven
penalty-warning/penalty-fare function on the HHD (printed ticket, whitelist, waybill entry), or is the
only real mechanism FBD-100716's fully automated back-office cEMV "Standard Fare" charge at
End-of-Day settlement (no operator action, no ticket, no whitelist)? Full-text search of FBD-100716/
651/690/658 found no manual-issuance mechanism — only one summary-report line mentioning "penalty
fares/warnings issued" as a Revenue Inspectors report rollup.
A: — source: FBD-100716 (only automated mechanism documented). ⇒ **POSSIBLE DESIGN/SPEC BUG or
suite invention** — an entire 9-case section may be testing functionality that doesn't exist as
described. Needs an engineer's confirmation before deciding rewrite-to-real-cEMV-flow vs "there's a
legacy manual function not in this requirements library."
**A (resolved — NOT invented — from `TFTS Requirements Matrix.xlsx`, 2026-07-22):** The manual,
operator-issued penalty function is **real and extensively specified** — this REQ-id index (a
different document from FBD-100716, not searched in the original pass) confirms it in detail:
**REQ-0062.0** "Issue Penalty Fares" — "The HHD shall be capable of issuing penalty fares" (HHD (All)).
**REQ-1449.0** "HHD Prints Penalty Fare Ticket" — penalty reference number, staff number, penalty fee,
date/time, T&Cs; three ticket types: **Penalty Fare Warning**, **Penalty Fare Ticket - Without
Travel**, **Penalty Fare Ticket - With Travel**. **REQ-1449.2/1449.3/1449.4** detail each type
(zero-value warning ticket always available regardless of passenger type; passenger-detail capture;
liability rules — Adults/yLink/24+ always liable, Children/Free Smartpass/Staff generally not but
issuable if required; SmarTrack whitelist recording). **REQ-3047.0/3048.0/3049.0** — reporting on
warnings issued, configuring penalty ticket layouts, and configuring **which products are eligible for
a penalty fare** (the whitelist mechanism). **REQ-2255.6** "BRT Revenue Inspectors Report" includes
"Number of Penalty Fare Tickets Issued". **REQ-0329.1** (Rail Operator Waybill) includes "No. of
Penalty Tickets issued". This is a real, manual, printed-ticket, whitelist-gated, waybill-reconciled
function — not an invented substitute for FBD-100716's automated cEMV flow (which is a *different*,
also-real mechanism for a different scenario). Not a design/spec bug. ⇒ All 9 cases' Refs corrected
from the mis-cited `FBD-100716`/`gap-register Q44` to the real REQ ids (REQ-0062.0/0062.1, REQ-1449.0/
1449.2/1449.3/1449.4, REQ-2255.6, REQ-3047.0/3048.0/3049.0, REQ-0329.1) — no wording/behaviour change,
the case bodies were already accurate, only uncited.
source: `TFTS Requirements Matrix.xlsx` (1_Requirements/TFTS Project Delivery Matrices & VCRMs),
"Description" sheet — REQ-0062.0, REQ-0062.1, REQ-1449.0, REQ-1449.2, REQ-1449.3, REQ-1449.4,
REQ-2255.6, REQ-3047.0, REQ-3048.0, REQ-3049.0, REQ-0329.1. Flagged to the coordinator by a sibling
POS gap-resolution pass that found this file had never been searched by name before.

**Q45 · SURFACE · HHD C4103901, 4103902, 4103903, 4103905, 4103906, 4103909, 4103910, 4103911** — Is
there an HHD-specific sign-on/sign-off UX design doc, or does the POS Overflow sign-on flow
(`knowledge/flows/translink-pos-signon.md`) apply 1:1 to HHD? FBD-100383 (the prior sole citation) has
zero sign-on/PIN/lockout/duty content — it's the CloudFare org-hierarchy doc, wrong surface entirely.
A: — source: — ⇒ **GAP**; closest analogy is the POS flow, unconfirmed for HHD.
**A (substantially resolved from TFTS Requirements Matrix, 2026-07-22):** Most of this group grounds
directly to HHD-specific REQs (not the POS flow by analogy): **REQ-0056.0/0056.1/0056.2/0056.3**
"Message of the Day" (HHD/POS/ETM — displayed after sign-on with a "Press Any Key to Clear" dialogue,
centrally configurable). **REQ-0276.0** "Colour and Word of the Day" (HHD from Phase A). **REQ-0050.3**
"BRT Revenue Inspectors Sign-on" (duty number/route number/direction additional steps). **REQ-0396.2**
(record operator sign-on data: HHD ID, operator number, home location, sign-on date/time, duty
number). **REQ-1478.0**/**REQ-0384.1** (docking-cradle requirement; HHD must be signed off and docked
for upload/download — grounds forced-sign-off-on-dock, C4103911). **REQ-2576.0** (device lockout after
a configurable period of no successful comms — a **different** lockout trigger from a failed-PIN-
attempt count). None of these is the "POS flow applied 1:1" the question worried about — they are
genuine HHD-specific requirements. **Remaining open nuance:** C4103903's specific claim (device locks
after N **failed PIN attempts**, a "Device Locked" screen) is not confirmed by any REQ found — only
the different comms-lockout mechanism (REQ-2576.0) is documented — so this one sub-case stays flagged.
⇒ Refs added: REQ-0056.0/0056.1/0276.0/0396.2/1478.0/0384.1 across the group; C4103903 kept open
(no change) pending the failed-PIN-lockout-specific confirmation.
source: `TFTS Requirements Matrix.xlsx`, REQ-0056.0-3, REQ-0276.0, REQ-0050.3, REQ-0396.2, REQ-1478.0,
REQ-0384.1, REQ-2576.0.

**Q46 · SURFACE/LIVE? · HHD C4103913, C4103919, C4103977** — Does "CR78" (a driver/operator break mode
that preserves Inspection-vs-Validation state, and reportedly allows smartcard inspection while
active) exist as a real change request/feature? `--find "CR78"` returns nothing anywhere in the local
requirements library, and FBD-100651/690 have zero "break" content.
A: — source: — ⇒ **GAP** across all three cases; either CR78 needs adding to the local library or an
engineer confirms the behaviour from elsewhere.
**A (partially resolved from TFTS Requirements Matrix, 2026-07-22):** The underlying **operator break
mode itself is real and well-specified** (independent of the "CR78" name, which still doesn't appear
anywhere) — **REQ-0305.0** "Enter Break Mode" (HHD/ETM/POS): operator enters a break where "ticket
issuing and other functions are suspended"; constraints — device stays signed-on, **"the touch-screen
and keyboard on the HHD will only enable entry of an operator ID and PIN"**, operator re-enters PIN to
leave. **REQ-0305.1** "Leave Break Mode". **REQ-0305.2**/**REQ-0360.0** (Supervisor unlock/override).
**REQ-1137.0** (Supervisor functions accessible when signed-on-but-in-break-mode). This grounds
C4103913/C4103919's core claim (a real break state exists; the device stays signed on through it) —
their added claim that the HHD "resumes the same mode (Inspection/Validation)" afterwards isn't
separately confirmed but is a low-risk inference from "stays signed on". **However, C4103977
("inspection is available in break mode") directly conflicts with REQ-0305.0's own constraint** — if
"the touch-screen and keyboard will only enable entry of an operator ID and PIN" while in break mode,
smartcard inspection (a distinct function) should NOT be available during break, contradicting the
case's premise. This reads as the same conflation the original question suspected, now with positive
evidence it's wrong rather than merely uncited. ⇒ C4103913/C4103919 re-cited to add
`REQ-0305.0,REQ-0305.1`, left otherwise as-is (still flagged for the CR78/mode-preservation nuance).
**C4103977 condemned** (`ZZ_DELETE_REVIEW`) — its central premise contradicts REQ-0305.0's explicit
constraint; noted as a likely genuine defect/invention, not merely a citation gap.
source: `TFTS Requirements Matrix.xlsx`, REQ-0305.0, REQ-0305.1, REQ-0305.2, REQ-0360.0, REQ-1137.0.

**Q47 · SURFACE · HHD C4103914, 4103916, 4103917, 4103920** — Does the HHD have an on-device
"View Totals" / mini-statement-print / "Status" Operator Menu at all, and if so what are the real
screen/layout names? (C4103917's "NIR Layout 20 / Glider Format 15" references have no match anywhere
in the requirements library — likely invented specifics, marked GAP rather than asserted.) Prior
citations (FBD-100342, FBD-100276, FBD-100266) are back-office/API/admin specs with zero on-device
menu content — assigned by topic-keyword association, not verified.
A: — source: — ⇒ **GAP**; needs an HHD Operator Menu UX source (Overflow flow or equivalent).
**A (substantially resolved from TFTS Requirements Matrix + old suite, 2026-07-22):** **View Totals**
(C4103916) grounds to **REQ-0299.0** "Display Tickets Sold" (HHD (All)) — on-screen waybill info
(tickets, passes, top-ups, revenue, annulled) since the last back-office upload — and **REQ-0350.2**
"Display Detailed Historic Waybill" (last 50 waybills, Supervisor-accessible). **Mini-Statement**
(C4103917) grounds to **REQ-2452.1** (already an existing citation elsewhere in the suite) plus the
old suite's own populated cases (5446 C2759099/C2759103, "Mini Statement - Expired Smartcard Status
Updated After Top Up") which enumerate the real on-device Mini Statement field list: Card Type, ESN,
PSN, Card Ref, Start Date, End Date, **Journeys Left**, **Days Left**, Usage Date/Time, Top Up
Date/Time. **Status** (C4103920) has no equivalent REQ or old-suite hit found — stays a narrower GAP.
The specific **"NIR Layout 20 / Glider Format 15"** ticket-layout numbers in C4103917 remain
unconfirmed — no document names these — kept as a narrow GAP on that detail only. ⇒ Refs updated:
C4103916 → `REQ-0299.0,REQ-0350.2`; C4103917 → `REQ-2452.1` (kept), layout-number clause remains
flagged; C4103914 (menu nav) and C4103920 (Status) left open pending an HHD Operator Menu UX source.
source: `TFTS Requirements Matrix.xlsx` REQ-0299.0, REQ-0350.2; TestRail suite 5446 C2759099, C2759103
("Mini Statement - Expired Smartcard Status Updated After Top Up").

**Q48 · SURFACE · HHD C4103918** — Does a "manage sale favourites" feature exist on the HHD at all?
FBD-100260 (prior sole citation) is a display-name-resolution spec with zero "favourite" content.
A: — source: — ⇒ **GAP**.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** **Yes, real.** REQ-0307.0 "Assign
Favourite Ticket Settings" (HHD (All), POS (NIR)) — "The device shall allow the Translink Operator to
setup a ticket type as a favourite, assigning to a hotkey or memory button"; constraints: stored
favourites recalled after end of shift, favourites accessible from the ticket-issue screen (not a
hidden menu). REQ-0307.1 mirrors the storage requirement. ⇒ **GAP** removed; cited
`REQ-0307.0,REQ-0307.1`.
source: `TFTS Requirements Matrix.xlsx`, REQ-0307.0, REQ-0307.1.

**Q49 · SURFACE · HHD C4103922** — Does HHD printer pairing use the same Bluetooth mechanism as the
M020 payment reader (FBD-100320), or is the printer a different peripheral with its own undocumented
pairing flow?
A: — source: — ⇒ **GAP**; FBD-100320 only covers the M020, not the printer.
**A (strengthened, not fully resolved — from TFTS Requirements Matrix, 2026-07-22):** New evidence
points toward this being invented/conflated rather than merely uncited. **REQ-0819.6** "HHD equipped
with printer" — "The HHD shall be equipped with 2\" thermal printer" (HHD) — describes the printer as
**integrated hardware**, not a separate pairable accessory. **REQ-0819.8** documents the HHD's
Bluetooth/NFC short-range wireless capability as being specifically "to communicate to an **external
payment card device** to perform EMV and NFC payment transactions" — i.e. reserved for the M020, with
no printer-pairing use mentioned. Given the printer is built into the device per its own core hardware
spec, a "pair the printer" Operator-menu workflow (C4103922) is hard to square with the hardware as
documented — it may be a conflation with the real M020 Bluetooth-pairing case (C4104007). Not
condemned outright (a detachable/spare printer accessory isn't explicitly ruled out), but the evidence
now leans toward "likely invented" rather than "plausible, just uncited". ⇒ Refs updated to
`FBD-100320,REQ-0819.6,REQ-0819.8`; GAP marker strengthened with this evidence; still escalated to
George rather than unilaterally condemned.
source: `TFTS Requirements Matrix.xlsx`, REQ-0819.0, REQ-0819.6, REQ-0819.8.

**Q50 · SURFACE · HHD C4103924** — Can a Supervisor "act as Operator" on the HHD (sign on/off, end a
duty as a separate operator session)? No requirement/design doc (including the full TFTS Requirements
Matrix) mentions "act as operator"/"acting operator" for HHD.
A: — source: — ⇒ **GAP**.

**Q51 · SURFACE · HHD C4103925** — Does a Supervisor *authorise* an operator into break mode (as the
case's title/steps claim), or only override/end a break already in progress (REQ-0360.0: "allow the
Translink Supervisor to override operator break mode... operator... signed off... does not require
the operator's PIN")? Every supervisor+break-mode requirement found (REQ-0305.0/0305.1/0360.0/1137.0)
describes ending/overriding, not authorising/starting.
A: — source: REQ-0360.0 et al. ⇒ Likely the case has the wrong direction/verb — flagged for
confirmation before a title/steps rewrite, not resolved unilaterally.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** Confirmed — the case had the wrong
direction. Every Supervisor+break-mode REQ in the library (REQ-0305.2 "Supervisor Unlocks Break Mode",
REQ-0360.0 "Override Operator Break Mode" — "the Translink operator who entered break mode will be
signed off... does not require the Translink operator's PIN", REQ-1137.0 "Access Translink Supervisor
Functions") describes only **ending/overriding** a break already in progress, never **authorising/
starting** one. No REQ, FBD, or old-suite case describes a Supervisor-authorised break *start*. ⇒
**C4103925 renamed and reworded** (old title kept as `match:` per the standard's rename convention)
from "Supervisor — authorise an operator break" to "Supervisor — override/end an operator break (ID
entry and card)", steps changed from "authorises the break" to "overrides the break... operator is
signed off, without the operator's PIN" — grounded on REQ-0360.0's exact wording. Cited
`REQ-0305.0,REQ-0305.2,REQ-0360.0,REQ-1137.0`.
source: `TFTS Requirements Matrix.xlsx`, REQ-0305.0, REQ-0305.2, REQ-0360.0, REQ-1137.0.

**Q52 · SURFACE · HHD C4103936** — Is HHD Bluetooth-printer connection via MAC-address manual entry
or barcode scan (as the case claims) the correct commissioning mechanism? Hardware capability (BT +
barcode scanning) is confirmed (REQ-0819.0) but no doc describes the specific printer-pairing
workflow; FBD-100320 (prior citation) only covers the M020 payment terminal.
A: — source: — ⇒ **GAP** (lower risk — outcome is plausible from hardware capability, only the exact
mechanism is unconfirmed).
**A (strengthened, not fully resolved — from TFTS Requirements Matrix, 2026-07-22):** Same evidence as
Q49 applies here — **REQ-0819.6** documents the HHD's printer as its own integrated 2" thermal
hardware, and **REQ-0819.8** scopes the HHD's Bluetooth/NFC short-range wireless to pairing an
*external payment card device* (the M020) specifically, not a printer. This raises the same doubt: a
Technician "connect the printer by MAC entry or barcode scan" workflow (C4103936) may be conflated
with the real M020-pairing mechanism rather than a genuine, separate printer-pairing flow. Kept as a
(strengthened) GAP rather than condemned, since a detachable/spare printer accessory isn't explicitly
ruled out by the hardware REQ. ⇒ Refs updated to `REQ-0819.0,REQ-0819.6,REQ-0819.8`.
source: `TFTS Requirements Matrix.xlsx`, REQ-0819.0, REQ-0819.6, REQ-0819.8.

**Q53 · SURFACE · HHD C4103970** — Does a legacy "Old Barcode Redemption (BRS)" flow exist on Glider
HHD? Full search (filename + content) across the entire local requirements library found zero mentions
of "BRS"/"Old Barcode Redemption" anywhere; FBD-100317/483 both confirm Glider HHD validates multi-use
barcodes only and explicitly does NOT use single-use functionality. This upgrades the 2026-07-17
coherence-audit suspicion to a confirmed spec gap.
A: — source: FBD-100317, FBD-100483 (both say Glider HHD ≠ single-use/BRS). ⇒ **GAP**, likely
candidate for retire/rewrite pending engineer confirmation.

**Q54 · VALUE · HHD C4103972 / C4103973** — Is there a documented pass-type colour scheme (adult vs
child) on the HHD smartcard-inspection result screen? Checked FBD-100236/250, the HHD Inspection and
Validation Design Note, and Smartcard Use Matrix.xlsx — wording "varies depending on smartcard" is
confirmed, colour is not.
A: — source: — ⇒ **GAP** (screen-detail only; the underlying pass-differentiation behaviour is
grounded).

**Q55 · VALUE · HHD C4103975 / C4103976** — Is the ~90-minute smartcard-inspection revalidation window
a real, separately-documented figure, or was it copied across from the unrelated Glider/NIR cEMV
inspection Maximum Journey Time (FBD-100651/716, a bank-card penalty-fare matching window, not a
smartcard revalidation window)? No spec documents any smartcard-specific revalidation window.
A: — source: — ⇒ Reframed to "the currently configured window" (assumed-knowledge value) rather than
asserting the borrowed 90-minute figure; **flag** the possible cross-section duplication for
confirmation.
**A (resolved from TFTS Requirements Matrix, 2026-07-22):** The underlying behaviour is real and
HHD(NIR)-specific — not borrowed from the unrelated cEMV MJT. **REQ-3488.0** "Apply Countdown Timer to
a Smartcard - HHD NIR": "As a Transport Operator I want the HHD (NIR) to apply a countdown timer to
[legacy smartcards: iLink, Belfast Visitor Pass, aLink, Staff/Spouse, EA Pupil/FE cards] when they
validate, so that cards revalidated within the countdown timer count as **transfers not journeys**...
Countdown Timer is configurable by Translink in the Back Office." (Commonality: HHD (NIR), PV (NIR),
GV.) This confirms the case's already-applied "assumed-knowledge configured window" framing was the
right call — the window is real and configurable, just not the borrowed 90-minute cEMV figure. ⇒ No
wording change needed (the case already avoided hard-coding a number); Refs strengthened with
`REQ-3488.0` alongside the existing Smartcard Use Matrix/Design Note citations.
source: `TFTS Requirements Matrix.xlsx`, REQ-3488.0 (HHD NIR), cross-referenced with REQ-3489.0 (GV)/
REQ-3490.0 (PV NIR) siblings.

**Q56 · SURFACE · HHD C4103995** — Does the HHD pair to an *external* printer by presenting an NFC
chip, or does every HHD carry its own integrated 2" thermal printer (REQ-0819.6)? No document mentions
an external/NFC-paired printer for any device; the only NFC/BT-paired peripheral documented is the
M020 payment reader (Bluetooth, FBD-100320) — already covered by its own case, C4104007.
A: — source: REQ-0819.6, FBD-100320. ⇒ **GAP**; likely mislabelled duplicate of the M020 pairing test.
**A (resolved — condemned, 2026-07-22):** Confirmed wrong, not just uncited. REQ-0819.6 is
unambiguous: the HHD's printer is its own integrated 2" thermal hardware. REQ-0819.8 confirms the
HHD's only documented NFC/Bluetooth pairing use is to an external **payment card device** (the M020),
not a printer. There is no external/NFC-paired printer for the HHD to pair to. ⇒ **C4103995
condemned** (`ZZ_DELETE_REVIEW`) as a mislabelled duplicate of the M020 NFC-pairing case (C4104007),
not a distinct real scenario.
source: `TFTS Requirements Matrix.xlsx`, REQ-0819.6, REQ-0819.8.

**Q57 · VALUE · HHD C4104002** — What are the real Android OS versions the HHD is upgraded between?
Case asserts "OS 7" → "OS 8" specifically; REQ-0569.0/1618.0/3511.0 confirm TMS-managed OS upgrades on
Android generically but no document names any specific version number.
A: — source: — ⇒ **GAP** on the specific version pairing only; the underlying upgrade capability is
grounded.

**Q58 · CONFLICT/BUG? · GV old suite 2754367/2754368 vs 2754377 (Legacy Support — POS top-up then GV validation)** — logged 2026-07-23, consolidation-completeness audit
Old suite 14973's "Legacy Support" section has 13 near-identical cases testing a smartcard topped up
on a legacy POS device then presented to a GV. Every iLink-family case (Adult/Child Zone 1-4/NW,
C2754367-376) records the **same outcome**: success screen, gate opens. But the **Metro Travelcard**
pair (Adult/Child, C2754377/2754378) records the **opposite** outcome on the same setup: "Validation
Failed" screen, gate stays closed. No spec in `REQS_DIR` was found governing GV-side legacy top-up
behaviour (this whole area is needs-spec, see `old-suite-audit.md` §3b). Is the Travelcard rejection
a genuine product-specific rule (e.g. Travelcard requires a different revalidation step before the GV
will accept it), or was it a defect/limitation at the time the old case was written that may since be
fixed? A case can't assert either outcome as gospel without knowing which.

## Session 2026-07-23 — TVM consolidation-COMPLETENESS audit (suite 30284 vs 9 old suites)

**Q59 · LIVE?/SURFACE · old-suite C2041439/C2041440 (EMV Offline Payment — Chip & PIN / Contactless), C1831600 (Chip & Pin — Purchase with No Network Availability)** — logged 2026-07-23
Old suite describes the TVM's Ingenico/ChipDNA terminal completing an EMV payment in a "pre-authorised"
state while the TVM itself is offline (LAN removed, up to 10 minutes for SIM failover). Given Q33 in
this same register already confirmed the TVM has a genuine WAN(Ethernet)↔SIM(cellular) comms failover
(so "offline" may not mean fully disconnected — it may just mean mid-failover-window), it's unclear
whether "EMV offline/pre-authorised payment" is: (a) a distinct terminal-level capability (ChipDNA
completing a transaction with no back-end authorisation call at all, settled later) that's genuinely
untested in the new suite, or (b) already subsumed by the comms-failover behaviour (Q33) and doesn't
need a separate case. Not authored as a new case — the mechanism (ChipDNA "Commit"-phase failure
handling) isn't detailed enough in the old suite to write without guessing. Is EMV offline/pre-auth
payment a real, distinct, still-relevant TVM capability?
A: — source: old suite 6160 (C2041439, C2041440, C1831600) only; no FBD/REQ match found in `REQS_DIR`.
⇒ **GAP** — no case authored pending an answer.

**Q60 · SURFACE · new-suite Alarmboard & Enclosure cluster (C4103768–C4103774), consolidation-completeness addition above (Alarmboard — Request Version)** — logged 2026-07-23
All live alarmboard maintenance cases are worded Kiosk-only ("Kiosk TVM", "Kiosk alarmboard"), and the
new "Request Version" case added this session follows the same Kiosk-only scoping (matching the old
suite's R2-MAN-FNC-TVM source, which wasn't itself model-specific in its wording). Old suite 6160 is
the shared/base suite (pre-dating the Kiosk/Astreo split), so it doesn't settle whether Astreo TVMs
have an alarmboard at all, or whether Astreo alarmboard maintenance was a real capability silently
dropped in consolidation. Does the Astreo TVM have an alarmboard, and if so should the alarmboard
cluster (887794) be widened from "Kiosk only" or does Astreo genuinely have no alarmboard?
A: — source: none found (old suite 6160 doesn't specify a model). ⇒ **GAP** — left as Kiosk-only
(matching the live suite's existing scoping convention), not widened without confirmation.
A: — source: old suite 14973 C2754367/C2754368/C2754377/C2754378 (full case bodies read). ⇒ Both
outcomes carried forward as **NEEDS-SPEC** scaffolding cases in
`proposals/gv-suite-restructure/pending-integration-scaffolding.cases.yaml` §9 (Legacy Support), with
the divergence flagged explicitly in the Travelcard case's Expected text rather than silently picking
one. Not pushed live — needs-spec, per this suite's established stance.

## Session 2026-07-23 — HHD consolidation-COMPLETENESS audit (suite 30285 vs 4 old suites, 2,087→211)

Full accounting in `proposals/coherence-audit/fixes/hhd-consolidation-completeness.changelog.md`. George's
brief named Sign On / role-based access as the priority family (worried a role×method matrix could be
silently folded away); the full old-suite Operator/Supervisor/Technician sign-on matrix (42 old cases
across 4 suites) was walked case-by-case against the live section. Two genuinely distinct scenarios were
found missing (no case, no Data-variation line) and have been added (C4104127, C4104128); everything
else in the matrix (ID entry, smartcard, invalid credentials, duty number, Message/Word&Colour of the
Day, topology NIR/Metro, route selection, sign-off incl. forced-by-docking, auto sign-off, break-mode
mode-resume, Technician/Supervisor sign-on+off, battery-replace sign-on) was confirmed present.

**Q61 · RESOLVED-BY-FIX · HHD, Sign On matrix — "Device Remains Locked" (Supervisor override failure)**
Old suite (5446 C2759053/C2759057, 13958 C2598944, 5446 C2735568 — 4 cases across 2 suites, all
consistent) models a **negative** counterpart to C4103926 ("Supervisor unlocks a PIN-locked HHD"): if the
Supervisor's own PIN entry is wrong, or times out, the device stays locked — the override itself can
fail. C4103926 only asserts the positive path; nothing in the live 211-case suite covered the negative.
A: — source: 5446 C2759053/C2759057/C2735568, 13958 C2598944 (bodies read in full). ⇒ **Fixed**: new case
C4104127 ("Sign On — an incorrect Supervisor PIN leaves a PIN-locked HHD locked"), Refs REQ-0099.1 (same
requirement family as C4103926).

**Q62 · RESOLVED-BY-FIX (UNCONFIRMED) · HHD, Sign On matrix — mode reset on a FULL sign-off vs a break**
Old suite 5446 C3509566 ("Device remains in Inspection mode on sign in after signing off in Inspection
Mode") and C3509644 ("Device defaults back to Inspector Mode on sign in after signing off in Validation
Mode") both test a **full sign-off/sign-on cycle** (not a driver break) and land on the *same* outcome —
Inspector Mode by default — regardless of the mode active before sign-off. This is a different trigger
from C4103913 ("Break-Mode Sign On — HHD resumes the same mode after an operator break"), which is
specifically about breaks and asserts the *opposite* effect (mode is preserved, not reset). Neither old
case is superseded/flagged, and nothing in the live suite covers the full-sign-off-resets-mode behaviour
at all — a real gap, not equivalence-class overlap with the break case, because the trigger and even the
direction of the outcome differ.
A: — source: 5446 C3509566/C3509644 (bodies read in full); no REQ/FBD found this pass distinguishing
"full sign-off" from "break" as separate mode-reset triggers. ⇒ **Fixed but marked UNCONFIRMED**: new case
C4104128 ("Sign On — device resets to Inspector Mode after a full sign-off"), Refs FBD-100651, carrying
an explicit `**UNCONFIRMED**` marker — confirm live before running.

**Q63 · SURFACE · HHD, Smartcards & ABT / Smartcard Inspection / Top-Ups / Metro-Ulsterbus Products —
missing product-family enumeration** — logged 2026-07-23
The ~100 old-suite "Validate/Inspect <Product> Smartcard Product" cases (32 named product sections in
5446 alone) were correctly consolidated to representative cases (structure.md's stated intent), but the
representative cases carried **no explicit "Data variations:" line** naming which of the ~30 product
families they stand in for — a plain gap against `docs/gherkin-standard.md`'s "Data variations are an
Examples list... list them in the case" rule. Same pattern found in Top-Ups (4103879 said "across
products" with no list) and Metro/Ulsterbus Products (4103875/4103876 named no specific product). A
background research pass opened `Smartcard Use Matrix.xlsx` (cell-by-cell via openpyxl) and
`TFTS Requirements Matrix.xlsx` "Description" sheet and confirmed live HHD applicability + a REQ-id
citation for ~30 of the ~32 old-suite product names.
A: — source: `Smartcard Use Matrix.xlsx` (Smartcard Validation / Smartcard Topups sheets, HHD = merged
E:F columns, Glider/NIR), `TFTS Requirements Matrix.xlsx` Description sheet (REQ-0837–0919, REQ-2025/2026,
REQ-2461/2463/2618/2633/2070/2065, REQ-3473/3475/3478/3480 — full per-product id list in the fix
changelog). ⇒ **Fixed**: Data-variations lines + REQ-id Refs added to C4103820/4103822/4103826 (Validate),
C4103840 (Annulment — 24+ flagged GAP, no REQ id found), C4103879 (Top-Ups), C4103875/4103876 (Metro/
Ulsterbus Products), C4103971 (Smartcard Inspection). Two product names flagged rather than asserted:
**iLink NW** (no distinct REQ found — folded as a GAP marker, only generic iLink + NW zone flag
evidenced) and **Metro TaxSmart / Joint TaxSmart** (REQ found but marked `#ARCHIVE#` — needs an engineer
call on whether still deployed; not yet added to any case pending that answer).

**Q64 · LIVE? · HHD, Annulment — "24+" discount product** — logged 2026-07-23
Old suite (5446/13958, "Annulment - Annul 24+ - Card") tests a distinct "24+" discount product
annulment, grouped with yLink under ticket Layout 7a/7b ("Half fare, yLink and 24+") but otherwise
undocumented as its own product line in the sources checked this pass (Smartcard Use Matrix / TFTS
Requirements Matrix). Is "24+" a currently live, distinct product (a discount band alongside yLink), or
a superseded/renamed product?
A: — source: old suite 5446 C1706672, 13958 C2598723 only; no REQ id located. ⇒ **GAP** — carried as a
Data-variation on C4103840 with an explicit GAP marker rather than a confirmed fact; needs George/an
engineer to confirm the product still exists.

**Q65 · SURFACE · HHD, Revenue Inspection / Smartcard Inspection — can a Supervisor (not just an
Operator) validate/inspect?** — logged 2026-07-23
Old suite 5446 C4068377 ("Scenario: Supervisor can Validate/Inspect") asserts Supervisor role also has
inspection/validation access when signed on at an NIR stop — distinct from the default assumption that
only an Operator inspects. Live suite's inspection cases (C4103971–C4103990) are written role-agnostically
("the HHD is in Inspector Mode signed on to..."), which doesn't contradict the old case, but doesn't
explicitly assert Supervisor eligibility either — a soft gap (no negative claim to fix, but no explicit
positive coverage of the Supervisor path). Not treated as blocking (the generic wording already covers
"whoever is signed on"); logged for confirmation rather than authoring a dedicated case on a single old
scenario with a `None` precondition/expected (C4068377's body is a bare three-line unstructured
scenario, no detail to ground a full case on).
A: — source: 5446 C4068377 (title only, body is unstructured/empty). ⇒ **GAP, not authored** — too thin
to ground a case; flagged for the engineer rather than guessed.

## Session 2026-07-23 — PV consolidation-COMPLETENESS audit (suite 30255 vs old suite 10047, the 1,144→136 reduction)

**Q61 · SURFACE/LIVE? · old-suite C4099861/C4099862/C4099863/C4099864/C4099865/C4099866 ("HMI - EMV -
Failure - Cancelled/Unknown/Queue Full/Queue Full - Tap Error" and "HMI - ISAM - Failure - Queue
Full/Queue Full - Tap Error"), Non-Functional / Human Machine Interface** — logged 2026-07-23,
the lead this session was scoped to resolve first
Do four (six, counting the ISAM pair) distinct PV HMI screens exist — a Cancelled state, an Unknown
error state, and a Queue Full / Queue Full-with-Tap-Error state for cEMV taps (plus the same Queue
Full / Queue Full-Tap Error pair again for "ISAM") — that the 1,144→136 consolidation silently
dropped, or were they never real to begin with?
Evidence gathered, all pointing the same way:
- The old cases themselves carry **zero functional content** — all 11 siblings in this flat section
  (Success, Failure-Expired, Failure-Declined, Failure-Denylist, Failure-Passback, plus the 6 in
  question) share the **identical** generic body ("Given the HHD is displaying the screen described
  in the title... When inspected and compared to the GUI Presentation Layer doc... Then it matches"),
  with no trigger, mechanism, or distinguishing detail for any of them — so the old suite provides no
  grounding to copy from, only a title.
- The current Overflow UX export (`knowledge/flows/pv-flow-annotations.md`) lists all **27** confirmed
  Platform Validator screens by name/number — none is called Cancelled, Unknown, Queue Full, or Tap
  Error. Its own annotation for the one cEMV decline screen that *is* real (`1.3.3 Invalid Card`) names
  exactly 8 causes (unsupported scheme, card clash, expired, invalid BIN, AID fail, ODA fail, deny
  list, negative list) — the same list already grounding `C4101088` — with no 9th/10th cause matching
  any of these four names.
- The old suite's own **functional** decline-reason tests (`Functional / ABT / Declined Taps`:
  `C2681553` Deny List, `C2681554` Negative List, `C2681555` Expired, `C2681556` BIN List) never
  exercise a Cancelled/Unknown/Queue-Full/Tap-Error condition either — so even the old suite's real
  behavioural coverage doesn't corroborate these four as live decline paths.
- A full-text search of the entire local `REQS_DIR` requirement library (352 documents, every
  docx/xlsx/pdf/txt/csv) for "tap error" returns **zero hits anywhere**; "queue full" returns zero
  hits; "queue" alone returns 129 hits, all for unrelated back-office/ticket-print queues (the
  CloudFare ABT Transaction Queue, ETM/POS ticket "shopping basket" queuing) — never a card-reader
  failure screen. "Cancelled" returns 238 hits, all about transaction annulment/portal-edit
  cancellation — never an EMV tap-cancelled screen state.
- "ISAM" is a real term (**ITSO Security Application Module** — the smartcard security chip housed in
  a POST/reader, defined in the CONOPS glossary, discussed in the context of the Wayfarer 6 ETM's SAM
  socket) but it names a **hardware component**, not a PV screen state — nothing in the local library
  ties an "ISAM Queue Full" or "ISAM Tap Error" condition to the Platform Validator's HMI.
- Checked for the same naming pattern (Unknown/Cancelled/Queue Full/Tap Error/timeout) across all
  1,144 old-suite titles — the only other hit, "Technician - Navigation - Page Timeouts"
  (`C2667023`/`C3275917`), is unrelated (Technician Menu idle timeouts, already resolved via Q32/
  `C4102181`) and confirms this 6-case cluster is an isolated anomaly, not part of a wider pattern of
  dropped states.
So: no source (old case body, live UX export, functional old-suite behaviour, or the requirements
library) confirms these four/six screens as real. This looks like a stamped-out placeholder set (11
near-identical titles covering a candidate list of EMV/ISAM outcome names) where several entries were
never confirmed to correspond to an actual shipped screen — not a case of consolidation deleting
proven coverage.
A: —
source: `knowledge/flows/pv-flow-annotations.md` (27-screen Platform Validator catalogue, `1.3.3
Invalid Card` 8-cause annotation); old suite 10047 `C2681553-556` (Declined Taps); full-text sweep of
`REQS_DIR` (352 entries) for "tap error"/"queue full"/"queue"/"cancelled"/"isam"; old-suite
title sweep (1,144 titles) for the same terms. ⇒ **Not actioned as a suite change** — per
`docs/gherkin-standard.md`'s no-gap-filling rule this is an "unknown *what*" (existence in doubt), not
an "unknown *how*", so it is left as an open question for the engineer rather than added on
inference. If the answer is "yes, real, still needed" — cite the mechanism (what makes a cEMV tap
read as Cancelled vs Unknown vs Queue Full, and what "ISAM Queue Full" physically is) and I will
ground+add the missing screen-validation/decline-reason coverage. If "no, obsolete/never shipped" —
no suite change needed and this closes as confirmation the consolidation lost nothing real.

**Q62 · SURFACE/GAP · new-suite HMI Screen Validation / Validation Screens — missing `1.3.3 Invalid
Card`** — logged 2026-07-23, found while resolving Q61
Unlike Q61 (unconfirmed existence), this screen **is** confirmed real — it's in the Overflow 27-screen
catalogue and is the very screen `C4101088` (`cEMV — decline reasons`) grounds its 8 decline causes
against. But there is **no dedicated HMI Screen Validation case** for it in suite 30255 (the
`HMI Screen Validation / Validation Screens` section has a case for every other catalogued screen —
`1_3_1`, `1_3_7`, `1_3_8`, `1_3_9`, `1_3_16`, etc. — but none numbered `1_3_3`). The functional case
covers the decline *causes*, but per this repo's HMI/Functional split doctrine
(`docs/test-practices.md`, "a dedicated per-screen layer... so the functional layer never fragments")
the screen *rendering* is meant to be independently validated the same as its 26 siblings. Old suite
10047's smartcard "Error Screen - Invalid Card" (`C3207743`) turned out on inspection to be a
different screen ("Card Not Yet Valid", i.e. `1.3.2`), not this one, so it isn't usable as the old-case
grounding source for `1.3.3` either — no old-suite HMI case for `1.3.3 Invalid Card` was found.
Is a screen-validation case for `1.3.3 Invalid Card` expected (matching every sibling screen), or was
it deliberately left out because `C4101088` already exercises its content functionally?
A: —
source: `knowledge/flows/pv-flow-annotations.md` (screen `1.3.3 Invalid Card` in the 27-screen
catalogue); suite 30255 `HMI Screen Validation / Validation Screens` (26 cases, no `1_3_3`); old suite
10047 (`C3207743` checked and ruled out — different screen, `1.3.2`). ⇒ **Not actioned** — no old-suite
case exists to ground a new one on, so adding one now would need the same Overflow screenshot/UI
Presentation Layer source the other 26 HMI cases cite, not invented wording. Left as a question rather
than authored blind.

---

## Session 2026-07-23 — HHD card/credential-variant sweep (suite 30285, modelled on the PV C4100998 scheme miss)

**Context.** George flagged that the PV consolidation-completeness pass (`pv-consolidation-completeness.changelog.md`) had wrongly signed off `C4100998`'s "Variation — Visa, Mastercard, mobile wallet" line as a correctly-folded consolidation of 13 old-suite card-scheme cases (Visa/Mastercard × Debit/Credit, Maestro), when it actually silently dropped the Debit/Credit distinction and Maestro. This session re-swept HHD (suite 30285) for the identical pattern — a representative card-payment/card-scheme case that names only one scheme, with no `Data variations:` line for the rest of the family the old suite tested.

**Finding — confirmed, same pattern, on HHD's M020 card-payment family:**
- Old suite 5446/13958 `Functional / Card Payments` tests 5 chip-and-PIN scheme combinations
  (Visa Credit, Visa Debit, Mastercard Credit, Mastercard Debit, Maestro — `C1692496/1694407/1694409/
  1694408/1694410`) and 2 contactless schemes (Visa, Mastercard — `C1692498/1694412`) as separate,
  mechanically identical cases. Live suite 30285 folded these into `C4103804` ("...a Visa credit sale
  completes...") and `C4103805` ("...a Mastercard debit sale completes...") for chip-and-PIN, and
  `C4103806`/`C4103807` for contactless — each naming only the one scheme in its title/body, no
  `Data variations:` line for the other 3 (chip-and-PIN) / 1 (contactless-Mastercard).
- Old suite 5446 `Card Payments / Validation checks` also tests `Diners Declined` (`C1694411`,
  REQ-0890.0) as a distinct decline reason (scheme rejected outright, no PIN prompt) — not present
  anywhere in the live suite's generic `Card Declined` family (`C4103808/09/10`, which cover
  provider-declined/expired/blocked only).
- The same pattern repeats one layer over in `Functional / Revenue Inspection (cEMV/RID)`: old suite
  5446's `ABT (Account Based Ticketing)` section tests 5 named schemes as "Valid Card Inspection"
  (Visa Debit/Credit, MasterCard Debit/Credit, Maestro — `C3498105-109`) and 2 as "Invalid Card
  Inspection" (American Express, Diners — `C3498112/113`). Live suite folded these into `C4103980`
  ("a valid card inspection succeeds...") and `C4103984` ("an unsupported scheme is declined...") with
  no scheme names at all in the former, and only the generic phrase "a scheme other than Visa,
  Mastercard or Maestro" (no worked examples) in the latter.

A: Fixed directly (not escalated — this is the same class of fix the PV session should have made, not
a new-behaviour question). Added explicit `Data variations:` lines to all 6 cases naming the full
scheme/type list evidenced by the old suite, citing the old cases' own REQ ids
(REQ-0163/REQ-0890/REQ-1384/REQ-1488/REQ-1489/REQ-1491/REQ-1514/REQ-1516/REQ-1630/REQ-1722/REQ-1723/
REQ-1854/REQ-2519 for the M020 family; FBD-100716 for the Revenue Inspection family, which had no REQ
id on the old ABT Card Inspection cases either). See
`proposals/coherence-audit/fixes/hhd-card-variant-sweep.changelog.md`.

**Secondary finding — logged, not actioned (Q66).**

**Q66 · SURFACE/LIVE? · HHD "cEMV Validation" (NIR Rail passenger boarding via bank card, distinct from
Revenue Inspection's Glider inspector-mode taps)** — logged 2026-07-23
Old suite 5446 carries a `cEMV Validation` family (duplicated across two near-identical sections,
`C2766456-471`/`C2766465-496`, REQ-3373.0/REQ-3563.0) testing a passenger boarding a **NIR Rail** HHD
route by presenting a cEMV bank card directly (not a Glider inspector tap) — including two "Capped
Travel" cases (`C2766492` Visa, `C2766493` Mastercard) where repeat same-day presentations are charged
a capped fare rather than the full fare each time. A full title/body sweep of the live 213-case suite
30285 found **no case anywhere** exercising cEMV fare-capping — the only live "cEMV card" mentions are
a generic payment-method value inside unrelated Data-variations lists (e.g. C4103784/4103785 ticket
sale, C4103829/30 top-up), and the live `Revenue Inspection (cEMV/RID)` family is confirmed Glider-only
(`Given the HHD is in Inspection Mode on a Glider Tap-On-Only route`), not NIR boarding.
Is NIR-Rail cEMV boarding-with-capping still a real, distinct HHD behaviour (as opposed to something
superseded by the Glider-only Revenue Inspection model), and if so what's the current capping rule /
REQ id (REQ-3373/REQ-3563 predate this pass and weren't independently re-verified against the live
system)?
A: —
source: old suite 5446 `cEMV Validation` sections (`C2766456-496`, 16 cases across 2 duplicate
sections); live suite 30285 full-text sweep (213 cases, `hhd-30285-raw.json` this session's dump) for
"cEMV"/"Capped"/"cap". ⇒ **Not actioned this session** — this is a distinct behavioural question
(does NIR cEMV fare-capping still exist as a boarding path), not a scheme-enumeration completeness gap,
so authoring a new case here would be gap-filling outside this session's scope (a targeted
card/scheme-variant re-check). Flagged for a dedicated follow-up once answered.

**Re-checked the 8 already-fixed cases (C4103820/4103822/4103826/4103840/4103879/4103875/4103876/
4103971) against `Smartcard Use Matrix.xlsx` for completeness.** Attempted a column-level cross-check
of the HHD Glider/NIR columns against each case's Data-variations list. The flattened `.xlsx.txt`
extract (`_text\Useful Documents\Smartcard Use Matrix.xlsx.txt`) does not preserve the original
spreadsheet's merged-cell column boundaries reliably enough to re-derive with confidence which of the
14 Yes/No columns are HHD's Glider/NIR pair independently of the prior session's own determination (it
recorded "HHD is the merged E:F columns" from viewing the live spreadsheet directly, which this
text-only re-derivation cannot safely reproduce or contradict). Rather than assert a product
addition/removal from an ambiguous re-parse, this re-check is left as **spot-checked, no new
discrepancy confidently found** — no changes made to those 8 cases this session. A follow-up with
direct spreadsheet (not flattened-text) access could re-verify column boundaries properly if a stronger
completeness guarantee is wanted.

---

## Session 2026-08-03 — TVM `MODE-ALL` product-ownership contradiction (suite 30284)

**Context.** While fixing the ETM/POS/TVM `MODE-ALL`-hardcodes-one-operator wording bug (see
`proposals/etm-suite-restructure/mode-all-route-hardcoding.changelog.md`), 27 of 31 flagged TVM cases
were safe mechanical rewordings (Adult Single, Child Single, Family & Friends — all confirmed shared
products per `knowledge/projects/translink.md`). 4 were **not** auto-fixed because they raise a real
product-ownership question, not just a wording one.

**Q35 · CONFLICT/VALUE · TVM `C4104866` "Ticket Issue — 1 Month Return ticket"**
The case is tagged `MODE-ALL` (shared, re-run per mode) and its precondition names the example
product as **"Metro Adult 1 Month Return."** But `knowledge/projects/translink.md` (product-ownership
table, sourced from the old-suite cross-tab) explicitly lists **"Month Return"** as **Ulsterbus-only**
— it is not in the Shared or NIR-only lists at all. Is Month Return actually sellable on Metro (in
which case the product-ownership table is stale and needs correcting), or is this TVM case simply
mistagged/mis-worded and should be `MODE-ULSTERBUS-ONLY` with the "Metro" wording removed entirely?
A: —
source: `knowledge/projects/translink.md` product-ownership table ("Ulsterbus-only: Bus Rambler,
Jobseeker Single, Month Return, Rail Substitution Service"); live TVM case `C4104866` custom_preconds
(pulled via `TestRailClient.get_case`, 2026-08-03). ⇒ **Not actioned** — left exactly as-is pending
George's answer, rather than guessing which side is wrong.

**Q36 · VALUE · TVM `C4103686`/`C4104859`/`C4104860` "Ticket Issue — Evening ticket" (cash/Chip&PIN/
contactless)**
All three are tagged `MODE-ALL` and worded "an example **Metro** Evening Adult ticket" / "a TVM inside
the **Metro** Evening validity window." Unlike Month Return, "Evening" does not appear anywhere in
`knowledge/projects/translink.md`'s product-ownership table at all (neither the Shared, NIR-only, nor
Ulsterbus-only lists), so there is no existing citable answer either way — is the Evening ticket sold
on Metro only, on all three modes, or on some other subset?
A: —
source: `knowledge/projects/translink.md` (no mention of "Evening" in the product-ownership section);
live TVM cases `C4103686`, `C4104859`, `C4104860` (pulled via `TestRailClient.get_case`, 2026-08-03).
⇒ **Not actioned** — left as-is pending an answer; do not infer from silence that it's shared.

**Why these weren't just reworded like the other 27:** the safe fixes (Adult Single, Child Single,
Family & Friends, Popular shortcut, Day/Day Return, Kiosk/Astreo commissioning language) all had a
confirmed-shared product backing the generic rewording. These two don't — genericising the wording
here without knowing the real mode-ownership would risk silently erasing a genuine `MODE-ULSTERBUS-ONLY`
mis-tag (Q35) or asserting shared-ness with zero source (Q36), which is exactly the kind of invention
the no-gap-filling rule exists to prevent. Once answered, fix the wording (same mechanism as the other
27) and/or the `MODE-*` tag as the answer dictates.

---

## Session 2026-08-03 (cont.) — PV and HHD re-checked for the same MODE-ALL pattern

**Context.** After fixing ETM/POS/TVM's `MODE-ALL`-hardcodes-one-variant bug, George asked whether
PV/HHD/GV needed the same check — they'd been missed from the first pass. Re-scanned all three.

**GV: clean, no bug.** GV's `MODE-ALL` dimension is gate **direction** (Entry/Exit/Bidi), not
fare/operator mode (confirmed in `proposals/gv-suite-restructure/mode-coverage.md`). Every "NIR"
hit in a `MODE-ALL` case is simply accurate — GVs are only ever deployed in an NIR/rail context, so
there's no wrong "other mode" for the wording to contradict. Not the same bug class; no action taken.

**PV: same bug, fixed.** 6 `MODE-ALL` cases (iLink Zone 1-4/NW validation + Belfast Visitor Pass,
`C4100987`/`C4104450`/`C4104451`/`C4104453`/`C4104455`/`C4104457`) said "a **Rail** PV" in their
precondition while their own Expected field states "Run for Adult and Child, **under Glider and
Rail**" — a direct self-contradiction. Fixed: `a Rail PV` → `a PV` in all 6. Re-audit clean (185
cases, 0 blocking).

**HHD: same bug, 16 fixed, 6 flagged.** 16 `MODE-ALL` cases hard-coded "Metro" for a confirmed-shared
product (Adult/Child Single, Basket, Multi-Journey Top-Up) or cited "the NIR fares export" as the
sole check source for a case meant to run under both NIR-Rail and Glider — fixed the same way as
ETM/POS/TVM (drop the mode name / generalise to "the currently configured fares export").

**Q37 · GROUNDING · HHD `C4103907`/`C4103908`/`C4103921`/`C4103944`/`C4103945`/`C4103946`** — NOT
auto-fixed, different in character from the other 16
Each of these names one mode inside an explicit **"worked example: ..."** clause, not as a bare
precondition assertion the way the fixed cases did — and two already self-caveat both sides
("Glider TOO live; NIR TOTO future"). Per the gherkin standard's own worked-example rule, a `MODE-ALL`
case only needs ONE concrete example; it isn't required to illustrate every mode. So the open question
isn't "is this wrong" the way the other 16 clearly were — it's whether an asymmetric single-mode
illustration inside a shared case is fine as-is (a tester adapts it to whichever mode they're
running), or whether it should carry a matching example for the other mode too, or whether one of
these six is actually mode-specific and mistagged `MODE-ALL`. Specific cases:
- `C4103907` (Sign On topology) — example only shows an NIR station (Yorkgate); no Glider-side example.
- `C4103908` (Sign On route selection) — example only shows "G1 Glider route (Metro)"; no NIR-side example.
- `C4103921`/`C4103946` (penalty fare warning, functional + ticket-format) — explicitly caveat
  "Glider TOO live; NIR TOTO future," i.e. may be intentionally Glider-only-for-now within a case
  meant to eventually cover both once NIR TOTO ships.
- `C4103944` (faulty smartpass/smartcard receipt ticket format) — names BOTH a NIR ticket layout
  and a Glider format side by side in one worked example, unlike the others' single-mode pick.
- `C4103945` (travel receipt/print-test ticket) — cites only NIR ticket layout numbers (17, 15);
  unclear if a Glider equivalent format exists or applies.
A: —
source: live HHD cases (pulled via `TestRailClient.get_case`, 2026-08-03); `docs/gherkin-standard.md`
"Concrete grounding" section (one worked example is sufficient, doesn't require covering every
mode). ⇒ **Not actioned** — left exactly as-is pending George's read on whether these are fine,
need a second example, or are actually mistagged.

## Session 2026-08-05 — ETM flow-map coherence audit (new UX-transcription cross-check, suite 30254)

**Context.** A second, independent grounding source came online: all 16 ETM boards from the Overflow
UX designs were transcribed (via the Claude Chrome extension) into `knowledge/flows/translink-etm-*.md`
flow-maps, then cross-checked against every live case (coverage pass) and then against case *content*
(correctness pass — does what the case says match what the flow-map documents, not just "does a case
exist"). This is complementary to the spec-grounded sessions above, not a duplicate — different source
document, catches different things. 30 confirmed correctness defects found (full detail:
`proposals/etm-suite-restructure/correctness-audit-2026-08-05.md`); the subset below are the ones that
need a human answer rather than a straightforward reword-to-match-the-flow-map fix.

**Q1 · VALUE · driver-signon, path 5** — What is the exact "x hours" threshold before Driver Sign On
enters Communications Locked? Not stated in the Overflow transcription.
A: — source: —

**Q2 · SURFACE/LIVE? · driver-menu-annulment, path 9** — Annulling a transaction older than 1 minute —
is the Annul option hidden/disabled, or does another error surface? No screen shows this state.
A: — source: —

**Q3 · CONFLICT · flu-basket-mode, path 4** — "Above Threshold" board content reads incomplete/
truncated in the source (annotation "Type something") — is there a missing PIN-entry step not shown?
A: — source: —

**Q4 · SURFACE · flu-basket-mode, path 10** — Quantity-change-rejected error variants: source
annotation says "Need to add possible different errors" — the design doc itself is incomplete. What
are the actual error variants?
A: — source: —

**Q5 · SURFACE/LIVE? · flu-navigation, path 10** — What happens if a currency-toggle is attempted on a
route not enabled for multi-currency? Silently ignored, or something else? Not screened on this board.
A: — source: —

**Q6 · CONFLICT/BUG? · flu-printer-travel-mode, path 9 (case C4100641)** — "Out of Service Error"
(07.0.x) trigger condition isn't detailed in this board's annotations — is it actually printer-related,
or does it belong to a hardware-fault board not yet transcribed? Case 4100641 currently asserts a
printer-triggered cause built on this unconfirmed assumption.
A: — source: —

**Q7 · LIVE? · technician, paths 13/14** — Decommissioning sub-flow is annotated `===This function is
pending design===` in the raw transcription. Is it implemented and testable, or should these paths be
marked UNCONFIRMED until design lands?
A: — source: —

**Q8 · CONFLICT · technician, path 33** — Two source connections from "Other Devices" to "BV Device
Selected" — one unlabelled, one "R2-4". Distinct trigger keys/slots, or a transcription duplicate?
A: — source: —

**Q9 · CONFLICT · barcode-scanning, paths 15/16 (case C4100628)** — 12.5.1 "Ticket Valid" screen's
'Valid' key has two conflicting transcribed connections: one to the "Online?" decision, one direct to
"Back to the FLU screen". Which is real?
A: — source: —

**Q10 · CONFLICT · barcode-scanning, paths 26/27** — 12.5.3/12.5.3.1 and 12.5.4/12.5.4.1 paging
screens: source states these aren't wired into the main decision tree. Reachable at all, or dead
transcription artefacts?
A: — source: —

**Q11 · CONFLICT · barcode-scanning, general** — "Back to the FLU screen" node is never explicitly
wired to "02.0.0 FLU Home" anywhere in the raw connections list — is that the actual target? Nearly
every path ending "back to FLU" rests on this assumption.
A: — source: —

**Q12 · SURFACE/LIVE? · revenue-limit, path 4 (case C4100634)** — How does a Supervisor or Technician
actually clear a Revenue-Limit-locked ETM? Mechanism not shown on the board; the case only asserts the
requirement, not the unlock action.
A: — source: —

**Q13 · LIVE? · displays-leds-audio, all CardReader/PID states** — Which upstream flow drives the
device into each PID/Info and CardReader/LED state? Trigger mapping is unconfirmed on the source board
for all 8 CardReader/LED codes and the PID/Info states.
A: — source: —

**Q14 · VALUE · displays-leds-audio** — CardReader/LEDxxxx letter-code legend (G/N/A/R meaning) is
undefined — no legend/annotation exists on the board.
A: — source: —

**Q15 · BUG? · regression-register.md rows 301937/301828** — These two NEEDS GEORGE rows carry no
topic information. Nine separate flow-map passes above independently flagged them as "can't rule out
overlap" with their own area (driver-signon, driver-menu-options, driver-menu-annulment, flu-
navigation, flu-promo-numeric, flu-smartcard, flu-ticket-issue, supervisor-menu, technician). What
defects are these, and what area do they actually touch? Resolving this one unblocks confidence
across every other area above, not just one.
A: — source: —

**Q16 · CONFLICT · cases C4100635 vs C4100636 (power-interruption)** — added after the 2026-08-05
correctness-fix pass. C4100635 ("Power interruption — minor versus major outage") models recovery as
temporary-outage-returns-to-original-screen vs longer-outage-triggers-a-safe-shutdown. C4100636 ("Power
loss recovery — within and outside the recovery period") models it completely differently: a
recovery-period threshold, recovery to a specific "10A FLU, same Driver" signed-in state within it, and
recovery to a break state outside it or during break — with no shutdown outcome mentioned at all. Both
cite the same Overflow board, which itself has 0 recorded connections (prose-only annotations), so
neither reading can be confirmed from the transcription alone. Which model is correct — or do both
describe real, distinct behaviours (e.g. a short recovery-period grace window nested inside the
longer temporary/longer split)? C4100635 was left as originally worded pending this answer; C4100636
was not touched at all.
A: — source: —

## Session 2026-08-06 — HHD flow-map coverage + correctness pass (suite 30285)

**Q62 · CONFLICT · HHD C4103934 ("Technician — set the Terminal ID and Transaction Key")** —
Two sources genuinely disagree on the allocation mechanism. FBD-100320 (cited by the case) describes
automatic TID/TK allocation from TMS config by device serial in the "HHD Retailing" terminal group —
no manual entry. The Overflow UX transcription (`knowledge/flows/translink-hhd-supervisor-technician-
technician-setup.md`, transcription confidence: **high**, verbatim) documents a 5-screen **manual**
keypad-entry flow for the identically-named feature (Payment Terminal - Blank → tap Terminal ID field
→ numeric-pad entry → tick → Terminal ID Entered → alphanumeric-keypad Transaction Key entry →
Continue → Details Saved). Is TID/TK actually entered manually on the HHD, allocated automatically by
serial, or is manual entry a fallback/override path alongside automatic allocation? The case has been
marked `**UNCONFIRMED**` pending this answer — do not assert either mechanism until resolved.
A: — source: —

## Session 2026-08-06 — GV flow-map coverage + correctness pass (suite 30286)

**Q63 · CONFLICT/BUG? · GV flow-map path 9 ("invalid AID (Amex etc) → deny list")** — Path 8's
Visa/Mastercard/Maestro AID bucket was corrected this session (Maestro is PV-only per FBD-100690,
confirmed live by case C4104024) — the raw Overflow transcription appears to have conflated GV's and
PV's accepted-scheme lists. Path 9 may be the same conflation: does a non-Visa/Mastercard scheme
(Amex etc.) at the GV specifically get routed through the AID→deny-list chain, or does it get
outright non-acceptance the way Maestro does? No case in suite 30286 tests this either way. Left as
an open GAP on the flow-map (not corrected) pending confirmation.
A: — source: —

## Session 2026-08-06 — PV flow-map coverage + correctness pass (suite 30255)

**Q64 · SURFACE · PV C4102167 ("Technician Menu — reboot")** — The case tests a standalone,
independently-selectable "Reboot" Home-Screen menu action. Neither `translink-pv-technician-menu.md`
nor `pv-flow-annotations.md` documents such an entry point — the only "10.02.03 Rebooting" screen
either source shows is reached via the Location Settings edit chain (change Home Location → confirm
→ reboot), already covered by C4101012. Does the live PV Technician Menu expose an independent manual
Reboot action, or is C4102167 a duplicate of C4101012 framed as a separate feature? Marked
`**UNCONFIRMED**` pending this answer.
A: — source: —

## Session 2026-08-06 — POS missing-path authoring pass (suite 30253)

**Q65 · SURFACE · POS `translink-pos-barcode-scanning.md` path 1, case C4105062** — "Main Screen →
barcode scanned → data **not** retrieved" is a dead-end connection in the source transcription with
no target screen named. The case tests only that the scan is attempted and marks the resulting
screen/outcome `**GAP**` rather than inventing one. What actually happens when barcode data fails to
retrieve at all (distinct from a retrieved-but-invalid barcode)?
A: — source: —

**Q66 · SURFACE · POS `translink-pos-basket-payment.md` path 16, case C4105082** — "Rail: Advance
Ticket Selected → routes into the **Bus** Advance Ticket basket screen (4.1.7)" — a cross-flow edge
present in the raw transcription that the flow-map's own Notes flag as possibly a transcription
artifact rather than confirmed behaviour. Does selecting a Rail Advance Ticket genuinely hand off
into the Bus basket screen, or is this a mis-linked connection in the source export?
A: — source: —

**Q67 · VALUE/HOW · POS `translink-pos-card-payment.md` path 5, case C4105086** — "Chip & PIN card
available? → No (U6) → User Confirming Amount (fallback path)" — the U6 decision node's fallback
confirmation mechanism (PIN re-entry vs. contactless vs. something else) isn't named in the source
transcription. What does the POS actually do when Chip & PIN isn't available at that point?
A: — source: —

**Q68 · SURFACE · POS `translink-pos-numerical-input-bus.md` path 11, case C4105116** — "Basket -
Group Ticket → Advance Ticket Flow (routes to the separate advance-ticket flow, not captured on this
board)" — the onward screen this hands off to isn't named on this board. Confirm the exact advance-
ticket entry screen this reaches (likely on `translink-pos-basket-payment.md`, but not cross-checked).
A: — source: —

**Q69 · SURFACE · POS `translink-pos-numerical-input-bus.md` path 12, case C4105117** — "Numeric
Entry 9002 Change Boarding and Alighting → UNKNOWN decision (unlabeled node in source)" — the raw
Overflow export has a decision node with no label and no confirmed branches. What decision does this
actually represent?
A: — source: —

**Q70 · LIVE? · POS `translink-pos-operator-menu.md` path 7, case C4105122** — "Driver on Break for
the configured amount of time → some further state change (decision node text not captured in
export)" — the flow-map records that *something* happens after a configured break duration elapses,
but not what. Does an extended break auto-sign-off, alert a Supervisor, or do something else?
A: — source: —

**Q71 · SURFACE · POS `translink-pos-topup-validation-topup.md` path 15, case C4105146** —
"Menu-ABT → Adult → ABT Smartcard/Top Up → ABT Basket/Expired → [Bank Card] path" — the outcome of
choosing Bank Card from this basket isn't named in the source (unlike the adjacent [Warrant] branch,
which resolves to Top Up Error on failure). What screen/outcome does the Bank Card path actually lead
to?
A: — source: —

## Session 2026-08-06 (cont.) — HHD missing-path authoring pass (suite 30285)

**Q72 · SURFACE · HHD `translink-hhd-barcode-mlink-multiuse.md` row 12, case (Multi-Use Barcode —
Query mode result shown per product type)** — the source has no incoming edge into the Query-mode
"Product Type?" decision node. How/when does the flow actually enter Query mode versus Validation
mode?
A: — source: —

**Q73 · SURFACE · HHD `translink-hhd-additional-features-updates-and-limits.md` row 6, case (Revenue
Limit — approaching notification shows amount remaining)** — what distinguishes the general "15.1
Limit Approaching" screen from the Rail variant "15.1.1 Limit Approaching - Rail"? Only the screen
IDs differ in the source; no annotation explains the difference.
A: — source: —

**Q74 · SURFACE · HHD `translink-hhd-additional-features-lockout-states.md` rows 2 & 4, cases
(Additional Features — HHD shows Remotely Locked / Remotely Out of Service state)** — both states
have zero screen-to-screen connections and no annotation beyond the screen name. What triggers each
state, and how is each cleared?
A: — source: —

**Q75 · SURFACE · HHD `translink-hhd-barcode-mlink-singleuse.md` row 4, case (Barcode Reference Entry
— selecting Cancel from the entry screen)** — the Cancel-option destination from "24 - Barcode
Reference Entry" is an unlabelled/orphan Overflow node (internal id `e2b1abf5-7303-406f-bca1-
e3312a518647`). Is this a stale/deleted Overflow reference, or does it point to a real screen that
lost its label in the transcription?
A: — source: —

**Q76 · CONFLICT · HHD `translink-hhd-sales-mode-smartcard-rail.md` rows 8 & 11, cases (Smartcard
Rail Sales — invalid card critical error retries to a card presentation screen; read/write fail retry
returns to card validation)** — row 8: the "Critical Error - Invalid Card - Generic Error" screen's
Retry button points to two different targets ("Concessionary Card - Sales mode" vs "Sales mode") with
no captured condition distinguishing which applies when. Row 11: the source connection label "Go to
'Card validation success?' check above" doesn't match any transcribed decision node by that name — the
flow-map's own Notes treat the mapping onto `Valid Smartcard?` as an inference, not a transcribed fact.
A: — source: —

**Q77 · CONFLICT · HHD `translink-hhd-sales-mode-printing.md` row 12, case (Waybill Printing —
continuing without printing exits the print-failure flow)** — the raw diagram shows "Print Failed
(7.2)" with duplicate Retry/Continue-Without-Printing edges pointing to two different destinations
(Login flow vs. back to Sales/Printing Receipt). Are the two PF72 instances (Waybill chain vs.
receipt-printing chain) the same board node or visually distinct nodes sharing a title? Does Waybill
Print Failed's "Continue Without Printing" go to the Login flow or back to Sales?
A: — source: —

**Q78 · SURFACE/CONFLICT · HHD `translink-hhd-operator-menu-annulment.md` rows 2 & 19, cases
(Annulment — exiting Annul Transaction (Glider) returns to Operator Menu; third failed refund print
routes to Contact Ticket Office)** — row 2: the source records this return edge with no bracketed
trigger-action text (unlike nearly every other edge on this board) — the control that fires the return
to Operator Menu - Glider isn't captured (outcome known, mechanism not). Row 19: the flow-map's Notes
flag a source discrepancy — the Contact Ticket Office → Sales timeout is recorded as both 3 seconds
and 5 seconds for what appears to be the same edge. Which is correct?
A: — source: —

## Session 2026-08-06 (cont.) — TVM missing-path authoring pass (suite 30284)

**Q79 · SURFACE · TVM `translink-tvm-collect-tickets-reference.md` rows 5 & 8, cases (Ticket
Collection — Please wait screen returns to the Home Screen; location-restricted reference shows a
location error)** — row 5: the trigger/condition for the Please-wait→Home-Screen transition isn't
named anywhere in the source (only that an unlabelled edge exists). Row 8: "6.0.5. Message (Location
Error)" has no entry or exit connection recorded anywhere in the source board — it exists only as a
standalone annotated screen.
A: — source: —

**Q80 · SURFACE · TVM `translink-tvm-ticket-printing.md` row 6, case (Change Voucher — voucher print
failure shows the error screen)** — does "13.1.10 Change Voucher failed" have a defined onward
connection (e.g. back to 13.2.15/13.1.8), or does recovery require attendant intervention? Not
captured in the source transcription.
A: — source: —

**Q81 · SURFACE · TVM `translink-tvm-choose-ticket-details.md` rows 5 & 7, cases (Ticket Issue —
ticket selection returns to the Home Screen; Smartcards & ABT — yLink ticket selection shows the
yLink select-tickets screen)** — row 5: the 3.0.2→Home edge exists but no bracketed trigger/button is
given. Row 7: the flow-map's own Notes say the connecting arrow into 3.1.0 (yLink) is not documented
and instruct not to assume the exact transition.
A: — source: —

**Q82 · VALUE · TVM `translink-tvm-timeouts.md` rows 3 & 4, cases (Timeouts — cash entered but
payment not completed times out to Home Screen; payment type selected times out to Home Screen)** —
both pairings ("cash entered but not completed" ↔ "Payment Cancelled - Change returned"; "payment
type selected" ↔ "payment cancelled please wait") are inferred from board order only, never stated
verbatim in the source annotation. Also open: per-screen timeout durations are unconfirmed
("configurable per screen", no values captured), and whether every TVM screen has this timeout
behaviour or only these 3.
A: — source: —

**Q83 · SURFACE · TVM `translink-tvm-basket.md` rows 21 & 22, cases (Select tickets with tickets
selected (Basket) — reaches the Basket / reaches Select Payment Type (Basket - 2025))** — both
connections out of "Select tickets – with tickets selected (Basket)" are unlabelled in the source.
Also worth cross-checking: rows 9/10 ("Add More Items" → two different documented destinations) have
concretely-named destinations but no stated rationale for why two edges exist — worth cross-checking
against board 6 "Destination and Boarding Selection" per the flow-map's own TODO.
A: — source: —

**Q84 · SURFACE · TVM `translink-tvm-smartcards.md` rows 12, 14, 17, 18, cases (an ABT deny-list
top-up can print a receipt; an ABT top-up can print a receipt; a card write error can end in Faulty
smartcard No Update / No Update - Cash)** — four unlabelled forks in the source: `ABTSTDDENY` →
`PAYSUM_ABT`/`ABTRCPTDENY`, `ABTSTD` → `PAYSUM_ABT`/`ABTRCPT`, and `FAULTYTRY` →
`FAULTYNOUPD`/`FAULTYNOUPDCASH`, none labelled with what determines the branch taken. Unlike the
iLink top-up screens (5.1.2, explicitly annotated as a receipt-toggle variant), the ABT top-up screens
(5.5.4/5.5.2) have no equivalent toggle annotation.
A: — source: —

**Q85 · SURFACE/CONFLICT · TVM `translink-tvm-multi-modal-home.md` rows 3, 6, 7, 11, 12 — follow-up
to the already-answered Q6** — Q6 (device-capabilities session, answered) established the TVM has no
smartcard reader/writer for *issuing* cards — POS/Card-Bureau only (FBD-100261/100236). This
flow-map's own diagram nonetheless depicts: presenting an ABT/top-up/Discount/Free-Smartpass card
routing to a "Smartcards" screen (rows 3, 6, 7), a "Buy ABT Card" menu option (row 11), and a
Smartcard button/present-card affordance on the Bus home screen (row 12) — all seemingly contradicting
Q6's confirmed hardware answer. Marked `**GAP**` on all 5 rather than asserting behaviour the hardware
can't perform. Is Q6's answer still current, and are these flow-map UI affordances stale/vestigial, or
does the physical TVM actually still show them despite having no reader? (Same underlying question
already flagged as "not yet actioned" in `proposals/tvm-suite-restructure/correctness-audit-2026-08-06.md`.)
A: — source: —

## Session 2026-08-06 (cont.) — GV and PV missing-path authoring pass (suites 30286, 30255) — CLOSES the department-wide missing-path authoring effort

**Q86 · SURFACE · GV `translink-gv-technician-menu.md` rows 6 & 16, cases (Technician Menu — Sign
Off returns to Home Screen; Network Interfaces — FecDetails ChangeIP navigation)** — row 6: which
control on the Sign Off screen routes back to Home Screen vs. the alternate exit to Present
SmartCard/Barcode is unlabelled in the source (same ambiguity already flagged for the sibling row 7,
already covered). Row 16: the diagram has no drawn edge from ChangeIP back to Network Interfaces
(only FecDetails→NetIf is drawn), yet the Paths table implies a return leg — not evidenced in the
source.
A: — source: —

**Q87 · SURFACE/CONFLICT · PV `translink-pv-technician-menu.md` row 6, case (Technician Menu — Sign
Off from Home Screen)** — the flow-map's own Notes flag this exact ambiguity: the raw transcription
shows both a "Sign Off → Home Screen" and "Sign Off → Present SmartCard/Barcode" connection with no
distinguishing trigger label. Is this a genuine two-outcome branch (e.g. cancel vs. confirm), or a
transcription duplicate? (The "→ Present SmartCard/Barcode" outcome is already covered by case
C4102166.)
A: — source: —

_Answered questions get cited back into the affected cases + `knowledge/`. Unanswered → escalated as possible design/spec findings. Add rows as new gaps surface._
