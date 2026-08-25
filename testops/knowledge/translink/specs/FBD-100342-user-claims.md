# FBD-100342 — User Claims (distilled)

**Source:** `FBD-100342 User Claims Specification V3.00` (1 Aug 2023, S. James) + `CloudFare Claims Reference Sheet V4.05`.
Distilled testable facts only — raw spec + reference sheet held locally in `dev/translink-requirements/`, not committed.

## Two claims systems (by era/product)
- **CloudFare ABT** (Operator Portal) → **KeyCloak** + Active Directory. AD supplies user login; KeyCloak assigns claims.
- **CloudFare hosted (pre-SaaS)** → **ADFS + AD**. Claims defined in ADFS "Claim Descriptions"; per-website Relying Party Trusts carry Claim Issuance Policies.
- **CloudFare SaaS (post-migration)** → moves to **KeyCloak too**, so one KeyCloak instance manages **both** CloudFare and ABT claims (cross-ref FBD-100359).

## Model (both systems)
- **Base claims** = individual feature/module access. **Composite claims** = named bundles of base claims assigned to groups. Base + composite claims are created **by Flowbird**, not Translink.
- Users pulled from **Active Directory** → assigned to **user groups** → inherit the group's claims. (Manual user setup also possible in KeyCloak.)
- **First-login default = NO claims → no portal/site access** until a Translink admin adds the user to a group. This is a testable gate for both ABT Portal and CloudFare.
- Day-to-day activity is expected to be **moving users between groups**, not editing claim assignments.

## KeyCloak specifics
- Realm = **`Translink`**. Clients: **`operator-react-client`** = Operator Portal (ABT); **`CloudfareWeb`** = CloudFare.
- Role Mappings tab shows Available / Assigned / effective (composites expanded to base) roles.
- MFA via `Required User Actions` → `Configure OTP`; locale set to `en`; temporary password forces reset on next login.

## CloudFare claims (functional + operator)
- **Operator claims:** `CF Full Operator` (KeyCloak `AccessControlFullAccess`) = all operators in hierarchy; `CF-Operator-<Name>` (`AccessControl<name>`) = that operator only, **no sub-operators**. (Contrast the ABT AD group structure which nests operator groups so a parent group inherits child operator visibility — see below.)
- **Module/sub-module claims** (each a separate claim): Dashboard; Events & Alerts (+ Alert Configuration, Event Group Configuration); Topology & Fares (+ Route Management, Service Delete, Legacy Stages, Product Editor, Fare Rules, Ticket Editor, Delete Label); Schedule Manager (+ Import, Topology Sync); Estate Management (+ Comms Monitor, Activity Log, Asset Manager, Cash View, Staff Manager, Device Dataset Deployment, Quarantine, Device Logging); Reports (+ TVM/Cash, Staff, Alert, Asset, Topology sub-reports); System Configuration (+ Notifications).
- **Gate/station claims** (KeyCloak-only, no AD name): `StationAdmin`, `TransitGuard`, `SystemSupervisor`, `StationSupervisor`, `Admin` — control gate/station monitoring scope.

## ABT composite claims (by subject area, from reference sheet)
- **Account Management:** AccountManagementReadOnly / CreateReadUpdate / Full, DebtRecovery, EPurseBalanceAdjustmentApproval, RefundApproval, RefundAuthorisation, UpdateMediaStatus, TransactionsReadAccess, JourneyHistoryColumns.
- **Admin:** AdminReadAccess / AdminFullAccess (Full includes assigning users to groups), EPurseReadAccess, ReceiptConfiguration, AdminRouteGroups.
- **Capping:** BusinessRulesReadAccess / CreateEdit / FullAccess.
- **Reports:** AccountStatus, ActionList, Audit, DeclinedCardTap, EPurseBalance, LateTap, RevenueByMid, RevenueInspection (each *ReadAccess).
- Composite claims decompose into base roles like `AccountManagement.Read/Write/Delete`, `Refunds.Do/Approve/Read`, `BusinessRules.Read/Write/Delete`. Some claims are release-gated (`Live`, `TOTO`, `UB TOO`, `GL TOO`, `N/A`, `TOTO`).

## Suggested Translink user groups (business roles)
Ticketing Administrator (full), Ticketing Manager (view admin + manage business rules), Ticketing Viewer (view admin + rules), Customer Manager (full customer incl. debt recovery/ePurse/refund approval), Customer Advisor (no account close, no ePurse), Customer Restricted (as Advisor + minors hidden), Customer View (view only), Finance Manager (authorise refunds), Report Manager (all reports), Report User (restricted), Treasury Report User (limited reports).

## Suite implications (BOS/ABT suite 30279 + device config)
- **First-login-no-claims gate** (both ABT Portal + CloudFare): unassigned user is denied all access — highest-value permission case.
- **Operator-scope claims**: `CF-Operator-<X>` sees only that operator (no sub-operators) in CloudFare, vs the **nested ABT AD groups** where a parent operator group inherits child visibility — assert the difference explicitly (this asymmetry is a real trap). Cross-ref FBD-100383 for the tree.
- **Composite → base decomposition**: assigning a composite (e.g. `AccountManagementFull`) grants exactly its base roles (Read+Write+Delete); removing the composite removes them. Verify effective-role view in KeyCloak.
- **Negative permission cases** per group: e.g. Customer Advisor cannot close an account or adjust ePurse; Report User cannot see all reports; RefundApproval requests but RefundAuthorisation approves (two-person control).
- **Module access on/off** cases: a user without `TicketEditor` cannot open Tickets sub-module; without `Quarantine` cannot open Quarantined Data; etc.
- Watch **release-gating** — some claims (`TOTO`, `UB TOO`, `GL TOO`) only exist in later releases; don't assert them against an earlier build.
