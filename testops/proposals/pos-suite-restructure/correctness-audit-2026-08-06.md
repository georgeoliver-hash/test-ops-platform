# POS correctness sense-check — confirmed issues + fixes (2026-08-06)

Combined coverage + correctness pass across all 21 POS flow-maps against suite 30253 (702 cases at
baseline). 32 potential correctness issues were flagged; 20 survived independent adversarial
verification. Of those 20, **3 were caught as false positives during fix-authoring** (the verifier
missed a source the finding didn't check) and were NOT applied — see "Caught before fixing" below.
The remaining **17 confirmed issues, spanning 25 cases, are now fixed and live**. Suite re-audited
CLEAN (600 counted cases, 0 blocking).

## Caught before fixing (do not re-flag these)

1. **C4100361 "Audio — tones for success, error and timeout"** — flagged as inventing a 4th "timeout
   tone" not in the Audio Tones flow-map. **False positive**: the case's own `refs` field cites
   `flow-annotations.md §2.0 FLU - Bus (timeout tone)` — a *different* board, which the correctness
   pass never checked. That source states verbatim: "Whenever a screen times out on POS, a time out
   tone will be played." The case is correctly grounded. **Not fixed.**
2. **C4099933 "Sign Off — automatic (inactivity)"** and **C4100436 "Sign Off / Suspend — inactivity
   timers"** — both flagged for naming "Operator Break screen" instead of "Idle screen" as the
   Auto-Sign-Off destination, per `translink-pos-power-interruption-audio.md`'s text. **False
   positive**: `proposals/coherence-audit/gap-register.md` Q18 records George's live-system
   confirmation (2026-07-21) that **"Break mode is used"** for this exact chain — which outranks the
   flow-map's own annotation-reconstructed text (that board is explicitly medium-confidence, 0
   recorded connections). **Not fixed** — flow-map annotated instead (see its Notes/unknowns).

These three are a useful lesson: adversarial re-verification checks whether a claim holds against
*the sources it looked at* — it doesn't guarantee those were the *right* sources. Always cross-check
`gap-register.md` for a prior live-confirmed answer before editing a case that a flow-map contradicts.

## Fixed and live (17 confirmed issues, 25 cases)

| Case(s) | Fix |
|---|---|
| 4099924 | Sign-on Comms-Locked reframed as an idle-state condition (device already can't reach the back office), not a submit-time sign-on failure |
| 4099988 | Cash limit reframed as a post-completion running-total check that locks the POS and requires Supervisor/Technician notification — not a pre-sale block |
| 4099989, 4099991 | Removed invented "Checkout" basket control; renamed to the flow-map's documented "Payment" screen/step throughout |
| 4099979 | Removed the invalid-date error's borrowed 3s-timeout/any-key claim (that behaviour is documented only for card-unavailable/basket-full errors) |
| 4100424 | Split the test-transactions-only "amount too large" condition from the two genuine live decline reasons (PIN lockout, signature mismatch); corrected the exit path to the documented FLU-via-receipt-choice / payment-screen-via-timeout split |
| 4100430 | Split the single generic "error banner" into the two distinct, separately-named documented screens ("Group Ticket Unavailable" vs "No Group Ticket") |
| 4104596–4104603 (8 cases) | Removed the copy-pasted "cross-border variants via L4/R4" step — the raw transcription explicitly states these 8 entitlement types (yLink/24+/Half-Fare ×5/Dependants) are NOT accepted for cross-border travel; only Senior/Blind/War Pensioner get XB |
| 4099940 | "Leave Break" now returns to Main Screen via the documented sign-back-in flow, not directly to the Operator Menu |
| 4099937 | Renamed "Soft Reset" → "Soft Reboot" throughout (title/preface/preconds/steps/expected) — every other reference to this feature (flow-map, sibling case, both screen-validation cases) uses "Soft Reboot" |
| 4099950 | Removed the invented CloudFare-activity-log step for Print & Zero — not documented anywhere, unlike Force Comms which the source explicitly ties to back-office communication |
| 4099956 | Added the documented Idle Screen landing assertion after Technician Soft Reboot (was only asserting generic "valid state") |
| 4099965 | **Condemned** (`ZZ_DELETE_REVIEW`) — an invented near-duplicate of Card Dump under a fabricated "Data Download" screen name; no such action or screen exists in the flow-map or raw transcription |
| 4099966 | Removed the invented "default Boarding Stage" claim — Boarding Stage is a distinct, Technician-only feature (case 4100507), not part of Administrator Device Settings |
| 4100033, 4100499, 4100500 | Passenger display now asserts the documented content (item name, or "Multiple Items" for more than one) instead of an invented "fare and running total" |
| 4100439 | **Condemned** (`ZZ_DELETE_REVIEW`) — conflates the manual Barcode-Reference-entry screen with a scan action, and describes a simplified flow that matches neither entry point's documented decrypt/validate/print pipeline |

## Not yet actioned
- The two condemned cases' real behaviour (Card Dump's actual download-success screen; the full
  barcode validate/print pipeline via both scan and manual-reference entry) should already be
  covered by other live cases per the flow-map's own coverage classification — not independently
  re-verified here, since condemning ≠ creating a gap if the real behaviour has proper coverage
  elsewhere. Worth a quick coverage double-check in a follow-up pass.
- `coverage_by_flowmap` (the missing/partial paths found alongside these correctness issues) is not
  yet written back into the 21 POS flow-maps' `Covered by` columns — that's the next step, same as
  the ETM `/audit-flows` write-back, before authoring any ADD cases for POS's gaps.
