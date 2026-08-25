# ABT/BOS suite (30279) — consolidation-COMPLETENESS audit, 2026-07-23

**Question asked:** did consolidating the old `2.1-Backoffice Systems - Acceptance Suite` (14441,
1,766 cases) down to the live `**NEW** BOS & ABT Suite` (30279, 496 cases, ~105 of them
`ZZ_DELETE_REVIEW`) silently drop any genuinely distinct required coverage — every report type,
entitlement/product, decline reason, config-rule variant the system needs tested — that should show
up somewhere (its own case, or an explicit "Data variations:" line)? This suite had the largest raw
old-suite base of any suite in the department and had already had a very active day (blank-steps bug
fix, terse rewrite, deep audit, gap resolution, the Q1 CR122 Operator→Passenger reversal) before this
pass — everything below was pulled fresh, not carried over from earlier-in-the-day descriptions.

**Method.** Pulled old suite 14441 fully (`get_cases(42, 14441)` → 1,766 cases, 257 sections) and the
live new suite 30279 fully (`get_cases(42, 30279)` → 496 cases, 98 sections), built a section-path
lookup for both, and cross-tabbed by top-level/level-2 family (Cloudfare/CloudFare, ABT, Merit, Merit
Web Reporter, Smartrack, Delete). For each priority family, read full case bodies (preface/
preconditions/steps/expected) on both sides, not just titles, before judging consolidated-vs-dropped.

## Priority family: Sign On & Access — Operator Portal, Passenger Portal, CloudFare (George's specific concern)

George's worry, verbatim: sign-on tests might have been consolidated down to "one case" when every
role/claim combination (AdminFullAccess/AdminReadAccess etc., per KeyCloak composite claims) with
genuinely distinct behaviour should be tested distinctly.

**Checked in full.** The old suite's own role-matrix cases turned out to be **templates, not a real
enumeration** — this is not a case of the new suite dropping something concrete the old suite had:
- **C2665794** "Operator Portal - Sign-On and Navigation" — one generic admin-rights user, no claim
  variants at all.
- **C2925102** "Operator Portal - Access Rights of Different Users" — literally three placeholder
  rows, "the user signs in with a user with the role **x** / **y** / **z**" (with a blank
  `Username:`/`Password:` note field), plus one "unrestricted user" row. No real role names anywhere.
- **C2665804** "Administrator can manage the Operator account access rights..." — preface says
  **"NOT IN SCOPE"**, and its steps are the same generic template ("repeat this step for each user /
  sub-role type").

So the old suite never named a concrete composite claim either — the consolidation didn't lose a
named-role matrix, because one was never authored. But the new suite's single case (**C4102857**,
"Access — portal tasks match the operator's assigned claims") also only carried an "e.g." with two
example claims (AdminFullAccess, AdminReadAccess) and no enumerated list — so the full composite-claim
catalogue that actually exists (`knowledge/translink/specs/FBD-100342-user-claims.md`, distilled from
`FBD-100342 User Claims Specification V3.00` + the CloudFare Claims Reference Sheet) wasn't named
anywhere in the suite either. That is a genuine completeness gap, independent of the old suite, and
is fixed below.

Also checked the **Passenger Portal** sign-on family (no claims model there — anonymous/registered
account only) and **CloudFare** sign-on/roles: old suite's `Cloudfare / Roles and Profiles` (4 cases:
Manage Report Access, Set Groups Access, Manage Passenger Journey/Revenue/System-Mining-Tool Access,
Set Specific Report Access) maps cleanly onto the new suite's `CloudFare / Roles & Profiles` (2 cases:
C4102963 report access, C4102964 module/group access) — correctly consolidated 4→2, but again with no
enumerated claim catalogue in the consolidated cases.

**Fixes applied** (`abt-consolidation-completeness.rewrite.json`, cited FBD-100342):
- **C4102857** — added a Data-variations line naming every composite-claim family from FBD-100342:
  Account Management (ReadOnly/CreateReadUpdate/Full, DebtRecovery, EPurseBalanceAdjustmentApproval,
  RefundApproval, RefundAuthorisation, UpdateMediaStatus, TransactionsReadAccess,
  JourneyHistoryColumns); Admin (AdminReadAccess/AdminFullAccess, EPurseReadAccess,
  ReceiptConfiguration, AdminRouteGroups); Capping (BusinessRulesReadAccess/CreateEdit/FullAccess);
  Reports (AccountStatus, ActionList, Audit, DeclinedCardTap, EPurseBalance, LateTap, RevenueByMid,
  RevenueInspection).
