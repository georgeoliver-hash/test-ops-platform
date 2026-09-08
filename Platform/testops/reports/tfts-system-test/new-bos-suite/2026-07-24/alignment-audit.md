# Alignment audit - suite 30287

- Cases audited: **191**
- Blocking findings: **48**
- Advisory (reviewed-intentional) findings: **67**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 60
- C4104287 | ExternalInfo/StaffCash API returns staff cash for a date range
- C4104288 | ExternalInfo/StaffCash API handles invalid requests and BST/GMT
- C4104260 | Import route data at parent and child operator level
- C4104292 | Card Reference File validates alighting stages across devices
- C4104314 | Filter quarantined data by device
- C4104315 | Edit and resubmit quarantined data
- C4104316 | Navigate the Commands Viewer
- C4104318 | [UNCONFIRMED] Create, clone, favourite and delete a dashboard
- C4104319 | [UNCONFIRMED] Add and remove dashboard tiles
- C4104320 | [UNCONFIRMED] View a dashboard full screen
- C4104327 | [UNCONFIRMED] Software Versions Report
- C4104329 | [UNCONFIRMED] Engineer Visits Report
- C4104330 | [UNCONFIRMED] Revenue Inspector's Report
- C4104331 | [UNCONFIRMED] TVM cash collection reports
- C4104332 | [UNCONFIRMED] TVM cash revenue reports
- C4104333 | [UNCONFIRMED] Rules List Export
- C4104334 | [UNCONFIRMED] Concise Area & Reference Fare Report
- C4104335 | [UNCONFIRMED] Route List Export
- C4104336 | [UNCONFIRMED] Product to Ticket Assignment Report
- C4104337 | [UNCONFIRMED] Product List Report
- C4104338 | [UNCONFIRMED] Events & Alerts Report
- C4104339 | [UNCONFIRMED] Vehicle Check Report
- C4104340 | [UNCONFIRMED] CloudFare Usage Report
- C4104355 | [UNCONFIRMED] Origin and Destination reports
- C4104356 | [UNCONFIRMED] Bus Loading by Route/Journey report
- C4104357 | [UNCONFIRMED] Route/Stage reports
- C4104358 | [UNCONFIRMED] Journey Analysis reports
- C4104359 | [UNCONFIRMED] Stage Timeband report
- C4104360 | [UNCONFIRMED] Patronage Timeband report
- C4104361 | [UNCONFIRMED] Revenue and Revenue by Stop reports
- C4104363 | [UNCONFIRMED] POS Revenue report
- C4104365 | [UNCONFIRMED] Bus Serviceability Final Defects report
- C4104366 | [UNCONFIRMED] GPS reports
- C4104367 | [UNCONFIRMED] Route Purchase report
- C4104372 | [UNCONFIRMED] Tickets By Operator report
- C4104373 | [UNCONFIRMED] NIR Revenue Performance reports
- C4104374 | [UNCONFIRMED] NIR Period Trend Analysis reports
- C4104375 | [UNCONFIRMED] BRT Revenue Performance reports
- C4104376 | [UNCONFIRMED] Glider Revenue Performance reports
- C4104377 | [UNCONFIRMED] Ticketing Reports including timebands
- C4104385 | [UNCONFIRMED] Revenue Foregone reports
- C4104386 | [UNCONFIRMED] Concessionary Class Summary reports
- C4104387 | [UNCONFIRMED] ENTCS Passenger and Revenue reports
- C4104388 | [UNCONFIRMED] Fare Foregone reports
- C4104394 | [UNCONFIRMED] Outstanding Duties report
- C4104395 | [UNCONFIRMED] Stage List report
- C4104396 | [UNCONFIRMED] Origin and Destination Distance reports
- C4104397 | [UNCONFIRMED] Route Distance Analysis report
- C4104401 | Synchronise staff into Merit
- C4104402 | Browse audit data with Client Tools
- C4104405 | Smartrack access rights for administrator and user
- C4104409 | [UNCONFIRMED] Run the Action List reports (Smartrack)
- C4104410 | [UNCONFIRMED] Run the Liability and Scheme Liability reports (Smartrack)
- C4104411 | [UNCONFIRMED] Run the Default Payment report (Smartrack)
- C4104412 | [UNCONFIRMED] Run the Delivery report (Smartrack)
- C4104413 | [UNCONFIRMED] Run the Refund report (Smartrack)
- C4104414 | [UNCONFIRMED] Run the Decommission Card report (Smartrack)
- C4104415 | [UNCONFIRMED] Run the POS Revenue Analysis report (Smartrack)
- C4104403 | View the available reports in the Merit Web Reporter
- C4104404 | View and export a report in the Merit Web Reporter

