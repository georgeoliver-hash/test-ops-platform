# ABT blank-steps fix — 51 cases with empty step content/expected

Suite 30279 (`**NEW** BOS & ABT Suite`, project 42). Fixed and re-applied via
`tools/apply_rewrite.py proposals/spec-grounded/abt/admin.rewrite.json
proposals/spec-grounded/abt/backoffice.rewrite.json
proposals/spec-grounded/abt/cloudfare-config.rewrite.json
proposals/spec-grounded/abt/correction.rewrite.json --commit` on 2026-07-21.

## Root cause

On 2026-07-17, `proposals/spec-grounded/abt/admin.rewrite.json` (51 cases across 9 sections:
Sign On & Access, Sign On & Account, Settings, Administrator Settings, Staff Manager, Ticket Editor,
Drawing Tool, Labeling & Publishing, Administration) was partially pushed live despite its own
changelog claiming "proposal only — nothing pushed." Title, `custom_preface`, `custom_preconds` and
`custom_expected` were written correctly. But **every step row came out with `content: ""` and
`expected: ""`** — because `admin.rewrite.json` writes each step as `{"when": "...", "then": [...]}`
while `tools/apply_rewrite.py` (and TestRail's real `custom_steps_seperated` field) expected
`{"content": "...", "expected": "..."}`. `.get("content","")` / `.get("expected","")` silently
returned empty strings for the mismatched keys instead of raising, so the push completed
"successfully" while writing 51 cases' worth of blank step tables.

The four sibling files named in the original diagnosis as possibly affected
(`backoffice.rewrite.json`, `cloudfare-config.rewrite.json`, `correction.rewrite.json`, plus
`capping.rewrite.json` and `reports.rewrite.json` which were also checked) all **already use the
correct `{"content","expected"}` schema** — confirmed by grepping every file in
`proposals/spec-grounded/abt/` for `"when":` as a JSON key: it appears **only** in
`admin.rewrite.json`. So the schema-mismatch bug itself was isolated to that one file.

### Mojibake — re-investigated, found NOT to be a real data bug

The task brief also flagged apparent mojibake (`�`) in several of the 51 titles. Direct
byte/codepoint inspection of the live TestRail titles (e.g. C4103093 "Merit — edit period...")
showed the character in question is a correctly-encoded UTF-8 **U+2014 em-dash**, not corrupted
data — `�` was only how PowerShell's cp1252 console rendered it on screen. A suite-wide scan of all
496 live case titles for `â€` byte-sequences or literal `�` codepoints found **zero** real mojibake
cases. No mojibake fix was needed or applied; this is recorded here so it isn't re-investigated
under a false premise later.

## Scope re-verified live (2026-07-21, before any change)

Ran the confirmed scan against suite 30279 (496 cases total, 391 audited by the conformance tool):
**51 cases had blank step content, exactly matching the previously-diagnosed list, all 51 sourced
from `admin.rewrite.json`** (id-for-id match against `json.load(admin.rewrite.json)`'s case list).
Zero additional blank-step cases were found anywhere else in the suite. Separately confirmed **0**
cases from `backoffice.rewrite.json` (41), `cloudfare-config.rewrite.json` (49),
`correction.rewrite.json` (47), `reports.rewrite.json` (99) or `capping.rewrite.json` (54) had blank
steps, live, before this fix.

### Affected case ids, by source file

- **`admin.rewrite.json` — all 51 of its cases, 100% of the file:**
  4102856, 4102857, 4102858 (Sign On & Access — sign on/off, claims-based access);
  4102927, 4102928, 4102929, 4102930 (Sign On & Account — Passenger Portal);
  4102960, 4102961, 4102962 (Sign On & Access — CloudFare sign on/off);
  4102965, 4102966, 4102967, 4102968, 4102969, 4102970, 4102971, 4102972 (Settings);
  4102878, 4102879, 4102880, 4102881, 4102882 (Administrator Settings);
  4103044, 4103045, 4103046, 4103047 (Staff Manager);
  4103080, 4103081, 4103082, 4103083, 4103084, 4103085, 4103086, 4103087 (Ticket Editor);
  4102981, 4102982, 4102983, 4102984, 4102985 (Drawing Tool);
  4103011, 4103012, 4103013, 4103014 (Labeling & Publishing);
  4103093, 4103094, 4103095, 4103096, 4103097, 4103098, 4103099 (Administration/Merit).
- **`backoffice.rewrite.json`, `cloudfare-config.rewrite.json`, `correction.rewrite.json` — none
  affected** (already used the correct schema; verified 0 blank live both before and after).

## Tool fix: `tools/apply_rewrite.py`

1. **Added `normalize_step()`** — accepts either the native `{"content","expected"}` step shape or
   the `{"when","then"}` shorthand `admin.rewrite.json` used, and normalises both into
   `{"content","expected"}` before building the push payload:
   - `content` = the `when` text, prefixed `"**WHEN** "` — unless it already starts with
     `**WHEN**`/`**THEN**`/`**AND**` (checked per-file: none of the source files' `when`/`then` text
     had inline markers, so every entry got the prefix added; the check exists to make the function
     safe against files that do already inline markers, matching how `capping.rewrite.json` and
     others already write `content`/`expected`).
   - `expected` = `"**THEN** " + then[0]`, then `"\n**AND** " + then[i]` for each subsequent item in
     the `then` list — same no-double-marker guard.
2. **Added a hard validation guard**: after building `custom_steps_seperated`, every step's
   `content` and `expected` must be non-empty (post-normalisation, post-strip). If any step fails
   this, the case is **refused** — printed to stderr as `REFUSED C<id>: blank content/expected in
   step(s) [...]` — and **not pushed**, instead of silently writing blanks. This is the direct
   defence against a repeat of this exact bug class for any future schema drift.
3. Dry-run tested first against three representative cases (4102856, 4102961, 4103087) via
   `normalize_step()` directly, confirming correct marker placement, no double-marking, and correct
   handling of a `then` entry that already carries a `**GAP**` marker (4102961 →
   `**THEN** **GAP** — outcome undefined: ...`).

## Applied

`tools/apply_rewrite.py admin.rewrite.json backoffice.rewrite.json cloudfare-config.rewrite.json
correction.rewrite.json` — dry-run first: `updated: 188 removed(ZZ): 0 fare-reframed: 0 skipped: 0
missing: 0` (188 = 51 + 41 + 49 + 47, matching all four files' full case counts, zero refused, zero
missing). Then `--commit`: identical counts, `updated: 188`, 0 refused.

## Verification

- Re-ran the blank-step scan live after commit: **0** cases with blank `content`/`expected`
  anywhere in suite 30279 (was 51).
- Spot-checked `custom_steps_seperated` content on 10 cases across all 4 pushed files after commit
  (4103093, 4102961, 4103087, 4102982, 4102927 from `admin.rewrite.json`; 4103031, 4103032 from
  `backoffice.rewrite.json`; 4102976, 4102977 from `cloudfare-config.rewrite.json`; 4102816, 4102817
  from `correction.rewrite.json`) — all non-empty, correctly Gherkin-marked, matching the source
  proposal wording, no double `**WHEN**`/`**THEN**` markers, existing `**UNCONFIRMED**`/`**GAP**`
  markers preserved intact.
- No case is worse off: `backoffice`/`cloudfare-config`/`correction` cases were already correct
  before this run and are unchanged in kind (re-pushed idempotently with the same content).

### Audit before/after (suite 30279, `python -m system_test_ops audit --suite 30279 --no-gate`)

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before (2026-07-17 baseline report, `reports/tfts-system-test/new-bos-abt-suite/2026-07-17/`) | 391 | **282** | 232 |
| After (2026-07-21, this fix, `reports/tfts-system-test/new-bos-abt-suite/2026-07-21/`) | 391 | **89** | 208 |

Blocking findings dropped by **193** (282 → 89) — a large share of the pre-existing blocking backlog
was in fact caused by this bug (blank steps trip several blocking rules at once: `steps-empty`,
`expected-empty`, `step-no-then`, `step-content-not-when-and`), so fixing it also retires most of
that backlog as a side effect. The remaining 89 blocking findings (mostly `preface-bad-preamble`,
82, and `then-compound-genuine`, 7) are the suite's separate, pre-existing, unrelated backlog and
are explicitly **out of scope** for this fix — left untouched, per the task boundary.

## Grounding

No new behaviour was invented by this fix. Every case's `content`/`expected` text is exactly the
`when`/`then` (or `content`/`expected`) wording already authored and cited in the corresponding
`*.rewrite.json` on 2026-07-17 — each of which traces its own claims to a governing FBD/spec
paragraph (see `admin.gaps.md`, `backoffice.gaps.md`, `cloudfare-config.gaps.md`,
`correction.gaps.md`). This was purely a transport/tooling bug between an already-grounded proposal
and the live suite; no wording was authored or altered as part of this fix beyond adding the
`**WHEN**`/`**THEN**`/`**AND**` Gherkin markers the standard requires.

## Files touched

- `tools/apply_rewrite.py` — added `normalize_step()` ({"when","then"} → {"content","expected"}
  normalisation) and a hard non-empty-step validation guard.
- `proposals/coherence-audit/fixes/abt-blank-steps-fix.changelog.md` (new, this file).
- `proposals/spec-grounded/abt/admin.changelog.md` — status line corrected (was "nothing pushed";
  now documents the 2026-07-17 partial push + 2026-07-21 proper fix).
- `proposals/spec-grounded/abt/backoffice.changelog.md`,
  `proposals/spec-grounded/abt/cloudfare-config.changelog.md`,
  `proposals/spec-grounded/abt/correction.changelog.md` — status lines corrected to record that
  these files were never affected by the blank-step bug (correct schema throughout) and were
  properly (re-)pushed 2026-07-21 alongside the admin batch.
- No changes to `capping.rewrite.json`/`reports.rewrite.json` or their changelogs — checked, not
  implicated (already correct schema, 0 blank-step cases found, not part of this push).
