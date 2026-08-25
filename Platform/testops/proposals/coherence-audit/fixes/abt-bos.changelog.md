# ABT/BOS suite — CR122 confirmed-live + C4102830 refund-mechanism fix — changelog

**Scope:** 37 cases in suite 30279 (`**NEW** BOS & ABT Suite`, project 42, TFTS - System Test).
**Status: PUSHED TO TESTRAIL** (unlike the sibling `proposals/spec-grounded/**` changelogs, which are
proposal-only). Applied via `tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-bos.rewrite.json
--commit` on 2026-07-21.

Both fixes are grounded on live-system confirmation directly from the engineer (George), 2026-07-21 —
cited in each case as **"George (live-system confirmation), 2026-07-21"**, not a spec paragraph. See
`proposals/coherence-audit/gap-register.md` Q1 and Q4.

## Fix 1 — C4102830: the refund mechanism was wrong

**Before:** "Journey History — cancelling a charged journey refunds it and retains the record" — modelled
a portal "cancel a settled journey" action that does not exist (no portal has a cancel-journey function;
the only cancel mechanism is ETM annulment, device-only, most-recent tap, within 1 minute — FBD-100662
para 204).

**After (George, 2026-07-21):** "on ABT you can refund a processed payment from the Transaction History,
then it must be authorised [approved]." Retitled to **"Transaction History — refunding a processed
journey payment requires authorisation"** and rewrote preface/preconditions/steps around:
1. Locate the settled/processed journey payment in **Transaction History** (not the journey record).
2. Initiate a refund against that payment — it is raised **pending authorisation**, not instant.
3. Once **authorised (approved)**, the refund completes and the journey is retained in Journey History.

Left one narrower gap open and marked `**UNCONFIRMED**` (not resolved by this fix, still needs a follow-up
check): the exact Journey-History indicator/retention representation of a refunded settled journey is not
in the requirement specs.

Citations: `George (live-system confirmation), 2026-07-21` only — this is a live-system fact, not a spec
paragraph, per the task's grounding instruction.

## Fix 2 — CR122 Operator Portal correction family: confirmed live

**Before:** every case in the Metro/Zonal/Reference/Uncapped/Town-service correction sections
(C4102757–C4102790) and two Journey-History correction cases (C4102825, C4102826) carried:
`**UNCONFIRMED** — the portal alighting-stop adjustment (CR122) is a proposal whose full UX is still to
be determined and is not verified on the live test system (FBD-100662 para 691, 693, 271); confirm it is
implemented before running.` — plus an `[UNCONFIRMED]` title prefix.

**After (George, 2026-07-21):** *"CR122 IS live and usable in the Operator Portal test environment."*
(George has **not** confirmed the Passenger Portal side — those cases, e.g. C4102824/827–829/831–849,
were **not** touched and remain `UNCONFIRMED`; out of scope for this fix.)

For all 36 Operator-Portal CR122 cases:
- Removed the `[UNCONFIRMED]` title prefix.
- Replaced the "proposal, UX to be determined" precondition line with a plain statement that the
  correction mechanism is **confirmed live** — cited to `George (live-system confirmation), 2026-07-21`
  — while keeping the FBD-100662 §5.6 (paras 691, 693, 271) citation as the spec basis for the mechanism
  itself.
- For the 34 Metro/Zonal/Reference/Uncapped/Town-service capping cases (C4102757–C4102790), no other
  wording changed: the fare/cap values were already reframed to "example per current ABT pricing config"
  under the earlier Q14 fix, and any pre-existing `**GAP**` markers on specific stop/fare confirmations
  were left as-is (untouched by this fix, still open).
- For C4102825/826 (Journey History, correcting an already-cancelled tap), per
  `docs/gherkin-standard.md`'s "unknown *how*, not unknown *what*" rule: the exact screen/filter mechanics
  the gap-register flagged as unconfirmed (Q21b, "Update Stop list" specifics) were **not** invented.
  Instead the correction action is now phrased as an assumed-tester-knowledge step (e.g. "you change the
  journey's alighting stop") since the **outcome** (CR122 correction working) is now confirmed real even
  though the UI mechanics aren't pinned. The separate, still-open `"**"` cancelled-indicator /
  no-duplicate-row retention gap (Q21) was left `**UNCONFIRMED**` on both cases — unresolved by this fix.

Citations per case: `FBD-100662 para 691`, `FBD-100662 para 693`, `FBD-100662 para 271` (+ `para 204` on
the two Journey History cases) as the spec basis, plus `George (live-system confirmation), 2026-07-21` for
the "confirmed live" fact.

## Case-id list (37)

- **C4102830** — refund-mechanism reground (Fix 1).
- **C4102757–C4102790** (34 cases, Metro/Zonal/Reference/Uncapped & Single Taps/Town Service Cap sections)
  — CR122 UNCONFIRMED marker removed (Fix 2).
- **C4102825, C4102826** (Journey History, correction-on-cancelled-tap) — CR122 UNCONFIRMED marker removed,
  screen mechanics kept as assumed-tester-knowledge, separate indicator/retention gap left open (Fix 2).

## Not touched (explicitly out of scope)

- Passenger-portal CR122 cases (Q2 unanswered) — remain `**UNCONFIRMED**`.
- The wider Journey-History/Correction-Limits/Update-Stop-List CR122 cases beyond C4102825/826
  (C4102827–849, C4103480–484) — the task scope was the Operator-Portal capping family +
  C4102825/826 only; these were not re-read/re-pushed in this pass.
- C4102823/824/829/832 (annulment-retention cases) and any case in the "Delete" section not named above.
- Any suite other than 30279.

## Verification

- `python tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-bos.rewrite.json` (dry-run):
  `updated: 37  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0`.
- `--commit`: same counts, applied.
- `python -m system_test_ops audit --suite 30279`: suite-wide result is 391 cases audited, 282 blocking +
  221 advisory findings — but **none of the 37 fixed case ids appear in any blocking-finding section**
  (`preface-bad-preamble`, `step-first-not-when`, `step-content-not-when-and`, `step-no-then`,
  `then-compound-genuine` all 0 hits for these ids). The only section any of the 37 appear in is the
  advisory **"Title over 72 chars"** list (pre-existing title lengths; unaffected by this fix — stripping
  `[UNCONFIRMED] ` only shortens titles). The suite's 282 blocking findings are pre-existing, spread across
  the ~354 other cases in this suite untouched by this task; this fix introduces zero new blocking
  findings. Report: `reports/tfts-system-test/new-bos-abt-suite/2026-07-21/alignment-audit.md`.
