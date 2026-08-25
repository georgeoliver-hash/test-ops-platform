# ETM consolidation audit

Two audits, two different results — this file tracks both.

## 2026-08-05 — pre-flow-map-pass fragmentation check (suite-wide)

Run before `/audit-flows` per the standard order (settle fragmentation first, so the coverage pass
classifies against a stable case set). Verdict: **no action needed.** ETM (suite 30254) already went
through this exact consolidation — see `build-complete.md` (2026-06-08, ~897 → 406 cases) and a later,
explicitly authorized un-merge (2026-07-24, 406 → 516) that intentionally split card-scheme/product/
entitlement variants back into individually-executable cases, per current policy (not a regression).
Re-checked the live baseline (587 cases = 516 live + 71 already `ZZ_DELETE_REVIEW`/`ZZ_DELETE_DUP`)
against the flow/variation lens per functional area — no remaining step-of-one-flow or bare-equivalence
splits found. **Fold-group count: 0.**

Two housekeeping items surfaced (not fragmentation, no action gated on them):
1. The ~32 `FOLD` defect-id Refs proposed in `regression-register.md` were never actually applied to
   live cases (checked: zero of the listed defect ids appear in any case's `refs` field). Pending —
   see "Refs backfill" below.
2. One stray `ZZ_DELETE_REVIEW` case (C4100570) sits in the live Functional/Smartcards/Validation
   section instead of the `ZZ - To Delete` bin — needs moving with the other 71, George's UI cleanup.

## 2026-08-05 — flow-map coverage pass fragmentation findings

`/audit-flows translink ETM 30254` (all 16 flow-maps) surfaced **2 genuinely fragmented paths** —
distinct from the suite-wide check above, these are cases where a *specific flow-map path* is only
"covered" by several scattered near-duplicate cases, none of which reads as the whole path
end-to-end. Per the `/audit-flows` triage rule, these are deferred — not authored over.

| Flow-map | Path | Scattered case ids | Why fragmented |
|---|---|---|---|
| `translink-etm-barcode-scanning.md` | #1 — Happy path: scan → validate → ticket valid → print → back to FLU | 4100622, 4100628 | Split into scan-to-result (4100622) and issue/print (4100628); neither reads through the full path. |
| `translink-etm-flu-ticket-issue.md` | #9 — Easibus product menu (configurable, per-stage-colour) | 4100555, 4104452, 4104454, 4104456, 4104458, 4104460, 4104462, 4104463, 4100765 | 8 near-identical cases, one per stage colour (Red/Orange/Yellow/Green/White/Buggy/Wheelchair/Other), same templated steps differing only by stage name. None tests the "configurable, appears immediately" behaviour itself. |

**Recommended aggressiveness for a future fold pass on these two:** obvious-only. Both are clean,
low-risk folds (steps-of-one-flow / bare product-variant duplication respectively) — not a suite-wide
re-audit. Human should confirm before executing per `/consolidate`'s own gate.

## Refs backfill (adjacent, not a fold — flag only)
The following live cases are FOLD targets in `regression-register.md` but carry empty `refs: []`:
4100557/4100566 (301107/300367), 4100572 (301058), 4100535 (301934/301566, 301241), 4100583
(301488), and 4100566 (301186, 301263) — full list is `regression-register.md`'s ~32 FOLD rows.
This is traceability debt, not fragmentation — a separate low-risk task if the department wants it.
