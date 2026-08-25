# HHD suite (30285) — MODE-* tagging, 2026-07-27

Mandate: George agreed a mode-execution tagging scheme for HHD's **NIR-Rail / Glider** operating-mode
axis (the same execution mechanism as ETM/GV — TestRail Run Configurations). Every classifiable case
gets a `MODE-*` tag appended to its **Refs** field so runs can be built as
`Shared (MODE-BOTH) + mode-specific cases for that Configuration`, plus the `MODE-PRIMARY-ONLY` set
run once, without re-running mode-irrelevant cases (Sign On, Supervisor, Technician, M020 pairing
mechanics, Non-Functional) twice over.

## Scope and search

Pulled all **338 live cases** fresh via `TestRailClient.get_cases(42, 30285)` (full body incl. `refs`).
Cross-checked the section tree and every live case's title/content against
`proposals/hhd-suite-restructure/structure.md`'s "Mode decision" (the six proven NIR/Glider
divergences) and `old-suite-audit.md` §4's shared-vs-mode cross-tab, then verified against actual case
content rather than inferring from section names alone.

**3 cases excluded from tagging** — flagged `ZZ_DELETE_REVIEW` by an earlier consolidation pass, not
part of the live suite: C4103831 (Top-Up on expired card), C4103977 (Smartcard Inspection in break
mode), C4103995 (Printer NFC pairing). Left untouched, not tagged, per the standard convention
(`audit_suite.py`'s treatment of `ZZ_DELETE_REVIEW` cases; same rule the GV pass applied).

The remaining **335 cases** all appear exactly once in the classification map (`tools/hhd_mode_tags.py`,
self-checked for duplicates: `NIR_ONLY=34 GLIDER_ONLY=72 PRIMARY_ONLY=83 BOTH=146 TOTAL=335, duplicates: []`).

## Classification method

Four tags, grounded in `structure.md`'s six named proven divergences plus a content read of every
other live case's title/Then:

- **`MODE-BOTH`** — shared case where the outcome could plausibly differ by mode (fare/ticket/product/
  entitlement/config-driven), even if the steps read identically. Includes the whole Smartcard
  Inspection section, generic Sales/Top-Up/Smartcard-validation cases, Smoke.
- **`MODE-NIRRAIL-ONLY`** — one of the three proven NIR divergences: Cross-Border tickets,
  Card-payment reference-number stations, Single-Use Barcodes (CR094, whole section — Glider HHD does
  not do single-use, FBD-100483).
- **`MODE-GLIDER-ONLY`** — one of the three proven Glider divergences: Metro/Ulsterbus product family
  (Multi-Journey/Daylink/Travelcard/Town Service), Old Barcode Redemption (BRS), cEMV Revenue
  Inspection (whole section — Glider TOO live now; NIR TOTO is `@future` per FBD-100690, not authored).
- **`MODE-PRIMARY-ONLY`** — shared AND genuinely mode-irrelevant: the whole Card Payment (M020)
  section (pairing/TID-TK/scheme mechanics), Sign On & Session generic mechanics, Supervisor,
  Technician, Operator menu/UI, one Penalty RBAC-only case, one Smartcards device-capability-limitation
  case, Ticket Formats waybill-reconciliation mechanic, the whole Non-Functional/Resilience area.

Full per-section rationale and the complete tally are in `proposals/hhd-suite-restructure/mode-coverage.md`
(new doc, mirrors `proposals/etm-suite-restructure/mode-coverage.md`'s structure, adapted for the
NIR-Rail/Glider axis, cross-referenced against the GV precedent's direction-axis doc for format).

## Applied

Dedicated scripts (suite-locked via `TestRailWriter`, appends to `refs` only — never overwrites
existing `TIBU-####`/`FBD-#####`/`REQ-####` refs already on a case): `tools/hhd_mode_tags.py` (the id
→ tag map) + `tools/apply_hhd_mode_tags.py` (the writer):

1. `--sample 5` (dry-run) — reviewed the diff shape (e.g. `'FBD-100383,gap-register Q37' ->
   'FBD-100383,gap-register Q37,MODE-NIRRAIL-ONLY'`) before running wider.
2. Full dry-run (all 335 mapped cases) — confirmed the full plan, 0 cases left unclassified, 0
   duplicates, tally matched the map's own counts exactly.
3. `$env:TESTRAIL_WRITE_SUITE_ID="30285"; --commit` — **first pass** wrote 256 cases then hit a
   TestRail `400: "Field :refs is too long (250 characters at most)."` rejection on C4103971 and
   aborted (the script's original form had no per-case error handling).
4. **Hardened `apply_hhd_mode_tags.py`** to catch a `TestRailWriteError` (or a would-overflow check
   computed up front) per case, print a `SKIP` line, and continue instead of aborting the whole run —
   so one bad case can no longer block the rest.
5. **Second pass, `--commit`** — the 256 already-tagged cases were idempotent no-ops (`append_ref`
   detects the tag already present); wrote the remaining **66** cases; flagged **13** as overflow
   (see below). Final: **322 written, 13 flagged/not-written, 0 errors on any other case.**

## Tally (post-tagging, re-pulled live)

| Tag | Cases |
|---|---:|
| `MODE-BOTH` | 133 (146 classified; 13 not written — see overflow below) |
| `MODE-PRIMARY-ONLY` | 83 |
| `MODE-GLIDER-ONLY` | 72 |
| `MODE-NIRRAIL-ONLY` | 34 |
| **Written total** | **322** |

322 of 335 classifiable live cases carry a `MODE-*` tag; 3 `ZZ_DELETE_REVIEW` cases correctly
excluded; 13 flagged (below), classified but not yet written due to a TestRail field-length limit —
not silently dropped, not silently forced through by editing existing citations.

## Flagged — TestRail `refs` 250-char field limit (13 cases, not written)

13 Smartcard Inspection cases share a long existing citation
(`Smartcard Use Matrix; HHD Inspection & Validation Design Note (NIR Inspection + Validation),REQ-...`,
already 245 characters) that leaves only 5 characters of headroom — too little for `,MODE-BOTH` (10
chars). TestRail's `update_case` API rejects any `refs` value over 250 characters.

**Not resolved unilaterally** — shortening the existing citation text would be an edit to an *existing*
reference, not an append, which is outside this task's append-only mandate and this repo's
no-invented-changes rule. Routed to engineer review instead (see `mode-coverage.md`'s "TestRail refs
250-char limit" section for the three proposed resolution options: shorten the shared doc-name
citation, relocate the long reference out of `refs` into the case preface, or accept the whole-section
`MODE-BOTH` classification by convention via `hhd_mode_tags.py` without a live `refs` token for these
13 specifically).

Affected: C4103971, C4104773, C4104774, C4104775, C4104776, C4104777, C4104778, C4104779, C4104780,
C4104781, C4104782, C4104783, C4104784 — all Smartcard Inspection, all classified `MODE-BOTH`.

## Audit result

`python -m system_test_ops audit --suite 30285` after commit: **CLEAN** — 335 cases audited, 0
blocking findings across all rules (mojibake, preface/preconds/steps/expected structure,
compound-THEN, stray tags — `has-tags` stayed 0, confirming the `MODE-*` refs values did not leak into
any case body/title/preface). 102 `title-too-long` advisories remain, matching the pre-existing
baseline (tagging touched only `refs`, no title/body edits).

## Not touched

- Old suites **5446, 13958, 5608, 5505** (read-only) — not touched, per the hard rule.
- No case title, preface, preconditions, steps, or expected text was modified — only `refs` was
  appended to, and only with `MODE-*` tokens (existing refs preserved verbatim, joined with `,`, no
  spaces added, consistent with the existing compact style already used in this suite's refs values).
- `proposals/hhd-suite-restructure/structure.md` and `old-suite-audit.md` — read as the starting maps,
  not edited (tally lives in the new `mode-coverage.md`).
- The 13 refs-overflow cases' existing citation text — left exactly as-is pending engineer decision.
