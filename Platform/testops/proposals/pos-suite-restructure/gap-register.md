# Gap Register & Q&A — POS suite restructure (coverage audit, TL_POS_3.0.0)

**Purpose.** Every gap the coverage audit found is a **question**, not a silent marker. Answer each
and the affected case-draft gets grounded + cited. Any question nobody can answer is flagged
**POSSIBLE DESIGN/SPEC BUG** and raised in JIRA. See `CLAUDE.md`'s "gaps trigger a Q&A loop" rule and
`.claude/commands/resolve-gaps.md`.

Legend: **SURFACE** (does this device/portal do this action?) · **LIVE?** (specified but is it
actually built/usable?) · **VALUE** (exact figure/threshold) · **CONFLICT** (two sources disagree —
which is right?) · **SCOPE** (does a CR add anything beyond what's already covered?).

---

**Q1 · VALUE · POS "Sign On — Ulsterbus reaches the main screen without hanging on the loading
screen" (closes TIBU-31553)** — OPEN
Two things are unconfirmed for this new draft case: (a) what screen an Ulsterbus operator actually
lands on after the "Please Wait..." transitional screen (the flow map only confirms Rail → Main
Screen and Metro → Present Smartcard); (b) whether there's a documented maximum/expected duration for
"Please Wait..." that should gate pass/fail, or whether "no hang" is the only assertable check.
A:
source: `knowledge/flows/translink-pos-signon.md` ("Confirm against Overflow" section, open Metro/Rail
branch note); no duration figure found anywhere in `knowledge/devices/pos.md` or the flow map.

---

**Q2 · CONFLICT · POS "Excess Ticket — available (Ulsterbus)" (TIBU-24804)** — OPEN
The coverage-audit task brief classifies TIBU-24804 as an **Ulsterbus** Operator Menu defect ("Excess
Ticket Feature" missing from the Ulsterbus Operator menu). But this repo's own, already-answered gap
register entry (`proposals/coherence-audit/gap-register.md`, session "2026-07-21/22 POS deep-audit
pass, suite 30253", **Q26**) cites old-suite case **C4078764**, titled *"TIBU-24804: TL POS Rail-
Operator Menu- Excess Ticket Feature doesnt exist"* — i.e. Rail, not Ulsterbus. The bug-regression
register (`proposals/pos-suite-restructure/bug-regression-register.md`, line 104) agrees: "TIBU-24804
| C4078764 | 2.0.X | TL POS Rail- Operator Menu- Excess Ticket Feature doesnt exist". Which is
correct — does TIBU-24804 (per the live JIRA ticket) actually name Rail, Ulsterbus, or both? This
determines whether the new Ulsterbus draft case should carry Refs TIBU-24804 at all, and whether
existing case `C4099946` ("Excess Ticket — available (rail)", also Refs TIBU-24804) needs anything
changed.
A:
source: `proposals/coherence-audit/gap-register.md` Q26 (ANSWERED, cites C4078764);
`proposals/pos-suite-restructure/bug-regression-register.md` line 104.

---

**Q3 · SCOPE/CONFLICT · Barcode print/scan/validate family mode classification (relates to
TIBU-28350)** — OPEN
`proposals/pos-suite-restructure/mode-coverage.md` tags the whole barcode-print/scan/validate case
family (including `C4100034` "Barcode — print barcode") `MODE-NIR-ONLY`, but flags this explicitly as
"grounded inference [from consistent Rail worked examples], not a stated exclusion... flagged for
engineer confirmation, not asserted as certain." Separately, `knowledge/flows/translink-pos-
barcode-scanning.md`'s entire scan flow is entered from the **Ulsterbus** FLU screen (`2.5.2 Main
Screen-Ulsterbus selected`), and a real defect (TIBU-28350) exists specifically about bus-ticket
barcode printing — which is evidence bus tickets *can* carry barcodes. Is the `MODE-NIR-ONLY` tag on
the barcode family correct, or should it be `MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY` (or similar)? This
affects whether the new "Barcode — print barcode (Ulsterbus ticket)" draft case is filling a genuine
mode gap or whether barcode printing was already meant to be shared.
A:
source: `proposals/pos-suite-restructure/mode-coverage.md` ("Flagged for engineer confirmation"
section); `knowledge/flows/translink-pos-barcode-scanning.md` (flow entry point).

---

**Q4 · SURFACE/SCOPE · Ticket Editor Integration with POS (TIBU-28211)** — OPEN
This epic has zero suite coverage and `coverage-analyst` could not pull its child issues from JIRA
(Atlassian MCP permission error). The only local grounding, `knowledge/translink/specs/FBD-100363-
ticket-editor.md`, describes the Ticket Editor tool itself (a CloudFare template builder covering
ETM/HHD/POS/TVM) but not what "integration with POS" means as a testable behaviour — e.g. is this
about template push/sync to the POS device, print-time application of a published template on POS,
device-side font/logo asset loading, or something else entirely? Please provide the epic's child
stories/acceptance criteria (or point at the right FBD/REQ) so a real case can be authored instead of
a placeholder.
A:
source: `knowledge/translink/specs/FBD-100363-ticket-editor.md` (tool spec, not integration AC).

---

**Q5 · SCOPE · Fare-Stage Selection vs CR113 Bus Stop Boarding Stage Grouping (TIBU-28051)** — OPEN
Existing cases `C4103578` ("...shows and prints the Fare Stage name, not the stop name"), `C4103579`
("...a zero-fare stage combination blocks ticket issue"), `C4103580` ("...reach a fare by keying the
Fare Stage ID") — all Refs `FBD-100207` — plausibly cover the ground CR113 is about, but nothing
locally confirms CR113 doesn't add new behaviour beyond FBD-100207 (e.g. a grouping/aggregation rule
across multiple boarding stages that the existing three cases don't exercise). Does CR113 introduce
anything beyond FBD-100207, or is it fully represented by the existing three cases? If it adds
something new, what is the new behaviour (concretely, so a case can be grounded rather than guessed)?
A:
source: `proposals/pos-suite-restructure/mode-coverage.md` line 98 (existing cases already flagged
there for a related, unresolved mode-classification question re: NIR fare-stage equivalence — same
case family, different open question).
