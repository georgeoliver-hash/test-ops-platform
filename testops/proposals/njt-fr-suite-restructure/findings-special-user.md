# Coverage Cross-Check — NJT Fare Register (Special User Functionality)

**Source dump:** `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/special-user.md`
(225 cases across three overlapping trees: legacy "Fare Register / Special User Functionality",
"Fare Register HMI / Administrator Mode (Section 12)" + "Supervisor Menu (Section 11)", and TIBU
"NJT - Administrator Mode" / "NJT - Supervisor Mode").

**Spec:** `knowledge/njt/specs/fs002-special-user-functionality.md` (NJT_FRFRP_FS002 §7).

Method: walked the knowledge note's "Suite implications" checklist item by item, classifying each
against the dump (citing case ids). Overall picture: the three trees together give surprisingly
strong, overlapping coverage of everything FS002 §7 actually specifies — better than any one tree
alone. The genuine gaps are almost all the ones the knowledge note already flagged as unspecified in
the source document (not testable without guessing), plus two concrete Printer-substate assertions
that are grounded but currently under-tested, and one cross-document field-naming mismatch on Serial
Numbers worth a targeted question.

## 1. Sign-on to special user mode (FM-7) — Covered

- Issue key from idle to operator#+PIN to staff-list validation to mode entered per role: C4086772
  (Supervisor), C4086773 (Administrator); entry gating also independently modelled in HMI as
  C4088418 (Administrator) / C4088334 (Supervisor).
