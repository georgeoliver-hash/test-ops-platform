# Project: Translink

Human-curated facts the agents load before reasoning about Translink coverage. Keep this current;
it is the project's source of truth for things the TestRail/JIRA data doesn't make obvious.

> ⚠️ Fill in the TODOs once you have the real TestRail/JIRA values. Agents should treat unknown
> values as unknown, not guess.

## TestRail

- **Project:** `TFTS - System Test` — **id 42** (Translink runs under the TFTS project). Set as
  `TESTRAIL_PROJECT_ID=42` in `.env`.
- **POS suites:**
  - **`AA-POS Acceptance Test`** — **id 9317**. The **existing/old** suite. **SOURCE, read-only.**
    Never modify or delete from it; only copy cases *out* of it into the new suite.
  - **`GG - POS - Claude Suite`** — **id 30253**. The **new** suite we are building/optimising.
    **TARGET.** All proposed cases, copies, rewrites and new cases go here.
- **Auth:** self-hosted TestRail at `http://testraildb/testrail` (LDAP/AD; API keys not enabled, so
  login is the email + AD password — internal network only).
- **TVM:** suite TBD.

## Old suite reality (`AA-POS Acceptance Test`, 2193 cases)

- **Organised mode-first:** top-level `NIR` (513), `Metro` (334), `Ulsterbus` (317) each carry their
  **own full duplicated tree** — plus `Confirmation Tests` (251), `Smoke Tests` (5), and a `Delete`
  section (**773 cases** — deprecation dumping-ground; leave them, never copy).
- **Sign-on is a matrix, written per mode:** roles **Operator / Supervisor / Technician /
  Administrator** × methods **Manual (ID+PIN) / Smartcard** × {sign on, Invalid Credentials, Device
  Locked, Unlock Device, Sign Off}. The screens are the same across modes → prime `@mode(all)` +
  Configurations consolidation; do NOT write ×3 per mode.
- **House Gherkin style:** cases use `**GIVEN** … **AND** … **WHEN** … **THEN** …`. Many are well
  populated; some (e.g. Invalid Credentials) only have a one-line objective and need fleshing out.
- **Comms component:** referred to as **"CloudFare"** (the back-office/cloud link). The Idle/Sign-On
  given is "the POS is communicating with CloudFare"; loss → the Communication Locked screen.

## Defects / regression coverage

- **Defect tracker = `TIBU-#####`** (e.g. `TIBU-28530`). The old suite's **`Confirmation Tests`**
  section (~247 cases, grouped by release 1.1.1 → 2.0.X) is the **bug-fix regression backlog** — each
  case title is `TIBU-#####: <bug>`. The bug id is in the **title**, not Refs (only 1 case uses Refs).
- **Optimisation for the new suite:** pin every past defect by **behaviour** — fold a regression step
  into the owning functional case, or a dedicated `@regression` case — and **link via the Refs field**
  (`TIBU-#####`), organised by feature not by release. Full list:
  `proposals/pos-suite-restructure/bug-regression-register.md`.
- TIBU is likely a JIRA project → bug detail can be pulled via the Atlassian MCP to design precise
  regression steps.

## Requirements & JIRA

- **Refs are requirement IDs (`REQ-####`)**, not JIRA keys — e.g. `REQ-0050`, `REQ-0056`, `REQ-2821`.
  This is the primary coverage signal: a case's Refs tie it to requirements. The "documentation"
  George is sourcing is most likely the **requirements** these REQ ids point at.
- **JIRA:** project key _TODO_; fix-version → REQ linkage _TODO_. JIRA still read via the Atlassian
  MCP when prepping a fix version, but expect coverage to hang off REQ ids.

## Devices in scope

- **POS** — INF212, Way6 variant, Android. Primary suite. See `knowledge/devices/pos.md`.
- **TVM** — Linux. Placeholder; suite TBD.

## POS operating modes (NIR / Ulsterbus / Metro)

