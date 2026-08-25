# TVM operating-mode coverage map

**Why this doc exists.** TVM is structured **test-type-first** (Functional / Non-Functional / Smoke),
not mode-first like POS. That is deliberate (see `structure.md` — the model×mode cross-tab proved
~90% shared behaviour) — but it means the suite's *sections* don't reliably tell a run-builder which
**mode** a case is worth re-running for. This map is the missing signal: every **live** case in suite
30284 now carries a `MODE-*` tag in its **Refs** field so George can filter TestRail by Refs when
building a run, instead of re-running every mode-irrelevant case (EMS, cash-hardware, EMV mechanics,
generic UI) across all four modes' runs.

**Scope note — Model vs Mode.** TVM's Configurations are two dimensions: **Model {Kiosk, Astreo} ×
Mode {NIR-Rail, Ulsterbus, Metro, Glider}**. This tagging pass is **mode only**. The model dimension
(Kiosk/Astreo — a hardware variant, not an operating mode) stays exactly as `structure.md` documents
it: handled by the existing `(Kiosk only)` / `(Astreo only)` section leaves and TestRail Run
Configurations, untouched here. A case's `MODE-*` tag says nothing about which model(s) it runs
against — that's still the section it lives in.

## The tag scheme

| Tag | Meaning |
|---|---|
| `MODE-ALL` | Shared case; the **outcome** could plausibly differ by mode (fare/ticket/product/rail-vs-bus-vs-glider config-driven behaviour) even though the steps read identically. Re-run per relevant mode. |
| `MODE-NIRRAIL-ONLY` | Genuinely NIR-Rail-specific (rail/cross-border ticket products, NIR legacy-stage barcode resolution, rail-only barcode ticket formats). Runs only under the NIR-Rail (Kiosk) configuration. |
| `MODE-ULSTERBUS-ONLY` / `MODE-METRO-ONLY` / `MODE-GLIDER-ONLY` | Reserved for a case genuinely specific to just that one mode. **Unused in this pass** — see "Why no Ulsterbus/Metro/Glider-only cases" below. |
| `MODE-PRIMARY-ONLY` | Shared **and** genuinely mode-irrelevant (EMS/Alarmboard/commissioning mechanics, cash-hardware/BNR/coin-recycler mechanics, most Non-Functional, generic UI/menu functions with zero mode dependency). Needs running only once, on any convenient configuration. |

Tags are **appended** to each case's existing `Refs` (never overwritten) — e.g. a case already citing
`FBD-100483` now reads `FBD-100483, MODE-PRIMARY-ONLY`.

## Coverage tally (suite 30284, 2026-07-27, 317 live cases tagged)

| Tag | Cases |
|---|---:|
| `MODE-PRIMARY-ONLY` | 204 |
| `MODE-ALL` | 80 |
| `MODE-NIRRAIL-ONLY` | 33 |
| `MODE-ULSTERBUS-ONLY` | 0 |
| `MODE-METRO-ONLY` | 0 |
| `MODE-GLIDER-ONLY` | 0 |
| **Total tagged** | **317** |
| Untagged (excluded) | 27 — `ZZ_DELETE_REVIEW` cases (Smartcards & ABT / Mini Statement / one Resilience case), pending George's UI bin-cleanup. Not live coverage; not tagged. See "Flagged finding" below. |

## Why no Ulsterbus/Metro/Glider-only cases

`cross-tab.md` and `structure.md` already proved the **only** genuine mode-divergence in the current
live suite is NIR-Rail (Kiosk-only rail/cross-border ticketing, plus a couple of NIR-specific barcode
behaviours). Every Ulsterbus/Metro/Glider distinction found during this pass turned out to be a
**product/fare variation within an already-shared case** (e.g. "Ticket Issue — Adult single ticket" is
the same case run against Ulsterbus/Metro/Glider products, not three separate cases) — i.e. `MODE-ALL`,
not a dedicated per-mode case. If a genuinely Ulsterbus-only, Metro-only, or Glider-only **behaviour**
is authored later (mirroring how ETM's zone-vs-boarding-stage split earned Metro-only/Ulsterbus-only
cases), tag it with the matching single-mode tag at authoring time and update this doc's tally.

## MODE-ALL — by area (80 cases)

Fare/product/ticket-config-driven areas where the same case is re-run per relevant mode because the
underlying product or fare genuinely varies:

| Area | Cases | Why MODE-ALL |
|---|---:|---|
| Sales — Ticket Issue | 32 | Product/fare selection (Adult/Child/Family/Popular/Evening/Day/3-Day-family/concessionary/barcode-on-issue), each payment-method variant (cash/card/contactless) — outcome (fare, barcode eligibility) is config-driven per mode's product catalogue. |
| Sales — Advance & 3-Day | 4 | 3-day product is bus/Metro/Glider-shared; fare and validity are config-driven. |
| Sales — Basket | 13 | Basket totals/lines are computed from the mode's live fare table; a fare-calc bug can be mode-specific. |
| Sales — Grouped Stops | 7 | Cheapest-fare/grouped-Area logic runs on bus-mode farestages (Ulsterbus/Metro/Glider); fare outcome is config-driven. |
| Barcode Redemption — collection by type & format | 8 | Barcode Type B/D/E/H/S/U map onto Rail/Metro/Glider/Ulsterbus products; ticket-layout format cases (Single/Day Return/Half-fare/yLink/24+/Family) are shared across modes' products. |
| Commissioning / EMS — home-location product catalogue | 4 (2 duplicated between Commissioning & EMS sections) | Home-location's fares triangle determines which mode's products are sellable; genuinely config/mode-driven. |
| Resilience — Multi-Modal Home (Bus) | 1 | Bus-mode home screen is shared across Ulsterbus/Metro/Glider. |
| Smoke | 7 | Authored once, run against every Model×Mode configuration per the smoke file's own header — the thin critical path is deliberately re-verified per mode. |

