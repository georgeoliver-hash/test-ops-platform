# PV mode-execution tagging — changelog

**Suite:** 30255 (`**NEW** PV-Acceptance Test Suite`, project 42, `TFTS - System Test`).
**Applied via:** `tools/tag_pv_modes.py` (dry-run + `--sample` verified first, then `--commit` on
2026-07-27).
**Status: PUSHED to TestRail.**

## Why this session exists

George agreed a new mode-execution tagging scheme for PV so he can filter TestRail cases when
building a run, avoiding re-running mode-irrelevant cases across both PV Configurations (**Glider**,
**Rail**). Four tags, appended to each case's **Refs** field:

- `MODE-BOTH` — shared case, steps identical, but the outcome could plausibly differ by mode
  (fare/product/config-driven behaviour) — run under both Configurations.
- `MODE-GLIDER-ONLY` / `MODE-RAIL-ONLY` — already mode-specific behaviour.
- `MODE-PRIMARY-ONLY` — shared **and** genuinely mode-irrelevant (Technician Menu, most
  Non-Functional, non-fare HMI, comms/hardware) — only needs running once.

## What was done

1. Pulled suite 30255 fully (`TestRailClient.get_cases(42, 30255)`, full case body including
   `refs`) — **185 cases**, 1 pre-existing condemned (`C4101005`, `ZZ_DELETE_REVIEW`, excluded) =
   **184 live cases**.
2. Re-verified the live section tree (21 sections) and read `proposals/pv-suite-restructure/
   coverage-map.md` + `structure.md` as the starting map, per George's note that the suite has grown
   substantially since those docs were written (the 2026-07-27 variant-expansion session alone added
   ~47 cases — card-scheme/product variants, cEMV decline reasons, duplicate-tap cases).
3. **Re-grounded against live case content, not just section names** — read every live case's full
   preface/preconditions/steps/expected (`tools/` scratch dump), because section names alone are an
   unreliable proxy (e.g. the `ABT (Glider)` section is Glider-only, confirmed by every case's own
   precondition text — "a Glider PV..." — and by `knowledge/flows/pv-flow-annotations.md`'s "Glider
   PV only screens" annotation; but the `Rail-specific` section also contains a genuine ABT case,
   confirming ABT/cEMV isn't purely Glider-only in an absolute sense — it's the *specific* cEMV
   decline/enablement mechanics that are Glider-only, while the base ABT Tag-successful outcome has
   its own Rail-suffixed variant).
4. Classified all 184 live cases into the 4 tags (tally below) with a dedicated script
   (`tools/tag_pv_modes.py`), dry-run + 5-case `--sample` spot-check, then a full dry-run (0
   warnings — every live case classified exactly once, no stray ids) before `--commit`.
5. Re-audited: `python -m system_test_ops audit --suite 30255` → **CLEAN — 0 blocking, 47
   advisory** (pre-existing title-style checks, unaffected by this change; up from 24 advisory at the
   last audit because the suite has grown by ~47 cases since then, not because of this change).
6. Wrote `proposals/pv-suite-restructure/mode-coverage.md` (new) with the full per-case rationale,
   mirroring `proposals/etm-suite-restructure/mode-coverage.md`'s structure/spirit — adapted because
   PV's scheme is a Refs-tag-per-case (queryable in TestRail), not ETM's documentation-only map.

## Tally

| Tag | Count |
|---|---|
| `MODE-BOTH` | 60 |
| `MODE-GLIDER-ONLY` | 36 |
| `MODE-RAIL-ONLY` | 12 |
| `MODE-PRIMARY-ONLY` | 76 |
| **Total live cases tagged** | **184** |

(1 condemned case, `C4101005`, left untouched — out of scope, pending George's normal UI bin-cleanup.)

## Flagged uncertain (see `mode-coverage.md` "Flagged uncertain" for full detail)

1. **Barcode family "inferred MODE-BOTH"** (17 cases: 11 multi-use product cases + early-morning
   expiry + 2 Barcode Validation green/red outcomes + 4 Legacy & Card Tech) — tagged by analogy to
   the Smartcard Validation family (fare/product-driven), but none of these cases state "Run under
   Glider and Rail" explicitly the way the smartcard cases do.
2. **Smoke smartcard/barcode cases "inferred MODE-BOTH"** (3) — same reasoning/caveat.
3. **HMI ABT deny-list / error-reading-card / hotlisted-card screens** (3, `C4101038`/`4101039`/
   `4101040`) — tagged `MODE-BOTH` (no Rail-suffixed variant exists, unlike ABT Tag successful), but
   they functionally pair with Glider-only cEMV decline-reason cases; `MODE-GLIDER-ONLY` is a
   plausible alternative.
4. **`PV to BOS — Deny and BIN list download`** (`C4101020`) tagged `MODE-GLIDER-ONLY` (explicit "PV
   has cEMV" precondition) while its sibling `PV to BOS — software and FEIG update via CloudFare TMS`
   (`C4101019`) was kept `MODE-PRIMARY-ONLY` — the split is a judgment call worth confirming with
   George (does a Rail PV carry a FEIG reader at all?).

These 24 cases are worth a second look but were not left unclassified — every live case got a tag so
the filtering scheme is usable immediately; the flags mean "revisit if it turns out wrong," not "not
yet done."

## Not touched

- Old suite `10047` (`AA-Platform Validator Acceptance Test`) — untouched, read-only, as always.
- Every other TestRail suite/project.
- The 1 pre-existing condemned case in 30255 (`C4101005`).
- No case title, preface, preconditions, steps, or expected result was changed — only the Refs field
  was appended to (existing refs preserved, never overwritten).

## Files

- `tools/tag_pv_modes.py` — the applied one-off tagging script (dry-run default, `--sample`,
  `--commit`).
- `proposals/pv-suite-restructure/mode-coverage.md` — new: the mode-tagging scheme + full per-case
  rationale + flagged uncertainties.
- This file.
