# Alignment audit - suite 30279

- Cases audited: **391**
- Blocking findings: **89**
- Advisory (reviewed-intentional) findings: **208**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 124
- C4103159 | Smartrack access rights for administrator and user
- C4103165 | [UNCONFIRMED] Run the Action List reports (Smartrack)
- C4103166 | [UNCONFIRMED] Run the Liability and Scheme Liability reports (Smartrack)
- C4103167 | [UNCONFIRMED] Run the Default Payment report (Smartrack)
- C4103168 | [UNCONFIRMED] Run the Delivery report (Smartrack)
- C4103169 | [UNCONFIRMED] Run the Refund report (Smartrack)
- C4103170 | [UNCONFIRMED] Run the Decommission Card report (Smartrack)
- C4103171 | [UNCONFIRMED] Run the POS Revenue Analysis report (Smartrack)
- C4103143 | View the available reports in the Merit Web Reporter
- C4103144 | View and export a report in the Merit Web Reporter
- C4103102 | [UNCONFIRMED] Origin and Destination reports
- C4103103 | [UNCONFIRMED] Bus Loading by Route/Journey report
- C4103104 | [UNCONFIRMED] Route/Stage reports
- C4103105 | [UNCONFIRMED] Journey Analysis reports
- C4103106 | [UNCONFIRMED] Stage Timeband report
- C4103107 | [UNCONFIRMED] Patronage Timeband report
- C4103108 | [UNCONFIRMED] Revenue and Revenue by Stop reports
- C4103110 | [UNCONFIRMED] POS Revenue report
- C4103112 | [UNCONFIRMED] Bus Serviceability Final Defects report
- C4103113 | [UNCONFIRMED] GPS reports
- C4103114 | [UNCONFIRMED] Route Purchase report
- C4103119 | [UNCONFIRMED] Tickets By Operator report
- C4103120 | [UNCONFIRMED] NIR Revenue Performance reports
- C4103121 | [UNCONFIRMED] NIR Period Trend Analysis reports
- C4103122 | [UNCONFIRMED] BRT Revenue Performance reports
- C4103123 | [UNCONFIRMED] Glider Revenue Performance reports
- C4103124 | [UNCONFIRMED] Ticketing Reports including timebands
- C4103125 | [UNCONFIRMED] Revenue Foregone reports
- C4103126 | [UNCONFIRMED] Concessionary Class Summary reports
- C4103127 | [UNCONFIRMED] ENTCS Passenger and Revenue reports
- C4103128 | [UNCONFIRMED] Fare Foregone reports
- C4103134 | [UNCONFIRMED] Outstanding Duties report
- C4103135 | [UNCONFIRMED] Stage List report
- C4103136 | [UNCONFIRMED] Origin and Destination Distance reports
- C4103137 | [UNCONFIRMED] Route Distance Analysis report
- C4103141 | Synchronise staff into Merit
- C4103142 | Browse audit data with Client Tools
- C4102963 | Configure report access for a role
- C4102964 | Configure module and group access for a role
- C4102973 | ExternalInfo/StaffCash API returns staff cash for a date range
- C4102974 | ExternalInfo/StaffCash API handles invalid requests and BST/GMT
- C4102980 | Import route data at parent and child operator level
- C4103010 | Card Reference File validates alighting stages across devices
- C4103048 | Filter quarantined data by device
- C4103049 | Edit and resubmit quarantined data
- C4103050 | Navigate the Commands Viewer
- C4103056 | [UNCONFIRMED] Create, clone, favourite and delete a dashboard
- C4103057 | [UNCONFIRMED] Add and remove dashboard tiles
- C4103058 | [UNCONFIRMED] View a dashboard full screen
- C4103065 | [UNCONFIRMED] Software Versions Report
- C4103067 | [UNCONFIRMED] Engineer Visits Report
- C4103068 | [UNCONFIRMED] Revenue Inspector's Report
- C4103069 | [UNCONFIRMED] TVM cash collection reports
- C4103070 | [UNCONFIRMED] TVM cash revenue reports
- C4103071 | [UNCONFIRMED] Rules List Export
- C4103072 | [UNCONFIRMED] Concise Area & Reference Fare Report
- C4103073 | [UNCONFIRMED] Route List Export
- C4103074 | [UNCONFIRMED] Product to Ticket Assignment Report
- C4103075 | [UNCONFIRMED] Product List Report
- C4103076 | [UNCONFIRMED] Events & Alerts Report
- C4103077 | [UNCONFIRMED] Vehicle Check Report
- C4103078 | [UNCONFIRMED] CloudFare Usage Report
- C4102791 | Re-tap at the same stage after annulment is the first good tap (Metro)
- C4102792 | Full Metro day reaches the daily cap after an annulment
- C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus)
- C4102794 | Ulsterbus reference fare cap applies on the correct tap after annulment
- C4102795 | Re-tap after annulment in the ref.61 band caps at the ref.61 value
- C4102796 | Annulment in the ref.60 band does not borrow the higher ref.61 cap
- C4102797 | Genuine duplicate without annulment is still rejected as £0.00
- C4102798 | Re-tap at a different stage after annulment is a normal first tap
- C4102799 | Annulling the re-tap as well leaves a later tap as the first good tap
- C4102800 | Annulment processed in the same settlement run as the re-tap
- C4102801 | Annulment with no re-tap leaves no chargeable journey
- C4102802 | Annulling a capped tap does not corrupt the day total
- C4102804 | Annulment on one card does not affect a similar tap on another card
- C4102805 | Ulsterbus re-tap with a different alighting and fare after annulment
- C4102806 | Re-tap at the same stage without an annulment is a genuine duplicate
- C4102807 | Multiple annulment and re-tap cycles in one day cap correctly
- C4102808 | Annulment on a previous day does not affect the new day's first tap
- C4102812 | Annulment processed before the second tap makes it a normal first journey
- C4102814 | Cancelling a tap with no following tap leaves nothing missing
- C4102883 | Account Status Report
- C4102884 | Action List Report
- C4102886 | Aftercare Report
- C4102887 | Audit Report
- C4102888 | Authorisation Failures Report
- C4102889 | Cancelled Tap Report
- C4102890 | Debt Report
- C4102891 | Declined Taps Report
- C4102892 | Deny List Report
- C4102893 | Duplicate Taps Report
- C4102894 | EMV Summary Report
- C4102895 | ePurse Balance Report
- C4102896 | Exception Report
- C4102897 | Expired Tap Report
- C4102898 | Fare Band Report
- C4102899 | Initial Taps by Brand Report
- C4102900 | Inspection Details Report
- C4102901 | Journey Summary Report
- C4102902 | Journeys by Card Scheme Report
- C4102903 | Journeys by Service/Route Report
- C4102904 | Late Taps Report
- C4102905 | Lost Tap Data Report
- C4102906 | PSP Technical Errors Report
- C4102907 | Refunds Report
- C4102908 | Retail Debt Report
- C4102909 | Retail Transactions Report
- C4102910 | Revenue Apportionment Report
- C4102911 | Revenue by Business Rule Report
- C4102912 | Revenue by MID Report
- C4102913 | Revenue Inspection Report
- C4102914 | Shared Liability Report
- C4102915 | Tap Reconciliation Report
- C4102916 | Transaction Report
- C4102917 | Unique Taps Report
- C4103583 | A matched tap-on and tap-off within PJT is charged the point-to-point fare
- C4103584 | A missing tap-off is charged the maximum fare
- C4103585 | A maximum-fare journey is excluded from capping
- C4103586 | A same-location re-tap within the Same Location Time is suppressed
- C4103587 | A free bus-to-rail transfer within the window leaves the bus leg uncharged
- C4103588 | A missing-tap correction recalculates the journey and refunds the difference
- C4103589 | The 3-Day cap applies within one Monday-to-Sunday week
- C4103597 | A first-login user with no claims is denied the Operator Portal and CloudFare
- C4103598 | An operator sees own and descendant data but not a sibling branch's

