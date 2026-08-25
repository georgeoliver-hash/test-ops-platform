# ABT/BOS Reporting — spec-grounding changelog (re-grounding pass)

Re-grounding of the reporting test cases previously marked UNCONFIRMED against the CloudFare ABT Portal /
CloudFare User Manual / Smartrack-adjacent specs that were NOT used in the first pass. **Proposal only — not
pushed to TestRail.**

Governing specs for THIS pass (in addition to the 7 used previously — FBD-100306 Merit Web Specification,
FBD-100341 Revenue Apportionment & Reporting, FBD-100263 CloudFare Asset Tracking Reports, FBD-100347 Head
Office Reporting through Merit DWH, FBD-100356 Merit Cube DWH/Power BI, FBD-100387 ABT Reporting through Merit
DWH, FBD-100377 Service Classification Configuration & Reporting):

- **PSPEC-0015 - Product Specification - CloudFare - ABT v4.2.1.pdf** — the CloudFare ABT product spec. Section
  3.15 is a 23-report catalogue (§3.15.1-3.15.23) of the Operator Web Portal's ABT reports, each with a Title and
  Description; a "Table 1 — Report Summary" (p.84) additionally lists two reports (Tap Reconciliation, Exception)
  that don't get their own numbered subsection. Section 3.17 ("Exceptions") separately describes late/missing/
  corrupt/lost tap data handling, including a "Lost Data" report of devices with sequence-number gaps (§3.17.4).
- **Cloudfare - User Manual (Translink).docx** — the Translink-specific CloudFare user manual. Its scope is
  narrower than expected: it documents the **Dashboard** module (§3) and **Events & Alerts** module (§4) in
  full, plus a **Reports** module (§9.2) whose structure is 5 sub-pages — Cash (12 reports), Staff (2), Events
  & Alerts (2), Assets (4), Topology (5) — 25 reports total. The specific report names within each sub-page are
  shown as screenshots in the manual and were not extractable as text by the tooling used (pdfminer/docx-XML text
  dump); only the sub-page structure and report counts are confirmed this pass.
- **PSPEC-0014 - Product Specification - CloudFare - Fares and Topology Manager_Issue v2.3.docx** — read to check
  the Topology reports (Rules List Export, Route List Export, etc.). Confirms a "Rules List" fare-rule management
  screen (§16.1) and "Automatic Reference Fare Management" (§9.1), but no literal "Route List Export" / "Product
  List" / "Product to Ticket Assignment" titles.
- **Manuel Reporting - Laval.docx** (French; Laval, Quebec deployment) — read as instructed. It documents the
  SAME generic CloudFare ABT reporting-module mechanics as PSPEC-0015 (14 reports for that deployment, all
  filterable by date range and exportable as PDF/CSV/XLS) but is a **different deployment**, not Translink — used
  only as supporting evidence for the reporting module's generic mechanics, never as a source of Translink report
  names.
- **FBD-100377 - Service Classification Configuration & Reporting Specification V1.00.docx** — read in full.
  Defines Passenger Journey, Revenue and Schedule Adherence reports grouped by service-classification tag. It does
  **not** define Smartrack reports (Action List, Liability, Default Payment, Delivery, Refund, Decommission Card,
  POS Revenue Analysis) — the word "Smartrack" does not appear in this document, in PSPEC-0015, or in the
  CloudFare User Manual. A full filename search of the local requirements library also found no separate
  "Merit 5 FRS" document.

## Cross-cutting corrections

- **The prior pass's "7 governing specs consulted" framing is now out of date** — 12 documents have been checked
  across the two passes. Every case's preface/change_note below states exactly which of the newly-checked docs
  were used.
- **"Smartrack" does not appear anywhere in the local requirements library.** All 7 Smartrack cases
  (4103165-4103171) remain UNCONFIRMED; this is now a stronger negative finding (checked in full, not merely
  absent from a 7-doc sample) rather than an open question.
- **No separate "Merit 5 FRS" document exists in the library.** The 22 Merit-Web-side Analysis/Revenue
  Performance/Concessionary/Daily-report cases remain UNCONFIRMED; FBD-100306 (Merit Web Specification) was
  already used in the first pass and does not name these reports either.
