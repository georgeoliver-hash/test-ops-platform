# Automation backlog — **NEW** BOS & ABT Suite (devtype:200)

_Generated 2026-06-29T12:19:12+00:00 by system-test-ops. Suite id 30279, project TFTS - System Test._

**217 fully automatable + 136 partial** of 365 cases (4 destructive, 12 manual-only). _Partial = the UI flow is automatable but a step (card tap / print / cash) needs a hardware fixture or human eye._

## How to consume

- Reference `ref` (TestRail case id, e.g. C4099911) in each automated test so a result maps back to its case.
- Mirror device + feature as pytest markers; add @pytest.mark.destructive where destructive is true (deselected by default).
- cross_check lists the back-office systems the case asserts — the test must verify the event landed there (CloudFare / MERIT / SmartTrack).
- automatable/priority are system-test-ops judgements and a starting point; the automation engineer may override with rationale.


## Priority: High

### C4102791 · Re-tap at the same stage after annulment is the first good tap (Metro)  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap has been annulled before settlement
**WHEN** the passenger re-taps at the same boarding stage
**AND** the EndOfDay settlement runs
**THEN** the re-tap is charged as the first good tap at full fare
**AND** the annulled tap is charged £0.00

### C4102792 · Full Metro day reaches the daily cap after an annulment  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap has been annulled and re-tapped at the same stage
**WHEN** the passenger completes further Metro taps to reach the cap
**AND** the EndOfDay settlement runs
**THEN** the day caps at £4.00 with the third tap charged £0.00
**AND** the annulled tap is charged £0.00

### C4102793 · Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus)  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** an Ulsterbus ref.60 tap has been annulled before settlement
**WHEN** the passenger re-taps at the same boarding stage
**AND** the EndOfDay settlement runs
**THEN** the re-tap is charged as the first ref.60 tap at full fare
**AND** the annulled tap is charged £0.00

### C4102794 · Ulsterbus reference fare cap applies on the correct tap after annulment  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** an Ulsterbus ref.60 tap has been annulled and re-tapped
**WHEN** further ref.60 taps are made to reach the cap
**AND** the EndOfDay settlement runs
**THEN** the ref.60 cap of £7.20 is reached with later taps charged £0.00
**AND** the day total for ref.60 equals £7.20

### C4102795 · Re-tap after annulment in the ref.61 band caps at the ref.61 value  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** an Ulsterbus ref.61 tap has been annulled before settlement
**WHEN** the passenger re-taps in the ref.61 band and reaches the cap
**AND** the EndOfDay settlement runs
**THEN** the ref.61 daily cap of £8.20 is applied, not the adjacent ref.60 cap of £7.20
**AND** the day total for ref.61 equals £8.20

### C4102796 · Annulment in the ref.60 band does not borrow the higher ref.61 cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** an Ulsterbus ref.60 tap has been annulled and re-tapped
**WHEN** further ref.60 taps reach the cap
**AND** the EndOfDay settlement runs
**THEN** the ref.60 daily cap of £7.20 is applied, not the adjacent ref.61 cap of £8.20
**AND** the day total for ref.60 equals £7.20

### C4102797 · Genuine duplicate without annulment is still rejected as £0.00  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap with no annulment
**WHEN** a second tap is made at the same boarding stage within the duplicate window
**AND** the EndOfDay settlement runs
**THEN** the first tap is charged full fare
**AND** the second tap is rejected as a duplicate and charged £0.00

### C4102798 · Re-tap at a different stage after annulment is a normal first tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap has been annulled before settlement
**WHEN** the passenger re-taps at a different boarding stage
**AND** the EndOfDay settlement runs
**THEN** the re-tap is charged as the first good tap at full fare
**AND** the annulled tap is charged £0.00

### C4102799 · Annulling the re-tap as well leaves a later tap as the first good tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap and its re-tap have both been annulled
**WHEN** the passenger makes a third tap at the same stage
**AND** the EndOfDay settlement runs
**THEN** both annulled taps are charged £0.00
**AND** the third tap is the first good tap at full fare

### C4102800 · Annulment processed in the same settlement run as the re-tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap is annulled and re-tapped at the same stage with no settlement between them
**WHEN** the EndOfDay settlement runs once
**THEN** the annulled tap is charged £0.00
**AND** the re-tap is the first good tap at full fare

### C4102801 · Annulment with no re-tap leaves no chargeable journey  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a single Metro tap
**WHEN** the tap is annulled
**AND** the EndOfDay settlement runs
**THEN** the annulled tap is charged £0.00
**AND** the day total is £0.00

### C4102802 · Annulling a capped tap does not corrupt the day total  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro day at the £4.00 cap with a £0.00 capped last tap
**WHEN** the capped tap is annulled before settlement
**AND** the EndOfDay settlement runs
**THEN** the annulled capped tap is charged £0.00
**AND** the day total stays £4.00

### C4102803 · Annulling the first capped-day tap then re-tapping restores correct totals  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro day approaching the cap
**WHEN** the first tap is annulled and a later re-tap is made
**AND** the EndOfDay settlement runs
**THEN** the annulled tap is charged £0.00
**AND** the day total is preserved at £4.00

### C4102804 · Annulment on one card does not affect a similar tap on another card  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** one card has an annulled tap at a stage and time
**WHEN** a different card taps at the same stage and time
**AND** the EndOfDay settlement runs
**THEN** the other card's tap is charged as a normal first tap
**AND** it is not treated as a duplicate

### C4102805 · Ulsterbus re-tap with a different alighting and fare after annulment  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** an Ulsterbus tap has been annulled before settlement
**WHEN** the passenger re-taps from the same stage to a different alighting stage and fare
**AND** the EndOfDay settlement runs
**THEN** the re-tap is charged its new fare as the first good tap
**AND** the annulled tap is charged £0.00

### C4102806 · Re-tap at the same stage without an annulment is a genuine duplicate  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap that was not annulled
**WHEN** a second tap is made at the same boarding stage
**AND** the EndOfDay settlement runs
**THEN** the first tap is charged full fare
**AND** the second tap is rejected as a duplicate at £0.00

### C4102807 · Multiple annulment and re-tap cycles in one day cap correctly  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** two separate annul-and-re-tap cycles earlier in the day
**WHEN** the passenger makes a further normal tap
**AND** the EndOfDay settlement runs
**THEN** all annulled taps are charged £0.00
**AND** the good taps cap the day at £4.00

### C4102808 · Annulment on a previous day does not affect the new day's first tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-23967
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a tap was annulled two days ago
**WHEN** the passenger makes the first tap of a new day
**AND** the EndOfDay settlement runs
**THEN** the new day's tap is charged as a normal first tap
**AND** it is not treated as a duplicate

### C4102809 · A valid tap rejected as duplicate is retained when the first tap is cancelled  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap and a same-stage tap flagged as a duplicate in the portal
**WHEN** the first tap is cancelled
**AND** the EndOfDay settlement runs
**THEN** the first tap is shown cancelled with the "**" indicator
**AND** the previously-duplicate tap becomes the valid first tap charged full fare and remains in Journey History

### C4102810 · Several same-stage taps then cancelling the first promotes the next valid tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a first tap and three same-stage duplicate taps
**WHEN** the first tap is cancelled
**AND** the EndOfDay settlement runs
**THEN** the cancelled tap shows the "**" indicator
**AND** the next tap becomes the valid first tap at full fare
**AND** the remaining taps stay duplicates at £0.00

### C4102811 · No valid journey is left missing after the annulment  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap and a same-stage duplicate tap
**WHEN** the first tap is cancelled
**AND** the EndOfDay settlement runs
**THEN** exactly one valid journey is shown, charged full fare, for the surviving tap
**AND** no valid journey is missing from Journey History

### C4102812 · Annulment processed before the second tap makes it a normal first journey  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap that is cancelled before any further tap
**WHEN** the passenger makes a second tap at the same stage
**AND** the EndOfDay settlement runs
**THEN** the cancelled tap shows the "**" indicator
**AND** the second tap is the valid first tap at full fare

### C4102813 · Cancelling the rehabilitated tap promotes the next tap in turn  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a first tap with two same-stage duplicate taps, with the first tap already cancelled
**WHEN** the rehabilitated (second) tap is then cancelled
**AND** the EndOfDay settlement runs
**THEN** the first two taps show the "**" indicator
**AND** the third tap becomes the valid first tap at full fare

### C4102814 · Cancelling a tap with no following tap leaves nothing missing  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a single Metro tap
**WHEN** the tap is cancelled
**AND** the EndOfDay settlement runs
**THEN** the tap shows the "**" indicator and no other journey is shown
**AND** the day total is £0.00

### C4102815 · A second tap from a different stage is unaffected by the annulment  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24259
_ABT / Functional / Annulment & Re-tap_

**GIVEN** a Metro tap and a valid different-stage tap
**WHEN** the first tap is cancelled
**AND** the EndOfDay settlement runs
**THEN** the first tap shows the "**" indicator
**AND** the different-stage tap remains the valid first tap at full fare

### C4102953 · Support multiple travel zones for a stop  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Configuration & Setup_

**GIVEN** an operator is on the ABT Operator Portal with rights to add daily capping rules
**WHEN** the operator configures a stop that belongs to multiple travel zones
**THEN** the stop is recognised in each of its travel zones
**AND** capping rules evaluate the stop against each zone

### C4102955 · Capping-rule products load from the fares engine  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Configuration & Setup_

**GIVEN** an operator is configuring a base product on Price Capping
**WHEN** the operator selects the base product
**THEN** the product list is loaded from the fares engine products

### C4102850 · A recoverable debt is recovered and the card returns to Active  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** a card with a recoverable debt linked to a second card
**WHEN** the debt recovery process runs
**THEN** both cards show status "Active" in the Operator Portal
**AND** each card shows its expected number of authorisation requests

### C4102851 · An unrecoverable debt leaves the cards Blocked  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** a card with an unrecoverable debt linked to a second card
**WHEN** the debt recovery process runs
**THEN** both cards show status "Blocked" in the Operator Portal
**AND** each card shows its expected number of authorisation requests

### C4102852 · Visa MIT recovery clears a recoverable issuer-liability debt  (6m)  — cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** a Visa account with an EndOfDay auth failure and a recoverable issuer-liability debt
**WHEN** the scheduled MIT recovery cycles run and recover the debt
**THEN** the Visa account is no longer blocked in the Operator Portal
**AND** it is removed from the Deny List

### C4102853 · A successful recovery removes the card from the Deny List  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** a card on the Deny List with a recoverable debt
**WHEN** the debt recovery process runs and recovers the debt
**THEN** the card is removed from the Deny List
**AND** its status is "Active"

### C4102854 · The recovered account is visible in the Operator Portal with the correct status  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** a completed debt recovery for a card with a masked PAN
**WHEN** an operator views the Customers page in the Operator Portal
**THEN** the account record for that masked PAN is shown
**AND** its status is "ACCEPTED"

