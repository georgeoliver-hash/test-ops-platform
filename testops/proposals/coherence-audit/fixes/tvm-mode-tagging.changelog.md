# TVM mode-execution tagging — changelog

**Task:** tag every live case in suite 30284 (`**NEW** TVM Test Suite`, project 42) with a `MODE-*`
Refs tag so George can filter TestRail by Refs when building a run — avoiding re-running
mode-irrelevant cases (EMS, cash-hardware, EMV mechanics, generic UI) across every mode's run.
Scope: the **Mode** dimension (NIR-Rail / Ulsterbus / Metro / Glider) only — the **Model**
dimension (Kiosk / Astreo, a hardware variant) is untouched, unchanged from `structure.md`.

**Method.**
1. Pulled suite 30284 fully (`TestRailClient.get_cases(42, 30284)`, 344 cases, full body incl.
   `refs`) and its section tree (`get_sections`).
2. Read `proposals/tvm-suite-restructure/structure.md` for the documented model/mode split (the
   4 proven divergences), then verified it against the **live** section content — all 5
   `*.cases.yaml` authoring files (sales-tickets, payments, commissioning-ems-nonfunctional,
   smartcards-barcode, smoke) plus a full title+preconditions+steps dump of every live (non-
   `ZZ_DELETE_REVIEW`) case, grouped by section.
3. Classified every case into one of the 4 requested tags, grounded in actual case content — not
   inferred from section name alone (e.g. two "Configuration Topology"/"Commissioning" cases whose
   *section* is generically Commissioning/EMS were tagged `MODE-ALL` because their content is
   literally about a mode-relevant fares-triangle/product-catalogue, while the other ~28 cases in
   the same sections are pure deployment/maintenance mechanics → `MODE-PRIMARY-ONLY`).
4. Built `tools/tag_tvm_modes.py` — a rule-based classifier (section-path defaults + title-substring
   overrides for the exceptions found in step 3) plus a suite-locked writer using
   `TestRailWriter.update_case_fields` to **append** the tag to each case's existing `Refs` (never
   overwrite). Dry-run on a 5-case sample, then a full dry-run over all 317 live cases (`ZZ_DELETE_
   REVIEW` cases excluded — see "Excluded" below), reviewed the classification output, then
   `--commit`.
5. Re-ran `python -m system_test_ops audit --suite 30284` — **CLEAN**.

**Suite:** `**NEW** TVM Test Suite` (30284), project 42.
```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python tools/tag_tvm_modes.py --sample 5      # dry-run sanity
python tools/tag_tvm_modes.py                 # full dry-run (no writes)
python tools/tag_tvm_modes.py --commit        # applied
python -m system_test_ops audit --suite 30284 # re-audit
```

---

## Tally

| Tag | Cases |
|---|---:|
| `MODE-PRIMARY-ONLY` | 204 |
| `MODE-ALL` | 80 |
| `MODE-NIRRAIL-ONLY` | 33 |
| `MODE-ULSTERBUS-ONLY` | 0 |
| `MODE-METRO-ONLY` | 0 |
| `MODE-GLIDER-ONLY` | 0 |
| **Tagged** | **317** |
| **Excluded (not tagged)** | **27** — see below |

