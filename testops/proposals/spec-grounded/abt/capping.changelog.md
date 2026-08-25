# ABT/BOS Capping — spec-grounding changelog

Re-grounding of the capping test cases against the requirement specs. **Proposal only — not pushed to TestRail.**
Governing specs: FBD-100334 (Revenue Reallocation w/ ABT Capping — V0.01 stub), FBD-100662 (Ulsterbus TOO),
FBD-100340 (Ulsterbus Town Services), FBD-100389 (ABT Scenarios), FBD-100698 (Topology/Fares usage),
FBD-100229 (Zone Configuration), FBD-100658 (ABT Audit).

## Cross-cutting corrections
- **Every 'correction' case (Metro/Zonal/Reference/Uncapped/Town) depends on the portal alighting-stop
  adjustment (CR122)**, which FBD-100662 (paras 271, 691, 693) records as a *proposal with UX still to be
  determined*. All such cases are now marked **UNCONFIRMED** — the mechanism is specified but not verified live.
- **All specific fare/cap values** (Metro £4.00/£2.30, iLink £6/£11/£19, ref.60 £7.20 / ref.61 £8.20, Bangor
  £2.50) come from the **UB-TOO tracker, not any FBD** — marked **UNCONFIRMED** (gap Q14). FBD-100389 uses a
  £5.00 daily-cap example; FBD-100662 uses a £4.00/£3.10 worked example; FBD-100340 uses a £1.00 town cap.
- **Surface**: capping is a back-office (CloudFare ABT) computation shown in **Journey History**; device steps
  only 'accept and record' the tap. Prefaces reworded from white-box wording ('the fix', 'the correction guard').
- 'auto-settlement' renamed to 'auto-charge' to match FBD-100662 para 691 ('charge them extra').

## Per-case changes

### Metro Daily Cap

**4102757** — action: `reword`
- old title: Same-fare correction holds the Metro cap
- new title: Metro cap — same-fare alighting correction holds the cap
- change: Tightened title; preface made behavioural; dropped the 'Passenger Portal to verify' clause; marked the Metro cap/single values UNCONFIRMED (tracker, not FBD) and added the CR122 UNCONFIRMED marker as the correction mechanism is an unverified proposal. Renamed 'auto-settlement' to 'auto-charge' (spec wording, FBD-100662 para 691).
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100389 para 219-221, FBD-100662 para 264, FBD-100662 para 233
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102758** — action: `reword`
- old title: Correction outside the Metro zone removes the cap and charges the difference
- new title: Metro cap — correction outside the Metro zone removes the cap and charges the difference
- change: Tightened title; removed the invented '£5.10 ref.70' out-of-zone value (not confirmed for this route) and replaced with a GAP to confirm the stop/fare; marked cap values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264, FBD-100229 para 149 (cap applies only within the configured zone)
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- gap: No confirmed out-of-Metro-zone stop/fare for a 10A/10b tap in the tracker — needs checking on the live portal.

**4102759** — action: `reword`
- old title: Correction into the Metro zone applies the cap and refunds the difference
- new title: Metro cap — correction into the Metro zone applies the cap and refunds the difference
- change: Tightened title; marked cap values UNCONFIRMED; added CR122 marker; generalised 'Ulsterbus tap' to 'out-of-zone tap' since the meaningful condition is zone membership.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102760** — action: `reword`
- old title: Correcting a settled free (capped) tap keeps it at £0.00
- new title: Metro cap — correcting a settled free (capped) tap keeps it at £0.00
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100389 para 219-221, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- gap: That a settled capped tap is NOT recalculated on correction is an implementation guard not stated in any FBD (FBD-100334 V0.01 is an unfilled stub) — confirm expected behaviour.

**4102761** — action: `reword`
- old title: Correcting a settled partially-capped tap keeps it at £1.70
- new title: Metro cap — correcting a settled partially-capped tap keeps it at £1.70
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100389 para 219-221, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- gap: Preservation of a settled reduced fare on correction is an implementation guard not in any FBD — confirm.

