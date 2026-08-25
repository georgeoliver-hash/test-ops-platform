# POS Test-Automation Handover Package

## What this is

This package hands over everything George's `automation-tests` repo has learned about the
Translink **POS** device (`com.flowbird.pos`, INF212 way6 Android terminal) to whoever is building
POS coverage in the company's **official `sit` Robot Framework repo**. `sit` currently has **zero**
POS test coverage, so this package exists to transfer two things that *do* survive the move to a
different codebase:

1. **Device research/facts** — hardware, OS, app package shape, provider authorities, EventLog
   schema, dataset parameters, BOS/Keycloak endpoints, the UI-string and screen catalog. See
   `device-facts.md`.
2. **Test intent** — for each of the 26 POS-tagged tests that exist in this repo today: what it
   checks, why, on which feature area, and what evidence source it asserts against. See
   `test-intent.md`. This is the part a `sit`-based engineer should actually re-implement, once
   `sit` has a POS device family / ConfigSet / Bindings layer to hang it off.

## IMPORTANT CAVEAT — the raw `.robot` files will NOT run in `sit`

`raw-repo-export/` is included **for reference and code-reading only** — so you can see exactly how
a given assertion was implemented, what Robot Framework keywords it called, and what the
surrounding resource/framework plumbing looked like. **Do not attempt to run, import, or copy these
`.robot` files directly into `sit` and expect them to work.**

This repo (`automation-tests`) and the official `sit` framework are **two different codebases**
with incompatible foundations:

| | This repo (`automation-tests`) | `sit` (official framework) |
|---|---|---|
| Library layer | Custom `framework/robot/*Library.py` (`DeviceLibrary`, `AndroidLibrary`, `BOSLibrary`, `WinceLibrary`, `BuildDataLibrary`) | `sit`'s own Bindings/Utility layer (different keywords entirely) |
| Device config | `devices.yaml` per project — a bespoke Pydantic-backed registry | `ConfigSet` / `SAM` — no equivalent file format |
| Device abstraction | Bespoke `transport`/`ui`/`android`/`bos` plain-Python layer under `framework/` | Whatever `sit`'s own device-family abstraction is (POS doesn't exist there yet) |
| Test runner conventions | RF tags (`device_types:POS`, `feature:*`, `destructive`) mapped by a project-agnostic listener/report layer | `sit`'s own tagging/reporting conventions |

None of the `Resource`/`Library` imports in `raw-repo-export/*.robot` will resolve inside `sit` —
there is no `framework.robot.android_library.AndroidLibrary` there, no `devices.yaml` loader, no
`DatasetParameters` reader. **Every test will need to be re-authored from scratch against `sit`'s
own Bindings, once `sit` has a POS device family to bind against.** Use `test-intent.md` as the
spec for what to re-author, and `raw-repo-export/` only to check implementation details (exact
keyword sequences, exact string/EventLog names used) when the plain-English description in
`test-intent.md` isn't enough.

## How to use this package

1. Read `device-facts.md` first — it's the ground-truth reference for the device itself (independent
   of any framework). Cite it back to George if anything looks stale; it was pulled from a real
   device/build on the dates noted inline.
2. Read `test-intent.md` — organized by feature folder (transactions, status, printing, signon,
   options, provisioning, flu, pos, display, audit). For each test: what it verifies, why it
   matters, and what evidence source (`EventLog` / on-device audit ledger / UI text / APK version /
   etc.) the real test should assert against once reimplemented in `sit`.
3. Use `reference/` as supporting data:
   - `pos_apk_metadata.json` — the full static APK scan (services, receivers, providers, 1,311 UI
     strings) that `test-intent.md`'s "evidence source" column draws on.
   - `screens.md` — the 109-screen layout catalog (which `@string` keys live on which screen).
   - `dataset_parameters_live.json` — a live-captured sample of the 14 device-behaviour config
     values (`DatasetParameters.json`), used as the expected-value source for build-verification
     assertions.
4. Only dip into `raw-repo-export/` when you need to see exactly how an assertion was implemented
   (e.g. the precise EventLog query, the precise keypad keycode) — never to run it as-is.

## Known gaps / caveats to carry forward

- **BOS audit API is not confirmed.** Every test in this repo asserts via the on-device `EventLog`
  content provider (durable) or the local `Audit/BOSRecords` ledger (ephemeral outbox) — never a
  live BOS round-trip. `BOSClient.get_audit_events` in this repo deliberately raises
  `NotImplementedError`. Don't invent a BOS assertion path that hasn't been confirmed against the
  real BOS API contract.
- **Many tests here are stubs/TODOs, not finished tests.** A large fraction `Skip` with an
  explanation (e.g. "needs a precondition we don't have a way to seed yet") rather than asserting
  anything. `test-intent.md` calls this out per-test — treat those as **documented intent**, not
  proof the behaviour was ever verified end-to-end on a live device.
- **One test has a known false-pass risk**: `Successful Signon Emits State Changed`
  (`signon/test_operator_signon.robot`) — the platform's periodic NTP `state.changed` event can
  satisfy the assertion without a genuine sign-on having happened. Flagged inline in
  `resources/translink/signon.resource` and repeated in `test-intent.md`.
- **Destructive tests are marked and excluded by default.** `Invalid Signon Shows Failure Dialog`
  is tagged `destructive` because repeated bad credentials trip a Fatal Error lockout on the real
  POS requiring a manual power cycle. Preserve this pattern in `sit` — mark any lockout-risk POS
  test so it's opt-in, not part of the default run.
- **Live device details** (as of the date this repo last touched real hardware): build
  `1.0.572.20749` (package `pos.STE11`), INF212 way6 / Android 5.1.1, POS provisioned in **NIR
  (Rail) mode** — Bus/Ulsterbus FLU screens are not reachable from standard sign-on on this specific
  unit, so those tests skip gracefully rather than fail. If the `sit` team's POS unit is provisioned
  differently (e.g. Ulsterbus/Metro mode), the Bus FLU tests become exercisable and the NIR-only
  main-screen test's expectations would need reviewing.