- Dual notification (special-user logon to CloudFare, maintenance logon to Clever Device) is
  asserted as both, not just one, in C4086772/C4086773 ("Staff Use History... login recorded in
  CloudFare" + "maintenance log on message... sent to the Clever Device"). Matches the knowledge
  note's explicit callout that a case checking only one side is a partial cover.
- Partial/Missing: no negative-path case anywhere in the dump for invalid operator number / PIN /
  non-special-user role rejection. This is squarely the sign-on GAP already flagged in the knowledge
  note (PIN length/format, lockout, rejection wording not stated at p.82). Not drafting a case;
  logged as Q1 in the gap register.
- TIBU has no independent sign-on case of its own (its Administrator/Supervisor scenarios all start
  from a precondition that entry already happened) — relies on the legacy/HMI trees for this
  checkpoint. Worth folding when the three trees are consolidated, not a coverage gap today.

## 2. Software Versions (7.1.1) — Covered

- Access via Soft Key: C4086775, C4088352, C4099727.
- Pagination (Down/Up, including boundary "cannot scroll further"): C4086776, C4088354, C4099728,
  C4099729.
- Print via Soft Key (including printer-fail path): C4086778, C4088355, C4099730, C4099731.
- Version/config content validation: C4086777 (generic); C4088353 (HMI) itemises OS/Internal, BSP,
  EBoot, Application Software, Configuration Dataset, Printer Firmware. This incidentally already
  answers the FS002 GAP ("which components appear in the list is not itemised in this range") from a
  different source document (the HMI spec, Section 11.1.2). Logged for the gap register (Q2) as
  evidence to bring to the engineer rather than treated as closing the FS002-side gap outright — the
  two documents haven't been confirmed to agree.

## 3. Force Communications (7.1.2) — Covered

- Access + comms-state display: C4086779, C4086780, C4088359, C4088360, C4099734.
- Both side-effects together (outstanding audit upload and software/config check): the knowledge
  note specifically flags a case testing only one as partial. The dump has this both ways: granular
  single-effect cases (C4086781 audit-only, C4086782 software/config-only) and a combined case
  (C4086783) asserting both together, plus TIBU's C4099735 which also combines "check for new
  manifest" with "attempt upload of all unsent data" in one scenario. Fully covered.
- Partial (GAP-blocked): no on-screen feedback/result-state case (success/failure/in-progress) —
  matches the FS002 GAP (p.83); not drafting, logged as Q3.

## 4. Historic Trip Reports (7.1.3) — Covered

- List ordering (most-recent-first): C4086784, C4099800 (TIBU explicitly asserts most-recent is
  displayed first).
- Pagination (both directions + boundary): C4086785, C4099740, C4099741.
- Per-waybill detail view: C4086786, C4099744, plus the deeper Shift Details tree in HMI (C4088398,
  C4088399).
- Print from detail view (including printer-fail path): C4086787, C4099745, C4099746, C4088400.
- Waybill-to-waybill scrolling once viewing a record: C4086788, C4099747, C4099748.
- Partial (GAP-blocked): the fields shown on a waybill detail view are generic ("waybill data is
  correct") rather than itemised, and there is no assertion of how many waybills are retained on
  device — both are the FS002 GAP at p.83 (fields/retention not specified). Not drafting; logged as
  Q4.

## 5. Serial Numbers (7.1.4) — Partial (new finding, not one of the source-flagged GAPs)

- Access: C4086789, C4088366, C4099751.
- FS002 names exactly four fields: device serial number, home location, tray serial number, bus
  number. The legacy/TIBU cases (C4086789/C4086790, C4099751) assert the screen generically ("Serial
  Number data is correct" / "hardware identifiers shall be shown") rather than itemising them — this
  is exactly what the knowledge note's Suite-implications note warns against (a single "screen
  displays correctly" case under-specifies this).
- HMI's C4088367 does itemise fields individually with worked examples — but names five fields (Fare
  Register ID, FareBox ID, TrayID, Home Location, Fleet ID), one of which (FareBox ID) has no
  counterpart named in FS002 §7 at all, and the other three do not obviously map 1:1 onto FS002's
  "device serial number" / "tray serial number" / "bus number" wording. This is a genuine
  cross-document naming mismatch, not a guess I can resolve — logged as a new gap-register entry
  (Q5, not one of the eight the task named up front) asking the engineer to confirm the field mapping
  between FS002 §7 and the HMI spec's Section 11.1.4 before either doc is treated as authoritative.
  No new case drafted for this until the mapping is confirmed.
- Read-only nature of the screen (FS002 GAP, p.83): not tested either way in the dump — consistent
  with the GAP, not drafting; logged as Q6.

## 6. Device Settings (7.1.5) — Covered, thoroughly

- Access: C4086791, C4088340, C4099754.
- Increment/decrement/restore-default across all five spec-named controls (FR backlight, FR volume,
  Farebox backlight, Farebox volume, FR restore-default) — covered at three levels of rigor: simple
  legacy pairs (C4086792 to C4086801), HMI key-mapped variants (C4088405 to C4088415), and TIBU
  boundary cases with explicit min/max and Farebox-connected/disconnected branches (C4099755 to
  C4099772, C4103398 reset).
- Consistent with the FS002 GAP that only Fare Register (not Farebox) has a stated restore-default —
  the suite does not test a Farebox restore-default, correctly not inventing one. No gap-fill found
  here.
- Partial (GAP-blocked): no case asserts a specific numeric range/step size, matching the FS002 GAP
  (p.84, ranges not stated). Not drafting; logged as Q7.

## 7. System Status (7.1.6) — Partial (two grounded, drafted gaps)

- Access + all six components displayed: covered broadly (C4086811, C4088345, C4088346, C4099596).
- Farebox background-colour-by-route-type logic (full-service = grey, Exact = red), the one piece of
  colour semantics FS002 actually specifies, is covered: TIBU's C4099614 (Exact mode, not connected,
  Red) and C4099615 (Full Service mode, not connected, Grey) directly test it.
- GPS Lock/No Lock: C4086812, C4086813, C4099626, C4099627 — covered.
- OBV Connected Ok / Connected Fault / Not Connected (3 spec states): C4086818 to C4086820,
  C4099620 to C4099622 — covered.
- Clever IVN / Spotter Display Connected/Not Connected: C4086824 to C4086826, C4086828,
  C4099616 to C4099619 — covered.
- Printer — grounded gap. FS002 states four distinct Printer states: Ok, and Error with three named
  sub-states (Paper low / Paper Jam / Paper out). Today: Ok is covered (C4086814, C4099623); Paper
  Low is covered distinctly (TIBU's C4099624 asserts "Yellow: Paper Low" specifically). But Paper Jam
  and Paper Out are not asserted distinctly anywhere — the three legacy cases (C4086815, C4086816,
  C4086817) all assert the identical generic "Printer status is Error" regardless of which sub-state
  the case title claims to test, and TIBU's C4099625 ("Printer State Error") is equally generic and
  does not distinguish Jam from Out. This is not a GAP in the source (FS002 states the three
  sub-state names plainly at p.84) — it is a real assertion gap in the test suite. Two new cases
  drafted in `special-user.cases.yaml` to close it (Paper Jam, Paper Out), following the established
  suite convention (seen in C4099624) of naming the specific sub-state in the expected result.
- Partial (GAP-blocked): whether the same colour-coding rule (grey/red by last-signed-on route type)
  applies to any other row besides Farebox is the FS002 GAP at p.84 — not drafting; logged as Q8.

## 8. Enable OBV Maintenance mode (7.1.7) — Partial (GAP-blocked, flagged not drafted)

- Command payload semantics (byte 01, Agent Number = signed-on employee number) and confirmation
  beep: covered — C4086829 validates the $E4 message per section 4.2.4 of the Flowbird/Conduent OBV
  interface spec explicitly; C4099632 also asserts the beep.
- Partial — the async-trigger design is at risk of being tested wrong. FS002 states the OBV
  indicator changes on receipt of an OBV status message with the relevant bit set, i.e.
  asynchronously, driven by the OBV's own reply, not by the button press. C4086829 currently asserts
  the indicator change in the same When/Then block as pressing the Soft Key, which reads as an
  instant, button-driven update — exactly the anti-pattern the knowledge note's Suite-implications
  section warns against (a case asserting instant UI update would be testing the wrong thing). This
  sits directly on top of the source-flagged GAP (exact OBV indicator appearance before/after the
  status bit is set, p.84 to 85) which the task brief named explicitly as excluded from drafting, so
  no corrective case is drafted here; the observation is logged against the existing gap-register
  entry (Q9) instead of invented.

## 9. Exit Supervisor mode (7.1.8) — Covered (via legacy tree)

- Sentinel End Run transaction count = 9999: explicitly asserted in C4086830 / C4086831 (legacy).
  TIBU's equivalents (C4099634 to C4099637) assert the "End Run" message is sent but do not re-assert
  the 9999 sentinel value — a tree-level gap, not a suite-level one (legacy already proves it). Worth
  folding into one canonical case when the three trees are consolidated; not drafted as a new case
  here since the checkpoint already has coverage.
- Conditional OBV exit-maintenance command (byte 00, Agent Number 000000), sent only if maintenance
  mode was enabled during the session, both paths covered: C4086831 (was enabled) and C4086830 (was
  not enabled, via omission) at the legacy level; TIBU's C4099634 (was enabled) / C4099635 (was not
  enabled) make both paths explicit.
- Partial (GAP-blocked): behaviour if maintenance was enabled AND separately disabled again within
  the same session before exit (idempotency of the exit-maintenance command) is the FS002 GAP at
  p.85 — not drafting; logged as Q10.

## 10. Administrator Mode entry (7.2) — Missing (GAP-blocked)

- No case anywhere distinguishes which staff-list role(s) grant Administrator vs Supervisor access,
  or confirms whether Administrator mode uses the same Issue-key/operator#+PIN flow. This is the
  FS002 GAP at p.85 named explicitly in the task brief. Not drafting; logged as Q11.

## 11. Unlock Farebox (7.2.1, EFADLS-3) — Covered

- CloudFare event fires on selection: C4087051, C4088425, C4099053.
- Farebox-not-detected path (no unlock message, no event): C4099054, good additional coverage
  beyond the FS002 baseline text, not contradicting it.
- Partial (GAP-blocked): no on-screen confirmation/feedback case (success/failure of the unlock
  command itself vs. only the event being raised) — FS002 GAP at p.85. Not drafting; logged as Q12.

## 12. Program Farebox Number (7.2.2) — Covered for happy path; one flagged possible spec bug

- Happy path (valid ID leads to Program Farebox ID message, then Request Farebox details, then
  display returned number): C4087052 (legacy, all three steps explicit), C4088435 (HMI, saves plus
  sends update command plus returns to menu, does not explicitly re-display the returned number, but
  legacy already covers that step), C4099048 (TIBU).
- Invalid-entry handling exists in all three trees but with inconsistent behaviour asserted: legacy's
  C4087053 says the FR simply returns to the Administrator menu; HMI's C4088439 (empty entry
  specifically) says it plays error.wav and does not save or transition; TIBU's C4099049 says it
  shows an explicit error message and stays on the Program Farebox Number screen. These three do not
  describe the same behaviour. This ties directly into the flagged digit-count ambiguity below and
  is not being resolved here by picking a most-likely version — logged as Q14 rather than drafted.
