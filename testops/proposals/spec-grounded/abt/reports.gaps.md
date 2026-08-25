# ABT/BOS Reporting — gap register (questions for the engineer)

**Re-grounding pass complete.** 42 of the ~84 previously-UNCONFIRMED cases are now grounded (`reword`, with real
citations) against docs that WERE NOT used in the first pass: PSPEC-0015 (CloudFare ABT v4.2.1), the CloudFare
User Manual (Translink), PSPEC-0014 (Fares and Topology Manager), and the Manuel Reporting - Laval.docx
(mechanics-only evidence). FBD-100377 and a full filename sweep of the local library were also checked. See
`reports.changelog.md` for the full per-case breakdown. 40 cases remain genuinely `unconfirmed` — this file now
tracks only what is still open.

## GAPs (report confirmed, a specific detail is not in the spec)
- 4103100 — Do "Sales Breakdown by value" and "by value/location" exist? Not in FBD-100306 6.1–6.18.
- 4103109 — Are "Class Breakdown by Device" / "Route Breakdown by Class Group" distinct reports or sub-options of FBD-100306 6.3/6.5?
- 4103116/117/118 — Exact summary/detailed/grouping forms of Class/Route Revenue Performance and Period Trend? FBD-100341 para 124 names them, not their forms.
- 4103130 — Daily Audit By Trip (FBD-100306 6.11) exists but has no case — add?
- 4103055 — Which specific Dashboard tiles are enabled for THIS environment? The tile mechanism and catalogue-is-per-deployment fact are now confirmed (CloudFare User Manual §3); only the live tile SET for this test environment remains to check.
- 4102885 — Is the deny/negative-list customer summary (PSPEC-0015 Table 1, "Customers on action list") a separate report, or a mode of the Action List Report (§3.15.2)?
- 4102900 — Confirm the exact UI label for the Revenue Inspection Report's detailed-view mode (PSPEC-0015 §3.15.19 describes it in prose but doesn't name a toggle/label).
- 4102904/4102897 — "Expired Taps" and "Late Taps" are named as the same report under two names within PSPEC-0015 §3.15.12 itself — candidate to consolidate into one case.
- 4102910 — Is there a single Operator Web Portal report titled "Revenue Apportionment Report", or does the case mean the Pay-In Reconciliation report (FBD-100341) or the general DWH/BI analytics feed (PSPEC-0015 p.101)?
- 4102914 — Confirm "Shared Liability" is the on-screen name for the Force Settle (Liability Protection) Report (PSPEC-0015 §3.15.13), or a different report — titles don't match exactly.
- 4103065 — Confirm the 4th Assets report (CloudFare User Manual: Assets sub-page has 4 reports, FBD-100263 names only 3) is literally called "Software Versions Report".
- 4103067/4103068 — The CloudFare User Manual confirms a Reports > Staff sub-page exists with 2 reports; confirm "Engineer Visits" and "Revenue Inspector's" are those 2 (names are a screenshot in the manual, not extractable text).
- 4103069/4103070 — The CloudFare User Manual confirms a Reports > Cash sub-page exists with 12 reports; confirm which match the cash-collection vs cash-revenue variants asserted in these cases (names are a screenshot, not extractable text).
- 4103071 through 4103075 — The CloudFare User Manual confirms a Reports > Topology sub-page exists with 5 reports (matching this group's count); confirm the exact on-screen names against "Rules List Export / Concise Area & Reference Fare / Route List Export / Product to Ticket Assignment / Product List" (names are a screenshot, not extractable text; only "Rules List" itself is separately confirmed via PSPEC-0014 §16.1).
- 4103076 — The CloudFare User Manual confirms a Reports > Events & Alerts sub-page exists with 2 reports; confirm the exact names (screenshot, not extractable text).

## UNCONFIRMED — remaining after the second grounding pass (checked PSPEC-0015, CloudFare User Manual (Translink), PSPEC-0014, Manuel Reporting - Laval.docx, FBD-100377, plus a full library filename sweep)

**These are now confirmed absent from every document available in the local requirements library — not merely
unchecked against a narrow 7-doc sample. Treat as genuine spec-coverage holes; escalate to the requirements
owner rather than re-grounding again without a NEW document being added to the library.**

Operator Web Portal ABT reports (PSPEC-0015's 23-report catalogue checked in full — these 7 are absent):
Fare Band (4102898), Initial Taps by Brand (4102899), Journeys by Card Scheme (4102902), Journeys by
Service/Route (4102903), PSP Technical Errors (4102906), Retail Debt (4102908), Revenue by Business Rule
(4102911).

Smartrack (whole page — "Smartrack" does not appear anywhere in the local requirements library, checked via
content search of FBD-100377, PSPEC-0015 and the CloudFare User Manual): Action List (4103165),
Liability/Scheme Liability (4103166), Default Payment (4103167), Delivery (4103168), Refund (4103169),
Decommission Card (4103170), POS Revenue Analysis (4103171).

Other CloudFare (checked against the CloudFare User Manual's full Reports module structure — Cash/Staff/Events &
Alerts/Assets/Topology, 25 reports total — neither of these fits any of the 5 sub-pages): Vehicle Check
(4103077), CloudFare Usage (4103078 — nearest adjacent-but-distinct features are the Activity Log module,
FBD-100358, and the ABT Audit Report, PSPEC-0015 §3.15.4).

Dashboard: full-screen view (4103058 — checked the CloudFare User Manual's Dashboard section §3 in full; no
full-screen mode described, only per-tile resize/expand).

Merit Web-side reports (Analysis / Revenue Performance / Concessionary / Daily — checked PSPEC-0015, the
CloudFare User Manual, FBD-100377, and confirmed no separate "Merit 5 FRS" document exists anywhere in the local
library via a full filename sweep): Origin/Destination (4103102), Bus Loading (4103103), Route/Stage (4103104),
Journey Analysis (4103105), Stage Timeband (4103106), Patronage Timeband (4103107), Revenue & Revenue by Stop
(4103108), POS Revenue (4103110), Bus Serviceability (4103112), GPS (4103113), Route Purchase (4103114), Tickets
By Operator (4103119), NIR (4103120), NIR Period Trend (4103121), BRT (4103122), Glider (4103123), Ticketing
timebands (4103124), Revenue Foregone (4103125), Concessionary Class Summary (4103126), ENTCS (4103127), Fare
Foregone (4103128), Outstanding Duties (4103134), Stage List (4103135).

## POSSIBLE SPEC-COVERAGE HOLE (escalate)

Two genuinely distinct holes remain, now that the CloudFare-side documents have been checked in full:

1. **Merit-Web-side analysis/revenue-performance/concessionary/daily reports (22 cases) and Smartrack (7 cases)
   have NO spec anywhere in the local library.** This is no longer "the 7 governing specs don't cover it" — it
   is "12 documents, including the two CloudFare product/user manuals and a full filename sweep, don't cover it
   either". Escalate to the requirements owner: either these were authored from the live UI/legacy Merit 5 system
   without a spec ever being written, or a document genuinely needs adding to the library (e.g. an actual
   "Merit 5 FRS" or Smartrack spec that isn't currently in `_current`).
2. **7 Operator Web Portal ABT report names (Fare Band, Initial Taps by Brand, Journeys by Card Scheme, Journeys
   by Service/Route, PSP Technical Errors, Retail Debt, Revenue by Business Rule) are not in PSPEC-0015's
   otherwise-exhaustive 23-report catalogue.** Given PSPEC-0015 §3.15 reads as a complete list ("The following
   reports are available from within CloudFare ABT:" followed by a titled table), these 7 look like either
   legacy/renamed reports, dimensions of other reports rather than distinct reports (e.g. card scheme is a filter
   on the Authorisation Failure Report), or reports that were removed/never built. Escalate rather than treat as
   missing test coverage.

Two moderate gaps also remain, but are lower priority (structure confirmed, only exact names unconfirmed because
the CloudFare User Manual's Reports lists are screenshots, not extractable text): the 10 "Other CloudFare"
Cash/Staff/Events & Alerts/Topology report names (4103065/67/68/69/70/71/72/73/74/75/76), and 3 detail-level
Operator Web Portal nuances (4102885, 4102900, 4102910, 4102914 — see the GAPs section above).
