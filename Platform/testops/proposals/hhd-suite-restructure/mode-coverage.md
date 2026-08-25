# HHD operating-mode coverage map

**Why this doc exists.** HHD is structured **test-type-first** (Functional / Non-Functional /
Regression / Smoke), not mode-first like POS. That is deliberate (see `structure.md`'s "Mode decision"
and the ETM precedent it follows) — but it means the suite's *sections* don't tell you which mode a
case runs in. This map is the missing signal: it states, per case, whether it runs under **both**
modes, is **NIR-Rail-only**, **Glider-only**, or is mode-irrelevant (**Primary-only**, run once). It is
the source of truth for setting up the TestRail **Run Configurations** and for the automation repo
(which mode(s) a test must exercise).

## The mode mechanism

HHD modes = **NIR-Rail** and **Glider** (bus / Metro network; Metro and Ulsterbus are product sets
*within* Glider, not separate device trees — see `structure.md` / `old-suite-audit.md` §4). Modes are
an **execution** concern, handled by **TestRail Run Configurations**, not by the section tree:

- **Shared cases** (`MODE-BOTH`, the largest group) are authored once and run **once per
  Configuration** (NIR-Rail, Glider). One case, two executions.
- **Mode-specific cases** (`MODE-NIRRAIL-ONLY` / `MODE-GLIDER-ONLY`) are named by mode and run
  **only** under that Configuration — the six proven divergences from `structure.md`'s "Mode decision".
- **Mode-irrelevant cases** (`MODE-PRIMARY-ONLY`) are genuinely mode-agnostic device/hardware/session
  mechanics (Card Payment/M020 pairing mechanics, Sign On/Supervisor/Technician menus, Non-Functional/
  Resilience) — run **once**, on a default/primary configuration, not duplicated across both.

> **Live setup still needed:** create the two Run Configurations (NIR-Rail, Glider) on suite 30285 in
> the TestRail UI, then build runs as `Shared (MODE-BOTH) + the mode-specific cases for that mode`, and
> the `MODE-PRIMARY-ONLY` set once regardless of configuration. Until that's done there is no mode
> signal in TestRail at all beyond this map and the `refs` tags.

## Tag scheme (agreed with George, 2026-07-27)

Every case's `refs` field carries an appended `MODE-*` token (existing `REQ-####`/`FBD-#####`/
`TIBU-####`/etc. citations preserved verbatim, comma-joined, no spaces added — see
`tools/apply_hhd_mode_tags.py`):

| Tag | Meaning |
|---|---|
| `MODE-BOTH` | Shared case where the outcome could plausibly differ by mode (fare/ticket/product/entitlement/config-driven), even if the steps read identically. Run once per Configuration. |
| `MODE-NIRRAIL-ONLY` | Already mode-specific to NIR-Rail (one of the three proven NIR divergences: Cross-Border tickets, Card-payment reference-number stations, Single-Use Barcodes/CR094). |
| `MODE-GLIDER-ONLY` | Already mode-specific to Glider/Metro/Ulsterbus (one of the three proven Glider divergences: Metro/Ulsterbus product family, Old Barcode Redemption/BRS, cEMV Revenue Inspection). |
| `MODE-PRIMARY-ONLY` | Shared AND genuinely mode-irrelevant (Sign On, most Non-Functional, general device/hardware mechanics, M020 pairing mechanics) — only needs running once. |

## Classification method

Grounded in a full-body content read of every live case in suite 30285, cross-checked against
`structure.md`'s "Mode decision" (the six proven divergences) and `old-suite-audit.md` §4's
shared-vs-mode cross-tab. The full id → tag map lives in `tools/hhd_mode_tags.py`; the section-by-section
rationale (as inline comments there) is:

- **NIR-only (34 cases):** Card Payment reference-number stations (2); Sales — Cross-Border Tickets +
  the explicit "(NIR-Rail, ...)" 3-Day-Select cases (10); the whole Single-Use Barcodes (CR094) section
  (11); Ticket Formats & Waybill NIR layouts (11).
- **Glider-only (72 cases):** Multi-Use Barcodes / Old Barcode Redemption (1); Sales — Metro &
  Ulsterbus Products (17); the whole Revenue Inspection (cEMV/RID) section (18, Glider TOO live now —
  NIR TOTO is `@future` per FBD-100690, not authored); Sign On — Inspector/Validation Mode tying to the
  Glider-only TOO feature (3); Smartcards & ABT explicit "(Glider)" products + Glider inspection-tap
  cases (9); Ticket Formats & Waybill Glider formats (16); Top-Ups Daylink/Metro Travelcard/BVP/
  Ulsterbus-labelled product family (8).
