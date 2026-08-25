# BOS & ABT — new suite structure (DRAFT — pending George's sign-off)

Target: `**NEW** BOS & ABT Suite` (30279). Built audit-first from `old-suite-audit.md`.
**Nothing is pushed until this structure is signed off.**

## Structuring principle

Unlike a single device, this suite spans **multiple back-office systems**, each with its own
devtype. So the top level is **system-first**, and under each system we use the familiar
**test-type / feature** split. Reporting is first-class (George's priority). Regression folds into the
owning feature via Refs (not release-version sections). Per-report and per-screen cases stay distinct
(each is a real function — do not over-fold, same rule as HMI per-screen).

```
BOS & ABT Suite (30279)
├─ Smoke                         # thin critical path across the back office (login, key report, a tap)
│
├─ CloudFare (BOS)               # devtype [100]
│   ├─ Sign On & Access          (Sign On/Off, Roles & Profiles, Google SSO)
│   ├─ Topology & Fares          (Products, Routes, Drawing Tool, Fares Export, Rules, Card Ref File)
│   ├─ Estate Management         (Dataset Deployment, Activity Log, Asset/Staff Manager, Comms Monitor)
│   ├─ Reports                   (Cash, Staff, Topology, Assets, Usage, Events & Alerts — per-report)
│   ├─ Events & Alerts           (Alerts Configuration, Events)
│   ├─ Settings                  (Scheduled Tasks, System Settings, Event Codes, Operating Units…)
│   ├─ Ticket Editor
│   ├─ Dashboard
│   └─ API
│
├─ ABT                           # devtype [200]
│   ├─ Operator Web Portal       (Customers, Administrator Settings, Sign On & Access Rights)
│   ├─ Capping                   (Capping Rules, Capping Groups)  ← core; spreadsheet tap→cap extends
│   ├─ Processing Taps           (Card Verification, Late Taps)   ← simulated taps → ABT process
│   ├─ Reports Management        (ABT reports — per-report)
│   ├─ Passenger Web Portal      (Anonymous Account, Mobile Wallet, Queries)
│   ├─ Debt Recovery
│   └─ End to End                (device tap → ABT outcome; cross-ref device case via Refs)
│
├─ Merit                         # devtype [151]
│   ├─ Analysis & Revenue Reports (Analysis, NIR Revenue, Concessionary, Daily, Ticketing — per-report)
│   ├─ Administration
│   ├─ Synchronisation
│   └─ Stored Procedures
│
├─ Merit Web Reporter            # devtype [151]/[152]
│   └─ Report Viewer             (per-report: Class/Route Breakdown, Pay-In Recon, Audit, Sales…)
│
└─ Smartrack                     # devtype [152]
    ├─ Reports
    ├─ Display Card Data         (incl. Transactions)
    └─ Imports / Exports
```

### Regression & defects
- The 843 version-organised `Fixes/New Features` cases (CloudFare 526 + ABT 317) and Merit/Smartrack
  `Fixes/Changes` are **folded into the owning feature case** above, linked via **Refs** (TIBU/version
  id). A dedicated `@regression` case only where no functional case owns the behaviour. This is the
  shrink — same as POS Confirmation Tests / ETM Regression Defects.

### Out of scope (do not carry over)
- The `Delete` section (108) and `Non-relevant tests` (14) — superseded / SAAS-migration / exploratory.
- ABT ref suite 16275 is read for coverage only (`DO NOT USE` as a run target).

## Build order (after sign-off)
1. **ABT first** — it's where the spreadsheet + George's focus land (Capping, Processing Taps,
   Reports Management, Operator/Passenger portals). Author from spreadsheet + 16275 + old ABT section.
2. **CloudFare** — the largest; Reporting + Estate + Topology, folding the V-regression.
3. **Merit + Merit Web Reporter** — reporting depth.
4. **Smartrack**.
5. Smoke, final fold of remaining regression, conformance audit CLEAN, enrich (priority/estimate/
   automatable tag), export automation backlog.

Each area = one `<area>.cases.yaml` → `push --commit` (auto-audits) → fix → re-push. Same proven
pipeline; write specs with the editor (never a PowerShell heredoc — UTF-8 mangling).

## Decisions needed before building
1. Confirm **all 5 systems** in scope (vs ABT-only first).
2. The **spreadsheet** — its rows + which area(s) they populate.
3. devtype per system confirmed: BOS `[100]`, ABT `[200]`, Merit `[151]`, Smartrack `[152]` — OK?
4. Any **Run Configurations** (e.g. Glider/NIR for ABT or Merit reports)?
