# FBD-100348 — Gate Acceptance (Production Approval) (distilled)

**Source:** `FBD-100348 Gate Acceptance V1.00` (28 Jul 2021, P. Weeks) — Flowbird GFTS Swing Gate
(TGS840). Distilled testable rules only — raw spec + read-across held locally, not committed.

> **Nature of doc:** a production-approval *acceptance report* of the **gate cabinet** against
> requirement IDs (PHY/ENV/INT/PER/FUN/PIC/RAM/COM/INT-integration). Many rows are marked **"To be
> validated on integration of Validator"** — those behaviours depend on the GV head and are the ones
> most relevant to system test. IDs below are the durable, testable requirements.

## Aisle configs & physical (PHY)
- **Standard aisle 600 mm**, **wide aisle 900 mm**; wide aisle must pass a wheelchair up to
  **1250 mm** long. Gate height **1095 mm** (raised to fit barcode reader + validator).
- Obstacles = **tempered glass, 10 mm**, ≥ **900 mm** tall closed, ~300 mm ground clearance; **two
  moving obstacles per aisle**, **motorised**; installable gap between obstacle pairs **50 mm**.
- Integrates a **Flowbird validator (lock-fixation)** + a **separate barcode-reader module**;
  validator target and barcode reader both mounted **750–1200 mm** above ground, accessible from the
  front without reaching over/under/around.
- **Buzzer** rated ≤ **80 dB**; circuit breaker cuts all PSU power; max cabinet weight **230 kg**.

## Electrical / performance (INT / PER)
- **230 V 50 Hz single-phase**; interfaces **2×Ethernet, 1×RS-232, 1×RS-485**; idle ≤ **150 VA**,
  peak **250 VA/unit** or **500 VA/aisle**, **6 A** rating.
- **Open time:** standard **≤ 650 ms**, wide **≤ 900 ms** after the validator authorisation command
  (900 mm glass obstacles). **Close time:** same 650 / 900 ms after passenger exit.
- **Boot to in-service ≤ 120 s** from power-off (incl. Built-in-Self-Tests).
- Distinguish **two people** apart to **23 mm**; brake withstands **200 Nm** before releasing.
- **Emergency push-through force:** standard **740 N**, wide **475 N** (either direction); from the
  controlled side with egress **< 200 N**. Brief power loss (**≤ 2 s**) → resume without reboot.

## Operational modes & functional behaviour (FUN)
- Modes: **Controlled** (entry / exit / bi-directional), **Fully Free**, **Locked**, **Maintenance**,
  **Evacuation**, **Out of Service**. **Evacuation takes priority over all modes** and opens in the
  evacuation direction (incl. on power failure).
- **Controlled:** stays closed until the **validator authorisation signal**; opens in passage
  direction only if **no obstruction** in the safety zone; closes a configurable time after
  authorisation + passage (or non-passage). Obstruction present → will not open/close, **signals an
  infraction** until cleared.
- **Open-fail:** cannot fully open within **3 s** → **immediately Out of Service** and close.
- **Close-fail:** reopen and retry; **Out of Service after 3 consecutive failures** to close (note:
  spec flags an internal FUN-0016 "2 attempts" vs FUN-0018 "3 attempts" ambiguity — treat **3
  consecutive** as the governing rule, confirm on integration).
- Bi-directional: obstacles already open keep the original direction if opposite passage validated;
  subsequent authorisation while open keeps it open (throughput).
- **Infractions:** declared for loiter after timeout, **>1 person** in aisle, or **wrong-direction**
  movement; buzzer sounds at configured volume; impact depends on mode.
- **Temporary override** (assisted passage): authorised user only, works **without back-office**
  (command from Flowbird reader to gate CPU), times out if passage not started, reverts to configured
  mode after passage.
- No throughput cap in peak / free / evacuation modes.

## Pictograms (PIC)
- Controlled: **static green arrow** on the enabled side, **static red cross** on the opposite side;
  **blinking red cross** marks the side where an infraction is detected (opposite side static red);
  cleared infraction reverts to default. **Locked / Maintenance** = static red cross both sides.
  **Out of Service** = blinking red cross both sides. **Evacuation** = green arrow exit side, red
  cross entry side.

## Gate↔Validator integration (INT, XML-RPC — "to be tested on production")
- Protocol = **XML-RPC per CO119310_GTO_TGS_V06R02**. A **heartbeat** command between gate and both
  validators, **configurable rate**, ≥ **1/second** capable.
- **Loss of heartbeat from either validator for the configured period → immediate MAJOR FAULT.**
- **Power-up defaults to Out of Service**; enters service **only when both validators communicate**
  and BIST passes (major fault during BIST → stays Out of Service). On mains restore the gate returns
  to its **previous operational mode** (absent major fault).
- Validator commands drive: mode changes (entry / exit / bi-di / free / evacuation / OOS), buzzer
  config, **authorise-passage** (open obstacles), and diagnostics (sensor + actuation test results).
  All open/monitor/mode management is supportable over the **Ethernet** validator↔gate interface.

## Suite implications (GV / gates)
- The **validator-dependent rows** (INT heartbeat/BIST/mode/authorise, FUN-0013/0021/0028/0030-0043,
  RAM-0007, buzzer) are the **system-test surface** — the cabinet-only PHY/ENV/COM rows are factory
  acceptance, mostly out of scope for functional suites.
- Assert **authorise → open within 650/900 ms**; **no authorise → stays closed**; obstruction blocks
  open/close and raises an **infraction**.
- Assert **mode matrix** incl. **evacuation priority**, power-fail open direction, and **pictogram**
  states per mode/infraction.
- Assert **heartbeat loss → major fault**, **power-up = Out of Service until both validators comms**,
  and **mains-restore returns previous mode**.
- Assert **open-fail 3 s → OOS** and **3-consecutive-close-fail → OOS** (confirm the 2-vs-3 ambiguity
  on integration).
- Cross-ref **FBD-100653/100654** for the router/interface + commissioning that make the GV heads talk
  to the gate; the XML-RPC command set lives in CO119310_GTO_TGS.
