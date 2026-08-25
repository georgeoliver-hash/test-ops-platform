# ABT (30279) + BOS (30287) — "Data variations:" one-case-per-variant expansion, 2026-07-24

## Why

George's hard rule (2026-07-24, `docs/test-practices.md` / `docs/gherkin-standard.md`): **"no test
should tell someone to test multiple variants... we should have a test for each."** A trailing
`Data variations:` line naming several card schemes/claims/report scopes/scenarios reads as
covered but only ever executes one example — each named variant needs its own trackable pass/fail.
This supersedes the "Data variations is an Examples list, not extra cases" guidance and the
`abt-card-variant-sweep` pass done earlier the same day (which had *added* `Data variations:`
lines to 6 cases — now itself superseded). Mirrors the Operator/Passenger portal split done
earlier today, which is the same rule applied to a different axis (portal, not card/claim/scope).

## Method

1. Pulled each suite fully fresh this session (`TestRailClient.get_cases(42, <suite>)`, excluding
   `ZZ_DELETE_*`): suite 30279 = 272 cases, suite 30287 = 175 cases.
2. Grepped every case's full body (title/preface/preconds/steps/expected) for `data variation` /
   `variations:`, plus a broader pass for multi-scheme mentions (`visa`/`mastercard`/`maestro`
   co-occurring) and other enumeration signals (`scheme split`, `product type`, `report type`,
   `entitlement`) to catch anything not using the exact tag. No additional families found beyond
   the tag-matched ones.
3. For each family, expanded at the **literal top-level semicolon-delimited item** in the original
   `Data variations:` text (the same granularity used for both suites, so a nested comma-list
   *inside* one item — e.g. individual report-detail columns, or sub-claims inside one module —
   stays as in-case supporting detail, not exploded further; only the top-level named things that
   can independently pass/fail become separate cases).
4. First/primary variant reuses the original case id (retitled + reworded to name just that
   variant); remaining variants become new cases in the same section. Grounded strictly on the
   source case's own content/refs — no invented values; unconfirmed worked examples marked `**GAP**`
   rather than fabricated (Transfers Scenarios 3/2+4/11).
5. Pushed via `tools/apply_rewrite.py` (primary-case updates) and a new generic
   `proposals/coherence-audit/fixes/push_new_cases.py` (new cases into the existing section —
   no new sections needed, unlike the portal split). Dry-run first, then `--commit`.
6. Re-audited each suite (`python -m system_test_ops audit --suite <id> --no-gate`).

## Suite 30279 (ABT-only) — 9 families found, 21 new cases

| Primary (retitled, id kept) | New variants created | Axis |
|---|---|---|
| C4102852 Debt Recovery — automated **Visa** recovery | C4104540 Mastercard, C4104541 Maestro | card scheme cadence |
| C4102857 Access — **Account Management** claims | C4104542 Admin, C4104543 Capping, C4104544 Reports | claim group |
| C4102871 Transfers — **Directional feeder→Glider** (Scenario 1) | C4104545 Non-Directional (Scenario 3), C4104546 Glider→feeder (Scenarios 2/4), C4104547 Ulsterbus→Glider (Scenario 11) | FBD-100651 §7.4 scenario |
| C4102894 EMV Summary Report — **Visa** | C4104548 MasterCard, C4104549 Maestro | card scheme |
| C4102908 Retail Debt Report — **Visa** | C4104550 Mastercard, C4104551 Maestro | card scheme |
| C4102937 Card Verification — Issuer Liability, **Visa** | C4104552 Mastercard, C4104553 Maestro | card scheme (REQ-3354) |
| C4102939 Card Verification — pre-auth first daily use, **Mastercard** | C4104554 Maestro | REQ-3360/REQ-3361 |
| C4102940 Card Verification — pre-auth after Deny List removal, **Mastercard** | C4104555 Maestro | REQ-3360/REQ-3361 |
| C4102954 Declined taps — **expired card** (DeclinedReason 1) | C4104556 On Deny List (2), C4104557 Declined/ODA (3), C4104558 Cancelled (4), C4104559 On BIN List (15), C4104560 Passback (20) | FBD-100658 DeclinedReason enum |

**Grounding notes:**
- Transfers (C4102871 family): Scenario 1's real worked example (Ulsterbus G10D→Glider East) was
  kept; Scenarios 3/2+4/11 have no worked route example in the source case, so each carries a
  `**GAP**` marker asking for a live route before running — not invented.
- EMV Summary Report / Retail Debt Report: only the **card-scheme** axis was split (each scheme's
  totals can fail independently); export-format (PDF/XLS/CSV) and row-detail columns stayed as
  in-case supporting content in every scheme variant, same treatment as the un-split axis in the
  card-variant-sweep precedent.
