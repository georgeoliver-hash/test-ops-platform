# Findings — NJT Cubic RS485 Network (FR <-> Farebox / Spotter / IVN messaging)

**Inputs.** Existing cases (63 total):
`reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/rs485-farebox-messaging.md`.
Spec: `knowledge/njt/specs/is001-fr-farebox-messaging.md` (`NJT_FRFRP_IS001`).

**Scope note.** This area has no counterpart in the legacy "Fare Register" tree — it only exists
under `TIBU-28853 - NJT ETM / TIBU-29116 - NJT - Cubic RS485 Network`. Five sub-sections
self-flag `(NOT COMPLETE)` / `(Incomplete)` in their own titles: Poll - Increment Funds, Poll -
Bill Rejected, Farebox - Enter Service, Farebox - Exit Service, Poll - Farebox Vaulted. These are
treated as known, self-declared gaps — the question answered below is whether IS001 has enough
detail to close them, not whether they're incomplete (they self-report that).

## Classification against the 18 IS001 message types

### FR → Farebox (12 types)

| # | Message (subtype) | Cases | Status | Notes |
|---|---|---|---|---|
| 1 | Poll (`10 00`) | C4098971–C4098978 | **Covered** | Send, ACK, NAK/timeout retry, plus all 5 piggyback response types (FB Status, Increment Funds, Funds Dumped, Bill Rejected, Farebox Vaulted) each have a receiving case. |
| 2 | FB Information request (`10 10`) | C4098964–C4098966, C4098968–C4098970 | **Partial** | All 3 documented triggers covered (power-on C4098964, post-Program-ID C4098965, cashbox re-insertion C4098966) and the FB IDs response is covered (new FB ID/new cashbox ID/unchanged: C4098968–C4098970). **Missing:** the NAK response path (IS001 p.9 lists "FB IDs or NAK" as the allowed responses) has no case. |
| 3 | FR ID Information (`10 11`) | C4098984, C4098985 | **Covered** | Comms-recovery trigger + valid-data success (FB Status response) and CRC-failure/NAK path both present. |
| 4 | Enter Service (`10 12`) | C4098986–C4098988 (section flagged `(NOT COMPLETE)`) | **Partial** | All 3 documented trigger scenarios covered (sign-on to exact fare, return from break, sign-on to out-of-service farebox). **Missing, groundable from IS001 p.11:** (a) payload composition — driver number/route/trip/bus number all BCD — is never asserted; (b) the two allowed responses (FB Status / NAK) are never exercised; (c) the implicit negative — Enter Service is *not* sent when signing on to a non-Exact-Fare route — is untested. **Not groundable:** the 8-digit wire field vs. 6-digit-supported driver number has no stated failure mode in IS001 (footnote only states the limit, not what happens on overflow) — logged as a gap, not completed. |
| 5 | Exit Service (`10 13`) | C4098989–C4098991 (section flagged `(NOT COMPLETE)`) | **Partial** | All 3 documented triggers covered (sign-off, break, state-mismatch). **Missing, groundable from IS001 p.12:** the two allowed responses (FB Status / NAK) are never exercised. No payload to test (message carries none beyond subtype). |
| 6 | Decrement Funds (`10 20`) | C4098992, C4098993 | **Partial** | Product-sale and driver-dump ($0.00) paths covered. **Missing, groundable from IS001 p.13:** the explicit short-fare "accept" boundary (Amount Accepted < Product Value — spec gives a worked example, $4.00 accepted vs $4.80 product) has no case. |
| 7 | Bill Reclassify (`10 21`) | C4098994 | **Partial** | "Accept next bill" invocation covered. **Missing, groundable from IS001 p.26:** the spec explicitly suggests the Bill Rejected → Bill Reclassify operator-recovery pairing as a linking scenario — not present. |
| 8 | Adjust Backlight/Volume (`10 22`) | C4098995–C4098998 | **Covered** | All 4 target×direction combinations (backlight/volume × increase/decrease) present. |
| 9 | Hold (`10 23`) | C4098999 | **Partial** | Invocation covered. **Missing, groundable from IS001 p.16:** the stated effect (Farebox resets its dump timeout to 60s/configurable) is never asserted as an observable outcome. |
| 10 | Bill Unjam (`10 24`) | C4099000 | **Partial** | Invocation covered. **Missing, explicitly called out in IS001 "Suite implications":** the follow-up poll that confirms the FB Status Jammed bit clears after the unjam completes is not present — only the immediate message send is tested. |
| 11 | Unlock Door (`10 30`) | C4098967 | **Partial** | Invocation with 5-digit code covered. **Missing, explicitly called out in IS001 "Suite implications":** the follow-up poll confirming the FB Status door-unlocked bit (which only flips on a *subsequent* poll, not the immediate response) is not present. |
| 12 | Program Farebox ID (`10 31`) | C4098963 (send), C4098965 (downstream FB-info-request trigger) | **Covered** | |

### Farebox → FR (6 types)