## Title over 72 chars _(advisory)_ - 84
- C4102999 | Product — a Smartcard product is configured (WTS SmartCreate / SmartRecharge) - 77 chars
- C4103035 | Activity Log — failed validations, declined taps and failed payments are identified with reason - 95 chars
- C4102758 | Metro cap — correction outside the Metro zone removes the cap and charges the difference - 88 chars
- C4102759 | Metro cap — correction into the Metro zone applies the cap and refunds the difference - 85 chars
- C4102764 | Metro cap — correcting the first full-fare tap leaves its charge unchanged - 74 chars
- C4102765 | Metro cap — correcting an unsettled capped tap re-evaluates and stays free - 74 chars
- C4102767 | Metro cap — re-running settlement after a correction does not re-charge the capped tap - 86 chars
- C4102769 | Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference - 94 chars
- C4102770 | Zonal cap — lower-fare correction within the zone, day still above cap, holds - 77 chars
- C4102773 | Zonal cap — correction into a capped zone audits a free tap under the zonal cap - 79 chars
- C4102774 | Zonal cap — a correction into a capped zone does not increase the account total - 79 chars
- C4102775 | Zonal cap — a corrected tap reports under the zonal cap, not a reference cap - 76 chars
- C4102776 | Zonal cap — correcting into a zone below cap charges toward the zonal cap - 73 chars
- C4102780 | Zonal cap — the cap applies after a correction regardless of transport mode - 75 chars
- C4102781 | Reference cap — correction to a higher ref removes the cap and charges the difference - 85 chars
- C4102782 | Reference cap — correction to a lower ref below the cap removes it and refunds - 78 chars
- C4102783 | Reference cap — correction to a lower ref still above the cap charges the extra - 79 chars
- C4102786 | Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds - 91 chars
- C4102787 | Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds - 86 chars
- C4102789 | Town service cap — correction outside the town to a higher fare removes the cap and charges the difference - 106 chars
- C4102790 | Town service cap — correction outside the town to a lower fare removes the cap and refunds - 90 chars
- C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus) - 78 chars
- C4102812 | Annulment processed before the second tap makes it a normal first journey - 73 chars
- C4102817 | Duplicate Detection — an out-of-order (earlier-timestamp) repeat tap is still a duplicate - 89 chars
- C4102818 | Duplicate Detection — interleaved retail transactions do not reset the duplicate reference - 90 chars
- C4102819 | Duplicate Detection — a same-stage repeat tap after a different-stage retail is still a duplicate - 97 chars
- C4102820 | Duplicate Detection — a same-stage tap outside the window is a genuine new tap - 78 chars
- C4102821 | Duplicate Detection — a retail transaction is never flagged as a duplicate of a tap - 83 chars
- C4102822 | Duplicate Detection — a later tap from a different boarding stage is a genuine new tap - 86 chars
- C4102827 | Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122) - 92 chars
- C4102833 | Journey History — a settled TOO journey offers onward stops for correction (CR122) - 82 chars
- C4102834 | Journey History — a settled TOO journey from another stage offers onward stops (CR122) - 86 chars
- C4102835 | Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122) - 93 chars
- C4102836 | Journey History — re-opening the correction always offers the onward stops (CR122) - 82 chars
- C4102837 | Journey History — no onward stops offered when boarding is the last stop on the route (CR122) - 93 chars
- C4102838 | Journey History — correction offers stops for the journey's operator (CR122) - 76 chars
- C4102825 | Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122) - 91 chars
- C4102826 | Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122) - 90 chars
- C4102828 | Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122) - 108 chars
- C4102830 | Journey History — cancelling a charged journey refunds it and retains the record - 80 chars
- C4102831 | Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122) - 119 chars
- C4102845 | Journey History — a cancelled £0.00 journey stays visible and correctable (CR122) - 81 chars
- C4102842 | Alighting-Stop Correction — selecting a stop updates the alighting stage and recalculates the fare (CR122) - 106 chars
- C4102843 | Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122) - 97 chars
- C4102844 | Journey History — a £0.00 capped journey stays visible and correctable (CR122) - 78 chars
- C4102846 | Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122) - 90 chars
- C4102848 | Alighting-Stop Correction — positive-fare transfer stops still offered (CR122) - 78 chars
- C4102849 | Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122) - 78 chars
- C4102850 | Debt Recovery — a recoverable debt is recovered and the card is re-enabled - 74 chars
- C4102852 | Debt Recovery — automated (scheme) recovery clears a recoverable issuer-liability debt - 86 chars
- C4102853 | Debt Recovery — a successful recovery removes the card from the Deny List - 73 chars
- C4102854 | Debt Recovery — the recovered account is visible in the Operator Portal with its correct status - 95 chars
- C4102855 | Debt Recovery — recovery outcome is verified in the portal; service logging by dev tests - 88 chars
- C4102945 | Deny List — a card is added when it fails payment authorisation at settlement - 77 chars
- C4102946 | Deny List — a listed card is declined at the validator and the tap is audited - 77 chars
- C4102947 | Deny List — a card is removed and re-enabled when its debt is recovered via any trigger - 87 chars
- C4102867 | Customer Services — operator reviews a customer's journeys over a date range - 76 chars
- C4102875 | Capping config — a new rule's created date-time is correct (not an hour ahead) - 78 chars
- C4102928 | Passenger Portal — sign-on prevented for invalid, no-journey or blocked cards - 77 chars
- C4102937 | Card Verification — declined payments are guaranteed up to the Issuer Liability Threshold - 89 chars
- C4102938 | Card Verification — first use of a Visa card triggers an Account Verification Request - 85 chars
- C4102939 | Card Verification — first daily use of a Mastercard triggers a pre-authorisation - 80 chars
- C4102940 | Card Verification — first use after Deny List removal triggers a pre-authorisation - 82 chars
- C4102941 | Late Taps — a tap received within the 14-day window is processed for its travel date - 84 chars
- C4103487 | Late Taps — a tap arriving after settlement is reconciled into the correct travel day - 85 chars
- C4103488 | Late Taps — a late annulment leaves the annulled tap free and the rest capped - 77 chars
- C4102954 | Declined taps — each decline reason is recorded on the Declined Taps Report - 75 chars
- C4103474 | [UNCONFIRMED] Daily cap — Ulsterbus reference-fare cap is reached within a band - 79 chars
- C4103475 | Daily cap — Metro cap and Ulsterbus reference cap both apply on the same day - 76 chars
- C4103476 | Daily cap — Metro and Ulsterbus caps evaluate independently when taps are interleaved - 85 chars
- C4103479 | Daily cap — single taps in different reference bands are each charged in full - 77 chars
- C4103480 | Correction Limits — first alighting-stop correction in the month is accepted (CR122) - 84 chars
- C4103481 | Correction Limits — a second correction in the same month is refused (CR122) - 76 chars
- C4103482 | Correction Limits — a correction in a new month is accepted within the annual limit (CR122) - 91 chars
- C4103484 | Correction Limits — third yearly correction accepted, immediate fourth refused (CR122) - 86 chars
- C4103583 | A matched tap-on and tap-off within PJT is charged the point-to-point fare - 74 chars
- C4103587 | A free bus-to-rail transfer within the window leaves the bus leg uncharged - 74 chars
- C4103588 | A missing-tap correction recalculates the journey and refunds the difference - 76 chars
- C4103590 | Capping timing — a newly configured capping rule activates the next business day - 80 chars
- C4103591 | Capping timing — taps either side of the 04:00 boundary fall into different cap days - 84 chars
- C4103592 | Capping timing — a deny-listed token starts being denied within about a delta cycle - 83 chars
- C4103595 | Shift Board — a Sunday-start CSV bitmask is stored/filtered in Monday-start DB order - 84 chars
- C4103596 | Shift Board — a re-import sets Valid-From at 4am and purges after the 7-day retention - 85 chars
- C4103597 | A first-login user with no claims is denied the Operator Portal and CloudFare - 77 chars

