# GV suite (30286) — MODE-* direction tagging, 2026-07-27

Mandate: George agreed a new mode-execution tagging scheme for GV's **Direction** dimension (Entry /
Exit / Bi-directional A→B / Bi-directional B→A — a different axis from the other devices' fare/rail
mode, but the same execution mechanism: TestRail Run Configurations). Every case gets a `MODE-*` tag
appended to its **Refs** field so runs can be built as `Shared (MODE-ALL) + direction-specific + the
Primary-only set once`, without re-running direction-irrelevant cases (Technician Menu, HMI screens,
comms) four times over.

## Scope and search

Pulled all **112 cases** fresh via `TestRailClient.get_cases(42, 30286)` (full body incl. `refs`) —
confirmed the suite has grown from 97 → 112 since the 2026-07-24 variant expansion (14 new cases from
that pass, see `gv-variant-expansion.changelog.md`). Cross-checked the section tree and every live
title against `proposals/gv-suite-restructure/structure.md`'s direction-split logic (the "Mode decision"
section) as the starting map, then verified against actual case content rather than inferring from
section names alone.

**1 case excluded from tagging:** C4104038 (`ZZ_DELETE_REVIEW - Barcode — a barcode validated on one
gate head is rejected on another head of the same gateline`) — already flagged for deletion by an
earlier consolidation pass, duplicate of live C4104051. Left untouched, not tagged, per the standard's
"old/flagged cases are not the live suite" convention (same treatment `audit_suite.py` gives
`ZZ_DELETE_REVIEW` cases).

## Classification method

Six tags, grounded directly in `structure.md`'s named direction-specific behaviours (the ABT deny-list
exception and Tap-On/Tap-Off classification — both `FBD-100690`) plus a content read of every other
live case's `Then`/title:

- **`MODE-ALL`** — assigned to any case whose observable outcome touches gate mechanics (opens/stays
  closed/beeps), a per-head-composed audit record, or throughput — i.e. genuinely worth re-confirming
  under each of the 4 configs even though the steps read identically.
- **`MODE-ENTRY-ONLY` / `MODE-EXIT-ONLY` / `MODE-BIDI-AB-ONLY` / `MODE-BIDI-BA-ONLY`** — assigned only
  where the title or `structure.md` names a specific direction. One case (C4104025) carries three of
  these tags at once because `structure.md` names its behaviour "Exit / bi-directional" — see
  `mode-coverage.md` flagged item 3 for the Bi-di-scope caveat.
- **`MODE-PRIMARY-ONLY`** — assigned to Commissioning & Router, Technician Menu, HMI Screen Validation,
  and the comms/device-state half of Non-Functional/Resilience — content that reads identically and
  produces identical outcomes regardless of which physical head/direction runs it.

Full per-case rationale, tally, and 4 flagged judgment calls are in
`proposals/gv-suite-restructure/mode-coverage.md` (new doc, mirrors
`proposals/etm-suite-restructure/mode-coverage.md`'s structure, adapted for the direction axis).

## Applied

Dedicated script `tools/tag_gv_mode.py` (suite-locked via `TestRailWriter`, appends to `refs` only —
never overwrites existing `TIBU-####`/`FBD-#####`/`REQ-####` refs already on a case):

1. `--sample` (dry-run, first 5) — reviewed the diff shape (`'FBD-100690,FBD-100658' ->
   'FBD-100690, FBD-100658, MODE-ENTRY-ONLY'`) before running wider.
2. `--dry-run` (all 111 live cases) — confirmed the full plan, 0 cases left unclassified.
3. `$env:TESTRAIL_WRITE_SUITE_ID="30286"; --commit` — applied to all 111 live cases.

## Tally (post-tagging, re-pulled live)

| Tag | Cases |
|---|---:|
| `MODE-ALL` | 57 |
| `MODE-PRIMARY-ONLY` | 50 |
| `MODE-ENTRY-ONLY` | 2 |
| `MODE-EXIT-ONLY` | 2 |
| `MODE-BIDI-AB-ONLY` | 1 |
| `MODE-BIDI-BA-ONLY` | 1 |

111 of 112 live cases carry a `MODE-*` tag (the 1 excluded is the `ZZ_DELETE_REVIEW` case above); 0
cases left unclassified (verified programmatically — the tagging script warns on any live case id not
covered by its classification map, no warning fired).

## Audit result

`python -m system_test_ops audit --suite 30286` after commit: **CLEAN** — 111 cases audited, 0 blocking
findings across all 13 blocking rules (mojibake, preface/preconds/steps/expected structure,
compound-THEN, stray tags — `has-tags` stayed 0, confirming the new `MODE-*` refs values did not get
written into any case body/title/preface by mistake). 52 `title-too-long` advisories remain, unchanged
from the 2026-07-24 baseline (tagging touched only `refs`, no title/body edits).

## Flagged for engineer review

Recorded in full in `mode-coverage.md`, summarised here:

1. C4104020/4104021/4104022 (ABT reader-disarm conditions) — tagged `MODE-ALL`; arguably closer to a
   `MODE-PRIMARY-ONLY` pure-config check. Flagged, not silently decided either way.
2. C4104091/4104093 (mains-fail gate-stays-open; Emergency Release Button) — tagged `MODE-ALL` per the
   literal "gate open/close" criterion; a case exists for `MODE-PRIMARY-ONLY` instead (same hardware
   response regardless of direction config). `FBD-100348` is still pending integration either way.
3. C4104025's Bi-di scope (both `MODE-BIDI-AB-ONLY` and `MODE-BIDI-BA-ONLY`) — **UNCONFIRMED**, taken on
   the conservative reading that a bi-directional gate is exit-capable in whichever direction is
   currently open. Worth a one-line confirmation when `FBD-100348` integration validation happens.
4. Smoke section's `MODE-ALL` cases (C4104103–4104105) — tagging implies a full 4-config smoke pass;
   noted that day-to-day sanity runs may reasonably use one default config and reserve the 4-way pass
   for release regression (a run-authoring choice, not a tagging one).

## Not touched

- Suite **14973** (old, read-only) — not touched, per the hard rule.
- No case title, preface, preconditions, steps, or expected text was modified — only `refs` was
  appended to, and only with `MODE-*` tokens (existing refs preserved verbatim, just re-joined with
  `", "` separators for consistency).
- `proposals/gv-suite-restructure/structure.md` — read as the starting map per the task brief, not
  edited (it doesn't carry a tally, that lives in the new `mode-coverage.md`).