- **Primary-only (83 cases):** Annulment & Reversal generic device/payment mechanics (6); the whole
  Card Payment (M020) section — pairing, TID/TK, scheme accept/decline, timeout, cancel, PAN masking,
  PRN format, on-charge are payment-device mechanics independent of fare mode (23); Operator menu/UI (7);
  one Penalty Warning RBAC-only case (1); Sign On & Session generic auth/session/device mechanics (13);
  one Smartcards & ABT device-capability-limitation case (1); the whole Supervisor section (10); the
  whole Technician section (7); Ticket Formats waybill-reconciliation mechanic (4); the whole
  Non-Functional/Resilience area (13, per the tag definition's explicit example).
- **Both (146 cases):** the remainder — Annulment (product-specific, 6), Multi-Use Barcodes (8),
  Operator favourites/penalty-fare-issue (2), Penalty Warning/Fares fare-driven rest (13), Sales
  Basket/Group/Ticket-Issue/Visual-Inspection generic product+payment cases (36), Sign On topology/
  route-service selection (2), the whole Smartcard Inspection section (18), Smartcards & ABT shared
  entitlement/product validation rest (29), Ticket Formats generic across-mode formats (5), Top-Ups
  shared entitlement rest (21), Smoke (6).

## Applied

Dedicated scripts, suite-locked via `TestRailWriter` (append-only to `refs`, never overwrites
existing `TIBU-####`/`FBD-#####`/`REQ-####` citations):

1. `tools/hhd_mode_tags.py` — the id → tag map (335 ids, 0 duplicates, verified via its own
   `__main__` self-check).
2. `tools/apply_hhd_mode_tags.py --sample 5` (dry-run) — reviewed the diff shape before running wider.
3. `tools/apply_hhd_mode_tags.py` (dry-run, all 335 mapped cases) — confirmed the full plan,
   0 cases left unclassified, before any write.
4. `$env:TESTRAIL_WRITE_SUITE_ID="30285"; --commit` — applied in **two passes** (see "TestRail refs
   250-char limit" below): first pass wrote 256 cases before hitting a field-length rejection; the
   script was hardened to catch per-case write errors and continue instead of aborting the whole run,
   then re-run to completion (idempotent — the 256 already-tagged cases were no-ops on the second pass).

## Tally (post-tagging, re-pulled live)

| Tag | Cases |
|---|---:|
| `MODE-BOTH` | 133 |
| `MODE-PRIMARY-ONLY` | 83 |
| `MODE-GLIDER-ONLY` | 72 |
| `MODE-NIRRAIL-ONLY` | 34 |
| **Tagged total** | **322** |
| Excluded (`ZZ_DELETE_REVIEW`, not tagged) | 3 |
| Flagged / not written (refs field overflow) | 13 |
| **Live suite total** | **338** |

322 of 335 classifiable live cases carry a `MODE-*` tag. The classification map itself covers all 335
(146 `MODE-BOTH` planned, 133 written — the 13-case gap is the overflow group below, still classified
as `MODE-BOTH` in `hhd_mode_tags.py`, just not yet written to TestRail).

## TestRail `refs` 250-char limit — 13 cases flagged, not written

**Not silently dropped — a genuine platform constraint, routed to engineer review per this repo's
gap-register convention, not decided unilaterally.**

TestRail rejects `update_case` with `"Field :refs is too long (250 characters at most)."` for 13
Smartcard Inspection cases. All 13 share the same long existing citation:

```
Smartcard Use Matrix; HHD Inspection & Validation Design Note (NIR Inspection + Validation),REQ-....
```
— already **245 characters**, leaving only 5 free before the field limit, but `,MODE-BOTH` needs 10.

**Affected cases (all Smartcard Inspection, all classified `MODE-BOTH` in the map, untouched refs):**
C4103971, C4104773, C4104774, C4104775, C4104776, C4104777, C4104778, C4104779, C4104780, C4104781,
C4104782, C4104783, C4104784.

**Not resolved here because:** shortening the existing citation text (e.g. dropping the
`(NIR Inspection + Validation)` parenthetical, which looks redundant given the section name) would be
an edit to an *existing* citation, not an append — outside this task's append-only mandate, and this
repo's rule is no invented/unconfirmed changes to case content without engineer sign-off.

**Recommended options for the engineer (pick one, or a route via `gap-register.md`):**
1. Shorten the shared doc-name citation for these 13 cases (confirm the parenthetical is genuinely
   redundant before removing it).
2. Move the long `Smartcard Use Matrix; HHD Inspection & Validation Design Note (...)` reference out
   of `refs` into the case preface/description (if the field supports it) and keep `refs` for
   short REQ/TIBU/MODE tokens only.
3. Accept these 13 as `MODE-BOTH` **by convention** (Smartcard Inspection is a whole-section
   `MODE-BOTH` call per the classification above) without a written tag, and rely on this doc + the
   `hhd_mode_tags.py` map as the source of truth for Run-Configuration authoring instead of the `refs`
   field for just these 13.

Until resolved, treat these 13 as `MODE-BOTH` (per the map) for Run-Configuration build purposes even
though the live `refs` field does not yet carry the token.

## Why HHD differs from POS (and matches the ETM/GV precedent)

| | POS | HHD |
|---|---|---|
| Modes | **3** — NIR (rail), Ulsterbus, Metro | **2** — NIR-Rail, Glider (Metro/Ulsterbus as product sets within Glider) |
| Divergence | Heavy — rail tickets, Metro cash-only + no-validation, mode-specific products | Moderate — 6 proven divergent areas (cross-border, CR094 single-use, ref-number stations / Metro-Ulsterbus products, Old BRS, cEMV inspection); ~65% of cases still `MODE-BOTH` or `MODE-PRIMARY-ONLY` |
| Old suite | Triplicated per mode | NIR + Glider parallel trees, tripled again by HHD Master |
| Chosen structure | **Mode-first sections** | **Feature/test-type-first** + Run Configurations |

**The department convention:** choose structure by **degree of mode divergence** (recorded in
`etm-suite-restructure/mode-coverage.md`). HHD's divergence is real but confined to six named areas —
feature-first + Run Configurations avoids recreating the old suite's NIR×Glider duplication (the very
thing this consolidation removes) while still making the six genuine divergences visible as named
mode-specific cases.

## Keeping this accurate

Regenerate the tally from `tools/hhd_mode_tags.py` + a fresh `TestRailClient.get_cases(42, 30285)`
pull whenever HHD cases are added/edited. If a new mode-specific behaviour is added, name it by mode,
add it to `hhd_mode_tags.py`, and re-run `tools/apply_hhd_mode_tags.py --commit`.