### C4102855 · Recovery behaviour is observable in the Operator Portal, logging verified by dev tests  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24990
_ABT / Functional / Debt Recovery_

**GIVEN** manual QA has no access to the open-payment-bs logs
**WHEN** the recovery behaviour is checked in the Operator Portal
**THEN** the recovery outcome is confirmed by the portal's observable status changes
**AND** the new log entries are confirmed by the automated dev tests, not this manual pack

### C4102945 · A card is added to the Deny List when it fails payment authorisation  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Debt Recovery_

**GIVEN** a customer's card is not on the Deny List
**WHEN** the card fails authorisation for a payment
**THEN** the card is automatically added to the Deny List

### C4102946 · A card on the Deny List is prevented from future travel until resolved  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Debt Recovery_

**GIVEN** a customer's card is on the Deny List
**AND** devices have the latest Deny List
**WHEN** the customer attempts to use the blocked card for travel
**THEN** the card is prevented from being used for travel

### C4102947 · A card is removed from the Deny List when its debt is recovered  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Debt Recovery_

**GIVEN** a customer's card is on the Deny List
**WHEN** the debt is recovered via back-office automatic retry, customer tap-initiated, customer online, or operator online recovery
**THEN** the card is automatically removed from the Deny List
**AND** the card is re-enabled for future travel

### C4102816 · Second tap after a same-stage retail transaction is flagged duplicate  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap followed by a same-stage retail transaction
**WHEN** a second same-stage tap is made within the duplicate window
**AND** the EndOfDay settlement runs
**THEN** the first tap is charged full fare
**AND** the second is flagged a duplicate at £0.00
**AND** the duplicate is recorded against the original tap

### C4102818 · Multiple interleaved retail transactions never reset the duplicate reference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap and several interleaved same-stage retail transactions
**WHEN** further same-stage taps are made
**AND** the EndOfDay settlement runs
**THEN** the first tap is charged full fare and every later same-stage tap is a duplicate at £0.00
**AND** each duplicate is recorded against the original tap

### C4102819 · A retail transaction from a different stage still allows the duplicate  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap and a retail transaction from a different stage
**WHEN** a second same-stage tap is made
**AND** the EndOfDay settlement runs
**THEN** the second tap is flagged a duplicate at £0.00
**AND** it is recorded against the original tap

### C4102821 · The retail transaction itself is never flagged a duplicate of a tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap
**WHEN** a same-stage retail transaction is made
**AND** the EndOfDay settlement runs
**THEN** the retail transaction is recorded correctly and charged its amount
**AND** it is not flagged as a duplicate

### C4102948 · ETM Metro Tap-On-Only — end to end  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / End to End_

**GIVEN** an ETM set to Metro is on the FLU screen with a valid EMV card
**WHEN** the customer performs a Tap-On-Only journey
**AND** the EndOfDay settlement runs
**THEN** the journey is charged correctly and capped per the Metro rules
**AND** the journey is visible in CloudFare, Merit and the ABT Operator and Passenger portals

### C4102949 · ETM Metro retail transaction — end to end  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / End to End_

**GIVEN** an ETM set to Metro is on the FLU screen with a valid EMV card
**WHEN** the operator processes a retail transaction
**AND** the EndOfDay settlement runs
**THEN** the retail transaction is charged correctly
**AND** it is visible in CloudFare, Merit and the ABT portals

### C4102950 · HHD Glider Tap-On-Only — end to end  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / End to End_

**GIVEN** an HHD set to Glider is on the Sales screen with a valid EMV card
**WHEN** the customer performs a Tap-On-Only journey
**AND** the EndOfDay settlement runs
**THEN** the journey is charged correctly and capped per the Glider rules
**AND** it is visible in CloudFare, Merit and the ABT portals

### C4102951 · HHD Glider retail transaction — end to end  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / End to End_

**GIVEN** an HHD set to Glider is on the Sales screen with a valid EMV card
**WHEN** the operator processes a retail transaction
**AND** the EndOfDay settlement runs
**THEN** the retail transaction is charged correctly
**AND** it is visible in CloudFare, Merit and the ABT portals

### C4102952 · HHD Rail retail transaction — end to end  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / End to End_

**GIVEN** an HHD set to Rail is on the Sales screen with a valid EMV card
**WHEN** the operator processes a retail transaction
**AND** the EndOfDay settlement runs
**THEN** the retail transaction is charged correctly
**AND** it is visible in CloudFare, Merit and the ABT portals

### C4102824 · A cancelled journey with a £0.00 fare is still visible  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a capped Metro tap charged £0.00 that is then cancelled
**WHEN** the EndOfDay settlement runs
**THEN** Journey History shows the £0.00 journey
**AND** it is marked as cancelled with the "**" indicator

### C4102826 · A zero-fare correction on a cancelled tap leaves a single visible row  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a cancelled Metro tap
**WHEN** its alighting stop is corrected so the fare shows £0.00
**AND** the EndOfDay settlement runs
**THEN** Journey History still shows a single cancelled journey for that tap
**AND** exactly one journey row exists for it

### C4102827 · Editing the stop on a non-cancelled journey still works  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a normal (non-cancelled) Metro journey
**WHEN** its alighting stop is corrected
**AND** the EndOfDay settlement runs
**THEN** Journey History shows the journey with the corrected stop charged its fare
**AND** it is not marked as cancelled

### C4102830 · Cancelling a charged journey produces a refund and retains the record  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a settled Metro journey charged £2.30
**WHEN** the journey is cancelled
**AND** the EndOfDay settlement runs
**THEN** a refund of £2.30 is made for the journey
**AND** Journey History shows a single cancelled journey for it

### C4102831 · Editing the stop on a cancelled tap after settlement keeps the record  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a settled Metro journey that was cancelled and refunded £2.30
**WHEN** its alighting stop is corrected
**AND** the EndOfDay settlement runs
**THEN** Journey History shows a single cancelled journey with the corrected stop
**AND** no additional refund is made

### C4102833 · A settled TOO journey shows its onward stops, not "No options"  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** a settled TOO journey on route 72b boarding from Greys Farm
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the dropdown is populated with the 14 onward fare-bearing stops
**AND** it does not show "No options" and excludes the zero-fare stop

### C4102834 · A settled TOO journey from another stage shows its onward stops  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** a settled TOO journey on route 72b boarding from Moygashel Busby Shop
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the dropdown is populated with the 15 onward fare-bearing stops
**AND** it does not show "No options" and excludes the zero-fare stop

### C4102837 · "No options" is correct when the boarding stage is the last stop  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** a settled TOO journey boarding from the last stop on the route
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the dropdown shows "No options"
**AND** this is expected because there are no onward stops with a fare

### C4102878 · Configure the End of the Operational Day and Week  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Administrator Settings_

**GIVEN** an administrator is signed into the Operator Portal
**WHEN** the administrator sets the End of the Operational Day and the End of the Operational Week
**THEN** each operational day is a 24-hour period anchored to that time
**AND** the operational week is anchored to the configured day

### C4102881 · Configure debt-recovery retry attempts and message  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Administrator Settings_

**GIVEN** an administrator is signed into the Operator Portal
**AND** a customer's card is on the deny list
**WHEN** the administrator sets the max online and tap-initiated retry attempts and the unsuccessful-recovery message
**THEN** the customer is limited to that number of retries
**AND** the configured message is shown on an unsuccessful recovery

### C4102882 · Configure a minimum fare for an e-Purse smartcard  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_ABT / Functional / Operator Web Portal / Administrator Settings_

**GIVEN** an administrator has rights to configure a minimum e-Purse fare
**AND** the Admin tab is displayed on the Operator Portal
**WHEN** the administrator sets a minimum fare for an e-Purse smartcard
**THEN** the minimum fare is saved
**AND** applied to e-Purse validation

### C4102869 · Configure a daily capping rule  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is signed in and the End of the Operating Day is configured
**WHEN** the administrator configures a daily capping rule
**AND** a customer performs transactions within a single operating day
**THEN** the customer's charges are capped at the configured daily cap

### C4102870 · Configure weekly and monthly capping rules  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is signed in and the operating week is configured
**WHEN** the administrator configures a weekly or monthly capping rule
**THEN** the rule is created
**AND** caps charges over the configured period

### C4102871 · Configure a transfer capping rule  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is signed in and the Price Capping page Transfer Caps tab is selected
**WHEN** the administrator configures a transfer cap
**THEN** the transfer cap is created
**AND** applied to qualifying transfers

### C4102872 · Add, edit and view a price cap  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is on the Price Capping page
**WHEN** the operator adds, edits or views a daily or weekly price cap
**THEN** the price cap is saved
**AND** shown with its configured values

### C4102873 · Deactivate and archive a capping rule  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator has selected a capping rule on the Price Capping page
**WHEN** the operator deactivates an active rule or archives an inactive rule
**THEN** the rule's status is updated accordingly

### C4102874 · Price Rule information icon  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is signed in on the Price Rule page
**WHEN** the operator selects the information icon
**THEN** the price-rule guidance is displayed

### C4102875 · A capping rule's created date-time is not set an hour in the future  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator is on the Price Capping tab
**WHEN** the operator creates a capping rule
**THEN** the rule's created date-time matches the actual creation time
**AND** it is not recorded an hour in the future

### C4102876 · Add a daily capping group  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator has navigated to the ABT Price Rule page
**WHEN** the operator adds a daily capping group
**THEN** the daily capping group is created

### C4102877 · Add a weekly capping group  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Capping Configuration_

**GIVEN** an operator has navigated to the ABT Price Rule page
**WHEN** the operator adds a weekly capping group
**THEN** the weekly capping group is created

### C4102867 · View all taps including taps not valid for a journey  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customer Services_

**GIVEN** a customer has performed valid and invalid taps on a payment card
**WHEN** the operator views the customer's transaction history for a date range
**THEN** all taps are shown, including those not valid for a journey

### C4102859 · Search and filter customers  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** an operator is on the Customer Information page
**WHEN** the operator searches by Unique Account ID, masked PAN, card expiry, or journey/transaction date
**THEN** the matching customer accounts are listed
**AND** the results can be paged and filtered by user type

### C4102860 · Select and view a customer account  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** an operator has located a customer on the Customer Information page
**WHEN** the operator selects the customer's card account
**THEN** the account details are displayed

### C4102862 · View and export a customer's Transaction History  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** a customer has performed tap transactions on a registered device
**AND** the operator has selected the customer's card account
**WHEN** the operator opens Transaction History and applies filters
**THEN** the tap/transaction details are displayed with paging
**AND** the transaction history can be exported

### C4102863 · Queue a refund from a transaction  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** the transaction history for a card is displayed
**AND** the operator has refund privileges
**WHEN** the operator queues a refund for a transaction
**THEN** the refund request is queued for authorisation
**AND** a refund value above the original payment is rejected

