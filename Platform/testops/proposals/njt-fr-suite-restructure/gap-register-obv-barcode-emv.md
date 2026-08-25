# Gap Register & Q&A — NJT Fare Register (OBV Barcode / EMV)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · STALE CROSS-REFERENCE · Automatic acknowledgment's "section 6.1.2.1" target is unclear** — OPEN

`knowledge/njt/specs/fs002-obv-barcode-emv.md` §"Automatic acknowledgment" (p.53): the source spec text says
automatic acknowledgment (transaction-approval byte `'01'`) "performs the actions as per section 6.1.2.1" — but
no subsection 6.1.2.1 exists in the read structure (6.1.2 is "Barcode products", not further subdivided). This
almost certainly means the Barcode-Accepted flow under §6.1.3.1, but the spec's own cross-reference is
wrong/stale.

This does not currently block any drafted case — the existing automatic-acknowledgment cases (C4086251,
C4086252, C4098904–C4098906) already assert the Barcode-Accepted actions directly rather than by cross-reference,
so the suite is unaffected either way. Logged so the ambiguity in the source spec itself is tracked and doesn't
get carried forward into a future edit that trusts the stale reference.

Question for the engineer: can you confirm with the spec owner that "section 6.1.2.1" in the automatic
acknowledgment passage (p.53) was meant to reference the Barcode-Accepted flow (§6.1.3.1), and that this is a
typo/renumbering artifact rather than a reference to different, not-yet-identified content?

A:

source: `knowledge/njt/specs/fs002-obv-barcode-emv.md`, Gap 1.

---

**Q2 · UNDEFINED VALUES · "Unknown"-labelled post-2019 barcode ticket-type codes** — OPEN

`knowledge/njt/specs/fs002-obv-barcode-emv.md` "Barcode products / ticket-type mapping" (p.46-49): in the
supplemental (post-2019) barcode-product table, a large number of OBV Ticket Type codes (e.g. 315, 12010, 21201,
23201, 31001, 32001, etc.) are labelled **"Unknown"** as their own Ticket/Rider Class description in the spec
itself — not an extraction artifact, the spec provides no descriptive name for these codes, only a paper/MyTix
product-code mapping.

This blocks meaningful test authoring for these specific codes: a case can assert a barcode transaction occurred,
but cannot assert an expected on-screen "Ticket Type"/"Rider Class" text without a real definition. None of the
69 existing "Barcode Products" cases exercise one of these codes (consistent with there being nothing definable
to assert), and per this task's sampling approach no new case was drafted against them either.

Question for the engineer: are these "Unknown"-labelled codes actually sent by the OBV in production today? If
so, what product/rider-class name should a test assert is displayed/recorded for each? If they are legacy/unused
codes that the current OBV never sends, can the spec (or a note in `knowledge/`) confirm that so the suite can
explicitly mark them out-of-scope rather than leaving a silent hole?

A:

source: `knowledge/njt/specs/fs002-obv-barcode-emv.md`, Gap 2.

---

**Q3 · UNSTATED DIVERGENCE · Barcode zone display-vs-audit field split** — OPEN

`knowledge/njt/specs/fs002-obv-barcode-emv.md` "Transaction Process — Waiting for Driver" (p.50-51): the zone
information **shown to the driver** on a barcode transaction is derived from the **"barcode start zone"/"barcode
end zone"** fields in the `$F1` message, while the zone information that is **audited** uses the **"OBV start
zone"/"OBV end zone"** fields in the *same* `$F1` message — two different field pairs, not guaranteed identical.
The spec doesn't state when/why these would diverge or which is authoritative for fare purposes.

Every existing display-side case (C4085073, C4085879, C4086248, C4086251, C4086252) correctly cites the
"barcode start/end zone" fields for the displayed value. No case anywhere asserts the *audited* zone comes from
the separate "OBV start/end zone" pair — the Transaction Auditing cases (C4086257, C4086258) check product and
payment type only, not zone provenance. Per this task's explicit brief this gap was **not** drafted around (would
require guessing when/why the fields diverge) — logged here instead.

Question for the engineer: do "barcode start/end zone" and "OBV start/end zone" ever actually carry different
values in practice, or are they always identical in the current OBV implementation? If they can diverge, which
pair is authoritative for revenue/fare purposes, and should the suite add an explicit case asserting the audited
zone independently of the displayed zone?

A:

source: `knowledge/njt/specs/fs002-obv-barcode-emv.md`, Gap 3.

---

**Q4 · EXTERNAL DEPENDENCY · EMV OW/CT toggle gating depends on §4.1.3 (out of this excerpt's scope)** — OPEN

`knowledge/njt/specs/fs002-obv-barcode-emv.md` "Waiting for EMV Validation Information" (p.57-58): the OW/CT
toggle is available **only** on services with "Enable ISSCTT" set in service options, **and** only if CT is a
valid rider-class/transaction-type combination per §4.1.3 — which is out of this excerpt's scope (another agent's
area; see the related open gap on the Class/Transaction Combinations matrix in
`proposals/njt-fr-suite-restructure/gap-register-fare-structure.md` Q1).

The existing case C4086283 exercises the OW/CT toggle only in the state where it's already available; no case
tests either half of the gating condition (ISSCTT disabled, or CT invalid for the current rider class per
§4.1.3). Not drafted here per this task's brief — pull in the §4.1.3 combination-validity answer (Q1 in the
fare-structure gap register) before attempting this case.

Question for the engineer: once the §4.1.3 Class/Transaction Combination matrix is confirmed, can a case be
written asserting the OW/CT toggle is unavailable/disabled when "Enable ISSCTT" is off, and separately when CT
is not a valid combination for the current rider class?

A:

source: `knowledge/njt/specs/fs002-obv-barcode-emv.md`, Gap 4.

---

**Q5 · UNSTATED INTERACTION · Barcode automatic acknowledgment + Override Required** — OPEN (newly identified,
not one of the knowledge note's original 4 gaps)

`knowledge/njt/specs/fs002-obv-barcode-emv.md` "Automatic acknowledgment" (p.53) doesn't state whether or how
Override Required interacts with an unattended automatic acceptance. Override normally requires the driver to
set a product parameter before pressing Issue (C4086033, single-passenger, Waiting-for-Driver path) — but
automatic mode by definition proceeds without driver input, so it's unclear whether an Override-flagged
transaction can even be auto-accepted, or whether it always falls back to the Waiting-for-Driver flow regardless
of the approval byte.

By contrast, the equivalent EMV case (automatic mode + override) **is** directly covered (C4086278), so this is a
barcode-specific hole, not a general gap in the suite's automatic-mode coverage.

Question for the engineer: can an Override-Required barcode transaction ever be presented with approval byte
`'01'` (automatic), and if so, does the Fare Register still auto-accept it, or does Override force a
Waiting-for-Driver-style interaction regardless of the approval byte? Depending on the answer, a new case may be
needed (or the current absence may be correctly explained by Override always forcing manual handling).

A:

source: `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/obv-barcode-emv.md`
(C4086033, C4086251/C4086252, C4086278); `knowledge/njt/specs/fs002-obv-barcode-emv.md` "Automatic
acknowledgment".

---