**4102762** — action: `reword`
- old title: A correction never pushes the day total over the Metro cap
- new title: Metro cap — a correction never pushes the day over the cap
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102763** — action: `reword`
- old title: A corrected capped tap stays settled and free
- new title: Metro cap — a corrected capped tap stays settled and free
- change: Tightened title; collapsed a duplicate THEN ('cap retained on that tap' + 'charged £0.00') into one; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102764** — action: `reword`
- old title: Correcting the first full-fare tap leaves its charge unchanged
- new title: Metro cap — correcting the first full-fare tap leaves its charge unchanged
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102765** — action: `reword`
- old title: Correcting an unsettled capped tap re-evaluates and stays free
- new title: Metro cap — correcting an unsettled capped tap re-evaluates and stays free
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 694, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102766** — action: `reword`
- old title: A declined journey is not treated as a settled capped tap
- new title: Metro cap — a declined journey is not treated as a settled capped tap
- change: Removed white-box preface language ('the correction guard keys off settled status'); made behavioural; grounded 'declined' to Declined Reason 2; marked CR122.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100658 (DeclinedReason enum; 2 = On Deny List), FBD-100662 para 243, FBD-100662 para 264
- gap: Whether a declined (no-fare) journey is even correctable via CR122 is not specified — the case tests an internal guard not described in any FBD; confirm expected behaviour.
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.

**4102767** — action: `reword`
- old title: Re-running settlement after a correction does not re-charge the capped tap
- new title: Metro cap — re-running settlement after a correction does not re-charge the capped tap
- change: Tightened title; marked values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 137, FBD-100662 para 264
- gap: Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- gap: Settlement idempotency (re-running settlement raises no new charge) is not stated in any FBD — confirm expected behaviour.

### Zonal Cap

**4102768** — action: `reword`
- old title: Higher-fare correction within the zone holds the cap
- new title: Zonal cap — higher-fare correction within the zone holds the cap
- change: Tightened title; marked iLink cap value UNCONFIRMED (tracker); added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100340 para 278, FBD-100662 para 264

**4102769** — action: `reword`
- old title: Higher-fare correction outside the zone removes the cap and charges the difference
- new title: Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference
- change: Tightened title; removed the invented '£5.90 Zone 3' fare (not confirmed); marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 322 (board/alight not both in zone → not capped), FBD-100662 para 264
- gap: No confirmed Zone 3 fare for the corrected 10b tap in the tracker — confirm the stop/fare on the live portal.

**4102770** — action: `reword`
- old title: Lower-fare correction within the zone keeps the day above cap and holds
- new title: Zonal cap — lower-fare correction within the zone, day still above cap, holds
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 264

**4102771** — action: `reword`
- old title: Lower-fare correction drops the day below cap and refunds
- new title: Zonal cap — lower-fare correction drops the day below cap and refunds
- change: Tightened title; marked cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 264

**4102772** — action: `reword`
- old title: Zone 4 correction within the highest band holds the cap
- new title: Zonal cap — Zone 4 correction within the highest band holds the cap
- change: Tightened title; marked cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13 (Zone 4 is the outermost iLink band), FBD-100340 para 149, FBD-100662 para 264

**4102773** — action: `reword`
- old title: Correction into a capped zone audits a free tap under the zonal cap
- new title: Zonal cap — correction into a capped zone audits a free tap under the zonal cap
- change: Tightened title; removed the tracker aside about 10b Metro codes from the step; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 337 (reference-fare capping group), FBD-100662 para 264
- gap: Zonal-cap-takes-precedence-over-reference-cap ordering is implied by the capping-group model but not stated explicitly — confirm precedence rule.

**4102774** — action: `reword`
- old title: A correction into a capped zone does not increase the account total
- new title: Zonal cap — a correction into a capped zone does not increase the account total
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 264

**4102775** — action: `reword`
- old title: The cap shown after a correction is the zonal cap, not a reference cap
- new title: Zonal cap — a corrected tap reports under the zonal cap, not a reference cap
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker. Near-duplicate of 4102773/4102774 — flagged for possible consolidation.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100662 para 337, FBD-100662 para 339 (Saving Type shows the capping rule/group), FBD-100662 para 264
- gap: 4102773/4102774/4102775 are three near-identical 'zonal cap beats reference cap' assertions on the same setup — candidate for consolidation into one case with a data-variations note.

**4102776** — action: `reword`
- old title: Correcting into a zone below cap charges toward the zonal cap
- new title: Zonal cap — correcting into a zone below cap charges toward the zonal cap
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 337, FBD-100662 para 264

