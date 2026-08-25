# ABT Correction / Journey-History / Duplicate / Late-Tap re-grounding — changelog

Scope: 47 cases across **Update Stop List (11)**, **Correction Limits (5)**, **Journey History (16)**,
**Duplicate Detection (7)**, **Late Taps (8)**. The "Annulment & Re-tap" section was handled separately
and is **not** included here.

**Status (2026-07-21): this file already used the correct `{"content","expected"}` step schema (not
the buggy `{"when","then"}` shorthand found in `admin.rewrite.json`), so its cases were never among
the 51 blank-step cases found in the 2026-07-17 partial push of the sibling admin batch. Verified
directly against the live suite: 0 blank-step cases from this file at any point. Properly
(re-)pushed 2026-07-21 alongside the admin/backoffice/cloudfare-config batch via the same,
now-hardened `tools/apply_rewrite.py` (which now also refuses to push any blank step outright). See
`proposals/coherence-audit/fixes/abt-blank-steps-fix.changelog.md` for the full writeup.**

Governing specs read (via the extractor, paragraph indices cited):
- **FBD-100662** v5.00 — Ulsterbus Tap-On-Only: annulment (para 204), Journey History display (para 264),
  TOO→TOTO split (paras 309–310), capping Saving Type (para 339), **CR122 Alighting Stop Adjustment
  §5.6 (paras 688–694)** incl. passenger correction limit 1/month, 3/year (para 692) and "UX to be
  determined" (para 693).
- **FBD-100690** v4.00 — NIR Tap-On-Tap-Off: DeclinedReason On BIN List = 15 (paras 305/367),
  Card Expired = 1 (paras 301/363), **Same Location Time / duplicate-tap ignoring (para 469)** and its
  icon+Show More indication (para 472), **CR134 leg-splitting exception (paras 473, 484)**, Missing Tap
  Correction incl. limit 1/month, 3/year (paras 792–810), revenue reported on processed date (para 882).
- **FBD-100658** v1.03 — ABT Audit: **DeclinedReason enum 1 = Card Expired, 15 = On BIN List,
  20 = Passback** (paras 210/214/215 and repeats). Note: there is **no "Duplicate" DeclinedReason** —
  duplicate handling is a back-office aggregation concept, not an audit reason.
- **FBD-100389** v5.00 — ABT Scenarios: **Scenario 3 late tap** — late taps accepted up to a **maximum
  of 14 days** (para 233), always retrospectively regarded as the last tap(s) of the day (para 226),
  worked example of retrospective capping (paras 263–288), held by comms failure / quarantine
  (para 229), marked "Late Tap" on the portal (para 278). Passback period referenced (para 147).

## Outcome by action

| Action | Count | Meaning |
|---|---|---|
| `reword` (grounded) | 19 | Traced to a spec paragraph; mojibake fixed; some carry GAP markers for unspecified detail. |
| `unconfirmed` | 28 | Depend on CR122 (a proposal, UX TBD) and/or on invented screen mechanics; intent kept, invented labels/rules removed, `**UNCONFIRMED**` markers added. |
| `keep` / `remove` | 0 | — |

Grounded vs UNCONFIRMED: **19 grounded, 28 UNCONFIRMED.**

## What changed, by section

### Duplicate Detection (7) — all `reword`, grounded on FBD-100690 para 469
- Fixed mojibake (`Â£`→`£`, `â†’`→`→`, `â€”`→`—`) throughout.
- Grounded the duplicate-ignoring principle on the **Same Location Time** rule (para 469) and its
  **icon + Show More** indication (para 472). Cross-referenced the device-level Passback check
  (FBD-100662 para 245, DeclinedReason 20).
- **UNCONFIRMED** the **15-minute window** value (no figure in para 469 — gap Q14) and the
  **"shows £0.00, marked Duplicate" row** representation (spec ignores + flags via icon; it does not
  create a zero-charge journey row — gap Q21).
- Flagged as GAP: the interaction of **retail transactions** with duplicate detection (not in any
  cited paragraph).