Full per-area breakdown, rationale and worked examples: `proposals/tvm-suite-restructure/mode-coverage.md`
(new doc, mirrors `proposals/etm-suite-restructure/mode-coverage.md`'s structure/spirit).

## Excluded — 27 `ZZ_DELETE_REVIEW` cases, not tagged

Found while grouping cases by section: **Smartcards & ABT** (21 cases) and **Mini Statement** (5
cases) live entirely under a top-level **`Delete`** section, every case titled
`ZZ_DELETE_REVIEW - ...`; a 27th (`Screensaver Wake-Up — a smartcard starts the smartcard flow`) is
similarly titled inside `Resilience`. No live (non-`ZZ_DELETE_REVIEW`) equivalent exists anywhere
else in suite 30284 — this coverage area currently has **no live cases at all**. These were
**excluded from tagging**: tagging content flagged for imminent deletion would be wasted effort, and
risks looking like live coverage if the deletion is later reversed without re-auditing. Flagged to
George as an independent finding in `mode-coverage.md` ("Flagged finding") — not something this
tagging task fixes, since restructuring/restoring that section is out of scope here.

## Uncertain cases flagged during classification (resolved, noted for review)

None left **unresolved** by the classifier (0 of 317) — every live case matched a section-default or
a title-substring override on the first full run. Judgment calls made during classification that are
less clear-cut than the bulk of the set, listed here for George to sanity-check:

- **Basket (13 cases) → `MODE-ALL`.** The *mechanics* (add/remove/merge/quantity) are themselves
  mode-independent UI logic; tagged `MODE-ALL` because every case's `Then` asserts a **basket total**
  computed from the mode's live fare table — a fare-calc defect could be mode-specific even though
  the steps read identically. If George considers basket mechanics themselves the primary risk (not
  the fare arithmetic), these could be re-tagged `MODE-PRIMARY-ONLY` instead.
- **Grouped Stops (7 cases) → `MODE-ALL`.** The Area-grouping/cheapest-fare mechanism is documented
  as bus-only (one worked example says "bus-only group") — genuinely NOT relevant to NIR-Rail (which
  has its own separate grouped-station case in the Rail leaf, tagged `MODE-NIRRAIL-ONLY`). No
  "all-bus-modes-but-not-rail" tag exists in the 4-tag scheme, so these were tagged `MODE-ALL` (the
  closest fit — re-run under Ulsterbus/Metro/Glider, skip under NIR-Rail) rather than invented a
  5th tag.
- **Barcode Redemption ticket-format cases (8 of 35) → split `MODE-ALL` (6) / `MODE-NIRRAIL-ONLY`
  (2).** All 8 share one worked example ("a Rail Single collected via a Type B booking reference"),
  but only **Cross Border** and **3 Day Select** are genuinely NIR-Rail-only *products* — Single, Day
  Return, Half-fare, yLink, 24+ and Family exist as barcode-redeemable products across other modes
  too, so those 6 were tagged `MODE-ALL` despite the rail-flavoured worked example (the example is
  grounding, not the scope of the behaviour).
- **Two "home-location product catalogue" cases duplicated across Commissioning & Deployment and EMS
  & TMS Maintenance** (`Commissioning — topology makes home-location products sellable` /
  `Configuration Topology — home location sets the selling operator`, and their "changing
  location"/"destination outside triangle" pairs) → `MODE-ALL`, the sole exceptions in their
  otherwise-`MODE-PRIMARY-ONLY` sections, because home location's fares triangle is what determines
  which mode's products are sellable.
- **Resilience "Multi-Modal Home" (2 cases)** — split by content, not by section default:
  "selecting Bus shows the Bus home" → `MODE-ALL` (applies across Ulsterbus/Metro/Glider); "selecting
  Rail shows the Rail home" → `MODE-NIRRAIL-ONLY` (Rail only exists under NIR-Rail Kiosk).

None of these are `GAP`/`UNCONFIRMED` per the repo's gap-register rules — they're tagging judgment
calls on already-grounded case content, not missing/unverified facts. Flagged here per this task's
brief rather than opened as gap-register questions.

---

## Verification

- **Re-audit:** `python -m system_test_ops audit --suite 30284` → **CLEAN**, 317 cases audited (the
  27 excluded `ZZ_DELETE_REVIEW` cases are outside the auditor's default active-case count), 0
  blocking findings, 100 advisory `title-too-long` (pre-existing, untouched by this pass — only the
  `Refs` field was written, never `title`).
- **Live re-pull confirms:** 317 cases carry exactly one `MODE-*` tag each (no duplicates, no
  double-application), the 27 `ZZ_DELETE_REVIEW` cases carry none, tallies match the plan exactly
  (204 / 80 / 33 / 0 / 0 / 0).
- **Not touched:** every case's `title`, `preconds`, `steps`, `expected` — only `refs` was written,
  and only by **appending** the tag to whatever was already cited (verified against the pre-tagging
  dump: every existing `FBD-####`/`REQ-####`/`old-suite C####`/regression citation survived intact).
  No other TVM suite (5602, 6160, Kiosk 22270/22272/22273/22274, Astreo 22275/22276/22278/22279) was
  touched — this pass only ever wrote to the guarded `TESTRAIL_WRITE_SUITE_ID=30284` target via
  `TestRailWriter`.

## Files

- `tools/tag_tvm_modes.py` — the classifier + writer script (reusable; re-run after any future
  authoring pass to catch newly-added untagged cases).
- `proposals/tvm-suite-restructure/mode-coverage.md` — the mode-coverage map (new), mirroring
  `proposals/etm-suite-restructure/mode-coverage.md`.
- `proposals/coherence-audit/fixes/tvm-mode-tagging.changelog.md` — this file.