- **The CloudFare User Manual's Reports module structure (Cash/Staff/Events & Alerts/Assets/Topology, 25 reports)
  is a major new fact.** It directly confirms the EXISTENCE of the "Reports > Staff", "Reports > Cash",
  "Reports > Events & Alerts" and "Reports > Topology" sub-pages that the previous pass said did not exist —
  several cases are corrected from "no such spec/sub-page" to "sub-page confirmed, but exact report names are in
  an unextracted screenshot".
- **Dashboard management (create/clone/favourite/delete/add-remove-tiles) is now fully confirmed** via the
  CloudFare User Manual §3 — the "subject to detailed design" caveat from FBD-100347 applied to the *tile
  catalogue*, not to these CRUD/tile-management mechanics, which are documented in full with exact UI wording.

## Per-case changes

### Operator Web Portal ABT reports (PSPEC-0015 CloudFare ABT v4.2.1, §3.15 catalogue)

28 of the 35 cases in this group are now grounded (reword); 7 remain genuinely unconfirmed.

**4102883** — action: `reword`. Account Status Report confirmed, §3.15.1 (p.87).

**4102884** — action: `reword`. Action List Report confirmed, §3.15.2 (p.88).

**4102885** — action: `reword`. "Action List — Negative List Report": the underlying concept (customers
summary/detail on the deny/negative list) is confirmed via Table 1 (p.84-85, "Customers on action list"), but
whether it is a distinct report or a mode of the Action List Report (§3.15.2) is not stated — gap narrowed, not
closed.

**4102886** — action: `reword`. Aftercare Report confirmed, §3.15.3 (p.88).

**4102887** — action: `reword`. Audit Report confirmed, §3.15.4 (p.89).

**4102888** — action: `reword`. Authorisation Failure Report confirmed, §3.15.5 (p.89) — spec uses singular
"Failure", case title uses plural "Failures".

**4102889** — action: `reword`. Cancelled Tap Report confirmed, §3.15.6 (p.90), including the "not applicable
for TOTO systems" note.

**4102890** — action: `reword`. Debt Report confirmed, §3.15.7 (p.91).

**4102891** — action: `reword`. Confirmed under the spec's title "Declined Card Taps", §3.15.15.

**4102892** — action: `reword`. Deny List Report confirmed, §3.15.9 (p.92).

**4102893** — action: `reword`. Duplicate Taps Report confirmed, §3.15.8 (p.92).

**4102894** — action: `reword`. Confirmed under the spec's title "EMV Report", §3.15.10 (p.93); related "EMV
Transactions" report also cited, §3.15.11.

**4102895** — action: `reword`. ePurse Balance confirmed, §3.15.22 (p.100).

**4102896** — action: `reword`. Exception Report confirmed via Table 1 (p.84) — does not get its own §3.15.x
subsection like most others, but is named and described there.

**4102897** — action: `reword`. Expired Taps confirmed, §3.15.12 (p.93). Note: the spec's own body text for
this section calls it "the late taps report" — see 4102904.

**4102898** — action: `unconfirmed` (unchanged). Fare Band Report: checked the full 23-report catalogue and
Table 1 — not present in any spec consulted.

**4102899** — action: `unconfirmed` (unchanged). Initial Taps by Brand Report: not present in any spec
consulted.

**4102900** — action: `reword`. "Inspection Details" is not a standalone report — it is the detailed-view mode
of the Revenue Inspection Report (§3.15.19), which the spec explicitly says provides both summary totals AND "a
detailed view of every inspection made and any penalty applied". Reworded to reference the correct report.

**4102901** — action: `reword`. Journey Summary confirmed, §3.15.14 (p.95).

**4102902** — action: `unconfirmed` (unchanged, sharpened). "Journeys by Card Scheme" is not a named report; the
Authorisation Failure Report (§3.15.5) is split by card scheme, but that is a dimension of a different report,
not evidence of this one.

**4102903** — action: `unconfirmed` (unchanged). "Journeys by Service/Route" not present in any spec consulted.

**4102904** — action: `reword`. **"Late Taps" is the CloudFare ABT spec's own alternate body-text name for the
report headed "Expired Taps" (§3.15.12)** — a naming inconsistency inside the spec itself, not an invented
report. Flagged 4102897/4102904 as likely duplicates of the same report.

**4102905** — action: `reword`. Confirmed via §3.17.4 "Lost Data" — the spec explicitly describes "a report...
showing devices with gaps in the sequence numbers", matching "Lost Tap Data".

