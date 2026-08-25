# FBD-100391 — Bus Validator Communication Protocol (distilled)

**Source:** `TFTS Bus Validator Communication Protocol Specification V0.01` (13 Dec 2021, Chris Warnes).
Distilled testable facts only — raw spec held locally, not committed.

> **STUB WARNING — this spec is effectively empty.** V0.01 contains only the document
> skeleton (Purpose/Scope/Glossary headers) plus an empty "Requirement Number | Description"
> table. **No protocol messages, framing, states, thresholds, or config are defined.** Do not
> author BV comms-protocol cases from this document — there is nothing testable in it yet.

## Scope (as stated)
- Defines the communication protocol between the **on-bus ETM** (controller) and **one or more Bus
  Validators (BV)** installed on the bus, so the ETM can **control the BV(s)**.
- Establishes the ETM↔BV relationship (ETM is master; BV is controlled peripheral) — but the actual
  message set is not specified.

## Testable facts available
- **None.** The requirements table is present but unpopulated in this version.

## CR / dependency notes
- Related device facts for BV live in FBD-100320 (BV has embedded Feig payment device, Travel Charge
  NMI Terminal Group) and FBD-100716 (BV listed as an ABT device type; cEMV inspection is HHD-only).

## Suite implications (BV)
- **Coverage gap — flag, do not fill.** The BV comms protocol is undefined in the requirements set.
  Any ETM→BV control behaviour (mode changes, validation relay, heartbeat between ETM and BV) is
  **unspecified**; suite cannot claim coverage and must record this as a **blocking documentation
  gap** for the BV device type.
- Chase an issued/populated version of FBD-100391 (or the equivalent gate-validator XML-RPC protocol
  in FBD-100348 INT-* as a possible analogue) before writing BV control-plane cases.
- What *is* groundable for BV today comes from other specs (TID/TK allocation, embedded Feig
  payment), not this one.
