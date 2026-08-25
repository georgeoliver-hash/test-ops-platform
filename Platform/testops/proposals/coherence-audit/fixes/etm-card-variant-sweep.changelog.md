# ETM card/credential-variant completeness sweep — suite 30254 (2026-07-23)

**Mandate:** a follow-up, narrower re-check on top of today's broader
`etm-consolidation-completeness.changelog.md` pass, modeled on a real miss just found in the PV
suite: 13 old-suite cases testing card **schemes** (Visa Debit, Visa Credit, Mastercard Debit,
Mastercard Credit, Maestro) — mechanically identical steps, only the card sample differing — folded
into one new case that named only "Visa, Mastercard, mobile wallet" generically, silently dropping
the Debit/Credit distinction and Maestro. George's directive: every card type/scheme variant tested
must stay individually traceable — "gospel" for any device with smartcard/EMV tapping.

## Method

1. Pulled old suite 4943 fresh (936 cases) and new suite 30254 fresh (526 cases) via the CLI.
2. Regex-swept all 936 old titles for `visa|mastercard|maestro|debit|credit|amex|emv|cemv|contactless`
   to find every card/credential-type family relevant to ETM (11 hits; 3 were HMI screen-validation
   titles and 3 were PV cases mis-filed under "Glider Transfers", already excluded by today's earlier
   pass — see that changelog's family #8).
3. Read the full body (`custom_preface/preconds/steps_seperated/expected`) of every candidate case in
   both suites via `TestRailClient.get_case`, not just titles.
4. For each family, checked whether the new suite's consolidated case names every distinct variant
   explicitly in a `Data variations:` line, or only a generic mention.

## Findings

### 1. Payment card scheme — Flat Fare Tap (the exact PV-pattern match)

Old suite: `Driver Operations / Smartcards and ABT / ABT / Visa` and `/ Mastercard` hold **5**
mechanically identical cases — same preface ("To confirm the ETM can accept EMV taps for Flat Fare
Journeys"), same precondition, same 6-step WHEN/THEN body (ODA scheme check → expiry → deny-list →
validate → success screen/sound → CloudFare/MERIT/passenger/operator portal lookup) — differing only
in the card presented: **Visa Debit** (C2478848), **Visa Credit** (C2478849), **Mastercard Debit**
(C2478846), **Mastercard Credit** (C2478847), **Maestro Debit** (C2478850). Same REQ-#### refs on all
5 (REQ-1488/1489/1507/1512/1516/1567/1720/2519/3345/3348/3559/3563).

New suite: `Functional / ABT` `C4100582` ("ABT — successful tap, passback and mobile wallet") folded
these 5 (plus the separate Mobile Wallet case, C2543144) into one case whose only naming of the
scheme dimension was step 3's `Then "Visa, Mastercard, Apple Pay, Google Pay and Samsung Pay ... are
accepted"` — **Debit/Credit and Maestro were silently dropped**, exactly the PV pattern. Mobile wallet
coverage itself (Apple/Google/Samsung Pay, phone & watch) was already complete — no gap there.

**Fixed.** Reworded `C4100582`:
- Preconditions now name the concrete card set: *"seeded contactless cards (Visa Debit, Visa Credit,
  Mastercard Debit, Mastercard Credit, Maestro Debit) and mobile wallets are available"*.
- Expected result now carries an explicit `Data variations: Visa Debit, Visa Credit, Mastercard
  Debit, Mastercard Credit, Maestro Debit (contactless EMV card schemes); Apple Pay, Google Pay,
  Samsung Pay (phone & watch).` line.
- Refs: old suite 4943 C2478848/C2478849/C2478846/C2478847/C2478850.

The mechanism genuinely is identical across schemes (equivalence partitioning — no new case needed
per `docs/test-practices.md` rubric step 2); the fix is naming, not new coverage.

### 2. Payment-card decline reasons — Deny List / BIN List

Same old-suite section tree, `.../ ABT / Declined Taps`: **2** cases, `Flat Fare Tap - Payment card on
the DenyList` (C2433859) and `- on the BINlist` (C2543145) — each names its specific decline reason
and (for DenyList) the exact passenger-portal banner text and operator-portal red-circle icon.