## Title over 72 chars _(advisory)_ - 7
- C4104795 | Configure module and group access for a role — Events & Alerts module access - 76 chars
- C4104796 | Configure module and group access for a role — Topology & Fares module access - 77 chars
- C4104797 | Configure module and group access for a role — Schedule Manager module access - 77 chars
- C4104798 | Configure module and group access for a role — Estate Management module access - 78 chars
- C4104800 | Configure module and group access for a role — System Configuration module access - 81 chars
- C4104279 | Product — a Smartcard product is configured (WTS SmartCreate / SmartRecharge) - 77 chars
- C4104301 | Activity Log — failed validations, declined taps and failed payments are identified with reason - 95 chars

## Objective/preface empty - 0
_none_

## Objective not starting 'This test is to confirm' - 46
- C4104318 | [UNCONFIRMED] Create, clone, favourite and delete a dashboard - **UNCONFIRMED** — dashboard create/clone/favourite/delete is not speci
- C4104319 | [UNCONFIRMED] Add and remove dashboard tiles - **UNCONFIRMED** — adding/removing dashboard tiles is not specified. Co
- C4104320 | [UNCONFIRMED] View a dashboard full screen - **UNCONFIRMED** — a dashboard full-screen view is not specified. Confi
- C4104327 | [UNCONFIRMED] Software Versions Report - **UNCONFIRMED** — no standalone 'Software Versions Report' is scoped; 
- C4104329 | [UNCONFIRMED] Engineer Visits Report - **UNCONFIRMED** — an 'Engineer Visits Report' is not among the scoped 
- C4104330 | [UNCONFIRMED] Revenue Inspector's Report - **UNCONFIRMED** — a 'Revenue Inspector's Report' (with a BRT variant) 
- C4104331 | [UNCONFIRMED] TVM cash collection reports - **UNCONFIRMED** — TVM cash-collection reports (total coins/notes from 
- C4104332 | [UNCONFIRMED] TVM cash revenue reports - **UNCONFIRMED** — TVM cash-revenue reports (sales revenue, change to c
- C4104333 | [UNCONFIRMED] Rules List Export - **UNCONFIRMED** — a Topology 'Rules List Export' is NOT specified in a
- C4104334 | [UNCONFIRMED] Concise Area & Reference Fare Report - **UNCONFIRMED** — a 'Concise Area & Reference Fare Report' is NOT spec
- C4104335 | [UNCONFIRMED] Route List Export - **UNCONFIRMED** — a Topology 'Route List Export' is NOT specified in a
- C4104336 | [UNCONFIRMED] Product to Ticket Assignment Report - **UNCONFIRMED** — a 'Product to Ticket Assignment Report' is NOT speci
- C4104337 | [UNCONFIRMED] Product List Report - **UNCONFIRMED** — a Topology 'Product List Report' is NOT specified in
- C4104338 | [UNCONFIRMED] Events & Alerts Report - **UNCONFIRMED** — an 'Events & Alerts Report' is NOT specified in any 
- C4104339 | [UNCONFIRMED] Vehicle Check Report - **UNCONFIRMED** — a 'Vehicle Check Report' is NOT specified in any of 
- C4104340 | [UNCONFIRMED] CloudFare Usage Report - **UNCONFIRMED** — a 'CloudFare Usage Report' auditing user actions (wi
- C4104355 | [UNCONFIRMED] Origin and Destination reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue; lik
- C4104356 | [UNCONFIRMED] Bus Loading by Route/Journey report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104357 | [UNCONFIRMED] Route/Stage reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104358 | [UNCONFIRMED] Journey Analysis reports - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104359 | [UNCONFIRMED] Stage Timeband report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104360 | [UNCONFIRMED] Patronage Timeband report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104361 | [UNCONFIRMED] Revenue and Revenue by Stop reports - **UNCONFIRMED** — no 'Revenue' or 'Revenue by Stop' report of these na
- C4104363 | [UNCONFIRMED] POS Revenue report - **UNCONFIRMED** — no Merit 'POS Revenue' report of this name in the co
- C4104365 | [UNCONFIRMED] Bus Serviceability Final Defects report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104366 | [UNCONFIRMED] GPS reports - **UNCONFIRMED** — the GPS report and GPS Stage Change Failure reports 
- C4104367 | [UNCONFIRMED] Route Purchase report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104372 | [UNCONFIRMED] Tickets By Operator report - **UNCONFIRMED** — not named in the governing revenue-reporting spec (w
- C4104373 | [UNCONFIRMED] NIR Revenue Performance reports - **UNCONFIRMED** — the generic Class/Route Revenue Performance reports 
- C4104374 | [UNCONFIRMED] NIR Period Trend Analysis reports - **UNCONFIRMED** — NIR-specific Period Trend Analysis reports are NOT n
- C4104375 | [UNCONFIRMED] BRT Revenue Performance reports - **UNCONFIRMED** — BRT-specific Class/Route Revenue Performance reports
- C4104376 | [UNCONFIRMED] Glider Revenue Performance reports - **UNCONFIRMED** — Glider-specific Route/Class Revenue Performance repo
- C4104377 | [UNCONFIRMED] Ticketing Reports including timebands - **UNCONFIRMED** — a 'Ticketing Reports' grouping combining Revenue Per
- C4104385 | [UNCONFIRMED] Revenue Foregone reports - **UNCONFIRMED** — not named in the governing spec (concessionary fare 
- C4104386 | [UNCONFIRMED] Concessionary Class Summary reports - **UNCONFIRMED** — Concessionary Class Summary reports are NOT named in
- C4104387 | [UNCONFIRMED] ENTCS Passenger and Revenue reports - **UNCONFIRMED** — ENTCS Passenger, ENTCS Revenue and ENTCS Revenue For
- C4104388 | [UNCONFIRMED] Fare Foregone reports - **UNCONFIRMED** — the Fare Foregone Summary and Fare Foregone by Fare 
- C4104394 | [UNCONFIRMED] Outstanding Duties report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104395 | [UNCONFIRMED] Stage List report - **UNCONFIRMED** — not in the confirmed Merit Web report catalogue. Con
- C4104409 | [UNCONFIRMED] Run the Action List reports (Smartrack) - **UNCONFIRMED** — the Smartrack Reports page and its Active/Inactive/d
- C4104410 | [UNCONFIRMED] Run the Liability and Scheme Liability reports (Smartrack) - **UNCONFIRMED** — the Smartrack Liability (summary/detailed) and Schem
- C4104411 | [UNCONFIRMED] Run the Default Payment report (Smartrack) - **UNCONFIRMED** — the Smartrack Default Payment report is NOT specifie
- C4104412 | [UNCONFIRMED] Run the Delivery report (Smartrack) - **UNCONFIRMED** — the Smartrack Delivery report (summary/detailed) is 
- C4104413 | [UNCONFIRMED] Run the Refund report (Smartrack) - **UNCONFIRMED** — the Smartrack Refund report is NOT specified in any 
- C4104414 | [UNCONFIRMED] Run the Decommission Card report (Smartrack) - **UNCONFIRMED** — the Smartrack Decommission Card report is NOT specif
- C4104415 | [UNCONFIRMED] Run the POS Revenue Analysis report (Smartrack) - **UNCONFIRMED** — the Smartrack POS Revenue Analysis report is NOT spe

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

## Genuine compound THEN (two distinct outcomes) - should split - 2
- C4104259 | Import Map Point File — stops are added and existing stops updated - a success box reports the number of stops added (Stops Added) and upda
- C4104322 | Alert Viewer — filter, acknowledge then clear alerts - the acknowledge icon turns green and the alert is marked acknowledged

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_