### C4102865 · Authorisations — approve, decline and reject a refund request  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** a refund request has been queued and requires second-level approval
**AND** the approver is on the Authorisations page
**WHEN** the approver approves, declines or rejects the request
**THEN** the request outcome is applied
**AND** recorded
**AND** the Authorisations table reflects the result with paging

### C4102887 · Run the Audit Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Audit Report
**THEN** the Audit Report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102892 · Run the Deny List Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Deny List Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102894 · Run the EMV Summary Report  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the EMV Summary Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102897 · Run the Expired Tap Report  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Expired Tap Report
**THEN** the report is generated
**AND** it displays expired card taps
**AND** the report can be exported

### C4102898 · Run the Fare Band Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Fare Band Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102902 · Run the Journeys by Card Scheme Report  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Journeys by Card Scheme Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102907 · Run the Refunds Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Refunds Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102909 · Run the Retail Transactions Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Retail Transactions Report or the Summary Retail Transaction Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102910 · Run the Revenue Apportionment Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Revenue Apportionment Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102911 · Run the Revenue by Business Rule Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Revenue by Business Rule Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102912 · Run the Revenue by MID Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Revenue by MID Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102913 · Run the Revenue Inspection Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Revenue Inspection Report or the Revenue Inspectors Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102916 · Run the Transaction Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Transaction Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102856 · Operator sign-on and navigation  (6m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Sign On & Access_

**GIVEN** the Operator Web Portal sign-on page is displayed
**AND** the user account has the required access rights
**WHEN** the operator signs on with valid credentials
**THEN** the operator is signed in
**AND** the portal menus are available
**AND** each menu option opens its page

### C4102857 · Access rights differ by user role  (6m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Sign On & Access_

**GIVEN** users are configured with different access-right profiles
**WHEN** each user signs on to the Operator Web Portal
**THEN** each user sees only the tasks permitted by their profile
**AND** restricted tasks are not available to them

### C4102858 · Operator can log out  (6m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Sign On & Access_

**GIVEN** an operator is signed into the Operator Web Portal
**WHEN** the operator logs out
**THEN** the session ends
**AND** the sign-on page is shown

### C4102931 · View and print Journey History  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on and the account home screen is displayed
**WHEN** the customer opens Journey History
**THEN** the taps and journeys for the card or mobile wallet are listed
**AND** the journey history can be printed

### C4102932 · View and print Transaction History  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on and the account home screen is displayed
**WHEN** the customer opens Transaction History
**THEN** the transactions for the card or mobile wallet are listed
**AND** the transaction history can be printed

### C4102933 · Request a refund  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on and viewing their transaction history
**WHEN** the customer raises a refund request for a transaction
**THEN** the refund request is submitted for operator authorisation

### C4102934 · Retry a declined payment  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on with a declined payment on their account
**WHEN** the customer retries the payment
**THEN** the payment is re-attempted
**AND** a successful retry clears the outstanding amount

### C4102935 · Request a card replacement  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on and the account home screen is displayed
**WHEN** the customer requests a card replacement
**THEN** the card replacement request is submitted

### C4102927 · Sign on to an anonymous account  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Sign On & Account_

**GIVEN** a customer is on the Passenger Web Portal sign-on page
**AND** their payment card or mobile wallet has journeys in the previous seven days
**WHEN** the customer enters valid card details
**THEN** the customer is signed on to their anonymous account
**AND** the account home screen is displayed

### C4102928 · Sign-on is prevented for invalid, no-journey or blocked cards  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Sign On & Account_

**GIVEN** a customer is on the Passenger Web Portal sign-on page
**WHEN** the customer enters invalid details, a card with no journeys in the previous seven days, or a blocked card
**THEN** the customer is prevented from signing on
**AND** the relevant message is shown for each case

### C4102929 · View account balance and home summary  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Sign On & Account_

**GIVEN** a customer is signed on and the account home screen is displayed
**AND** the card has completed ABT taps that day
**WHEN** the customer views the home screen
**THEN** the account balance is shown
**AND** a summary of card details, account ID and journey/transaction history is shown

### C4102930 · Sign off the Passenger Web Portal  (6m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Sign On & Account_

**GIVEN** a customer is signed into the Passenger Web Portal
**WHEN** the customer signs off
**THEN** the session ends
**AND** the sign-on page is shown

### C4102937 · Declined payments are guaranteed up to the Issuer Liability Threshold  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Card Verification_

**GIVEN** a customer has made a transaction with a Visa, MasterCard or Maestro card
**AND** the card failed authentication for payment
**WHEN** the declined payment is not recovered from the customer
**THEN** the card issuer guarantees the payment up to the Issuer Liability Threshold

### C4102938 · Account Verification Request on first use of a Visa card  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Card Verification_

**GIVEN** a customer has not yet transacted in this network with their Visa card
**WHEN** the customer uses the Visa card to make a transaction
**THEN** an Account Verification Request is performed
**AND** the card is confirmed for use

### C4102939 · Pre-Authorisation check on first use each day  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Card Verification_

**GIVEN** a customer has not yet transacted today with their MasterCard or Maestro card
**WHEN** the customer uses the card to make a transaction
**THEN** a Pre-Authorisation check is performed

### C4102940 · Pre-Authorisation check on first use after removal from the Deny List  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Card Verification_

**GIVEN** a customer's MasterCard or Maestro card has been removed from the Deny List
**WHEN** the customer next uses the card to make a transaction
**THEN** a Pre-Authorisation check is performed

### C4102943 · Capping rules are applied retrospectively to late taps  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Late Taps_

**GIVEN** the maximum late data period is configured to 14 days
**AND** active capping rules are configured
**WHEN** a late tap is received within the period that should trigger a cap
**THEN** the capping rules are applied retrospectively to that day

### C4102757 · Same-fare correction holds the Metro cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day has reached the £4.00 daily cap
**AND** the scenario is run in both the Operator and Passenger portals
**WHEN** an alighting stop is corrected to another Metro stage of equal fare
**AND** the overnight EndOfDay settlement runs
**THEN** the Metro cap still applies
**AND** the day total stays £4.00
**AND** no auto-settlement or refund is raised

### C4102758 · Correction outside the Metro zone removes the cap and charges the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** two Metro-zone taps that would settle under the £4.00 cap
**WHEN** one tap's alighting is corrected to a stop outside the Metro zone at a higher fare
**AND** the overnight EndOfDay settlement runs
**THEN** the Metro cap is removed
**AND** the corrected tap is charged its higher fare
**AND** an auto-settlement collects the difference, taking the day above £4.00

### C4102759 · Correction into the Metro zone applies the cap and refunds the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** one Metro tap and one Ulsterbus tap outside the Metro zone
**WHEN** the Ulsterbus tap's alighting is corrected to a stop inside the Metro zone
**AND** the overnight EndOfDay settlement runs
**THEN** both taps fall under the £4.00 Metro cap
**AND** the day total is £4.00
**AND** an auto-refund returns the difference to the account

### C4102760 · Correcting a settled free (capped) tap keeps it at £0.00  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap, with the third tap charged £0.00
**WHEN** the alighting stop on the settled £0.00 tap is corrected
**THEN** that tap is still charged £0.00
**AND** is not recalculated to the full £2.30
**AND** the day total stays £4.00 and the tap remains settled

### C4102761 · Correcting a settled partially-capped tap keeps it at £1.70  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap, with the second tap reduced to £1.70 to complete the cap
**WHEN** the alighting stop on the settled £1.70 tap is corrected
**THEN** that tap is still charged £1.70
**AND** is not recalculated to the full £2.30
**AND** the day total stays £4.00 and the tap remains settled

### C4102762 · A correction never pushes the day total over the Metro cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap
**WHEN** the alighting stop on a capped tap is corrected
**THEN** the day total charged on the card does not exceed £4.00

### C4102764 · Correcting the first full-fare tap leaves its charge unchanged  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap, with the first tap charged the full £2.30
**WHEN** the alighting stop on the first tap is corrected
**THEN** the first tap is still charged £2.30
**AND** the day total stays £4.00

### C4102781 · Correction to a higher ref removes the cap and charges the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Reference Fare Cap_

**GIVEN** two same-ref taps that would settle under the ref daily cap
**AND** zonal capping is disabled so the reference cap governs
**WHEN** one tap's alighting is corrected to a higher reference-fare stop
**AND** the overnight EndOfDay settlement runs
**THEN** the reference cap is removed and both taps are charged their uncapped fares
**AND** an auto-settlement collects the difference above the former cap

### C4102782 · Correction to a lower ref below the cap removes it and refunds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Reference Fare Cap_

**GIVEN** two same-ref taps capped at the reference daily cap
**AND** zonal capping is disabled so the reference cap governs
**WHEN** one tap's alighting is corrected to a lower fare so the uncapped aggregate falls below the cap
**AND** the overnight EndOfDay settlement runs
**THEN** the reference cap is removed
**AND** the charge is the lower aggregate
**AND** an auto-refund returns the difference

### C4102783 · Correction to a lower ref still above the cap charges the extra  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Reference Fare Cap_

**GIVEN** two same-ref taps capped at the reference daily cap
**AND** zonal capping is disabled so the reference cap governs
**WHEN** one tap's alighting is corrected to a lower fare on a different ref, leaving the aggregate above the cap
**AND** the overnight EndOfDay settlement runs
**THEN** the reference cap is removed
**AND** the charge is the uncapped aggregate
**AND** an auto-settlement collects the amount above the former cap

### C4102788 · Correction within the town service zone holds the cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Town Service Cap_

**GIVEN** a Bangor town service day has reached the £2.50 cap (Bus mode)
**AND** the scenario is run in both the Operator and Passenger portals
**WHEN** one tap's alighting is corrected to another stop within the town service zone
**AND** the overnight EndOfDay settlement runs
**THEN** the town service cap still applies
**AND** the total stays £2.50
**AND** no auto-settlement or refund is raised

### C4102789 · Correction outside the town to a higher fare removes the cap and charges the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Town Service Cap_

**GIVEN** a Bangor town service day has reached the £2.50 cap
**WHEN** one tap's alighting is corrected to a higher-fare stop outside the town area
**AND** the overnight EndOfDay settlement runs
**THEN** the town service cap is removed
**AND** the corrected tap is charged the higher fare
**AND** an auto-settlement collects the difference

### C4102790 · Correction outside the town to a lower fare removes the cap and refunds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Town Service Cap_

**GIVEN** a Bangor town service day has reached the £2.50 cap
**AND** a stop outside the town area exists at a fare below £2.50
**WHEN** one tap's alighting is corrected to that lower-fare stop outside the town area
**AND** the overnight EndOfDay settlement runs
**THEN** the town service cap is removed
**AND** the corrected tap is charged the lower fare
**AND** an auto-refund returns the difference

### C4102784 · Single uncapped tap raised to a higher fare charges the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Uncapped & Single Taps_

