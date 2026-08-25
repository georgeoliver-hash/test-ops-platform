# Gap Register & Q&A — NJT Fare Register (CloudFare Communication)

Source: `knowledge/njt/specs/fs002-cloudfare-communication.md` (`NJT_FRFRP_FS002` §8/8.1) and the
cross-exam in `findings-cloudfare-comms.md`. Per `CLAUDE.md`'s hard rule, none of these are guessed
at — each is a question for the engineer; answers get cited back into the spec note and, where
relevant, into the affected cases.

## Q1 — Guaranteed-delivery retry/backoff/timeout semantics

**Question:** §8 states comms incorporate a "guaranteed delivery mechanism so data is not lost"
(p.86), but this excerpt does not detail the retry count, backoff strategy, or timeout behaviour of
that mechanism. What are the actual retry/backoff/timeout parameters (or where else in the spec are
they defined)?

**Why it matters:** several existing cases (C4105031, C4099035) already assert generic
"data sent after comms re-established" behaviour, which is fine at that level of generality — but no
case may assert specific retry counts, backoff timing, or a timeout value until this is answered.

**Status:** Open. (`NJT_FRFRP_FS002 p.86`)

## Q2 — 10-second transaction-delivery: fallback behaviour if the window is missed

**Question:** §8 states the FR sends the transaction record to the back office "within 10 seconds"
of completion, but notes this SLA depends on comms infrastructure outside Arrive's control (p.86).
What does the device do if the 10-second delivery fails or is delayed — is the record queued locally
for retry, and if so for how long / with what limit?

**Why it matters:** existing cases (C4087060, C4099036) only assert the happy-path 10s delivery.
No case has been drafted for the failure path in this pass because the behaviour is unconfirmed.

**Status:** Open. (`NJT_FRFRP_FS002 p.86`)

## Q3 — Reboot: mid-transaction safeguard and post-reboot resume state

**Question:** §8.1 states a CloudFare Reboot command "directs the device to execute a reboot cycle"
(p.88) but gives no detail on (a) whether a reboot is deferred/queued if the device is mid-transaction
the way Out of Service and Lock commands are, and (b) what state the device resumes to after
rebooting.

**Why it matters — raised with urgency:** the existing case **C4087088** ("Remote Commands - Reboot")
currently asserts "the FR powers on in the same state it was in before the reboot" — this is
specific behaviour that is **not stated** in the cited spec section. Per the hard rule against
inventing device behaviour, this assertion is currently **UNCONFIRMED**. Do not treat C4087088's
current wording as ground truth until this is answered; if confirmed correct, cite the confirming
source into the case; if incorrect, the case needs correcting and this may be a
**POSSIBLE DESIGN/SPEC BUG** if the intended resume behaviour differs from what is implemented.

**Status:** Open — highest priority of this batch (existing, executed test case may assert unconfirmed
behaviour). (`NJT_FRFRP_FS002 p.88`)

## Q4 — Block state: on-screen/operator-visible behaviour

**Question:** §8.1 states devices in the Block state "will not receive an acknowledgement" to their
back-office communication requests (p.88), but does not describe what, if anything, is visibly shown
to the operator on-screen when a device is blocked (versus simply not receiving an ack silently).
What is the actual on-screen behaviour?

**Why it matters:** existing cases (C4087093, C4087097) correctly assert the no-ack and auto-sign-off
behaviour, but no case may assert a specific on-screen message/state until this is confirmed.

**Status:** Open. (`NJT_FRFRP_FS002 p.88`)

## Q5 — "CloudFare Quarantine data" terminology (C4105030)

**Question:** the orphaned case C4105030 ("Device Communication - Quarantined Data") references a
"CloudFare Quarantine data" view where rejected data can be inspected. This term does not appear
anywhere in the distilled FS002 §8 excerpt, which instead describes an invalid dataset producing "an
event to CloudFare" (p.86). Is "quarantine" a real, named CloudFare feature documented elsewhere in
FS002 (outside the excerpted range), or is this case asserting a concept that doesn't exist?

**Why it matters:** if quarantine is a real, separate feature it should be traced to its own spec
citation; if not, C4105030 may be asserting invented functionality and should be corrected or
condemned.

**Status:** Open. (excerpt range: `NJT_FRFRP_FS002` lines 15082–end)

## Q6 — "Registration token" terminology (C4105032)

**Question:** the orphaned case C4105032 ("Device Communication - Device Registration") asserts the
FR "receives a registration token from CloudFare" on successful registration. This term is not present
in the distilled FS002 §8 excerpt. Is device registration (and a token mechanism specifically)
documented in another part of FS002, and if so, can it be cited?

**Why it matters:** same reasoning as Q5 — an uncited mechanism in an existing case is a standing gap
until traced to a source.

**Status:** Open. (excerpt range: `NJT_FRFRP_FS002` lines 15082–end)

## Q7 — TIBU "Remote Device Management" tree mislabeling (C4099043/C4099044)

**Question:** C4099043 is titled "Remotely Lock a Device" but its body describes a Reboot command;
C4099044 is titled "Remotely Trigger a Reboot" but its body describes a Force Comms command
(duplicating C4099045's Force Comms body). This looks like a shifted copy-paste error when the TIBU
tree was authored, rather than a spec ambiguity. Can the engineer confirm this is a data-entry error
(so the titles/bodies can be corrected or the cases condemned as redundant with the main "Fare
Register / CloudFare Communication / Remote Commands" tree, which already covers Lock and Reboot
correctly), rather than something intentional?

**Why it matters:** as currently written, the TIBU tree has no genuine Lock or Reboot test despite
appearing to, and has Force Comms duplicated. Left uncorrected this could mislead a coverage read
that only skims TIBU titles.

**Status:** Open — data-quality/process question, not a spec gap. (see `findings-cloudfare-comms.md`
§3)
