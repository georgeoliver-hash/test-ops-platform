# ETM — MODE-ALL cases hard-coding a single operator's route (fix)

**Found:** 2026-08-03, via the live run `ETM - OS v8.0.6356` (plan 52401). George flagged testers
marking cases Invalid because a shared case's precondition named an operator/route that didn't match
the Configuration they were running (e.g. a `MODE-ALL` case reading "signed on to **Ulsterbus** route
72b" while executing under the **Metro** run).

**Scope:** scanned all 183 live `MODE-ALL` cases in suite 30254 for a hard-coded `Metro route <n>` /
`Ulsterbus route <n>` in `custom_preconds`. **62 of 183** had one. This was the majority driver of the
~35 Invalid-Test marks logged against this plan so far (confirmed by cross-referencing: several case
ids were marked Invalid in *both* the Metro and Ulsterbus runs — the fingerprint of a shared case that
can never be right in at least one Configuration).

**Fix:** replaced the hard-coded operator+route clause with generic wording, e.g.:
- `a Driver is signed on to Ulsterbus route 72b (IN) at the FLU screen` →
  `a Driver is signed on to a valid route (IN) at the FLU screen`
- `the ETM is signed on and in service on Ulsterbus route 105a (IN) in iLink Zone 2` →
  `the ETM is signed on and in service on a valid route (IN) in iLink Zone 2`

This does not lose real coverage: in every one of the 62 cases, the specific route number was never
referenced again in the steps or expected result — it was scene-setting, not load-bearing. The
fare/product side of each precondition was already generic ("at its configured fare") per the existing
"unknown configured value" convention, so only the route clause needed changing.

**New standing rule** (added to `docs/gherkin-standard.md`, "Concrete grounding" section): `MODE-ALL`
cases must never name a single operator's route — generic wording only. `MODE-<OPERATOR>-ONLY` cases
should keep concrete, operator-specific worked examples as before, grounded via
`knowledge/ABT/ABT_FARE_REFERENCE.md` (the derived route/zone/fare reference built from the ABT
Testing Crib Sheet CSVs) rather than an uncited raw number.

**Cases fixed (62):** C4100539, C4100540, C4100541, C4100545, C4100556, C4104437, C4104441, C4104443,
C4104447, C4104449, C4100567, C4100571, C4104481, C4104483, C4104485, C4100578, C4104488, C4104490,
C4104492, C4104494, C4100581, C4102537, C4102538, C4102540, C4102541, C4102542, C4102543, C4104502,
C4104504, C4104506, C4104508, C4102544, C4102545, C4102546, C4102547, C4102548, C4102549, C4104511,
C4102551, C4102552, C4102553, C4102554, C4102555, C4102556, C4104516, C4104517, C4104518, C4104519,
C4104520, C4104521, C4100582, C4100583, C4100585, C4100591, C4104522, C4104523, C4104524, C4104525,
C4104526, C4104527, C4104528, C4104529.

**Re-audit:** CLEAN — 516 cases, 0 blocking (77 advisory, pre-existing title-style items unrelated to
this change).

**Not yet checked:** other suites (POS, TVM, HHD, GV, PV) may have the same `MODE-ALL`-hardcodes-one-
variant pattern where a shared case names a specific project/mode value. Worth a follow-up sweep before
relying on any suite's `MODE-ALL` cases in a live multi-config run.