### Journey History (16) — mixed
- **Cancellation-retention cases (4102823/24/29/30/32):** removed the cross-surface invention
  "cancel that journey **from the portal**" — there is **no cancel-a-journey action in any portal**;
  reframed on **ETM annulment** (device-only, most-recent tap, within 1 min — FBD-100662 para 204).
  Grounded JH display on para 264. **UNCONFIRMED** the **"\*\*" cancelled indicator** and the
  retain-after-cancel guarantee (defect-fix criteria, not requirements). 4102830 (cancel-a-charged-
  journey + refund) marked fully `unconfirmed` — no portal cancel/refund of a settled journey is
  specified. 4102829 additionally flags that annulment only cancels the most-recent tap, so
  "cancel one of two" may not be achievable.
- **Correction-on-cancelled cases (4102825/26/27/28/31):** `unconfirmed` — removed the invented
  "Update Stop list" label; marked CR122 (FBD-100662 §5.6). Recalculation is grounded (para 691) but
  the feature is unconfirmed.
- **Dropdown-population cases (4102833–38):** `unconfirmed` — the strongest invented-mechanics group.
  Removed the invented "Update Stop list" label, the **"No options"** wording, the exact stop counts
  ("14 stops", "15 stops"), and the **operator-match** rule. Kept only the grounded para-693 rule
  (selectable stops = those after the boarding stop on the same route). These read as acceptance
  criteria for an implemented screen/defect, not requirements.

### Update Stop List (11) — all `unconfirmed`
- Section retitled in each case away from the **invented "Update Stop List"** name (zero requirement
  docs). All the **fare-based filter rules** (fare>0, zero-fare/negative/TVM-only/transfer exclusions,
  "smallest positive fare") are **not in the spec** — para 693 says only "after the boarding stop on
  the same route". Marked CR122 UNCONFIRMED; invented rules removed.
- 4102842 (select stop → update stage + recalc fare) is the best-grounded: recalculation (para 691)
  and operator-portal fare-preview (para 693) are specified — but still CR122 UNCONFIRMED.

### Late Taps (8) — all `reword`, grounded on FBD-100389
- Grounded the **14-day maximum** (para 233), **retrospective-last-tap** capping (paras 226, 263–288),
  comms-failure/quarantine hold (para 229), and the **"Late Tap"** portal marker (para 278).
- 4102941: changed "configured to 14 days" → "is 14 days" (spec states a maximum, not a configurable
  value — minor GAP).
- 4102942: removed the asserted **"rejected as expired"** label — no reject behaviour is specified
  beyond 14 days, and **"expired" collides with DeclinedReason 1 (Card Expired)**, which is unrelated
  card expiry. Marked GAP.
- 4103485: reframed "blocked ETM" as "not communicating / held"; the block-then-release mechanism is
  a GAP (para 229 gives comms failure/quarantine, not a device block).
- 4103488: annulment grounded device-only (para 204); the annulled-tap-among-late-taps settlement
  representation flagged GAP.

### Correction Limits (5) — all `unconfirmed`
- The **1/month, 3/year limit is grounded** (FBD-100662 para 692; analogous TOTO limit FBD-100690
  para 810), and recalculation is grounded (para 691) — but the underlying **alighting-stop correction
  is CR122, a proposal (UX TBD)**, so each case is marked UNCONFIRMED.
- Flagged the **£1.90 Greys Farm** example fare as unverified against a fares export (gap Q14).
- 4103482: the explicit monthly-reset behaviour is implied ("maximum of 1 per month") but not stated.

## The 5 biggest corrections
1. **Invented "Update Stop list" screen name removed everywhere (16 cases).** It appears in zero
   requirement docs; FBD-100662 §5.6 only speaks of "a screen … to select a new alighting stop".
2. **Invented filter rules stripped (fare>0, zero/negative/TVM-only/transfer exclusions, "No options",
   operator-match).** None are in the spec — para 693 grounds only "after the boarding stop on the
   same route". These were asserted as working features and are now UNCONFIRMED.
3. **Cross-surface invention removed: "cancel a journey from the portal".** No portal has a cancel-
   journey action; cancellation is **ETM annulment only** (device-only, most-recent tap, within 1 min —
   para 204). Five Journey-History cases reframed.
4. **CR122 correctly demoted to UNCONFIRMED across all correction cases.** A change request in a spec
   is not a shipped feature; intent kept, but no case now asserts CR122 works.
5. **Late-tap "rejected as expired" corrected.** Removed the label that conflated the 14-day late-data
   limit with DeclinedReason 1 (Card Expired); the >14-day reject behaviour is a GAP, and the "£0.00
   marked Duplicate" journey row was corrected to the spec's ignore + icon representation.
