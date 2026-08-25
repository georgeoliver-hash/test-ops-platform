# FS002 §3 — Functional States: State Management (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` §3 "Functional States" /
§3.1 "State Management" (3.1.1 Initialisation, 3.1.2 Communications lock, 3.1.3 Low power mode,
3.1.4 Screen Saver, 3.1.5 Out of Service). Distilled from lines 273–891 of the extracted text only —
raw PDF held locally, not committed. Page citations use the nearest preceding "Page N" footer marker
in the extraction, per repo convention.

## Scope note — Operational State vs Functional State
The spec distinguishes **Operational State** (In Service / Out of Service / Locked-Blocked — set by
back-office command) from **Functional State** (Initialising / Idle / Comms Locked / Low Power /
Screen Saver / Out of Service — the device's own internal state machine). §3's intro and the three
state-diagram captions ("In service Operation State", "Out of Service Operational State",
"Locked/Blocked Operational State", NJT_FRFRP_FS002 p.10–11) sit above §3.1 but the actual diagrams
are graphical and **not present in the text extraction** — no transition diagram content is
available from this source, only the prose transition rules captured below.
**GAP** — the exact mapping between the three Operational States and the functional states
(specifically: is "Comms Locked" the functional-state realisation of the "Locked/Blocked
Operational State", or are they distinct?) is not spelled out in the extracted prose — confirm with
engineer before asserting one implies the other in a test case.

## 3.1.1 Initialisation (p.11)
- On power-on, FR enters **"Initialising"** functional state; loads software and configuration.
- If initialisation completes **without errors** AND **no condition is active that blocks Driver
  access**, FR transitions to **"Idle"**.
- **GAP** — the target state when initialisation fails or a blocking condition IS active is not
  stated in this section (§3.1.5 Out of Service lists fault *examples* but does not explicitly say
  "failed initialisation → Out of Service" — infer with caution; confirm before asserting).

## 3.1.2 Communications lock (p.11)
- FR unable to communicate with back office for a **configurable period** → enters **"Comms
  Locked"** functional state.
- **Only enterable from "Idle"** (no other functional state transitions directly to Comms Locked).
- While locked: Driver **cannot sign on**. Driver's only available action is to **force a
  communications session**. **Special users** can still access special-user mode.
- On a **successful** comms session → returns to **"Idle"**.
- **Comms lock timeout**: configurable in **hours**, range **0 (lock disabled) to 99,999 hours**.
- **GAP** — "special user" is referenced (here and in §3.1.5) but not defined in this section: what
  credential/action invokes special-user mode is not stated — confirm before writing real test steps.

## 3.1.3 Low power mode (p.11–12)
- FR inactive for a **configurable period** → enters **"Low Power"** functional state.
- **Only enterable from "Screen Saver"** (p.11) — i.e. not directly from Idle; the device must pass
  through Screen Saver first.
- While in Low Power (p.12): screen and a number of other components are **powered down** to reduce
  power usage; FR **maintains communication** with the back-office system **and** with devices
  attached via **RS485**.
- **Any keypress** → returns to **"Idle"** and displays the relevant **Idle Mode screen**.
- **GAP** — no numeric default/range given for the Low Power inactivity timeout (unlike Comms Lock's
  explicit 0–99,999hr range) — confirm the configurable value/bounds before writing boundary cases.

## 3.1.4 Screen Saver (p.12)
- FR inactive for a **configurable period** → enters **"Screen Saver"** functional state.
- **Only enterable from "Idle"**.
- **Any keypress** → returns to **"Idle"**.
- **GAP** — no numeric default/range given for the Screen Saver inactivity timeout — confirm before
  writing boundary cases. Also confirm the Screen Saver timeout is intended to be **shorter** than
  the Low Power timeout (implied by the required Idle→Screen Saver→Low Power chain, not stated
  explicitly as a rule).

## 3.1.5 Out of Service (p.12–13)
- Entered when FR is unable to allow Driver access, due to either:
  1. detection of a **localised fault condition**, or
  2. an **operational state change command from CloudFare** (e.g. "Locked").
- On entry: FR **clearly indicates to the Driver** that the device cannot be used, and **sends an
  out-of-service status to CloudFare** (requirement refs cited in-spec: **GR-3, FRT-1**).
- Driver **cannot sign on** until either:
  - the fault is cleared and the device returns to **"Idle"**, or
  - CloudFare places the device into the **In Service** state (remote override).
- **Special user access remains available** while Out of Service.
- Example faults that trigger Out of Service (p.12–13, non-exhaustive per spec wording "examples of
  this are"):
  - Missing/corrupt software or configuration file (e.g. no valid fare information).
  - Unable to identify key information from the mounting tray (e.g. cannot determine home location)
    — **Note 1** (p.13): this should be isolated to the **commissioning phase** (incorrect installer
    programming, to be rectified before finalising installation); once correctly programmed, the tray
    chip is expected to remain consistently readable. A tray-read OOS fault seen **outside**
    commissioning is therefore anomalous per spec intent.
  - Essential component not detected / not functioning (e.g. faulty printer).
- **GAP** — the list is explicitly non-exhaustive ("examples of this are") — other fault classes that
  drive OOS are not enumerated in this section; do not assume the three examples are the complete set.
- **GAP** — mechanism/command by which CloudFare pushes "In Service" to recover a device is not
  detailed here (only that it can).

## Suite implications
- Assert **Initialising → Idle** transition only when init has no errors AND no Driver-access-blocking
  condition; assert Idle is NOT reached if either fails (target state on failure is a GAP — flag, don't
  assume "Out of Service" without confirming).
- Assert **Comms Locked** is reachable **only from Idle** (never from Screen Saver/Low Power/OOS
  directly) and that a locked device blocks sign-on, exposing only "force comms session" +
  special-user access.
- Boundary-test the **Comms Lock timeout**: `0` = lock disabled (never locks), a mid-range value, and
  the max `99,999` hours.
- Assert a **successful** forced comms session returns the device to Idle from Comms Locked.
- Assert **Low Power is reachable only via Screen Saver** — explicitly test that Idle cannot jump
  straight to Low Power.
- Assert Low Power behaviour: screen/components powered down, but back-office comms AND RS485-device
  comms are maintained; assert **any key** returns to Idle and shows the correct Idle Mode screen
  (not a stale/blank screen).
- Assert **Screen Saver reachable only from Idle**, and **any key** returns to Idle.
- Assert the inactivity chain **Idle → Screen Saver → Low Power** occurs in the correct order under
  sustained inactivity (once timeout values are confirmed — currently a GAP).
- Assert **Out of Service** entry via both trigger paths: (a) local fault detection, (b) CloudFare
  remote operational-state-change command (e.g. "Locked") — cover both as distinct scenarios.
- Assert OOS entry always produces a clear Driver-facing "device cannot be used" indication **and**
  sends OOS status to CloudFare (cite GR-3/FRT-1 in the case as the traced requirement).
- Assert Driver sign-on is blocked while OOS, but **special user access still works** while OOS
  (pending the special-user-mechanism GAP being resolved to write real steps).
- Assert OOS recovery via both paths: local fault cleared → Idle, and CloudFare forcing In Service
  remotely → device usable again.
- Cover the three named OOS fault examples explicitly: missing/corrupt software/config (no valid fare
  info), tray-chip unreadable (and treat as commissioning-only per Note 1 — flag as anomaly if
  reproduced on an already-commissioned device), essential-component failure (e.g. faulty printer).
- Do **not** treat the three OOS fault examples as exhaustive — log the "other fault classes" GAP to
  the gap register rather than assuming suite coverage of OOS triggers is complete.
- Route the following to the gap register / engineer Q&A before authoring dependent cases: (1)
  Operational-State ↔ Functional-State mapping, (2) failed-initialisation target state, (3) Low
  Power / Screen Saver timeout default & range, (4) special-user invocation mechanism, (5) CloudFare
  "force In Service" mechanism.
