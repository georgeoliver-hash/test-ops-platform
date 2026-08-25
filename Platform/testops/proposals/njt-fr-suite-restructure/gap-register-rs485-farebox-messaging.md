# Gap Register & Q&A — NJT Fare Register (RS485 Farebox Messaging)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · GAP · No defined behaviour for sustained non-response from the Farebox to a Poll** — OPEN

`knowledge/njt/specs/is001-fr-farebox-messaging.md` ("Timing / error handling" section): IS001
defines no poll interval, timeout value, retry count, or backoff for the FR↔Farebox RS485 link.
The existing Poll cases (C4098971–C4098973) cover a single retry-on-NAK/timeout sequence but the
spec itself never says what happens if the Farebox stays silent through the retry sequence — no
escalation, alarm, or fallback state is specified anywhere in this document. This is a *different*
channel from the back-office "Comms Locked" state in `knowledge/njt/specs/fs002-functional-states.md`
§3.1.2 (that's FR↔back-office; this is FR↔Farebox) — do not conflate them.

The one adjacent documented behaviour is FR ID Information's "after a nightly reboot or comms
loss/recovery event" re-announcement (p.10) — a FR-initiated re-handshake on *recovery*, not a
definition of what happens *during* a sustained outage.

Question for the engineer: is sustained-Farebox-silence escalation/alarm behaviour defined in
document [1] ("NJT Communications Protocol Description", not sighted), or is it genuinely
undefined in the interface spec set? If undefined anywhere, this is a candidate
**POSSIBLE DESIGN/SPEC BUG** — a bus with no farebox response has no documented driver-facing or
back-office-facing failure signal in this interface layer.

A:

source: `knowledge/njt/specs/is001-fr-farebox-messaging.md`.

---

**Q2 · GAP · CRC algorithm/width is referenced but never defined** — OPEN

Every RS485 message frame in IS001 ends `... <CRC>` (p.8 onward) but the CRC variant, width, and
polynomial are never specified in this document. It is presumably defined in document [1] ("NJT
Communications Protocol Description", not sighted). Existing cases (e.g. C4098984, C4098985) refer
to "a valid ... CRC" / "a CRC failure" generically without asserting a specific algorithm, which is
correct given the current evidence — no case has been drafted or edited to assume a specific CRC
variant.

Question for the engineer: can you confirm the CRC algorithm (e.g. CRC-8/CRC-16 variant, poly,
seed) from document [1] or the wider protocol description, so cases needing a concrete
worked CRC value (if any are ever required) can cite it?

A:

source: `knowledge/njt/specs/is001-fr-farebox-messaging.md`.

---

**Q3 · GAP · 8-digit Enter Service driver-number field vs. 6-digit system support has no stated failure mode** — OPEN

IS001 p.11 (Enter Service, `10 12`) footnotes that the driver-number field is 8 digits wide
("future-proofed") but the system currently only supports 6-digit driver numbers. The spec states
the limit but not the behaviour on overflow — truncate the extra digits, reject sign-on, pad, or
something else. This sits inside the `(NOT COMPLETE)` "Farebox - Enter Service" section: the other
gaps in that section (payload composition, response handling FB Status/NAK, the non-Exact-Fare
negative case) were groundable and have been drafted in
`rs485-farebox-messaging.cases.yaml`; this one specifically was not, because inventing the failure
mode would violate the no-gap-filling rule.

Question for the engineer: what happens today if a driver number longer than 6 digits is entered
at sign-on — is it rejected at the sign-on screen before an Enter Service message is ever built, is
it truncated, or is there another documented behaviour? If genuinely unspecified anywhere
(including FS002 or the sign-on functional spec), flag as a **POSSIBLE DESIGN/SPEC BUG**: an
8-digit wire format exists for a value the system can't yet produce without a defined boundary
behaviour.

A:

source: `knowledge/njt/specs/is001-fr-farebox-messaging.md`.

---