**GIVEN** a single uncapped tap to which no cap applies
**WHEN** the tap's alighting is corrected to a higher-fare stop
**AND** the overnight EndOfDay settlement runs
**THEN** the journey shows the amended alighting stop charged at the higher fare
**AND** an auto-settlement collects the additional balance

### C4102785 · Single uncapped tap lowered refunds the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Uncapped & Single Taps_

**GIVEN** a single uncapped tap to which no cap applies
**WHEN** the tap's alighting is corrected to a lower-fare stop
**AND** the overnight EndOfDay settlement runs
**THEN** the journey shows the amended alighting stop charged at the lower fare
**AND** an auto-refund returns the difference

### C4102786 · Aligning two different-ref taps to the same ref applies the cap and refunds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Uncapped & Single Taps_

**GIVEN** two taps on different reference fares, so no cap applies at settlement
**AND** zonal capping is disabled
**WHEN** one tap is corrected so both taps share the same reference fare
**AND** the overnight EndOfDay settlement runs
**THEN** the reference cap now applies
**AND** the total is the capped amount
**AND** an auto-refund returns the difference above the cap

### C4102787 · Lowering the higher-ref tap to match applies the lower cap and refunds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Uncapped & Single Taps_

**GIVEN** two taps on different reference fares, so no cap applies at settlement
**AND** zonal capping is disabled
**WHEN** the higher-fare tap is corrected down to match the other tap's reference fare
**AND** the overnight EndOfDay settlement runs
**THEN** the lower reference cap now applies
**AND** the total is that cap
**AND** an auto-refund returns the difference

### C4102768 · Higher-fare correction within the zone holds the cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** an iLink zone day has reached its zone cap
**AND** the scenario is run in both the Operator and Passenger portals
**WHEN** one tap is corrected to a higher-fare stage still within the same zone
**AND** the overnight EndOfDay settlement runs
**THEN** the zone cap still applies at its correct value
**AND** no auto-settlement or refund is raised

### C4102769 · Higher-fare correction outside the zone removes the cap and charges the difference  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** an iLink zone day has reached its zone cap
**WHEN** one tap is corrected to a higher-fare stage outside the zone
**AND** the overnight EndOfDay settlement runs
**THEN** the zone cap is removed
**AND** the corrected tap is charged its higher fare
**AND** an auto-settlement collects the difference, or a higher zone cap applies if reached

### C4102770 · Lower-fare correction within the zone keeps the day above cap and holds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** an iLink zone day has reached its zone cap
**WHEN** one tap is corrected to a lower-fare stage still within the zone, keeping the day above the cap
**AND** the overnight EndOfDay settlement runs
**THEN** the zone cap still applies
**AND** the day total is unchanged
**AND** no auto-refund or settlement is raised

### C4102771 · Lower-fare correction drops the day below cap and refunds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** an iLink zone day has reached its zone cap
**WHEN** one tap is corrected to a lower fare so the day total drops below the cap
**AND** the overnight EndOfDay settlement runs
**THEN** the zone cap is removed
**AND** the charge reduces to the new total
**AND** an auto-refund returns the difference

### C4102772 · Zone 4 correction within the highest band holds the cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: CR122
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** an iLink Zone 4 day has reached the £19.00 cap (the highest band)
**WHEN** one tap is corrected to a higher-fare stage outside Zone 4 but still within the £19.00 band
**AND** the overnight EndOfDay settlement runs
**THEN** the Zone 4 cap still applies
**AND** the account stays at £19.00
**AND** no auto-settlement is raised

### C4102773 · Correction into a capped zone audits a free tap under the zonal cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** the iLink Zone 2 cap of £11.00 is already reached
**AND** a tap is charged and assigned to the Zone 1 cap
**WHEN** that tap's alighting is corrected to a Zone 2 stop
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is audited as a £0.00 free tap under the Zone 2 cap
**AND** it is not charged the reference fare and the day total stays at the £11.00 cap

### C4102774 · A correction into a capped zone does not increase the account total  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** the iLink Zone 2 cap of £11.00 is already reached
**AND** the aggregated account total for the day is noted
**WHEN** a Zone 1 tap is corrected to a Zone 2 stop
**AND** the EndOfDay settlement runs
**THEN** the aggregated account total for the day has not increased
**AND** the corrected tap is audited at £0.00

### C4102775 · The cap shown after a correction is the zonal cap, not a reference cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** the iLink Zone 2 cap of £11.00 is already reached
**WHEN** a Zone 1 tap is corrected to a Zone 2 stop
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is audited at £0.00 because the Zone 2 cap was reached
**AND** it is not charged the reference fare

### C4102777 · A journey with no zonal cap still uses the reference cap correctly  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** no zonal cap applies to the day and the ref.60 cap of £7.20 is reached
**AND** zonal capping is not enabled for these journeys
**WHEN** a ref.60 tap's alighting is corrected to another ref.60 stage
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is audited as a £0.00 free tap under the ref.60 cap
**AND** the £7.20 reference cap still governs the day

### C4102778 · Correcting to another stop in the same zone keeps the zonal cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** the iLink Zone 1 cap of £6.00 is reached
**WHEN** a tap's alighting is corrected to another Zone 1 stop
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is audited as a £0.00 free tap
**AND** the day's Zone 1 total stays at the £6.00 cap

### C4102779 · Re-running settlement after a zonal correction adds no charge  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** a Zone 1 tap has been corrected to a Zone 2 stop with the Zone 2 cap reached
**WHEN** the EndOfDay settlement process runs again
**THEN** the corrected tap is still audited at £0.00 with the Zone 2 cap applied
**AND** no additional charge is made to the account

### C4102780 · The zonal cap applies after a correction regardless of transport mode  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** the iLink Zone 2 cap of £11.00 is reached across mixed transport modes
**WHEN** a Zone 1 tap is corrected to a Zone 2 stop
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is audited as a £0.00 free tap under the Zone 2 cap
**AND** the reference cap is not applied regardless of transport mode

### C4102839 · Only stops with a fare greater than zero are shown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 boarding from Newbuildings Primary School
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** every stop shown has a fare greater than zero
**AND** no stop with a blank, zero or negative fare is shown

### C4102840 · Zero-fare transfer stops are not shown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 from a stage with several zero-fare transfer stops
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the zero-fare transfer stops are not shown in the list

### C4102841 · Valid stops with a positive fare are still shown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 from a stage with positive-fare onward stops
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the onward stops with a positive reference fare are shown

### C4102842 · Selecting a valid positive-fare stop updates the journey  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 with the Update Stop list open
**WHEN** the user selects a positive-fare stop and confirms the change
**THEN** the journey's alighting stage is updated to the selected stop
**AND** the journey fare is recalculated for that stop

### C4102843 · A zero-fare stop is hidden but the smallest positive-fare stop is shown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 with a zero-fare stop and a smallest positive-fare stop
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the zero-fare stop is not shown
**AND** the smallest positive-fare stop is shown

### C4102844 · A £0.00 capped journey stays visible and editable  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a journey charged £0.00 because the daily cap was reached
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the journey is still shown in Journey History
**AND** is editable
**AND** the Update Stop list still shows only stops with a fare greater than zero

### C4102845 · A cancelled £0.00 journey stays visible and editable  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a cancelled journey charged £0.00
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the journey is still shown with the cancelled indicator
**AND** is editable
**AND** the Update Stop list still shows only stops with a fare greater than zero

### C4102846 · A transfer journey charged £0.00 stays displayed  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a journey accepted as a transfer and charged £0.00
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the journey is still shown with the transfer icon
**AND** is editable
**AND** the Update Stop list still shows only stops with a fare greater than zero

### C4102847 · A stop with a negative fare is not shown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 with a stop carrying a negative fare
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** no stop with a negative fare is shown

### C4102848 · Transfer stops with a positive fare still appear  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 with positive-fare transfer stops
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the positive-fare transfer stops still appear in the list

### C4102849 · TVM-only stops with a positive fare still appear  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24300
_ABT / Functional / Update Stop List_

**GIVEN** a TOO journey on route 273 with TVM-only stops carrying a positive fare
**WHEN** the user opens the Update Stop list for the journey's alighting stage
**THEN** the positive-fare TVM-only stops still appear in the list
**AND** their exclusion is a known limitation tracked separately

### C4102973 · ExternalInfo/StaffCash API returns staff cash for a date range  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / API_

**GIVEN** the user is authenticated to the API tool
**WHEN** the user sends a GET ExternalInfo/StaffCash request for a single past day, a multi-day past range, or the current day
**THEN** the API returns the staff cash data for the requested period

### C4102974 · ExternalInfo/StaffCash API handles invalid requests and BST/GMT  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / API_

**GIVEN** the user is authenticated to the API tool
**WHEN** the user sends an invalid GET ExternalInfo/StaffCash request, or a request spanning the BST/GMT change
**THEN** an invalid request is rejected with an error
**AND** a BST/GMT request returns the correct staff cash data for the period

### C4103055 · View the Dashboard summary tiles  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Dashboard_

**GIVEN** an operator has configured a Dashboard with summary tiles
**AND** the operator is signed into CloudFare
**WHEN** the operator views the Dashboard
**THEN** each tile shows its metric (hours since last communication, missing transactions, devices by status, recent alerts, ABT users, ABT journeys, ABT revenue, TVM status, quarantine count)

### C4103056 · Create, clone, favourite and delete a dashboard  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Dashboard_

**GIVEN** a user is signed into CloudFare on the dashboard homepage
**WHEN** the user creates, clones, favourites or deletes a dashboard
**THEN** each change is applied to the user's dashboards

### C4103057 · Add and remove dashboard tiles  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Dashboard_

**GIVEN** a user is signed into CloudFare with a dashboard created
**WHEN** the user adds and removes tiles
**THEN** the dashboard reflects the tile changes

### C4103058 · View a dashboard full screen  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Dashboard_

**GIVEN** a dashboard with tiles is displayed
**WHEN** the user selects full screen
**THEN** the dashboard is shown full screen

### C4103031 · Filter the activity log by activity, device, date and time  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Activity Log_

**GIVEN** the All Activities page is displayed with communicated data to filter
**WHEN** the user filters by activity, device, date and time
**THEN** only the activities matching the selected filters are shown

### C4103032 · Page through the activity log  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Activity Log_

**GIVEN** the All Activities page is displayed with more results than one page
**WHEN** the user navigates between pages
**THEN** the next and previous pages of activities are shown

### C4103033 · View transactions, events and staff activity  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Activity Log_

**GIVEN** the All Activities page is displayed with communicated data
**WHEN** the user views transactions, events and staff activity
**THEN** each activity type is shown with its detail

### C4103034 · Filter the activity log by barcode ID  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Estate Management / Activity Log_

**GIVEN** a HHD is commissioned and communicating with CloudFare
**AND** the All Activities page is displayed
**WHEN** the user filters by a validated, printed, failed or invalid barcode ID
**THEN** only the activities matching that barcode ID are shown

