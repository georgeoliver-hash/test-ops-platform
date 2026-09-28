# Test-Ops Console — issues & feedback (v5)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`
- `archive/ISSUES-2026-09-28-resolved.md`

**How to use:** just drop raw bullet points below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## Carried forward, not yet resolved

- **Run-status conflation: "failed" vs "waiting on you"** — a run whose overall `status` is
  `waiting_human` can actually be sitting on a **failed** CLI step several steps past the last
  human gate (real example: run `a45a020d`, onboard-suite/Translink-POS — summary described a
  succeeded step 2 steps back while the actual stopping point, `push_area[FBD-100293-product-
  group-usage]`, had failed). Anyone reading the run card looks for a confirmation button that
  isn't there. Run-level status needs to distinguish these two states.
- **Raw traceback shown in the run card for failed CLI steps** — a `cli`-kind step failure
  renders the full Python traceback with no human-readable summary line above it. Fine for
  debugging, not fine as the primary thing a non-engineer reads. Worth a one-line "what broke"
  synthesis above the raw stderr.
- **No signal on whether a failed step is worth a plain Retry vs needs a real fix** — the
  `FBD-100293` YAML failure above turned out to be a real bug (fixed 2026-09-28 — see archived
  round), but a different failure on the same suite genuinely was transient/stale. Today there's
  no way to tell from the UI which kind you're looking at before you retry.
- **Silent, near-instant agent-step failures** — an **agent**-kind step (`cross_tab`, run
  `84d39936`) failed in under a second with `output: "(the agent returned no output)"` — no
  error, no partial output, nothing to diagnose from. Whatever captures the agent's result before
  writing `failed` has a real gap here.
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
  doesn't model a genuine "just work in this existing suite, skip onboarding" mode. Flag if you
  want it prioritized.
