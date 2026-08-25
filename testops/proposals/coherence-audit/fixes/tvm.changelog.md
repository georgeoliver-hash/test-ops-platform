# TVM coherence-audit fixes — changelog

**Suite:** `**NEW** TVM Test Suite` (30284), project 42. **Pushed to TestRail:** yes, via
`python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm.rewrite.json --commit`
(dry-run counts matched the commit counts: 7 updated, 27 removed(ZZ), 0 skipped, 0 missing).
Post-push `audit --suite 30284`: **CLEAN** — 174 cases audited, 0 blocking findings, 24 advisory
`title-too-long` (pre-existing across the suite, unrelated to this change).

All three facts below were confirmed directly by George (live-system confirmation), 2026-07-21 —
see `proposals/coherence-audit/gap-register.md` Q5, Q6, Q15.

---

## 1. Barcode / Collect-Ticket-Code cluster — 3 cases reworded

**Fact:** the TVM has **no barcode scanner**; ticket collection is **Collect-Ticket-Code entry
only** (manual code entry), matching spec FBD-100317. Confirmed by George, 2026-07-21.

The audit's "~30 barcode-collection cases" estimate was a rough upper bound covering the whole
Barcode Redemption + Ticket Collection area. Enumerating the live suite (full-text search across
title/preface/preconds/steps/expected for scan/present/barcode/scanner/BRID in a TVM context) found
that **most of that area was already correctly grounded** (the barcode redemption state machine
C4103620–C4103633 matches FBD-100483 and already asserts booking-reference/Collect-Ticket-Code
entry, not scanning). Only **3 cases** actually assumed a scan/present/BRID action:

| Case | Problem | Fix |
|---|---|---|
| **C4103628** | "the multiple-use barcode is **presented**" — TVM has no scanner to present a barcode to. | Reworded trigger to "the customer **enters** the multiple-use ticket's Collect Ticket Code"; removed the 2026-07-17 UNCONFIRMED scanner marker (now confirmed). Rejection message unchanged. |
| **C4103729** | Title/step used "**BRID**" — a POS/HHD-only mechanism (12-digit), not a TVM one; contradicted C4103629. | Renamed to "booking reference (Collect Ticket Code)", matching C4103620's wording. |
| **C4103677** | Precondition "valid **collection barcode** or booking code"; step "**presents** the collection reference" — implied a scan. | Dropped "barcode"/"presents"; now "an example pre-paid order identified by a valid booking reference (Collect Ticket Code)" / "enters the booking reference (Collect Ticket Code)". |

Not touched (already correct, reused as the wording pattern): C4103620, C4103629. Not touched
(ticket-format case, not an entry-action case): C4103633. Confirmed false positives from the keyword
search (matched only on unrelated "24+" text, no scan/barcode assumption): C4103786, C4103795 (this
one moved to the smartcard cluster below), C4103797, C4103798.

**Noted, not actioned:** C4103729–C4103732 duplicate the entry-validation cases already in Barcode
Redemption (C4103620/25/26) — flagged as a future consolidation candidate, out of scope here.

---

## 2. Smartcard / ABT cluster — 27 cases condemned (`ZZ_DELETE_REVIEW`), 3 reworded

