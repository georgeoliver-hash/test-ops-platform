# ETM Smartcards & ABT — product × mode cross-tab (audit-first, before authoring)

337 old smartcard/ABT cases (BV-excluded). Classified by mode from title + section evidence — not
guessed. This is the POS lesson applied: prove shared-vs-mode before authoring.

## Mode split (proven)
- **Metro-specific (125):** Metro Multi-Journey by **zone** (City / Inner / Extended) — Adult/Child ×
  {same/diff direction, within/outside transfer, wrong-zone invalid}; generic Metro MJ; **Metro
  Travelcard**; **Metro ABT zones** (boarding/alighting within Metro ABT zone).
- **Ulsterbus-specific (61):** **Ulsterbus Multi-Journey** (Adult/Child validation + invalid boarding
  stage); **Ulsterbus Town Service Travelcard**; **Capping Groups** (daily/weekly cap reached or not,
  multiple services/modes); **Ulsterbus ABT zones**; ABT reverts to fixed fare on rule change; TOO
  annulment; cross-device validation (ETM/HHD/PV → ETM).
- **Shared / either mode (151):** concessionary passes (60+, Senior, ROI Senior, Blind, War
  Pensioner, DLA / Partially Sighted / Learning Disability / No Driving Licence / PIPS Half-Fare,
  Free Smartpass, Staff / Spouse / Dependants / Retired / External Staff, EA Smartpass Bus & Rail
  Pupil + Further Education); DayLink; Belfast Visitor Pass; iLink Zones 1–4 + NW; aLink; yLink; ABT
  taps (Visa / Mastercard / mobile wallet / passback / declined / BIN-deny / expired / tap error);
  hotlisted; faulty smartcard.

## The duplication (why 337)
Every product is multiplied by: Adult/Child × {validation same/different direction, within/outside
transfer period, passback, invalid (wrong zone / wrong boarding stage / outside time band / expired
/ hotlisted)} × {top-up successful / back / max-50 journeys / expired-journeys-removed / on-expiry /
annulment} × {inter-device top-up on POS-TGX150 / POS-WAY6 / HHD / PV / ETM then validate on ETM}.
The **mechanic is identical across products** — only fare/zone/eligibility differ.

## Proposed consolidation: 337 → ~28 behaviour cases (product + Adult/Child variation lines)

**Functional / Smartcards / Validation** (@mode all unless noted)
1. Smartcard validation and passback — tap-on validates; passback within transfer period (variation: product list, Adult/Child).
2. Validation — same vs different direction, within vs outside transfer period (passback rules).
3. Validation — invalid card: wrong zone *(Metro)*, invalid boarding stage *(Ulsterbus)*, outside time band, expired, hotlisted.
4. Concessionary pass validation — representative list + invalid presented + passback override (Free / Half-Fare / yLink).
5. Faulty smartcard — select card type / charge full fare / issue ticket / faulty Smartpass receipt.

**Functional / Smartcards / Top-Up**
6. Top-up successful — receipt + auto-validate (variation: DayLink=days, iLink/Travelcard=periods, MJ=journeys).
7. Top-up unsuccessful / Back (cancel).
8. Top-up — maximum 50 journeys (MJ).
9. Top-up — expired journeys removed / top-up on expiry.
10. Top-up — annulment.
11. Smartcard mini-statement.
12. Inter-device top-up then validate on ETM (variation: source device POS-TGX150 / POS-WAY6 / HHD / PV / ETM; product).

**Functional / Smartcards / Multi-Journey** (mode-specific zones)
13. Metro Multi-Journey by zone — City / Inner / Extended; wrong-zone rejection *(Metro)*.
14. Ulsterbus Multi-Journey — invalid boarding stage *(Ulsterbus)*.

**Functional / ABT**
15. ABT tap-on-only — successful (success tone, passenger display "Success").
16. ABT tap — declined / error (declined / BIN-deny / expired / tap error → error tone, declined receipt, "See Driver").
17. ABT — passback (second tap).
18. ABT — availability (not enabled on basket / break / smartcard / annul / start-new-journey / travel-mode > 5kph).
19. ABT — Metro zone boarding/alighting *(Metro)*.
20. ABT — Ulsterbus zone boarding/alighting *(Ulsterbus)*.
21. ABT — reverts to standard fixed fare on different service/journey/rule *(Ulsterbus)*.
22. ABT — mobile wallet (Apple / Google / Samsung Pay; phone + watch).
23. ABT — EMV validation failure variants (tap error / expired / declined / already validated).
24. ABT — invalid taps recorded in back office under ABT.

**Functional / Capping** *(Ulsterbus)*
25. Capping group — cap reached (same day / week).
26. Capping group — journeys without reaching cap (same day / week).
27. Capping — multiple services / multiple transport modes / daily capping group.

**Functional / Smartcards / Hotlist**
28. Hotlisted smartcard — presented / marked for hotlist.

Per-product fare/eligibility detail stays covered by the products catalogue + HMI Ticket Layouts. The
old 337 fold in by behaviour; bug refs attach where applicable.
