# PV Acceptance Suite — consolidation-COMPLETENESS audit (30255 vs old suite 10047)

Date: 2026-07-23. Mandate: George's concern that the PV suite's aggressive 1,144→136 consolidation
(the biggest reduction ratio of any suite) may have folded away — not just redundancy, but a
genuinely distinct required scenario. Prior sessions already found one lead: the old suite carries
96 (81 by a stricter EMV/cEMV/ABT title match, see below) EMV/cEMV/ABT-titled cases against ~13-15
covering that area in the new suite; a spot-check of `C4101088` ("cEMV — decline reasons and
route-type enablement") showed its 8 enumerated decline conditions are genuine consolidation — BUT
the old suite's HMI decline-screen list also names **Cancelled, Unknown, Queue Full, and Tap Error**,
which don't appear anywhere in the new suite. This session resolves that lead first, then sweeps the
rest of the old suite family-by-family.

## Method

1. Pulled old suite 10047 fresh in full (`python -m system_test_ops cases --project 42 --suite
   10047` → 1,144 cases) and new suite 30255 fresh in full (136 cases), plus raw case bodies for the
   cases in question via `TestRailClient.get_cases`.
2. Re-read `proposals/pv-suite-restructure/coverage-map.md` (the existing old→new area map) and
   `proposals/coherence-audit/fixes/pv-deep-audit.changelog.md` + its 2026-07-22 addendum as the
   starting map, then verified current live state independently rather than trusting them blind.
3. Resolved the Cancelled/Unknown/Queue Full/Tap Error question (below).
4. Swept the wider EMV/cEMV/ABT family (81 title-matched old cases) and the full HMI section tree
   (52 old cases across the flat list + the three `Screens/...` subsections) for any other instance
   of the same pattern.
5. Re-ran `python -m system_test_ops audit --suite 30255` to confirm the suite stayed CLEAN (no
   changes were made this session — see "Resolution" below for why).

## The Cancelled / Unknown / Queue Full / Tap Error resolution

**Old suite:** `Non-Functional / Human Machine Interface` (a flat, non-`Screens/`-nested section) has
11 cases: `C4099856` EMV-Success, `C4099857` EMV-Failure-Expired, `C4099858` EMV-Failure-Declined,
`C4099859` EMV-Failure-Denylist, `C4099860` EMV-Failure-Passback, `C4099861` **EMV-Failure-Cancelled**,
`C4099862` **EMV-Failure-Unknown**, `C4099863` **EMV-Failure-Queue Full**, `C4099864` **EMV-Failure-
Queue Full-Tap Error**, `C4099865` **ISAM-Failure-Queue Full**, `C4099866` **ISAM-Failure-Queue
Full-Tap Error**. The bolded six are the ones in question.

**Finding: cannot confirm these six ever corresponded to a real, shipped PV screen.** Evidence,
converging from four independent angles:

1. **The old cases carry zero functional content.** All 11 siblings — including the 5 that clearly
   do map to real screens (Success, Expired, Declined, Denylist, Passback) — share one identical
   boilerplate body: *"Given the HHD is displaying the screen described in the title... When
   inspected and compared to the GUI Presentation Layer document... Then it matches."* There is no
   trigger, mechanism, or distinguishing detail anywhere — the title is the only information. So the
   old suite provides no grounding to copy from for the six in question; it only proves the title
   existed as a candidate at some point.
2. **The current UX source doesn't list them.** `knowledge/flows/pv-flow-annotations.md` (the
   Overflow export) catalogues all 27 confirmed Platform Validator screens by number/name — none is
   Cancelled, Unknown, Queue Full, or Tap Error. Its own annotation for the one cEMV decline screen
   that *is* real, `1.3.3 Invalid Card`, names exactly 8 causes (unsupported scheme e.g. AMEX, card
   clash, expired, invalid BIN, AID fail, ODA fail, deny list, negative list) — the same 8 already
   grounding `C4101088` — with no 9th/10th cause matching any of the four missing names.
3. **The old suite's own functional decline tests don't exercise them either.** `Functional / ABT /
   Declined Taps` (`C2681553` Deny List, `C2681554` Negative List, `C2681555` Expired, `C2681556`
   BIN List) is the old suite's real behavioural coverage of decline reasons, and it never tests a
   Cancelled/Unknown/Queue-Full/Tap-Error condition either.
