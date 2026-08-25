# BOS / CloudFare — back-office knowledge

CloudFare (CF) is the **back office** for the Translink estate — CRM / station-manager / **device
manager**, the **audit sink** for device events, and the channel that **distributes software/config
down to the devices** (TMS). MERIT and SmartTrack are downstream reconciliation systems (revenue and
smartcard lifecycle). The device suites (POS / ETM / PV) assert the *device* side; this folder is the
grounding for the **back-office side** — what happens to a transaction/event after it leaves the device.

Drop material here and Claude will use it to (1) make the `Cross-check: CloudFare / MERIT / SmartTrack`
flags on device tests **precise** (which event each action should raise), (2) add accurate
**audit-verification steps** to the relevant device tests ("…and a `state.changed` event is recorded
in CloudFare"), and (3) when you want, **build/audit a BOS acceptance suite** (TestRail already has
`AA-Backoffice Systems` suites).

## What to drop in here
- **`requirements/`** — BOS/CloudFare requirement & functional specs (PDF/MD). The REQ/IF ids the
  device audits trace to.
- **`event-catalogue.*`** — the list of **device → CF events** and when they fire: transactions,
  sign-on / sign-off, declined/denied cards (Deny/BIN list), transaction declined, faulty-device,
  comms/heartbeat, shift/duty, top-up/issue/validation. (A table or export is ideal — it becomes the
  authoritative cross-system map.)
- **`screenshots/`** — CF UI screens (Dashboard, Events & Alerts, Estate Management, Device Manager,
  Asset Manager, Reports, Topology & Fares, Schedule Management, Settings) — for HMI/coverage grounding.
- **`tms/`** — software/configuration **distribution** docs (how a build/config is sent to a device,
  activation dates, FEIG/PCA/OS deployment).
- **`merit/`, `smarttrack/`** — what reconciles where (which transactions land in MERIT for revenue,
  which smartcard events land in SmartTrack), so the routing is fact-based not inferred.

Images/large exports are gitignored (like `knowledge/flows`); the **derived notes** (an
`event-catalogue.md`, a `bos-audit-map.md`) are committed and are what the agents read.

## How it improves the existing work
- The **cross-system enrichment** (priority/estimate already applied; automatable + Cross-check still
  pending a usable TestRail field) becomes accurate per event rather than keyword-inferred.
- Device tests gain a grounded **"Then … is audited in CloudFare as <event>"** assertion where the
  spec confirms one — strengthening the end-to-end coverage you flagged (MERIT/SmartTrack).
- Feeds a future **BOS suite** built with the same audit-first / consolidation process.