## Objective/preface empty - 0
_none_

## Objective not starting 'This test is to confirm' - 82
- C4103165 | [UNCONFIRMED] Run the Action List reports (Smartrack) - **UNCONFIRMED** — the Smartrack Reports page and its Active/Inactive/d
- C4103166 | [UNCONFIRMED] Run the Liability and Scheme Liability reports (Smartrack) - **UNCONFIRMED** — the Smartrack Liability (summary/detailed) and Schem
- C4103167 | [UNCONFIRMED] Run the Default Payment report (Smartrack) - **UNCONFIRMED** — the Smartrack Default Payment report is NOT specifie
- C4103168 | [UNCONFIRMED] Run the Delivery report (Smartrack) - **UNCONFIRMED** — the Smartrack Delivery report (summary/detailed) is 
- C4103169 | [UNCONFIRMED] Run the Refund report (Smartrack) - **UNCONFIRMED** — the Smartrack Refund report is NOT specified in any 
- C4103170 | [UNCONFIRMED] Run the Decommission Card report (Smartrack) - **UNCONFIRMED** — the Smartrack Decommission Card report is NOT specif
- C4103171 | [UNCONFIRMED] Run the POS Revenue Analysis report (Smartrack) - **UNCONFIRMED** — the Smartrack POS Revenue Analysis report is NOT spe
- C4103102 | [UNCONFIRMED] Origin and Destination reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue; lik
- C4103103 | [UNCONFIRMED] Bus Loading by Route/Journey report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103104 | [UNCONFIRMED] Route/Stage reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103105 | [UNCONFIRMED] Journey Analysis reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103106 | [UNCONFIRMED] Stage Timeband report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103107 | [UNCONFIRMED] Patronage Timeband report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103108 | [UNCONFIRMED] Revenue and Revenue by Stop reports - **UNCONFIRMED** — no 'Revenue' or 'Revenue by Stop' report of these na
- C4103110 | [UNCONFIRMED] POS Revenue report - **UNCONFIRMED** — no Merit 'POS Revenue' report of this name in the co
- C4103112 | [UNCONFIRMED] Bus Serviceability Final Defects report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103113 | [UNCONFIRMED] GPS reports - **UNCONFIRMED** — the GPS report and GPS Stage Change Failure reports 
- C4103114 | [UNCONFIRMED] Route Purchase report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103119 | [UNCONFIRMED] Tickets By Operator report - **UNCONFIRMED** — not named in the governing revenue-reporting spec (w
- C4103120 | [UNCONFIRMED] NIR Revenue Performance reports - **UNCONFIRMED** — the generic Class/Route Revenue Performance reports 
- C4103121 | [UNCONFIRMED] NIR Period Trend Analysis reports - **UNCONFIRMED** — NIR-specific Period Trend Analysis reports are NOT n
- C4103122 | [UNCONFIRMED] BRT Revenue Performance reports - **UNCONFIRMED** — BRT-specific Class/Route Revenue Performance reports
- C4103123 | [UNCONFIRMED] Glider Revenue Performance reports - **UNCONFIRMED** — Glider-specific Route/Class Revenue Performance repo
- C4103124 | [UNCONFIRMED] Ticketing Reports including timebands - **UNCONFIRMED** — a 'Ticketing Reports' grouping combining Revenue Per
- C4103125 | [UNCONFIRMED] Revenue Foregone reports - **UNCONFIRMED** — not named in the governing spec (concessionary fare 
- C4103126 | [UNCONFIRMED] Concessionary Class Summary reports - **UNCONFIRMED** — Concessionary Class Summary reports are NOT named in
- C4103127 | [UNCONFIRMED] ENTCS Passenger and Revenue reports - **UNCONFIRMED** — ENTCS Passenger, ENTCS Revenue and ENTCS Revenue For
- C4103128 | [UNCONFIRMED] Fare Foregone reports - **UNCONFIRMED** — the Fare Foregone Summary and Fare Foregone by Fare 
- C4103134 | [UNCONFIRMED] Outstanding Duties report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103135 | [UNCONFIRMED] Stage List report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4103056 | [UNCONFIRMED] Create, clone, favourite and delete a dashboard - **UNCONFIRMED** — dashboard create/clone/favourite/delete is not speci
- C4103057 | [UNCONFIRMED] Add and remove dashboard tiles - **UNCONFIRMED** — adding/removing dashboard tiles is not specified. Co
- C4103058 | [UNCONFIRMED] View a dashboard full screen - **UNCONFIRMED** — a dashboard full-screen view is not specified. Confi
- C4103065 | [UNCONFIRMED] Software Versions Report - **UNCONFIRMED** — no standalone 'Software Versions Report' is scoped; 
- C4103067 | [UNCONFIRMED] Engineer Visits Report - **UNCONFIRMED** — an 'Engineer Visits Report' is not among the scoped 
- C4103068 | [UNCONFIRMED] Revenue Inspector's Report - **UNCONFIRMED** — a 'Revenue Inspector's Report' (with a BRT variant) 
- C4103069 | [UNCONFIRMED] TVM cash collection reports - **UNCONFIRMED** — TVM cash-collection reports (total coins/notes from 
- C4103070 | [UNCONFIRMED] TVM cash revenue reports - **UNCONFIRMED** — TVM cash-revenue reports (sales revenue, change to c
- C4103071 | [UNCONFIRMED] Rules List Export - **UNCONFIRMED** — a Topology 'Rules List Export' is NOT specified in a
- C4103072 | [UNCONFIRMED] Concise Area & Reference Fare Report - **UNCONFIRMED** — a 'Concise Area & Reference Fare Report' is NOT spec
- C4103073 | [UNCONFIRMED] Route List Export - **UNCONFIRMED** — a Topology 'Route List Export' is NOT specified in a
- C4103074 | [UNCONFIRMED] Product to Ticket Assignment Report - **UNCONFIRMED** — a 'Product to Ticket Assignment Report' is NOT speci
- C4103075 | [UNCONFIRMED] Product List Report - **UNCONFIRMED** — a Topology 'Product List Report' is NOT specified in
- C4103076 | [UNCONFIRMED] Events & Alerts Report - **UNCONFIRMED** — an 'Events & Alerts Report' is NOT specified in any 
- C4103077 | [UNCONFIRMED] Vehicle Check Report - **UNCONFIRMED** — a 'Vehicle Check Report' is NOT specified in any of 
- C4103078 | [UNCONFIRMED] CloudFare Usage Report - **UNCONFIRMED** — a 'CloudFare Usage Report' auditing user actions (wi
- C4102855 | Debt Recovery — recovery outcome is verified in the portal; service logging by dev tests - This test documents the QA split: manual QA verifies the observable re
- C4102883 | Account Status Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102884 | Action List Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102885 | Action List — Negative List Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102886 | Aftercare Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102887 | Audit Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102888 | Authorisation Failures Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102889 | Cancelled Tap Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102890 | Debt Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102891 | Declined Taps Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102892 | Deny List Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102893 | Duplicate Taps Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102894 | EMV Summary Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102895 | ePurse Balance Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102896 | Exception Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102897 | Expired Tap Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102898 | Fare Band Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102899 | Initial Taps by Brand Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102900 | Inspection Details Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102901 | Journey Summary Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102902 | Journeys by Card Scheme Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102903 | Journeys by Service/Route Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102904 | Late Taps Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102905 | Lost Tap Data Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102906 | PSP Technical Errors Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102907 | Refunds Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102908 | Retail Debt Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102909 | Retail Transactions Report - **UNCONFIRMED** — neither the Retail Transactions Report nor the Summa
- C4102910 | Revenue Apportionment Report - **UNCONFIRMED** — FBD-100341 defines the apportionment mechanism and t
- C4102911 | Revenue by Business Rule Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102912 | Revenue by MID Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102913 | Revenue Inspection Report - **UNCONFIRMED** — neither the Revenue Inspection Report nor the Revenu
- C4102914 | Shared Liability Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102915 | Tap Reconciliation Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102916 | Transaction Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s
- C4102917 | Unique Taps Report - **UNCONFIRMED** — not named in the seven governing ABT/BOS reporting s

## Preconditions empty - 0
_none_

## Preconditions without a GIVEN - 0
_none_

## No When/Then steps at all - 0
_none_

## First step is not a WHEN - 0
_none_

## Step content not WHEN/AND - 0
_none_

## A WHEN with no THEN outcome - 0
_none_

## Genuine compound THEN (two distinct outcomes) - should split - 7
- C4102979 | Import Map Point File — stops are added and existing stops updated - a success box reports the number of stops added (Stops Added) and upda
- C4103060 | Alert Viewer — filter, acknowledge then clear alerts - the acknowledge icon turns green and the alert is marked acknowledged
- C4102818 | Duplicate Detection — interleaved retail transactions do not reset the duplicate reference - the 09:05 tap is not charged again and is flagged a duplicate of the 0
- C4102818 | Duplicate Detection — interleaved retail transactions do not reset the duplicate reference - the 09:10 tap is not charged and is flagged a duplicate of the same 09
- C4102822 | Duplicate Detection — a later tap from a different boarding stage is a genuine new tap - at settlement the 09:00 Casement Park tap is charged £2.30 and the 09:
- C4102865 | Customers — Authorisations: approve, decline or reject a refund request - the request outcome is applied and recorded against the account
- C4103488 | Late Taps — a late annulment leaves the annulled tap free and the rest capped - the annulled tap is charged £0.00 and shown cancelled in Journey Histo

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_