## MODE-NIRRAIL-ONLY (33 cases)

| Area | Cases | Why NIR-Rail-only |
|---|---:|---|
| Sales — Rail & Cross-Border (Kiosk) | 26 | The documented Kiosk-only leaf (`structure.md` divergence #2) — NI Rail and Cross-Border ticket products; Astreo has zero rail sales. |
| Barcode Redemption — legacy-stage resolution (Type B/E/U) | 3 | Resolves the legacy stage **"Any NIR Station"** — an NIR-specific legacy-stages-file entry. |
| Barcode Redemption — ticket format (Cross Border, 3 Day Select) | 2 | Cross-Border and 3-Day-Select are NIR-Rail-only products (no bus-mode equivalent). |
| Ticket Issue — Cross Border/Family & Friends/concession rail products (multi-use barcode) | 1 | Explicitly rail-product multi-use barcode behaviour. |
| Resilience — Multi-Modal Home (Rail) | 1 | Rail-mode home screen only exists under the NIR-Rail (Kiosk) configuration. |

## MODE-PRIMARY-ONLY (204 cases) — representative areas

Exactly the areas the task brief anticipated — mechanics that don't depend on which mode is
configured, so they need only one execution:

- **Commissioning & Deployment** (13 of 15 — all except the 2 home-location-product cases above):
  TID/TK provisioning, software/topology deployment timing, coin-vault threshold, EMV-only config,
  BOS Force-Comms/uVNC.
- **EMS & TMS Maintenance** (28 of 30 — all except the 2 home-location-product cases): sign-in/roles,
  remote lifecycle commands, cash/collection reports, location/sub-location settings, ticket-roll
  length, transaction report, volume/brightness, product-list export, burglary events, battery-saver,
  EMS exit paths.
- **Alarmboard & Enclosure (Kiosk only)** (14) and **Coin Recycler Hopper (Kiosk only)** (3): hardware
  maintenance — mode-irrelevant by nature (and already model-scoped to Kiosk via the section).
- **Payments — Cash** (32) and its **Note Recycler & Change** (Astreo-only 6, Kiosk-only 3) and
  **Coin Recycler Hopper** (Kiosk-only 2) leaves: coin/note acceptance, escrow, jams, BNR/BNA error
  states, change-voucher mechanics — hardware behaviour, not mode-driven.
- **Payments — EMV & Contactless** (50): card-scheme approval/decline, PIN, contactless limits,
  mobile wallets, magnetic stripe — payment-provider mechanics, identical regardless of mode.
- **Sales — Ticket Collection** (4) and **Ticket Numbering** (5): booking-reference entry validation
  and ticket-number sequencing are generic mechanics, not fare/product-dependent.
- **Barcode Redemption — back-office mechanics** (24 of 35): reference-field validation, malformed
  entry, offline/ceiling-limit handling, business-error/retry/fallback, already-redeemed rejection,
  single-use-only enforcement — API/validation mechanics shared regardless of which mode's product
  the barcode represents.
- **Non-Functional / Resilience** (25 of 27, excluding the 2 Multi-Modal-Home cases): degraded/amber
  states, low-change, print failure, mains-failure, device lockout, heartbeat/comms-lock/recovery/
  failover, screensaver wake, audio prompts, performance/throughput — device-level resilience,
  mode-independent.

## Flagged finding — Smartcards & ABT / Mini Statement currently orphaned

While auditing section content for this pass, the **Smartcards & ABT** (21 cases) and **Mini
Statement** (5 cases) sections were found parented under a top-level **`Delete`** section, with every
case titled `ZZ_DELETE_REVIEW - ...` (plus one `ZZ_DELETE_REVIEW` Screensaver/smartcard-flow case
sitting inside `Resilience`). No equivalent live (non-`ZZ_DELETE_REVIEW`) Smartcards & ABT or Mini
Statement content exists anywhere else in suite 30284 — i.e. **this coverage area currently has no
live cases at all**, pending George's review/UI bin-cleanup of the flagged set. These 27 cases were
excluded from mode-tagging (tagging content that's about to be deleted would be wasted effort and
could be silently lost on deletion). **This is a gap worth flagging to George independently of the
mode-tagging task**: either restore the Smartcards & ABT / Mini Statement content to a live section
(it was previously classified in `smartcards-barcode.cases.yaml` as largely `MODE-ALL` — Buy/Top-up/
Concession/Staff-Pass/ABT cases reference Metro- and Ulsterbus-specific products — with no
NIR-Rail-specific behaviour found), or confirm the deletion is intentional and coverage moved
elsewhere.

## Keeping this accurate

Whenever a new case is authored into 30284 (or an existing one materially changes scope), add the
matching `MODE-*` tag to its Refs at authoring time — same discipline as citing `FBD-####`/`REQ-####`.
Re-run `tools/tag_tvm_modes.py --sample 0` (dry-run) to spot any newly-added, untagged case before it
ships un-tagged. If Smartcards & ABT / Mini Statement content is restored to a live section, tag it
per the classification noted above and update this doc's tally.
