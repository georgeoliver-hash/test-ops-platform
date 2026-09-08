# Case drafts — Translink POS, fix version TL_POS_3.0.0

Target suite: `GG - POS - Claude Suite` (id 30253). All drafts below are proposals only — nothing
here has been pushed. Grouped by feature area per the gap list handed off by `coverage-analyst`.

---

## Sign On (auth)

## DRAFT — ADD — closes TIBU-31553

```
Title: Sign On — Ulsterbus reaches the signed-on landing screen without hanging on the loading screen
Tags: @project(translink) @device(POS) @mode(Ulsterbus) @feature(auth) @regression

Given the POS is signed off, in Ulsterbus mode, and showing the sign-on screen
  And a valid operator's seeded credentials are available
When the operator signs on with the seeded ID and PIN
Then the "Please Wait..." screen is shown only transiently
  And the operator reaches the signed-on landing screen without hanging

Refs: TIBU-31553
```

Basis: `knowledge/flows/translink-pos-signon.md` (screen `1_2_2 Please Wait...`; the open question
under "Confirm against Overflow" noting the Rail/Metro post-sign-on branch is resolved but no
Ulsterbus branch is confirmed). No existing case in any of the sign-on flow-map paths (1–9) or the
old-suite audit covers a stuck/hung loading screen for any mode — this is genuinely `MISSING`, not a
duplicate. Tagged `@mode(Ulsterbus)` rather than `@mode(all)` specifically because the flow map does
**not** confirm the Ulsterbus post-sign-on landing screen behaves like Rail's — claiming `@mode(all)`
would assert a genericity that isn't grounded.

**GAP** — the Ulsterbus signed-on landing screen reached after "Please Wait..." is not confirmed in
`translink-pos-signon.md` (only Rail → Main Screen and Metro → Present Smartcard are confirmed for
the post-sign-on branch; no Ulsterbus branch is documented there) — confirm the exact screen name on
the live system before running. Both this case's title and Then now use the same generic term,
"signed-on landing screen," rather than asserting an unconfirmed screen name.

Note (assumed-knowledge, not a GAP) — the "Please Wait..." duration is an unknown **configured**
value, not an unknown behaviour: `knowledge/projects/translink.md` already documents that lockout/
sign-off timeouts on this device are configurable, not hard-coded, and the same applies here. The
case deliberately asserts "shown only transiently"/"without hanging" rather than any specific number
of seconds, so no threshold needs confirming before this case can run.

This `**GAP**` marker should be routed through the gap-register Q&A loop (see
`proposals/pos-suite-restructure/gap-register.md`, new Q1 below) before this case is finalised for
push.

---

## Operator Menu — Excess Ticket

## DRAFT — ADD-PARTIAL — closes TIBU-24804 (conflict flagged — see Basis)

```
Title: Excess Ticket — available (Ulsterbus)
Tags: @project(translink) @device(POS) @mode(Ulsterbus) @feature(transactions) @regression

Given an operator is signed on with the POS in Ulsterbus mode
When the operator opens the Operator menu
Then the Excess Ticket feature is available
  And the corresponding event is recorded in the Back Office System (CloudFare) activity log
  And the transaction appears in MERIT

Refs: TIBU-24804 **UNCONFIRMED — pending JIRA mode re-check, conflicts with gap-register Q26**
```

