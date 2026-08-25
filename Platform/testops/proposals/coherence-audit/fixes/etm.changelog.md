# ETM changelog — coherence-audit fixes (2026-07-21)

**Suite:** 30254 (`**NEW** ETM-Acceptance Suite`, project 42 `tfts-system-test`)
**Status:** PUSHED to TestRail (`tools/apply_rewrite.py proposals/coherence-audit/fixes/etm.rewrite.json --commit`).
**Source:** `proposals/coherence-audit/fixes/etm.rewrite.json`
**Grounding:** George (live-system confirmation), 2026-07-21 — answers gap-register.md Q7 and Q19.
**Audit:** `python -m system_test_ops audit --suite 30254` → **CLEAN** (0 blocking; 74 pre-existing advisory
title findings unrelated to this change). Report: `reports/tfts-system-test/new-etm-acceptance-suite/2026-07-21/alignment-audit.md`.

## Summary

3 cases updated (2 reworded, 1 condemned). 2 cases spot-checked, no change needed (already clean).

## Reworded

### C4100586 — "ABT — Metro zone boarding and alighting"
Previously stamped `**UNCONFIRMED** (audit 2026-07-17, gap Q7)` — assumed a customer alighting tap
("alighting-only tap", "boarding-and-alighting tap") on a tap-on-only ETM. George confirms there is
**no customer tap-off** on Metro/Ulsterbus TOO ETMs; alighting is always ETM-calculated or
driver-selected. Reworded to a single customer boarding tap with the alighting stop **ETM-calculated**
as the last stop on the route within the configured Metro Network Zone.
- Cites: FBD-100658 (Alighting-location calculation — Metro ETM), FBD-100662 (migration plan — Metro
  routes = "Tap On Only (Flat Fare)"), George (live-system confirmation) 2026-07-21, gap-register.md Q7
  (now ANSWERED).

### C4100587 — "ABT — Ulsterbus zone boarding and alighting"
Same premise error as C4100586, on the Ulsterbus (driver-initiated) TOO variant. Reworded to a single
customer boarding tap, the customer stating their alighting stage, and the **Driver selecting** that
alighting stage on the FLU screen — no customer alighting tap.
- Cites: FBD-100662 (UX flow — driver-initiated FLU screen; "alighting location = the driver-selected
  stage (not ETM-calculated)"), FBD-100658 (Alighting-location calculation — Ulsterbus ETM), George
  (live-system confirmation) 2026-07-21, gap-register.md Q7 (now ANSWERED).

## Condemned

### C4100588 — "ABT — reverts to standard fixed fare on rule change" → `ZZ_DELETE_REVIEW`
Previously stamped `**UNCONFIRMED** (audit 2026-07-17, gap Q19)` — asserted a Ulsterbus ABT journey
"reverts to the standard fixed fare" on a service/journey/rule trigger. George confirms flat-fare
behaviour is **Metro-only now** (FBD-100662); Ulsterbus routes use the driver-selected-alighting TOO
business rules instead, so there is no UB "fixed fare" left to revert to. No FBD describes an
equivalent UB behaviour for this trigger, so a replacement could not be grounded without inventing
functionality — condemned (title prefixed `ZZ_DELETE_REVIEW`, not hard-deleted) rather than guessed.
- Cites: FBD-100662 (Scope — flat fare superseded for Ulsterbus routes), George (live-system
  confirmation) 2026-07-21, gap-register.md Q19 (now ANSWERED).

## Spot-checked, no change

### C4100946 — "Regression — passenger display GDPR compliance"
George confirms the ETM does have a customer-facing passenger display peripheral — the case's premise
was already correct and carried no doubt/gap marker. Left untouched.

### C4102566 — "Fare-Paying Smartcard — validation"
### C4102567 — "Fare-Paying Smartcard — top-up"
George confirms fare-paying/stored-value smartcard is a real product. Both cases already read clean
with no UNCONFIRMED/GAP marker questioning the product's existence. Left untouched.
