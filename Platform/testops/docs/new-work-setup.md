# Starting new work — a new project, device, suite, or bug backlog

This is the repeatable playbook for **any** test engineer picking up **any** device or project. The
tooling is project-agnostic; everything project-specific is just a few files you add under
`knowledge/`. Follow the steps that apply — you rarely need all of them at once.

> First time on this machine? Do the one-time setup in [`getting-started.md`](getting-started.md)
> (install, TestRail `.env`, connect the JIRA/Atlassian MCP) before the steps below.

## What you must provide first (or the agents are guessing)

This work is **audit-first** (see `test-practices.md`): the agents prove what is shared/specific/
covered from real evidence. **The quality of the help is capped by the inputs you give.** Without
these, the agents guess — and guessing *hinders* a live test suite. Bring as many as exist, up front:

| Input | Why it's needed | How to provide |
|---|---|---|
| **Old TestRail suite** (source) + the **new/target** suite | The baseline to mine and consolidate; the cross-tab that proves shared vs mode-specific | TestRail access (API key) + the suite names/ids |
| **Requirements / specs** (e.g. REQ-####) | Trace each case to a requirement; judge "covered vs stale" | The docs/specs, or links/IDs the cases reference |
| **UX / design flows** (e.g. Overflow) | The behaviour spec: preconditions, rules, thresholds, error handling, screens | **Preferred:** the Claude Chrome extension transcribing the flow verbatim (scales to large, densely-annotated diagrams). Or a PDF/PNG export. Either way → `knowledge/flows/` |
| **Defect / bug history** (e.g. the TIBU tracker) | Pin every fixed bug as regression coverage; build the bug register | Where defects live + which suite section holds the regression/"confirmation" tests |
| **Device knowledge** | On-screen wording, operating modes, payment methods, terminology | A short brief, or point at a sibling automation repo / glossary |
| **Links** | Dashboards, share links, ticket boards, design links | Paste them into the project knowledge file |

Rule of thumb: **documentation + design docs + images + links + specs + requirements + the old
suite/cases** = enough to do real test-maintenance well. Missing several of these? Say so, and the
agents will scope their confidence accordingly rather than inventing coverage.

## A. Onboard a new PROJECT
1. Copy the template: `knowledge/projects/_TEMPLATE.md` → `knowledge/projects/<project>.md`.
2. Fill it in: TestRail **project id**, the **suites** (old/source + new/target), the **defect
   tracker** prefix (e.g. `TIBU-`), the **requirement** ref prefix (e.g. `REQ-`), any **operating
   modes/configurations**, and what "covered" means for this project.
3. Confirm access: `python -m system_test_ops check` (lists projects + ids).
4. **Discover the case schema** (required — differs per project/template):
   `python -m system_test_ops discover-fields --project <id> --sample-case <an existing case id>`.
   It lists the REQUIRED case fields and prints a ready-to-paste **`defaults:`** block (template_id +
   required custom fields) for the push YAMLs. The POS defaults (`template_id: 1`,
   `custom_devtypes: [5]`, `custom_steps_seperated`) are **project-specific** — do not reuse blindly.

## B. Onboard a new DEVICE
1. Copy `knowledge/devices/_TEMPLATE.md` → `knowledge/devices/<device>.md`.
2. Capture the device's behaviours, terminology/on-screen wording, feature areas, and the **source
   of truth** for facts (a sibling automation repo, a spec, the design files). The `gherkin-author`
   relies on this to stay grounded and never invent behaviour.
3. Add the device type to the `@device` list in `gherkin-standard.md` if it's new.

## C. Capture the UX flows
1. **Preferred:** open the flow in your browser with the **Claude Chrome extension** and ask it to
   transcribe every board verbatim — screen names, annotation/spec-note text, decision points, and
   connections (which screen leads to which, and what triggers it). Paste the result as a raw `.md`
   into `knowledge/flows/`. This scales far better than screenshots once a diagram has many small
   text annotations, which is most of them. See `knowledge/flows/README.md` for the exact ask.
2. **Alternative:** export the flows from your design tool (Overflow etc.) to images/PDF — screens
   **plus a zoomed-out overview** per flow (the overview shows the branches; that's the important one).
3. Drop each flow in its own folder under `knowledge/flows/` (keep the tool's own names; the numbers
   in screen names encode the branch hierarchy).
4. Ask Claude to transcribe each flow to a `<project>-<device>-<flow>.md` map (Mermaid + path list).
   Each path becomes a *candidate* scenario — not an automatic new case (apply the rubric).

## D. Pull what already exists (read-only)
- **Old suite cases:** `python -m system_test_ops cases --project <id> --suite "<old suite>"`
  → `cases.json` (the inventory + house Gherkin style to match).
- **Run history:** `python -m system_test_ops runs --project <id> --suite "<old suite>" --last 10`
  → flags always-failing / flaky / never-run / orphaned cases to retire rather than carry over.
- **Bug backlog:** find where past defects live (often a "Confirmation Tests"/regression section or
  defect-linked cases). Build the **bug-regression register** so every fixed bug is accounted for.

## E. Design the new suite (apply the practices)
1. Read [`test-practices.md`](test-practices.md) — the mindset for every add/edit/merge/fold/leave
   decision ("do we even need a new test?").
2. Structure **test-type-first** (Smoke / Functional / Non-Functional / Regression), features under
   Functional, mode-specific subsections **only** where behaviour genuinely diverges.
3. Map old → new: **copy-as-is / copy+rewrite / merge / split / leave** — into the new suite only;
   never edit or delete the old one.
4. **Fold each past defect** into the case that owns the behaviour (link via Refs); a dedicated
   `@regression` case only where nothing covers it.
5. Draft any genuinely new cases in the standard, `@mode(all)` unless they truly differ per mode.
6. Review with `standards-keeper`; then a human pastes/pushes the result into the new TestRail suite.
7. **Run the conformance audit — required, not optional.** `python -m system_test_ops audit
   --suite <id>` (`push --commit` runs it automatically). The suite is not done until it is **CLEAN
   of blocking findings**. This is part of the process for everyone, every time — see
   `test-practices.md` "Conformance audit". (Never rewrite the `*.cases.yaml` specs with PowerShell
   `Set-Content`/`Out-File` — it corrupts encoding and creates duplicate cases; the audit flags it.)
8. **Run the deep grounding + consolidation-completeness audit — also required, not a later cleanup.**
   A clean conformance audit only proves cases are *well-formed*, not that their claims are *true* or
   that the consolidation in step 3 kept everything genuinely distinct. Before calling a new suite
   done: (a) for every case, verify its claim against a real cited source (spec/old-suite/UX flow) —
   don't trust an existing citation without checking it actually supports the claim; (b) walk the old
   suite by family (card/product types, decline reasons, roles × sign-on methods × operating modes)
   and confirm every distinct member survived the fold somewhere (own case or a named
   `Data variations:` line) — write back in anything genuinely missing, grounded on the old case's
   real content, never invented; (c) check the live section tree against your own `structure.md` for
   drift. See `test-practices.md` "Deep grounding audit — beyond conformance" for the full method and
   the gap-register Q&A loop (exhaust old suite/spec/UX evidence before ever asking the engineer).

## F. Ongoing: prep a release & maintain
- Before a run: `/audit-coverage <project> <fix-version>` — covered/partial/missing/stale vs the
  release scope, citing case ids + requirement/defect refs.
- Across runs: `/review-runs <project> <suite> --last 10` — retire dead/flaky cases, keep the suite
  lean.
- Any time: `python -m system_test_ops audit --suite <id>` — re-check standard conformance (e.g.
  after manual UI tidies). Keep it clean; it's the suite's standing health check.

## What lives where (so a newcomer can navigate)
- `docs/` — `introduction`, `getting-started`, **`test-practices`** (the rules), `gherkin-standard`
  (how to write a case), this file.
- `knowledge/projects/<project>.md`, `knowledge/devices/<device>.md`, `knowledge/flows/…` — the only
  files that change per project/device. **No code change needed for a new project.**
- `proposals/<…>/` — per-suite restructure work (structure, drafts, bug register).
- `.claude/agents` + `.claude/commands` — the team and the two commands. Shared by everyone.