- **C4102963** — added the CloudFare Reports sub-claim catalogue (TVM/Cash, Staff, Alert, Asset,
  Topology sub-reports) as a Data-variations line.
- **C4102964** — added the CloudFare operator-scope claim asymmetry that FBD-100342 explicitly flags
  as a real trap worth testing (`CF Full Operator`/`AccessControlFullAccess` sees all operators in
  hierarchy, vs `CF-Operator-<Name>`/`AccessControl<name>` — that operator only, **no sub-operators**
  — contrasted with the nested ABT AD-group model where a parent group *does* inherit child
  visibility), plus the module/sub-module and gate/station claim catalogues.

**Not touched / correctly as-is:** C4103597/C4103598 (first-login-no-claims gate; operator
hierarchy scoping, Metro vs Ulsterbus) were already added in the 2026-07-22 deep audit specifically
to close this class of gap and remain correct and distinct — no change needed.

## Family: ABT decline/error reasons (DeclinedReason enum, FBD-100658)

FBD-100658 defines a 6-value decline taxonomy (excl. `0`=Success): `1` Card Expired, `2` On Deny
List, `3` Declined, `4` Cancelled, `15` On BIN List, `20` Passback. Checked the consolidated
**C4102954** ("Declined taps — each decline reason is recorded on the Declined Taps Report") — its
Then-line and Data-variations enumerated only 4 of 6 (Expired, Declined/ODA, On BIN List, On Deny
List); **Cancelled** and **Passback** were missing from this case's own list.
- **Cancelled** is separately, thoroughly covered elsewhere (Journey History / Annulment & Re-tap
  sections, ~19 live cases) — not a drop overall, just missing from this one report-scoped case's
  enumeration.
- **Passback** had no case or Data-variation anywhere naming it as a *decline* reason (distinct from
  the `Product — Passback Time configured` config case, which only tests the period setting, not a
  passback-triggered decline). Old suite's own regression case **C3211528** (CA-14070, "Masked Pan and
  Smart Card ID data is not displayed in Declined Taps Report") directly evidences "Negative List"
  (passback) rows on the live report alongside "Deny List" rows — confirming this is a real,
  reportable, distinct decline reason, not just a theoretical enum value with no old-suite trace.

**Fix applied:** C4102954's preconditions/step/expected/Data-variations updated to name all 6
DeclinedReason codes; Refs updated to FBD-100658 + `OldSuite-C3211528`.

## Family: CloudFare config-rule variants — Fares Export

Old suite's `Cloudfare / Topology & Fares Management / Fares List Export` (9 cases) + 3 adjacent cases
(`Fares List Export - ABT Fares` C2925143; `- XLSX/CSV - Report Downloaded` C2970781/2970782) — 12
cases total — fragmented one behaviour across file format (XLSX vs CSV) and content variant
(standard/ABT Fares/Route Attributes/Area-Zone Overlays/single-file). New suite correctly folds this
into **one** flow case, **C4102978** ("Fares export — configured fares are exported") — but the
consolidated case named none of the format/content dimensions, only "the fares file is produced."

**Fix applied:** added a Data-variations line (file format XLSX/CSV; export scope — standard fares
list, ABT Fares export, Route Attributes, Area/Zone overlays; single-file export) citing the 12
matching old-suite case ids. Correctly-consolidated verdict stands (one flow, not 12 cases) — the fix
only restores the enumerated variants that a rushed reader would otherwise assume were dropped.

## Family: Merit Web report names + Smartrack (Q28/Q29) — already resolved earlier today, confirmed, no further action

