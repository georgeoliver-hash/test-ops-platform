# ETM flow-map coverage — `/audit-flows translink ETM 30254`

Baseline: `cases.json` (587 cases, suite 30254, 2026-08-05). All 16 flow-maps under
`knowledge/flows/translink-etm-*.md` audited. Consolidation pre-check: `consolidation-audit.md`
(suite-wide: clean, 0 fold groups; flow-level: 2 fragmented paths, both deferred below).

## Totals across all 16 flow-maps

| Classification | Count |
|---|---|
| covered | ~93 |
| partial | ~70 |
| missing | ~46 |
| stale | 1 |
| fragmented | 2 |
| flow-map row itself GAP (excluded from above, escalated) | 15 |

(Counts are additive across per-flow-map agent reports; treat as approximate — the authoritative
detail lives in each flow-map's own Paths table, now fully filled.)

## Per flow-map

| Flow-map | Paths | covered | partial | missing | stale | fragmented | GAP |
|---|---|---|---|---|---|---|---|
| driver-signon | 25 | 11 | 8 | 6 | 0 | 0 | 0 (1 note) |
| driver-menu-options | 23 | 15 | 7 | 1 | 0 | 0 | 0 |
| driver-menu-annulment | 9 | 2 | 5 | 0 | 0 | 0 | 1 |
| flu-abt-emv | 5 | 1 | 3 | 1 | 0 | 0 | 0 |
| flu-basket-mode | 12 | 2 | 6 | 2 | 1 | 0 | 2 |
| flu-navigation | 10 | 3 | 3 | 3 | 0 | 0 | 1 |
| flu-printer-travel-mode | 9 | 2 | 4 | 2 | 0 | 0 | 1 |
| flu-promo-numeric | 9 | 1 | 4 | 4 | 0 | 0 | 0 |
| flu-smartcard | 14 | 4 | 7 | 3 | 0 | 0 | 0 |
| flu-ticket-issue | 9 | 5 | 2 | 0 | 0 | 1 | 0 |
| supervisor-menu | 12 | 6 | 4 | 2 | 0 | 0 | 0 |
| technician | 36 | 9 | 8 | 19 | 0 | 0 | 1 |
| barcode-scanning | 28 | 9 | 5 | 12 | 0 | 1 | 2 (4 paths affected) |
| displays-leds-audio | 29 (screen states) | 29 | 0 | 0 | 0 | 0 | 0 (2 notes) |
| power-interruption | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| revenue-limit | 4 | 3 | 1 | 0 | 0 | 0 | 0 |

## Highest-risk gaps (recommend authoring first)

1. **technician** — 19 of 36 paths missing, almost entirely Go Back/Cancel navigation edges and
   error/edge forks (home-location-unavailable destination, invalid-smartcard routing, print-failure
   routing, BV reboot, page-2 paging). Largest single gap surface in ETM.
2. **barcode-scanning** — the entire Retry/Cancel button cluster (7 unverified navigation branches on
   failure screens) plus path 2 (no-data-received isn't in the failure taxonomy at all) and path 15
   (silent background offline-store path completely untested).
3. **supervisor-menu path 10** — Soft Reboot landing screen (Idle vs. the Driver Menu's own Soft
   Reboot landing on "On Break") is asserted nowhere, despite this flow-map's own notes flagging it
   as the one behaviour worth double-checking.
4. **driver-signon paths 13/14** — the entire scheduled Journey-Selection + Manual-Override branch is
   untested.
5. **flu-ticket-issue path 9 / barcode-scanning path 1** — fragmented, logged to
   `consolidation-audit.md`, not authored over.

## Escalated to `gap-register.md` (15 items)
Flow-map rows that are themselves unresolved source-transcription gaps or unconfirmed device
behaviour — see the register for the full table. Route through `/resolve-gaps` before authoring
against any of these. Notably **row 15** (regression-register's two NEEDS GEORGE defects, 301937 and
301828, carry no topic detail) was independently flagged by 9 separate flow-map passes as "can't rule
out overlap" — resolving it unblocks confidence across most of the suite, not just one area.

## Regression-register guard rail
Confirmed: neither `301937` nor `301828` (the two open NEEDS GEORGE rows) was touched, edited, or
had its Refs/status changed by this pass. Both remain exactly as they were, flagged in multiple
per-area findings above as unconfirmed-overlap risk pending George's input.

## Suite audit status
Not yet re-run — no cases were added, edited, or pushed in this pass (write-back was flow-map-file-
only, per the user's chosen "consolidate + pause before authoring" option). `python -m system_test_ops
audit --suite 30254` should still read CLEAN, since no TestRail data changed.

## Next step (not yet done — awaiting go-ahead)
Dispatch **gherkin-author** for the ADD items (missing paths) and EDIT items (partial paths worth
strengthening, prioritised by the highest-risk list above), grounded strictly in each flow-map's
screen states/notes. Then **standards-keeper** review. Then a human runs `push --commit`. The 2
fragmented paths and 15 gap-register items are explicitly NOT authoring targets yet.

## Artefacts
- `cases.json` — `reports/tfts-system-test/new-etm-acceptance-suite/2026-08-05/cases.json`
- `proposals/etm-suite-restructure/consolidation-audit.md`
- `proposals/etm-suite-restructure/gap-register.md`
- All 16 `knowledge/flows/translink-etm-*.md` files (Covered-by columns now filled)
