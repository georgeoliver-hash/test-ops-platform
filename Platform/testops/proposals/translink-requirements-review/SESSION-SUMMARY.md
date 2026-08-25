# Session summary — requirements ingestion, cross-examination & Phase-6 coverage

Covers 2026-07-13 → 2026-07-16. Everything done, with adds / edits / removes.
Companion to `register.md` (questions/blockers/findings) and `gaps-*.md` (per-suite gaps).

## 1. TestRail changes (the actual suites) — ADDS

**82 new cases** authored requirement-grounded, pushed, **audit-CLEAN**, and enriched (priority +
manual/automation estimate + Automatable marker). No existing cases were edited or deleted.

| Suite | New cases | Case ids | Areas |
|---|---|---|---|
| BOS & ABT 30279 | 16 | C4103473–488 | Daily Capping, Correction Limits, Late Taps (UB-TOO cross-check) |
| BOS & ABT 30279 | 16 | C4103583–598 | NIR TOTO, Capping timing, Shift Board, Access & Claims |
| POS 30253 | 12 | C4103533–544 | Refund (cash/card/role/audit/finality/CR115) |
| POS 30253 | 13 | C4103570–582 | Barcode scoping/audit, Fare-Stage display, Heartbeat, Revenue allocation |
| ETM 30254 | 14 | C4103545–558 | Rail Substitution, Shift Board, Legacy transfer, ABT audit |
| PV 30255 | 11 | C4103559–569 | Barcode reject(+multi-use), Pilot list, TOTO audit, Comms-lock |

## 2. Repo ADDS (committed — awaiting your push)
- `knowledge/translink/specs/` — **59 distilled requirement-spec notes** (FBD-#####), cited, each
  with a "Suite implications" gap list. (Namespaced `knowledge/<project>/` for multi-project.)
- `tools/ingest_docs.py` + `.claude/commands/ingest-docs.md` — reusable, project-agnostic docs→
  knowledge pipeline (dedupe/convert/distil → PR).
- `docs/overview.md` — the unified "one tool" overview (Confluence-ready).
- `docs/start-example.md` — `/start` worked-example walkthrough.
- `proposals/translink-requirements-review/` — `register.md`, `gaps-{pos,etm,pv,bos-abt}.md`,
  this summary.
- `proposals/*/requirements-additions.cases.yaml` (+ POS `refund.cases.yaml`) — the push specs.
- `proposals/automation-generation-prototype/` — Robot Framework step-7 POC.
- `.gitattributes`, top-level `README.md` (front door), `proposals/README.md` (navigation).

## 3. EDITS
- `docs/gherkin-standard.md` — new **"Concrete grounding"** rule: cases that depend on routes/
  operators/stops/products/config must carry a concrete worked example in preconditions.
- `docs/overview.md` — rebuilt as the one-tool process (menu of steps, Live/Roadmap), + grounding-
  inputs table + per-case estimates.
- `README.md` — refreshed as a current front door.
- Claude memory — session state recorded.
- `.env` (local, NOT committed) — TestRail URL → `http://10.120.54.19/testrail`; AD password updated.

## 4. REMOVES / ARCHIVED (history preserved via git mv — nothing destroyed)
- `tools/archive/` ← one-shot scripts: consolidate_pos, fix_consolidation, fix_refs, wave2_edits,
  _enrich_diff, and the empty audit_suite.py shim. (8 reusable tools kept.)
- `proposals/*/archive/` ← 17 spent working intermediates (refine-*, sweep-*, wave2-*, _scaffold,
  consolidate-keepers, working *-audit.md): POS 15, ETM 2.
- Nothing removed from TestRail. (ZZ_DELETE bin is your UI step — see §6.)

## 5. Commits (local — push via GitHub Desktop)
```
1dc776b Repo tidy: README, .gitattributes, proposals guide, archive tools + intermediates
2642e73 Phase 6: additive coverage across POS/ETM/PV/BOS-ABT (66 cases) + register
7d36745 Phase 6 pilot: POS Refund (12 cases, FBD-100373) + register
ae8a96d Concrete-grounding standard rule, review register, 4 cross-examination gap reports
cb2344c Distilled Translink requirement specs (59 notes), ingest tool + /ingest-docs command
c9417eb docs: /start worked-example walkthrough
ba4ac0d one-tool overview, ABT capping-gap cross-check + 16 cases, RF automation POC
```
(`32f313e` overview update was already pushed.)

## 6. Existing cases FLAGGED for you (verify / ZZ_DELETE) — NOT edited
| Case | Suite | Issue |
|---|---|---|
| C4101005 | PV | Asserts single-use *validates* — spec says reject → ZZ_DELETE (superseded) |
| C4100439 / C4100440 | POS | Generic/overstated barcode cases → verify vs body, supersede |
| C4102954 | BOS-ABT | "Add new decline reasons" omits Passback (15=BIN/20=Passback) |
| C4100583 / C4100591 | ETM | ABT declined/invalid-tap may assert pre-alignment codes |
| C4103487 | BOS-ABT | Late-tap-after-settlement: date-split + "Late Tap" flag not asserted |

## 7. Outstanding — your hand-offs & the open questions
- **Push** the 7 commits (GitHub Desktop).
- **Answer the open questions** (register B1–B3): which barcode flow ships (old vs CR094 REST API),
  Declined-Reason values, CR statuses (CR094/105.x/115/116/122/123/134) — needed before editing the
  flagged existing cases.
- **Bin the flagged ZZ_DELETE** cases in the UI (after the fixes).
- **TVM:** pick the source suite(s) + create the `**NEW** TVM` target (candidates sized in the
  register/chat: 5602 baseline, 6160 R2, or the active Kiosk/Astreo set 22270–22279).
- **Blocked devices:** BV (FBD-100391 empty stub) and GV/Gates (FBD-100348 "validate on
  integration") — need real specs before a suite.
- **Harden:** NIR TOTO exact fares/PJT values (need the FBD-100450 NIR bespoke-fares export).
- **Feed** epics/sprints/fix+affected versions for JIRA coverage audits.

## 8. Governance (unchanged, honoured throughout)
Raw requirement docs (~11 GB) stay LOCAL in `dev/translink-requirements/` — **never committed**.
Only distilled knowledge + specs reach the repo. Verified no PANs/secrets committed.
