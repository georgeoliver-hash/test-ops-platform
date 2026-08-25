# ABT/BOS Capping — open questions / gap register

Route these to the engineer (Q&A loop, per CLAUDE.md). A gap nobody can answer is itself a finding.
**Proposal only — nothing pushed.**

## Headline open questions

1. **Q14 — Fares source.** Where do the concrete fare/cap values used across these cases come from
   (Metro £4.00/£2.30, iLink Z1 £6 / Z2 £11 / Z4 £19, ref.60 £7.20 / ref.61 £8.20, Bangor TS £2.50)?
   They are in the UB-TOO tracker but not in any FBD. Confirm the authoritative fares export so the worked
   examples can be grounded (currently all **UNCONFIRMED**).
2. **CR122 alighting-stop adjustment — is it live?** FBD-100662 paras 271/691/693 describe it as a *proposal*
   with UX 'to be determined'. ~34 correction cases depend on it. Is the portal mechanism actually implemented
   in the env5 test system? If not, those cases cannot run yet.
3. **Metro flat-fare correction applicability.** Metro routes are Tap On Only (Flat Fare) with alighting
   auto-set to the last stop in the Metro Network Zone (FBD-100658). Does CR122 even offer an alighting change
   for a flat-fare Metro tap? (Affects all Metro Daily Cap correction cases 4102757–4102767.)
4. **FBD-100334 is a stub.** V0.01 is an unfilled template; it does not specify the capping/reallocation
   *mechanics* the correction cases assert (auto refund/charge on recalculation). Is there a completed version,
   or should mechanics be grounded solely on FBD-100389/100662/100698? — **POSSIBLE SPEC GAP**, consider raising.

## Per-case gaps

- **4102757** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102758** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
  - No confirmed out-of-Metro-zone stop/fare for a 10A/10b tap in the tracker — needs checking on the live portal.
- **4102759** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102760** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
  - That a settled capped tap is NOT recalculated on correction is an implementation guard not stated in any FBD (FBD-100334 V0.01 is an unfilled stub) — confirm expected behaviour.
- **4102761** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
  - Preservation of a settled reduced fare on correction is an implementation guard not in any FBD — confirm.
- **4102762** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102763** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102764** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102765** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102766** (Metro Daily Cap):
  - Whether a declined (no-fare) journey is even correctable via CR122 is not specified — the case tests an internal guard not described in any FBD; confirm expected behaviour.
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
- **4102767** (Metro Daily Cap):
  - Metro routes are Tap On Only (Flat Fare) with the alighting auto-set to the last stop in the Metro Network Zone (FBD-100658); whether CR122 alighting-stop adjustment is even offered for flat-fare Metro taps is not specified — confirm before running.
  - Settlement idempotency (re-running settlement raises no new charge) is not stated in any FBD — confirm expected behaviour.
- **4102769** (Zonal Cap):
  - No confirmed Zone 3 fare for the corrected 10b tap in the tracker — confirm the stop/fare on the live portal.
- **4102773** (Zonal Cap):
  - Zonal-cap-takes-precedence-over-reference-cap ordering is implied by the capping-group model but not stated explicitly — confirm precedence rule.
- **4102775** (Zonal Cap):
  - 4102773/4102774/4102775 are three near-identical 'zonal cap beats reference cap' assertions on the same setup — candidate for consolidation into one case with a data-variations note.
- **4102777** (Zonal Cap):
  - Case sits in the 'Zonal Cap' section but tests the reference cap — consider moving to 'Reference Fare Cap'.
- **4102778** (Zonal Cap):
  - The tracker flags that some 10b Zone 1 stops also carry Metro codes and would cap at Metro £4.00 — the Zone 1 route/stop pair must be confirmed so the case exercises the Zone 1 (not Metro) cap.
- **4102779** (Zonal Cap):
  - Settlement idempotency is not stated in any FBD — confirm expected behaviour.
