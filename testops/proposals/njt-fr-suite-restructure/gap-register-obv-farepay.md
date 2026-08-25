# Gap Register & Q&A — NJT Fare Register (OBV Fare Pay card)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · SCOPE · Family (6) / Foreign (7) outgoing rider-classification mapping is undocumented** — OPEN
FS002 §6.3.1.4 (p.67-68, "Table – Outgoing FR to OBV mapping") lists outgoing FR→OBV codes for
Adult, Child, Senior, Student, and explicitly marks Employee as N/A/not selectable — but Family (6)
and Foreign (7), which exist as FR rider classifications elsewhere in the spec, have no outgoing
mapping row at all. It is not stated whether Family/Foreign are simply never selectable/sendable in
this flow, or whether the mapping table was incompletely transcribed. This blocks writing a
confident case for Family/Foreign under approval mode 03 (Waiting for NJT Card Validation
Information) — no existing case in the dump attempts one either, which is correct behaviour given
the gap, but the gap itself needs resolving before the suite can claim exhaustive rider-class
coverage for mode 03.
A:
source: `knowledge/njt/specs` FS002 §6.3.1.4 distilled note (p.67-68); existing outgoing-mapping
cases `C4086361`-`C4086365` (Adult/Child/Senior/Student/Student-not-enabled only, no Family/Foreign).

---

**Q2 · VALUE · "Magnetic or smart card pass" payment-type determination for Ticket audit is unconfirmed** — OPEN
FS002 §6.3.2.6 (p.76) states Ticket Product transactions audit with payment type "magnetic or smart
card pass" but never states the rule by which the FR picks one of those two values for a given
transaction — is it card-type-driven (e.g. from a field in $F4), config-driven, or is the literal
compound string always written as-is regardless of card type? Every existing Ticket Transaction
Auditing case (`C4086678`-`C4086683`) asserts the literal ambiguous compound string, which is
correct per the spec text as written but doesn't resolve whether a more specific single-value
assertion should ever be possible. Answering this could let those six cases be tightened to assert
the actual determined value instead of the compound placeholder.
A:
source: `knowledge/njt/specs` FS002 §6.3.2.6 distilled note (p.76); existing cases `C4086678`,
`C4086679`, `C4086680`, `C4086681`, `C4086682`, `C4086683`.

---

**Q3 · SCOPE · Product-code mapping (§6.1.2) and CT-validity matrix (§4.1.3) are out of this note's range** — OPEN
FS002 §6.3.2.5 (p.75) states the Ticket Type Pass → product mapping is "the same as per the barcode
products, see Barcode products in section 6.1.2" — the actual product-code lookup table lives there,
not in §6.3. Separately, §6.3.1.3 (p.65) gates CT selectability on "a valid rider-class/transaction
combination per §4.1.3", also out of range. Neither table is reproduced in the distilled §6.3 note
used for this cross-examination, so the 55 Product Mapping cases (`C4086604`-`C4086658`, sampled not
exhaustive — see findings) and the CT-eligibility gating cases drafted here cannot be independently
verified against the source tables from this note alone. Before calling Product Mapping or
CT-eligibility coverage complete, cross-reference the sibling knowledge notes that own §6.1.2 and
§4.1.3.
A:
source: FS002 §6.3.2.5 (p.75) and §6.3.1.3 (p.65) distilled note pointers; sibling notes covering
§6.1.2 (barcode products) and §4.1.3 (rider class/transaction validity matrix) — not yet
cross-referenced against this area's cases.

---

**Q4 · CONFLICT · "Pop-up window" vs "SV/ticket transaction screen" — one UI or two?** — OPEN
FS002 §6.3.2.3 (p.71-73) calls the Waiting-for-zones UI a "pop-up window", while §6.3.1.1/.2/.3 and
most of §6.3.2 call the equivalent UI "the SV transaction screen" / "the Fare Pay ticket transaction
screen". Existing Ticket Transaction Auditing cases for Waiting for Zones and Waiting for Rider
Classification and Zones (`C4086682`, `C4086683`) both say "the zone entered on the pop-up window",
matching the spec's own wording exactly — so the cases are not wrong, but it's unconfirmed whether
this is a genuinely distinct overlay UI or just inconsistent spec terminology for the same screen.
This affects whether future HMI-level cases should treat "pop-up window" as a distinct screen state
from the "Fare-Pay Details" overlay already covered in `C4088154`-`C4088183`.
A:
source: FS002 §6.3.2.3 (p.71-73) distilled note; existing cases `C4086682`, `C4086683`;
`knowledge/njt/specs/hmi01-fare-register-hmi.md` FARE-PAY Transactions screens (`C4088154`-`C4088183`).

---

**Q5 · SCOPE · "Override Required" screen asserted for Ticket Product Processing but only documented for Stored Value** — OPEN
FS002 §6.3.1.1 (pp.60-61) documents the "Override Required" Tx Result message as an SV-specific
override flag behaviour. The distilled §6.3.2 (Ticket Product Processing) note does not carry any
equivalent override-flag rule. Yet the case dump contains eight Ticket Product Processing cases
asserting an identical "Override Required" screen and flow — `C4086418`, `C4086419` (Automatic),
`C4086416`, `C4086417` (Waiting for Driver), `C4086421`, `C4086423` (Waiting for zones), `C4086426`,
`C4086430` (Waiting for Rider Classification and Zones). Is the override flag a generic Fare Pay
card mechanism that applies to both SV and Ticket (and the distilled note simply didn't carry it
into the §6.3.2 range), or were these eight cases incorrectly copied from the SV family during
authoring? This determines whether the eight Ticket "Override Required" cases are valid coverage or
need correcting/removing.
A:
source: FS002 §6.3.1.1 (pp.60-61) distilled note (override flag documented for SV only); existing
Ticket cases `C4086418`, `C4086419`, `C4086416`, `C4086417`, `C4086421`, `C4086423`, `C4086426`,
`C4086430`.

---
