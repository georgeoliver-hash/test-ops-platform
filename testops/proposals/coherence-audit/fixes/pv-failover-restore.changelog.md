# PV comms-failover restore — changelog

**Suite:** 30255 (`**NEW** PV-Acceptance Test Suite`, project 42, `TFTS - System Test`).
**Applied via:** `python tools/apply_rewrite.py proposals/coherence-audit/fixes/pv-failover-restore.rewrite.json --commit`
(dry-run verified first, then `--commit` on 2026-07-21).
**Status: PUSHED to TestRail.**

## Why this session exists

Earlier the same day (2026-07-21), an agent condemned **C4101085** ("PV to BOS — communications
resilience and failover") as `ZZ_DELETE_REVIEW`, on George's live-system confirmation that the PV
is "Ethernet-only, no failover" (gap-register **Q9**) — believing sibling **C4103568** ("sustained
network outage drives the PV out of service") already fully modelled the real behaviour.

A later coverage-audit pass the same session, cross-checking JIRA TIBU fixVersions v5.0.0/.1/.3
against the **old PV suite (10047, read-only)**, found the old suite has real, populated cases
under **`REQ-2746.0`** — **C2700890** ("Secondary Communication Failover Method", NIR route) and
**C3275939** (same title, Glider route) — that explicitly test the PV **failing over to cellular**
and continuing to operate normally. This directly contradicted the morning's condemnation and was
logged as gap-register **Q23**, unresolved.

George has now ruled: **"if there is an old test case with it, then yes for now assume it has
failover."** This session reverses the condemnation and reconciles the suite around that ruling.

## What REQ-2746.0 actually says (old suite 10047, the ground truth for the mechanism)

**C2700890** (id 2700890, NIR route) / **C3275939** (id 3275939, Glider route) — both:

- Preface: *"To verify the platform validator continues to operate when the ethernet network fails
  and moves over to cellular."*
- Precondition: *"the ethernet is disconnected from the platform validator and is running on
  cellular"* + a valid smartcard available.
- Steps: present the smartcard → "Validation Success" screen; remove the card → "Home Screen";
  check the transaction is identifiable in CloudFare activity logs, SmarTrack, Merit, and Merit Web
  Reporter.
- Expected: *"the platform validator continues to operate as normal."*

## The TIBU-24428 nuance (raised mid-task, checked before writing anything)

TIBU-24428 ("PrimaryCommsChannelFailed event spamming") was flagged as a **third, possibly
conflicting** signal — its bug description contains the line *"the PV should continue to
communicate over ethernet AND not fail over to cellular"* (also present verbatim in the old
suite's own regression cases for it, **C4069405** / **C4091894**). Read in isolation this looks like
a second confirmation of "no failover."

Reading the **full** Jira ticket (all 17 comments, via `getJiraIssue`) resolves this: that line is
the **initial bug report's own description of the defect** — a *spurious* failover/event-flap
happening on a perfectly healthy Ethernet link (Translink network noise), not a claim that failover
doesn't exist as a mechanism. The fix went through several iterations (a damping fix, then a full
NCS polling rewrite) and the ticket's own **final QA-passed builds prove real, working, bidirectional
failover**:

- Build **1.1.1151.27197** (Thomas James, 2026-01-30, "QA PASSED"): *"PrimaryCommsChannelFailed Event
  812 (Set) raised when disconnecting ethernet from PV. The device then failed over to cellular
  connection... PrimaryCommsChannelFailed Event 812 (Clear) raised after reconnecting the ethernet
  cable back into the PV."* Tested on three devices, all successful.
- Build **1.0.9603.23768** (Thomas James, 2026-04-20, "QA PASSED") — full bidirectional test-coverage
  matrix: Ethernet+cellular connected → disconnect Ethernet → fails over to cellular → reconnect →
  fails back; cellular-only → connect Ethernet → fails over to Ethernet; Ethernet+cellular both down
  → no back-office connection (the only "out of service" scenario in the whole matrix).

So **TIBU-24428, read in full, corroborates REQ-2746.0** rather than contradicting it. There is no
"failover exists generally but not for this condition" nuance to preserve — the earlier "no failover"
reading of TIBU-24428 was a misread of its opening bug description, not its resolution. The only
real residual tension is between REQ-2746.0/TIBU-24428 (PV has cellular failover) and **FBD-100359**,
which classifies "Platform & Gate Validators" under its Ethernet-only device list with no cellular
failover path described — see Gaps below; this is not corrected here (confidential source doc).

## Changes applied

### C4101085 — restored (was `ZZ_DELETE_REVIEW`)

- **Title:** `ZZ_DELETE_REVIEW - PV to BOS — communications resilience and failover` →
  **`Comms Failover — Ethernet loss fails the PV over to cellular`**.
- **Reworded**, not just un-prefixed — the pre-condemnation wording was generic ("uses the secondary
  failover channel"); the restored case is grounded precisely on REQ-2746.0 (continues to operate
  normally on cellular; transaction identifiable in the back office) and TIBU-24428 (the named
  `PrimaryCommsChannelFailed` / event **812** set-clear audit event; the confirmed Ethernet⇌cellular
  bidirectional fail-over/fail-back behaviour), tightened to 3 steps per the Gherkin standard.
- Refs: `REQ-2746.0, TIBU-24428`.

### C4103568 — narrowed (not reversed)

- **Title:** `Comms Lock — a sustained network outage drives the PV out of service` →
  **`Comms Lock — a sustained loss of both Ethernet and cellular drives the PV out of service`**.
- The case's core claim (sustained outage → communication-locked, out-of-service, stops accepting
  taps) is **unchanged and still correct** per FBD-100359 — only the *trigger* is narrowed. As
  written it read as if losing the Translink-network Ethernet path alone (regardless of cellular)
  caused this state; that is now understood to be incomplete, since a single-channel Ethernet
  failure fails over to cellular (per restored C4101085) and keeps the PV in service. TIBU-24428's
  own QA-passed test matrix explicitly separates "Ethernet & Cellular not connected" (no back-office
  connection) from every single-channel-down case (fails over, stays in service) — that distinction
  is what the narrowed precondition now states.
