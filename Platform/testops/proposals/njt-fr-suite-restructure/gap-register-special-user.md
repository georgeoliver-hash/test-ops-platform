# Gap Register & Q&A — NJT Fare Register (Special User Functionality)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · GAP · Sign-on negative path — PIN format, lockout, rejection wording** — OPEN

FS002 §7 (sign-on to special user mode, p.82) states operator#+PIN is validated against the latest
staff list, but does not state PIN length/format, lockout-on-repeated-failure behaviour, or the
on-screen wording for a rejected operator number/PIN. No case in the dump exercises this negative
path (`reports/.../special-user.md`).

Question for the engineer: what is the PIN format, is there a lockout after N failed attempts, and
what does the rejection screen say? Needed before any negative-path sign-on case can be drafted.

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q2 · GAP · Software Versions component list not itemised in FS002** — OPEN

FS002 §7.1.1 (p.82) doesn't itemise which components/subsystems appear in the version list. Separately,
the HMI spec (Section 11.1.2, case C4088367/C4088353) lists OS (Internal), BSP, EBoot, Application
Software Version, Configuration Dataset Version, Printer Firmware.

Question for the engineer: is the HMI spec's component list authoritative for FS002 §7.1.1 too, or are
they two different lists (e.g. one is a superset)? If confirmed, this closes the FS002-side gap.

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`; case C4088353.

---

**Q3 · GAP · Force Communications — no on-screen feedback/result states described** — OPEN

FS002 §7.1.2 (p.83) doesn't describe success/failure/in-progress feedback for a forced comms call.

Question for the engineer: does the Force Comms screen show any result state (spinner, success tick,
failure banner) during/after a forced call, or does the operator only infer success from the updated
timestamps/counts (as HMI's C4088360/C4088361 test)?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q4 · GAP · Historic Trip Reports — waybill detail fields and retention count not specified** — OPEN

FS002 §7.1.3 (p.83) doesn't itemise which fields appear on a waybill's detail view, nor how many
waybills are retained on device. Current cases (C4086786, C4099744) assert the detail view generically
("waybill data is correct / matches trip details") rather than field-by-field.

Question for the engineer: what fields must the waybill detail view show, and what's the on-device
retention limit (if any)?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q5 · FINDING · Serial Numbers — field naming mismatch between FS002 and the HMI spec** — OPEN

FS002 §7.1.4 (p.83) names exactly four fields: device serial number, home location, tray serial
number, bus number. The HMI spec's Section 11.1.4 (case C4088367) itemises five, worded differently:
Fare Register ID, FareBox ID, TrayID, Home Location, Fleet ID. "FareBox ID" has no counterpart in
FS002's list at all, and the mapping of "device serial number" → "Fare Register ID" / "bus number" →
"Fleet ID" is not confirmed anywhere in either doc as read.

Question for the engineer: do FS002 §7.1.4 and HMI §11.1.4 describe the same screen? If so, please
confirm the field-name mapping (or that one document supersedes the other) so a single itemised case
can be grounded correctly instead of guessed.

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`; case C4088367.

---

**Q6 · GAP · Serial Numbers screen read-only confirmation** — OPEN

FS002 §7.1.4 (p.83) describes the Serial Numbers screen as view-only (no edit action described), but
this isn't explicitly confirmed as a hard rule in the source range.

Question for the engineer: can you confirm the Serial Numbers screen has no supervisor edit
capability (i.e. Program Farebox Number, 7.2.2, is the only path that can change any of these values,
and only from Administrator mode)?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q7 · GAP · Device Settings — numeric range/step size, and Farebox restore-default** — OPEN

FS002 §7.1.5 (p.84) doesn't state the numeric range or step size for backlight/volume adjustments, and
only mentions a restore-default for Fare Register brightness/volume — not for the Farebox settings.

Question for the engineer: (a) what are the min/max/step values for each of the five Device Settings
controls? (b) is there intentionally no Farebox restore-default, or is that also a spec omission?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q8 · GAP · System Status — colour-coding scope beyond the Farebox row** — OPEN

FS002 §7.1.6 footnote 1 (p.84) only specifies background-colour semantics (grey/red by last-signed-on
route type) for the Farebox row. It's not stated whether an equivalent colour-coding rule applies to
any of the other five rows (GPS, Printer, OBV, Clever IVN, Spotter Display).

