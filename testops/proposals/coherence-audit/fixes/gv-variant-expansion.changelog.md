# GV suite (30286) — variant expansion, 2026-07-24

Mandate: George's hard rule — **"no test should tell someone to test multiple variants... we should
have a test for each."** Every case with a trailing `Data variations:` line gets expanded into one
separate, individually-executable case per listed variant (the first/primary variant reuses the
original case id, retitled; the rest are new cases in the same section). Mirrors the earlier
Operator-Portal/Passenger-Portal split. See `docs/gherkin-standard.md` and `docs/test-practices.md`
(both updated 2026-07-24, "Structure by flow/risk").

## Scope and search

Pulled all **98 cases** (97 live + 1 pre-existing `ZZ_DELETE_REVIEW`) fresh via
`TestRailClient.get_cases(42, 30286)` (`proposals/coherence-audit/fixes/gv-suite-30286-raw-2026-07-24.json`)
and searched every case's full body (title/preface/preconds/steps/expected) for `Data variation`.

**4 hits, all in the `custom_expected` field** — the suite's established (now-retired) convention of
naming a variant list in the Expected line rather than the title/preconds:

| Case | Variant list |
|---|---|
| C4104011 ABT Tap — card scheme | Visa Debit / Visa Credit / Mastercard Debit / Mastercard Credit |
| C4104018 ABT Tap — declined-check sweep | Declined Reason 1 Expired / 2 Deny List / 3 Declined / 15 BIN List / 20 Passback |
| C4104028 Barcode — product | Adult / Child / 3-Day Select / 1-3 Off Day Return / 24+ / Ylink / Concession / Half Fare / Day Tracker / Unemployed Day Return |
| C4104046 Barcode — 3-Day Select date logic | current date equals Start / an Additional Date / End |

`C4104024` ("ABT Tap — a Maestro card is not accepted at the GV") was checked per the task brief and
confirmed **not** a variant-list case — it is a single negative assertion (Maestro declined, no data
list in its Expected). No other case in the suite carries this pattern (full-body regex sweep, no
other hits beyond the 4 above).

## Family-by-family resolution

**1. C4104011 — card scheme (4 variants → 4 cases, all new work).** No other case in the suite tests
Visa/Mastercard individually (checked: only C4104011 and C4104024, the Maestro-declined negative,
mention either scheme name). All 4 are genuinely new coverage. C4104011 reused as **Visa Debit**
(already its precondition); 3 new cases created for Visa Credit, Mastercard Debit, Mastercard Credit
— identical body, only the card type in the precondition and the title's bracket suffix differ.

**2. C4104018 — declined-check sweep (5 listed reasons → 0 new cases, re-scoped in place).** Applying
the "do we need a new test?" rubric (`test-practices.md` #1: *is the behaviour already exercised by an
existing case? if yes, do not add a test*) found that **4 of the 5** listed Declined Reasons already
have their own dedicated, individually-executable case in the same section: Reason 1 Expired =
C4104014, Reason 2 Deny List = C4104017, Reason 3 Declined = C4104015, Reason 15 BIN List = C4104016.
Only **Reason 20 (Passback)** had no dedicated case — C4104018 was the only place it was exercised, and
only as one line of a data-variation list. Creating 4 more cases here would have duplicated coverage
that already exists elsewhere, which the rubric and `CLAUDE.md`'s "minimal sufficient set" principle
both rule out. **Resolution:** re-scoped/renamed C4104018 in place to be the dedicated Passback (20)
case — same behavioural shape as its siblings, concrete precondition ("re-tapped within the
TMS-configured passback time"), Declined Reason 20 named in Then. No new cases needed; the variant set
is now completely and individually covered across 5 cases (C4104014/15/16/17/18), matching the
original 5-item list with zero duplication.

**3. C4104028 — barcode product (10 variants → 10 cases, 9 new).** No other case in the Multi-Use
Barcode Validation section names an individual product (checked all 20 cases in that section). C4104028
reused as **Adult** (already its precondition, Scheme ID 5720/format 01/mode RAIL 0002 unchanged — this
grounding was already spec-cited on the original case, not re-derived); 9 new cases created for Child,
3-Day Select, 1-3 Off Day Return, 24+, Ylink, Concession, Half Fare, Day Tracker, Unemployed Day Return
— identical body shape, only the product name in the precondition and the title's bracket suffix differ.
(3-Day Select here tests only the general accept-with-green-tick behaviour for that product; its
date-specific validity logic is a distinct behaviour, handled by family 4 below — no overlap.)

**4. C4104046 — 3-Day Select date logic (3 variants → 3 cases, 2 new).** No other case tests this
date-window logic. C4104046 reused as **Start date** (retitled to drop the "start, additional and end"
compound framing since it now proves only one of the three, per the standard's "title needs an 'and',
it's probably two [now three] cases" rule); 2 new cases created for an Additional-Dates-offset date and
the End date — same body shape, only the date condition in the precondition/expected and the title
differ.

## Applied

Pushed via `python -m system_test_ops push --file
proposals/coherence-audit/fixes/gv-variant-expansion.cases.yaml --update` (dry-run first: 4 would-update
+ 14 would-create, 0 errors — then `--commit`) against `TESTRAIL_WRITE_SUITE_ID=30286`.

- **4 cases updated in place** (retitled/re-scoped, same id, no duplication): C4104011, C4104018,
  C4104028, C4104046.
- **14 new cases created**: C4104418–C4104420 (ABT Tap card scheme: Visa Credit, Mastercard Debit,
  Mastercard Credit), C4104421–C4104429 (Barcode product: Child, 3-Day Select, 1-3 Off Day Return,
  24+, Ylink, Concession, Half Fare, Day Tracker, Unemployed Day Return), C4104430–C4104431 (Barcode
  3-Day Select date logic: Additional Date, End date).

## Before / after count

| | Total cases | Live (non-`ZZ_DELETE`) |
|---|---|---|
| Before | 98 | 97 |
| After | 112 | 111 |

Net **+14 cases** (18 rows processed: 4 in-place updates, 14 creates, 0 removals) — matches "one test
per variant" exactly: the 4 families' variant lists totalled 4+5+10+3 = 22 named variants; 5 were
already independently covered pre-expansion (the C4104018 family, folded rather than duplicated) and
1 (Passback) was covered by re-scoping its existing case rather than adding a new one, leaving 22 −
8 pre-existing/reused-in-place = 14 genuinely new cases, with the full 22-variant set now completely
and individually traceable across 18 cases total (4 reused-in-place + 14 new).

## Audit result

`python -m system_test_ops audit --suite 30286` after commit: **CLEAN** — 111 live cases, 0 blocking
findings (mojibake 0, preface/preconds/steps/expected structural checks 0, compound-THEN 0, stray-tags
0). 52 `title-too-long` advisories remain (up from 38 pre-expansion — expected, since bracket-suffixed
variant titles are longer; advisory-only, not gating, consistent with the standard's stance that a
variant qualifier in brackets is a legitimate reason for a longer title).

## Not touched

- Suite **14973** (old, read-only) — not touched, per the hard rule.
- `proposals/gv-suite-restructure/abt-barcode-grounded.cases.yaml` — the original scaffolding draft
  this suite was built from still carries the old compressed `Data variations:` wording verbatim (it
  mirrors what was live before this change). Not updated as part of this task (out of scope — the task
  target was the live TestRail suite); flagged here as a follow-up so a future reader of that draft
  isn't misled into thinking the compressed form is still the standard.