**4102777** — action: `reword`
- old title: A journey with no zonal cap still uses the reference cap correctly
- new title: Reference cap — a journey with no zonal cap still uses the reference cap
- change: Tightened title; removed 'after the fix' white-box phrasing; marked ref cap value UNCONFIRMED; added CR122 marker. (Section was 'Zonal Cap' but the case is a reference-cap case — noted for re-section.)
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337 (same reference fare → same capping group), FBD-100662 para 265 (Ulsterbus daily cap on reference fares), FBD-100662 para 264
- gap: Case sits in the 'Zonal Cap' section but tests the reference cap — consider moving to 'Reference Fare Cap'.

**4102778** — action: `reword`
- old title: Correcting to another stop in the same zone keeps the zonal cap
- new title: Zonal cap — correcting to another stop in the same zone keeps the cap
- change: Tightened title; removed the tracker aside about 10b Zone 1 stops carrying Metro codes; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 264
- gap: The tracker flags that some 10b Zone 1 stops also carry Metro codes and would cap at Metro £4.00 — the Zone 1 route/stop pair must be confirmed so the case exercises the Zone 1 (not Metro) cap.

**4102779** — action: `reword`
- old title: Re-running settlement after a zonal correction adds no charge
- new title: Zonal cap — re-running settlement after a correction adds no charge
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 para 12-13, FBD-100340 para 149, FBD-100662 para 264
- gap: Settlement idempotency is not stated in any FBD — confirm expected behaviour.

**4102780** — action: `reword`
- old title: The zonal cap applies after a correction regardless of transport mode
- new title: Zonal cap — the cap applies after a correction regardless of transport mode
- change: Tightened title; marked cap value UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100229 (rail vs bus capping is by transport-mode setting, not zone), FBD-100340 para 149, FBD-100662 para 264
- gap: 'Transport Mode = All' on the iLink cap rule needs confirming in the live cap configuration.

### Reference Fare Cap

**4102781** — action: `reword`
- old title: Correction to a higher ref removes the cap and charges the difference
- new title: Reference cap — correction to a higher ref removes the cap and charges the difference
- change: Tightened title; marked ref cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337 (same reference fare → same capping group), FBD-100662 para 265, FBD-100662 para 264

**4102782** — action: `reword`
- old title: Correction to a lower ref below the cap removes it and refunds
- new title: Reference cap — correction to a lower ref below the cap removes it and refunds
- change: Tightened title; marked cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337, FBD-100662 para 265, FBD-100662 para 264

**4102783** — action: `reword`
- old title: Correction to a lower ref still above the cap charges the extra
- new title: Reference cap — correction to a lower ref still above the cap charges the extra
- change: Tightened title; marked cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337, FBD-100662 para 265, FBD-100662 para 264

### Uncapped & Single Taps

**4102784** — action: `reword`
- old title: Single uncapped tap raised to a higher fare charges the difference
- new title: Uncapped tap — single tap raised to a higher fare charges the difference
- change: Tightened title; marked fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 183 (single tap, not capped), FBD-100662 para 264

**4102785** — action: `reword`
- old title: Single uncapped tap lowered refunds the difference
- new title: Uncapped tap — single tap lowered refunds the difference
- change: Tightened title; marked fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100389 para 183, FBD-100662 para 264

**4102786** — action: `reword`
- old title: Aligning two different-ref taps to the same ref applies the cap and refunds
- new title: Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds
- change: Tightened title; marked fare/cap values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337 (same reference fare → same capping group), FBD-100662 para 265, FBD-100662 para 264

**4102787** — action: `reword`
- old title: Lowering the higher-ref tap to match applies the lower cap and refunds
- new title: Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds
- change: Tightened title; marked fare/cap values UNCONFIRMED (ref.55 £6.40 from tracker); added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100662 para 337, FBD-100662 para 265, FBD-100662 para 264

### Town Service Cap