- Retail Debt Report refs distributed per real bug scope, not copied blind: `CA-13549` ("NaN in
  Visa and Mastercard cells") on the Visa/Mastercard variants only; `TODEV-15538`/`TODEV-11567`
  (Maestro-specific) on the Maestro variant only.
- Card Verification families reuse the exact old-suite id already cited per scheme in the
  2026-07-23 card-variant-sweep changelog (C2665815/16/17, C2665819–22).

## Suite 30287 (BOS) — 3 families found, 16 new cases

| Primary (retitled, id kept) | New variants created | Axis |
|---|---|---|
| C4104254 Configure report access — **TVM/Cash** reports | C4104790 Staff, C4104791 Alert, C4104792 Asset, C4104793 Topology | report sub-claim (FBD-100342) |
| C4104255 Configure module/group access — **operator-scope claims** | C4104794 Dashboard, C4104795 Events & Alerts, C4104796 Topology & Fares, C4104797 Schedule Manager, C4104798 Estate Management, C4104799 Reports, C4104800 System Configuration, C4104801 gate/station claims | module/claim group (FBD-100342) |
| C4104258 Fares export — **standard fares list** | C4104802 ABT Fares export, C4104803 Route Attributes, C4104804 Area/Zone overlays, C4104805 single-file export | export scope |

**Grounding notes:**
- Operator-scope claims (CF Full Operator vs CF-Operator-`<Name>`) kept as **one** case — the
  source text presented it as a single "vs" comparison (like the un-split original, which already
  set up two operators to compare), not a flat enumerated list, so splitting it further would
  invent a distinction the source doesn't draw.
- Fares export: only the **export-scope** axis (standard fares list / ABT Fares export / Route
  Attributes / Area/Zone overlays / single-file export) was split — each is a genuinely different
  export surface. File format (XLSX/CSV) stayed as in-case supporting detail in every scope
  variant, same treatment as EMV Summary Report's export-format list in 30279.

## Not touched / no other family found

Broader sweep for scheme/report/entitlement enumeration signals outside the literal `Data
variations:` tag found nothing further in either suite — no other case combines >=2 scheme
mentions or an unflagged enumerated list.

## Verification

- Suite 30279: dry-run then `--commit` — `apply_rewrite.py`: `updated: 9 removed(ZZ): 0 skipped: 0
  missing: 0`; `push_new_cases.py`: `created=21 skipped=0 errors=0` (C4104540–C4104560).
  `python -m system_test_ops audit --suite 30279 --no-gate`: **293 cases, 45 blocking** (was 41
  pre-existing). The +4 is **not a new defect**: it is the pre-existing, already-blocking
  `**UNCONFIRMED**`-report-existence `preface-bad-preamble` finding on C4102894/C4102908 now
  counted once per split case (2 pre-existing instances -> 6 across the 3 Visa/MasterCard/Maestro
  variants each = +4 net). The 5 `then-compound-genuine` findings are all pre-existing, unrelated
  case ids (C4102818 x2, C4102822, C4102865, C4103488) — none of the 30 touched/created ids appear
  in any blocking category.
- Suite 30287: dry-run then `--commit` — `apply_rewrite.py`: `updated: 3 removed(ZZ): 0 skipped: 0
  missing: 0`; `push_new_cases.py`: `created=16 skipped=0 errors=0` (C4104790–C4104805).
  `python -m system_test_ops audit --suite 30287 --no-gate`: **191 cases, 48 blocking** — identical
  to the 48 pre-existing baseline. None of the 19 touched/created ids appear in any blocking
  category; 5 new cases (C4104795–C4104798, C4104800) appear only in the advisory
  `title-too-long` list (descriptive module-name titles run long — same carve-out as the portal
  split).

## Counts summary

- **30279**: 9 families expanded, 21 new cases (C4104540–C4104560), 9 primary cases retitled/
  reworded in place, 0 cases removed. Blocking findings 41 -> 45 (fully explained mechanical
  duplication of a pre-existing gap, see above).
- **30287**: 3 families expanded, 16 new cases (C4104790–C4104805), 3 primary cases retitled/
  reworded in place, 0 cases removed. Blocking findings 48 -> 48 (unchanged).
- **Total: 12 families, 37 new cases, 12 primary cases reworded, 0 net new blocking findings**
  (30279's +4 is a pre-existing gap counted per split case, not a new one).

## Files

- `proposals/coherence-audit/fixes/build_abt_variant_expansion_30279.py` — generator (30279).
- `proposals/coherence-audit/fixes/abt-variant-expansion-30279.rewrite.json` — 9 primary updates.
- `proposals/coherence-audit/fixes/abt-variant-expansion-30279.new-cases.json` — 21 new cases.
- `proposals/coherence-audit/fixes/build_bos_variant_expansion_30287.py` — generator (30287).
- `proposals/coherence-audit/fixes/bos-variant-expansion-30287.rewrite.json` — 3 primary updates.
- `proposals/coherence-audit/fixes/bos-variant-expansion-30287.new-cases.json` — 16 new cases.
- `proposals/coherence-audit/fixes/push_new_cases.py` — generic new-case pusher (reusable), used
  for both suites.
- `proposals/coherence-audit/fixes/abt-bos-variant-expansion.changelog.md` — this file.
- No changes to old suite 14441 (read-only, never touched); no re-touch of the 56 Operator/
  Passenger portal-split pairs from earlier today.