Question for the engineer: do any other System Status rows carry route-type-driven colour coding, or
is the Farebox row unique in this respect? (Note: the HMI spec separately defines a generic
Green/Yellow/Red severity colour scheme for all rows — Section 11.1.1, case C4088347 — which appears
unrelated to this specific route-type rule; please confirm these are two independent colour schemes,
not conflicting ones.)

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`; case C4088347.

---

**Q9 · GAP · Enable OBV Maintenance mode — indicator appearance and async-trigger test risk** — OPEN

FS002 §7.1.7 (p.84–85) states the OBV indicator changes **on receipt of an OBV status message with
the relevant bit set** — i.e. asynchronously, not on the button press itself — but doesn't describe
the indicator's exact appearance (icon/colour/text) before vs after.

Separate from the appearance question: case **C4086829** currently asserts the indicator change in
the same When/Then step as pressing the Soft Key, which reads as an instant, button-driven update.
That's a test-design risk regardless of the appearance answer — if the real device only updates the
indicator once the OBV's status reply arrives, C4086829 could pass without the async path ever being
exercised (e.g. if the OBV happens to be slow to reply in a test run).

Question for the engineer: (a) what does the indicator look like before/after the status bit is set?
(b) can we get confirmation that the existing case's instant-update assertion doesn't mask a timing
defect, or should it be restructured to explicitly wait for the OBV status reply before checking the
indicator?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`; case C4086829.

---

**Q10 · GAP · Exit Supervisor mode — idempotency of the exit-maintenance command** — OPEN

FS002 §7.1.8 (p.85) doesn't state what happens if OBV maintenance mode was enabled and then
separately disabled again within the same supervisor session, before Exit Supervisor mode is
selected — specifically, does Exit still (harmlessly) resend the byte-00/Agent-Number-000000 exit
command regardless of current OBV state, or does it skip it because maintenance is already off?

Question for the engineer: please confirm the expected behaviour for this within-session
enable-then-disable-then-exit sequence.

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q11 · GAP · Administrator Mode — staff-list role taxonomy** — OPEN

FS002 §7.2 (p.85) states Administrator mode is "only available to a very restricted group of users"
but doesn't name the staff-list role(s) that grant it, nor confirm whether entry uses the same
Issue-key/operator#+PIN flow as Supervisor mode or a separate path. No case in the dump distinguishes
the two entry paths by role.

Question for the engineer: which staff-list role name(s) map to Administrator access (vs Supervisor),
and is entry via the same flow as Supervisor sign-on?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q12 · GAP · Unlock Farebox — no on-screen confirmation described** — OPEN

FS002 §7.2.1 (p.85) states selecting Unlock Farebox sends a CloudFare event, but doesn't describe any
on-screen confirmation/feedback of the unlock command itself succeeding or failing.

Question for the engineer: does the screen show anything (success/failure banner) when the Farebox
unlock command completes, or does the operator only see confirmation via the CloudFare events portal
(as TIBU's C4099053/C4099054 currently test)?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`.

---

**Q13 · POSSIBLE DESIGN/SPEC BUG · Program Farebox Number — "6 digit" prompt vs "1–6 digit" validation rule, and a case already assumes an answer** — OPEN

FS002 §7.2.2 (p.85) has an internal wording inconsistency: the on-screen prompt text says the new
Farebox ID is a "6-digit number," but the stated validation rule allows "1–6 numeric digits." These
cannot both be exactly true — either the prompt wording is loose (and 1-6 digits really is accepted,
e.g. "42"), or the validation description is wrong and exactly 6 digits is enforced.

**This is not just an open question — it's already a live risk in the suite.** TIBU's **C4099048**
("Successfully program a new Farebox ID") already tests the happy path as "enters a valid numeric ID
between 1 and 6 digits," i.e. the suite has silently adopted the 1–6-digit interpretation as ground
truth, without engineer confirmation. If the live system actually enforces exactly 6 digits, this case
is asserting incorrect expected behaviour and would give a false-positive pass. Separately, the three
trees also disagree on **invalid-entry behaviour**: legacy's C4087053 says the FR "returns to the
Administrator menu"; HMI's C4088439 (empty-entry case) says it plays error.wav and does not
save/transition; TIBU's C4099049 says it shows an explicit error message and stays on the Program
Farebox Number screen — three different described behaviours for what should be one rule.

Per CLAUDE.md's rule that a gap nobody can answer is itself a finding: if the engineer cannot resolve
which digit-count rule is authoritative, this should be raised as a **possible design/spec bug** in
JIRA against FS002 §7.2.2, not silently left as-is with C4099048 continuing to test an unconfirmed
assumption.

Question for the engineer: which is correct — exactly 6 digits, or 1–6 digits? And what is the actual
on-screen behaviour (message text, whether the field allows retry) for an invalid entry?

A:

source: `knowledge/njt/specs/fs002-special-user-functionality.md`; cases C4099048, C4087053,
C4088439, C4099049.

---

**Q14 · FINDING · Program Farebox Number invalid-entry behaviour disagrees across the three trees** — OPEN

See Q13 — the three described invalid-entry behaviours (return to menu / error.wav no transition /
explicit error message + stay on screen) are mutually inconsistent, independent of the digit-count
question. Even once Q13 is resolved, the actual on-screen behaviour for a rejected entry still needs
confirming and reconciling across C4087053, C4088439, and C4099049 before any one of them can be
treated as canonical (or before a single consolidated case can be drafted).

A:

source: `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/special-user.md`
cases C4087053, C4088439, C4099049.

---