**4102788** — action: `reword`
- old title: Correction within the town service zone holds the cap
- new title: Town service cap — correction within the town zone holds the cap
- change: Tightened title; marked cap/fare values UNCONFIRMED (tracker, not FBD-100340's £1.00 example); added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100340 para 149 (cap applies when boarding+alighting both in the town zone), FBD-100340 para 278, FBD-100662 para 264

**4102789** — action: `reword`
- old title: Correction outside the town to a higher fare removes the cap and charges the difference
- new title: Town service cap — correction outside the town to a higher fare removes the cap and charges the difference
- change: Tightened title; marked cap/fare values UNCONFIRMED; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100340 para 322 (board in / alight out → not capped), FBD-100662 para 264

**4102790** — action: `reword`
- old title: Correction outside the town to a lower fare removes the cap and refunds
- new title: Town service cap — correction outside the town to a lower fare removes the cap and refunds
- change: Tightened title; marked cap value UNCONFIRMED; kept the existing GAP that no confirmed sub-£2.50 out-of-zone stop exists; added CR122 marker.
- citations: FBD-100662 para 691, FBD-100662 para 693, FBD-100662 para 271, FBD-100662 para 694, FBD-100698 (RouteType=1 RoutePointToPointFares – Ulsterbus alighting-stop changes), FBD-100340 para 322, FBD-100662 para 264
- gap: No confirmed 203b out-of-zone stop below £2.50 — the scenario may be unrunnable as written; confirm a suitable stop or drop the case.

### Capping Configuration

**4102869** — action: `reword`
- old title: Configure a daily capping rule
- new title: Capping config — configure a daily capping rule
- change: Grounded the operating-day definition (04:00–03:59) to FBD-100389; named the two rule-creation mechanisms per FBD-100662; generalised the invented screen wording.
- citations: FBD-100662 para 313-315 (two capping-rule creation mechanisms), FBD-100389 para 137 (daily cap over the 04:00–03:59 operating day), FBD-100340 para 149

**4102870** — action: `reword`
- old title: Configure weekly and monthly capping rules
- new title: Capping config — configure weekly and monthly capping rules
- change: Grounded weekly/monthly caps to FBD-100662/FBD-100340; generalised screen wording.
- citations: FBD-100662 para 265 (Ulsterbus Daily/Weekly/Monthly caps), FBD-100662 para 356-357 (UB Weekly Cap product/rule), FBD-100340 para 149 (daily/weekly/monthly caps per zone)
- gap: The operating-week start day is not stated in the specs read — confirm the configured week boundary.

**4102871** — action: `reword` — **RESOLVED 2026-07-21, superseded, see below**
- old title: Configure a transfer capping rule
- new title: Capping config — configure a transfer capping rule
- change: Removed the invented 'Transfer Caps tab' screen reference; flagged that a 'transfer cap' as a capping-rule type is not described in the capping specs — transfers are handled as zero-charge journeys (FBD-100651), not as a cap.
- citations: FBD-100651 (Glider transfer logic: a qualifying transfer is charged £0.00 — there is no separate 'transfer cap' concept in the capping specs)
- gap: **GAP** — a 'transfer capping rule' / 'Transfer Caps tab' is not described in FBD-100334/100340/100389/100651/100662. Transfers produce a zero charge (FBD-100651 CR123), which is not the same as a cap. Confirm whether a transfer-cap rule type actually exists in the portal before running.
- **Resolution note (2026-07-21):** George decided the case should test "transfer settles at £0.00" instead of the invented cap. Checked the live suite for existing CR123/£0.00-transfer coverage — none found (the only other free-transfer case, C4103587, covers the separate bus-to-rail CR133/CR064 mechanism). Rather than the above `reword` (which only tightened the title but kept the invented 'transfer cap' steps), the case was actually re-worded and pushed via `proposals/coherence-audit/fixes/abt-transfer-cap.rewrite.json` — see `abt-transfer-cap.changelog.md` for the applied title/body and full FBD-100651 §7.4 citations. This capping.rewrite.json entry is left unchanged for history/audit trail; it is no longer the operative version of C4102871.

**4102872** — action: `reword`
- old title: Add, edit and view a price cap
- new title: Capping config — add, edit and view a price cap
- change: Generalised the 'Price Capping page' screen name (not in specs); kept the add/edit/view CRUD behaviour.
- citations: FBD-100662 para 313-315, FBD-100340 para 149 (caps set up in the Operator Portal)
- gap: Exact screen name ('Price Capping page') is not in the specs — confirm the live UI label.

**4102873** — action: `reword`
- old title: Deactivate and archive a capping rule
- new title: Capping config — deactivate and archive a capping rule
- change: Kept behaviour but could not ground the deactivate/archive lifecycle in the specs read; generalised screen wording.
- citations: **none — see gaps**
- gap: **GAP** — the deactivate/archive rule lifecycle is not described in the capping specs read — confirm the states and transitions in the live portal.

**4102874** — action: `reword`
- old title: Price Rule information icon
- new title: Capping config — Price Rule information icon
- change: UI-only case; behaviour retained but not grounded in specs.
- citations: **none — see gaps**
- gap: **GAP** — the information-icon content/behaviour is a UI detail not described in any FBD — confirm against the live portal or a UX spec.

**4102875** — action: `reword`
- old title: A capping rule's created date-time is not set an hour in the future
- new title: Capping config — a new rule's created date-time is correct (not an hour ahead)
- change: Kept as a regression check for a timezone/BST off-by-one-hour defect; generalised screen wording.
- citations: **none — see gaps**
- gap: **GAP** — this is a defect-regression case (created-time stored an hour ahead, likely a BST/UTC bug) with no governing FBD requirement. Link the originating defect in the Refs field and tag @regression; confirm the defect id.

**4102876** — action: `reword`
- old title: Add a daily capping group
- new title: Capping config — add a daily capping group
- change: Grounded the capping-group concept to FBD-100662; retained behaviour.
- citations: FBD-100662 para 334-347 (ABT Capping Group product/rule; reference-fare → cap lookup), FBD-100662 para 337

**4102877** — action: `reword`
- old title: Add a weekly capping group
- new title: Capping config — add a weekly capping group
- change: Grounded weekly capping group to FBD-100662; retained behaviour.
- citations: FBD-100662 para 356-357 (UB Weekly Cap product/rule), FBD-100662 para 334-347

### Daily Capping

**4103473** — action: `reword`
- old title: Metro daily cap is reached and applied
- new title: Daily cap — Metro daily cap is reached and applied
- change: Grounded cap aggregation to FBD-100389; marked Metro cap/single values UNCONFIRMED; changed hard-coded '15 minutes' to 'the configured passback window' with an UNCONFIRMED note (passback is configurable per FBD-100389 assumptions).
- citations: FBD-100389 para 137 (daily cap, operating day 04:00–03:59), FBD-100389 para 219-221 (aggregate reaches cap; later charge reduced/£0.00), FBD-100662 para 264, FBD-100662 para 233 (Metro flat fare via CloudFare rules)
- gap: Exact passback/duplicate window value not in the specs (configurable) — confirm the configured value for the test environment.

**4103474** — action: `reword`
- old title: Ulsterbus reference-fare cap is reached within a fare band
- new title: Daily cap — Ulsterbus reference-fare cap is reached within a band
- change: Grounded reference-cap mechanism to FBD-100662 capping groups; marked cap/single values UNCONFIRMED; replaced hard-coded 15 min with the configured passback window.
- citations: FBD-100662 para 265 (Ulsterbus daily cap on reference fares), FBD-100662 para 337 (same reference fare → same capping group), FBD-100662 para 339 (Saving Type), FBD-100389 para 219-221
- gap: Passback window value — confirm for the test environment.

**4103475** — action: `reword`
- old title: Metro cap and Ulsterbus reference cap both apply on the same day
- new title: Daily cap — Metro cap and Ulsterbus reference cap both apply on the same day
- change: Grounded cap independence to FBD-100662 para 265; marked values UNCONFIRMED.
- citations: FBD-100662 para 265 (Ulsterbus caps distinct from Metro caps), FBD-100662 para 337, FBD-100389 para 137

**4103476** — action: `reword`
- old title: Metro and Ulsterbus caps evaluate independently when taps are interleaved
- new title: Daily cap — Metro and Ulsterbus caps evaluate independently when taps are interleaved
- change: Grounded to FBD-100662; marked values UNCONFIRMED. Near-variant of 4103475 — flagged for possible consolidation as a data variation.
- citations: FBD-100662 para 265, FBD-100662 para 337 (grouping is by reference fare, order-independent), FBD-100389 para 137
- gap: 4103475/4103476 differ only by tap ordering — candidate to fold into one case with an 'interleaved vs grouped' data variation.

**4103477** — action: `reword`
- old title: Two reference-fare bands cap independently on the same day
- new title: Daily cap — two reference bands cap independently on the same day
- change: Grounded per-band independence to the capping-group lookup (FBD-100662 para 337/340); marked cap values UNCONFIRMED.
- citations: FBD-100662 para 337 (each reference fare maps to its own capping group), FBD-100662 para 340 (cap lookup table keyed by reference fare), FBD-100662 para 265

**4103478** — action: `reword`
- old title: A single Metro tap does not trigger the Metro cap
- new title: Daily cap — a single Metro tap is charged in full
- change: Removed the over-specified claim that 'the cap requires two in-zone taps' (no such rule in the specs — the cap is purely an aggregate). Reworded to: a single tap's fare is below the cap so it is charged in full.
- citations: FBD-100389 para 183 (single tap, not capped), FBD-100389 para 137
- gap: No FBD states a minimum tap count to trigger a cap — the cap is aggregate-based; a single tap is charged in full simply because its fare is below the cap.

**4103479** — action: `reword`
- old title: Single taps in different reference bands are each charged in full
- new title: Daily cap — single taps in different reference bands are each charged in full
- change: Grounded to the capping-group model; marked fare values UNCONFIRMED.
- citations: FBD-100662 para 337 (one tap per reference band → no group reaches its cap), FBD-100389 para 183

### Capping Timing

**4103590** — action: `reword`
- old title: A newly configured capping rule activates the next business day
- new title: Capping timing — a newly configured capping rule activates the next business day
- change: Kept behaviour but could not ground the 'activates next business day' rule in any spec read.
- citations: **none — see gaps**
- gap: **GAP** — capping-rule activation timing ('next business day', not same day) is not stated in FBD-100334/100340/100389/100662/100698. Confirm the actual effective-date behaviour before running (may live in FBD-100307 or a config/UX spec).

**4103591** — action: `reword`
- old title: Taps either side of the 04:00 operating-day boundary fall into different cap days
- new title: Capping timing — taps either side of the 04:00 boundary fall into different cap days
- change: Fully grounded to FBD-100389 para 137; no value changes needed.
- citations: FBD-100389 para 137 (operating day 04:00:00 to 03:59:59 is the capping window)

**4103592** — action: `reword`
- old title: A newly deny-listed token starts being denied within about 30 minutes
- new title: Capping timing — a deny-listed token starts being denied within about a delta cycle
- change: Grounded the 15-minute delta and Declined Reason 2 to FBD-100662; changed the asserted '~30 minutes' to '~one delta cycle (~15 minutes)' since the spec states 15-minute deltas. (Section is 'Capping Timing' but this is a deny-list case — noted for re-section.)
- citations: FBD-100662 para 210 (full Deny List ≥ once/day; delta files every 15 minutes), FBD-100662 para 243 (Declined Reason 2 = On Deny List), FBD-100658 (DeclinedReason enum: 2 = On Deny List)
- gap: The original '~30 minutes' was an unsourced worst-case; spec states 15-minute deltas (FBD-100662 para 210). Confirm the device delta-pull cadence if a tighter/looser SLA is required.
- gap: Case belongs under a Deny List / device section rather than 'Capping Timing'.

**4103593** — action: `reword`
- old title: A tap-initiated re-authorisation removes a card within about 15 minutes
- new title: Capping timing — a re-authorised card is removed from the Deny List
- change: Grounded deny-list removal + 15-min delta propagation to FBD-100662; removed the unsourced 'tap-initiated re-authorisation within about 15 minutes' specifics — the trigger and exact timing are not in the specs read.
- citations: FBD-100662 para 210 (delta files carry additions AND removals every 15 minutes), FBD-100662 para 267 (add/remove cards from the deny list per the same rules as Metro TOO)
- gap: **GAP** — the 'tap-initiated re-authorisation' trigger and the specific ~15-minute removal SLA are not described in FBD-100662; the removal mechanism/timing likely lives in FBD-100307 (data flow) — confirm before asserting the trigger and timing.
- gap: Case belongs under a Deny List / device section rather than 'Capping Timing'.
