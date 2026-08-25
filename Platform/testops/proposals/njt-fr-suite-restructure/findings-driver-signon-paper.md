# Findings — NJT Fare Register (Driver Sign-on / Default Display / Paper Ticket Transactions)

Cross-examined ~258 existing cases (legacy "Fare Register / Driver Functionality / Sign on, Default
Display, Paper Ticket Transactions"; HMI "Sign On Process (Section 7)" + "Ticket Issue
Screen"/"Transaction Rejected"; TIBU-28899 Sign On tree; TIBU-29471 Product Issue tree) against
`knowledge/njt/specs/fs002-driver-signon-display-paper.md` (FS002 §5.1–5.3, pp.26–33) and the
relevant HMI01 screens.

## Overall

Coverage is **strong**. Every named HMI Sign-On-Process screen (7.1–7.10) and every Ticket-Issue-
Screen/Transaction-Rejected screen has a case. All sign-on fields (Run/Line/Trip/Board Zone/Alight
Zone/Class/Transaction) are validated including numeric boundaries (1/4-digit Run, 1/3-digit Trip).
All six named Special Transaction Sequences, the Wheelchair counter, and the Non Payment counter are
fully covered including their negative exclusions.

## Missing — 5 items (cases drafted, see `driver-signon-paper.cases.yaml`)

1. Board Zone conditional-on-Line validity — no case proves a zone valid on one Line is rejected on
   another.
2. Same gap for Alight Zone.
3. 60s auto-dump — only "dump occurs" is tested; no negative case for attempting to finalise *after*
   the dump has occurred.
4. Accept — underpayment record on the receipt: only "receipt printed" is asserted, not its content.
5. Accept — dual Clever Device message: existing cases assert only one message; spec requires two.

## Gated on named spec gaps (no case drafted, per instruction)

PIN retry/lockout limit; Accept's "certain circumstances" precondition; CLEAR's boarding-zone-not-
reset ambiguity; the Class/Transaction "last default" wording (possible spec copy-paste). See
`gap-register-driver-signon-paper.md`.

## New findings routed to the gap register (Q5–Q7)

- **C4087315** hard-codes Class's default to "Adult," contradicting FS002's sticky-default rule — a
  real conflict, not just an unconfirmed value.
- **C4087276** (legacy) vs **C4099401** (TIBU) disagree on whether CLEAR resets boarding zone —
  supporting evidence for the CLEAR gap.
- Mode-gating unavailability tests for Hold/Dump/Cancel Ticket/Accept Next Bill/Clear Bill Jam are out
  of this note's scope (FS002 defers their behaviour elsewhere); only Sum's unavailability-in-Exact-
  Fare is actually proven.

No writes were made to TestRail; no "To Delete" cases were touched.