**Fact:** the TVM has **no smartcard reader/writer** at all — issue, read, top-up, and validation
are **POS / Card-Bureau only** (FBD-100261: "POS is the only device that issues these smartcard
products"; FBD-100236: ABT personalisation is a Card-Bureau/AbtPerso function). Confirmed by George,
2026-07-21, as a blanket "no reader/writer" answer — not just an issue-only restriction.

Enumerated the full **Smartcards & ABT** section (887775, 21 cases) and **Mini Statement** section
(887790, 5 cases), plus a full-text keyword sweep for smartcard/smartlink/multi-journey/travelcard/
smartpass/ylink/24+ terms across the whole suite. Checked whether any genuine TVM-side action
survived (e.g. top-up without issue) per the task's instruction — it does not: George's confirmation
is that there is **no reader/writer whatsoever**, so top-up, read, mini-statement, and
concession-by-presented-card are all equally impossible, not just card issue. **Nothing is
salvageable in any of the 27 cases** — every one is condemned rather than reworded:

**Section 887775 (21 cases):** C4103599 (Buy a Smartcard/issue), C4103600–C4103602, C4103615
(Smartcard Top-up variants), C4103603 (Smartcard Details), C4103605–C4103609 (Concession-by-card:
yLink / 24+ / half-fare / free-concession / funded-disability), C4103610 (Staff Pass),
C4103611–C4103614 (Invalid Smartcard: faulty / expired / dual-presented / passback),
C4103616 (card removed early), C4103617–C4103619 (ABT issue / AID-rejection / top-up).

**Section 887790 (5 cases):** C4103733–C4103737 (Mini Statement: Multi-Journey after top-up,
Multi-Journey after validation, Period Pass after top-up, DayLink after top-up, printed-layout-vs-HMI).

**Elsewhere (1 case):** C4103795 ("Screensaver Wake-Up — a smartcard starts the smartcard flow") —
same reason, presenting a smartcard to wake the TVM is not possible.

Total condemned: **27**. (C4103604 vs C4103733 and C4103604 itself were both already flagged by the
audit as duplicates of each other before being condemned — both are now condemned, so the duplication
finding is moot.)

**3 cases reworded (not condemned)** — smartcard mentioned only as one throwaway item in a Data
Variations list, not as the case's actual subject; the primary test (cash-sale lockout / audio
prompts / idle-launch performance) is valid and untouched, only the invalid smartcard variation was
removed:

| Case | Change |
|---|---|
| **C4103786** (Device Lockout — cash sale at limit) | Removed "smartcard top-up" from the Data Variations list. |
| **C4103797** (Audio Prompts) | Removed "smartcard" from the payment-input Data Variations list. |
| **C4103798** (Performance — idle launch) | Removed "Smartcard Top-up" from the workflow Data Variations list. |

**27 + 3 = 30**, matching the audit's "~30" estimate once the full set was verified case-by-case
rather than assumed.

---

## 3. Scottish banknote — C4103641 corrected

**Fact:** Scottish banknotes are sterling (issued under UK law by Scottish clearing banks), not
foreign currency. George confirms the TVM should **accept** a Scottish note like any other GBP note
— the case's premise ("rejected as foreign/non-sterling") was factually wrong.

**Fix:** flipped the expected outcome from reject to accept, and retitled from "Banknotes — foreign
notes are rejected" to "**Banknotes — a Scottish banknote is accepted as valid sterling**" so title/
preface stay coherent with the corrected (accept) result — a case titled "rejected" with an "accept"
expected outcome would itself be an audit-blocking incoherence. This also resolves the contradiction
the original audit flagged against C4103639 ("valid UK banknotes from every issuing bank" — which
this case now actually exercises for a non-Bank-of-England issuer).

**Flagged, not actioned:** repurposing this case removes the only "foreign notes rejected" case in
Payments — Cash, so there is now no case testing genuine non-sterling banknote rejection (e.g. Euro).
C4103638 covers foreign **coins**, but no sibling covers foreign **banknotes**. Logged as a gap on the
case rather than inventing a new one (out of scope for this fix — no new case authoring was
requested).

---

## Totals

| Cluster | Cases found | Action |
|---|---:|---|
| Barcode / Collect-Ticket-Code | 3 | reworded |
| Smartcard / ABT (primary) | 27 | condemned (`ZZ_DELETE_REVIEW`) |
| Smartcard mention (secondary, data-variations only) | 3 | reworded |
| Scottish banknote | 1 | reworded |
| **Total rewrite entries** | **34** | 7 reword + 27 remove |

**Push:** `python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm.rewrite.json --commit`
— dry-run and commit both reported `updated: 7  removed(ZZ): 27  skipped: 0  missing: 0`.

**Audit:** `python -m system_test_ops audit --suite 30284` — **CLEAN**, 174 cases audited (201 − 27
condemned), 0 blocking findings, 24 advisory `title-too-long` (pre-existing across the suite, not
introduced by this change).

**Not touched:** every other TestRail suite; the 27 condemned cases were retitled with a
`ZZ_DELETE_REVIEW -` prefix per this repo's guarded-writer convention (the API cannot hard-delete) —
they remain in TestRail for human review/binning via the UI, not removed from the repo's evidence
trail.
