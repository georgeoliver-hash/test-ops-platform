# Test-Ops Console — issues & feedback (v8)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`
- `archive/ISSUES-2026-09-28-resolved.md`
- `archive/ISSUES-2026-09-28-b-resolved.md`
- `archive/ISSUES-2026-10-08-resolved.md` (v7: everything up to 2026-10-08)

**How to use:** just drop raw bullet points under "Testing notes" below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## To test today (built since v7, none of it eyeballed by you yet)

- **Automation → Coverage** — Robot tests tied to TestRail cases, and which sections have a linked functional test. Draft numbers; most
  sections read ZERO until mapping rows are approved (see below).
- **Automation → Runs → Judge failures** — pulls a finished sit run, groups failures, AI judges P1–P5, you confirm, writes a
  `severity=P<n>` tag patch for sit. Has a **run picker** (default: newest finished run with Robot results). The AI step has never run.
- **Automation → Live runs → Schedule & manual run** — when the pipeline runs by itself (read from sit's workflow), and a guarded
  "Start run now" (preview first; needs the tick box; uses the lab device). Please don't start one unless you mean to.
- **Hand-offs** (Test-Ops sidebar) — the author → review → approve → automate → run → report queue; approve/reject as yourself.
- **Status page** no longer gets overwritten by a view you open while it is loading.
- **Change target** edit/add pair is a second pop-up (checked in tests, not by eye).
- Sidebar icon rail: icons were missing for Overview, Coverage and Hand-offs — fixed.

## Known open (not bugs in what is built; things that need a person, data or hosting)

- **Hosting / logins** for company-wide use — needs IT's answer on who owns internal hosting; then SSO, per-user secrets, Postgres,
  shared uploads. Also gates the runner → console live push (`tops-live-push-mode` branch in sit is held for this).
- **Mapping approvals** — `system-test-ops/proposals/Translink-POS-suite-restructure/robot-case-mapping-DRAFT.csv`: fill `approved_case_id`
  for the rows you agree with (only 7 tests link to a case today), then re-run the two tools; Coverage updates.
- **Judge failures**: P2–P4 wording in `system-test-ops/knowledge/severity-rubric.md` is my proposal; a tag is a snapshot of one run's
  judgement (the patch replaces an existing `severity=` tag but never removes it from a test that now passes).
- **Lab database** ("TDS server unavailable") fails every sit suite setup, so no test body has run on a device.
- **Ingest-docs** has not been run on the real POS docs through the console; 246 marker cases still need device checks / Translink
  answers; 47 gap answers are "needs a decision".
- **Coverage**: no Refresh button (re-running the two tools needs TestRail from wherever the console is hosted).
- **Schedule**: shown, not editable — changing it is a PR to sit's workflow file.
- **Stale-render guard** covers the Status page only; other slow views could in principle land on top of one opened early.
- **e2e**: no pipeline-run test yet (a run writes into the real system-test-ops; needs a throw-away copy of it).
- **ZZ_DELETE_REVIEW** binning in TestRail — yours (needs delete rights).
- **Open question**: scheduled checks — against a centralised doc location, or just internal uploads?
- **Naming/IA umbrella** — review remaining pipeline/option names against their real scope.

---

## Claude progress on the testing notes (started 2026-10-09; updated after every batch)

**Batch 1 - menu / layout clean-up (done):**
- Repos removed from the menu. Scheduled checks and Hand-offs moved into **Settings** as tabs (the pending-suggestions badge now sits on Settings).
- Settings tab has **"Allow re-running Setup"**; when Setup is complete (credentials verified + suite + docs) the Setup menu item gets a **✓** and the Setup page is faded except its banner.
- Folded into their host page as **tabs** (no menu item, host stays highlighted): Scheduled scan -> Ingest docs; Update from docs -> Build suite; Defect -> Cross-Check JIRA; Merge check + Trace check -> Checkup; Clarify + Group gaps -> Gaps page.
- Archived (menu item removed, pipeline files kept): Targeted run, Design (audit-flows), Standard (still runs inside Build suite / Checkup), Automation > Tests written.

**Batch 2 - Status is now a dashboard you build yourself (done):**
- **Customise** button: add / remove widgets, move them (◀ ▶), width (Small / Medium / Full) and height (Fit / Short / Tall). Layout is saved in your browser; "Reset" puts the default back.
- Default: Cases (total only), Old vs new (live), Gaps (pills: open / GAP / UNCONFIRMED / answered), Recent activity (left), Run health (runs considered, total passing, total failures, always failing + which run ids), Run comments, Observed changes, Answer one gap (answer or skip, one at a time), SAM device + job health, Last audit, Docs (count + last upload), AI spend.
- Extra widgets you can add: Scheduled checks, Last JIRAs audited, Defects in latest run, Coverage in automation, Coverage against specs.
- Removed: Suite health breakdown, Open suggestions.
- **Your question "Run health, is this even right?"** - yes, it is real. It reads every TestRail run on the new POS suite (30607), manual or automated: 6 runs (R21978, 21742, 21495, 19352, 19087, 19074). They are people's manual runs, not agentic ones. The widget now lists the run ids so you can check them.

**Batch 3 - How to's (done):** bold, theme-coloured section titles; square tiles 4 across (★ on Setup), name + one-line description + AI / code / human / process pills; click a tile -> pop-up with the steps and an "Open ... →" button. Folded pipelines say where they live ("a tab on Build suite").

**Batch 4 - Gaps / Case review (done):** "Refresh against new docs" and the recheck text removed from Gaps. **Case review "0 open, 0 done"**: those counts are for the current check only (nothing open right now). Added a third pill "N fixed or accepted so far" (all time, from the review log - 52 today).

**Batch 5 - the bugs list (done):**
- Links now move the menu highlight to where you land (folded pipelines highlight their host page).
- Run from elsewhere: links such as Gaps log "Run →" open a small pop-up with just the required inputs + context and a Run button; it starts in the console without leaving the page.
- Console: **Acknowledge & clear** button (cancels the run if it is still going, then clears the console).
- **Give context** is now a button that opens a pop-up (no more inline box).
- Banners are full width with **–** (shrink to a thin bar you click to reopen) and **✕** (clear). They are cleared when you change page.
- Two-column pipeline pages: both boxes are the same height.
- Checkup: the composite steps (Merge check, Trace check, Standard) are shown as **PROCESS** steps, not human steps - they are pipelines Checkup runs for you.

**Batch 6 - pipeline pages (done):**
- **Build suite renamed "Suite builder"**. Your question: it builds a new suite from docs *or* updates an existing one (Update from docs tab). Change target points the console at an existing suite; Suite builder is what fills it.
- Ingest docs: **Check relevance** is a button next to Run; the result shows as a banner (no card).
- Update from docs: the last 3 ingest runs with status pills ("Use this run" ticks its files); knowledge files are a multi-select picker (All / None / filter) instead of typing paths.
- Resolve: **area is no longer something you type** - it is proposed from the areas your answered gaps point at (you can still change it).
- Trace check: if nothing was raised or covered in the window it reports "nothing to trace" and finishes (not a failure). Checkup already runs Merge check + Trace check + Standard.
- History: choose 1, 2, 3, 4, 5, then 10, 15 ... 50 runs.
- **Link defects - what is it for?** It matches the known-defect list (e.g. the 128 POS defects) to the cases they affect and tags those cases KNOWN DEFECT, so a failure on them is expected and not raised again.
- **Run report "blue test" text:** I could not find it in any saved report (the only one on disk, 2026-09-28, has none). Most likely the agent copied the Word template's blue guidance/example text. The pipeline + template note now say template guidance is never content and the draft must be re-read and stripped of anything not backed by the run data. **Needs checking:** if you see it again, send me the run so I can see the exact text.
- **Feature / Cross-check JIRA picker (board in Settings + search after 3 characters):** not built yet - the console has no Jira access of its own (Jira goes through the Atlassian MCP in Claude). Needs a decision: add a Jira API token to Settings (then I build the picker), or keep typing keys.

## Testing notes (George)

Test-Ops
- Admin
-- Status
--- do we need edited, or added in the cases total? whats the purpose - just need to see how many cases are in the suite (not marked as delete) no need to put the not marked as delete though
--- move old vs new up in place of the removed edit, added and same height - still cool to see the old vs new suite data.
--- Run Health, is this even right? i dont think any POS agentic method runs have been done on testrail? 
--- Move recent activity to the left in place of suite health breakdown. 
--- Would it actually be possible to make the dashboard self edited, so I can select what data and info I want to display, and move the dashboard components to different widths, heights, and move into different positions or is this too much work?
--- No need for the case, title, pass/fail on the run health, just have quick runs considered, Total failures, Always failing, Totsal Passing
--- Suite health breakdown, not sure this is useful as orphaned is confusing anyway, just get rid of this, recent acvitiy good to keep. 
--- Remove open suggestions, what was this for?
--- Comments i like, keep
--- Observed changed good
--- Open gap register can this just be a pill total gaps, unconfirmed, how many asnwered type thing
--- we should have another one avialable for the dashboard thats like, one gap question so you can click it and answer quickly, good for like re occcuring use for people to come on see dashboard answer one questions then move on to somethign else
--- SAM stuff should be on the dashboard too or option to add, about the device, some cool info - maybe multiple optiosn to have to add for all we have, like different ways to show it. edit the dashboard how you want configure it how you want
--- Dcs on file is good to have, maybe just a wait to see the totla number, the last time uploaded, etc
--- Dashboard options to add, shceduled checks (for device targeted), last JIRAs audited agaisnt, added, how many runs are ongoing, open, closed, how many defects are raised in the latest run only, coverage against specs, coverage in automation
-- Hows to's
--- make the pipeliens and checks sub titles, bolder and theme coloured
--- Can we have square pills with a 4 square wide - so one, two ,three, four and each pill is the name so Setup /start (star) the brief description and the coloured pills for ai human code. Instead oaccordions just make a pop up with the how to text inside when you click on the square option understand? this way we fit more in the screen.
-- Repos (delete this from the test tool - not needed. remove
-- Scheduled Checks can put this in the settings instead? remove from menu Sidebar
-- Gaps
--- Refresh against new docs does this actually do anything? is this essentially the scheduled check, or like a way of refreshing the knowledge against a updated spec? 
--- Maybe get rid of the refresh against docs button here, too much going on, maybe we just need somewhere in the docs to do this? as tbh we normally make versions of a doc anyway so they would upload v2 of the doc we have, so it would be a pipeline we have already i think? that re ingests the new doc.
--- Get rid of the bit with the rechecked agains 0 gaps etc, no need now
-- Case review
--- the 0 open 0 done is that not working as there is 52 done right on this targeted suite? or is it based on a real time update of the current reviews?
- Pipelines
-- Hand-offs
--- Can we put this in the settings area too? like most human to approve stuff like this and scheduled checks, should be in settings I think
-- Setup
--- If setup is complete and the green bar is showing and credentials all verified etc, then can we add a small tick icon to the setup menu option
--- Can we fade out all the options, the run options and stuff on this page except the banner so that people know it is done.
--- Add somewhere in the settings to undo the fade, so if you really wanna run it again you can turn it back on so people can re-run the setup part again
-- Ingest docs
--- Check relevance against devcies do we need this here? isnt this something already being done when there uploaded, or a pre ingest step? or can it be moved to just one button alongside thr 'run' and give context buttons, and then just use our green, red, amber banners now mentioned above to give the result?
--- we need a way to clear the banners too dont forget that not just open and close
-- Scheduled Scan
--- I feel like we could have both this piepline and ingest docs pipeline under the same page, so on ingest docs, with page, logs, and then another tab before logs? with doing a check of current documents (really only worth it when we have centralised location) 
-- Build Suite
--- Question - when does someone want to edit, review, work on an existing suite and make this the suite for there upcoming work but use claude and our tool to continue work on it?
-- Feature
--- Do we want to have in settings instead a way to pass it the board or space, or whatever for the targeted areas, like a config or JIRA locations that re the epic, the project space that hodls all the jiras and URLS so that we can actually have a search and select picker that pulls in the JIRAAs or is this a stupid idea for a picker if there might be 2000 jiras?
--- Maybe you have to put in 3 numbers of a JIRA ID to get jira ids to show?
-- Update from Docs
--- Is this where the user has an existing suite and wants to review the uploaded docs against it? Can we put this in the build suite page with a tab? 
--- Maybe build suit eneeds to be ab etter wording to account for building, editing, updating a suite but a better consolidated word for it all.
--- Past ingest docs doesnt need to be that many whens statsus, maybe literally the last two or three audits done, and make it look prettier with like green success or red failed.
--- Knowledge files here needs to be a picker? a dropdown picker? i have no idea where these docs live or what needs to be here to work, update from docs?
--- We need multiple options here, we might upload 5 docs, and then want to review these docs and all distilled knowledghe against an existing suite (never made with claude and our tool)
--- We also want a scenario where i have a new doc, add it to the existing 4 docs already ingested and used to write tests, we need a way to pick multiple or one newly added doc (which should then automatically know all distilled knowledge related to that doc) - against the current existing suite targeted
-- Merge
-- Targeted Run
--- Think we should remove this tbh, mark as archive, dont know if it is useful, we can keep the files and work for a little bit as we may as kfor the featurr back but for now not needed
-- Cross Check JIRA
--- Maybe the JIRA picker needs to to for a specific config set up as above, set translink board beforehand
--- Then write three numbers to match a Jira id type thing
-- Design
--- Do we need this anymore if we dont need seperate UX flows? seems silly to ask them to provide a transcribed format of the flows
--- Archive it and remove
-- Standard
--- Remove from menu - as this is something that runs inside other pipelines right runs in checkup - so remove menu option for seperate pipeline just keep the logic so it runs in checkup
-- Run Report
--- the report still produces with like blue test? this is example text from the template we need to deep dive into how its reading and using the current template
-- Defect
--- Is this a jira issue or bug right? feel like cross check JIRA does the same thing? can we no use maybe this pipeline as a tab option on the same page as cross check JIRA? 
-- History
--- Can we choose 1 run or 2, 3 4 or 5 - then go in incrememnts of 5 after that?
-- Trace Check
--- How does this work if no jiras have been done? i think this should probably just be a if stuff done, then do this, if not skip it inside the checkup pipeline tbh, same as merge check maybe checkup covers all of this
-- Chckup
--- This probably should include all of the stuf above inside the pipeline dont know why they are human steps when were basically doing the functional stuff in other piepliens here, so lets fix this
-- Resolve
--- Why do we need area* here? whats the point? surely we just see the answers given on the gaps and now we use this to create more knwoeldge and distilled knowlegdhe rigjt?
--- Think the tool should see the answers and area's already on the question of like potential area maybe? or just makle the judgement dont know why i should give an area
-- Clarify
--- Think this should be a button inside GAPS page, or a different tab, this should be inside there not its own seperate entity on the menu
-- Group Gaps
--- Same as above, move inside GAPS page on the tool instead either a tab or button, no need for menu option really
-- Link defects - please explain what this area is for?

project
- Can we have menu options for each currently onboard Project, so NJT and Translink then the project dashboard for each of them seperate. 
- Maybe add the devcies, and whats onboarded - etc the current display for IT
- Also be good to have like other things the tool has been doing, like cases total, money spent, new vs old, last audits, tests passing, failing, skipping automation, manual tests, run comments, issues being raised etc.

Reports
- Again we need menu options here, so we can view different projects potential already onboarded right so NJT and Translink, maybe then underneath each project the onboarded device as a menu option to then see that specific report.
- How are we syncing this, as things change all the time with where the automation readiness is?
- The generated reports bit no need, just bulking out the dashboard for no reason
- Maybe have this report as a dahsboard
- Then another menu option with the TREE of structured tests, and then how many tests are currently done in each area
- How many smoke, operator, area tests, blah blah

Automation
- SIT
-- Overview
---  Looks good but how is this true to the SIT framework, how is this staying up to date? it could be really far behind in terms of what tests we actually have passing, failing, skipped written, not written, smoke, bvt, area tags, other tags
--- export autoamtion remove from this overview
--- Only show the stuff thats been onboarded and suites written for, and automation done for
--- maybe use some metrics here similar to SAM
-- Live Runs
--- Results folder and printer files folder? can these not be just mapped hardcoded? do we even want the ability to change this?
--- Do we need a better way to help someone set this page up? where do i get this info to set it up what do i do
--- Scheduled runs and live runs is good i like you can pick stuff, maybe we need to refresh things, or need the settings or sources set up properly, but would be good to choose the tag and the operator mode and what not for the targeted device and this actually kickstart a live SAM pipeline job
--- We have more data now so why is it not here?
--- printed tickets, is this just the file thats printed, maybe we need a way to live view the test executed, and the expected printed ticket and then the actual printed ticket]
--- tests are good but im skeptical im not actually seeing a live view of the tests being executed in the flow and run, want to see like the actual tests case and steps with it visible and then pass, fail, skip once it executes.
--- the log is cool is tis the github logs yes> not the device logs? maybe it should be our own cool log of the passed and failed stuff
-- Coverage
--- Is this fake data as i feel we have actual tests coverage or is this because we havent actually got much functiona lstuff just screens?
-- Test written
--- Probably archive this and remove it, no need. all this data is in other areas and dashboards
-- Keywords
--- Is this not being refreshed against the current SIT, as the POS now has loads of better keywords
--- Dont know how beneficial this actually is unless it was to actually tell you like keyword, how many cases use this keyword, what the keyword does?
-- Screen flows
--- Is thsi the source of truth for the flows on the devices, it should be
-- Draft
--- Feel like this is a bit shit and doesnt work as you can see the jira area, the last ingested area, this just needs to be provide me a file, or files, or data knowledge and tlel me to write a test without scanning other files



STILL TO COME
- Judge failures
- SAM jobs
Projects 
- Changing target
- Asking questions


Bugs and issues:
- Clicking a link in like gaps, run resolve, goes to that screen but stays toggled to gaps on the side menu? same happens with alot of links on the site, but should always direct you to where you wanna be when clicked
- what might solve that is, when you wanna run a pipeline from a different area, then open a small pop up with the run button and key areas * you need to have to start it, then you can start it from where you are, and it starts in the console then as well. 
- when something fails on a run, the console shows a red results reason for it, but we need to be able acknowledge the fialure so it can be cancelled, and clearing the console process. 
- the Give Context button to the right side of the Run button on all the pipeline pages which holds a pop up with the field to give a contect (prompt the run) is not working? its not even visible, I can see the give content prompt full width near the top of the pages but no, put in a button instead otherwise clunking up the pages
- Green, red banners (like notifications_ example on set up we have the tick and green banner for everything done, these type of notifications and banners can they go full widthunderneath the top part underneath the hamburger, and targeted text and field and change target, full width go herer whereever there displaying, with a cross so people can close it (but keep a small half now height green / red bar there still so people can open again more of a close button to remove from view.
- Why is it sometimes, like dashboard and other place so exmaple is feature you have the info steps 1 - 6 and then the feature or key container next to it, one container is bigger than the other, can we not have like better heighted containers, so there isnt weird small gaps?
