# Proposal: restructured Translink POS suite (practice run on the new build)

Goal: take the existing POS suite and reorganise it into a cleaner, optimised new suite — reuse the
good old cases, write new ones for the gaps the UX flow exposed, and handle the three operating
modes without duplication. Read-only/propose-first: this is the blueprint you create in TestRail.

## Operating modes — the decision
- Modes: **NIR · Ulsterbus · Metro**. Most flows identical; only **top-up** differs (sometimes).
- Mechanism (confirmed): **shared cases authored once as `@mode(all)`**, executed against each mode
  via TestRail **Run Configurations** (NIR/Ulsterbus/Metro). Mode-specific cases only where the steps
  genuinely differ (top-up), tagged `@mode(<mode>)`. Single source of truth, no triplication.

## Proposed section tree (derived from the 16 Overflow flows + old suite + test-type-first)
```
GG - POS - Claude Suite                 ← Configurations: NIR (rail) · Ulsterbus · Metro
│
├─ SMOKE                                @mode(all)   thin critical path only
│     sign on → fare look-up → basket → payment → print → sign off
│
├─ FUNCTIONAL
│   ├─ Sign On & Session                @mode(all)   [flow 1.0]
│   ├─ Operator                         @mode(all)   [flow 9.0]
│   ├─ Supervisor                       @mode(all)   [flow 10.0]
│   ├─ Technician                       @mode(all)   [flow 11.0]
│   ├─ Administrator                    @mode(all)   [flow 12.0]
│   ├─ Fare Look-Up (FLU)                            [flows 2.0 Bus / 3.0 Rail]
│   │     Common @mode(all)  +  Bus @mode(Ulsterbus,Metro) / Rail @mode(NIR) where divergent
│   ├─ Basket & Payment                 @mode(all)   [flow 4.0]
│   ├─ Card Payment                     @mode(all)   [flow 5.0]
│   ├─ Numerical Input                  @mode(all)   [flow 6.0]
│   ├─ Top Up & Validation                           [flow 7.0]
│   │     Common @mode(all)  +  NIR / Ulsterbus / Metro subsections where divergent
│   ├─ Issue Card                       @mode(all)   [flow 8.0]
│   ├─ Customer Displays                @mode(all)   [flow 13.0]
│   └─ Barcode Scanning                 @mode(all)   [flow 14.0]
│
├─ NON-FUNCTIONAL / RESILIENCE          @mode(all)
│   ├─ Printer Errors                                [flow 15.0]
│   ├─ Power Interruption & Audio Tones              [flow 16.0]
│   ├─ Comms Lock / loss of CloudFare                [flow 1.0 + TIBU defects]
│   └─ (performance / security-lockout as applicable)
│
└─ REGRESSION
      NOT a parking lot. TIBU defects are folded into the FUNCTIONAL case that owns the
      behaviour (linked via Refs). This area only holds defects with no natural functional
      home. See bug-regression-register.md.
```
Mode handling: `@mode(all)` is the default, run against all three Configurations. Only **Fare Look-Up**
and **Top Up & Validation** carry mode-specific subsections (Bus/Rail and per-mode divergence).

## Governing mindset
All add/edit/merge/fold/leave decisions follow **`docs/test-practices.md`** — risk-based, minimal
sufficient coverage, no duplication, one behaviour per case, traceability via Refs (REQ + TIBU). The
question on every flow path and every old case is the rubric in that doc: *does a test already cover
this — and if so, do we extend it or leave it, rather than add a duplicate?*
4. **Configurations over copies** for modes; **single source of truth** for shared behaviour.

## Suites
- **Source (old, read-only):** `AA-POS Acceptance Test` — never modified or deleted from.
- **Target (new):** `GG - POS - Claude Suite` — everything below is built here.

## Old → new mapping plan  (fill once the TestRail API key is connected)
For each existing case in `AA-POS Acceptance Test`, decide whether/how to **copy it into**
`GG - POS - Claude Suite`. `python -m system_test_ops cases --project translink --suite "AA-POS
Acceptance Test"` produces the inventory; `coverage-analyst` proposes the action. **Nothing is ever
removed from the old suite** — "leave" simply means we don't carry it over.

| Old case (Cxx) | Old title | Action (copy into new) | New section | Notes |
|---|---|---|---|---|
| _TBD_ | _pull from old suite_ | copy-as-is / copy+rewrite / merge / split / leave | 1.x … | |

Actions (all land in the new suite; old is untouched):
- **copy-as-is** — already good and matches the new structure/standard; copy over unchanged.
- **copy+rewrite** — right behaviour, but reword to the standard / fix stale steps as you copy.
- **merge** — duplicate of another case; copy one combined case into new.
- **split** — covers >1 behaviour; copy as multiple cases.
- **leave** — obsolete / always-failing-and-invalid (cross-check with `/review-runs`); don't copy it
  over. It stays in the old suite untouched.

## New cases identified from the UX flow (drafted now)
See `sign-on-cases.md` — 9 Sign On cases, all `@mode(all)`. Of these, the likely **gaps** in the
current suite are the Communication Locked, Device-Locked-after-3, and the two "Unavailable" cases.

## Past-defect / regression coverage
The old suite's `Confirmation Tests` section holds **247 `TIBU` defects** (bug id in the title,
grouped by release 1.1.1 → 2.0.X). See `bug-regression-register.md` for the full list. For the new
suite, each defect must be **pinned by behaviour, not parked in a version bucket**:
- **Fold a regression step** into the functional case that owns the behaviour (preferred), or write a
  dedicated **`@regression`** case where it doesn't fit one.
- **Link the defect via the Refs field** (`TIBU-#####`), not the title — so coverage is queryable.
- Enrich each bug's intent from the **TIBU tracker** (via the Atlassian MCP, if `TIBU` is reachable
  there) before deciding the regression step.
The register's "Functional area" / "New coverage" columns get filled during the build.

## Still gated / inputs needed
- **TestRail API key** → pull existing cases, run the old→new mapping, fill coverage.
- **Documentation/requirements** (you're sourcing) → sharpen "stale vs current" and confirm the
  top-up mode differences so 3.2.2–3.2.4 can be drafted.
- A few **flow-wiring confirmations** for Sign On — see the "Confirm against Overflow" list in
  `knowledge/flows/translink-pos-signon.md`.