- **4102780** (Zonal Cap):
  - 'Transport Mode = All' on the iLink cap rule needs confirming in the live cap configuration.
- **4102790** (Town Service Cap):
  - No confirmed 203b out-of-zone stop below £2.50 — the scenario may be unrunnable as written; confirm a suitable stop or drop the case.
- **4102870** (Capping Configuration):
  - The operating-week start day is not stated in the specs read — confirm the configured week boundary.
- **4102871** (Capping Configuration): **RESOLVED 2026-07-21** — George confirmed the intent should be "transfer settles at £0.00", not a cap. Reworded and pushed live: title now "Transfers — a qualifying Metro/Glider transfer is charged £0.00", grounded on FBD-100651 §7.4 (CR123 Glider transfer logic) with a worked example from the Glider Transfer Scenarios V3.00.xlsx tracker (Scenario 1, G10D In → Glider East In). Verified no other live case in suite 30279 already covers this CR123 mechanism (C4103587 covers the separate bus-to-rail CR133/CR064 free-transfer mechanism, not CR123) — see `proposals/coherence-audit/fixes/abt-transfer-cap.rewrite.json` and `.changelog.md`. No longer an open gap; the original "GAP — a 'transfer capping rule' is not described in the specs" finding is superseded because the case no longer asserts that invented concept.
- **4102872** (Capping Configuration):
  - Exact screen name ('Price Capping page') is not in the specs — confirm the live UI label.
- **4102873** (Capping Configuration):
  - **GAP** — the deactivate/archive rule lifecycle is not described in the capping specs read — confirm the states and transitions in the live portal.
- **4102874** (Capping Configuration):
  - **GAP** — the information-icon content/behaviour is a UI detail not described in any FBD — confirm against the live portal or a UX spec.
- **4102875** (Capping Configuration):
  - **GAP** — this is a defect-regression case (created-time stored an hour ahead, likely a BST/UTC bug) with no governing FBD requirement. Link the originating defect in the Refs field and tag @regression; confirm the defect id.
- **4103473** (Daily Capping):
  - Exact passback/duplicate window value not in the specs (configurable) — confirm the configured value for the test environment.
- **4103474** (Daily Capping):
  - Passback window value — confirm for the test environment.
- **4103476** (Daily Capping):
  - 4103475/4103476 differ only by tap ordering — candidate to fold into one case with an 'interleaved vs grouped' data variation.
- **4103478** (Daily Capping):
  - No FBD states a minimum tap count to trigger a cap — the cap is aggregate-based; a single tap is charged in full simply because its fare is below the cap.
- **4103590** (Capping Timing):
  - **GAP** — capping-rule activation timing ('next business day', not same day) is not stated in FBD-100334/100340/100389/100662/100698. Confirm the actual effective-date behaviour before running (may live in FBD-100307 or a config/UX spec).
- **4103592** (Capping Timing):
  - The original '~30 minutes' was an unsourced worst-case; spec states 15-minute deltas (FBD-100662 para 210). Confirm the device delta-pull cadence if a tighter/looser SLA is required.
  - Case belongs under a Deny List / device section rather than 'Capping Timing'.
- **4103593** (Capping Timing):
  - **GAP** — the 'tap-initiated re-authorisation' trigger and the specific ~15-minute removal SLA are not described in FBD-100662; the removal mechanism/timing likely lives in FBD-100307 (data flow) — confirm before asserting the trigger and timing.
  - Case belongs under a Deny List / device section rather than 'Capping Timing'.

## Structural / section observations
- 4102777 sits in 'Zonal Cap' but tests the reference cap — move to 'Reference Fare Cap'.
- 4103592 / 4103593 sit in 'Capping Timing' but are Deny List cases — consider a Deny List section.
- Possible consolidations: 4102773/4102774/4102775 (zonal cap beats reference cap); 4103475/4103476 (independent caps, ordering variation).
- The 7 'Daily Reports' cases (4103129–4103135) were reviewed and EXCLUDED: they are Merit report generate/export cases, not capping-related.