### C4103035 · Failed validations and payments appear in the activity log  (6m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Estate Management / Activity Log_

**GIVEN** the All Activities page is displayed with communicated data
**WHEN** the user reviews failed barcode validations, failed ABT taps on an ETM and failed bank-card retail payments
**THEN** each failure is identified in the activity log with its reason

### C4103036 · View and edit device information  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Asset Manager_

**GIVEN** the Device Information page is displayed with a list of existing devices
**WHEN** the user views and edits a device's information
**THEN** the device information is updated

### C4103037 · Disable and enable a device  (4m)  — **DESTRUCTIVE**; cross-check: CloudFare
_CloudFare / Functional / Estate Management / Asset Manager_

**GIVEN** the Device Information page is displayed with a list of existing devices
**WHEN** the user disables a device and later enables it
**THEN** the device's enabled state is updated accordingly

### C4103038 · Quick Product Assignment — add, remove and abandon products  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Asset Manager_

**GIVEN** the Quick Product Assignment page is displayed with the operator level set
**WHEN** the user adds products, removes products, or abandons the changes
**THEN** the product changes are saved
**AND** abandoned changes are discarded

### C4103050 · Navigate the Commands Viewer  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Commands Viewer_

**GIVEN** a user is signed into CloudFare on the Estate Management page
**AND** the Commands Viewer is available to the user
**WHEN** the user opens the Commands Viewer
**THEN** the Commands Viewer page is displayed

### C4103039 · Comms Monitor — recent activity, search, filter and report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Comms Monitor_

**GIVEN** the Comms Monitor page is displayed with a dynamic device list
**WHEN** the user views recent activity and uses search, filter and report
**THEN** the recent activity table updates to the search and filter
**AND** the communications report is produced

### C4103040 · Comms Monitor — change of operating company  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Comms Monitor_

**GIVEN** the Comms Monitor page is displayed
**WHEN** the operating company of a device changes
**THEN** the Comms Monitor reflects the new operating company

### C4103041 · Create and modify a device dataset version  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Device Dataset Deployment_

**GIVEN** the Device Datasets page is displayed with existing versions
**WHEN** the user creates a new dataset version and modifies its details
**THEN** the dataset version is saved with the modified details

### C4103042 · Upload and configure device software  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Device Dataset Deployment_

**GIVEN** the Device Dataset Deployment software distribution page is displayed
**WHEN** the user uploads a new software version and configures its parameters
**THEN** the software version is uploaded with the configured parameters

### C4103043 · Manage device dataset version state and deployment  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Device Dataset Deployment_

**GIVEN** the Device Datasets page is displayed with a valid dataset version
**WHEN** the user changes the version state and deploys it
**THEN** the version state is updated
**AND** the dataset is deployed to the target devices

### C4103048 · Filter quarantined data by device  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Quarantined Data_

**GIVEN** the user is on the Quarantined Data section under Estate Management
**WHEN** the user filters the quarantined data by device
**THEN** only the quarantined data for that device is shown

### C4103049 · Edit and resubmit quarantined data  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Quarantined Data_

**GIVEN** there is quarantined data in the table
**WHEN** the user edits a quarantined record and submits it
**THEN** the corrected record is resubmitted for processing

### C4103044 · Add, modify and disable a staff member  (4m)  — **DESTRUCTIVE**; cross-check: CloudFare
_CloudFare / Functional / Estate Management / Staff Manager_

**GIVEN** the Staff Manager page is displayed with a list of existing staff
**WHEN** the user adds a new staff member, modifies their details, or disables them
**THEN** each change is saved against the staff record

### C4103045 · Modify a staff member's PIN  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Staff Manager_

**GIVEN** the Staff Manager page is displayed with an existing staff member
**WHEN** the user modifies the staff member's PIN
**THEN** the new PIN is saved against the staff record

### C4103046 · Modify a staff member's home and working location  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Staff Manager_

**GIVEN** the Staff Manager page is displayed with an existing staff member
**WHEN** the user modifies the staff member's home and working locations
**THEN** the updated locations are saved against the staff record

### C4103047 · View staff history  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Estate Management / Staff Manager_

**GIVEN** the Staff Manager module is available to the user
**WHEN** the user views a staff member's history
**THEN** the staff history is displayed

### C4103059 · Create, view, edit and delete an alert configuration  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Events & Alerts_

**GIVEN** the Alert Configuration page is displayed under Events & Alerts
**WHEN** the user creates, views, edits or deletes an alert
**THEN** each change is applied to the alert configuration

### C4103060 · Alert Viewer — filter, acknowledge and clear alerts  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Events & Alerts_

**GIVEN** the Alert Viewer page is displayed with alerts
**WHEN** the user filters the list and acknowledges or clears an alert, with or without a note
**THEN** the alert status is updated to acknowledged or cleared
**AND** any note is recorded against the alert

### C4103061 · Configure event groups  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Events & Alerts_

**GIVEN** the Event Group Configuration page is displayed under Events & Alerts
**WHEN** the user adds, modifies or deletes an event group
**THEN** each change is applied to the event groups

### C4103062 · Events Viewer — filter the events list  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Events & Alerts_

**GIVEN** the Event Viewer page is displayed under Events & Alerts
**WHEN** the user filters the events list by its adjustable fields
**THEN** only the events matching the filters are shown

### C4103063 · Run the Depot Location Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Assets sub-page with audit data processed
**WHEN** the user runs the Depot Location Report
**THEN** the Depot Location Report is generated
**AND** the report can be exported

### C4103064 · Run the Devices Last Seen Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Assets sub-page with audit data processed
**WHEN** the user runs the Devices Last Seen Report
**THEN** the Devices Last Seen Report is generated
**AND** the report can be exported

### C4103065 · Run the Software Versions Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Assets sub-page with audit data processed
**WHEN** the user runs the Software Versions Report
**THEN** the Software Versions Report is generated
**AND** the report can be exported

### C4103066 · Run the Staff Activity Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Assets sub-page with audit data processed
**WHEN** the user runs the Staff Activity Report
**THEN** the Staff Activity Report is generated
**AND** the report can be exported

### C4103067 · Run the Engineer Visits Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Staff sub-page with audit data processed
**WHEN** the user runs the Engineer Visits Report for a TVM, PV or GV
**THEN** the Engineer Visits Report is generated for the selected device type
**AND** the report can be exported

### C4103068 · Run the Revenue Inspector's Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Staff sub-page with audit data processed
**WHEN** the user runs the Revenue Inspector's Report, including for the BRT operator level
**THEN** the Revenue Inspector's Report is generated
**AND** the report can be exported

### C4103069 · Run the TVM cash collection reports  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Cash sub-page with audit data processed
**WHEN** the user runs a TVM cash collection report (total coins and notes from vaults, coin refloat and residual hopper total, float balances by hopper and vault, coin acceptance recycling, no change available, almost full exceptions)
**THEN** the selected cash collection report is generated
**AND** the report can be exported

### C4103070 · Run the TVM cash revenue reports  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Cash sub-page with audit data processed
**WHEN** the user runs a cash revenue report (cash ticket sales revenue, change to customer, summary totals by driver)
**THEN** the selected cash revenue report is generated
**AND** the report can be exported

### C4103071 · Run the Rules List Export  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Topology sub-page
**WHEN** the user runs the Rules List Export
**THEN** the Rules List Export is generated
**AND** the report can be exported

### C4103072 · Run the Concise Area & Reference Fare Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Topology sub-page
**WHEN** the user runs the Concise Area & Reference Fare Report
**THEN** the report is generated
**AND** the report can be exported

### C4103073 · Run the Route List Export  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Topology sub-page
**WHEN** the user runs the Route List Export
**THEN** the Route List Export is generated
**AND** the report can be exported

### C4103074 · Run the Product to Ticket Assignment Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Topology sub-page
**WHEN** the user runs the Product to Ticket Assignment Report
**THEN** the report is generated
**AND** the report can be exported

### C4103075 · Run the Product List Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Topology sub-page
**WHEN** the user runs the Product List Report
**THEN** the Product List Report is generated
**AND** the report can be exported

### C4103076 · Run the Events & Alerts Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Events & Alerts sub-page with audit data processed
**WHEN** the user runs the Events & Alerts Report
**THEN** the report is generated
**AND** the report can be exported

### C4103077 · Run the Vehicle Check Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** a user is on the Reports Events & Alerts sub-page with audit data processed
**WHEN** the user runs the Vehicle Check Report
**THEN** the Vehicle Check Report is generated
**AND** the report can be exported

### C4103078 · Run the CloudFare Usage Report  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** user actions have been performed on the environment
**AND** the CloudFare Reporting module is displayed
**WHEN** the user runs, filters and downloads the CloudFare Usage Report
**THEN** the report shows the audited user actions for the filter
**AND** the report can be downloaded

### C4103079 · Run the Reports end-to-end flow  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Reports_

**GIVEN** device audit data has been generated and processed by CloudFare
**WHEN** the user runs the corresponding report
**THEN** the report reflects the processed audit data end to end

### C4102963 · Configure report access for a role  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Roles & Profiles_

**GIVEN** an administrator is signed into CloudFare
**WHEN** the administrator sets the report access for a role, including specific report access
**THEN** the role can access only the permitted reports

### C4102964 · Configure module and group access for a role  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Roles & Profiles_

**GIVEN** an administrator is signed into CloudFare
**WHEN** the administrator sets the group access and module access (Passenger Journey, Revenue Reporting, System Mining Tool) for a role
**THEN** the role can access only the permitted groups and modules

### C4102965 · Navigate the Settings menu  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare with the Dashboard displayed
**WHEN** the user opens Settings and selects each option
**THEN** each Settings page opens

### C4102966 · Event Codes — view, add, edit and import  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the Event Codes page
**WHEN** the user selects an event code, edits it, adds a new one, or imports codes
**THEN** the event codes table reflects each change

### C4102967 · Operating Units — add, edit and delete  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare in Settings
**WHEN** the user adds, edits or deletes an operating unit
**THEN** the operating units list reflects each change

### C4102968 · Scheduled Tasks — enable and disable purges  (4m)  — **DESTRUCTIVE**; cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the Scheduled Tasks settings page
**WHEN** the user enables or disables purges for successful quarantine messages, events and alerts, or communications data
**THEN** the purge schedule for that data type is updated accordingly

### C4102969 · System Settings — edit values, VAT and feature toggles  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the System Settings page
**WHEN** the user edits a system setting value, adds a VAT value, or changes a feature toggle
**THEN** the system setting is saved with the new value

### C4102970 · Notifications — edit a value  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the Notifications settings page
**WHEN** the user edits a notifications value
**THEN** the notifications value is saved

### C4102971 · External Interface Settings — edit  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the External Interface Settings page
**WHEN** the user edits an external interface setting
**THEN** the setting is saved

### C4102972 · Scheduled Adherence — edit  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Settings_

