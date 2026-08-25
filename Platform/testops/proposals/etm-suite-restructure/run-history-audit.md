# ETM old-suite run-history audit (evidence)

Source: `python -m system_test_ops runs --project 42 --suite 4943 --last 20`
→ `reports/tfts-system-test/aa-etm-acceptance-test/2026-06-05/run-health.{md,json}`.

## What the runs actually are
- Only **6 runs** exist for `AA-ETM-Acceptance Test` (ids 21978, 21742, 21495, 19352, 19087, 19074).
- **959 cases tracked. Only 23 were executed in any of those 6 runs.** The other **936 are
  "orphaned" — i.e. simply not included in these particular runs, NOT invalid.** With only 6 runs
  over a 959-case suite, "orphaned" is a weak signal here; absence of runs ≠ a bad case.
- **Crucial:** all 23 executed cases are **CloudFare / BOS back-office web-admin** tests, not ETM
  device tests — "Verify Dashboard/ABT/Schedule Management/Reports/Settings/Estate/Business
  Intelligence/Menu/Events Screen Contents", "Cloudfare SignOn (Administrator / AD User)",
  "Rules/Products/Tickets Create & Delete", "Staff/Asset Manager", "Route Management – Glider",
  "Activity Log". So the recent runs exercised the **back office**, and the **ETM device cases have
  effectively no run history** to judge stale-vs-good from.

## Genuine signals (not just "orphaned")
- **Flaky (15):** every one is a CloudFare/BOS screen-content or sign-on case (C2082941–950,
  C2092775/793, C2131388, C2132847/848). Their 1–3 failures are back-office-UI churn, not ETM.
- **Recently-regressed (1):** C2092782 "UnSuccessful Cloudfare SignOn – Administrator" — again BOS.
- **always-failing: 0. never-executed: 0** (every case has at least appeared; the metric counts
  presence across all-time, not these 6 runs).

## Author comments / scope markers found in titles
- **Explicitly flagged for removal:** C2442022 / C2442023 / C2442024 —
  `** For Removal? Test is for Bus Validator ** MIFARE … Validation on BV`.
- **Flagged untestable:** C2448294 `EMV hardware and transaction timings (Potentially untestable –
  No performance measure provided)`.
- **BV (Bus Validator) device content in an ETM suite:** C2471577–580 (`8.9 BV Devices` HMI screens),
  C2442032 (`GPS – Travelling Mode on BV`), C2442034/035 (`Time Change … on BV`), C2441561
  (`Other devices – Forced comms on BV Device`), and a large `BV - ETM - …` MJ/Ulsterbus validation
  block (C2602935–C2645091) + `BV to ETM to BOS Communication` (C2645168).

## Scope buckets (full 959 titles)
- **~26 BOS / CloudFare back-office** cases (the only ones with run history). → these belong to a
  **BOS/back-office suite**, not an ETM *device* acceptance suite.
- **~36 BV / BV-ETM** cases. Split: **pure BV device** tests (validation/GPS/time-change *on BV*) →
  BV is its **own device type** (own suite); vs **ETM-manages-BV** (`Other devices – … BV`) which is
  legitimately ETM driver functionality, and the `BV - ETM -` validation block which is ambiguous.
- **~897 ETM-device** cases — the real scope of the new ETM suite.

## Judgement (for the new suite)
1. **Exclude the ~26 BOS/CloudFare back-office cases** — different system; they have a home elsewhere.
   (Don't carry over; old suite untouched.)
2. **Exclude pure-BV device cases**; **keep** ETM "Other devices" management of a BV (ETM is the
   actor). Treat the `BV - ETM -` validation block per George's steer (see decision).
3. **Drop** the 3 `For Removal? … Bus Validator` cases and the untestable EMV-timings case (or keep
   the latter as a documented manual/observational check — George's call).
4. For everything else, **run history gives no keep/kill signal** — base keep/leave on the old-suite
   content audit + UX flows + product×mode cross-tab, not on the (BOS-only) run data.
