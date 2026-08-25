# Gap Register & Q&A — NJT Fare Register (Other Functions / Warnings & Errors)

**Purpose.** Every gap the knowledge note flags is a **question**, not a silent marker. Answer each and
the affected case-draft gets grounded + cited. A gap nobody can answer is flagged **POSSIBLE DESIGN/SPEC
BUG** and raised in JIRA. See `CLAUDE.md`'s "gaps trigger a Q&A loop" rule and
`.claude/commands/resolve-gaps.md`.

Legend: **SURFACE** (does this device do this action?) · **LIVE?** (specified but is it actually built?) ·
**VALUE** (exact figure/threshold) · **CONFLICT** (two sources disagree) · **SCOPE** (does this add
anything beyond what's covered?).

Source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` (NJT_FRFRP_FS002 §5.5–5.6).

---

**Q1 · VALUE · Spotter Display class-code table (§5.5.1)** — OPEN
The spec confirms the 12-character Spotter Display string format and gives `SEN` as one example class
code, but the full 3-character class-code table is not in the distilled range. Needed before asserting
exact string content for any class other than `SEN` in a case.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.1 (p.39).

---

**Q2 · SURFACE · Sum Function — 11th-entry behaviour (§5.5.2)** — OPEN
Spec states a maximum of 10 transactions per Sum function use but does not state what happens if the
driver attempts an 11th sum entry (reject / error message / silently capped). Existing case `C4104972`
("Sum Function - Maximum of 10 Transactions") already asserts a specific outcome (warning beep + warning
message) for pressing S past the cap — worth confirming this existing assertion is actually correct/
grounded, since the knowledge note treats this as unresolved.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.2 (p.40); existing case
`C4104972` (pre-supposes an answer — please confirm or correct).

---

**Q3 · SURFACE · Paper Loading — failed test-print recovery (§5.5.3)** — OPEN
Spec describes the happy-path sequence (lid open → roll swap → lid close → FR prompts test print → return
to prior state) but not what happens if the test print itself fails (still jams/mis-feeds). Existing
cases `C4104978`, `C4099494`, `C4099500` do assert an "unsuccessful print → error message" outcome —
worth confirming these already answer this gap, or whether they describe a different failure mode.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.3 (p.40); existing cases
`C4104978`, `C4099494`, `C4099500`.

---

**Q4 · SURFACE/VALUE · Bus Inspection — receipt content + non-numeric input (§5.5.4)** — OPEN
Two related unknowns: (a) the printed inspection receipt's exact content/format is not stated; (b) the
spec only states the ">6 digits" invalid case (error beep, prompt remains) — behaviour for a non-numeric
or empty submission is not distinguished. Needed before asserting exact receipt text or non-numeric-entry
handling in a case.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.4 (p.40–41).

---

**Q5 · VALUE · Colour of the Day — colour/day mapping table (§5.5.5)** — OPEN
Spec confirms a 3-character Colour-of-the-Day code is shown and is calendar-driven, but the actual
colour/day mapping table and code values are not in this range. Needed to assert a specific display
string on a given day.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.5 (p.41).

---

**Q6 · SURFACE · GPS — no-fix/unavailable handling (§5.5.8)** — OPEN
Spec confirms lat/long is recorded in transaction and event records but does not state behaviour when GPS
has no fix (blank field? last-known value? error flag?). **Additional finding:** existing case `C4104995`
("GPS - No GPS Data") has steps identical to `C4104994` (the normal-GPS case) — it does not actually
simulate a no-fix condition, so it isn't real coverage of this gap today. Once answered, `C4104995` will
need rewriting, not just a title change.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.8 (p.41); existing case
`C4104995` (currently a duplicate of `C4104994`, not real no-fix coverage).

---

**Q7 · VALUE/CONFLICT · AutoLog off — warning wording + post-timeout state (§5.5.9)** — OPEN
Spec states the 120-minute timeout, the 10-second warn+audio window, and the cancel path, but not the
exact warning-screen wording nor what happens if the driver does *not* cancel. **Lead:** `C4088333`
(Fare Register HMI §10.1) and `C4099514` (TIBU-30140) already assert concrete post-timeout behaviour
(display returns to Idle screen; FR prints an End of Run report; End of Run record to CloudFare; IVN
message if connected) — please confirm whether HMI §10.1 / TIBU-30140 is the authoritative source for
this FS002 §5.5.9 detail, so it can be cited back into a grounded case rather than left as a gap.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.9 (p.41); existing cases
`C4088333`, `C4099514` (candidate answers, need confirmation of authority).

---

**Q8 · VALUE · Paper Low — default threshold value (§5.6.3)** — OPEN
Spec confirms Paper Low fires at a "configurable threshold" of tickets remaining but does not state the
default/typical value.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.6.3 (p.42).

---

**Q9 · SURFACE · Paper Out — "special users" role definition (§5.6.4)** — OPEN
Spec states that with no paper loaded and the FR idle, only "special users" can log in (regular driver
login blocked). "Special users" is not defined as a role/permission level in this range. Needed before
writing an assertion naming the specific role(s) that qualify.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.6.4 (p.42).

---

**Q10 · CONFLICT/VALUE · Farebox Failure — 6-vs-10-consecutive-NAK relationship + mode-changed message
wording (§5.6.6.1)** — OPEN
Spec sends a CloudFare event at 6 consecutive NAKs and separately triggers standby mode at 10 consecutive
NAKs, but does not disambiguate whether the 6-NAK event is a distinct earlier warning or part of the same
count toward 10. Exact wording of the driver-facing "mode changed" message is also not stated.
**Additional finding (supporting evidence, not a fix):** existing case `C4099505` is titled "Scenario:
10 consecutive NAKs received" but its own step reads "**And** 6 consecutive NAKs have been received from
the Farebox -> Then the Fare Register must display the Standby screen" — i.e. the case's title and body
disagree on which count triggers Standby. This looks like exactly the ambiguity this gap is asking about;
flagging as an existing-case defect requiring the same answer.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.6.6.1 (p.43); existing case
`C4099505` (title/body mismatch, 6 vs 10).

---

**Q11 · SURFACE · Farebox Fault — recovery path back to Exact mode (§5.6.6.3)** — OPEN
Spec states Farebox Fault causes Full Service fallback with a CloudFare event + IVN fault message, but
(unlike Communication Restore's explicit auto-retry poll) states no recovery path back to Exact mode.
Is fault-recovery automatic, does it require a farebox reset event, or does it require manual/driver
action?
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.6.6.3 (p.43–44).

---

**Q12 · SCOPE · Fare Mode — attribute configuration/display detail (§5.5.7)** — OPEN
Spec confirms fare mode (Exact/Full Service) is set by a route attribute but gives no detail on how/where
the attribute is configured, or on operator-visible indication of the current mode outside of the
farebox-failure fallback messaging covered under §5.6.6. Needed if a case is to assert general mode-
display behaviour beyond the failure-triggered case.
A:
source: `knowledge/njt/specs/fs002-other-functions-warnings-errors.md` §5.5.7 (p.41).

---

## POSSIBLE DESIGN/SPEC BUG candidates (flag if unanswered after Q&A)
None yet — all 12 items above are genuine unknowns awaiting an engineer answer, not yet escalated. Q10's
existing-case title/body mismatch (`C4099505`) is the strongest candidate to become one if the 6-vs-10-NAK
relationship turns out to be genuinely undefined in the spec rather than just undistilled.