**GIVEN** a user is signed into CloudFare on the Scheduled Adherence settings page
**WHEN** the user edits a scheduled adherence threshold
**THEN** the threshold is saved

### C4102960 · Sign on with username and password  (6m)  — cross-check: CloudFare
_CloudFare / Functional / Sign On & Access_

**GIVEN** the CloudFare sign-on page is displayed
**WHEN** the user signs on with a valid username and password
**THEN** the user is signed in
**AND** the Dashboard is displayed

### C4102961 · Sign on with a Google account  (6m)  — cross-check: CloudFare
_CloudFare / Functional / Sign On & Access_

**GIVEN** the CloudFare sign-on page is displayed
**AND** the user's Google account is authorised for the current environment
**WHEN** the user signs on with their Google account
**THEN** the user is signed in
**AND** the Dashboard is displayed

### C4102962 · Sign off  (6m)  — cross-check: CloudFare
_CloudFare / Functional / Sign On & Access_

**GIVEN** a user is signed into CloudFare
**WHEN** the user signs off using the sign-off button or the back button
**THEN** the session ends
**AND** the sign-on page is shown

### C4103088 · Create a rail line and station  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Station Manager_

**GIVEN** a user is on the Station Management Network View page
**WHEN** the user adds a new rail line and creates a station
**THEN** the rail line and station are added to the network

### C4103089 · Delete or change a station  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Station Manager_

**GIVEN** a user is on the Station Management Network View page
**WHEN** the user deletes or changes a station
**THEN** the change is applied to the network

### C4103090 · Add a branch  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Station Manager_

**GIVEN** a user is on the Station Management Network View page
**WHEN** the user adds a branch
**THEN** the branch is added to the network

### C4103080 · Create, edit and copy a ticket layout  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user is signed into CloudFare with the Ticket Editor available
**WHEN** the user creates, edits or copies a ticket layout
**THEN** each change is saved to the ticket layout

### C4103081 · Add ticket elements to a template  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a ticket template is loaded in the Ticket Editor preview
**WHEN** the user adds ticket elements
**THEN** the elements are added to the template

### C4103082 · Configure a ticket for different devices  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user is in the Ticket Editor
**WHEN** the user configures a ticket for different device types
**THEN** the ticket layout is saved per device type

### C4103083 · Configure a change ticket  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user is in the Ticket Editor
**WHEN** the user configures a change ticket
**THEN** the change ticket configuration is saved

### C4103084 · Configure a product on a ticket  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user is in the Ticket Editor
**WHEN** the user configures a product on a ticket
**THEN** the product configuration is saved to the ticket

### C4103085 · Group a set of ticket layouts  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user is in the Ticket Editor with ticket layouts available
**WHEN** the user groups a set of ticket layouts
**THEN** the ticket layout group is saved

### C4103086 · Add a barcode to a ticket  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user has access to the Ticket Editor in CloudFare
**WHEN** the user adds a barcode to a ticket
**THEN** the barcode is added to the ticket layout

### C4103087 · Configure payment-card fields on a ticket  (6m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Ticket Editor_

**GIVEN** a user has access to the Ticket Editor in CloudFare
**WHEN** the user adds the payment-card fields to a ticket (unique reference number, obfuscated card number, printed serial number, card start date, expiry date)
**THEN** each payment-card field is added to the ticket layout

### C4103010 · Card Reference File validates alighting stages across devices  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Card Reference File_

**GIVEN** the latest Card Reference File is implemented on a commissioned ETM, POS, PV and HHD
**WHEN** the device uses the Card Reference File to check alighting stages
**THEN** the correct alighting stages are provided on each device

### C4102981 · Add a new map point  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Drawing Tool_

**GIVEN** a user is on the Topology & Fares Management Drawing Tool
**WHEN** the user adds a new map point, including a linked stop
**THEN** the map point is created
**AND** it is shown on the map

### C4102982 · Create, edit and delete a zone  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Drawing Tool_

**GIVEN** a user is on the Topology & Fares Management Drawing Tool
**WHEN** the user creates, edits and deletes a zone
**THEN** each change is applied to the zone
**AND** a smaller zone is layered above a larger overlaid zone so it stays accessible

### C4102983 · Configure positional points on a route  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Drawing Tool_

**GIVEN** a user has selected an existing route and zoomed into the map
**WHEN** the user configures positional points on the route
**THEN** the positional points are saved to the route

### C4102984 · Export and edit map points via file  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Drawing Tool_

**GIVEN** a user is on the Topology & Fares Management Drawing Tool
**WHEN** the user exports the map points to CSV, edits the file and re-imports it
**THEN** the edited map points are updated in CloudFare

### C4102985 · Search for a map point  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Drawing Tool_

**GIVEN** a user is on the Topology & Fares Management Drawing Tool
**WHEN** the user searches for a map point
**THEN** the matching map point is located on the map

### C4103011 · Label configuration data  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Labeling & Publishing_

**GIVEN** a user is on the Topology & Fares page with prepared configuration data
**WHEN** the user labels the configuration data
**THEN** the configuration data is labelled

### C4103012 · Publish configuration with a future transition date  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Labeling & Publishing_

**GIVEN** a user is on the Topology & Fares page with labelled configuration data
**WHEN** the administrator publishes the configuration with a future transition date and time
**THEN** the configuration is published
**AND** devices transition from current to future fares at the set date and time

### C4103013 · Publish an old configuration  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Labeling & Publishing_

**GIVEN** a user is on the Topology & Fares page with appropriate configuration data prepared
**WHEN** the user publishes an older configuration
**THEN** the older configuration is published

### C4103014 · Delete a topology label  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Labeling & Publishing_

**GIVEN** an active published topology label exists on the environment
**WHEN** the user deletes the topology label
**THEN** the topology label is deleted

### C4102992 · Configure a product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user configures a product
**THEN** the product is saved with its configuration

### C4102993 · Configure an ABT product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user configures an ABT product
**THEN** the ABT product is saved with its configuration

### C4102994 · Configure an Open product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures an Open product
**THEN** the Open product is saved with its configuration

### C4102995 · Configure a FLU product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures a FLU product
**THEN** the FLU product is saved with its configuration

### C4102996 · Configure a Preset Reverse FLU product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures a preset reverse FLU product
**THEN** the product is saved with its configuration

### C4102997 · Configure a Reference Type product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures a reference type product
**THEN** the product is saved with its configuration

### C4102998 · Configure an Excess product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures an excess product
**THEN** the excess product is saved with its configuration

### C4102999 · Configure a Smartcard product  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the CloudFare Topology Management page with an operator selected
**WHEN** the user configures a smartcard product, including the WTS SmartRecharge and SmartCreate variants
**THEN** the smartcard product is saved with its configuration

### C4103000 · Configure a Barcode product  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user configures barcode printing for a paper ticket product
**THEN** the barcode product setting is saved

### C4103001 · Configure the alighting stage for a product  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user has selected fares for a product on the Topology & Fares Management screen
**WHEN** the user configures the alighting stage for the product
**THEN** the alighting stage is saved to the product

### C4103002 · Configure annulments per device for a product  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a product has been set up and the user is viewing its details
**WHEN** the user configures annulments for the product per device type
**THEN** the annulment settings are saved per device

### C4103003 · Configure the passback period for a product  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is viewing a product on the Topology & Fares Management screen
**WHEN** the user configures the passback period for the product
**THEN** the passback period is saved to the product

### C4103004 · Configure device keyboard buttons for products  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user adds, removes or toggles product keyboard buttons for a device
**THEN** the device keyboard button configuration is saved

### C4103005 · Create and edit a FLU product group  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with toggle groups created
**WHEN** the user creates or edits a FLU group for a device type (ETM, POS, HHD or TVM)
**THEN** the FLU group is saved for that device

### C4103006 · Set a product assignment expiry  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Products_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user sets the expiry of a product assignment
**THEN** the product assignment expiry is saved

### C4102986 · Create, amend, copy and delete a route  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user is on the Topology & Fares Management page
**WHEN** the user creates, amends, copies or deletes a route
**THEN** each change is applied to the route list
**AND** a copied route retains its assigned fare area

### C4102987 · Configure a route's service code and operator  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user has selected an operator and service on the Topology & Fares Management page
**WHEN** the user sets the service code and assigns the operator
**THEN** the route is saved with the service code and operator

### C4102988 · Enable ABT flat fare on a route  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user has selected a route on the Topology & Fares Management page
**WHEN** the user enables ABT flat fare on the route
**THEN** the route is configured for ABT flat-fare travel

### C4102989 · Enable transfers and set the transfer time on a route  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user has selected an operator and service
**WHEN** the user enables transfers on the route and sets the transfer time in minutes
**THEN** transfers are enabled on the route
**AND** a transfer within the configured time retrieves the correct fare

### C4102990 · Configure a route's fares triangle and calculate a fare  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user has selected an operator and service
**WHEN** the user configures the fares triangle, creates a new fare area and calculates a fare
**THEN** the fares triangle is saved
**AND** the calculated fare matches the configured fare area

### C4102991 · Configure an ETM rail substitute route  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Route Management_

**GIVEN** a user has selected an ETM operator and created a rail replacement service
**WHEN** the user configures the rail substitute route
**THEN** the ETM rail substitute route is saved

### C4103007 · Add a fares rule  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Rules_

**GIVEN** a user is on the Topology & Fares Management page
**WHEN** the user adds a new fares rule
**THEN** the rule is saved

### C4103008 · Configure an e-Purse single fares charge rule  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Rules_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user configures an e-Purse single fares charge rule
**THEN** the rule is saved
**AND** it is applied to e-Purse single fares

### C4103009 · Configure a fixed fare rule  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Rules_

**GIVEN** a user is on the Topology & Fares Management screen with an operator selected
**WHEN** the user configures a fixed fare rule, including a smartcard fixed fare
**THEN** the fixed fare rule is saved
**AND** it is applied

### C4102976 · Navigate the Topology & Fares Management menu  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Setup & Import_

**GIVEN** a user is signed into CloudFare with the Dashboard displayed
**WHEN** the user opens Topology & Fares Management and selects each option
**THEN** each Topology & Fares page opens

### C4102977 · Filter topology by operator  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Setup & Import_

**GIVEN** a user is on the Topology & Fares Management page
**WHEN** the user filters by a selected operator
**THEN** only that operator's services and routes are shown

### C4102978 · Export fares  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Setup & Import_

**GIVEN** a user is on the Topology & Fares Management page with fares to export
**WHEN** the user exports the fares for a selected operator
**THEN** the fares are exported

### C4102979 · Import a map point file (CSV)  (4m)  — PARTIAL; cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Setup & Import_

**GIVEN** a user is on the Topology & Fares Management page
**WHEN** the user imports a map point CSV file
**THEN** stops not already present are added
**AND** existing stops are updated from the file

### C4102980 · Import route data at parent and child level  (4m)  — cross-check: CloudFare
_CloudFare / Functional / Topology & Fares / Setup & Import_

