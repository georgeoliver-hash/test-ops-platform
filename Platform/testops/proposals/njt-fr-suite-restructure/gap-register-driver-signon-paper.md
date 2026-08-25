# Gap Register & Q&A — NJT Fare Register (Driver Sign-on / Display / Paper)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · GAP · Sign-on PIN retry/lockout limit is unspecified** — OPEN
`knowledge/njt/specs/fs002-driver-signon-display-paper.md` §5.1 (p.27): on an incorrect Driver
Number/PIN match, the FR tells the driver the details are incorrect and they must re-enter — but the
section states no limit on re-entry attempts (no lockout/retry count). Existing cases (C4087252,
C4098848, C4098847) test the "invalid → re-enter" path but none assert a retry-limit/lockout, since
none is confirmed to exist.

Question for the engineer: is there a configured maximum PIN retry count before lockout (matching the
"Communications Lock" idle-screen state described in HMI01 §6), or does the FR allow unlimited
re-entry attempts? If a limit exists, what is it (or is it configurable), and what happens on the
final failed attempt?

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`.

---

**Q2 · GAP · Accept's "certain circumstances" precondition is unenumerated** — OPEN
`knowledge/njt/specs/fs002-driver-signon-display-paper.md` §5.3.3.1 (p.31): Accept "allows the driver
to issue a product even with insufficient Farebox funds, in certain (unspecified-here) circumstances."
Beyond the one stated precondition (at least $0.01 registered), the spec does not enumerate what
governs whether Accept is permitted or blocked. Existing cases (C4104911, C4104912, C4099417–C4099419,
C4099438–C4099440, C4099458–C4099460) test the $0.01 boundary and the successful/blocked outcomes but
do not (and cannot, without this answer) test any other precondition.

Question for the engineer: what are the "certain circumstances" under which Accept is permitted vs.
blocked, beyond the $0.01-registered boundary already tested? Is it unconditional above that boundary,
or are there additional route/config/transaction-type restrictions?

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`.

---

**Q3 · GAP · CLEAR's boarding-zone-not-reset behaviour is ambiguous (with a conflicting case found)** — OPEN
`knowledge/njt/specs/fs002-driver-signon-display-paper.md` §5.3.1 (p.30): CLEAR resets "alighting
zone, class, and transaction type" back to sign-on values; boarding zone is not listed as reset — the
knowledge note flags this as a possible deliberate design choice or a spec omission.

Existing case C4087276 ("Change Product Parameters - Clear Key") matches the spec wording exactly
(alight zone/class/transaction only). However, C4099401 ("Operator resets the modified parameters",
TIBU-29480) describes CLEAR resetting "the product parameters" broadly, without excluding boarding
zone — a wording mismatch between the legacy case and the JIRA-organised TIBU case that itself may be
evidence either way.

Question for the engineer: does CLEAR reset the boarding zone or not? If C4099401's broader wording is
correct, C4087276 needs editing to match; if C4087276/the FS002 text is correct, C4099401's wording
should be tightened so it doesn't imply boarding zone is included.

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`.

---

**Q4 · POSSIBLE SPEC BUG · Class/Transaction "last default" wording looks like a copy-paste error** — OPEN
`knowledge/njt/specs/fs002-driver-signon-display-paper.md` §5.1 (p.27–28): the spec's sentence
describing the Transaction field's initial value literally repeats the Class field's wording verbatim
("The initial class displayed is the last class that was set as the default") rather than describing
a "last transaction type" default. This reads as a copy-paste artifact rather than a confirmed
statement that Transaction Type has no independent default-memory.

Question for the engineer: does the Transaction field retain its own sticky "last used" default on
sign-on (mirroring Class), or does it always reset to a fixed default (e.g. the route's default
transaction type / "Cash")? If nobody can confirm which is intended, this is itself a finding — flag
as **POSSIBLE DESIGN/SPEC BUG** and raise a JIRA ticket against NJT_FRFRP_FS002.

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`.

---

**Q5 · CONFLICT · Existing case hard-codes the Class field's default to "Adult", contradicting FS002's sticky-default rule** — OPEN
Existing case C4087315 ("Verify Initialization Summary Layout (Section 7.3)", HMI01 §7.3) asserts:
"the 'Class' field must default to 'Adult' and 'Transaction' to 'Cash'" on the Enter Run screen.
FS002 §5.1 (p.27) states the Class field's initial value is "the last class that was set as the
default" — i.e. sticky from the previous sign-on, not a fixed value.

These two statements are only reconcilable if "Adult" happens to always be the previous sign-on's
class (e.g. on a device's very first-ever sign-on, or if the fleet always signs off leaving Class at
Adult) — otherwise C4087315 looks like it asserts the wrong (hard-coded) behaviour.

Question for the engineer: is the Class field's default genuinely sticky (per FS002), and if so is
"Adult" simply what HMI01's screenshot/mock-up happened to show at the time it was authored (not a
hard rule), or does the live system actually reset Class to "Adult" every sign-on (contradicting
FS002)? Whichever is correct, one of the two documents (or C4087315) needs a correction.

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`, `knowledge/njt/specs/hmi01-fare-register-hmi.md`.

---

**Q6 · GAP · Mode-gating unavailability tests for Hold/Dump/Cancel Ticket/Accept Next Bill/Clear Bill Jam are out of this note's scope** — OPEN
`knowledge/njt/specs/fs002-driver-signon-display-paper.md`'s scope note (pp.26–27) names these as
mode-exclusive functions in the availability table but explicitly states their own behaviour is
specified later in the document (out of this note's line range) — "do not treat as covered by this
note." One mode-exclusive function, `Sum`, IS confirmed unavailable-in-Exact-Fare by existing cases
(C4099420, C4099441, C4099461); the rest have no unavailability test anywhere found in this area.

Question for the engineer: is coverage for Hold/Dump/Cancel Ticket/Accept Next Bill/Clear Bill Jam's
mode-gating already held elsewhere (e.g. a Driver Menu / Operator Menu area not reviewed in this
pass), or does it need drafting once the FS002 §5.4-onward note is distilled? No case has been drafted
here — this is a scope/sequencing question, not a behaviour unknown.

A:

source: `knowledge/njt/specs/fs002-driver-signon-display-paper.md`.

---

**Q7 · POSSIBLE SPEC BUG · HMI01 §7.8 Enter Class Screen's ISSUE-row validation text is a verbatim copy of the Alighting Zone bullet** — OPEN
`knowledge/njt/specs/hmi01-fare-register-hmi.md` (already flags this as a cross-cutting gap): the
`ISSUE` row for the Enter Class Screen literally repeats "If Zone ID is not on selected Line..."
rather than describing any class-specific validation logic. Existing coverage (C4087342–C4087346)
correctly has no "invalid class" case, consistent with Class being a scroll-only selection with no
typed-entry invalid state — but this means the copy-paste line in the spec has never been resolved
with the engineer.

Question for the engineer: was this line meant to describe real Class-entry validation (and if so,
what is it), or is it confirmed dead/erroneous spec text that should simply be struck? Surfacing here
because it directly affects this area's Enter Class Screen coverage decision.

A:

source: `knowledge/njt/specs/hmi01-fare-register-hmi.md`.

---