Checked whether today's Q28/Q29 gap-register entries (~24 Merit report names + all 7 Smartrack report
names had "no governing spec in the library") were still open. **They were not** — both were already
resolved from the old suite on 2026-07-22 (`abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json`,
pushed and committed same day, well before this pass started):
- **Q28** (Merit report names): old suite 14441's `Merit / Analysis Reports`, `Concessionary Report`,
  `Distance Reports`, `NIR Revenue Reports`, `Translink Reports` sections carry matching titles + real
  REQ-#### tags for nearly all of them (e.g. Origin/Destination = C2700374/REQ-1212.11-12, Bus Loading
  = C2700324/REQ-1212.10). `TFTS Requirements Matrix.xlsx` independently confirms the REQ-1212 family
  as "Test | Cloudfare | Deployed." Refs were added to 18 of the ~24 cases; a residual **6 report
  names genuinely have no old-suite or REQ match** (BRT, Glider, Concessionary Class Summary excl.
  ENTCS, Fare Foregone, Ticketing-timebands, Route Distance Analysis) and remain correctly flagged
  `[UNCONFIRMED]` — not a consolidation loss (no source ever existed for them, old or new), so nothing
  further to fix here.
- **Q29** (Smartrack): old suite 14441's `Smartrack` section has populated, REQ-traceable cases for
  every one of the 7 report names (Action List, Liability/Scheme Liability, Default Payment,
  Delivery, Refund, Decommission Card, POS Revenue Analysis) plus Access (Administrator/User). Refs
  added to all 7 (+ Access/Card Data/Import & Export cases). Fully resolved.

Re-verified this pass by re-reading the resolved rewrite file and cross-checking its case ids against
the live suite — all citations are present live, matching the changelog's claim. **No new action
needed; Q28/Q29 stand resolved.**

## Family: ABT capping / entitlement / product types

Reviewed the full capping family (Metro Daily / Zonal / Reference Fare / Uncapped & Single Taps / Town
Service caps, Transfers, Capping Configuration/Groups) — old suite's `ABT / Operator Web Portal / ABT
Capping Rules` + `ABT Capping Groups` (13 cases) maps cleanly onto the new suite's `Operator Web
Portal / Capping Configuration` (8 cases, each a genuine flow consolidation, not a drop — e.g. daily/
weekly/monthly rules folded into 2 cases with Data-variations, not silently reduced). The Tap
Correction family (34 cases across Metro/Zonal/Reference/Uncapped/Town Service) was already
exhaustively audited in the 2026-07-21/22 deep-audit and gap-resolution passes (Q1 reversal, capping-
charge-timing, transfer-cap) — re-checked here at the title/section level only, found no further gap.
**Verdict: fully covered / correctly consolidated, no action needed.**

## Family: Card Reference File (per-device fragmentation)

Old suite: 4 per-device cases (`Card Reference File - ETM/POS/PV/HHD`, C2952091-94). New suite: 1
case, **C4103010** ("Card Reference File validates alighting stages across devices"), which names all
four devices explicitly in its precondition/expected ("on each device (ETM, POS, PV, HHD)"). **Verdict:
correctly consolidated, no gap** — each device is already an explicit named variation, not silently
dropped.

## Fixes applied this pass

Pushed via `tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-consolidation-completeness.rewrite.json --commit`
(dry-run first: `updated: 5 removed(ZZ): 0 skipped: 0 missing: 0`; then `--commit`, identical counts).
5 existing cases reworded (no new cases created, no cases removed):
- **C4102857** — Data variations: full ABT composite-claim catalogue (FBD-100342).
- **C4102963** — Data variations: CloudFare Reports sub-claims (FBD-100342).
- **C4102964** — Data variations: CloudFare operator-scope + module + gate/station claims (FBD-100342).
- **C4102954** — Data variations: all 6 DeclinedReason codes (FBD-100658, OldSuite-C3211528).
- **C4102978** — Data variations: fares-export file formats + content variants (12 old-suite case ids).

## Audit result after this pass

`python -m system_test_ops audit --suite 30279 --no-gate`: **391 cases audited, 89 blocking, 208
advisory** — unchanged from the pre-existing baseline recorded earlier today
(`abt-blank-steps-fix.changelog.md`: 89 blocking after that fix). None of the 5 edited case ids
(`C4102857`, `C4102963`, `C4102964`, `C4102954`, `C4102978`) appear in the blocking-findings list;
`C4102963`/`C4102964`/`C4102954` appear only under the pre-existing, advisory
`title-no-emdash`/`title-too-long` sections (unchanged title text, so this is carried-over, not
newly introduced). **This pass's changes added zero blocking findings.**

## Files touched
- `proposals/coherence-audit/fixes/abt-consolidation-completeness.rewrite.json` (new, pushed live)
- `proposals/coherence-audit/fixes/abt-consolidation-completeness.changelog.md` (new, this file)
- No changes to old suite 14441 (read-only, never touched).
