# Gap Register & Q&A — NJT Fare Register (Operator Menu)

Source: cross-examination of `knowledge/njt/specs/fs002-operator-menu.md` (NJT_FRFRP_FS002 §5.4)
against the existing TestRail cases in the orphaned top-level sections, the legacy Fare Register tree,
the TIBU-29384 JIRA tree, and the Fare Register HMI / Driver menu (Section 9) tree. Each item below is
a question for the engineer — do not fabricate an answer; cite it back into the case once resolved.

## Q1 — Cancel Ticket: is it available at all in Exact Fare mode?

FS002 §5.4.1 states Cancel Ticket is "only available in Full Service mode" but never explicitly states
whether it's hidden, disabled, or produces an error in Exact Fare mode. The HMI/TIBU trees already
implement a no-op/error-beep behaviour in Exact mode (`C4088292`, `C4099072`) — **is this the intended
behaviour, or should Cancel Ticket simply not appear in the menu at all in Exact Fare mode?**
(NJT_FRFRP_FS002 p.34)

## Q2 — Pay Leave: exact meaning of the zone-range wording

FS002 §5.4.3 says the Pay Leave ticket-issue screen shows zones "set from the default boarding zone to
the current boarding zone". **Does this denote a zone range (e.g. Zone 1 through Zone 14) or a specific
boarding/alighting zone pair?** This affects how the fare-due calculation and the screen's zone display
should be asserted. (NJT_FRFRP_FS002 p.34–35)

## Q3 — Passenger Count: standalone menu entry or folded into Driver Totals only?

FS002 §5.4.4 says only "the passenger count is now included on the driver totals screen" with no
further detail. The HMI Driver Menu screen list (§9.1–9.12) has no separate Passenger Count screen
either. **Is Passenger Count ever a standalone Operator Menu entry/screen on the live device, or is
5.4.4 purely a note that it now surfaces inside Driver Totals?** No case should assert a standalone
screen until this is confirmed. (NJT_FRFRP_FS002 p.35)

## Q4 — Relief: is there a cancel path, and does it match what HMI/TIBU already test?

FS002 §5.4.8 describes only the confirm/ISSUE path for Relief with no stated cancel option — but the
existing HMI (`C4088236`) and TIBU (`C4099338`) trees **already implement and test** a 'C'/Cancel path
at the Relief confirmation screen that returns to the Driver Menu without performing the relief.
**Can the engineer confirm this Cancel behaviour is correct and intentional (i.e. the spec is simply
silent, not describing a Relief that cannot be aborted)?** (NJT_FRFRP_FS002 p.37)

## Q5 — Device Settings: does the Farebox have its own "restore default" control?

FS002 §5.4.9 lists a "restore default" option only for FR brightness/volume, not for Farebox
brightness/volume, and no case in any tree tests a Farebox restore-default. **Is this omission
intentional (Farebox has no restore-default control), or is one missing from the spec/menu?**
(NJT_FRFRP_FS002 p.37)

## Q6 — Driver Break: who may invoke Force Sign Off, and what is audited?

FS002 §5.4.11 mentions an option to "force a sign-off for the original driver" if they fail to return,
but states neither **who may invoke it** (supervisor/audit-role only, or any driver with device
access?) nor **what audit trail it produces**. All three trees (orphan `C4105450`, HMI
`C4088246`/`C4088255-259`, TIBU `C4099368`/`C4099374-376`) implement Force Sign Off with **no PIN or
role check depicted** — implying any driver present can invoke it — and TIBU's audit event on force
sign-off is logged as an **"End of Run" record** (`C4099374`), not a distinct "Force Sign Off" event.
**Please confirm: (a) is Force Sign Off unrestricted by design, and (b) is reusing the End of Run
CloudFare record correct, or should a distinct audit event exist?** (NJT_FRFRP_FS002 p.38)

## Q7 — Supervisor/Audit Reports: is a failed ID entry logged anywhere?

FS002 §5.4.12 states an invalid supervisor/audit ID produces "an error" with no detail on whether the
failed attempt is logged to CloudFare. None of the existing cases (`C4105451`, `C4088317`/`C4088324`,
`C4099383`/`C4099388`) assert a CloudFare event for this path. **Should a failed ID-entry attempt be
audited, and if so what event?** (NJT_FRFRP_FS002 p.38)

## Q8 — Clear Bill Jam: is a CloudFare audit event expected?

FS002 §5.4.14 sends the 'clear bill jam' command to the Farebox but states no corresponding CloudFare
event — unlike Accept Next Bill (§5.4.13), which explicitly does send an Event. No case in any tree
asserts a CloudFare event for Clear Bill Jam. **Is the absence of an event intentional, or should Clear
Bill Jam also raise a CloudFare Event like Accept Next Bill does?** (NJT_FRFRP_FS002 p.39)

## Q9 — Driver Break: "if connected" (spec) vs "if in Exact Fare mode" (TIBU tests) — same condition?

FS002 §5.4.11 gates the Farebox out-of-service/back-in-service messages on the Farebox being
**"connected"**. The TIBU tree's equivalent cases (`C4099366`, `C4099369`) instead gate the Farebox
command on the Fare Register being **"in Exact Fare mode"**. Since the Farebox is presumably only ever
relevant/connected on Exact Fare routes, these may be equivalent in practice — but **can the engineer
confirm whether "connected" and "in Exact Fare mode" are interchangeable here, or whether a
Full-Service-but-somehow-connected-Farebox edge case exists that the current tests would miss?**
(NJT_FRFRP_FS002 p.38; cf. `C4099366`)

## Q10 — Hold: should it appear in the Operator Menu's Exact-Fare-only restriction list?

The orphaned top-level case `C4105439` ("Exact Fare Features - Option Restrictions in Non-Exact Fare
Mode") asserts that Dump, Accept Next Bill, and Clear Bill Jam are hidden/disabled outside Exact Fare
mode, but **does not include Hold** — even though FS002 §5.4.2 states Hold is Exact-Fare-service-only
in the same way as those three. **Is this an intentional omission from that case, or should Hold be
added to the restriction-list assertion?** (NJT_FRFRP_FS002 p.34, p.36–39; cf. `C4105439`)
