# knowledge/flows/ — machine-readable mirrors of the Overflow user flows

Overflow has no API/MCP, so we **bridge by export**. Two ways to do this, either is fine:

1. **PDF/PNG export** — export a flow from Overflow to PDF (or PNG-per-board) and drop it in this
   folder; Claude transcribes it **once** into a structured `<project>-<device>.md` flow map
   (Mermaid diagram + explicit path list).
2. **Browser-extension transcription (preferred for large/annotated diagrams)** — open the flow in
   Overflow with the Claude Chrome extension, ask it to transcribe (not summarize) every board:
   screen names verbatim, every annotation/spec-note's exact text, decision points, and the
   screen-to-screen connections including what action triggers each one. Paste the result as a
   `.md` file into this folder (e.g. `<project>-<device>-full-transcription-<version>.md`) — this
   is the **raw source**, same role as the PDF. See "Getting a transcription via the Chrome
   extension" below for the exact ask. This scales far better than screenshots once a diagram has
   many small text annotations, which is most of them.

Either way, Claude then transcribes the raw source **once** into a structured `<project>-<device>.md`
flow map (Mermaid diagram + explicit path list). The agents read the structured markdown, not the
raw picture or the raw transcription dump.

## Getting a transcription via the Chrome extension

Open the Overflow flow in a browser with the Claude Chrome extension, and ask it to **transcribe,
not summarize** — paraphrased text is exactly the "lossy summary" this repo's `knowledge/` rules
warn against. Ask it to capture, per board:
- Every screen/node name, verbatim.
- Every annotation/spec-note's exact text (not a description of it).
- Every decision point.
- Every connection — which screen leads to which, and what action/condition triggers it.
- Any labelled values (thresholds, field names, error messages) exactly as written.

Paste the output here as a raw `.md` file. This has already been done once for Translink POS
(`translink-pos-full-transcription-v4.0.3.md`, 2026-08-04, all 17 boards) and worked well — it both
confirmed and *resolved open questions* in the existing hand-transcribed `translink-pos-signon.md`
(e.g. confirming Communication Locked is reached from Idle, not from a failed sign-on submit).

Overflow stays the design source of truth. These files are the derived, version-controlled mirror —
same idea as the rest of `knowledge/`. When a flow changes in Overflow, re-export the PDF and ask
Claude to re-sync the map.

## Behaviour notes (authoritative)

- `overflow_data.json` — the full Overflow document (export of the share). Source of truth.
- `flow-annotations.md` — the **annotation notes** extracted per flow from that JSON (540 notes).
  These are the design behaviour spec (preconditions, rules, configurable thresholds, printout
  contents, error handling). `gherkin-author` and `coverage-analyst` should **ground cases in these
  notes** — they often state behaviour the screen images alone don't show. Regenerate from the JSON
  if the Overflow doc is re-exported.

## Files here

- `<project>-<device>.pdf` — the raw Overflow export (human reference; the input for transcription).
- `<project>-<device>.md` — the transcribed flow map the agents consume (see template below).

## How the agents use it

- **coverage-analyst** overlays a JIRA fix version onto the **paths** and flags branches with no
  TestRail case → coverage gaps you can see at a glance.
- **gherkin-author** turns each uncovered path into a Gherkin scenario in the standard.

## Template for a transcribed flow map

```markdown
# Flow: <Project> <Device> — <flow name>

- Source: knowledge/flows/<file>.pdf  (Overflow export, <YYYY-MM-DD>)
- Project: <name>   Device: <POS|TVM|BV|…>   Feature: <area>
- Transcription confidence: <high|medium|low> — <note any labels that were unclear>

## Diagram
\`\`\`mermaid
flowchart TD
  A[Sign-off screen] -->|valid ID+PIN| B[Main menu]
  A -->|invalid ID+PIN| C[Sign On Failed dialog]
  C -->|dismiss| A
\`\`\`

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Sign-off → valid ID+PIN → Main menu | auth | @bos | ? |
| 2 | Sign-off → invalid ID+PIN → Sign On Failed → dismiss → Sign-off | auth | @destructive | ? |

## Screen states (Given/Then anchors)
- **Sign-off screen** — shows "ID" and "PIN" labels.
- **Main menu** — …
- **Sign On Failed dialog** — …

## Notes / unknowns
- TODO: confirm <anything the export didn't make clear>.
```

> Keep the `Covered by` column as `?` at transcription time — `coverage-analyst` fills it in against
> the live TestRail `cases.json`. Never invent screen names or audit events; if the export is
> unclear, leave a `TODO: confirm …` rather than guessing.

## Filling in `Covered by`

Transcription alone never resolves `?` → a real case id — that's a separate, later step. Run
**`/audit-flows <project> <device> <suite-id>`** once a device's flow-maps are structured: it globs
every `knowledge/flows/<project>-<device>-*.md` file (excluding the raw `*-full-transcription-*.md`
source), dispatches `coverage-analyst` per flow-map against the live suite, and writes the resulting
case ids (or an explicit gap/defer pointer) back into each `Covered by` cell. See
`.claude/commands/audit-flows.md`.