Basis / **CONFLICT — flag before pushing**: this case mirrors existing `C4099946` ("Excess Ticket —
available (rail)") structurally — including its two audit-verification steps, not just its first
step — per the task brief's classification of TIBU-24804 as an Ulsterbus Operator Menu defect. The
CloudFare activity-log and MERIT steps above are copied verbatim from `C4099946`'s own stored body
(`proposals/coherence-audit/fixes/pos-suite-30253-raw.json`, id 4099946: "**WHEN** the CloudFare
activity log is checked / **THEN** the corresponding event is recorded in the Back Office System
(CloudFare) activity log" and "**WHEN** the data is reviewed in MERIT / **THEN** the transaction
appears in MERIT"), re-cast as Given/When/Then `And` clauses against the single Ulsterbus outcome
already asserted — this repo has no `event-catalogue.md` yet (see `knowledge/bos/README.md`) naming
a specific CloudFare event for Excess Ticket, so the wording stays exactly as generic as the sibling
case's own grounded text, not tightened into an invented event name. However, the repo's own gap
register already answered a question about this exact defect
(`proposals/coherence-audit/gap-register.md`, session "2026-07-21/22 POS deep-audit", **Q26**): it
cites old-suite case **C4078764**, titled *"TIBU-24804: TL POS Rail- Operator Menu- Excess Ticket
Feature doesnt exist"* — i.e. the locally-held evidence says TIBU-24804 is a **Rail** defect, not
Ulsterbus. `proposals/pos-suite-restructure/bug-regression-register.md` line 104 agrees ("TL POS
Rail- Operator Menu- Excess Ticket Feature doesnt exist"). The `Refs` line above carries this
conflict explicitly (`**UNCONFIRMED**`) so the marker travels with the pushable case text itself,
not only with this surrounding commentary.

This is a direct conflict between the task brief and the repo's cited, already-answered evidence. Per
CLAUDE.md's no-invention rule, I have **not** silently trusted either side — the Ulsterbus case above
is drafted as requested, but is marked here as **UNCONFIRMED pending a re-check of the live JIRA
ticket TIBU-24804** (which mode(s) it actually names) before push. See new gap-register question Q2
below. **Do not remove Refs from C4099946** until that re-check confirms which mode(s) the bug
actually covers — removing a correct Refs pin on a guess would be worse than leaving a possibly-loose
one. If TIBU-24804 is confirmed Rail-only, this Ulsterbus draft should be re-filed under whatever the
correct Ulsterbus-side defect key turns out to be (if one exists), not TIBU-24804.

---

## Barcode (bus ticket printing)

## DRAFT — ADD-PARTIAL — closes TIBU-28350

```
Title: Barcode — print barcode (Ulsterbus ticket)
Tags: @project(translink) @device(POS) @mode(Ulsterbus) @feature(printing) @regression

Given an operator is signed on to the POS in Ulsterbus mode at the FLU screen
  And a valid single-use bus barcode ticket is available for presentation
When the operator presents the ticket to the barcode reader
Then the ticket passes validation and visual inspection
  And a scannable barcode is printed on the issued ticket
  And the POS returns to the FLU screen with the barcode marked validated

Refs: TIBU-28350
```

Basis: `knowledge/flows/translink-pos-barcode-scanning.md` — the entire barcode-scan/validate/print
flow is entered **from the Ulsterbus FLU screen** (`2.5.2 Main Screen-Ulsterbus selected`), and its
paths 11/12 ("Ticket Valid → Online?  → POS attempts print → Print successful → Printed?") are the
grounding for the print step and the "returns to FLU, barcode validated" outcome. This is deliberately
**not** a straight copy of existing case `C4100034` ("Barcode — print barcode"): that case's actual
stored body (`proposals/coherence-audit/fixes/pos-suite-30253-raw.json`, id 4100034) uses a **Rail**
worked example ("a Rail Adult Single... paid by cash") and carries Refs `TIBU-13180`, a different
defect. `proposals/pos-suite-restructure/mode-coverage.md` already flags the whole
barcode-print/scan/validate family (including C4100034) as tagged `MODE-NIR-ONLY` on **grounded
inference only, not a stated exclusion** — "flagged for engineer confirmation, not asserted as
certain." Given the barcode-scan entry point in the flow map is the Ulsterbus FLU screen, that
NIR-only inference looks questionable on its own evidence.

**Recommendation:** do not edit `C4100034` in place (its Rail worked example and TIBU-13180 pin are
still valid for Rail). Instead **ADD** the new Ulsterbus-specific case above, and separately raise the
`mode-coverage.md` NIR-only classification of the barcode family for re-confirmation — see gap-register
Q3 below, since a bus-specific bug (TIBU-28350) existing at all is evidence bus tickets *can* carry
barcodes, which the current MODE-NIR-ONLY tag doesn't account for.

**GAP** — the specific bus ticket product/type that carries a barcode is not named in
`translink-pos-flu-bus.md` or `translink-pos-barcode-scanning.md` (barcode ticket types B/U/E/S/D/H
are only confirmed against Rail worked examples per `mode-coverage.md`) — confirm which Ulsterbus
ticket product(s) are configured to carry a barcode before running this case, and cite it once known.

---

## Ticket Editor Integration — placeholder only

## DRAFT — none authored — closes TIBU-28211 (blocked, logged as a gap, not a case)

No case is drafted for TIBU-28211. `coverage-analyst` could not retrieve this epic's child issues
from JIRA (Atlassian MCP permission error), so there is no acceptance criteria to test against. The
only local grounding available is `knowledge/translink/specs/FBD-100363-ticket-editor.md`, which
describes the **Ticket Editor tool itself** (a CloudFare back-office template builder for
ETM/HHD/POS/TVM) — it does not describe what "integration with POS" means as a testable behaviour
(e.g. whether it's about template push/sync to device, print-time application of a published
template, or something else). Per CLAUDE.md's "never invent device behaviour" rule, writing a case
here would mean fabricating the acceptance criteria wholesale. Logged instead as gap-register Q4
below, requesting the epic's child stories before authoring proceeds.

---

## Fare-Stage / CR113 — no draft, routed to gap register only

## DRAFT — none authored — closes TIBU-28051 (routed to gap register, not drafted)

No new case is drafted for TIBU-28051 (CR113 Bus Stop Boarding Stage Grouping). Existing cases
`C4103578`/`C4103579`/`C4103580` (Refs `FBD-100207`, Fare-Stage Selection family) plausibly already
cover the behaviour, but it is unconfirmed whether CR113 introduces anything beyond what FBD-100207
already specifies. Per the "do we need a new test?" rubric (`docs/test-practices.md` step 1), writing
a new case before confirming that would risk an untraceable duplicate. Logged as gap-register Q5
below for the engineer to confirm scope before any case is added, edited, or left as-is.

---

## Summary of Refs / cross-references

| Gap | Action | New/edited case | Refs | Cross-references |
|---|---|---|---|---|
| TIBU-31553 | ADD | "Sign On — Ulsterbus reaches the signed-on landing screen without hanging on the loading screen" | TIBU-31553 | None found anywhere in suite/old-suite; genuinely new. |
| TIBU-24804 | ADD-PARTIAL (conflict flagged) | "Excess Ticket — available (Ulsterbus)" | TIBU-24804 (UNCONFIRMED pending JIRA re-check) | Cross-ref `C4099946` (rail case, kept as-is); old-suite `C4078764`; gap-register Q26 (already answered, conflicts with this task's premise). |
| TIBU-28350 | ADD-PARTIAL | "Barcode — print barcode (Ulsterbus ticket)" | TIBU-28350 | Cross-ref `C4100034` (rail case, Refs `TIBU-13180`, left as-is); `mode-coverage.md` NIR-only flag on the barcode family (flagged for re-confirmation). |
| TIBU-28211 | none (placeholder logged) | — | TIBU-28211 | `FBD-100363-ticket-editor.md` (tool spec only, not integration behaviour); gap-register Q4. |
| TIBU-28051 | none (gap register only) | — | TIBU-28051 | `C4103578`/`C4103579`/`C4103580` (Refs `FBD-100207`); gap-register Q5. |
