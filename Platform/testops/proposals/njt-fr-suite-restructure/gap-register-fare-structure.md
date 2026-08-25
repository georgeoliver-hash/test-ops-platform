# Gap Register & Q&A — NJT Fare Register (Fare Structure)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · CONFLICT · Class/Transaction validity matrix cannot be reconstructed from the extracted PDF text** — OPEN
`knowledge/njt/specs/fs002-fare-structure.md` §4.1.3 (p.22–23): the spec presents a checkmark matrix of
25 transaction-type rows (IDs 0–24, ID 15 unused) x 7 class columns (Adult/Child/Senior/Student/
Family/Employee/Foreign) defining which Class/Transaction combinations are valid, and states this
matrix also drives auto-select behaviour (when an operator picks a Class with only one valid
Transaction Type, the system should auto-select it).

The PDF-to-text extraction collapsed the checkmark grid into a run-on line and lost the column
(x-position) alignment that distinguishes which class column each checkmark belongs to. Confidently
extractable: row 15 ("not used") has zero valid classes (fully retired); every other row has at
least one valid class; rows 3 (Ticket) and 5 (Transfer Rx) look broadest, rows 2/4/9/16/18/23 look
narrowest by checkmark count — but the specific class(es) each of those maps to is NOT confirmed.

This affects the 23 existing "Class / Transaction Combinations" cases (C4087221–C4087243), each of
which asserts a specific split of which classes are valid vs. invalid for its transaction type (e.g.
C4087222 "Cash" asserts Adult/Senior/Child valid, Student/Family/Employee/Foreign invalid). Per this
task's method, those specific per-case splits were NOT re-verified or second-guessed against the
unreliable extraction — they are left as-is, but their correctness against the actual p.22–23 table
is unconfirmed. It also blocks two suite-implication items noted in the knowledge file: (a) explicit
negative/rejection cases for combinations the spec marks invalid, and (b) an auto-select-on-single-
valid-Transaction-Type case.

Question for the engineer: can you visually re-check the checkmark matrix on p.22–23 of
`NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` against the class columns, and confirm
(or correct) the per-transaction-type valid-class list — starting with the 23 transaction types the
suite already has combination cases for? If the existing 23 cases' asserted splits turn out wrong,
those cases need editing (not new cases) once confirmed.

A:

source: `knowledge/njt/specs/fs002-fare-structure.md`.

---
