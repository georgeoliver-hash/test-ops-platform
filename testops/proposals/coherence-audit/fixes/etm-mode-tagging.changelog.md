# ETM mode-execution tagging — changelog

**Suite:** 42 / 30254 (ETM, Translink). **Date:** 2026-07-27 (tagging), verified/closed out 2026-07-28.

## What this pass did

Added a **Refs-based mode-execution tag** — `MODE-BOTH` / `MODE-METRO-ONLY` /
`MODE-ULSTERBUS-ONLY` / `MODE-PRIMARY-ONLY` — to every live (non-`ZZ_DELETE_*`) case in suite 30254,
per the 4-tag scheme agreed with George. Full scheme, per-area reasoning, and the flagged-uncertain
list live in `proposals/etm-suite-restructure/mode-coverage.md` (rewritten 2026-07-27 to match this
pass); this file is the changelog/audit trail for the write itself.

**Re-derivation, not reuse of stale docs.** The classification was re-derived fresh against live
suite content (`TestRailClient.get_cases(42, 30254)`, full case body including steps/preconditions),
because the 2026-07-24 variant-expansion pass had taken the suite from 456 → 516 live cases (61 new
cases from splitting "Data variations" lists into individual cases —
`proposals/coherence-audit/fixes/etm-variant-expansion.changelog.md`), which would have made the
pre-expansion mode-coverage doc's case lists stale.

## Mechanism

Tags were appended to each case's existing **Refs** field via `TestRailWriter.update_case_fields`
(e.g. a case citing `FBD-100662` now reads `FBD-100662,MODE-BOTH`), never overwriting existing
citations. `TESTRAIL_WRITE_SUITE_ID=30254` was set for every write; suite 4943 (old, read-only) was
not touched.

**250-character Refs limit:** checked on every case post-write. Max observed Refs length across all
516 live cases is **104 characters** — no case came close to the 250-char cap, so no abbreviation of
existing citation text was needed for this pass (unlike some sibling device passes where it was).

## Result (verified 2026-07-28 against live TestRail data)

Pulled suite 30254 fresh (`get_cases(42, 30254)`, 587 total cases returned) and tallied `MODE-*`
occurrences in `refs`:

| Tag | Count |
|---|---|
| `MODE-PRIMARY-ONLY` | 294 |
| `MODE-BOTH` | 183 |
| `MODE-ULSTERBUS-ONLY` | 25 |
| `MODE-METRO-ONLY` | 14 |
| **Tagged total** | **516** |
| Untagged | 71 (all `ZZ_DELETE_*` — out of scope by design) |

All 71 untagged cases were confirmed to be `ZZ_DELETE_REVIEW` / `ZZ_DELETE_DUP` titles (retired,
excluded from the tagging scope). Zero live cases were found untagged.

Mode-specific cases (`METRO-ONLY` + `ULSTERBUS-ONLY`) = 39 of 516 (~7.6%), consistent with ETM's
"two near-identical bus modes" profile vs POS's heavier 3-mode divergence.

## Audit

`python -m system_test_ops audit --suite 30254`:

```
        0  mojibake
        8  title-no-emdash (advisory)
       69  title-too-long (advisory)
        0  preface-empty / preconds-empty / steps-empty / step-*-not-when / then-compound-genuine / expected-*
        0  has-tags
  audited 516 cases: CLEAN; 77 advisory.
```

**CLEAN of blocking findings.** The 77 advisory items are pre-existing title-style notes (title
missing em-dash, or long screen-validation titles that intentionally mirror exact UI screen names —
see `docs/test-practices.md` on the two advisory title checks) and are unrelated to this tagging
pass — no new blocking findings were introduced by adding `MODE-*` refs.

## Flagged uncertain cases

Carried over from `mode-coverage.md` (all defaulted to the conservative `MODE-BOTH` so nothing is
under-tested) — see that doc's "Flagged uncertain cases" section for full detail and case IDs:

1. Ticket Issue — Gateway (`C4104443`) / ME Rugby Day (`C4104449`, `C4104476`) — product-mode
   ownership not in `knowledge/projects/translink.md`; confirm with engineer.
2. Promo Menu — Park & Ride (`C4104474`) — FBD-100377 lists it as a service classification, not
   clearly tied to one mode.
3. ABT Audit both cases (`C4103557`, `C4103558`) — grounded in one mode's worked example each, but
   the audited-field claim reads as generic ABT auditing.
4. EA Bus SmartPass — Pupil / Further Education (`C4102549`, `C4104511`) — Ulsterbus-route worked
   example, but school passes aren't obviously Ulsterbus-only the way EA **Rail** passes are.
5. Ticket Issue — issue a single ticket (Metro Single) (`C4100550`) — **content bug, not a tagging
   uncertainty**: tagged `MODE-METRO-ONLY` by product name, but its Preconditions still carry the
   Ulsterbus route 72b / ref.60 worked example from the 2026-07-24 variant split. Needs an engineer
   fix to the case body independent of the mode tag (which is correct).
6. Smartcards > Transfers family (`C4103553`–`C4103556`) — tagged `MODE-METRO-ONLY` on strong textual
   evidence ("Metro Transfer Zone" / "Metro Multi-Journey card"); confirm no equivalent Ulsterbus
   transfer scheme needs its own coverage.
7. Ticket Issue — printer/power interrupt during print recovers (`C4100557`) — tagged
   `MODE-PRIMARY-ONLY` (recovery mechanism); reasonable alternate read if print-recovery is believed
   to differ by mode.

None of these block the audit or the tagging completeness — they are content-accuracy /
product-ownership questions for the engineer, logged here and in `mode-coverage.md` per the repo's
gap Q&A convention.

## Status

**Complete.** This changelog was the one artifact missing from the 2026-07-27 pass (write cut off by
a connection error before it could be produced) — the underlying TestRail tagging, the
`mode-coverage.md` rewrite, and the audit were already done and are unchanged by this pass. This
2026-07-28 check re-verified live suite state end-to-end (fresh `get_cases` pull, tally, refs-length
check, `audit --suite 30254`) rather than trusting the prior write blind, and confirms all figures in
`mode-coverage.md` match live TestRail exactly.