- Refs unchanged: `FBD-100359, TIBU-24428`.

### C4103569 — unchanged

"Comms Recovery — transactions queued during an outage are delivered on restore" needed no edit — it
already describes the total-outage/queued-data recovery case, which is valid regardless of whether
a single-channel failure now fails over first.

## Gap-register

`proposals/coherence-audit/gap-register.md`:

- **Q9** — updated: original "Ethernet-only, no failover" answer marked **REVERSED same day**, with
  a pointer to Q23 for the full resolution.
- **Q23** — marked **ANSWERED**: George's directive recorded verbatim, the TIBU-24428 full-ticket
  re-check documented, and the concrete C4101085/C4103568/C4103569 disposition recorded.
- New residual gap logged (not a blocker): FBD-100359 lists the PV under Ethernet-only devices with
  no cellular failover described — recommended as a candidate FBD-100359 update for the requirements
  owner; not corrected in this session (confidential source document, out of scope for a TestRail fix).

## Audit result

`python -m system_test_ops audit --suite 30255` after the push:

```
audited 135 cases: CLEAN; 24 advisory.
```

CLEAN of blocking findings (0 mojibake, 0 of every blocking rule). The 24 advisory items are the
pre-existing title-style checks (`title-no-emdash`, `title-too-long`) — advisory only, unaffected by
this fix's substance. Report: `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/alignment-audit.md`.

## Files

- `proposals/coherence-audit/fixes/pv-failover-restore.rewrite.json` — the applied rewrite spec.
- `proposals/coherence-audit/gap-register.md` — Q9/Q23 updated.
- `proposals/coherence-audit/fixes/pv.rewrite.json` / `pv.changelog.md` — the earlier same-day
  condemnation this session reverses (for C4101085 only; the C4101005/barcode condemnation in that
  same file is untouched and still stands).
- This file.
