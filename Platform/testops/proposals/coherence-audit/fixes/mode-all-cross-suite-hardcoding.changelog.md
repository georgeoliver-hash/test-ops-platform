# `MODE-ALL` cases hard-coding one variant — cross-suite sweep (2026-08-03)

**Trigger.** George flagged live testers marking ETM cases Invalid because a `MODE-ALL` case's
precondition named a specific operator/route that didn't match the Configuration being run (e.g.
"signed on to **Ulsterbus** route 72b" while executing the **Metro** run of plan `ETM - OS
v8.0.6356`). Confirmed via TestRail run results (`get_results_for_run`) that several case ids were
independently marked Invalid in *both* the Metro and Ulsterbus runs of that plan — the fingerprint of
a shared case that can never be right under at least one Configuration.

**New standing rule** (added to `docs/gherkin-standard.md`, "Concrete grounding" section): a
`MODE-ALL` case must never hard-code a single variant's name in its precondition. Generic wording only
("a valid route", "an Adult Single at its configured fare"). `MODE-<VARIANT>-ONLY` cases keep concrete,
cited worked examples as before — that rule is unchanged.

**Scope checked:** all `MODE-ALL`-tagged cases across ETM (183), POS (46), TVM (80), HHD (146), GV
(57).

| Suite | MODE-ALL cases | Hardcoded-variant hits | Fixed | Flagged (needs George) |
|---|---:|---:|---:|---:|
| ETM (30254) | 183 | 62 | 62 | 0 |
| POS (30253) | 46 | 5 | 5 | 0 |
| TVM (30284) | 80 | 31 | 27 | 4 (`C4103686`, `C4104859`, `C4104860`, `C4104866` — see gap-register Q35/Q36) |
| HHD (30285) | 146 | 0 | — | — |
| GV (30286) | 57 | 0 (1 false-positive match on the word "entry" in a lane-reader description, not a mode name) | — | — |

**ETM detail:** `proposals/etm-suite-restructure/mode-all-route-hardcoding.changelog.md` (full case
list, 62 ids).

**POS fix (5 cases):** `Ulsterbus route 10A` → `a valid route` in `C4099989`, `C4099990`, `C4099991`,
`C4100432`, `C4100433` (all Basket-family cases). Mechanically identical to the ETM fix.

**TVM fix (27 of 31 cases):** every hit used "Metro" as the example operator for a product confirmed
shared in `knowledge/projects/translink.md` (Adult Single, Child Single, Family & Friends, Popular
shortcut, Day/Day Return) or for device-commissioning language where the mode is irrelevant
(Kiosk/Astreo boot, screensaver, generic Single Adult ticket sale). Fixed: `C4103680`, `C4103681`,
`C4103682`, `C4103683`, `C4103685`, `C4103687`, `C4103691`, `C4104847`, `C4104848`, `C4104849`,
`C4104850`, `C4104851`, `C4104852`, `C4104853`, `C4104854`, `C4104857`, `C4104858`, `C4104865`,
`C4103704`, `C4103705`, `C4103706`, `C4103707`, `C4103708`, `C4103673`, `C4103674`, `C4103675`,
`C4103676`.

**TVM NOT fixed (4 cases) — logged as `gap-register.md` Q35/Q36 instead of guessed:**
- `C4104866` ("1 Month Return") — worded "Metro," but `knowledge/projects/translink.md` states Month
  Return is **Ulsterbus-only**. Direct contradiction; could mean the case is mistagged `MODE-ALL` when
  it should be `MODE-ULSTERBUS-ONLY`, or the knowledge note is stale. Needs George's call, not a guess.
- `C4103686`, `C4104859`, `C4104860` ("Evening ticket", 3 payment-method variants) — worded "Metro,"
  and unlike Month Return there is **no existing record at all** of which mode(s) actually sell an
  Evening ticket. Left as-is rather than asserting shared-ness with zero source.

**Re-audit after the 27+5 (ETM 62 included) fixes:**
- ETM (30254): CLEAN, 516 cases, 0 blocking.
- POS (30253): CLEAN, 601 cases, 0 blocking.
- TVM (30284): CLEAN, 317 cases, 0 blocking.

**Follow-up sweep (2026-08-03, same day): PV and GV, and a re-check of HHD.** The first pass's HHD/GV
scan used a narrow keyword regex and PV was omitted entirely. Redone properly:

| Suite | MODE-ALL cases | Hardcoded hit | Fixed | Flagged |
|---|---:|---:|---:|---:|
| PV (30255) | 60 | 6 | 6 | 0 |
| HHD (30285) | 146 | 22 | 16 | 6 (gap-register Q37) |
| GV (30286) | 57 | 51 (false positives) | 0 | 0 |

- **PV (6 fixed):** iLink Zone 1-4/NW + Belfast Visitor Pass validation cases said "a **Rail** PV"
  while their own Expected field says "Run for Adult and Child, under Glider and Rail" — a direct
  self-contradiction. Fixed `a Rail PV` → `a PV`. Re-audit clean (185/0).
- **GV (0 fixed — confirmed clean):** GV's `MODE-ALL` dimension is gate **direction**
  (Entry/Exit/Bidi), not operator/fare mode. Every "NIR" hit is accurate — GVs only ever run in an
  NIR/rail context, so there's no wrong "other mode" to contradict. Not the same bug class.
- **HHD (16 fixed, 6 flagged):** same pattern as ETM/POS/TVM — "Metro" hardcoded for confirmed-shared
  products (Adult/Child Single, Basket, Multi-Journey Top-Up) or "the NIR fares export" cited as the
  sole check source for a case meant to run under both NIR-Rail and Glider. Fixed the same way. 6
  cases NOT touched — see `gap-register.md` Q37: each names one mode inside an explicit "worked
  example:" clause rather than a bare precondition assertion, and two already self-caveat both sides
  ("Glider TOO live; NIR TOTO future") — different enough in character that guessing a fix risked
  erasing an intentional single-mode illustration. Re-audit clean (335/0).

**All 6 suites with a MODE-ALL dimension now checked.** ABT/BOS have no MODE-* scheme (no
operating-mode dimension applies to those suites), so this bug class doesn't apply there.
