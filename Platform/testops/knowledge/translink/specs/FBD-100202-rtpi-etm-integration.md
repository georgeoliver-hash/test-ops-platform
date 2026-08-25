# FBD-100202 — RTPI Server & ETM Integration (DAIP) (distilled)

**Source:** `FBD-100202 RTPI & ETM Integration Specification V2.00` (16 Feb 2022, C. Kiraz) (folder also holds a copy of the RTIGT030 v1.1 interface spec v2.00).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100345 (RTIGT030-V1.1 DAIP interface — message field detail). Requirement CR025 / REQ-3104.0.

## What it is
- Wayfarer 6s **ETM sends real-time passenger info to the Vix RTPI server** over **3G/4G using RTIGT030-v1.1 DAIP** (UDP-based). Goal: ETM replaces separate on-bus RTPI hardware. **RACI:** mobile network/SIM = Translink; RTPI server/env = Vix; ETM device = Flowbird.
- **NAT rule:** if a NAT router/load-balancer sits between, responses must return to the ETM on the **same IP+port** as the original source; **ETM only accepts responses addressed to the IP+port it logged on from** for the session.

## Session + message model (assert flows)
- **Log On** (msg 10/0A): ETM sends vehicle identity, **retransmits until a response** is received; server returns a **Session Vehicle Identifier (SVID)** used for all subsequent messages. On a parseable error response the ETM **does NOT retry** but **logs it**.
- **Log Off** (msg 11/0B): best-effort, **no retry**, ack not required; may be absent on sudden power-off — **server must time out and close idle sessions**.
- **Journey Details** (msg 30/1E) — full; **Start of Journey** (msg 31/1F) — cut-down, for subsequent journeys after break/partial sign-off; **End of Journey** (msg 39/27) — ends trip but **keeps the session open** (ETM still receives events). Journey/Start require **ack + retry until acked**; always accompanied by a Position Update.
- **Position Update** (msg 40/28): sent regularly; **every 4th requires an ack** to confirm end-to-end liveness. **GPS unavailable → null coordinates** (`0x7FFFFFFF` lat/long, `0xFF` bearing, `0` satellites).
- **Events**: only **Departing from Stop (type 128 code 0)** and **Arriving at Stop (type 128 code 2)** are in scope; require server ack + retry. Server→ETM events also require ack. **Ack = msg 127 code 0** with `Reference Sequence ID` linking to the original.

## ETM operational-state gating (assert the matrix)
- RTI ability depends on ETM mode. **Log On/Off + Position Update work in ALL states** (Idle, Driver, Route Error, In Service, Driver Break, Operator, ErrorOutOfService, ForcedOutOfService, UnCommissioned).
- **Journey Details** only in Driver / In Service / Operator states. **Start/End of Journey and Stop Depart/Arrive events ONLY in "In Service".** Powered-down/power-save ETM sends nothing.

## Error handling (assert retries)
- Retry count is a **configured parameter (n)** for Log On, Journey Details, Start/End of Journey, Stop events. **Log Off has no retry.**
- **Position-update failure**: retry; if network/server still down the ETM **ends the journey then logs off**, and keeps re-sending Log On periodically until acked or powered down.
- **Stop depart/arrive detection failure (incl. GPS)** → **ETM sends NO event** (must not fabricate). Departing-from-stop only sent if GPS functional.
- **Log On error codes** (msg 20 response): 0 success, 1 Unknown Sender, 2 Unknown Running Board, 3 Unknown Operator Code, 4 Unknown Vehicle ID, 5 Unknown Service Code, 6 Unknown Journey Number, 7/8 unknown event, 9/10 config/serial unsupported, 11 Duplicate Vehicle ID, 12 No SVID available, 13 Corrupt Message.

## Assumptions / out of scope
- ETM must not be power-save to talk to RTPI; RTPI must retry its acks; **ETM must not display/report RTI itself**; only the listed messages/events are in scope.

## Suite implications (device/integration)
- Assert **state-gated transmission**: Start/End Journey + stop events only in "In Service"; Log On/Off + Position Update in every state.
- Assert **retry semantics**: retransmit-until-ack for Log On/Journey/Start/Stop (n configurable), **no retry** for Log Off/parse-error responses, and the **every-4th-Position-Update ack**.
- Assert **GPS-loss → null position** and **detection-failure → no stop event** (no fabricated data).
- Assert **NAT/session binding** (ETM rejects responses from a different IP/port) and **server idle-session timeout** when Log Off is missing.
- Assert the **Log On error-code** handling (no retry + logging on error).
- Gap: this is an ETM↔Vix integration surface (not BOS/Merit) — needs a stubbed RTPI server to test; likely absent from current suites.
