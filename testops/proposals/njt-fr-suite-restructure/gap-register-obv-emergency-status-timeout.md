# Gap Register & Q&A — NJT Fare Register (OBV Emergency Mode / Status / Timeout)

Source: `knowledge/njt/specs/fs002-obv-emergency-status-timeout.md` (`NJT_FRFRP_FS002` §6.4–6.7) and
the cross-exam in `findings-obv-emergency-status-timeout.md`. Per `CLAUDE.md`'s hard rule, none of
these are guessed at — each is a question for the engineer; answers get cited back into the spec
note and, where relevant, into the affected cases.

## Q1 — Emergency Mode repeat-trigger ambiguity

**Question:** §6.4 says the FR displays the entry message when it "first sees" the OBV Emergency
Mode status bit set. Does a *second, later* Emergency-Mode entry (bit set again, after having
already been cleared once) re-trigger the entry message, or does "first" mean only the very first
occurrence ever / per session / per trip?

**Why it matters:** determines whether a repeat-entry case is even valid to write. Writing one either
way without an answer risks asserting invented behaviour.

**Status:** Open. (`NJT_FRFRP_FS002 p.77`)

## Q2 — OBV Status bit-pattern table (Bit 7…Bit 0, Part 1 / Part 2)

**Question:** the §6.5 scenario-to-bit-pattern table's column headers and cell values were
interleaved by PDF-to-text extraction and are not reliably transcribable. Can you supply the
authoritative bit table (re-extracted from the original PDF table, or a clean copy) so scenario
→ bit-pattern mappings can be cited correctly?

**Why it matters:** no case may assert a specific bit combination until this is resolved.

**Status:** Open. (`NJT_FRFRP_FS002 p.78`–`p.79`)

## Q3 — OBV Status "N/A" values: genuine display state or extraction artifact?

**Question:** for every §6.5 scenario, the legible text says "status bar shows N/A." Does the status
bar genuinely display nothing (or literally "N/A") for all of these scenarios, or is "N/A" itself a
symptom of the same table-extraction corruption as Q2?

**Why it matters:** existing legacy cases (C4085171–C4085178, C4086755, C4086756) test "the symbol
displayed matches ... the table" by cross-reference rather than asserting a literal value, which
sidesteps this — but if a future case ever asserts "no status bar text" as an expected outcome, it
needs this confirmed first.

**Status:** Open. (`NJT_FRFRP_FS002 p.78`–`p.79`)

## Q4 — SV transaction: does a Transaction Timeout (§6.7) path exist?

**Question:** §6.7's auto-accept/auto-reject enumeration names only Barcode, EMV, and Fare card — SV
(stored value) is not listed, even though §6.6 (Communication loss) explicitly includes SV among the
affected transaction types. Does SV have a Transaction Timeout auto-accept/auto-reject path at all,
and if so, what is its outcome (auto-accept, auto-cancel, or something else)?

**Why it matters — raised urgently:** the existing suite already contains three cases
(**C4086765, C4086766, C4086767** — "Transaction Timeout - NJT Card Stored Value") asserting that SV
**auto-accepts with a printed receipt** on transaction timeout. Per this cross-exam, that behaviour is
currently **UNCONFIRMED** against the cited spec section — it may be correct (SV could simply have
been omitted from the §6.7 excerpt's list by oversight) or it may be asserting functionality that
doesn't exist. Do **not** edit or remove C4086765–C4086767 until this is answered; if confirmed
correct, cite the confirming source into those cases' Refs field; if incorrect, raise a
**POSSIBLE DESIGN/SPEC BUG** (or correct the cases, whichever the answer implies) as a follow-up.

**Status:** Open — highest priority of this batch (existing, executed test cases may be wrong).
(`NJT_FRFRP_FS002 p.80`–`p.81`, cf. §6.6 p.80)
