# ABT/BOS coherence + grounding audit — first half (suite_ABT.json indices 0–198)

**Summary:** 199 cases in range audited (0 skipped — every id in `annul_section.json` sits in the
back half of the array, indices >198, so none were excluded here). **196 clean, 3 findings: 0 High,
1 Med, 2 Low.** Headline: the first half does **not** exhibit the re-pass defect class the audit was
commissioned to catch. No in-scope case invokes a portal "cancel/annul a tap/journey" action, no
case annuls an old/settled tap, and no case conflates daily-cap £0.00 with cancellation/annulment
£0.00. Indices 0–174 are formulaic Merit/Smartrack/CloudFare report/config/admin cases that are
coherent and grounded to real portal modules. Indices 175–198 (Metro Daily Cap, Zonal Cap) all use
the **legitimate** Operator-Portal alighting-stop correction (CR122 "Update Stop" / FBD-100690), with
£0.00 consistently and correctly attributed to capping ("audited as a £0.00 free tap under the
[zonal/ref] cap, not the reference cap") — these are the *correct* handling of the mechanic, not the
conflation. The three findings below are the only genuine issues.

---

**C4102766** (idx 184, Metro Daily Cap) | Med | grounding / possibly-impossible action |
Title "A declined journey is not treated as a settled capped tap"; precond "the card has one Metro
journey that was **declined** at the reader … shown in Journey History as declined"; step "in the
Operator Portal you **correct the alighting stop on the declined journey**". A tap that was declined
at the reader (DeclinedReason 3/Declined or 2/Deny — FBD-100658) is a *failed* tap with no accepted
boarding→alighting journey to re-stage; the portal's alighting-stop correction (CR122 / Missing-Tap
Correction, FBD-100690) operates on matched journeys in Journey History, and it is unconfirmed that
"Update Stop" is even offered on a declined tap. If it is not, the step tests an impossible action;
if the intent is a white-box guard test (correction code path keys off *settled* status, not
declined), that is salvageable. | **Recommended:** confirm against FBD-100690 / the portal whether an
alighting-stop correction is selectable on a declined journey. If not, reword the WHEN to "attempt to
open Update Stop on the declined journey" and assert the action is unavailable / produces no charge,
rather than implying a successful correction.

**C4102758** (idx 176, Metro Daily Cap) | Low | coherence (precond mislabel) |
Precond: "the card has two Metro-zone taps that **settle under the cap**: … 09:00 charged £2.30, then
… 12:00 charged £1.70, day total £4.00". £2.30 + £1.70 = £4.00, which **is** the cap; the £1.70 is
the *capped* amount (natural £2.30 + £2.30 = £4.60 reduced to the £4.00 cap — cf. the identical
journey in C4102757 which correctly says "£1.70 to complete the cap"). Describing the day as settling
"under the cap" contradicts the mechanic the test relies on — the cap must be *binding* for the
subsequent out-of-zone correction to "remove the cap". | **Recommended:** change "settle under the
cap" to "reach the £4.00 cap (uncapped £4.60, second tap reduced to £1.70)", matching the wording
used in the sibling Metro-cap cases.

**C4102757–C4102780** (idx 175–198, Metro Daily Cap + Zonal Cap) | Low | needs-confirmation (values) |
Every concrete monetary value in these 24 correction cases — Metro cap £4.00 / Metro single £2.30
(ref.20); iLink Zone 1 £6.00, Zone 2 £11.00, Zone 4 £19.00; ref.60 £7.20, ref.61 £8.20; Ulsterbus
singles £4.50 (ref.60) / £2.90 (ref.25) / £5.10 (ref.70) — is **not** verifiable from the committed
FBD specs. FBD-100389 gives only a generic worked example (£5.00 daily cap, £2.00 flat fare);
FBD-100334 (capping) is an unfilled V0.01 stub that explicitly defers mechanics elsewhere; FBD-100690
describes cap *windows/zones/groups* but no pound values. The cases self-source these from the
"UB-TOO tracker" and repeatedly hedge "confirm the exact route/stop in the portal", which is honest
but leaves the fares/caps unconfirmed against a requirement. Same hedge applies to the specific
route→zone corrections (e.g. C4102758 correcting a Metro-zone stop to an "Ulsterbus ref.70 £5.10
stage") — CR122 alighting correction picks another stage on the *boarded route*, so a Metro→Ulsterbus
cross-fare correction is only valid if that route physically spans the zone boundary; the cases flag
this as needing portal confirmation. | **Recommended:** before treating these as pass/fail-ready,
reconcile the cap and reference-fare figures against the authoritative fares source (topology export
/ FBD-100698 / the UB-TOO tracker) and record confirmed values in `knowledge/`; treat the
cross-zone-correction routes as "needs checking" until the route/stop pairs are verified in the
portal. No change to the mechanics — the capping logic and £0.00-under-cap semantics are sound.

---

## Notes on clean cases (not findings)

- Indices 0–174 (Smartrack/Merit Web Reporter/Merit admin + analysis/revenue/daily/concessionary/
  distance reports, CloudFare sign-on/roles/settings/topology/products/rules/labeling/activity-log/
  asset-manager/comms/dataset/staff/quarantine/dashboard/events/ticket-editor/station-manager) are
  coherent (title↔preface↔steps↔expected aligned) and grounded to real portal modules. "Annulled
  Tickets report" (idx 54), "Annulled Tickets" in the Merit report list (idx 14), and "Configure
  annulments per device for a product" (idx 106) are display/report and product-config capabilities
  respectively — consistent with confirmed fact (b), not portal cancel actions.
- Correction cases that operate on **settled** capped taps (idx 178, 181, 185, 197) are correct:
  confirmed fact (a) forbids *annulling* a settled tap, but *correcting* one is a real portal
  capability (FBD-100690: operator corrections available 13 months; settlement adjusted / refunded at
  end of day). These cases test that a correction does **not** recalculate a settled capped tap —
  grounded and coherent.
- Capping arithmetic spot-checked and consistent where values are internally defined, e.g. C4102771
  (uncapped £11.90 → correct £4.50→£2.30 → aggregate £9.70 → refund £11.00−£9.70 = £1.30) and
  C4102769 (Zone 2 £4.50×3 = £13.50 uncapped, held at £11.00 cap).