4. **Zero hits in the full local requirements library.** Searched all 352 documents in `REQS_DIR`
   (every `.docx/.xlsx/.pdf/.txt/.csv`, loose files and zips) for the literal terms: **"tap error"
   returns zero hits anywhere**; **"queue full" returns zero hits**; "queue" alone returns 129 hits,
   every one an unrelated back-office/ticket-print concept (the CloudFare **ABT Transaction Queue**,
   the ETM/POS ticket "shopping basket" print queue) — never a card-reader failure screen;
   "cancelled" returns 238 hits, all about transaction annulment or portal-edit cancellation — never
   an EMV tap-cancelled screen state. **"ISAM"** is a real, correctly-spelled term — *ITSO Security
   Application Module*, the smartcard security chip housed in a POST/reader (CONOPS glossary, and
   discussed there in the context of the older Wayfarer 6 ETM's SAM socket) — but it names a
   **hardware component**, not a PV screen state; nothing ties an "ISAM Queue Full"/"ISAM Tap Error"
   condition to the Platform Validator's HMI specifically.
5. **No wider pattern.** Swept all 1,144 old-suite titles for the same vocabulary (Unknown, Cancel*,
   Queue, Timeout, Tap Error) — the only other hit, `C2667023`/`C3275917` "Technician - Navigation -
   Page Timeouts", is unrelated (Technician Menu idle timeouts, already resolved and grounded as
   `C4102181` via gap-register Q32) — confirming this 6-case cluster is an isolated anomaly, not one
   instance of a broader dropped-state pattern elsewhere in the suite.

**Conclusion:** this reads as a stamped-out placeholder set — 11 near-identical titles enumerating a
candidate list of EMV/ISAM outcome names, five of which are confirmed real screens and six of which
were never corroborated by any source (old case content, live UX export, old-suite functional
behaviour, or the requirement library). This is **not** a case of the 1,144→136 consolidation
deleting proven coverage — the six cases had no proven coverage to begin with, even in the old suite.

**Action taken: none to the suite.** Per this repo's no-gap-filling rule
(`docs/gherkin-standard.md`) this is an "unknown *what*" (the existence of the behaviour itself is in
doubt), not an "unknown *how*" — the correct handling is a gap-register question for the engineer,
not adding cases on inference, and not silently dropping the question either. Logged as
**gap-register Q61** (`proposals/coherence-audit/gap-register.md`, new session header). If George
confirms these are real (and can name the trigger/mechanism), the missing screen-validation/
decline-reason coverage will be grounded and added in a follow-up pass. If he confirms they were
never real/are obsolete, this closes as confirmation the consolidation lost nothing.

### Secondary finding surfaced while resolving the above (Q62)

The HMI Screen Validation section of the *new* suite is missing a case for **`1.3.3 Invalid Card`**
itself — the one screen in the Overflow catalogue that *is* confirmed real and that `C4101088`
functionally grounds its 8 decline causes against. Every other catalogued screen has a dedicated
`HMI Screen Validation / Validation Screens` case; this one doesn't. No old-suite case was found to
ground a new one on (`C3207743` "Error Screen - Invalid Card" was checked and is a different screen,
`1.3.2 Card Not Yet Valid`, not `1.3.3`). Logged as **gap-register Q62** rather than authored blind,
since adding a screen-validation case needs the same Overflow screenshot/UI Presentation Layer source
its 26 siblings cite, not invented wording.

## Fuller family-by-family sweep

Beyond the HMI cluster above, re-verified the rest of the old suite's decomposition against the new
suite, refreshing (not just trusting) `proposals/pv-suite-restructure/coverage-map.md`'s 2026-06-08
reconciliation:

- **EMV/cEMV/ABT title sweep (81 old cases matching `emv|cemv|abt` case-insensitive, across
  `Functional/ABT/*`, `Functional/Back Office/FEIG`, the Glider TOO cEMV-enablement tree, and the
  superseded `Delete/*` duplicates of that tree):**
  - `Functional / ABT / Card Presentation` (18 cases: Visa/Mastercard/Visa Credit/Debit/Mastercard
    Credit/Debit/Maestro/Apple Pay/Apple Pay Express/Removed-from-Deny-List/Removed-from-BIN-List/
    Passback/Invalid-Card-Amex/Diners/Non-EMV/Expired-EMV/On-Deny-List/On-BIN-List) — **card-scheme
    variants correctly folded** as the "Variation — Visa, Mastercard, mobile wallet" line in
    `C4100998`; the Amex/Diners/Non-EMV/Expired/Deny/BIN variants correctly folded into `C4101088`'s
    8-cause enumeration (equivalence partitioning, no new test needed per
    `docs/test-practices.md` rubric step 2). **Removed-from-Deny/BIN-List is explicitly still
    tested** — read `C4101079`'s body directly: step 3 is "present a Deny/BIN-listed card, then
    re-present it after it is removed from the list → the listed card is rejected, the removed card
    is accepted" — this is not a silent drop.
  - `Functional / ABT / Deny List` (2), `/ BIN List` (1) — covered by `C4101079` (delta/full updates,
    retries, TIBU-26320/25745 regression pins), confirmed by reading its full body.
  - `Functional / ABT / Pilot List` (3) — covered by `C4101078`/`C4103562`/`C4103563`/`C4103564`,
    confirmed by reading all four bodies (registration mode, enrolled/non-enrolled tap, once-daily
    zip upload — all present).
  - `Functional / ABT / End-to-End` (1), `Functional / Back Office / FEIG` (2) — covered by
    `C4101004`/`C4101081`.
  - Glider TOO cEMV-enablement tree (route/location/fare-check scenarios, transfers, duplicate taps,
    successful taps, passback, Technician-Menu disable — ~20 old cases across the live `Glider/...`
    tree and its superseded `Delete/...` duplicate) — covered by `C4101001`/`C4101002`/`C4101003`/
    `C4101088`, confirmed present as data variations/steps in those bodies.
  - `C4101093` ("cEMV — EMV result screens and transaction generation") explicitly covers EMV
    success/failure/passback screens and their timeout behaviour (pinning TIBU-25700/25702/25704/
    25705) — this is the case that would have hosted Cancelled/Unknown/Queue-Full/Tap-Error *if* they
    were confirmed real; it does not name them, consistent with the Q61 finding above.
  - **No other title in the 81 hides an un-mapped distinct scenario** beyond the HMI six already
    flagged.
- **Full HMI section tree (52 old cases: the flat 11 + `Screens/Validator Screens for Smartcards`
  (20) + `.../for Barcodes` (11) + `.../Technician Menu` (10)):** the three `Screens/...` subsections
  map cleanly 1:1 onto the new suite's 26-case `HMI Screen Validation` catalogue (Idle/Default,
  Not-In-Service, Invalid-Card→Card-Not-Yet-Valid, Error-Reading-Card, Not-Valid-At-Location,
  Invalid-Time-Of-Day, Product-Expired, Not-Accepted, Barcode-Type-Invalid, Re-present-Card, Passback
  variants, Success variants, all Technician Menu screens) — no further gaps found there. The flat
  11-case section (not the `Screens/` tree) is the one anomalous list, isolated to the Q61 finding.
- **Technician Menu / Non-Functional / Comms / smartcard-product families**: not re-audited from
  scratch this session (out of the time budget) — relied on the existing `coverage-map.md`
  reconciliation (781 folded validation-matrix cases, 84 technician/comms/power/DST cases, etc.,
  "zero genuine gaps" as of 2026-06-08) plus the fact that the 2026-07-21/22 deep-audit session
  already cross-examined every live case in the new suite against full spec text and found no
  consolidation-completeness issue outside the EMV/ABT area George had already flagged. No new
  anomaly of the "flat placeholder list with untested candidate names" shape (the pattern that
  produced Q61) was found anywhere else this session's title sweeps touched.

## Result

- **No suite changes made this session.** Both open questions (Q61, Q62) are existence/sourcing
  questions, not resolvable without the engineer or the original UX export, so nothing was added —
  adding either would be gap-filling.
- **Suite 30255 re-audited: CLEAN of blocking findings** (135 cases; 24 pre-existing advisory
  title-length/em-dash notices, unchanged from before this session; 0 new).
- **Old suite 10047: untouched** (read-only throughout, per the hard rule).

## Files

- `proposals/coherence-audit/gap-register.md` — Q61 (Cancelled/Unknown/Queue Full/Tap Error
  existence) and Q62 (missing `1.3.3 Invalid Card` HMI screen-validation case) appended under a new
  "Session 2026-07-23 — PV consolidation-COMPLETENESS audit" header.
- This file.
