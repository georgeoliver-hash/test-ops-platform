# HHD terse-rewrite — changelog

Suite **30285** (`**NEW** HHD Test Suite`, project 42, `TFTS - System Test`). Compression pass per
`docs/gherkin-standard.md` § "Terse, not bloated — trust the tester (George, 2026-07-21 — a hard
rule)" — shorten bloated prose to tags, and relocate every citation/date/confirmation-attribution
out of the body text a tester reads and into the case's **Refs** field. This was a compression pass
only: no case's tested behaviour, facts, or values were changed or re-derived.

## Coverage

All **211** live cases in the suite were read and classified (full dump in
`reports/tfts-system-test/new-hhd-test-suite/2026-07-21/cases.json` /
`.../hhd_cases.json` intermediate). Not capped — every case was inspected.

- **Changed: 26**
- **Already clean: 185** — no bloated prose, no embedded citations found; left untouched.
- **Not reached: 0**

## What was changed (by kind)

### 1. CONFLICT-marker compression (4 cases) — Q16/Q17, gap-register
The two known unresolved conflicts each have two cases whose `preface` opened with a bloated,
provenance-heavy marker: `**CONFLICT (audit 2026-07-17)** — <description>. Resolve which is
correct — gap-register Q16.` This both (a) buried the required objective sentence ("This test is
to confirm…") behind the marker, which also tripped the audit's `preface-bad-preamble` rule, and
(b) baked an audit date + an explicit "go resolve this" instruction into body text.

Fix: objective sentence now leads (satisfies the standard's Preface rule and the audit), the
CONFLICT tag trails as a short fragment naming the counterpart case only, and the date +
gap-register pointer moved into **Refs**. The underlying conflict is **not** resolved — both cases
are still flagged, per the task's instruction.

| Case | Before (preface, truncated) | After |
|---|---|---|
| C4103831 | `**CONFLICT (audit 2026-07-17)** — same expired Adult iLink at top-up as C4103883 but opposite outcome. Resolve which is correct — gap-register Q16.\n\nThis test is to confirm a top-up is rejected...` | `This test is to confirm a top-up is rejected when the presented smartcard has expired.\n\n**CONFLICT** — same expired Adult iLink at top-up as C4103883, opposite outcome.` (Refs: `FBD-100261,gap-register Q16`) |
| C4103883 | (mirror of above, Q16) | mirrored, refs `FBD-100261,gap-register Q16` |
| C4103835 | `**CONFLICT (audit 2026-07-17)** — expired-card inspection modelled differently from C4103982. Resolve which is correct — gap-register Q17.\n\nThis test is to confirm...` | `This test is to confirm an inspection tap of an expired card records the correct DeclinedReason in the audit.\n\n**CONFLICT** — expired-card inspection modelled differently from C4103982.` (Refs: `FBD-100658,gap-register Q17`) |
| C4103982 | (mirror of above, Q17) | mirrored, refs `FBD-100716,gap-register Q17` |

### 2. Inline FBD/CR/REQ citation removed from body (already present in Refs) (17 cases)
A worked-example precondition or the expected-result summary carried a bracketed
`(FBD-100336)` / `(FBD-100340)` / `(FBD-100167 printing rule)` etc. citation that duplicated a
reference already sitting in the case's Refs field. These are footnote-style citations, not
data/rule names (a rule-name usage like "under CR78" or "ref.60 cap" was left alone — see the
gherkin standard's ref.60 example). Stripped from the body; nothing added to Refs since the
citation was already there.

Cases: C4103847, C4103848, C4103858, C4103859, C4103861, C4103871, C4103875, C4103876, C4103877,
C4103878, C4103880, C4103933, C4103934.

Example (C4103848):
- Before: `an example Metro Adult Single, 10A (IN) Casement Park to City Hall, £2.30 (fares export FBD-100336)`
- After: `an example Metro Adult Single, 10A (IN) Casement Park to City Hall, £2.30`

### 3. Inline citation missing from Refs — added, then stripped from body (9 cases)
Same pattern as (2), but the citation was **not yet** in Refs, so it was added there first
(never delete a real citation, only relocate it) before stripping the body text.

- **FBD-100690** (Glider TOO live / NIR TOTO future-scope note) — added to Refs and the body
  parenthetical shortened: C4103913, C4103919, C4103921, C4103946.
  - Before (C4103913): `(Glider TOO live; NIR TOTO inspection is future scope, FBD-100690)`
  - After: `(Glider TOO live; NIR TOTO future)`, Refs gains `FBD-100690`.
- **REQ-1630.0** — C4103845: stripped from the expected-result sentence, added to Refs.
- **CR115** — C4103846: stripped from preconditions, added to Refs; also shortened
  `(Deselect if CR115 is not shipped.)` to `(Deselect if not shipped.)`.
- **CR105.3** — C4103966: stripped from expected-result, added to Refs.
- **CR116** — C4103969: stripped from the preface sentence, added to Refs. Left the
  "CR116 expiry-display rule" precondition and "per CR116" expected-result tag alone — rule-name
  usage, not a footnote citation.
- **CR78** — C4103977: stripped from the preface sentence, added to Refs. Left "under CR78" in
  preconditions alone (rule-name usage).

## What was left alone (and why)

The remaining 185 cases were read in full and found already terse: short GIVEN/WHEN/THEN clauses,
no full explanatory sentences, no baked-in dates/attributions/paragraph references. Rule-name style
in-body tags (`ref.60`, `under CR78`, `CR116 expiry-display rule`, "example fare, confirm against
the NIR fares export") were kept — they name a behaviour/config, they don't cite a source
paragraph, so they don't fall under the terse-rule ban (matches the standard's own `ref.60 cap
£7.20` worked example).

## Mechanics

- Rewrite file: `proposals/coherence-audit/fixes/hhd-terse-rewrite.rewrite.json` (26 entries,
  `action: reword`), applied via `tools/apply_rewrite.py` (dry-run then `--commit`).
- `tools/apply_rewrite.py` already passed `refs` through to the writer (added by a prior session
  today) — no code change was needed for this task.
- `TESTRAIL_WRITE_SUITE_ID=30285` set for both the dry-run and commit; writer confirmed every
  touched case's section is in suite 30285 before writing (guarded, suite-locked writer).

## Audit result

First `audit --suite 30285` after the initial commit surfaced **4 blocking `preface-bad-preamble`**
findings — the 4 CONFLICT cases, because the CONFLICT tag was placed *before* the mandatory
"This test is to confirm…" objective sentence. Fixed by reordering (objective leads, CONFLICT tag
trails) and re-applied.

Final `audit --suite 30285`:
```
audited 211 cases: CLEAN; 43 advisory.
```
0 blocking findings. The 43 advisory `title-too-long` items are pre-existing and out of scope for
this pass (title wording untouched).