| # | Message (subtype) | Cases | Status | Notes |
|---|---|---|---|---|
| 13 | FB Status (`10 08`) | C4098974, C4098979 | **Partial** | Generic receipt/parse covered. **Missing, explicitly flagged in IS001 "Suite implications" as the richest under-covered area:** no case asserts individual bits from the three status bytes (coin/bill fill level, validator jammed/offline, revenue-mode/maintenance-jumper, cashbox door/removed/top-cover/door-open≥3min) — only the "happy path" all-clear/generic case exists. |
| 14 | FB IDs (`10 18`) | C4098968–C4098970 | **Covered** | |
| 15 | Increment Funds (`10 28`) | C4098975, C4098980 (section flagged `(NOT COMPLETE)`) | **Partial** | Generic receipt (C4098975) and detailed processing — funds counter, vault-cash counter, display update, ACK — (C4098980) covered. **Missing, groundable from IS001 p.24:** the Bill/Coin indicator (0x01 coin / 0x10 bill / 0x11 both) is never distinguished — no case exercises coin-only vs bill-only vs combined increments, and the "delta since last increment, not a running total" semantic is untested. |
| 16 | Funds Dumped (`10 29`) | C4098976, C4098981 | **Partial** | Reset-to-$0, display update, CloudFare dump transaction, and "if IVN detected → IVN detail message" all covered by C4098981. **Missing, groundable by the stated conditional in the same spec line:** the else-branch (IVN not detected → no IVN message sent) is untested. |
| 17 | Bill Rejected (`10 2A`) | C4098977, C4098982 (section flagged `(NOT COMPLETE)`) | **Partial** | ACK + "no further action" covered. **Missing, groundable from IS001 p.26:** the explicit suggested pairing with Bill Reclassify (bill rejected → driver invokes accept-next-bill → Farebox subsequently accepts) is the concrete detail available to close this flagged gap — see item 7 above (one linking case serves both #7 and #17). |
| 18 | Farebox Vaulted (`10 2B`) | C4098978, C4098983 (section flagged `(NOT COMPLETE)`) | **Partial** | Operator-event-to-CloudFare + ACK covered. **Missing, groundable from IS001 p.27–28:** the message's actual payload — cumulative cash counted since last cashbox replacement, broken out per denomination (1¢/5¢/10¢/25¢/$1 coin; $1/$2/$5/$10/$20 bill, all HEX) plus a coin-bypass indicator — is never parsed/asserted; only the generic operator-event outcome is tested. |

## The five self-flagged "(NOT COMPLETE)" sections — groundable or not?

| Section | Groundable completion available in IS001? | Disposition |
|---|---|---|
| Poll - Increment Funds (NOT COMPLETE) | **Yes** — Bill/Coin indicator values (p.24) | Drafted: 3 indicator-variant cases (coin-only, bill-only, both) |
| Poll - Bill Rejected (NOT COMPLETE) | **Yes** — explicit Bill Rejected → Bill Reclassify pairing (p.26) | Drafted: 1 linking scenario |
| Farebox - Enter Service (NOT COMPLETE) | **Partially** — payload/response detail (p.11) groundable; 8-vs-6-digit overflow failure mode is NOT | Drafted: payload-composition, response-handling, negative-trigger cases. Gap logged for driver-number overflow. |
| Farebox - Exit Service (NOT COMPLETE) | **Partially** — response detail (p.12) groundable; no further payload exists to complete beyond that | Drafted: response-handling case |
| Poll - Farebox Vaulted (NOT COMPLETE) | **Yes** — full denomination breakdown payload (p.27–28) | Drafted: 1 denomination-parsing case |

No section in this list is left un-actioned by "IS001 is silent" alone — every one had at least
one groundable completion. The only genuinely un-groundable item nested inside these sections is
the Enter Service driver-number-overflow failure mode, logged to the gap register (not drafted).

## Explicitly NOT drafted (per task instruction — IS001 itself is silent)

- **Poll-timeout/escalation behaviour** beyond re-sending FR ID Information — IS001 defines no
  retry count, backoff, or escalation state for a sustained silent Farebox ("Timing / error
  handling" section of the distilled note). No case drafted; logged as a gap.
- **CRC algorithm/width** — referenced on every message frame but never defined in IS001; presumed
  to live in document [1] (not sighted). No case drafted; logged as a gap.
- **6-digit vs 8-digit driver-number overflow failure mode** — IS001 states the limit but not what
  happens on overflow (truncate/reject/other). No case drafted; logged as a gap.

## Summary counts

- Message types fully Covered: 6 of 18 (Poll, FR ID Information, Adjust Backlight/Volume, FB IDs,
  Program Farebox ID — and Poll counts as one of the 12 FR→Farebox types).
- Message types Partial: 12 of 18 (all listed above with specific missing items).
- Message types Missing outright: 0 — every message type has at least a baseline send/receive case.
- Cases drafted: 13 (see `rs485-farebox-messaging.cases.yaml`).
- Gap-register entries: 3 (see `gap-register-rs485-farebox-messaging.md`).