**GIVEN** a user is on the Topology & Fares Management page with an operator selected
**WHEN** the user imports route data at parent level and at child operator level
**THEN** the route data is imported at the selected level

### C4103093 · Date Editor — period, roll-over time and start of week  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Date Editor
**WHEN** the administrator edits the period, roll-over time and start of week
**THEN** the date settings are saved

### C4103094 · Timeband Editor  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Timeband Editor
**WHEN** the administrator configures a timeband
**THEN** the timeband is saved

### C4103095 · Staff Editor  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Staff Editor
**WHEN** the administrator edits a staff member's details and operator details
**THEN** the staff details are saved

### C4103096 · Class Type and Class Group Editors  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Class Type and Class Group Editors
**WHEN** the administrator edits class types and class groups, assigning a product class to more than one group
**THEN** the class type and class group settings are saved

### C4103097 · Location, Location Group and Location Restrictions Editors  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Location editors
**WHEN** the administrator edits a location, a location group and location restrictions
**THEN** the location settings are saved

### C4103098 · Route Group Editor  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Route Group Editor
**WHEN** the administrator edits a route group, assigning a route to more than one group
**THEN** the route group settings are saved

### C4103099 · Route Revenue Editor  (4m)  — cross-check: MERIT
_Merit / Functional / Administration_

**GIVEN** an administrator is in the Merit Route Revenue Editor
**WHEN** the administrator configures pass revenue, generation factor, and rail and BRT mileage and journey allocation
**THEN** the route revenue settings are saved

### C4103100 · Sales Breakdown reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs a Sales Breakdown report (by driver, class, value, value/location or route/class)
**THEN** the selected Sales Breakdown report is generated
**AND** the report can be exported

### C4103101 · Sales Analysis by Class report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Sales Analysis by Class report
**THEN** the report is generated
**AND** the report can be exported

### C4103102 · Origin and Destination reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs an Origin, Destination or Origin/Destination report (by class, direction of travel, rail or mileage)
**THEN** the selected report is generated
**AND** the report can be exported

### C4103103 · Bus Loading by Route/Journey report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Bus Loading by Route/Journey report, including by direction of travel
**THEN** the report is generated
**AND** the report can be exported

### C4103104 · Route/Stage reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Route/Stage report or the Route/Stage Analysis Detailed report
**THEN** the report is generated
**AND** the report can be exported

### C4103105 · Journey Analysis reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Journey Analysis or Journey Analysis Detailed report, including by direction of travel
**THEN** the report is generated
**AND** the report can be exported

### C4103106 · Stage Timeband report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Stage Timeband report, including by direction of travel
**THEN** the report is generated
**AND** the report can be exported

### C4103107 · Patronage Timeband report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Patronage Timeband report
**THEN** the report is generated
**AND** the report can be exported

### C4103108 · Revenue and Revenue by Stop reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Revenue report or the Revenue by Stop report
**THEN** the report is generated
**AND** the report can be exported

### C4103109 · Class Breakdown and Route Breakdown reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs a Class Breakdown or Route Breakdown report (including by device or by class group)
**THEN** the selected report is generated
**AND** the report can be exported

### C4103110 · POS Revenue report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the POS Revenue report
**THEN** the report is generated
**AND** the report can be exported

### C4103111 · Duty Comparison and Driver Shift reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Duty Comparison report or the Driver Shift report
**THEN** the report is generated
**AND** the report can be exported

### C4103112 · Bus Serviceability Final Defects report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Bus Serviceability Final Defects report
**THEN** the report is generated
**AND** the report can be exported

### C4103113 · GPS reports  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the GPS report or a GPS Stage Change Failure report (by bus, by stage or detailed)
**THEN** the selected report is generated
**AND** the report can be exported

### C4103114 · Route Purchase report  (4m)  — cross-check: MERIT
_Merit / Functional / Analysis Reports_

**GIVEN** an administrator is on the Merit Analysis Reports with audit data processed
**WHEN** the administrator runs the Route Purchase report
**THEN** the report is generated
**AND** the report can be exported

### C4103125 · Revenue Foregone reports  (4m)  — cross-check: MERIT
_Merit / Functional / Concessionary Reports_

**GIVEN** an administrator is on the Merit Concessionary Reports with audit data processed
**WHEN** the administrator runs a Revenue Foregone report (by group and class, by operator by eligible route, or detailed)
**THEN** the selected report is generated
**AND** the report can be exported

### C4103126 · Concessionary Class Summary reports  (4m)  — cross-check: MERIT
_Merit / Functional / Concessionary Reports_

**GIVEN** an administrator is on the Merit Concessionary Reports with audit data processed
**WHEN** the administrator runs a Concessionary Class Summary report
**THEN** the selected report is generated
**AND** the report can be exported

### C4103127 · ENTCS Passenger and Revenue reports  (4m)  — cross-check: MERIT
_Merit / Functional / Concessionary Reports_

**GIVEN** an administrator is on the Merit Concessionary Reports with audit data processed
**WHEN** the administrator runs an ENTCS Passenger, ENTCS Revenue or ENTCS Revenue Foregone report
**THEN** the selected report is generated
**AND** the report can be exported

### C4103128 · Fare Foregone reports  (4m)  — cross-check: MERIT
_Merit / Functional / Concessionary Reports_

**GIVEN** an administrator is on the Merit Concessionary Reports with audit data processed
**WHEN** the administrator runs the Fare Foregone Summary report or the Fare Foregone by Fare Band report
**THEN** the report is generated
**AND** the report can be exported

### C4103129 · Daily Summary report  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Daily Summary report
**THEN** the report is generated
**AND** the report can be exported

### C4103130 · Daily Audit reports  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Daily Audit report or the Daily Audit by Module report
**THEN** the report is generated
**AND** the report can be exported

### C4103131 · Class Audit and Route Audit reports  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Class Audit report or the Route Audit report in summary or detailed form
**THEN** the selected report is generated
**AND** the report can be exported

### C4103132 · Annulled Tickets report  (4m)  — PARTIAL; cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Annulled Tickets report
**THEN** the report is generated
**AND** the report can be exported

### C4103133 · Inspectors report  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Inspectors report
**THEN** the report is generated
**AND** the report can be exported

### C4103134 · Outstanding Duties report  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Outstanding Duties report
**THEN** the report is generated
**AND** the report can be exported

### C4103135 · Stage List report  (4m)  — cross-check: MERIT
_Merit / Functional / Daily Reports_

**GIVEN** an administrator is on the Merit Daily Reports with audit data processed
**WHEN** the administrator runs the Stage List report
**THEN** the report is generated
**AND** the report can be exported

### C4103136 · Origin and Destination Distance reports  (4m)  — cross-check: MERIT
_Merit / Functional / Distance Reports_

**GIVEN** an administrator is on the Merit Distance Reports with audit data processed
**WHEN** the administrator runs an Origin and Destination Distance report (including by class or direction of travel)
**THEN** the selected report is generated
**AND** the report can be exported

### C4103137 · Route Distance Analysis report  (4m)  — cross-check: MERIT
_Merit / Functional / Distance Reports_

**GIVEN** an administrator is on the Merit Distance Reports with audit data processed
**WHEN** the administrator runs the Route Distance Analysis report
**THEN** the report is generated
**AND** the report can be exported

### C4103138 · Ulsterbus revenue stored procedures  (6m)  — PARTIAL; cross-check: MERIT
_Merit / Functional / Stored Procedures_

**GIVEN** Merit has processed Ulsterbus audit data
**WHEN** the Ulsterbus bus revenue stored procedures are run, including by payment type and operational payment type
**THEN** the stored procedures return the correct Ulsterbus revenue

### C4103139 · Metro revenue stored procedures  (6m)  — PARTIAL; cross-check: MERIT
_Merit / Functional / Stored Procedures_

**GIVEN** Merit has processed Metro audit data
**WHEN** the Metro bus revenue stored procedures are run, including by payment type and operational payment type
**THEN** the stored procedures return the correct Metro revenue

### C4103140 · NIR rail revenue stored procedures  (6m)  — PARTIAL; cross-check: MERIT
_Merit / Functional / Stored Procedures_

**GIVEN** Merit has processed NIR rail audit data
**WHEN** the NIR rail revenue stored procedures are run, including by payment type and operational payment type
**THEN** the stored procedures return the correct NIR rail revenue

### C4103141 · Synchronise staff into Merit  (4m)  — **DESTRUCTIVE**; cross-check: MERIT
_Merit / Functional / Synchronisation & Tools_

**GIVEN** staff records exist in CloudFare
**WHEN** staff are added, modified, disabled, have their ID or locations changed, or are imported via Import Staff
**THEN** the corresponding staff changes are synchronised into Merit

### C4103142 · Browse audit data with Client Tools  (4m)  — cross-check: MERIT
_Merit / Functional / Synchronisation & Tools_

**GIVEN** a user has the Merit Client Tools available
**WHEN** the user browses the audit data
**THEN** the audit data is displayed

### C4103143 · View the available reports in the Merit Web Reporter  (4m)  — cross-check: MERIT
_Merit Web Reporter / Functional / Report Viewer_

**GIVEN** a user is signed into the Merit Web Reporter
**WHEN** the user views the available reports
**THEN** the list of available reports is displayed

### C4103160 · View and search card data  (1m)  — PARTIAL
_Smartrack / Functional / Card Data_

**GIVEN** a user is signed into Smartrack on the Display Card Data page
**WHEN** the user searches by customer name and address, ESN and PSN, or card type
**THEN** the matching single or multiple cards are displayed

### C4103161 · Add notes and attached files to a card  (1m)  — PARTIAL
_Smartrack / Functional / Card Data_

**GIVEN** a user has selected a card in Smartrack
**WHEN** the user adds notes and attaches files
**THEN** the notes and attached files are saved against the card
**AND** they can be viewed

### C4103162 · View card transactions  (1m)  — PARTIAL
_Smartrack / Functional / Card Data_

**GIVEN** a user has selected a card in Smartrack
**WHEN** the user views the card transactions for an adult or child Ulsterbus Multi-Journey or Town Service product
**THEN** the card transactions are displayed for the selected product and passenger type

### C4103163 · Import a card issue and pass-create record file  (3m)  — PARTIAL
_Smartrack / Functional / Import & Export_

**GIVEN** a user is signed into Smartrack
**WHEN** the user imports a CSV issue and pass-create record file
**THEN** the records are imported into Smartrack

### C4103167 · Run the Default Payment report  (3m)  — PARTIAL
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Default Payment report
**THEN** the report is generated
**AND** the report can be exported

### C4103169 · Run the Refund report  (1m)
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Refund report
**THEN** the report is generated
**AND** the report can be exported

### C4103170 · Run the Decommission Card report  (1m)  — PARTIAL
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Decommission Card report
**THEN** the report is generated
**AND** the report can be exported

