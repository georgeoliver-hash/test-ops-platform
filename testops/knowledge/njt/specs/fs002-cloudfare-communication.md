# FS002 — CloudFare Communication (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf`, Section 8 "CloudFare
Communication" and 8.1 "Remote Commands" (NJT Transit Fare Register). Distilled testable facts
only — raw spec held locally in `njt-requirements/_text/`, not committed. Requirement-id tags
(GR-2, GR-4, GR-5, FF-5, GR-3, FRT-1) are cited as printed in the source; their own definitions are
outside this excerpt.

## Comms channel & guaranteed delivery
- FR communicates with CloudFare in **near real time**, using industry-standard protocols
  (NJT_FRFRP_FS002 p.86, GR-2/GR-4/GR-5/FF-5).
- Comms incorporate a **guaranteed delivery mechanism** so data is not lost (p.86). **GAP** — retry
  count/backoff/timeout behaviour of the guaranteed-delivery mechanism is not detailed in this
  section; confirm on the live system or in another spec section before asserting specific retry
  semantics.
- All events and transactions are sent to CloudFare **in a manner that allows verification of
  authenticity and integrity** (p.86).
- If a device is **not registered as an authorised device** in CloudFare, any communications are
  **rejected with an unauthorised error response**; the device then **puts itself into an
  out-of-service state** until a successful communication occurs (p.86).

## Software / configuration updates (pull model)
- **Staff list**: FR requests the latest list from CloudFare **every 15 minutes** — the "staff list
  check period," configurable by Flowbird support staff (p.86).
- **Other software updates** (manifest): FR requests the latest manifest **every 15 minutes** — the
  "manifest check period," also configurable by Flowbird support staff (p.86).
- If a new update is identified via the manifest, the device **immediately downloads it in advance
  of its activation date**, in the **background**, without affecting functionality offered by the
  device (p.86).
- Once received, updates are **verified for authenticity and integrity**; only updates that pass
  verification are used. If an **invalid data set is detected, the FR sends an event to CloudFare**
  (p.86, GR-3/FRT-1).
- FR supports storing **both current and future sets of configuration data**; the future set
  **becomes active when the configured activation date/time is reached** (p.86).

## Transactional data, events & status (push model)
- FR sends the **transaction record to the back office within 10 seconds** of the transaction being
  completed (p.86).
- Successful delivery within that 10s window **relies on comms infrastructure outside Arrive's
  control** — i.e. the 10s target is not itself a hard guarantee if the network is degraded (p.86).
  **GAP** — this excerpt does not state what the device does if the 10s delivery fails (e.g. local
  queuing/retry); do not assume behaviour from other sections without a citation.
- FR also transmits **events and status information** for CloudFare to monitor (p.86).

## Out of Service / entering service, driven by CloudFare
- CloudFare can instruct the FR to **enter an Out Of Service mode** (p.86) — separate from the
  device's own local logic for going OOS.
- **Remote commands are CloudFare-initiated, but local device logic and parameters take precedence**
  — specifically so a remote command cannot inadvertently harm passenger experience, e.g. sending a
  device out of service **mid-transaction**, or sending a device into service while it is in a
  **degraded operational state** (p.87).
- Once a device has entered an **out-of-service** or **locked** state as a result of being
  instructed by CloudFare, it **can only exit that state by receiving an 'In Service' Command** from
  CloudFare (or, for exiting a **lock** state specifically, also by receiving an **'Out of Service'**
  Command) (p.87).

## Remote command types (all CloudFare-originated)
| Command | Effect |
|---|---|
| **Force Comms** | Directs the device to attempt a communication session with the back office, **immediately checking for a new staff list and manifest** (p.87) — i.e. bypasses the normal 15-minute check periods on demand. |
| **Out of Service** | Directs the device to go out of service. **Local device logic dictates when it reverts** to an alternative operation state, in line with device settings and user interactions (p.87). |
| **In Service** | Directs the device to attempt to go into service. **Local device logic dictates whether the command can be executed**, and dictates when the device later reverts to an alternative state (p.87). |
| **Lock** | Directs the device to enter a **locked** state. The device may only exit this state by receiving an **alternative command** from CloudFare (p.88) — i.e. not by local logic alone. |
| **Reboot** | Directs the device to execute a **reboot cycle** (p.88). **GAP** — no detail here on reboot timing safeguards (e.g. mid-transaction), or on what state the device resumes to after reboot; confirm before asserting behaviour. |

- **"Block" is explicitly NOT a device command** — it is a **device state managed entirely by
  CloudFare**: CloudFare both **initiates and confirms** the status change (p.88).
- Devices in the **blocked** state **will not receive an acknowledgement** to their request to
  communicate with the back office (p.88). **GAP** — the spec does not describe what, if anything,
  is visibly shown to the operator when a device is blocked (vs. simply not getting an ack);
  confirm on-screen behaviour before asserting a specific UI outcome.
- Should a Fare Register be instructed to go **out of service, lock, or be blocked** while it is
  **signed on**, it will **immediately sign off the driver**, then change to the new state (p.88).

## CR / requirement-id tags to track
GR-2, GR-4, GR-5, FF-5 (near-real-time comms, guaranteed delivery) · GR-3, FRT-1 (invalid update
data → event to CloudFare). Definitions of these tags are outside the excerpted range
(lines 15082–end); do not assume their scope beyond what is stated here.

## Suite implications
- Assert the **staff-list (15 min) vs manifest (15 min) check periods** are each independently
  configurable, and that a **Force Comms** command triggers both checks immediately, bypassing the
  timer.
- Assert **background download + activation-date gating** for updates: update downloads without
  disrupting device function, and only activates at its configured date/time — plus the **current +
  future config set** dual-storage behaviour.
- Assert **update integrity verification**: a corrupted/invalid update is rejected and produces an
  **event to CloudFare** (GR-3/FRT-1) rather than being applied.
- Assert the **10-second transaction delivery SLA** is measured from transaction completion (case
  should note the SLA is comms-dependent, not a hard device guarantee) — flag as **GAP** any
  assumption about local retry/queue behaviour beyond this excerpt.
- Assert the **unauthorised-device rejection path**: an unregistered device's comms are rejected and
  it self-transitions to **out-of-service** until a successful comms occurs.
- Cover **each remote command** (Force Comms, Out of Service, In Service, Lock, Reboot) as a
  distinct scenario, citing p.87–88, including:
  - **Local-precedence override** — a device mid-transaction must not be forced OOS by a remote
    command; a degraded device must not be forced into service.
  - **Exit-state gating** — a device in remote-OOS/locked state only exits via an explicit
    **In Service** (or, for lock, also **Out of Service**) command — never by local logic alone once
    CloudFare put it there.
  - **Lock is a one-way local exit** — device cannot self-exit Lock; only an alternative CloudFare
    command clears it.
- Assert **Block is state-only, not a command**: verify device behaviour is "no ack to comms
  requests" while blocked, and that both entry and confirmation of Block are CloudFare-side, never
  device-initiated.
- Assert **signed-on driver auto sign-off** on transition to OOS / Lock / Block while signed on.
- Flag the two **GAP** items above (10s-failure fallback behaviour; Reboot mid-transaction/resume
  state; Block on-screen behaviour) for the engineer Q&A loop before writing cases that assert
  specific behaviour beyond what's stated here.
