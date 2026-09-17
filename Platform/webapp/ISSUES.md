# Test-Ops Console — issues & feedback (v3)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`

**How to use:** drop a new entry under whichever section you're testing, using this template.
I'll read this file directly, fix what I can, and mark items `Status: fixed`/`answered` with a
one-line note (and commit, once committed).

```
### Short title
**Type:** Bug / UX / UI / Change request
**Severity:** blocker / annoying / nice-to-have / Q+A
**What happened / what you want:** ...
**Expected:** ...
**Status:** open
```

---

## Questions still to do (carried over, not yet resolved)

- **Manual vs. automation coverage %** — blocked on real prerequisite work: TestRail case ↔
  `.robot` test linkage is free-text today (inside a `Documentation` field), not a structured
  tag, and inconsistent across suites. Needs that parsed properly first.
- **Manual-edit-only "observed changes" scoping** — needs either TestRail's `updated_by`/
  `updated_on` per case (not available on the bulk snapshot call `build-stats` uses today), or
  this tool tagging its own pushes so they can be excluded from the diff.
- **Review/approve manual edits inline** — depends on the item above existing first; nothing to
  review/tick yet.
- **Docs ingest status — per-document breakdown** — suite-level last-ingested + pass/fail is
  real now; which *specific file* passed/failed within a run still isn't tracked anywhere.
- **Existing-suite mode needs its own toolset** — real governance decision, not mine to make
  silently: today's `fresh_build` flag only distinguishes "no old suite" from "has one," it
  doesn't model a genuine "just work in this existing suite, skip onboarding" mode (which would
  also let New-suite-from-docs show a real "you're targeting an existing suite, skip this"
  warning). Flag if you want it prioritized.
- **Test provenance — manual vs. Claude-written** — repo/folder/project is already shown per
  test. Whether a test was hand-written vs. generated has no reliable signal to build from today
  (Claude's commits land under George's own git identity) — would need this tool tagging its own
  generated files at write time.

---

*(Fresh sheet — nothing else logged yet.)*

- Arrive logo and Test ops console title to be centre of top left of page - aligned centrally one after the other
- Can we make the parent level sidebar menu options (i.e. overview for example) pills, or tabs? with clearer arrows for the accordion? so its more obvious to open and close
- Lets rename the side bar menu stuff to be more clearer 
-- Overview to be Dashboards
-- All processed to be Processes & Flows
-- Features to be Knowledge & Feature Files
-- Repo map to be Repo structure & map
- Real work? can we make Gap Register a whole parent menu item - and have it re-worked so it has a Project GAPs, Device GAPs, Common GAPs and Bespoke GAPs
- We then need to ensure we map the right GAP questions to the correct place, if i was to change target to Translink POS and Translink ETM then the Project GAPS will remain, but device GAps will differ right, so forth
- Start to be changed to Get Started
-- Change Start to Check setup
- Change build to Tools
- Onboard suite to New Suite Onboarding
- New suite from docs no need really?
- Add Feature to Onboard New JIRA
- Consolidate to Check Duplication
- exportat automaton to Automation Hand Off
- write automation to Write Automated Test Cases
- Audit (title) to be changed to Audit Coverage vs Release
- Audit flows to Audit flow maps 
- Question on audit flows, what is it auditing? a uploaded doc? or the sit flows? 
- Audit to be changed to Audit Syntax
- resolve gaps to be moved as a button in gap register, but also move to maintain i think
- Maintain to be changed to maintenance
- fold defect to be changed to Defect Steps to Case
- Review runs to review latest run comments
- Maintain to change to Health Check

Suite Health
- (this can be a global change on all pages) lets keep title of pages the same, but the like mini info beneath, the warning, the generated time and date of this suite, and any cool ideas, in like little pills to the right of the title so it looks cooler. bringing up the page a bit more closer to the title but enough gap to be tidy.
- probably need a button on most of the dasboard items here, so you can comfortable do a like sync, and just quickly sync the old vs new if any changes, run comments, recentl activity, etc. make this buttons the arrive colours
- organise the components on the dashboard so it fits better, not so gappy

Processes & Flows
- processes and flows should be updated as we improve our process, keeping it up to date with new things ocming in, like flow updates and stuff.
- parent level how to get started to be arrive purple, and open an accordion of not pills but the same dropdown white background, with then start and other things in a seperate pill to click on, maybe number them so its more clear on what to do first, 2nd then 3rd.
- new suite from docs is just a human process right no need, just get rid of entirely.
- Flows look fine tbh

Features
- The layour for this page is pretty bad. its like all pills, then content? and not ordered or structured nicely, just tap a card, then another functions - do we think this could be bettered structured like a tree, like following the flows of devices, and structure of test rail suites, like Communication, signing on, ticket purchasing, like more broad titles and features underneath, how can we imrpove this for UI/UX
- Gaps found should be able to switch with a filter between the targeted project, device, comon and bespoke as well (or tbf no need for it if were gonna make a whole menu section for it instead)
- Maybe we should be able to filter through Common features, and Bespoke (but bespoke only works if you have a project or device selected, maybe it should be filtered toggle tabs like toggle common, or bespoke, or device only, project only
- Just layout needs massive rethinking

Repo map
- Same here, layout is weird, could we do a similar layout to how github actually shows the files? and we can click into a folder to the see the files type thing?

Gap register
- As mentioned above do those changes
- Needs real work
- Want to click on a gap item. and a pop up show with a explanantion of the gap, and for me to answer the gap questions with all the form tools available to help give the best answer.
- This page needs a sync button somewhere to ensure once questions and gaps are answered you can syn them to claude, and this then should be a pipeline right, we should be able to re-audit and edit the existing cases from the gaps answered.
- Maybe just a sync button at the top to sync and audit the suite, and make sure any gaps now answered gets added to steps needed or tests written

Start