### C4103171 · Run the POS Revenue Analysis report  (1m)
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the POS Revenue Analysis report
**THEN** the report is generated
**AND** the report can be exported


## Priority: Normal

### C4102954 · Add new decline reasons  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Configuration & Setup_

**GIVEN** declined card taps have occurred for expired, authenticity-failed, BIN-listed and Deny-listed cards
**WHEN** the operator views the Declined Taps Report
**THEN** each decline reason is recorded against its tap

### C4102817 · Later taps including an out-of-order timestamp are flagged duplicates  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap and a same-stage retail transaction
**WHEN** two further same-stage taps are made, one timestamped before the original
**AND** the EndOfDay settlement runs
**THEN** both later taps are flagged duplicates at £0.00
**AND** both are recorded against the original tap

### C4102820 · A same-stage tap outside the duplicate window is not a duplicate  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap and a same-stage retail transaction
**WHEN** a second same-stage tap is made more than 15 minutes after the original
**AND** the EndOfDay settlement runs
**THEN** the second tap is not flagged as a duplicate
**AND** it is charged as the second tap of the day

### C4102822 · A later tap from a different boarding stage is a genuine new tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24258
_ABT / Functional / Duplicate Detection_

**GIVEN** a Metro tap and a same-stage retail transaction
**WHEN** a second tap is made from a different boarding stage
**AND** the EndOfDay settlement runs
**THEN** the second tap is not flagged as a duplicate
**AND** it is charged as the second tap of the day

### C4102823 · A cancelled journey remains visible in Journey History  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a Metro tap that has been cancelled
**WHEN** the EndOfDay settlement runs
**THEN** Journey History shows a single journey for that tap
**AND** it is marked as cancelled with the "**" indicator

### C4102825 · Editing the alighting stop on a cancelled tap keeps the journey visible  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a cancelled Metro tap
**WHEN** its alighting stop is corrected
**AND** the EndOfDay settlement runs
**THEN** Journey History shows a single journey with the corrected stop
**AND** it is still marked as cancelled with the "**" indicator

### C4102828 · A cancelled journey stays cancelled after a stop correction and further settlement  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a cancelled Metro tap whose alighting stop has been corrected
**WHEN** a further EndOfDay settlement runs
**THEN** the journey is still marked as cancelled
**AND** it remains visible in Journey History with the "**" indicator

### C4102829 · Cancelling one journey does not affect other visible journeys  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** two Metro journeys on the same day
**WHEN** one journey is cancelled
**AND** the EndOfDay settlement runs
**THEN** Journey History shows the cancelled journey marked cancelled
**AND** the other journey is shown as not cancelled

### C4102832 · A cancelled transfer journey remains visible  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24061
_ABT / Functional / Journey History_

**GIVEN** a Metro transfer leg charged £0.00 with a non-zero initial fare, then cancelled
**WHEN** the EndOfDay settlement runs
**THEN** Journey History shows a single cancelled transfer journey
**AND** it is marked as cancelled with the "**" indicator

### C4102835 · Both settled ref.60 taps from the same stage populate the dropdown  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** two settled TOO ref.60 taps on route 72b from the same boarding stage
**WHEN** the user opens the Update Stop list for each tap
**THEN** each dropdown is populated with the onward stops
**AND** neither shows "No options"

### C4102836 · Re-opening the Update Stop modal always populates the dropdown  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** a settled TOO journey on route 72b
**WHEN** the user opens, closes and re-opens the Update Stop modal several times
**THEN** the dropdown shows the onward stops on every open
**AND** it never shows "No options"

### C4102838 · The correct operator returns stops; a mismatched operator returns none  (4m)  — cross-check: CloudFare / MERIT; refs: TODEV-24397
_ABT / Functional / Journey History_

**GIVEN** a settled TOO journey on route 72b from Greys Farm
**WHEN** the Update Stop list is opened using the journey's correct operator
**THEN** the dropdown is populated with the onward stops and does not show "No options"
**AND** using a mismatched operator id returns no stops as user error

### C4102879 · Configure the maximum late data period  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Administrator Settings_

**GIVEN** an administrator is signed into the Operator Portal
**WHEN** the administrator sets the maximum late data period
**THEN** late tap data is processed according to that period

### C4102880 · Configure the maximum journey duration  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Administrator Settings_

**GIVEN** an administrator wants to configure the maximum journey duration
**WHEN** the administrator sets the maximum journey duration
**THEN** the duration is used to determine when a journey is treated as incomplete

### C4102868 · Corrupt tap messages are rejected and quarantined  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customer Services_

**GIVEN** a device is registered with CloudFare-ABT
**WHEN** a corrupt tap message is received from the device
**THEN** the journey tap service rejects the tap and places it in the quarantine queue
**AND** it is flagged so it can be processed

### C4102861 · View and export a customer's Journey History  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** a customer has performed tap journeys on a registered device
**AND** the operator has selected the customer's card account
**WHEN** the operator opens Journey History and applies filters
**THEN** the tap/journey details are displayed
**AND** paging and show-more detail are available
**AND** the journey history can be exported

### C4102864 · Aftercare — operator queries and comments  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** an operator has selected a customer account with aftercare available
**WHEN** the operator submits, comments on, or cancels an aftercare query
**THEN** the query, comment or cancellation is recorded against the account
**AND** the aftercare list can be paged

### C4102866 · Authorisations — accept all and reject all  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Customers_

**GIVEN** the approver is on the Authorisations page with pending requests
**WHEN** the approver selects Authorise All or Reject All
**THEN** all pending requests are actioned accordingly

### C4102883 · Run the Account Status Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Account Status Report for a date range
**THEN** the Account Status Report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102884 · Run the Action List Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Action List Report
**THEN** the Action List Report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102885 · Run the Action List — Negative List Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Action List Negative List Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102886 · Run the Aftercare Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Aftercare Report
**THEN** the Aftercare Report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102888 · Run the Authorisation Failures Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Authorisation Failures Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102889 · Run the Cancelled Tap Report  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Cancelled Tap Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102890 · Run the Debt Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Debt Report
**THEN** the Debt Report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102891 · Run the Declined Taps Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Declined Taps Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102893 · Run the Duplicate Taps Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Duplicate Taps Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102895 · Run the ePurse Balance Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the ePurse Balance Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102896 · Run the Exception Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Exception Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102899 · Run the Initial Taps by Brand Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Initial Taps by Brand Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102900 · Run the Inspection Details Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Inspection Details Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102901 · Run the Journey Summary Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Journey Summary Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102903 · Run the Journeys by Service/Route Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Journeys by Service/Route Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102904 · Run the Late Taps Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Late Taps Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102905 · Run the Lost Tap Data Report  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Lost Tap Data Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102906 · Run the PSP Technical Errors Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the PSP Technical Errors Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102908 · Run the Retail Debt Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Retail Debt Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102914 · Run the Shared Liability Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Shared Liability Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102917 · Run the Unique Taps Report  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Operator Web Portal / Reports_

**GIVEN** an operator is signed into the Operator Web Portal
**AND** the Reports page is displayed
**WHEN** the operator runs the Unique Taps Report
**THEN** the report is generated
**AND** it is displayed
**AND** the report can be exported

### C4102936 · Raise a general query  (4m)  — cross-check: CloudFare / MERIT
_ABT / Functional / Passenger Web Portal / Account Functions_

**GIVEN** a customer is signed on and the account home screen is displayed
**WHEN** the customer raises a general query
**THEN** the query is submitted to the operator

### C4102941 · Late taps within the maximum late data period are processed  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Late Taps_

**GIVEN** the maximum late data period is configured to 14 days
**AND** a customer made a transaction tap on a device
**WHEN** the ABT system receives the tap within 14 days of the tap date
**THEN** the tap is processed

### C4102942 · Late taps beyond the maximum late data period are rejected  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Late Taps_

**GIVEN** the maximum late data period is configured to 14 days
**AND** a customer made a transaction tap on a device
**WHEN** the ABT system receives the tap more than 14 days after the tap date
**THEN** the tap is rejected

### C4102944 · Duplicate late taps are disregarded  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_ABT / Functional / Processing Taps / Late Taps_

**GIVEN** a tap has already been processed by the ABT system
**WHEN** the ABT system receives a duplicate of that tap
**THEN** the duplicate tap is disregarded

### C4102763 · A corrected capped tap stays settled and free  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap with a £0.00 capped tap
**WHEN** the alighting stop on the capped tap is corrected
**THEN** the tap is still shown as settled with the cap retained
**AND** it is still charged £0.00 and the day total stays £4.00

### C4102765 · Correcting an unsettled capped tap re-evaluates and stays free  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** three Metro taps where the cap is already reached, before settlement
**WHEN** the alighting stop on the capped tap is corrected
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is charged £0.00
**AND** the day total is £4.00

### C4102766 · A declined journey is not treated as a settled capped tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a declined Metro journey
**WHEN** the alighting stop on the declined journey is corrected
**THEN** the journey is handled as declined, not as a settled capped journey
**AND** no settled-cap charge is produced for it

### C4102767 · Re-running settlement after a correction does not re-charge the capped tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24096
_ABT / Functional / Tap Correction / Metro Daily Cap_

**GIVEN** a Metro day settled at the £4.00 cap with a corrected £0.00 capped tap
**WHEN** the EndOfDay settlement process runs again
**THEN** the capped tap is still charged £0.00 with no additional charge
**AND** the day total stays £4.00 and the tap remains settled

### C4102776 · Correcting into a zone below cap charges toward the zonal cap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TODEV-24348
_ABT / Functional / Tap Correction / Zonal Cap_

**GIVEN** one Zone 2 journey has been made and the £11.00 Zone 2 cap is not yet reached
**WHEN** a Zone 1 tap is corrected to a Zone 2 stop
**AND** the EndOfDay settlement runs
**THEN** the corrected tap is charged toward the Zone 2 cap and never above £11.00
**AND** it is not charged under the reference cap

### C4103159 · Smartrack access rights for administrator and user  (1m)
_Smartrack / Functional / Access_

**GIVEN** administrator and standard user accounts are configured for Smartrack
**WHEN** each user signs into Smartrack
**THEN** the administrator sees the administrative functions
**AND** the standard user sees only the permitted functions

### C4103164 · Export the ESN list  (1m)
_Smartrack / Functional / Import & Export_

**GIVEN** a user is signed into Smartrack
**WHEN** the user exports the ESN list
**THEN** the ESN list is exported

### C4103165 · Run the Action List reports  (1m)
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Active Action List, Inactive Action List or daily action list content report
**THEN** the selected Action List report is generated
**AND** the report can be exported

### C4103166 · Run the Liability and Scheme Liability reports  (1m)
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Liability report in summary or detailed form, or the Scheme Liability report
**THEN** the selected report is generated
**AND** the report can be exported

### C4103168 · Run the Delivery report  (1m)
_Smartrack / Functional / Reports_

**GIVEN** a user is on the Smartrack Reports page
**WHEN** the user runs the Delivery report in summary or detailed form
**THEN** the report is generated
**AND** the report can be exported