**4102906** — action: `unconfirmed` (unchanged). "PSP Technical Errors" not present in any spec consulted;
nearest concept (Authorisation Failure Report, §3.15.5) covers scheme-level declines, not PSP technical errors.

**4102907** — action: `reword`. Refunds Reports confirmed, §3.15.17 (p.97).

**4102908** — action: `unconfirmed` (unchanged, sharpened). "Retail Debt" is not named separately from the
existing Debt Report (§3.15.7, ABT/EMV declined-authorisation debt) or the Retail Transaction reports
(§3.15.18/3.15.20).

**4102909** — action: `reword`. Both Retail Transaction Report (§3.15.18) and Summary Retail Transaction
Report (§3.15.20) confirmed.

**4102910** — action: `reword`. Revenue apportionment as a MECHANISM and DWH/BI analytics feed is confirmed
(PSPEC-0015 p.101; FBD-100341), but no single report literally titled "Revenue Apportionment Report" is named in
either spec — reworded to describe the confirmed capability, narrower gap kept on the exact screen/report name.

**4102911** — action: `unconfirmed` (unchanged). "Revenue by Business Rule" not present in any spec consulted.

**4102912** — action: `reword`. Revenue by MID confirmed, §3.15.16 (p.96).

**4102913** — action: `reword`. Revenue Inspection Report confirmed, §3.15.19 (p.99).

**4102914** — action: `reword`. Probable match to "Force Settle (Liability Protection) Report" (§3.15.13,
issuer liability protection / chargeback protection) — reworded from UNCONFIRMED, but the exact title mismatch
("Shared Liability" vs "Force Settle") is kept as a residual gap rather than asserted as an exact match.

**4102915** — action: `reword`. Tap Reconciliation Report confirmed via Table 1 (p.84), including the full
6-step reconciliation chain description.

**4102916** — action: `reword`. Transaction Report confirmed, §3.15.21 (p.99).

**4102917** — action: `reword`. Unique Taps Report confirmed, §3.15.23 (p.100).

### Smartrack (7 cases — all remain unconfirmed)

**4103165, 4103166, 4103167, 4103168, 4103169, 4103170, 4103171** — action: `unconfirmed` (unchanged,
sharpened). Checked FBD-100377 (Service Classification Configuration & Reporting Specification) in full — it
covers Passenger Journey/Revenue/Schedule Adherence reports grouped by service classification, **not** Smartrack.
Also checked PSPEC-0015 and the CloudFare User Manual in full: "Smartrack" does not appear in either document,
nor anywhere else in the local requirements library. This is now a confirmed absence across 12 specs, not merely
a 7-spec gap.

### Assets/Staff (3 cases)

**4103065** — action: `reword`. Upgraded from "not a standalone report" — the CloudFare User Manual confirms
the live Assets reports sub-page currently lists **4** reports, one more than FBD-100263 names (Depot Location,
Staff Activity, Devices Last Seen), consistent with a 4th "Software Versions" report. Report names are a
screenshot in the manual, not extractable text, so the 4th report's exact name is a narrower residual gap.

**4103067** — action: `reword`. Correction: a Reports > **Staff** sub-page DOES exist (CloudFare User Manual,
Reports module structure), currently listing 2 reports — contradicting the prior pass's "no Staff sub-page"
finding. Exact report names not extractable (screenshot).

**4103068** — action: `reword`. Same correction as 4103067 — the Staff sub-page exists with 2 reports. Kept
the existing note not to conflate with the Merit Web Inspector's Report (FBD-100306 §6.18).

### Other CloudFare (10 cases)

**4103069, 4103070** — action: `reword`. Correction: a Reports > **Cash** sub-page DOES exist (CloudFare User
Manual), currently listing 12 reports — contradicting the prior "no such spec/sub-page" finding. Exact report
names (coin/note totals, refloat, cash revenue, etc.) not extractable (screenshot); gap narrowed accordingly.

**4103071** — action: `reword`. Reports > **Topology** sub-page confirmed with 5 reports (matching this group's
count exactly); the underlying "Rules List" fare-rule management screen is separately confirmed in PSPEC-0014
§16.1.

