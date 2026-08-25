# ABT annul/correction — rebuild plan (after grounding)

**Status:** 32 of the 35-case Tap-Correction/Annulment section **condemned** (ZZ_DELETE_REVIEW) on 2026-07-17 — built on the false "cancel/annul in the Operator Portal" premise. 3 left intact: C4102808 (prev-day annul), C4102864 (aftercare query), C4103488 (late-upload annul).

**Do NOT rebuild until:** (a) full requirement docs are grounding the work, and (b) gap-register Q1–Q4 are answered (portal fare-recalc / alighting-stop change real? any "cancel journey" action? back-office void of settled journey?).

## Real behaviours to rebuild clean (grounded), once confirmed
Ground each in the cited spec + George's confirmed device-annul facts (device-only, ~1 min, most-recent tap, same boarding). Annulment display: FBD-100358 (summary £0.00, expanded original fare retained, negative annul row). Capping: FBD-100662/100389.

1. **Device annul of a fresh tap** → tap £0.00, marked Annulled; shows in Journey History + Annulled/Cancelled report. (FBD-100358, FBD-100662 annul rule.)
2. **Annul-then-immediate-retap** → re-tap is the first good tap; capping counts from it. Cover Metro (£4.00/£2.30) and Ulsterbus reference bands (ref.60/ref.61) — **VALUE gap Q14** (confirm fares/source first).
3. **Annul, no re-tap** → no chargeable journey that day.
4. **Annul most-recent only / within window** — negative: cannot annul after a later tap or after the window (the exact class the old cases got wrong).
5. **Annulled tap excluded from capping** / does not corrupt an already-capped day total.
6. **Late-uploaded annul** settles correctly (keep C4103488).
7. **CR122 alighting-stop change** (if Q1/Q2 confirm it's live) → recalc fare + cap re-run + auto refund/charge; operator unlimited/sees fare, passenger 1-month·3-year/no fare. Otherwise mark `**UNCONFIRMED**` and do not build. (FBD-100662.)

Target: ~6–10 clean, coherent, cited cases replacing 32 confused ones. Everything not confirmable → `**UNCONFIRMED**` or escalated as a design/spec finding, never invented.
