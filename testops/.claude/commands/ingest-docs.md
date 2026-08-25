---
description: Ingest a project's requirement/design documents into distilled, cited knowledge. Point at a locally-synced folder of docs; produces knowledge/<project>/specs notes and a coverage gap-check. Usage: /ingest-docs <project> <path-to-docs>
argument-hint: <project> <path-to-local-docs-folder>
---

You are ingesting a project's **requirement/design documents** so the suite can be grounded in and
cross-examined against real requirements — for **any** project (Translink, Edinburgh Trams, …), not
just the first one. Documents are large and **confidential**, so they never enter the repo; only the
**distilled knowledge** does.

## The rule (governance)
- **Raw docs stay LOCAL** — in the project's synced Drive folder / working dir. **Never commit them.**
- **Only distilled `knowledge/<project>/specs/*.md` is committed** (facts + spec-id citations, no raw
  dumps, no PANs/secrets).
- Each project namespaces its knowledge under `knowledge/<project>/` so projects never collide.

## How a colleague gets the docs (no dependence on anyone's laptop)
The raw docs live in the project's **shared Drive** (SharePoint/Google Drive). Each engineer syncs
that folder locally (Google Drive for Desktop → "Available offline"), then runs this command against
that local path. The **repo** carries the distilled knowledge + this pointer; the **Drive** carries
the source. Contributing distilled knowledge back = a normal **PR**.

## Steps
1. **Prep (once):** ensure the docs are synced locally and the venv has the deps:
   `pip install python-docx openpyxl pypdf`.
2. **Convert:** run the deterministic ingest tool — it de-duplicates by version (keeps the latest),
   skips archive/video/CAD/Visio/milestone noise, and converts Word/Excel/PDF → plain text:
   ```
   python tools/ingest_docs.py --project <project> --src "<local docs folder>"
   ```
   Text lands in `dev/<project>-requirements/_text` (local). Read its reconciliation output — note
   what was **excluded** (images are readable on demand but not bulk-converted; flag key diagrams).
3. **Distil (your judgement):** for each current spec, read its `_text` file(s) and write a concise
   `knowledge/<project>/specs/<spec-id>-<slug>.md` — testable rules only, each citing the source
   spec + version, ending with a **"Suite implications"** gap list. Open the relevant **images**
   (screenshots/diagrams) directly when they carry behaviour the text doesn't. Follow the template of
   `knowledge/translink/specs/FBD-100167-multiple-use-barcodes.md`.
   - **Latest version wins**; note superseded/removed behaviour if it affects existing cases.
   - Never invent — if a fact isn't in the docs, say so.
4. **Cross-examine:** once an area's specs are distilled, re-audit the live suite against them
   (like the UB-TOO cross-check) — list covered / missing / stale / wrong, citing case ids + spec
   ids. Draft the gap cases; push per the normal build loop (`push --commit`, audit clean).
5. **Commit + PR** the new `knowledge/<project>/specs/*.md` (and any suite changes). That's how the
   knowledge reaches every colleague on that project.

## Incremental (new sprint docs)
Drop the new/updated docs into the project's synced folder and re-run — version-aware dedupe means
only new/changed specs are re-distilled. Then re-audit the affected area. No full re-read.

## Scale tip
For a large library, batch by area (barcode/ABT/CloudFare, Tap-On, cards, fares, devices, gates,
reporting). Distil an area, cross-examine, commit — then the next. The suite should end **fully
grounded in the current requirements**, with every gap either covered or logged.
