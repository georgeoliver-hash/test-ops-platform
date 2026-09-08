# Alignment audit - suite 30279

- Cases audited: **272**
- Blocking findings: **41**
- Advisory (reviewed-intentional) findings: **218**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 62
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

## Title over 72 chars _(advisory)_ - 156
- C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus) - 78 chars
- C4102812 | Annulment processed before the second tap makes it a normal first journey - 73 chars
- C4102817 | Duplicate Detection — an out-of-order (earlier-timestamp) repeat tap is still a duplicate - 89 chars
- C4102818 | Duplicate Detection — interleaved retail transactions do not reset the duplicate reference - 90 chars
- C4102819 | Duplicate Detection — a same-stage repeat tap after a different-stage retail is still a duplicate - 97 chars
- C4102820 | Duplicate Detection — a same-stage tap outside the window is a genuine new tap - 78 chars
- C4102821 | Duplicate Detection — a retail transaction is never flagged as a duplicate of a tap - 83 chars
- C4102822 | Duplicate Detection — a later tap from a different boarding stage is a genuine new tap - 86 chars
- C4102830 | Journey History — cancelling a charged journey refunds it and retains the record - 80 chars
- C4102850 | Debt Recovery — a recoverable debt is recovered and the card is re-enabled - 74 chars
- C4102852 | Debt Recovery — automated (scheme) recovery clears a recoverable issuer-liability debt - 86 chars
- C4102853 | Debt Recovery — a successful recovery removes the card from the Deny List - 73 chars
- C4102854 | Debt Recovery — the recovered account is visible in the Operator Portal with its correct status - 95 chars
- C4102855 | Debt Recovery — recovery outcome is verified in the portal; service logging by dev tests - 88 chars
- C4102945 | Deny List — a card is added when it fails payment authorisation at settlement - 77 chars
- C4102946 | Deny List — a listed card is declined at the validator and the tap is audited - 77 chars
- C4102947 | Deny List — a card is removed and re-enabled when its debt is recovered via any trigger - 87 chars
- C4104131 | Metro cap — same-fare alighting correction holds the cap (Operator Portal) - 74 chars
- C4104133 | Metro cap — correction outside the Metro zone removes the cap and charges the difference (Operator Portal) - 106 chars
- C4104135 | Metro cap — correction into the Metro zone applies the cap and refunds the difference (Operator Portal) - 103 chars
- C4104137 | Metro cap — correcting a settled free (capped) tap keeps it at £0.00 (Operator Portal) - 86 chars
- C4104139 | Metro cap — correcting a settled partially-capped tap keeps it at £1.70 (Operator Portal) - 89 chars
- C4104141 | Metro cap — a correction never pushes the day over the cap (Operator Portal) - 76 chars
- C4104143 | Metro cap — a corrected capped tap stays settled and free (Operator Portal) - 75 chars
- C4104145 | Metro cap — correcting the first full-fare tap leaves its charge unchanged (Operator Portal) - 92 chars
- C4104147 | Metro cap — correcting an unsettled capped tap re-evaluates and stays free (Operator Portal) - 92 chars
- C4104149 | Metro cap — a declined journey is not treated as a settled capped tap (Operator Portal) - 87 chars
- C4104151 | Metro cap — re-running settlement after a correction does not re-charge the capped tap (Operator Portal) - 104 chars
- C4104153 | Zonal cap — higher-fare correction within the zone holds the cap (Operator Portal) - 82 chars
- C4104155 | Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference (Operator Portal) - 112 chars
- C4104157 | Zonal cap — lower-fare correction within the zone, day still above cap, holds (Operator Portal) - 95 chars
- C4104159 | Zonal cap — lower-fare correction drops the day below cap and refunds (Operator Portal) - 87 chars
- C4104161 | Zonal cap — Zone 4 correction within the highest band holds the cap (Operator Portal) - 85 chars
- C4104163 | Zonal cap — correction into a capped zone audits a free tap under the zonal cap (Operator Portal) - 97 chars
- C4104165 | Zonal cap — a correction into a capped zone does not increase the account total (Operator Portal) - 97 chars
- C4104167 | Zonal cap — a corrected tap reports under the zonal cap, not a reference cap (Operator Portal) - 94 chars
- C4104169 | Zonal cap — correcting into a zone below cap charges toward the zonal cap (Operator Portal) - 91 chars
- C4104171 | Reference cap — a journey with no zonal cap still uses the reference cap (Operator Portal) - 90 chars
- C4104173 | Zonal cap — correcting to another stop in the same zone keeps the cap (Operator Portal) - 87 chars
- C4104175 | Zonal cap — re-running settlement after a correction adds no charge (Operator Portal) - 85 chars
- C4104177 | Zonal cap — the cap applies after a correction regardless of transport mode (Operator Portal) - 93 chars
- C4104179 | Reference cap — correction to a higher ref removes the cap and charges the difference (Operator Portal) - 103 chars
- C4104181 | Reference cap — correction to a lower ref below the cap removes it and refunds (Operator Portal) - 96 chars
- C4104183 | Reference cap — correction to a lower ref still above the cap charges the extra (Operator Portal) - 97 chars
- C4104185 | Uncapped tap — single tap raised to a higher fare charges the difference (Operator Portal) - 90 chars
- C4104187 | Uncapped tap — single tap lowered refunds the difference (Operator Portal) - 74 chars
- C4104189 | Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds (Operator Portal) - 109 chars
- C4104191 | Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds (Operator Portal) - 104 chars
- C4104193 | Town service cap — correction within the town zone holds the cap (Operator Portal) - 82 chars
- C4104195 | Town service cap — correction outside the town to a higher fare removes the cap and charges the difference (Operator Portal) - 124 chars
- C4104197 | Town service cap — correction outside the town to a lower fare removes the cap and refunds (Operator Portal) - 108 chars
- C4104199 | Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122, Operator Portal) - 108 chars
- C4104201 | Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122, Operator Portal) - 107 chars
- C4104203 | Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122, Operator Portal) - 109 chars
- C4104205 | Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122, Operator Portal) - 125 chars
- C4104207 | Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122, Operator Portal) - 136 chars
- C4104209 | Journey History — a settled TOO journey offers onward stops for correction (CR122, Operator Portal) - 99 chars
- C4104211 | Journey History — a settled TOO journey from another stage offers onward stops (CR122, Operator Portal) - 103 chars
- C4104213 | Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122, Operator Portal) - 110 chars
- C4104215 | Journey History — re-opening the correction always offers the onward stops (CR122, Operator Portal) - 99 chars
- C4104217 | Journey History — no onward stops offered when boarding is the last stop on the route (CR122, Operator Portal) - 110 chars
- C4104219 | Journey History — correction offers stops for the journey's operator (CR122, Operator Portal) - 93 chars
- C4104233 | Journey History — a cancelled £0.00 journey stays visible and correctable (CR122, Operator Portal) - 98 chars
- C4104221 | Alighting-Stop Correction — fare-based filter of offered stops (CR122, Operator Portal) - 87 chars
- C4104223 | Alighting-Stop Correction — zero-fare transfer stops excluded (CR122, Operator Portal) - 86 chars
- C4104225 | Alighting-Stop Correction — positive-fare stops offered (CR122, Operator Portal) - 80 chars
- C4104227 | Alighting-Stop Correction — Operator Portal previews the recalculated fare before confirming (CR122, Operator Portal) - 117 chars
- C4104229 | Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122, Operator Portal) - 114 chars
- C4104231 | Journey History — a £0.00 capped journey stays visible and correctable (CR122, Operator Portal) - 95 chars
- C4104235 | Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122, Operator Portal) - 107 chars
- C4104237 | Alighting-Stop Correction — negative-fare stop excluded (CR122, Operator Portal) - 80 chars
- C4104239 | Alighting-Stop Correction — positive-fare transfer stops still offered (CR122, Operator Portal) - 95 chars
- C4104241 | Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122, Operator Portal) - 95 chars
- C4102867 | Customer Services — operator reviews a customer's journeys over a date range - 76 chars
- C4102875 | Capping config — a new rule's created date-time is correct (not an hour ahead) - 78 chars
- C4102928 | Passenger Portal — sign-on prevented for invalid, no-journey or blocked cards - 77 chars
- C4104132 | Metro cap — same-fare alighting correction holds the cap (Passenger Portal) - 75 chars
- C4104134 | Metro cap — correction outside the Metro zone removes the cap and charges the difference (Passenger Portal) - 107 chars
- C4104136 | Metro cap — correction into the Metro zone applies the cap and refunds the difference (Passenger Portal) - 104 chars
- C4104138 | Metro cap — correcting a settled free (capped) tap keeps it at £0.00 (Passenger Portal) - 87 chars
- C4104140 | Metro cap — correcting a settled partially-capped tap keeps it at £1.70 (Passenger Portal) - 90 chars
- C4104142 | Metro cap — a correction never pushes the day over the cap (Passenger Portal) - 77 chars
- C4104144 | Metro cap — a corrected capped tap stays settled and free (Passenger Portal) - 76 chars
- C4104146 | Metro cap — correcting the first full-fare tap leaves its charge unchanged (Passenger Portal) - 93 chars
- C4104148 | Metro cap — correcting an unsettled capped tap re-evaluates and stays free (Passenger Portal) - 93 chars
- C4104150 | Metro cap — a declined journey is not treated as a settled capped tap (Passenger Portal) - 88 chars
- C4104152 | Metro cap — re-running settlement after a correction does not re-charge the capped tap (Passenger Portal) - 105 chars
- C4104154 | Zonal cap — higher-fare correction within the zone holds the cap (Passenger Portal) - 83 chars
- C4104156 | Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference (Passenger Portal) - 113 chars
- C4104158 | Zonal cap — lower-fare correction within the zone, day still above cap, holds (Passenger Portal) - 96 chars
- C4104160 | Zonal cap — lower-fare correction drops the day below cap and refunds (Passenger Portal) - 88 chars
- C4104162 | Zonal cap — Zone 4 correction within the highest band holds the cap (Passenger Portal) - 86 chars
- C4104164 | Zonal cap — correction into a capped zone audits a free tap under the zonal cap (Passenger Portal) - 98 chars
- C4104166 | Zonal cap — a correction into a capped zone does not increase the account total (Passenger Portal) - 98 chars
- C4104168 | Zonal cap — a corrected tap reports under the zonal cap, not a reference cap (Passenger Portal) - 95 chars
- C4104170 | Zonal cap — correcting into a zone below cap charges toward the zonal cap (Passenger Portal) - 92 chars
- C4104172 | Reference cap — a journey with no zonal cap still uses the reference cap (Passenger Portal) - 91 chars
- C4104174 | Zonal cap — correcting to another stop in the same zone keeps the cap (Passenger Portal) - 88 chars
- C4104176 | Zonal cap — re-running settlement after a correction adds no charge (Passenger Portal) - 86 chars
- C4104178 | Zonal cap — the cap applies after a correction regardless of transport mode (Passenger Portal) - 94 chars
- C4104180 | Reference cap — correction to a higher ref removes the cap and charges the difference (Passenger Portal) - 104 chars
- C4104182 | Reference cap — correction to a lower ref below the cap removes it and refunds (Passenger Portal) - 97 chars
- C4104184 | Reference cap — correction to a lower ref still above the cap charges the extra (Passenger Portal) - 98 chars
- C4104186 | Uncapped tap — single tap raised to a higher fare charges the difference (Passenger Portal) - 91 chars
- C4104188 | Uncapped tap — single tap lowered refunds the difference (Passenger Portal) - 75 chars
- C4104190 | Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds (Passenger Portal) - 110 chars
- C4104192 | Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds (Passenger Portal) - 105 chars
- C4104194 | Town service cap — correction within the town zone holds the cap (Passenger Portal) - 83 chars
- C4104196 | Town service cap — correction outside the town to a higher fare removes the cap and charges the difference (Passenger Portal) - 125 chars
- C4104198 | Town service cap — correction outside the town to a lower fare removes the cap and refunds (Passenger Portal) - 109 chars
- C4104200 | Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122, Passenger Portal) - 109 chars
- C4104202 | Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122, Passenger Portal) - 108 chars
- C4104204 | Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122, Passenger Portal) - 110 chars
- C4104206 | Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122, Passenger Portal) - 126 chars
- C4104208 | Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122, Passenger Portal) - 137 chars
- C4104210 | Journey History — a settled TOO journey offers onward stops for correction (CR122, Passenger Portal) - 100 chars
- C4104212 | Journey History — a settled TOO journey from another stage offers onward stops (CR122, Passenger Portal) - 104 chars
- C4104214 | Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122, Passenger Portal) - 111 chars
- C4104216 | Journey History — re-opening the correction always offers the onward stops (CR122, Passenger Portal) - 100 chars
- C4104218 | Journey History — no onward stops offered when boarding is the last stop on the route (CR122, Passenger Portal) - 111 chars
- C4104220 | Journey History — correction offers stops for the journey's operator (CR122, Passenger Portal) - 94 chars
- C4104234 | Journey History — a cancelled £0.00 journey stays visible and correctable (CR122, Passenger Portal) - 99 chars
- C4104222 | Alighting-Stop Correction — fare-based filter of offered stops (CR122, Passenger Portal) - 88 chars
- C4104224 | Alighting-Stop Correction — zero-fare transfer stops excluded (CR122, Passenger Portal) - 87 chars
- C4104226 | Alighting-Stop Correction — positive-fare stops offered (CR122, Passenger Portal) - 81 chars
- C4104228 | Alighting-Stop Correction — Passenger Portal updates the alighting stage without a fare preview (CR122, Passenger Portal) - 121 chars
- C4104230 | Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122, Passenger Portal) - 115 chars
- C4104232 | Journey History — a £0.00 capped journey stays visible and correctable (CR122, Passenger Portal) - 96 chars
- C4104236 | Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122, Passenger Portal) - 108 chars
- C4104238 | Alighting-Stop Correction — negative-fare stop excluded (CR122, Passenger Portal) - 81 chars
- C4104240 | Alighting-Stop Correction — positive-fare transfer stops still offered (CR122, Passenger Portal) - 96 chars
- C4104242 | Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122, Passenger Portal) - 96 chars
- C4103480 | Correction Limits — first alighting-stop correction in the month is accepted (CR122) - 84 chars
- C4103481 | Correction Limits — a second correction in the same month is refused (CR122) - 76 chars
- C4103482 | Correction Limits — a correction in a new month is accepted within the annual limit (CR122) - 91 chars
- C4103484 | Correction Limits — third yearly correction accepted, immediate fourth refused (CR122) - 86 chars
- C4102937 | Card Verification — declined payments are guaranteed up to the Issuer Liability Threshold - 89 chars
- C4102938 | Card Verification — first use of a Visa card triggers an Account Verification Request - 85 chars
- C4102939 | Card Verification — first daily use of a Mastercard or Maestro card triggers a pre-authorisation - 96 chars
- C4102940 | Card Verification — first use after Deny List removal triggers a pre-authorisation - 82 chars
- C4102941 | Late Taps — a tap received within the 14-day window is processed for its travel date - 84 chars
- C4103487 | Late Taps — a tap arriving after settlement is reconciled into the correct travel day - 85 chars
- C4103488 | Late Taps — a late annulment leaves the annulled tap free and the rest capped - 77 chars
- C4102954 | Declined taps — each decline reason is recorded on the Declined Taps Report - 75 chars
- C4103475 | Daily cap — Metro cap and Ulsterbus reference cap both apply on the same day - 76 chars
- C4103476 | Daily cap — Metro and Ulsterbus caps evaluate independently when taps are interleaved - 85 chars
- C4103479 | Daily cap — single taps in different reference bands are each charged in full - 77 chars
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

## Objective not starting 'This test is to confirm' - 36
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

## Genuine compound THEN (two distinct outcomes) - should split - 5
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
