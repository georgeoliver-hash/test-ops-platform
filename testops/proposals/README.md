# proposals/

Per-suite working artifacts from building and maintaining each suite. **You don't need to read these
to use the tool** — they're the audit trail and the push specs. If you just want to understand or run
the process, start at the repo `README.md` / `docs/overview.md`.

## What's a *record* (keep, useful) vs *working intermediate* (archived)

Per suite folder (`pos-suite-restructure/`, `etm-suite-restructure/`, `pv-suite-restructure/`,
`bos-abt-suite-restructure/`):

**Records worth reading**
- `structure.md` — the suite's target structure.
- `old-suite-audit.md` — the evidence base the build was grounded in.
- `build-complete.md` — what was built.
- `requirements-additions.cases.yaml` (+ POS `refund.cases.yaml`) — the latest requirement-grounded
  cases pushed to the suite.
- `<area>.cases.yaml` — the canonical per-area push specs (idempotent by title).

**Working intermediates** (superseded scaffolding — kept for history, safe to ignore; moved under
`archive/` where present): `refine-*`, `sweep-*`, `wave2-*`, `_scaffold`, `consolidate-*`, and the
one-off `*-audit.md` working passes.

## Cross-suite reviews
- `translink-requirements-review/` — the requirements ingestion + cross-examination: the **register**
  (all questions/blockers/findings), and per-suite `gaps-*.md` coverage reports.
- `function-granularity-audit.md` — the cross-suite distinct-function vs data-variation audit.
