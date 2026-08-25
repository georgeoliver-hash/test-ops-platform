# HHD correctness sense-check — confirmed issues + fixes (2026-08-06)

Combined coverage + correctness pass across all 20 HHD flow-maps against suite 30285 (338 cases).
This run had the ETM/POS false-positive lesson baked into the prompts (check `gap-register.md` and
the case's own `refs` for a cited alternate source before flagging anything) — result: only 9
potential issues flagged, 6 confirmed, all 6 real. No false positives this time.

## Fixed and live (6 cases)

| Case | Fix |
|---|---|
| C4103890 | Top-Up annul-and-cash-refund was asserted as flat fact; the mechanism is still an open gap-register question (Q60) — marked `**UNCONFIRMED**` instead of asserting it |
| C4103917 | Mini Statement wrongly claimed to "summarise the duty's totals" — that's the separate View Totals function. Rewritten to the actual documented smartcard-status content (card type, ESN/PSN, card ref, dates, journeys/days left, usage/top-up times) |
| C4103924 | "Supervisor — act as Operator" already had a GAP marker in its preconditions (no source confirms this feature exists at all, per gap-register Q50) but the steps still read as confident fact. Reinforced the UNCONFIRMED marker in the summary too |
| C4103934 | Genuine **new conflict** — the case's citation (FBD-100320: automatic serial-based TID/TK allocation) and the flow-map (high-confidence, verbatim 5-screen manual keypad entry) describe two different mechanisms for the same feature. Neither guessed at — marked UNCONFIRMED, logged as **gap-register Q62** |
| C4103975, C4103976 | Title-only fix: both used "passback window", but the flow-map has a *separate*, always-rejecting "Passback" decision distinct from the countdown-timer/transfer-period mechanism these cases actually test (confirmed via gap-register Q55 + REQ-3488.0). Renamed to "transfer period" — the case bodies already used generic wording, only the titles clashed |

## Note on back-office (CloudFare/MERIT/SmartTrack) assertions
None of these 6 fixes removed a back-office assertion just because a flow-map didn't mention it — flow-
maps only capture the UI/screen layer by design and were never the bar for that judgment. The one
back-office-related fix (C4103890) is UNCONFIRMED because gap-register Q60 is explicitly open, not
because the flow-map is silent on it.

## Not yet actioned
`coverage_by_flowmap` (missing/partial paths, notably the two Card-Error-during-unlock gaps on the
Login flow-map, and the entirely-untested Test Printer step during sign-on) not yet written back to
the 20 HHD flow-maps' `Covered by` columns — same follow-up as ETM/POS.
