# PV coherence-audit fixes — changelog

**Suite:** 30255 (`**NEW** PV-Acceptance Test Suite`, project 42)
**Applied via:** `python tools/apply_rewrite.py proposals/coherence-audit/fixes/pv.rewrite.json --commit`
**Status: PUSHED to TestRail** (dry-run verified first, then `--commit` on 2026-07-21).

## Source of the two fixes

Both facts were confirmed directly by George (live-system confirmation), 2026-07-21, and are
recorded as answered questions **Q8** and **Q9** in `proposals/coherence-audit/gap-register.md`.
Both cases had already been stamped `**UNCONFIRMED**` in-suite on 2026-07-17 pointing at these
same gap-register questions, so this session closes that loop.

## Cases corrected: 0 · Cases condemned: 2

Both cases were resolved by **condemnation** (`ZZ_DELETE_REVIEW` title prefix via `action: "remove"`),
not rewording — in both cases the sibling case already fully and correctly models the real
behaviour, so rewriting to match reality would only produce a duplicate. Per
`docs/test-practices.md` (no duplication) and the CLAUDE.md no-invention rule, condemning rather
than forcing a distinct-sounding rewrite was the correct call.

### C4101005 — "Barcode — single-use validation" → `ZZ_DELETE_REVIEW - Barcode — single-use validation`

- **Was:** described the PV validating a single-use barcode (accept when valid, reject with reason
  when invalid).
- **Confirmed wrong** (George, live-system confirmation, 2026-07-21 — gap-register Q8): the PV
  validates **multi-use barcodes only**. FBD-100167's device matrix states POS/TVM validate
  single-use only; ETM/HHD/GV/**PV** validate multi-use. There is no PV single-use validate-and-accept
  flow to correct the case into.
- **Sibling check:** C4103559 ("Single-Use Barcode — rejected as not accepted on this device",
  citing FBD-100167 + FBD-100317) already tests exactly the correct PV behaviour for a single-use
  barcode (rejected as not accepted on this device).
- **Decision:** condemned, not reworded — nothing distinct is left for C4101005 to cover once the
  wrong "PV validates single-use" premise is removed; any rewrite would duplicate C4103559.
- Citations: FBD-100167, FBD-100317, gap-register.md Q8.

### C4101085 — "PV to BOS — communications resilience and failover" → `ZZ_DELETE_REVIEW - PV to BOS — communications resilience and failover`

- **Was:** described the PV continuing to work through a back-office comms interruption/loss by
  using a secondary failover channel.
- **Confirmed wrong** (George, live-system confirmation, 2026-07-21 — gap-register Q9): the PV is
  **Ethernet-only with no failover**. Per FBD-100359's Ethernet hard-failure rule, a sustained
  Translink-network outage puts Ethernet devices offline and, after a significant period, into a
  communication-locked **out-of-service** state — there is no secondary/failover channel.
- **Sibling check:** C4103568 ("Comms Lock — a sustained network outage drives the PV out of
  service", citing FBD-100359) already tests exactly this — sustained outage → out of service, no
  failover. C4103569 ("Comms Recovery — transactions queued during an outage are delivered on
  restore") already covers the recovery/queue angle.
- **Decision:** condemned, not reworded — with the "keeps working via failover" premise removed,
  the correct behaviour (drop → out-of-service) and the recovery angle are both already covered by
  C4103568/C4103569; a rewrite would duplicate one of them.
- Citations: FBD-100359, gap-register.md Q9.

## Audit result

`python -m system_test_ops audit --suite 30255` after the push:

```
audited 131 cases: CLEAN; 22 advisory.
```

CLEAN of blocking findings. The 22 advisory items are the two pre-existing title-style checks
(`title-no-emdash`, `title-too-long`) — advisory only, not blocking, and out of scope for this fix.
Report: `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/alignment-audit.md`.

## Files

- `proposals/coherence-audit/fixes/pv.rewrite.json` — the applied rewrite spec.
- `proposals/coherence-audit/gap-register.md` — Q8/Q9 answers (source of truth for the two facts).
- This file.