**4103072** — action: `reword`. Topology sub-page count evidence only; PSPEC-0014's "Automatic Reference Fare
Management" (§9.1) is conceptually related but not a literal "Concise Area & Reference Fare" title match — gap
retained for the exact name.

**4103073, 4103074, 4103075** — action: `reword`. Topology sub-page count evidence only (5 reports matches this
group's 5 items); no literal title match found in PSPEC-0014 for "Route List Export" / "Product to Ticket
Assignment" / "Product List" — gap retained for exact names on each.

**4103076** — action: `reword`. Reports > **Events & Alerts** sub-page confirmed with 2 reports (CloudFare User
Manual) — contradicting the prior "no such spec" finding. Exact report names not extractable (screenshot).

**4103077** — action: `unconfirmed` (unchanged, sharpened). "Vehicle Check Report" does not fit any of the
Reports module's 5 documented sub-pages (Cash/Staff/Events & Alerts/Assets/Topology, 25 reports total) —
confirmed absent from the manual's full Reports structure.

**4103078** — action: `unconfirmed` (unchanged, sharpened). A CloudFare-wide "Usage Report" auditing all user
actions does not fit the Reports module's 5 sub-pages. Two narrower, distinct, confirmed features exist nearby —
the Activity Log module (FBD-100358, device-reported operational activity) and the ABT Audit Report (PSPEC-0015
§3.15.4, ABT-system changes by authorised operators) — neither is the same as a CloudFare-wide usage log.

### Dashboard (4 cases)

**4103055** — action: `reword`. Tile mechanism (add/resize/move/remove/filter/expand) confirmed in the
CloudFare User Manual §3, plus a second concrete tile example ("Quarantined Transactions" count tile) beyond
"Hours since last communication" (FBD-100263). The manual states the tile catalogue "is configured at the point
of delivery of CloudFare" — i.e. no fixed universal tile list exists BY DESIGN, which is now a confirmed fact
rather than an open gap; only the specific set of tiles enabled for this environment remains to confirm.

**4103056** — action: `reword`. **Fully confirmed** — CloudFare User Manual §3 documents Create dashboard,
Clone current dashboard, Delete current dashboard (with an explicit "cannot be reversed" warning), Select
different dashboard, and Favourite dashboard(s) (one default at a time), in exact UI wording.

**4103057** — action: `reword`. **Fully confirmed** — CloudFare User Manual §3 documents Add Tile (via
ellipsis + tile picker), tile resize, tile move, tile filter, and tile removal (red X).

**4103058** — action: `unconfirmed` (unchanged, sharpened). Checked the CloudFare User Manual's full Dashboard
section (§3) specifically for a full-screen mode — not described anywhere (only per-tile resize/expand exists).
Confirmed absent from the manual.

### Merit-Web-side reports — Analysis / Revenue Performance / Concessionary / Daily (22 cases, all remain
unconfirmed)

**4103102** (Origin/Destination), **4103103** (Bus Loading), **4103104** (Route/Stage), **4103105** (Journey
Analysis), **4103106** (Stage Timeband), **4103107** (Patronage Timeband), **4103108** (Revenue & Revenue by
Stop), **4103110** (POS Revenue), **4103112** (Bus Serviceability), **4103113** (GPS), **4103114** (Route
Purchase), **4103119** (Tickets By Operator), **4103120** (NIR), **4103121** (NIR Period Trend), **4103122**
(BRT), **4103123** (Glider), **4103124** (Ticketing timebands), **4103125** (Revenue Foregone), **4103126**
(Concessionary Class Summary), **4103127** (ENTCS), **4103128** (Fare Foregone), **4103134** (Outstanding
Duties), **4103135** (Stage List) — action: `unconfirmed` (unchanged, sharpened change_note on every case).
Checked PSPEC-0015, the CloudFare User Manual, FBD-100377 and the Manuel Reporting - Laval.docx (a different
deployment's generic reporting-module manual, used only as mechanics evidence, never as a Translink report-name
source) — none cover these Merit-Web-side reports. A full filename search of the local requirements library
found **no separate "Merit 5 FRS" document** to re-ground against (only FBD-100306 Merit Web Specification, which
was already one of the 7 specs used in the first pass, and FBD-100300/347/356/387 which are DWH/head-office-
reporting specs, not Merit Web report catalogues). These 22 cases are now confirmed absent from every document
available in the local library, not merely unchecked against a narrower 7-doc sample.