- **Test provenance — manual vs. Claude-written** — no reliable signal today (Claude's commits
  land under George's own git identity) — would need this tool tagging its own generated files.
- **Features layout — named conceptual-area taxonomy** (Communication/Signing on/Ticket
  purchasing) doesn't exist as a field in `Platform/model/features.py` today. Needs a real
  curated `area` field added (data-modelling decision) — flag if you want it scoped for real.
- **Gap Register sync → re-audit/re-edit pipeline** — needs the same pipeline-execution-from-
  console plumbing every disabled "Run" button is already waiting on.
- **4 pre-existing blocking `then-compound-genuine` audit findings on Translink/POS suite
  30253** (C4109983, C4109984, C4109989, C4110000) — flagged by the 2026-09-28 push's suite-wide
  conformance audit, unrelated to that push itself. Not split yet — want these done next?
- **`system-test-ops` working tree has uncommitted content** (multiple `knowledge/translink/
  specs/*.md` modified/deleted/added, plus the in-progress `proposals/Translink-POS-suite-
  restructure/` folder) — looks like output from more than one earlier pipeline run never got
  committed. Real content, not a code bug — flag before anything gets committed/pushed on top of
  it without a look first.

---

- Side bar menu, when closing it, theres a wierd overlay of text\? its like the paddling left or margin left of the text content just moves outside or rally close to the left side of the screen? should flow well when opening and closing.
- siebar menu would be cool to have icons for buttons that open up the sub menu options? when siebar is closed, compared to open does that make sense?
- think the projects menu option on automation is broken?
- can we deep dive the SIT view only dashboards, and content i think its not really up to do date? real reflection of what we actually have or is it purely based on the sit clone, pull we do?
- Can we change up the dashboard status page, can we mix in like line graphs, pie charts, other cool dashboard stuff into anywhere here? like use the data we have but make it look cooler? anything better we can add to like automation tests written by the tool? data etc
- Add a like confidence in coverage for the suite? maybe make the judgement based off gaps, and tests and specs covered etc? whatever yo uthink can be used, old runs etc or whatever
- what does the sync do? do we need to start adding buffers like visual buffers on most of our stuff to ensure people are not mis led, or are visually understanding
- pipeline info, still annoyingly only has one of the accordions a different colour, each open accordion should change to the purple colour, but be white background when not open
- the piplein info btw is not the flows of the sit automation stuff, i meant we need flow diagrams here to show how our pipelines work? each part of the pipeline will be informative, do this, this happens, this next, blah blah we need one for each pipeline we have
- I think the text and gaps right, are so vague? like no one will ever know what the question actually is, maybe you need to ensure your asking us the question better? like understand the unconfirmed, or gap and write it out in plain english what the gap and unconfirmed issue is, maybe even a button on the page to say AI summarize? and you go through each and write a description or question better for each so they can be asnwered
- can we re-organise our side bar menu options can stuff be moved around better structured, less accordions? maybe dont know have a think and suggest
- the repos? how come we dont have the test sit repo there as well or all the repos related/
- gaps on the knowledge can be a bit more info? bullet pointed? give more info on what you think is missing in the specs? whats maybe hasnt been gien like a doc or something etc?
- do you want to check out the logs history bit on like all the pipelines and just ground down the summary? it should be that long? i like the small couple sentenced lines of what happened, if it needs to be more sentences fine but make it more summarised right? none of the stuff that takes up a hole ass page
- new pipeline in the future, generate test summary report (we have old ones, and template to use for it and you can scan a test run and write it out> generate it? make sense - let me know what you need
- i wanna change the names of everything again and broaden the names to match the pipeline. like release this is actually a JIRA pipleine right anything you put in there from JIRA will work doesnt have to just be a release, so its more of a Audit againt JIRA but cross examining it, with the suite maybe come up with a coll name for this and ensure this pipeline is this purpose.
- maybe get rid of start entirely, and just have setup and ingest docs in the same pipeline accordion menu option? as its all pipelines right
- docs path why is it still editable? we just wanna see visually where the path is but thats it, take away the field, just move this in a highlighted text area near the title of the page you know like dashboards have the pills. 
- only file? can this not be a drop-down? of the recently uploaded files and you choose out of this? and clearly lable optional
- can we make the long list of currently uploaded docs, an accordion so you can open and close view
- can we put the waiting on you of for you bit on each pipeline under the steps on the left of the two columns for what each step does and the steps? 
- Is pipelines the right word for the accordion in menu? like what are these, tools? functions? abilities? what is it actually really doing in these pipelines? change it to what you think best
- is there a better way to pass in the flow data path, or UX documnets? can we have a whole seperate like section in the settings george oliver menu, like Functional docs, and then a Design docs area? so people can upload purely that doc and we remove the data path field from onboarding entirely?
- Need a way to ensure that our updated from docs, and onboarding dont get confused, like if someone wants to onboard every doc again, they can but shall this be called like re-examine whole suite? or something similar? Examine all docs? let me know haha 
- As we basically need these functionalitys below
- chekcing setup of laptop
- a way to ingest docs, but to give zips of loads of folders, give one doc, examine docs for a bran new suite, examine docs against existing suite, examine one document against existing suite get me? do we need multiple pipelines or one with ability to select, de-select documents?
- onboarding, a newly uploaded documents, for a new suite or an existing suite
- feature (jira, so anything from jira url, or id, that we can examine against and check existing functionality and current suite knowledge, and automation knowledge maybe to ensure bugs, epics, stories, releases, changes anything can be examined against JIRA
- update from docs so this is now the new way to examine existing against a newly uploaded doc, one or multiple? - we need a clear way to select which doc or multiple docs we want
- merge is basically after you have maybe edit existing, or resolved gaps, or done more work on the suite, this will help consolidate dupes, or test cases that could be merged to one, this is a way to review basically the health of the structure and suite.
- targeted run, this is so we can choose a targeted run and get it created by the tool
- we need a way to generate a test run report, so examine the latest run and generate a report based on the templates and existing ones we have to use for knowledge and how it should look
- we need a way to answer questions, gaps, and resolve these gaps on the tool so we can help understand things, update cases afterwards. 
- each needs a short breif step by step guide, no jargan, just singular steps sentences, in an accordion to open and close with just basic steps
- we need a way to check coverage again the design docs.
- need a way to upload functional and design docs seperately
- we need a way to ensure our testrail has kept up with standards, gherkin syntax, english, and understanding or basic readable best practices. 
- health is a weird word for the menu option, maybe merge audit and health together
- we need a way to review test runs, and comments, and new defects, and fails, passed, retest, invalids all statuses, to ensure it may answer gaps, it may help understand changes to the test case, it may create new cases off it.
- checking run history
- checking changes to cases manually 
- we need a way to have automation cases shown in a dashboard for automation tab
- a way to view the keywords, flows
- a repo type structured view of able to click on the tests written, no need to actually show like the tests written in bulk detail just a way to click on them and view them
- pull cases from test rail, write them for automation
- a way to use docs, and jiras to write automation without the whole pre step for testrail and manual cases beforehand
- a way to view project info, like small details like each projects test cases updated, audits, automation tests written, gaps to resolve, like project data in the project tab right
- reports can be more of a link to the generated test run reports, and other tabs menu options for like the tools bug issues, reports, latest logs for the tool, uhh money spent with tool functions anything liek that useful.
- please review every pieploe or option in the menus, and make sure with the above scope that we are naming these options correctly to justfiy the exact scope, coverage nad stuff we do