The Translink POS runs in **three operating modes**: **NIR** (NI Railways — this is the **"Rail POS"**;
same device, rail mode), **Ulsterbus**, and **Metro** (the two bus modes). **Most flows are identical
across all three** (e.g. Sign On). The **top-up flow** can differ by mode. Modelling rule (see `docs/gherkin-standard.md`):

- Shared behaviour → one case tagged `@mode(all)`, executed against each mode via TestRail **Run
  Configurations** (NIR/Ulsterbus/Metro). No duplication.
- Genuinely different behaviour (top-up) → mode-specific cases tagged `@mode(<mode>)` in the
  feature's mode-specific subsection.

This keeps the suite single-source: shared once, mode-specific only where it must be.

## Audit-confirmed POS facts (mode-specific behaviour)

Proven from the old suite cross-tab + the Overflow design notes (`flow-annotations.md`). Don't guess
these — they are the things that make a mode run correct:

- **Metro sells NO tickets** (George review, 2026-06-03) — Metro mode does **only top-ups and new
  smartcard issues**; there is no ticket sale and no bus Fare-Look-Up on Metro. (So a Metro suite has
  Top Up + Issue Card, but no Tickets / FLU sections.)
- **Metro is cash-only** — bank card and warrant payment are **NIR + Ulsterbus only**. (Bank card
  also requires a PCD attached; without one the option is hidden.) **Warrant** is a payment option on
  **Rail/Ulsterbus only**, not Metro.
- **Rail/Ulsterbus issue *tickets*, not cards** — a rail "Warrant" or UB ticket is a ticket sale
  (covered by the Tickets section), not a smartcard issue. Card *issue* (from blank) is shared +
  Metro; rail has no card-issue flow of its own.
- **Metro has no smartcard validation** — validation behaviour is **NIR + Ulsterbus only**.
- **Cross-border (XB) ticket types are Rail (NIR) only**; XB stations aren't offered on bus; the
  price button toggles GBP↔euro for XB.
- **Top-up is shared** — any POS mode can top up any card (iLink, Multi-Journey, BVP, DayLink, ABT,
  Metro Travelcard, Town Service). Only the Metro/Ulsterbus-branded products are mode-homed.
- **Shared tickets** (NIR + Ulsterbus): Single, Day Return, iLink Single, Warrant Return, Family &
  Friends. **NIR-only:** 1/3 Off Day Return, 3 Day Select, Weekly/Monthly Season. **Ulsterbus-only:**
  Bus Rambler, Jobseeker Single, Month Return, Rail Substitution Service.
- **Entitlement smartcards** (Senior/Blind/War Pensioner/yLink/24+/Half-Fare/Dependants) set a ticket
  type, **validate per transaction**, and **cannot be added to a basket**.
- **Basket** caps at **9** tickets; bus basket can't mix two routes.
- **Comms component** is **CloudFare**; loss beyond the configured period → Communication Locked.
- Lockout threshold and most timeouts (auto sign-off / suspend) are **configurable**, not hard-coded.

The full evidence + per-flow design notes: `knowledge/flows/flow-annotations.md`,
`proposals/pos-suite-restructure/old-suite-audit.md`, and `.../annotation-coverage.md`.

## Back-office (BOS)

- **Environment:** `uktest-tl-env5` (test BOS).
- **Auth:** Keycloak, realm **`TranslinkDevices`**.
- Audit events are verified device-side via the EventLog (e.g. `state.changed` on sign-on) and
  correlated against BOS. When a case asserts a BOS event, name the event — don't invent it.

## What "covered" means here

A 5.0.0 scope item is **covered** when there's a TestRail case whose behaviour exercises the
story/feature/bug-fix and whose Refs (or unambiguous wording) tie it to the JIRA key. A bug fix is
covered when there's a case that would **catch the regression**, not merely a case in the same area.

## Cross-references

- Automated mirror of these tests: `C:\Users\GeorgeOliver\dev\automation-tests` →
  `projects/translink/tests/` (signon, transactions, printing, provisioning, status, options, audit).
- Log analysis of runs: `C:\Users\GeorgeOliver\dev\log-intelligence`.
