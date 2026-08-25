# FBD-100345 — RTIGT030-V1.1 DAIP Interface (distilled)

**Source:** `RTIGT030-V1.1 DAIP Interface Specification v1.1` (22 Jul 2021, C. Kiraz).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100202 (RTPI/ETM integration — states, retries, error handling). This spec = the **wire-level message contract** between Flowbird GFTS and Vix RTPI.

## Transport / encoding
- **UDP** 2-way protocol (smaller packets than TCP → less mobile data). Field format codes: **C** = ASCII char (null-terminated, no leading spaces), **N** = BCD nibble/flags, **X** = hex byte (0-255 / 8 flags), **S** = signed 2's-complement int, **U** = unsigned int.
- GPS null sentinels: lat/long `0x7FFFFFFF`, bearing `0xFF`, satellites `0` = no fix. Lat/long in **milliarcsecs** (N +, S −; E +, W −). Bearing = degrees ÷ 2. Journey start times **BCD hhmm**, current time zone incl. summer time.

## Message IDs (assert structure)
- **10** Log On req (Operator ID 9C, Vehicle ID/Fleet 7C, optional OBU ID). **20** Log On response (SVID 2X, Error Number, server addr/port). **11** Log Off req (SVID).
- **30** Journey Details, **31** Start of Journey, **39** End of Journey — carry Service Code (6C, route ID), Running Board (7C), Journey Number (5C, = Trip ID), Journey Scheduled Start Time (BCD hhmm), Duty Number (6C), Public Service Code (6C, route name), Direction (0=OUT/1=IN/2=BOTH); 30 also has Depot Code (from TransXChange GarageCode), Driver ID, First/Destination Stop ID (12C each).
- **40** Position Update: lat, long, bearing, satellites, **Position Quality** (bits 0-3 last stop, 4-7 GPS; 0=invalid 1=valid), **Last Stop Index** (count from 1 along stop pattern, 0=not reached first), Distance from last stop, optional Schedule Deviation.
- **50** ETM→server Event / **60** server→ETM Event: both carry **Sequence ID** (unique 1-65535, 0 reserved, rolls over) + **Reference Sequence ID** (links to the message being answered) + lat/long + Message Type/Code/Params.

## Enums worth asserting
- **Log On error codes:** 0 success, 1 Unknown Sender, 2 Unknown Running Board, 3 Unknown Operator Code, 4 Unknown Vehicle ID, 5 Unknown Service Code, **6 Unknown Trip Number**, 7 Unknown Event, 8 Unknown Event data, 9 Config unsupported, 10 Serial unsupported, 11 Duplicate Vehicle ID, 12 No SVID available, 13 Corrupt Message; 14-127 RFU, 128-255 scheme.
- **Stop events:** type **128 code 0 = Stop depart**, **128 code 2 = Stop arrive** (param = Stop Id). **129 code 3 = Excessive Idling** (param = idle timeout). **127 code 0 = Acknowledgement** (params len 0).
- **Driver-message short codes** (type/code): 0/1 Accident, 0/2 Obstruction, 0/3 Diverting, 0/4 Abandoning Trip, 0/5 Curtailing Trip; 1/0 Request radio call, 1/1-1/6 accept/decline duty·rest day·overtime, 1/7 Request Relief, 1/8 Ack incoming; 2/0 Puncture, 2/1 Low Oil Pressure, 2/2 High Engine Temp, **2/3 Passenger Load** (data 0=empty,1=¼,2=½,3=¾,4=full,5=overloaded).

## Scope note
- Driver messaging, duress/fire alarm, closure & diversion messaging are **out of scope** for Translink (spec lists the codes but they are not used). Excessive Idling appears here but not in the FBD-100202 v2.00 in-scope set — confirm before testing.

## Suite implications (device/integration)
- Assert **message encoding** per field-format codes (BCD start times, milliarcsec lat/long, null sentinels) and **Direction enum** (0/1/2).
- Assert **Sequence ID roll-over** (65535→1, 0 reserved) and **Reference Sequence ID** correctly links acks to originals.
- Assert **Position Quality bit-packing** and **Last Stop Index** counting rule.
- Assert only the **in-scope events** (stop arrive/depart; verify idling) are emitted; out-of-scope driver/alarm codes are not exercised for Translink.
- Gap: pure protocol conformance needs an RTPI test harness/decoder — not a device-UI or BOS test; almost certainly uncovered today.
