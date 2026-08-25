# C4102871 — transfer cap → transfer £0.00 fix

Suite 30279 (`**NEW** BOS & ABT Suite`, project 42), section `ABT / Operator Web Portal / Capping
Configuration`. Applied via `tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-transfer-cap.rewrite.json --commit`.

## Background

The live case (originally authored 2026-06-24 as "Configure a transfer capping rule" in
`proposals/bos-abt-suite-restructure/abt-operator-web-portal.cases.yaml`) tested configuring a
"transfer cap" via a "Transfer Caps tab" on a "Price Capping" page. A spec-grounding pass
(`proposals/spec-grounded/abt/capping.rewrite.json` id 4102871) found **no such concept as a
"transfer cap" anywhere in the capping specs** (FBD-100334/100340/100389/100651/100662) — that
pass tightened the title (to "Capping config — configure a transfer capping rule", which *was*
live) but the case **body still asserted the invented premise** ("the administrator configures a
transfer cap" / "the transfer cap is created"). Confirmed directly against the live case via the
TestRail client before making any change.

George's decision (2026-07-21): the case should test that **a qualifying transfer settles at
£0.00**, per FBD-100651/CR123's Glider transfer logic — a genuinely documented behaviour, distinct
from "capping" — if not already covered elsewhere in the suite.

## Duplicate-coverage check

Searched the full live suite 30279 cases baseline (`cases.json`, 496 cases) for "transfer",
"£0.00", "zero", "CR123", "FBD-100651", "Glider":

- **C4103587** "A free bus-to-rail transfer within the window leaves the bus leg uncharged"
  (section `ABT / Functional / NIR Tap-On-Tap-Off`, refs `FBD-100690`) — a genuinely different
  mechanism: a **Bus-to-Rail free-transfer zone** (CR133/CR064), matched by boarding/alighting
  stop membership in a shared zone within the Multi-Journey Time (MJT). Not the CR123 Metro⇄Glider
  transfer logic.
- Several `ZZ_DELETE_REVIEW` / `Delete`-section cases reference "Transfer" only as a **stop name**
  ("Bangor (Transfer)") or as raw audit-table columns (`TransferRouteType` in duplicate/annulment
  test data) — not CR123 transfer-charging assertions, and already condemned/superseded.

**Conclusion: no existing live case tests the CR123 Metro/Glider £0.00-transfer mechanism.** This
is a genuine gap, not a duplicate — so C4102871 was reworded in place rather than condemned.

## Grounding (FBD-100651 §7.4, Glider Tap On Only Specification v5.00)

- §7.4 para 300: Glider Transfers — free transfer to/from Metro/Ulsterbus is a new Glider-era
  concept ("Same Stop taps" vs "Glider Transfers").
- §7.4 para 326: CR123 — introduced to align ABT with the existing SmartLink smartcard transfer
  behaviour.
- §7.4.1 para 330: `TransferRouteType` audit flag. A value of `None` means transfers are not
  enabled for that tap — the rest of the transfer logic is skipped.
- §7.4.3 para 334–337: a previous tap is a transfer-match candidate only if (a) the time between
  taps is ≤ the configured transfer time (spec: "expected to be 90 minutes"), (b) the previous tap
  was itself charged (not a transfer), and (c) the previous tap's `TransferRouteType` was not
  `None`.
- §7.4.4–7.4.5 para 338–341: the new tap is marked as a transfer if **either** matched tap has
  `TransferRouteType = Non-Directional`, **or** both taps share the same `RouteDirection`
  (`Inbound`/`Outbound`).
- §7.4.6–7.4.7 para 342–346: if transfer logic does not apply, the tap is charged as normal; if it
  does, the tap is **not charged** (£0.00), shown in the portals with a transfer icon, and still
  sent to MERIT but under a distinct transfer product (not the standard ABT product).
- Worked example: `Glider Transfer Scenarios V3.00.xlsx`, sheet "1-Dir Fdr to GL" / Scenario 1
  ("Dir Fdr to GL", route example "G10D In to Glider East In"): Tap 1 — Feeder route G10D,
  Directional, Inbound — **Charged**. Tap 2 — Glider East, Directional, Inbound — **No Charge
  (Transfer)**. Used as the case's concrete example per `docs/gherkin-standard.md`'s "concrete
  grounding" rule.

## Change applied (C4102871)

- **Old title:** Capping config — configure a transfer capping rule (title had been tightened by
  an earlier partial push of `capping.rewrite.json`; body was untouched and still invented)
- **New title:** Transfers — a qualifying Metro/Glider transfer is charged £0.00
- **Old body:** administrator "configures a transfer cap"; "the transfer cap is created … applied
  to qualifying transfers" — no such capping-rule type exists in the specs.
- **New body:**
  - Preface: confirms a qualifying Metro/Ulsterbus-to-Glider transfer (or vice versa) is charged
    £0.00 rather than a normal fare (CR123).
  - Preconditions: the seeded ABT test card makes two consecutive taps within the configured
    transfer time (e.g. 90 minutes) — a Directional feeder tap that is charged, then a Glider tap
    in the same direction with `TransferRouteType` not `None`; worked example = Inbound G10D →
    Inbound Glider East (FBD-100651 Scenario 1); signed in to the ABT Operator Portal to verify
    Journey History.
  - Step: the two taps settle at EndOfDay and Journey History is opened → the feeder tap is
    charged its normal fare; the Glider tap is charged £0.00 and shown with the transfer icon; the
    transfer tap is sent to MERIT under the transfer product, not the standard ABT product.
  - Expected result (prose) + a **Data variations** note per the Gherkin standard, covering the
    other qualifying combinations from the scenario tracker (Non-Directional feeder→Glider;
    Glider→feeder; Ulsterbus-with-transfers-enabled→Glider) without multiplying cases.
- **Refs:** `FBD-100651` (was empty).
- No `**GAP**`/`**UNCONFIRMED**` markers needed: the behaviour, the mechanics, and a concrete
  worked example are all directly cited from the full FBD-100651 spec and its companion scenario
  tracker — nothing here is invented or unconfirmed.

## Tooling note

`tools/apply_rewrite.py` did not previously support setting the overall `custom_expected` field or
list-type `refs` (only `title`/`custom_preface`/`custom_preconds`/`custom_steps_seperated`, and it
crashed on a list `refs` value with `TestRail POST … 400: Field :refs is not a valid string.`).
Extended it to (a) accept an optional `expected` key per case (written to `custom_expected`, opt-in
— absent in every other entry in `capping.rewrite.json`, so this is backward-compatible and does
not touch any other case) and (b) join a list `refs` into a comma string like `update_case` already
does. No other proposal file was affected by either change.

## Verification

- `python -m system_test_ops audit --suite 30279 --no-gate`: 391 cases audited, **282 blocking /
  221 advisory** findings total — matches the suite's pre-existing baseline exactly (per the
  earlier note that ~282 blocking findings predate this change). **C4102871 does not appear in the
  audit report at all** (`reports/tfts-system-test/new-bos-abt-suite/2026-07-21/alignment-audit.md`
  has zero matches for `4102871`) — the reworded case introduces no new finding, blocking or
  advisory.
- Live case content re-fetched via `TestRailClient.get_case(4102871)` after commit and confirmed
  to match the intended title/preface/preconditions/steps/expected/refs above.

## Files touched

- `proposals/coherence-audit/fixes/abt-transfer-cap.rewrite.json` (new, this fix)
- `proposals/coherence-audit/fixes/abt-transfer-cap.changelog.md` (new, this file)
- `proposals/spec-grounded/abt/capping.gaps.md` — C4102871 entry marked RESOLVED, rest untouched
- `proposals/spec-grounded/abt/capping.changelog.md` — C4102871 entry annotated as superseded, rest
  untouched
- `tools/apply_rewrite.py` — added `expected` field + list-`refs` support (backward-compatible)