New suite: `C4100591` ("ABT — invalid taps recorded in back office") generalised both into "the
decline reason is shown against the tap" with no reason named. **Fixed** — added `Data variations:
Deny List decline / BIN List decline.` to the Expected result and named both conditions in the
Preconditions. (Scope note: the old cases' distinct passenger/operator-portal message *wording* per
reason was not re-added — that is a UI-message-fidelity question, out of this pass's card-variant-
naming scope; not flagged as a further gap here since C4100591's existing assertion — "decline reason
shown" — is not factually wrong, just less specific than the old two cases.)

### 3. Other card/credential dimensions checked — no further gap

- **Smartcard products** (60+ concessionary/ABT products) — already the subject of the dedicated
  `smartcards-abt-crosstab.md` audit and `smartcard-products.cases.yaml` build; spot-checked again
  this session, each still its own case with its own invalid/expired/hotlisted branch. No drop.
- **Card technology / PSN range** (MIFARE Classic 1K/EV1, 8-digit PSN) — already fixed in today's
  earlier consolidation-completeness pass (`C4100655`); re-verified live, still present.
- **Barcode types** (Single Use Online/Offline failure reasons, Multiple Use, mLink, legacy) — already
  verified in the earlier pass; re-checked titles/refs this session, all still explicitly named.
- **International Payment Cards** (old C2480211, generic "International Payment Card", no named
  scheme e.g. Amex/Diners) and **Offline/cEMV transactions** (old C2480518, cEMV tap stored during
  comms loss) — checked the full local requirements library (`FBD-100389 ABT Scenarios`, the ABT
  Testing Crib Sheet, the FB110 Handover doc) for Amex/Diners/international-scheme references and
  found none — the old case itself never names a specific scheme either, so there is no named variant
  to silently drop; treated as already-generic in the source, not a card-scheme completeness gap.
  Offline/cEMV tap-storage is covered as a generic comms-restore mechanism by `C4100647`
  ("Communications — comms lock, interruption and restore") — same mechanism regardless of what data
  is queued, a legitimate equivalence-class fold, not scheme-specific.
- **Mobile wallet** (Apple/Google/Samsung Pay, phone & watch) — already fully named in `C4100582`
  before this session's edit; confirmed intact.

## Applied changes

1. Reworded `C4100582` — added the 5 named card schemes to Preconditions + a `Data variations:` line.
   Refs: old suite 4943 C2478848, C2478849, C2478846, C2478847, C2478850.
2. Reworded `C4100591` — added `Data variations: Deny List decline / BIN List decline.`
   Refs: old suite 4943 C2433859, C2543145.

File: `proposals/coherence-audit/fixes/etm-card-variant-sweep.rewrite.json`, applied via
`tools/apply_rewrite.py --commit` against `TESTRAIL_WRITE_SUITE_ID=30254`.

## Re-audit result

`python -m system_test_ops audit --suite 30254` after commit:

```
        0  mojibake
        8  title-no-emdash (advisory)
       68  title-too-long (advisory)
        0  preface-empty / preface-bad-preamble
        0  preconds-empty / preconds-no-given
        0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
        0  then-compound-genuine
        0  expected-empty / expected-starts-then
        0  has-tags
  audited 456 cases: CLEAN; 76 advisory.
```

**CLEAN of blocking findings** (456 active cases, unchanged count — this session only reworded 2
existing cases, added no new ones; 76 advisory title-style items, unchanged).

## Summary

- **Families checked:** payment card scheme (Flat Fare Tap / ABT), payment-card decline reasons
  (Deny List / BIN List), smartcard products, card technology/PSN range, barcode types, international
  payment cards, offline/cEMV transactions, mobile wallet.
- **Genuine gap found and fixed (the PV-pattern match):** payment card scheme — Debit/Credit
  distinction and Maestro silently dropped from `C4100582`, now named explicitly.
- **Related gap found and fixed:** decline-reason naming (Deny List / BIN List) on `C4100591`.
- **No further gap found** in the other dimensions swept this session.
- **Old suite 4943: untouched** (read-only throughout).
- **Suite 30254: CLEAN of blocking findings** after commit.