- POSSIBLE DESIGN/SPEC BUG, flagged per CLAUDE.md's Q&A-loop rule. FS002 states the on-screen prompt
  says a "6-digit number" but the stated validation rule is "1 to 6 numeric digits", a wording
  inconsistency in the source itself (p.85). TIBU's C4099048 has silently picked a side: it tests
  entering a valid numeric ID between 1 and 6 digits as the happy path, i.e. the suite already
  asserts the 1-to-6-digit interpretation is correct without engineer confirmation. That is a real
  risk: if the live system actually enforces exactly 6 digits (the prompt text), C4099048 is testing
  incorrect expected behaviour, and would pass a test against a wrong assumption. No case is drafted
  here to fix this, since doing so would require guessing which rule is right. This is logged as Q13
  in the gap register, explicitly marked POSSIBLE DESIGN/SPEC BUG, per the hard rule that a gap
  nobody can answer is itself a finding.

## Summary

| Menu item | Classification | New cases drafted |
|---|---|---|
| Sign-on to special user mode | Covered / Partial (negative path GAP-blocked) | 0 |
| Software Versions | Covered | 0 |
| Force Communications | Covered / Partial (feedback GAP-blocked) | 0 |
| Historic Trip Reports | Covered / Partial (fields GAP-blocked) | 0 |
| Serial Numbers | Partial (new field-mapping finding) | 0 |
| Device Settings | Covered / Partial (ranges GAP-blocked) | 0 |
| System Status | Partial (Printer sub-states, grounded) | 2 |
| Enable OBV Maintenance mode | Partial (indicator timing GAP-blocked) | 0 |
| Exit Supervisor mode | Covered (via legacy tree) | 0 |
| Administrator Mode entry | Missing (role-taxonomy GAP-blocked) | 0 |
| Unlock Farebox | Covered / Partial (feedback GAP-blocked) | 0 |
| Program Farebox Number | Covered (happy path) / possible spec bug | 0 |

2 new cases drafted (`special-user.cases.yaml`), both under System Status — Printer, closing a
genuinely under-specified assertion (not a source GAP). 14 gap-register questions logged
(`gap-register-special-user.md`): the 8 named in the task brief, 5 further GAPs the knowledge note
flags that were not in that list (Historic Trip Reports fields/retention, Serial Numbers read-only
confirmation, Exit Supervisor idempotency, Unlock Farebox on-screen feedback, Program Farebox Number
invalid-entry behaviour), plus 1 new self-discovered finding (Serial Numbers field-naming mismatch
across FS002 vs the HMI spec). The digit-count inconsistency (Q13) is explicitly flagged POSSIBLE
DESIGN/SPEC BUG because the suite already tests one unconfirmed interpretation of it.
