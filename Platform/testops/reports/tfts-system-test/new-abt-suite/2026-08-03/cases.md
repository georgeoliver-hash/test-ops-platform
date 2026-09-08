# Cases — TFTS - System Test / **NEW** ABT Suite

- Generated: 2026-08-03T11:01:02.478267+00:00
- Total cases: 633

| Case | Title | Section | Linked refs | Has steps |
|---|---|---|---|---|
| C4102791 | Re-tap at the same stage after annulment is the first good tap (Metro) | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102792 | Full Metro day reaches the daily cap after an annulment | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus) | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102794 | Ulsterbus reference fare cap applies on the correct tap after annulment | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102795 | Re-tap after annulment in the ref.61 band caps at the ref.61 value | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102796 | Annulment in the ref.60 band does not borrow the higher ref.61 cap | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102797 | Genuine duplicate without annulment is still rejected as £0.00 | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102798 | Re-tap at a different stage after annulment is a normal first tap | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102799 | Annulling the re-tap as well leaves a later tap as the first good tap | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102800 | Annulment processed in the same settlement run as the re-tap | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102801 | Annulment with no re-tap leaves no chargeable journey | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102802 | Annulling a capped tap does not corrupt the day total | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102804 | Annulment on one card does not affect a similar tap on another card | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102805 | Ulsterbus re-tap with a different alighting and fare after annulment | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102806 | Re-tap at the same stage without an annulment is a genuine duplicate | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102807 | Multiple annulment and re-tap cycles in one day cap correctly | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102808 | Annulment on a previous day does not affect the new day's first tap | ABT / Annulment & Re-tap | TODEV-23967 | yes |
| C4102812 | Annulment processed before the second tap makes it a normal first journey | ABT / Annulment & Re-tap | TODEV-24259 | yes |
| C4102814 | Cancelling a tap with no following tap leaves nothing missing | ABT / Annulment & Re-tap | TODEV-24259 | yes |
| C4102816 | Duplicate Detection — a repeated same-stage tap is not charged again | ABT / Duplicate Detection | FBD-100690, TIMING-2026, TODEV-24258 | yes |
| C4102817 | Duplicate Detection — an out-of-order (earlier-timestamp) repeat tap is still a duplicate | ABT / Duplicate Detection | FBD-100690, TIMING-2026, TODEV-24258 | yes |
| C4102818 | Duplicate Detection — interleaved retail transactions do not reset the duplicate reference | ABT / Duplicate Detection | FBD-100690, TIMING-2026, TODEV-24258 | yes |
| C4102819 | Duplicate Detection — a same-stage repeat tap after a different-stage retail is still a duplicate | ABT / Duplicate Detection | TIMING-2026, TODEV-24258 | yes |
| C4102820 | Duplicate Detection — a same-stage tap outside the window is a genuine new tap | ABT / Duplicate Detection | TIMING-2026, TODEV-24258 | yes |
| C4102821 | Duplicate Detection — a retail transaction is never flagged as a duplicate of a tap | ABT / Duplicate Detection | TIMING-2026, TODEV-24258 | yes |
| C4102822 | Duplicate Detection — a later tap from a different boarding stage is a genuine new tap | ABT / Duplicate Detection | TIMING-2026, TODEV-24258 | yes |
| C4104935 | Annulling a tap reverses a Same Location duplicate marking where applicable | ABT / Duplicate Detection | FBD-100651 | yes |
| C4102823 | Journey History — an annulled (cancelled) journey remains visible | ABT / Journey History | FBD-100662, TODEV-24061 | yes |
| C4102824 | Journey History — an annulled £0.00 journey is still visible | ABT / Journey History | FBD-100662, TODEV-24061 | yes |
| C4102829 | Journey History — annulling one journey does not affect other journeys | ABT / Journey History | FBD-100662, TODEV-24061 | yes |
| C4102830 | Journey History — cancelling a charged journey refunds it and retains the record | ABT / Journey History | FBD-100662, TODEV-24061 | yes |
| C4102832 | Journey History — a cancelled transfer journey remains visible | ABT / Journey History | FBD-100662, TODEV-24061 | yes |
| C4102850 | Debt Recovery — a recoverable debt is recovered and the card is re-enabled | ABT / Debt Recovery | TODEV-24990 | yes |
| C4102851 | Debt Recovery — an unrecoverable debt leaves the cards blocked | ABT / Debt Recovery | TODEV-24990 | yes |
| C4102852 | Debt Recovery — automated Visa recovery clears a debt at a different amount | ABT / Debt Recovery | PSPEC-0015, TODEV-24990 | yes |
| C4102853 | Debt Recovery — a successful recovery removes the card from the Deny List | ABT / Debt Recovery | TODEV-24990 | yes |
| C4102854 | Debt Recovery — the recovered account is visible in the Operator Portal with its correct status | ABT / Debt Recovery | TODEV-24990 | yes |
| C4102855 | Debt Recovery — recovery outcome is verified in the portal; service logging by dev tests | ABT / Debt Recovery | TODEV-24990 | yes |
| C4102945 | Deny List — a card is added when it fails payment authorisation at settlement | ABT / Debt Recovery | — | yes |
| C4102946 | Deny List — a listed card is declined at the validator and the tap is audited | ABT / Debt Recovery | — | yes |
| C4102947 | Deny List — a card is removed and re-enabled when its debt is recovered via any trigger | ABT / Debt Recovery | — | yes |
| C4104540 | Debt Recovery — automated Mastercard recovery clears a debt at a different amount | ABT / Debt Recovery | PSPEC-0015, TODEV-24990 | yes |
| C4104541 | Debt Recovery — automated Maestro recovery clears a recoverable issuer-liability debt | ABT / Debt Recovery | PSPEC-0015, TODEV-24990 | yes |
| C4102856 | Sign On — valid credentials reach the ABT Operator Portal | ABT / Operator Web Portal / Sign On & Access | — | yes |
| C4102857 | Access — portal tasks match the operator's assigned Account Management claims | ABT / Operator Web Portal / Sign On & Access | FBD-100342 | yes |
| C4102858 | Sign On — operator can sign off the ABT Operator Portal | ABT / Operator Web Portal / Sign On & Access | — | yes |
| C4104542 | Access — portal tasks match the operator's assigned Admin claims | ABT / Operator Web Portal / Sign On & Access | FBD-100342 | yes |
| C4104543 | Access — portal tasks match the operator's assigned Capping claims | ABT / Operator Web Portal / Sign On & Access | FBD-100342 | yes |
| C4104544 | Access — portal tasks match the operator's assigned Reports claims | ABT / Operator Web Portal / Sign On & Access | FBD-100342 | yes |
| C4104131 | Metro cap — same-fare alighting correction holds the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104133 | Metro cap — correction outside the Metro zone removes the cap and charges the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104135 | Metro cap — correction into the Metro zone applies the cap and refunds the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104137 | Metro cap — correcting a settled free (capped) tap keeps it at £0.00 (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104139 | Metro cap — correcting a settled partially-capped tap keeps it at £1.70 (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104141 | Metro cap — a correction never pushes the day over the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104143 | Metro cap — a corrected capped tap stays settled and free (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104145 | Metro cap — correcting the first full-fare tap leaves its charge unchanged (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104147 | Metro cap — correcting an unsettled capped tap re-evaluates and stays free (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104149 | Metro cap — a declined journey is not treated as a settled capped tap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104151 | Metro cap — re-running settlement after a correction does not re-charge the capped tap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104153 | Zonal cap — higher-fare correction within the zone holds the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104155 | Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104157 | Zonal cap — lower-fare correction within the zone, day still above cap, holds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104159 | Zonal cap — lower-fare correction drops the day below cap and refunds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104161 | Zonal cap — Zone 4 correction within the highest band holds the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104163 | Zonal cap — correction into a capped zone audits a free tap under the zonal cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104165 | Zonal cap — a correction into a capped zone does not increase the account total (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104167 | Zonal cap — a corrected tap reports under the zonal cap, not a reference cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104169 | Zonal cap — correcting into a zone below cap charges toward the zonal cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104171 | Reference cap — a journey with no zonal cap still uses the reference cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104173 | Zonal cap — correcting to another stop in the same zone keeps the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104175 | Zonal cap — re-running settlement after a correction adds no charge (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104177 | Zonal cap — the cap applies after a correction regardless of transport mode (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104179 | Reference cap — correction to a higher ref removes the cap and charges the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104181 | Reference cap — correction to a lower ref below the cap removes it and refunds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104183 | Reference cap — correction to a lower ref still above the cap charges the extra (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104185 | Uncapped tap — single tap raised to a higher fare charges the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104187 | Uncapped tap — single tap lowered refunds the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104189 | Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104191 | Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104193 | Town service cap — correction within the town zone holds the cap (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104195 | Town service cap — correction outside the town to a higher fare removes the cap and charges the difference (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104197 | Town service cap — correction outside the town to a lower fare removes the cap and refunds (Operator Portal) | ABT / Operator Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104199 | Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104201 | Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104203 | Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104205 | Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104207 | Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104209 | Journey History — a settled TOO journey offers onward stops for correction (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104211 | Journey History — a settled TOO journey from another stage offers onward stops (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104213 | Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104215 | Journey History — re-opening the correction always offers the onward stops (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104217 | Journey History — no onward stops offered when boarding is the last stop on the route (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104219 | Journey History — correction offers stops for the journey's operator (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104233 | Journey History — a cancelled £0.00 journey stays visible and correctable (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104221 | Alighting-Stop Correction — fare-based filter of offered stops (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104223 | Alighting-Stop Correction — zero-fare transfer stops excluded (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104225 | Alighting-Stop Correction — positive-fare stops offered (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104227 | Alighting-Stop Correction — Operator Portal previews the recalculated fare before confirming (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104229 | Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104231 | Journey History — a £0.00 capped journey stays visible and correctable (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104235 | Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104237 | Alighting-Stop Correction — negative-fare stop excluded (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104239 | Alighting-Stop Correction — positive-fare transfer stops still offered (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104241 | Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122, Operator Portal) | ABT / Operator Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102859 | Customers — search and filter customer accounts | ABT / Operator Web Portal / Customers | — | yes |
| C4102860 | Customers — select and view a customer account | ABT / Operator Web Portal / Customers | — | yes |
| C4102861 | Customers — view and export a customer's Journey History | ABT / Operator Web Portal / Customers | — | yes |
| C4102862 | Customers — view and export a customer's Transaction History | ABT / Operator Web Portal / Customers | — | yes |
| C4102863 | Customers — queue a refund from a transaction | ABT / Operator Web Portal / Customers | — | yes |
| C4102864 | Customers — operator aftercare queries and comments | ABT / Operator Web Portal / Customers | — | yes |
| C4102865 | Customers — Authorisations: approve, decline or reject a refund request | ABT / Operator Web Portal / Customers | — | yes |
| C4102866 | Customers — Authorisations: accept all and reject all | ABT / Operator Web Portal / Customers | — | yes |
| C4102867 | Customer Services — operator reviews a customer's journeys over a date range | ABT / Operator Web Portal / Customer Services | — | yes |
| C4102868 | Customer Services — corrupt tap messages are rejected and quarantined | ABT / Operator Web Portal / Customer Services | — | yes |
| C4104889 | Customer Services — operator retries a customer's declined payment (Visa) | ABT / Operator Web Portal / Customer Services | PSPEC-0015 | yes |
| C4104890 | Customer Services — operator retries a customer's declined payment (Mastercard) | ABT / Operator Web Portal / Customer Services | PSPEC-0015 | yes |
| C4102869 | Capping config — configure a daily capping rule | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102870 | Capping config — configure weekly and monthly capping rules | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102871 | Transfers — a qualifying Directional feeder-to-Glider transfer is charged £0.00 (Scenario 1) | ABT / Operator Web Portal / Capping Configuration | FBD-100651 | yes |
| C4102872 | Capping config — add, edit and view a price cap | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102873 | Capping config — deactivate and archive a capping rule | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102874 | Capping config — Price Rule information icon | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102875 | Capping config — a new rule's created date-time is correct (not an hour ahead) | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102876 | Capping config — add a daily capping group | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4102877 | Capping config — add a weekly capping group | ABT / Operator Web Portal / Capping Configuration | — | yes |
| C4104545 | Transfers — a qualifying Non-Directional feeder-to-Glider transfer is charged £0.00 (Scenario 3) | ABT / Operator Web Portal / Capping Configuration | FBD-100651 | yes |
| C4104546 | Transfers — a qualifying Glider-to-feeder transfer is charged £0.00 (Scenarios 2/4) | ABT / Operator Web Portal / Capping Configuration | FBD-100651 | yes |
| C4104547 | Transfers — a qualifying Ulsterbus-to-Glider transfer is charged £0.00 (Scenario 11) | ABT / Operator Web Portal / Capping Configuration | FBD-100651 | yes |
| C4102878 | Admin — set End of Operational Day and Week | ABT / Operator Web Portal / Administrator Settings | PSPEC-0015 | yes |
| C4102879 | Admin — set the maximum late data period | ABT / Operator Web Portal / Administrator Settings | PSPEC-0015 | yes |
| C4102880 | Admin — set the maximum journey duration | ABT / Operator Web Portal / Administrator Settings | REQ-3414 | yes |
| C4102881 | Admin — set debt-recovery retry attempts and message | ABT / Operator Web Portal / Administrator Settings | PSPEC-0015, REQ-3399, REQ-3400 | yes |
| C4102882 | Admin — set a minimum fare for an e-Purse smartcard | ABT / Operator Web Portal / Administrator Settings | PSPEC-0015, REQ-3192 | yes |
| C4102883 | Account Status Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3438, REQ-3457 | yes |
| C4102884 | Action List Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3436, REQ-3457 | yes |
| C4102885 | Action List — Negative List Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3436, REQ-3457 | yes |
| C4102886 | Aftercare Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102887 | Audit Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102888 | Authorisation Failures Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102889 | Cancelled Tap Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102890 | Debt Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3435, REQ-3457 | yes |
| C4102891 | Declined Taps Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102892 | Deny List Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102893 | Duplicate Taps Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3442 | yes |
| C4102894 | EMV Summary Report — Visa | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662, REQ-3457, REQ-3491 | yes |
| C4102895 | ePurse Balance Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3441 | yes |
| C4102896 | Exception Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662, REQ-3442, REQ-3457 | yes |
| C4102897 | Expired Tap Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3442 | yes |
| C4102898 | Fare Band Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102899 | Initial Taps by Brand Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102900 | Inspection Details Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102901 | Journey Summary Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102902 | Journeys by Card Scheme Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102903 | Journeys by Service/Route Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102904 | Late Taps Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3442 | yes |
| C4102905 | Lost Tap Data Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3457, REQ-3533 | yes |
| C4102906 | PSP Technical Errors Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102907 | Refunds Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3439 | yes |
| C4102908 | Retail Debt Report — Visa | ABT / Operator Web Portal / Reports | CA-13549, FBD-100387 | yes |
| C4102909 | Retail Transactions Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102910 | Revenue Apportionment Report | ABT / Operator Web Portal / Reports | FBD-100341 | yes |
| C4102911 | Revenue by Business Rule Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102912 | Revenue by MID Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3440, REQ-3457 | yes |
| C4102913 | Revenue Inspection Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-3437 | yes |
| C4102914 | Shared Liability Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4102915 | Tap Reconciliation Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662 | yes |
| C4102916 | Transaction Report | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662, REQ-3457, REQ-3492 | yes |
| C4102917 | Unique Taps Report | ABT / Operator Web Portal / Reports | FBD-100387 | yes |
| C4104548 | EMV Summary Report — MasterCard | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662, REQ-3457, REQ-3491 | yes |
| C4104549 | EMV Summary Report — Maestro | ABT / Operator Web Portal / Reports | FBD-100387, REQ-2662, REQ-3457, REQ-3491 | yes |
| C4104550 | Retail Debt Report — Mastercard | ABT / Operator Web Portal / Reports | CA-13549, FBD-100387 | yes |
| C4104551 | Retail Debt Report — Maestro | ABT / Operator Web Portal / Reports | FBD-100387, TODEV-11567, TODEV-15538 | yes |
| C4102927 | Passenger Portal — sign on to an anonymous account | ABT / Passenger Web Portal / Sign On & Account | PSPEC-0015, REQ-3561 | yes |
| C4102928 | Passenger Portal — sign-on prevented for invalid, no-journey or blocked cards | ABT / Passenger Web Portal / Sign On & Account | REQ-3561 | yes |
| C4102929 | Passenger Portal — home screen shows balance and summary | ABT / Passenger Web Portal / Sign On & Account | PSPEC-0015 | yes |
| C4102930 | Passenger Portal — customer can sign off | ABT / Passenger Web Portal / Sign On & Account | — | yes |
| C4104132 | Metro cap — same-fare alighting correction holds the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104134 | Metro cap — correction outside the Metro zone removes the cap and charges the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104136 | Metro cap — correction into the Metro zone applies the cap and refunds the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4104138 | Metro cap — correcting a settled free (capped) tap keeps it at £0.00 (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104140 | Metro cap — correcting a settled partially-capped tap keeps it at £1.70 (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104142 | Metro cap — a correction never pushes the day over the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104144 | Metro cap — a corrected capped tap stays settled and free (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104146 | Metro cap — correcting the first full-fare tap leaves its charge unchanged (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104148 | Metro cap — correcting an unsettled capped tap re-evaluates and stays free (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104150 | Metro cap — a declined journey is not treated as a settled capped tap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104152 | Metro cap — re-running settlement after a correction does not re-charge the capped tap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4104154 | Zonal cap — higher-fare correction within the zone holds the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104156 | Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104158 | Zonal cap — lower-fare correction within the zone, day still above cap, holds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104160 | Zonal cap — lower-fare correction drops the day below cap and refunds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104162 | Zonal cap — Zone 4 correction within the highest band holds the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4104164 | Zonal cap — correction into a capped zone audits a free tap under the zonal cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104166 | Zonal cap — a correction into a capped zone does not increase the account total (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104168 | Zonal cap — a corrected tap reports under the zonal cap, not a reference cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104170 | Zonal cap — correcting into a zone below cap charges toward the zonal cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104172 | Reference cap — a journey with no zonal cap still uses the reference cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104174 | Zonal cap — correcting to another stop in the same zone keeps the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104176 | Zonal cap — re-running settlement after a correction adds no charge (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104178 | Zonal cap — the cap applies after a correction regardless of transport mode (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4104180 | Reference cap — correction to a higher ref removes the cap and charges the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104182 | Reference cap — correction to a lower ref below the cap removes it and refunds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104184 | Reference cap — correction to a lower ref still above the cap charges the extra (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4104186 | Uncapped tap — single tap raised to a higher fare charges the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104188 | Uncapped tap — single tap lowered refunds the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104190 | Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104192 | Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4104194 | Town service cap — correction within the town zone holds the cap (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104196 | Town service cap — correction outside the town to a higher fare removes the cap and charges the difference (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104198 | Town service cap — correction outside the town to a lower fare removes the cap and refunds (Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4104200 | Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104202 | Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104204 | Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104206 | Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104208 | Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4104210 | Journey History — a settled TOO journey offers onward stops for correction (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104212 | Journey History — a settled TOO journey from another stage offers onward stops (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104214 | Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104216 | Journey History — re-opening the correction always offers the onward stops (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104218 | Journey History — no onward stops offered when boarding is the last stop on the route (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104220 | Journey History — correction offers stops for the journey's operator (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4104234 | Journey History — a cancelled £0.00 journey stays visible and correctable (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Journey History | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104222 | Alighting-Stop Correction — fare-based filter of offered stops (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104224 | Alighting-Stop Correction — zero-fare transfer stops excluded (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104226 | Alighting-Stop Correction — positive-fare stops offered (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104228 | Alighting-Stop Correction — Passenger Portal updates the alighting stage without a fare preview (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104230 | Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104232 | Journey History — a £0.00 capped journey stays visible and correctable (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104236 | Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104238 | Alighting-Stop Correction — negative-fare stop excluded (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104240 | Alighting-Stop Correction — positive-fare transfer stops still offered (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4104242 | Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122, Passenger Portal) | ABT / Passenger Web Portal / Tap Correction / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102931 | Account Functions — view and print Journey History | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4102932 | Account Functions — view and print Transaction History | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4102933 | Account Functions — request a refund | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4102934 | Account Functions — retry a declined payment (Visa) | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4102935 | Account Functions — request a card replacement | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4102936 | Account Functions — raise a general query | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4104888 | Account Functions — retry a declined payment (Mastercard) | ABT / Passenger Web Portal / Account Functions | PSPEC-0015 | yes |
| C4103480 | Correction Limits — first alighting-stop correction in the month is accepted (CR122) | ABT / Passenger Web Portal / Correction Limits | FBD-100662, GEORGE-2026 | yes |
| C4103481 | Correction Limits — a second correction in the same month is refused (CR122) | ABT / Passenger Web Portal / Correction Limits | FBD-100662, FBD-100690, GEORGE-2026 | yes |
| C4103482 | Correction Limits — a correction in a new month is accepted within the annual limit (CR122) | ABT / Passenger Web Portal / Correction Limits | FBD-100662, GEORGE-2026 | yes |
| C4103483 | Correction Limits — a fourth correction in the year is refused (CR122) | ABT / Passenger Web Portal / Correction Limits | FBD-100662, GEORGE-2026 | yes |
| C4103484 | Correction Limits — third yearly correction accepted, immediate fourth refused (CR122) | ABT / Passenger Web Portal / Correction Limits | FBD-100662, GEORGE-2026 | yes |
| C4102937 | Card Verification — declined Visa payments are guaranteed up to the Issuer Liability Threshold | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3354 | yes |
| C4102938 | Card Verification — first use of a Visa card triggers an Account Verification Request | ABT / Processing Taps / Card Verification | PSPEC-0015 | yes |
| C4102939 | Card Verification — first daily use of a Mastercard card triggers a pre-authorisation | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3360 | yes |
| C4102940 | Card Verification — first use after Deny List removal of a Mastercard card triggers a pre-authorisation | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3360 | yes |
| C4104552 | Card Verification — declined Mastercard payments are guaranteed up to the Issuer Liability Threshold | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3354 | yes |
| C4104553 | Card Verification — declined Maestro payments are guaranteed up to the Issuer Liability Threshold | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3354 | yes |
| C4104554 | Card Verification — first daily use of a Maestro card triggers a pre-authorisation | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3361 | yes |
| C4104555 | Card Verification — first use after Deny List removal of a Maestro card triggers a pre-authorisation | ABT / Processing Taps / Card Verification | PSPEC-0015, REQ-3361 | yes |
| C4102941 | Late Taps — a tap received within the 14-day window is processed for its travel date | ABT / Processing Taps / Late Taps | FBD-100389 | yes |
| C4102942 | Late Taps — a tap received beyond the 14-day window is not accepted | ABT / Processing Taps / Late Taps | FBD-100389, FBD-100658 | yes |
| C4102943 | Late Taps — capping is applied retrospectively to a late tap | ABT / Processing Taps / Late Taps | FBD-100389 | yes |
| C4102944 | Late Taps — a duplicate of an already-processed tap is disregarded | ABT / Processing Taps / Late Taps | FBD-100690 | yes |
| C4103485 | Late Taps — taps held on a device are processed and capped once uploaded | ABT / Processing Taps / Late Taps | FBD-100389 | yes |
| C4103486 | Late Taps — an intraday late tap is capped with the day's live taps | ABT / Processing Taps / Late Taps | FBD-100389 | yes |
| C4103487 | Late Taps — a tap arriving after settlement is reconciled into the correct travel day | ABT / Processing Taps / Late Taps | FBD-100389 | yes |
| C4103488 | Late Taps — a late annulment leaves the annulled tap free and the rest capped | ABT / Processing Taps / Late Taps | FBD-100389, FBD-100662 | yes |
| C4102948 | ETM Metro Tap-On-Only — end to end | ABT / End to End | — | yes |
| C4102949 | ETM Metro retail transaction — end to end | ABT / End to End | — | yes |
| C4102950 | HHD Glider Tap-On-Only — end to end | ABT / End to End | — | yes |
| C4102951 | HHD Glider retail transaction — end to end | ABT / End to End | — | yes |
| C4102952 | HHD Rail retail transaction — end to end | ABT / End to End | — | yes |
| C4102953 | Zones — a multi-zone stop is a member of each of its travel zones | ABT / Configuration & Setup | FBD-100229 | yes |
| C4102954 | Declined taps — an expired card (DeclinedReason 1) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4102955 | Capping rule — base products are loaded from the fares engine | ABT / Configuration & Setup | — | yes |
| C4104556 | Declined taps — a Deny-listed card (DeclinedReason 2) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4104557 | Declined taps — an ODA/authenticity failure (DeclinedReason 3) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4104558 | Declined taps — a cancelled tap (DeclinedReason 4) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4104559 | Declined taps — a BIN-listed card (DeclinedReason 15) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4104560 | Declined taps — a passback (Negative List) (DeclinedReason 20) is recorded on the Declined Taps Report | ABT / Configuration & Setup | FBD-100658 | yes |
| C4103473 | Daily cap — Metro daily cap is reached and applied | ABT / Functional / Daily Capping | — | yes |
| C4103474 | Daily cap — Ulsterbus reference-fare cap is reached within a band | ABT / Functional / Daily Capping | — | yes |
| C4103475 | Daily cap — Metro cap and Ulsterbus reference cap both apply on the same day | ABT / Functional / Daily Capping | — | yes |
| C4103476 | Daily cap — Metro and Ulsterbus caps evaluate independently when taps are interleaved | ABT / Functional / Daily Capping | — | yes |
| C4103477 | Daily cap — two reference bands cap independently on the same day | ABT / Functional / Daily Capping | — | yes |
| C4103478 | Daily cap — a single Metro tap is charged in full | ABT / Functional / Daily Capping | — | yes |
| C4103479 | Daily cap — single taps in different reference bands are each charged in full | ABT / Functional / Daily Capping | — | yes |
| C4103583 | A matched tap-on and tap-off within PJT is charged the point-to-point fare | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100690, FBD-100698 | yes |
| C4103584 | A missing tap-off is charged the maximum fare | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100307, FBD-100690 | yes |
| C4103585 | A maximum-fare journey is excluded from capping | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100389, FBD-100690 | yes |
| C4103586 | A same-location re-tap within the Same Location Time is suppressed | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100690 | yes |
| C4103587 | A free bus-to-rail transfer within the window leaves the bus leg uncharged | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100690 | yes |
| C4103588 | A missing-tap correction recalculates the journey and refunds the difference | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100690 | yes |
| C4103589 | The 3-Day cap applies within one Monday-to-Sunday week | ABT / Functional / NIR Tap-On-Tap-Off | FBD-100690 | yes |
| C4103590 | Capping timing — a newly configured capping rule activates the next business day | ABT / Functional / Capping Timing | FBD-100307 | yes |
| C4103591 | Capping timing — taps either side of the 04:00 boundary fall into different cap days | ABT / Functional / Capping Timing | FBD-100389 | yes |
| C4103592 | Capping timing — a deny-listed token starts being denied within about a delta cycle | ABT / Functional / Capping Timing | FBD-100307, FBD-100690 | yes |
| C4103593 | Capping timing — a re-authorised card is removed from the Deny List | ABT / Functional / Capping Timing | FBD-100307, FBD-100662 | yes |
| C4103594 | Shift Board — CSV import rejects a malformed row | ABT / Functional / Shift Board | FBD-100831 | yes |
| C4103595 | Shift Board — a Sunday-start CSV bitmask is stored/filtered in Monday-start DB order | ABT / Functional / Shift Board | FBD-100831 | yes |
| C4103596 | Shift Board — a re-import sets Valid-From at 4am and purges after the 7-day retention | ABT / Functional / Shift Board | FBD-100831 | yes |
| C4103597 | A first-login user with no claims is denied the Operator Portal and CloudFare | ABT / Functional / Access & Claims | FBD-100342 | yes |
| C4103598 | An operator sees own and descendant data but not a sibling branch's | ABT / Functional / Access & Claims | FBD-100342, FBD-100383 | yes |
| C4102657 | ZZ_DELETE_REVIEW - Same-fare Metro adjustment — cap re-applies, no change | Delete | — | yes |
| C4102658 | ZZ_DELETE_REVIEW - Metro-zone UB tap adjusted OUTSIDE zone — cap removed, charge increases | Delete | — | yes |
| C4102659 | ZZ_DELETE_REVIEW - UB tap adjusted INTO Metro zone — Metro cap applies, charge reduces | Delete | — | yes |
| C4102660 | ZZ_DELETE_REVIEW - Higher-fare adjustment WITHIN zone — cap holds, no change [Outline × 5: Z1/Z2/Z3/Z4/ZNW] | Delete | — | yes |
| C4102661 | ZZ_DELETE_REVIEW - Higher-fare adjustment OUTSIDE zone — cap removed, charge increases [Outline × 4: Z1/Z2/Z3/ZNW] | Delete | — | yes |
| C4102662 | ZZ_DELETE_REVIEW - Lower-fare adjustment WITHIN zone, day still ABOVE cap — cap holds [Outline × 5: Z1/Z2/Z3/Z4/ZNW] | Delete | — | yes |
| C4102663 | ZZ_DELETE_REVIEW - Lower-fare adjustment drops day BELOW cap — cap removed, charge reduces [Outline × 4: Z2/Z3/Z4/ZNW] | Delete | — | yes |
| C4102664 | ZZ_DELETE_REVIEW - Zone 4 — higher-fare OUTSIDE Zone 4 but still in highest band — cap holds | Delete | — | yes |
| C4102665 | ZZ_DELETE_REVIEW - Adjust one same-ref tap to HIGHER ref — cap removed, charge increases | Delete | — | yes |
| C4102666 | ZZ_DELETE_REVIEW - Adjust one same-ref tap to LOWER ref so aggregate < cap — cap removed, charge reduces | Delete | — | yes |
| C4102667 | ZZ_DELETE_REVIEW - Adjust one same-ref tap to LOWER ref but aggregate still > cap — cap removed, extra charge | Delete | — | yes |
| C4102668 | ZZ_DELETE_REVIEW - Single uncapped tap adjusted to HIGHER fare — extra charge | Delete | — | yes |
| C4102669 | ZZ_DELETE_REVIEW - Single uncapped tap adjusted to LOWER fare — refund | Delete | — | yes |
| C4102670 | ZZ_DELETE_REVIEW - Adjust two different-ref taps to SAME ref — ref.60 cap now applies, refund £1.30 | Delete | — | yes |
| C4102671 | ZZ_DELETE_REVIEW - Adjust higher-ref tap DOWN to match other — ref cap applies, refund | Delete | — | yes |
| C4102672 | ZZ_DELETE_REVIEW - Adjustment stays WITHIN Bangor TS zone — cap holds, no change | Delete | — | yes |
| C4102673 | ZZ_DELETE_REVIEW - Adjustment to HIGHER-fare stage OUTSIDE town area — cap removed, charge increases | Delete | — | yes |
| C4102674 | ZZ_DELETE_REVIEW - Adjustment to LOWER-fare stage OUTSIDE town area — cap removed, charge reduces | Delete | — | yes |
| C4102675 | ZZ_DELETE_REVIEW - Re-tap at same boarding stage after annulment is charged as first good tap (Metro) | Delete | TODEV-23967 | yes |
| C4102676 | ZZ_DELETE_REVIEW - Full Metro day reaches daily cap correctly after an annulment | Delete | TODEV-23967 | yes |
| C4102677 | ZZ_DELETE_REVIEW - Re-tap at same boarding stage after annulment counts as first ref fare tap (Ulsterbus) | Delete | TODEV-23967 | yes |
| C4102678 | ZZ_DELETE_REVIEW - Ulsterbus reference fare cap applies on correct tap after annulment | Delete | TODEV-23967 | yes |
| C4102679 | ZZ_DELETE_REVIEW - Re-tap after annulment in the ref.61 band caps at 8.20, not the adjacent ref.60 7.20 | Delete | TODEV-23967 | yes |
| C4102680 | ZZ_DELETE_REVIEW - Annulment in the ref.60 band does not borrow the higher ref.61 cap | Delete | TODEV-23967 | yes |
| C4102681 | ZZ_DELETE_REVIEW - Genuine duplicate (no annulment) at same stage is still rejected as 0.00 | Delete | TODEV-23967 | yes |
| C4102682 | ZZ_DELETE_REVIEW - Re-tap at a DIFFERENT boarding stage after annulment is a normal first tap | Delete | TODEV-23967 | yes |
| C4102683 | ZZ_DELETE_REVIEW - Annul the re-tap as well; a third tap is still the first good tap | Delete | TODEV-23967 | yes |
| C4102684 | ZZ_DELETE_REVIEW - Annulment processed in same settlement run as the re-tap | Delete | TODEV-23967 | yes |
| C4102685 | ZZ_DELETE_REVIEW - Annulment with no re-tap leaves no chargeable journey | Delete | TODEV-23967 | yes |
| C4102686 | ZZ_DELETE_REVIEW - Annulment of a tap that already had the daily cap applied does not corrupt the day | Delete | TODEV-23967 | yes |
| C4102687 | ZZ_DELETE_REVIEW - Annul the FIRST tap after the daily cap is already reached, then re-tap | Delete | TODEV-23967 | yes |
| C4102688 | ZZ_DELETE_REVIEW - Annulment on one card does not affect a duplicate-looking tap on another card | Delete | TODEV-23967 | yes |
| C4102689 | ZZ_DELETE_REVIEW - Ulsterbus re-tap at same boarding stage but DIFFERENT alighting stage and fare after annulment | Delete | TODEV-23967 | yes |
| C4102690 | ZZ_DELETE_REVIEW - Re-tap at same boarding stage WITHOUT a preceding annulment is a genuine duplicate | Delete | TODEV-23967 | yes |
| C4102691 | ZZ_DELETE_REVIEW - Multiple annulment+re-tap cycles in one day cap correctly | Delete | TODEV-23967 | yes |
| C4102692 | ZZ_DELETE_REVIEW - Annulment on a previous day does not affect the new day's first tap | Delete | TODEV-23967 | yes |
| C4102693 | ZZ_DELETE_REVIEW - A cancelled journey remains visible in Journey History after cancellation | Delete | TODEV-24061 | yes |
| C4102694 | ZZ_DELETE_REVIEW - A cancelled journey showing a 0.00 fare is still visible in Journey History | Delete | TODEV-24061 | yes |
| C4102695 | ZZ_DELETE_REVIEW - Editing the alighting stop on a cancelled tap keeps the journey visible | Delete | TODEV-24061 | yes |
| C4102696 | ZZ_DELETE_REVIEW - A stop-location update on a cancelled tap must not remove the audit record | Delete | TODEV-24061 | yes |
| C4102697 | ZZ_DELETE_REVIEW - REGRESSION - Editing the alighting stop on a NON-cancelled journey still works | Delete | TODEV-24061 | yes |
| C4102698 | ZZ_DELETE_REVIEW - REGRESSION - A cancelled journey stays cancelled after a stop correction and a further settlement | Delete | TODEV-24061 | yes |
| C4102699 | ZZ_DELETE_REVIEW - Cancelling one journey does not affect other visible journeys | Delete | TODEV-24061 | yes |
| C4102700 | ZZ_DELETE_REVIEW - Cancelling a charged journey produces a refund and the record is retained | Delete | TODEV-24061 | yes |
| C4102701 | ZZ_DELETE_REVIEW - Editing the stop on a cancelled tap AFTER settlement keeps the audit record | Delete | TODEV-24061 | yes |
| C4102702 | ZZ_DELETE_REVIEW - A cancelled transfer journey remains visible | Delete | TODEV-24061 | yes |
| C4102703 | ZZ_DELETE_REVIEW - Correcting the stop on a settled FREE (capped) tap keeps it at 0.00 | Delete | TODEV-24096 | yes |
| C4102704 | ZZ_DELETE_REVIEW - Correcting the stop on a settled PARTIALLY-capped tap keeps it at 1.70 | Delete | TODEV-24096 | yes |
| C4102705 | ZZ_DELETE_REVIEW - A stop correction on a capped tap must never push the card's daily total over 4.00 | Delete | TODEV-24096 | yes |
| C4102706 | ZZ_DELETE_REVIEW - REGRESSION - Correcting a settled capped tap keeps it settled and charged 0.00 | Delete | TODEV-24096 | yes |
| C4102707 | ZZ_DELETE_REVIEW - REGRESSION - Correcting the stop on the first (non-capped) tap leaves its 2.30 charge unchanged | Delete | TODEV-24096 | yes |
| C4102708 | ZZ_DELETE_REVIEW - REGRESSION - Correcting an UNSETTLED capped tap still re-evaluates correctly and stays free | Delete | TODEV-24096 | yes |
| C4102709 | ZZ_DELETE_REVIEW - REGRESSION - A declined journey is not treated as settled by the correction guard | Delete | TODEV-24096 | yes |
| C4102710 | ZZ_DELETE_REVIEW - REGRESSION - Re-running settlement after a correction does not re-charge the capped tap | Delete | TODEV-24096 | yes |
| C4102711 | ZZ_DELETE_REVIEW - Second Model 2 tap is flagged duplicate after a same-stage retail transaction | Delete | TODEV-24258 | yes |
| C4102712 | ZZ_DELETE_REVIEW - Both later TOO taps are duplicates including an out-of-order timestamp (dev PASSED) | Delete | TODEV-24258 | yes |
| C4102713 | ZZ_DELETE_REVIEW - Multiple interleaved retail transactions never reset the duplicate reference | Delete | TODEV-24258 | yes |
| C4102714 | ZZ_DELETE_REVIEW - REGRESSION - Retail transaction from a DIFFERENT stage still allows the duplicate (was already working) | Delete | TODEV-24258 | yes |
| C4102715 | ZZ_DELETE_REVIEW - A same-stage tap OUTSIDE the 15-minute window after a retail is NOT a duplicate | Delete | TODEV-24258 | yes |
| C4102716 | ZZ_DELETE_REVIEW - The Model 1 retail transaction itself is never flagged as a duplicate of a TOO tap | Delete | TODEV-24258 | yes |
| C4102717 | ZZ_DELETE_REVIEW - A later Model 2 tap from a DIFFERENT boarding stage is a genuine new tap, not a duplicate | Delete | TODEV-24258 | yes |
| C4102718 | ZZ_DELETE_REVIEW - A valid tap rejected as a duplicate is retained when the first tap is cancelled | Delete | TODEV-24259 | yes |
| C4102719 | ZZ_DELETE_REVIEW - Several same-stage taps then cancel the first - the next tap becomes the valid journey | Delete | TODEV-24259 | yes |
| C4102720 | ZZ_DELETE_REVIEW - No valid journey is left missing after the annulment | Delete | TODEV-24259 | yes |
| C4102721 | ZZ_DELETE_REVIEW - When the annulment is processed before the second tap, the second tap is a normal first journey | Delete | TODEV-24259 | yes |
| C4102722 | ZZ_DELETE_REVIEW - Cancelling the rehabilitated tap promotes the next tap in turn | Delete | TODEV-24259 | yes |
| C4102723 | ZZ_DELETE_REVIEW - Cancelling a tap with no following tap leaves nothing missing | Delete | TODEV-24259 | yes |
| C4102724 | ZZ_DELETE_REVIEW - A second tap from a different boarding stage is a valid journey and is unaffected by the annulment | Delete | TODEV-24259 | yes |
| C4102725 | ZZ_DELETE_REVIEW - Only stops with a fare greater than 0 are shown in the Update Stop list | Delete | TODEV-24300 | yes |
| C4102726 | ZZ_DELETE_REVIEW - Zero-fare (Transfer) stops are not shown | Delete | TODEV-24300 | yes |
| C4102727 | ZZ_DELETE_REVIEW - Valid stops with a positive fare are still shown | Delete | TODEV-24300 | yes |
| C4102728 | ZZ_DELETE_REVIEW - Selecting a valid positive-fare stop updates the journey correctly | Delete | TODEV-24300 | yes |
| C4102729 | ZZ_DELETE_REVIEW - A zero-fare stop is hidden but the smallest positive-fare stop is shown | Delete | TODEV-24300 | yes |
| C4102730 | ZZ_DELETE_REVIEW - A 0.00 journey from hitting the daily cap stays visible and editable | Delete | TODEV-24300 | yes |
| C4102731 | ZZ_DELETE_REVIEW - A cancelled 0.00 journey stays visible and editable | Delete | TODEV-24300 | yes |
| C4102732 | ZZ_DELETE_REVIEW - A transfer journey (0.00 fare) stays displayed in Journey History | Delete | TODEV-24300 | yes |
| C4102733 | ZZ_DELETE_REVIEW - A stop with a negative fare is not shown | Delete | TODEV-24300 | yes |
| C4102734 | ZZ_DELETE_REVIEW - Transfer stops that have a positive fare still appear | Delete | TODEV-24300 | yes |
| C4102735 | ZZ_DELETE_REVIEW - TVM-only stops with a positive fare still appear (tracked separately) | Delete | TODEV-24300 | yes |
| C4102736 | ZZ_DELETE_REVIEW - Correcting a Zone 1 tap into Zone 2 (cap already reached) audits a 0.00 free tap under the Zone 2 cap | Delete | TODEV-24348 | yes |
| C4102737 | ZZ_DELETE_REVIEW - The account aggregated total is unchanged by the correction | Delete | TODEV-24348 | yes |
| C4102738 | ZZ_DELETE_REVIEW - The cap shown after the correction is the zonal cap, not a reference cap | Delete | TODEV-24348 | yes |
| C4102739 | ZZ_DELETE_REVIEW - Correcting into a zone whose cap is NOT yet reached charges toward the zonal cap, not the reference cap | Delete | TODEV-24348 | yes |
| C4102740 | ZZ_DELETE_REVIEW - REGRESSION - A journey with no applicable zonal cap still uses the UB reference cap correctly | Delete | TODEV-24348 | yes |
| C4102741 | ZZ_DELETE_REVIEW - EDGE - Correcting to another stop in the SAME zone keeps the zonal cap | Delete | TODEV-24348 | yes |
| C4102742 | ZZ_DELETE_REVIEW - REGRESSION - Re-running settlement after the correction keeps the zonal cap and adds no charge | Delete | TODEV-24348 | yes |
| C4102743 | ZZ_DELETE_REVIEW - EDGE - The zonal cap (Transport Mode All) applies after a correction regardless of transport mode | Delete | TODEV-24348 | yes |
| C4102744 | ZZ_DELETE_REVIEW - A settled TOO journey from Greys Farm on 72b shows 14 stops, not "No options" | Delete | TODEV-24397 | yes |
| C4102745 | ZZ_DELETE_REVIEW - A settled TOO journey from Moygashel Busby Shop on 72b shows 15 stops, not "No options" | Delete | TODEV-24397 | yes |
| C4102746 | ZZ_DELETE_REVIEW - Both settled ref.60 taps from the same boarding stage populate the dropdown | Delete | TODEV-24397 | yes |
| C4102747 | ZZ_DELETE_REVIEW - Re-opening the Update Stop modal always populates the dropdown (not sporadic) | Delete | TODEV-24397 | yes |
| C4102748 | ZZ_DELETE_REVIEW - "No options" is correct when the boarding stage is the last stop on the route | Delete | TODEV-24397 | yes |
| C4102749 | ZZ_DELETE_REVIEW - With the correct operator the stops are shown; a mismatched operator id returns none (user error) | Delete | TODEV-24397 | yes |
| C4102750 | ZZ_DELETE_REVIEW - A recoverable debt is recovered and the card returns to Active (mirrors FHTM-28476) | Delete | TODEV-24990 | yes |
| C4102751 | ZZ_DELETE_REVIEW - An unrecoverable debt leaves the cards Blocked (mirrors FHTM-28477) | Delete | TODEV-24990 | yes |
| C4102752 | ZZ_DELETE_REVIEW - Visa MIT recovery clears a recoverable issuer-liability debt | Delete | TODEV-24990 | yes |
| C4102753 | ZZ_DELETE_REVIEW - A successful recovery removes the card from the Deny List | Delete | TODEV-24990 | yes |
| C4102754 | ZZ_DELETE_REVIEW - The recovered account is visible in the Operator Portal with the correct status (mirrors FHTM-28474) | Delete | TODEV-24990 | yes |
| C4102755 | ZZ_DELETE_REVIEW - The enhanced open-payment-bs logging is verified by the dev automated tests, not manual QA | Delete | TODEV-24990 | yes |
| C4102803 | ZZ_DELETE_REVIEW - Annulling the first capped-day tap then re-tapping restores correct totals | Delete | TODEV-23967 | yes |
| C4102809 | ZZ_DELETE_REVIEW - A valid tap rejected as duplicate is retained when the first tap is cancelled | Delete | TODEV-24259 | yes |
| C4102810 | ZZ_DELETE_REVIEW - Several same-stage taps then cancelling the first promotes the next valid tap | Delete | TODEV-24259 | yes |
| C4102811 | ZZ_DELETE_REVIEW - No valid journey is left missing after the annulment | Delete | TODEV-24259 | yes |
| C4102813 | ZZ_DELETE_REVIEW - Cancelling the rehabilitated tap promotes the next tap in turn | Delete | TODEV-24259 | yes |
| C4102815 | ZZ_DELETE_REVIEW - A second tap from a different stage is unaffected by the annulment | Delete | TODEV-24259 | yes |
| C4102827 | ZZ_DELETE_REVIEW - Journey History — correcting a non-cancelled journey keeps it active at its new fare (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4102833 | ZZ_DELETE_REVIEW - Journey History — a settled TOO journey offers onward stops for correction (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102834 | ZZ_DELETE_REVIEW - Journey History — a settled TOO journey from another stage offers onward stops (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102835 | ZZ_DELETE_REVIEW - Journey History — two settled ref.60 taps from the same stage each offer onward stops (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102836 | ZZ_DELETE_REVIEW - Journey History — re-opening the correction always offers the onward stops (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102837 | ZZ_DELETE_REVIEW - Journey History — no onward stops offered when boarding is the last stop on the route (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102838 | ZZ_DELETE_REVIEW - Journey History — correction offers stops for the journey's operator (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24397 | yes |
| C4102825 | ZZ_DELETE_REVIEW - Journey History — correcting the alighting stop on a cancelled tap keeps it visible (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4102826 | ZZ_DELETE_REVIEW - Journey History — a zero-fare correction on a cancelled tap leaves one visible row (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4102828 | ZZ_DELETE_REVIEW - Journey History — a cancelled journey stays cancelled after a stop correction and further settlement (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4102831 | ZZ_DELETE_REVIEW - Journey History — correcting the stop on a refunded cancelled tap keeps one record and raises no further refund (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24061 | yes |
| C4102845 | ZZ_DELETE_REVIEW - Journey History — a cancelled £0.00 journey stays visible and correctable (CR122) | Delete | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102960 | ZZ_DELETE_REVIEW - Sign On — valid credentials reach the CloudFare Dashboard | Delete / CloudFare / Sign On & Access | — | yes |
| C4102961 | ZZ_DELETE_REVIEW - Sign On — Google account sign-on (UNVERIFIED) | Delete / CloudFare / Sign On & Access | — | yes |
| C4102962 | ZZ_DELETE_REVIEW - Sign On — user can sign off CloudFare | Delete / CloudFare / Sign On & Access | — | yes |
| C4102963 | ZZ_DELETE_REVIEW - Configure report access for a role | Delete / CloudFare / Roles & Profiles | FBD-100342 | yes |
| C4102964 | ZZ_DELETE_REVIEW - Configure module and group access for a role | Delete / CloudFare / Roles & Profiles | FBD-100342 | yes |
| C4102965 | ZZ_DELETE_REVIEW - Settings — each Settings option opens its page | Delete / CloudFare / Settings | — | yes |
| C4102966 | ZZ_DELETE_REVIEW - Settings — Event Codes view/add/edit/import | Delete / CloudFare / Settings | — | yes |
| C4102967 | ZZ_DELETE_REVIEW - Settings — Operating Units add/edit/delete | Delete / CloudFare / Settings | — | yes |
| C4102968 | ZZ_DELETE_REVIEW - Settings — Scheduled Tasks enable/disable purges | Delete / CloudFare / Settings | — | yes |
| C4102969 | ZZ_DELETE_REVIEW - Settings — System Settings edit value / VAT / feature toggle | Delete / CloudFare / Settings | — | yes |
| C4102970 | ZZ_DELETE_REVIEW - Settings — edit a Notifications value | Delete / CloudFare / Settings | — | yes |
| C4102971 | ZZ_DELETE_REVIEW - Settings — edit External Interface Settings | Delete / CloudFare / Settings | — | yes |
| C4102972 | ZZ_DELETE_REVIEW - Settings — edit a Scheduled Adherence threshold | Delete / CloudFare / Settings | — | yes |
| C4102973 | ZZ_DELETE_REVIEW - ExternalInfo/StaffCash API returns staff cash for a date range | Delete / CloudFare / API | — | yes |
| C4102974 | ZZ_DELETE_REVIEW - ExternalInfo/StaffCash API handles invalid requests and BST/GMT | Delete / CloudFare / API | — | yes |
| C4102976 | ZZ_DELETE_REVIEW - Topology & Fares Management — each menu option opens its page | Delete / CloudFare / Topology & Fares / Setup & Import | — | yes |
| C4102977 | ZZ_DELETE_REVIEW - Topology filter — services and routes filter by operator | Delete / CloudFare / Topology & Fares / Setup & Import | FBD-100385, FBD-100698 | yes |
| C4102978 | ZZ_DELETE_REVIEW - Fares export — configured fares are exported | Delete / CloudFare / Topology & Fares / Setup & Import | FBD-100296, FBD-100336, FBD-100385 | yes |
| C4102979 | ZZ_DELETE_REVIEW - Import Map Point File — stops are added and existing stops updated | Delete / CloudFare / Topology & Fares / Setup & Import | FBD-100296 | yes |
| C4102980 | ZZ_DELETE_REVIEW - Import route data at parent and child operator level | Delete / CloudFare / Topology & Fares / Setup & Import | FBD-100296 | yes |
| C4102981 | ZZ_DELETE_REVIEW - Drawing Tool — add a new map point with a linked stop | Delete / CloudFare / Topology & Fares / Drawing Tool | — | yes |
| C4102982 | ZZ_DELETE_REVIEW - Drawing Tool — create, edit and delete a zone | Delete / CloudFare / Topology & Fares / Drawing Tool | — | yes |
| C4102983 | ZZ_DELETE_REVIEW - Drawing Tool — configure positional points on a route | Delete / CloudFare / Topology & Fares / Drawing Tool | — | yes |
| C4102984 | ZZ_DELETE_REVIEW - Drawing Tool — export map points to CSV and re-import edits | Delete / CloudFare / Topology & Fares / Drawing Tool | — | yes |
| C4102985 | ZZ_DELETE_REVIEW - Drawing Tool — search for a map point | Delete / CloudFare / Topology & Fares / Drawing Tool | — | yes |
| C4102986 | ZZ_DELETE_REVIEW - Route Management — create, amend, copy and delete a route | Delete / CloudFare / Topology & Fares / Route Management | FBD-100296 | yes |
| C4102987 | ZZ_DELETE_REVIEW - Route — service and public route code configured | Delete / CloudFare / Topology & Fares / Route Management | FBD-100296, REQ-3291 | yes |
| C4102988 | ZZ_DELETE_REVIEW - Route — enable ABT flat fare | Delete / CloudFare / Topology & Fares / Route Management | FBD-100296 | yes |
| C4102989 | ZZ_DELETE_REVIEW - Route — enable Multi-Journey transfers and set the transfer time | Delete / CloudFare / Topology & Fares / Route Management | FBD-100698 | yes |
| C4102990 | ZZ_DELETE_REVIEW - Route — configure the fares triangle and calculate a fare | Delete / CloudFare / Topology & Fares / Route Management | FBD-100296, FBD-100336 | yes |
| C4102991 | ZZ_DELETE_REVIEW - Route — ETM rail substitution service | Delete / CloudFare / Topology & Fares / Route Management | FBD-100698 | yes |
| C4102992 | ZZ_DELETE_REVIEW - Product — a product is configured and saved | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4102993 | ZZ_DELETE_REVIEW - Product — an ABT product is configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4102994 | ZZ_DELETE_REVIEW - Product — an Open product is configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4102995 | ZZ_DELETE_REVIEW - Product — a FLU product is configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4102996 | ZZ_DELETE_REVIEW - Product — a Preset Reverse FLU product is configured | Delete / CloudFare / Topology & Fares / Products | FBD-100268, REQ-0516, REQ-1592, REQ-1862 | yes |
| C4102997 | ZZ_DELETE_REVIEW - Product — a Reference Type product is configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4102998 | ZZ_DELETE_REVIEW - Product — an Excess (open-value) product is configured | Delete / CloudFare / Topology & Fares / Products | FBD-100268 | yes |
| C4102999 | ZZ_DELETE_REVIEW - Product — a Smartcard product is configured (WTS SmartCreate / SmartRecharge) | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103000 | ZZ_DELETE_REVIEW - Product — barcode printing configured on a paper ticket product | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103001 | ZZ_DELETE_REVIEW - Product — default alighting stage configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103002 | ZZ_DELETE_REVIEW - Product — annulment allowed configured per device type | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103003 | ZZ_DELETE_REVIEW - Product — Passback Time configured | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103004 | ZZ_DELETE_REVIEW - Product buttons — assigned via Menu product groups per device | Delete / CloudFare / Topology & Fares / Products | FBD-100293 | yes |
| C4103005 | ZZ_DELETE_REVIEW - Product Group — create and edit a FLU group per device type | Delete / CloudFare / Topology & Fares / Products | — | yes |
| C4103006 | ZZ_DELETE_REVIEW - Product — assignment expiry / enablement | Delete / CloudFare / Topology & Fares / Products | FBD-100268, FBD-100385 | yes |
| C4103007 | ZZ_DELETE_REVIEW - Fares rule — a new rule is added | Delete / CloudFare / Topology & Fares / Rules | FBD-100385 | yes |
| C4103008 | ZZ_DELETE_REVIEW - Rule — e-Purse single fare charge | Delete / CloudFare / Topology & Fares / Rules | — | yes |
| C4103009 | ZZ_DELETE_REVIEW - Rule — fixed fare (including smartcard fixed fare) | Delete / CloudFare / Topology & Fares / Rules | — | yes |
| C4103010 | ZZ_DELETE_REVIEW - Card Reference File validates alighting stages across devices | Delete / CloudFare / Topology & Fares / Card Reference File | — | yes |
| C4103011 | ZZ_DELETE_REVIEW - Topology — label prepared configuration data | Delete / CloudFare / Topology & Fares / Labeling & Publishing | — | yes |
| C4103012 | ZZ_DELETE_REVIEW - Topology — publish configuration with a future transition date | Delete / CloudFare / Topology & Fares / Labeling & Publishing | — | yes |
| C4103013 | ZZ_DELETE_REVIEW - Topology — re-publish an older configuration | Delete / CloudFare / Topology & Fares / Labeling & Publishing | — | yes |
| C4103014 | ZZ_DELETE_REVIEW - Topology — delete an active published topology label | Delete / CloudFare / Topology & Fares / Labeling & Publishing | — | yes |
| C4103031 | ZZ_DELETE_REVIEW - Activity Log — filter by activity, device, and date/time | Delete / CloudFare / Estate Management / Activity Log | — | yes |
| C4103032 | ZZ_DELETE_REVIEW - Activity Log — page through results | Delete / CloudFare / Estate Management / Activity Log | — | yes |
| C4103033 | ZZ_DELETE_REVIEW - Activity Log — shows transactions, events and staff activity with detail | Delete / CloudFare / Estate Management / Activity Log | — | yes |
| C4103034 | ZZ_DELETE_REVIEW - Activity Log — filter by barcode ID | Delete / CloudFare / Estate Management / Activity Log | — | yes |
| C4103035 | ZZ_DELETE_REVIEW - Activity Log — failed validations, declined taps and failed payments are identified with reason | Delete / CloudFare / Estate Management / Activity Log | — | yes |
| C4103036 | ZZ_DELETE_REVIEW - Device Details — view and edit device information | Delete / CloudFare / Estate Management / Asset Manager | FBD-100263 | yes |
| C4103037 | ZZ_DELETE_REVIEW - Device — status set from Device Details page | Delete / CloudFare / Estate Management / Asset Manager | FBD-100263 | yes |
| C4103038 | ZZ_DELETE_REVIEW - Quick Product Assignment — add, remove and abandon products | Delete / CloudFare / Estate Management / Asset Manager | — | yes |
| C4103039 | ZZ_DELETE_REVIEW - Comms Monitor — recent activity, search, filter and report | Delete / CloudFare / Estate Management / Comms Monitor | — | yes |
| C4103040 | ZZ_DELETE_REVIEW - Comms Monitor — change of operating company | Delete / CloudFare / Estate Management / Comms Monitor | — | yes |
| C4103041 | ZZ_DELETE_REVIEW - Device dataset — create and modify a version | Delete / CloudFare / Estate Management / Device Dataset Deployment | — | yes |
| C4103042 | ZZ_DELETE_REVIEW - Device software — upload and configure a version | Delete / CloudFare / Estate Management / Device Dataset Deployment | — | yes |
| C4103043 | ZZ_DELETE_REVIEW - Device dataset — change version state and deploy | Delete / CloudFare / Estate Management / Device Dataset Deployment | — | yes |
| C4103044 | ZZ_DELETE_REVIEW - Staff Manager — add a staff member | Delete / CloudFare / Estate Management / Staff Manager | — | yes |
| C4103045 | ZZ_DELETE_REVIEW - Staff Manager — modify a staff member's PIN | Delete / CloudFare / Estate Management / Staff Manager | — | yes |
| C4103046 | ZZ_DELETE_REVIEW - Staff Manager — modify home and working location | Delete / CloudFare / Estate Management / Staff Manager | — | yes |
| C4103047 | ZZ_DELETE_REVIEW - Staff Manager — view staff history | Delete / CloudFare / Estate Management / Staff Manager | — | yes |
| C4103048 | ZZ_DELETE_REVIEW - Filter quarantined data by device | Delete / CloudFare / Estate Management / Quarantined Data | — | yes |
| C4103049 | ZZ_DELETE_REVIEW - Edit and resubmit quarantined data | Delete / CloudFare / Estate Management / Quarantined Data | — | yes |
| C4103050 | ZZ_DELETE_REVIEW - Navigate the Commands Viewer | Delete / CloudFare / Estate Management / Commands Viewer | — | yes |
| C4103055 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Dashboard — summary tiles show their metrics | Delete / CloudFare / Dashboard | FBD-100263, FBD-100347, REQ-3585 | yes |
| C4103056 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Create, clone, favourite and delete a dashboard | Delete / CloudFare / Dashboard | FBD-100347, REQ-3585 | yes |
| C4103057 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Add and remove dashboard tiles | Delete / CloudFare / Dashboard | FBD-100347 | yes |
| C4103058 | ZZ_DELETE_REVIEW - [UNCONFIRMED] View a dashboard full screen | Delete / CloudFare / Dashboard | FBD-100347 | yes |
| C4103059 | ZZ_DELETE_REVIEW - Events & Alerts — create, view, edit and delete an alert configuration | Delete / CloudFare / Events & Alerts | — | yes |
| C4103060 | ZZ_DELETE_REVIEW - Alert Viewer — filter, acknowledge then clear alerts | Delete / CloudFare / Events & Alerts | — | yes |
| C4103061 | ZZ_DELETE_REVIEW - Events & Alerts — configure event groups | Delete / CloudFare / Events & Alerts | — | yes |
| C4103062 | ZZ_DELETE_REVIEW - Events Viewer — filter the events list | Delete / CloudFare / Events & Alerts | — | yes |
| C4103063 | ZZ_DELETE_REVIEW - Depot Location Report — generates and exports | Delete / CloudFare / Reports | — | yes |
| C4103064 | ZZ_DELETE_REVIEW - Devices Last Seen Report — generates and exports | Delete / CloudFare / Reports | — | yes |
| C4103065 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Software Versions Report | Delete / CloudFare / Reports | FBD-100263 | yes |
| C4103066 | ZZ_DELETE_REVIEW - Staff Activity Report — generates and exports | Delete / CloudFare / Reports | REQ-2499 | yes |
| C4103067 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Engineer Visits Report | Delete / CloudFare / Reports | FBD-100263 | yes |
| C4103068 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Revenue Inspector's Report | Delete / CloudFare / Reports | FBD-100263, FBD-100306, FBD-100716 | yes |
| C4103069 | ZZ_DELETE_REVIEW - [UNCONFIRMED] TVM cash collection reports | Delete / CloudFare / Reports | — | yes |
| C4103070 | ZZ_DELETE_REVIEW - [UNCONFIRMED] TVM cash revenue reports | Delete / CloudFare / Reports | FBD-100276 | yes |
| C4103071 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Rules List Export | Delete / CloudFare / Reports | — | yes |
| C4103072 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Concise Area & Reference Fare Report | Delete / CloudFare / Reports | — | yes |
| C4103073 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Route List Export | Delete / CloudFare / Reports | — | yes |
| C4103074 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Product to Ticket Assignment Report | Delete / CloudFare / Reports | — | yes |
| C4103075 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Product List Report | Delete / CloudFare / Reports | — | yes |
| C4103076 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Events & Alerts Report | Delete / CloudFare / Reports | — | yes |
| C4103077 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Vehicle Check Report | Delete / CloudFare / Reports | — | yes |
| C4103078 | ZZ_DELETE_REVIEW - [UNCONFIRMED] CloudFare Usage Report | Delete / CloudFare / Reports | — | yes |
| C4103079 | ZZ_DELETE_REVIEW - Reports — audit data flows end to end into a report | Delete / CloudFare / Reports | FBD-100356, FBD-100387 | yes |
| C4103080 | ZZ_DELETE_REVIEW - Ticket Editor — create a ticket template | Delete / CloudFare / Ticket Editor | — | yes |
| C4103081 | ZZ_DELETE_REVIEW - Ticket Editor — add elements to a template | Delete / CloudFare / Ticket Editor | — | yes |
| C4103082 | ZZ_DELETE_REVIEW - Ticket Editor — copy a template and change its device type | Delete / CloudFare / Ticket Editor | — | yes |
| C4103083 | ZZ_DELETE_REVIEW - Ticket Editor — configure a change ticket (NOT IN SPEC) | Delete / CloudFare / Ticket Editor | FBD-100363 | yes |
| C4103084 | ZZ_DELETE_REVIEW - Product Editor — assign a ticket template to a product | Delete / CloudFare / Ticket Editor | — | yes |
| C4103085 | ZZ_DELETE_REVIEW - Ticket Editor — group a set of ticket layouts (NOT IN SPEC) | Delete / CloudFare / Ticket Editor | FBD-100363 | yes |
| C4103086 | ZZ_DELETE_REVIEW - Ticket Editor — add a barcode to a template | Delete / CloudFare / Ticket Editor | — | yes |
| C4103087 | ZZ_DELETE_REVIEW - Ticket Editor — add payment-card fields to a template | Delete / CloudFare / Ticket Editor | — | yes |
| C4103088 | ZZ_DELETE_REVIEW - Station Manager — create a rail line and station | Delete / CloudFare / Station Manager | — | yes |
| C4103089 | ZZ_DELETE_REVIEW - Station Manager — delete or change a station | Delete / CloudFare / Station Manager | — | yes |
| C4103090 | ZZ_DELETE_REVIEW - Station Manager — add a branch | Delete / CloudFare / Station Manager | — | yes |
| C4103143 | ZZ_DELETE_REVIEW - View the available reports in the Merit Web Reporter | Delete / Merit Web Reporter / Report Viewer | — | yes |
| C4103144 | ZZ_DELETE_REVIEW - View and export a report in the Merit Web Reporter | Delete / Merit Web Reporter / Report Viewer | FBD-100306 | yes |
| C4103159 | ZZ_DELETE_REVIEW - Smartrack access rights for administrator and user | Delete / Smartrack / Access | — | yes |
| C4103160 | ZZ_DELETE_REVIEW - Smartrack — view and search card data | Delete / Smartrack / Card Data | — | yes |
| C4103161 | ZZ_DELETE_REVIEW - Smartrack — add notes and attached files to a card | Delete / Smartrack / Card Data | — | yes |
| C4103162 | ZZ_DELETE_REVIEW - Smartrack — view card transactions | Delete / Smartrack / Card Data | — | yes |
| C4103163 | ZZ_DELETE_REVIEW - Smartrack — import a card issue and pass-create record file | Delete / Smartrack / Import & Export | — | yes |
| C4103164 | ZZ_DELETE_REVIEW - Smartrack — export the ESN list | Delete / Smartrack / Import & Export | FBD-100385 | yes |
| C4103165 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Action List reports (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103166 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Liability and Scheme Liability reports (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103167 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Default Payment report (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103168 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Delivery report (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103169 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Refund report (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103170 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the Decommission Card report (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103171 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Run the POS Revenue Analysis report (Smartrack) | Delete / Smartrack / Reports | REQ-2375 | yes |
| C4103093 | ZZ_DELETE_REVIEW - Merit — edit period, roll-over time and start of week (Date Editor) | Delete / Merit / Administration | — | yes |
| C4103094 | ZZ_DELETE_REVIEW - Merit — configure a timeband (Timeband Editor) | Delete / Merit / Administration | — | yes |
| C4103095 | ZZ_DELETE_REVIEW - Merit — edit staff and operator details (Staff Editor) | Delete / Merit / Administration | — | yes |
| C4103096 | ZZ_DELETE_REVIEW - Merit — edit class types and class groups | Delete / Merit / Administration | — | yes |
| C4103097 | ZZ_DELETE_REVIEW - Merit — edit locations, location groups and location restrictions | Delete / Merit / Administration | — | yes |
| C4103098 | ZZ_DELETE_REVIEW - Merit — edit route groups (Route Group Editor) | Delete / Merit / Administration | — | yes |
| C4103099 | ZZ_DELETE_REVIEW - Merit — configure route revenue allocation (Route Revenue Editor) | Delete / Merit / Administration | FBD-100341, REQ-2066, REQ-2137, REQ-2153, REQ-2754, REQ-3285 | yes |
| C4103100 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Sales Breakdown reports — generate and export | Delete / Merit / Analysis Reports | FBD-100306 | yes |
| C4103101 | ZZ_DELETE_REVIEW - Sales Analysis by Class report — generates and exports | Delete / Merit / Analysis Reports | — | yes |
| C4103102 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Origin and Destination reports | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212 | yes |
| C4103103 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Bus Loading by Route/Journey report | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212 | yes |
| C4103104 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Route/Stage reports | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212, REQ-1993 | yes |
| C4103105 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Journey Analysis reports | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212, REQ-1993, REQ-2005, REQ-2012 | yes |
| C4103106 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Stage Timeband report | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212, REQ-1993, REQ-2012 | yes |
| C4103107 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Patronage Timeband report | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212, REQ-1993 | yes |
| C4103108 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Revenue and Revenue by Stop reports | Delete / Merit / Analysis Reports | FBD-100306, FBD-100356 | yes |
| C4103109 | ZZ_DELETE_REVIEW - Class Breakdown and Route Breakdown reports — generate and export | Delete / Merit / Analysis Reports | FBD-100306 | yes |
| C4103110 | ZZ_DELETE_REVIEW - [UNCONFIRMED] POS Revenue report | Delete / Merit / Analysis Reports | FBD-100306, FBD-100341, REQ-1212 | yes |
| C4103111 | ZZ_DELETE_REVIEW - Duty Comparison and Driver Shift reports — generate and export | Delete / Merit / Analysis Reports | — | yes |
| C4103112 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Bus Serviceability Final Defects report | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212 | yes |
| C4103113 | ZZ_DELETE_REVIEW - [UNCONFIRMED] GPS reports | Delete / Merit / Analysis Reports | FBD-100306, FBD-100347, REQ-1212, REQ-1993 | yes |
| C4103114 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Route Purchase report | Delete / Merit / Analysis Reports | FBD-100306, REQ-1212 | yes |
| C4103115 | ZZ_DELETE_REVIEW - Pay-In Reconciliation report — generates and exports | Delete / Merit / Analysis Reports | FBD-100306 | yes |
| C4103116 | ZZ_DELETE_REVIEW - Class Revenue Performance report — generates and exports | Delete / Merit / Revenue Performance Reports | FBD-100341 | yes |
| C4103117 | ZZ_DELETE_REVIEW - Route Revenue Performance report — generates and exports | Delete / Merit / Revenue Performance Reports | FBD-100341 | yes |
| C4103118 | ZZ_DELETE_REVIEW - Period Trend Analysis reports — generate and export | Delete / Merit / Revenue Performance Reports | FBD-100341 | yes |
| C4103119 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Tickets By Operator report | Delete / Merit / Revenue Performance Reports | FBD-100341, TIBU-17536, TIBU-22350 | yes |
| C4103120 | ZZ_DELETE_REVIEW - [UNCONFIRMED] NIR Revenue Performance reports | Delete / Merit / Revenue Performance Reports | FBD-100341, REQ-1212, REQ-1967, REQ-1989, REQ-1993, REQ-2000, REQ-2323, REQ-2327 | yes |
| C4103121 | ZZ_DELETE_REVIEW - [UNCONFIRMED] NIR Period Trend Analysis reports | Delete / Merit / Revenue Performance Reports | REQ-1212, REQ-1967, REQ-1989, REQ-1993, REQ-2000, REQ-2330, REQ-2334 | yes |
| C4103122 | ZZ_DELETE_REVIEW - [UNCONFIRMED] BRT Revenue Performance reports | Delete / Merit / Revenue Performance Reports | — | yes |
| C4103123 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Glider Revenue Performance reports | Delete / Merit / Revenue Performance Reports | — | yes |
| C4103124 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Ticketing Reports including timebands | Delete / Merit / Revenue Performance Reports | — | yes |
| C4103125 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Revenue Foregone reports | Delete / Merit / Concessionary Reports | FBD-100341, REQ-1212, REQ-1993 | yes |
| C4103126 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Concessionary Class Summary reports | Delete / Merit / Concessionary Reports | — | yes |
| C4103127 | ZZ_DELETE_REVIEW - [UNCONFIRMED] ENTCS Passenger and Revenue reports | Delete / Merit / Concessionary Reports | REQ-1212, REQ-2388 | yes |
| C4103128 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Fare Foregone reports | Delete / Merit / Concessionary Reports | — | yes |
| C4103129 | ZZ_DELETE_REVIEW - Daily Summary report — generates and exports | Delete / Merit / Daily Reports | — | yes |
| C4103130 | ZZ_DELETE_REVIEW - Daily Audit reports — generate and export | Delete / Merit / Daily Reports | FBD-100306 | yes |
| C4103131 | ZZ_DELETE_REVIEW - Class Audit and Route Audit reports — generate and export | Delete / Merit / Daily Reports | — | yes |
| C4103132 | ZZ_DELETE_REVIEW - Annulled Tickets report — generates and exports | Delete / Merit / Daily Reports | — | yes |
| C4103133 | ZZ_DELETE_REVIEW - Inspector's Report — generates and exports | Delete / Merit / Daily Reports | — | yes |
| C4103134 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Outstanding Duties report | Delete / Merit / Daily Reports | FBD-100306, REQ-1212, REQ-2255 | yes |
| C4103135 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Stage List report | Delete / Merit / Daily Reports | FBD-100306, REQ-1993 | yes |
| C4103136 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Origin and Destination Distance reports | Delete / Merit / Distance Reports | FBD-100306, REQ-1212, REQ-1993, REQ-2012 | yes |
| C4103137 | ZZ_DELETE_REVIEW - [UNCONFIRMED] Route Distance Analysis report | Delete / Merit / Distance Reports | FBD-100306 | yes |
| C4103138 | ZZ_DELETE_REVIEW - Merit — Ulsterbus revenue stored procedures | Delete / Merit / Stored Procedures | FBD-100356 | yes |
| C4103139 | ZZ_DELETE_REVIEW - Merit — Metro revenue stored procedures | Delete / Merit / Stored Procedures | FBD-100356 | yes |
| C4103140 | ZZ_DELETE_REVIEW - Merit — NIR rail revenue stored procedures | Delete / Merit / Stored Procedures | FBD-100356 | yes |
| C4103141 | ZZ_DELETE_REVIEW - Synchronise staff into Merit | Delete / Merit / Synchronisation & Tools | — | yes |
| C4103142 | ZZ_DELETE_REVIEW - Browse audit data with Client Tools | Delete / Merit / Synchronisation & Tools | — | yes |
| C4102757 | ZZ_DELETE_REVIEW - Metro cap — same-fare alighting correction holds the cap | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4102758 | ZZ_DELETE_REVIEW - Metro cap — correction outside the Metro zone removes the cap and charges the difference | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4102759 | ZZ_DELETE_REVIEW - Metro cap — correction into the Metro zone applies the cap and refunds the difference | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026 | yes |
| C4102760 | ZZ_DELETE_REVIEW - Metro cap — correcting a settled free (capped) tap keeps it at £0.00 | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102761 | ZZ_DELETE_REVIEW - Metro cap — correcting a settled partially-capped tap keeps it at £1.70 | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102762 | ZZ_DELETE_REVIEW - Metro cap — a correction never pushes the day over the cap | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102763 | ZZ_DELETE_REVIEW - Metro cap — a corrected capped tap stays settled and free | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102764 | ZZ_DELETE_REVIEW - Metro cap — correcting the first full-fare tap leaves its charge unchanged | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102765 | ZZ_DELETE_REVIEW - Metro cap — correcting an unsettled capped tap re-evaluates and stays free | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102766 | ZZ_DELETE_REVIEW - Metro cap — a declined journey is not treated as a settled capped tap | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102767 | ZZ_DELETE_REVIEW - Metro cap — re-running settlement after a correction does not re-charge the capped tap | Delete / Metro Daily Cap | FBD-100662, GEORGE-2026, TODEV-24096 | yes |
| C4102768 | ZZ_DELETE_REVIEW - Zonal cap — higher-fare correction within the zone holds the cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4102769 | ZZ_DELETE_REVIEW - Zonal cap — higher-fare correction outside the zone removes the cap and charges the difference | Delete / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4102770 | ZZ_DELETE_REVIEW - Zonal cap — lower-fare correction within the zone, day still above cap, holds | Delete / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4102771 | ZZ_DELETE_REVIEW - Zonal cap — lower-fare correction drops the day below cap and refunds | Delete / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4102772 | ZZ_DELETE_REVIEW - Zonal cap — Zone 4 correction within the highest band holds the cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026 | yes |
| C4102773 | ZZ_DELETE_REVIEW - Zonal cap — correction into a capped zone audits a free tap under the zonal cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102774 | ZZ_DELETE_REVIEW - Zonal cap — a correction into a capped zone does not increase the account total | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102775 | ZZ_DELETE_REVIEW - Zonal cap — a corrected tap reports under the zonal cap, not a reference cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102776 | ZZ_DELETE_REVIEW - Zonal cap — correcting into a zone below cap charges toward the zonal cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102777 | ZZ_DELETE_REVIEW - Reference cap — a journey with no zonal cap still uses the reference cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102778 | ZZ_DELETE_REVIEW - Zonal cap — correcting to another stop in the same zone keeps the cap | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102779 | ZZ_DELETE_REVIEW - Zonal cap — re-running settlement after a correction adds no charge | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102780 | ZZ_DELETE_REVIEW - Zonal cap — the cap applies after a correction regardless of transport mode | Delete / Zonal Cap | FBD-100662, GEORGE-2026, TODEV-24348 | yes |
| C4102781 | ZZ_DELETE_REVIEW - Reference cap — correction to a higher ref removes the cap and charges the difference | Delete / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4102782 | ZZ_DELETE_REVIEW - Reference cap — correction to a lower ref below the cap removes it and refunds | Delete / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4102783 | ZZ_DELETE_REVIEW - Reference cap — correction to a lower ref still above the cap charges the extra | Delete / Reference Fare Cap | FBD-100662, GEORGE-2026 | yes |
| C4102784 | ZZ_DELETE_REVIEW - Uncapped tap — single tap raised to a higher fare charges the difference | Delete / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4102785 | ZZ_DELETE_REVIEW - Uncapped tap — single tap lowered refunds the difference | Delete / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4102786 | ZZ_DELETE_REVIEW - Reference cap — aligning two different-ref taps to the same ref applies the cap and refunds | Delete / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4102787 | ZZ_DELETE_REVIEW - Reference cap — lowering the higher-ref tap to match applies the lower cap and refunds | Delete / Tap Correction / Uncapped & Single Taps | FBD-100662, GEORGE-2026 | yes |
| C4102788 | ZZ_DELETE_REVIEW - Town service cap — correction within the town zone holds the cap | Delete / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4102789 | ZZ_DELETE_REVIEW - Town service cap — correction outside the town to a higher fare removes the cap and charges the difference | Delete / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4102790 | ZZ_DELETE_REVIEW - Town service cap — correction outside the town to a lower fare removes the cap and refunds | Delete / Tap Correction / Town Service Cap | FBD-100662, GEORGE-2026 | yes |
| C4102839 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — fare-based filter of offered stops (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102840 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — zero-fare transfer stops excluded (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102841 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — positive-fare stops offered (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102842 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — selecting a stop updates the alighting stage and recalculates the fare (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102843 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — zero-fare stop hidden while smallest positive-fare stop shown (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102844 | ZZ_DELETE_REVIEW - Journey History — a £0.00 capped journey stays visible and correctable (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102846 | ZZ_DELETE_REVIEW - Journey History — a transfer journey charged £0.00 stays displayed and correctable (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102847 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — negative-fare stop excluded (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102848 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — positive-fare transfer stops still offered (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
| C4102849 | ZZ_DELETE_REVIEW - Alighting-Stop Correction — TVM-only positive-fare stops still offered (CR122) | Delete / Update Stop List | FBD-100662, GEORGE-2026, TODEV-24300 | yes |
