---
description: Audit-first INITIAL BUILD of a restructured suite for a device/project (the longest task). Usage: /onboard-suite <project> <device> [old-suite-id] [new-suite-id]
argument-hint: <project> <device> [old-suite-id] [new-suite-id]
---

Build (or rebuild) a clean, consolidated TestRail suite for a device. Arguments: `$ARGUMENTS`
(`$1` = project, `$2` = device, `$3` = old/source suite id, `$4` = new/target suite id).

Act as the **test-lead** agent. This is **audit-first** — read `docs/test-practices.md` and
`docs/new-work-setup.md` first, and do not author a single case until the audit is done.

**Inputs to confirm with the user before building** (per `new-work-setup.md` "What you must provide
first"): the old/source suite, requirements/REQ docs, UX flows + the Overflow flow-data JSON, defect
history, and a device brief. Missing inputs = guessing = a hindered suite — ask for them.

1. **Per-project setup.** `python -m system_test_ops discover-fields --project $1 --sample-case <id>`
   to get the push `defaults:` block (template_id + `custom_devtypes` — these differ per device;
   trust the value mirrored from a real case of THIS device, not option ordinals). Set
   `TESTRAIL_WRITE_SUITE_ID=$4` in `.env`.
2. **Audit (record everything under `proposals/<device>-suite-restructure/`):**
   - `python -m system_test_ops cases --project $1 --suite $3` → inventory the old suite; write
     `old-suite-audit.md` (section tree, counts, scope decisions, what's in/out).
   - `python -m system_test_ops runs --project $1 --suite $3 --last 20` → `run-history-audit.md`
     (always-failing/never-run/flaky + author comments like "for removal"; remember absent-from-runs
     ≠ invalid).
   - Mine the Overflow JSON: `python tools/extract_overflow_annotations.py <json> <out.md>` and (if
     images) `python tools/organise_flow_zips.py --device <device>`.
   - **Cross-tab** the dimension that matters (e.g. product × operating mode) to PROVE shared vs
     specific — never guess. Write `<area>-crosstab.md`.
   - Confirm scope + mode model with the user.
3. **Structure.** Write `structure.md` — test-type-first (Smoke / Functional / Non-Functional /
   Regression) + an `HMI Screen Validation` per-screen section. Apply the **consolidation lens**
   (test-practices "Structure by flow, not by screen"): functional = flow-based, variations as
   data-variation lines, screens validated per-screen in the HMI section.
4. **Build area-by-area.** One `<area>.cases.yaml` per functional area, grounded in the audit + flow
   annotations + real test bodies. `push --commit` each (auto-runs the conformance audit). Fix any
   blocking findings and re-`push --commit --update`. HMI cases can be generated with
   `tools/gen_hmi_cases.py`.
5. **Fold defects** per `/fold-defect` logic; **smoke** = thin critical path.
6. **Definition of done:** `python -m system_test_ops audit --suite $4` is **CLEAN of blocking**.
   Write `build-complete.md` with the final shape + the human's TestRail UI actions (bin the
   `ZZ_DELETE_*` cases via a `ZZ - To Delete` section, set up Run Configurations).

Spec-authoring rules (avoid rework): preface starts "This test is to confirm"; never put two
outcomes on one THEN line (use `**AND**`); never generate `*.cases.yaml` via a PowerShell heredoc or
`Set-Content` (em-dash/quote mangling → duplicate cases) — write specs with the editor or Python with
explicit utf-8. Read-only against the OLD suite; write ONLY to `TESTRAIL_WRITE_SUITE_ID`.
