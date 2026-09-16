# Test-Ops Console — quick-start cheat sheet

## Setup (once)

1. Ask George for GitHub access to `test-ops-platform`, `system-test-ops`, and `test-automation-sit`.
2. Clone all three repos into the same folder, side by side (not nested).
3. Install Claude Code and log in.
4. Run `python -m venv .venv` then `.venv\Scripts\python.exe -m pip install -e ".[dev]"` inside both `system-test-ops` and `test-ops-platform`.
5. Copy `system-test-ops\.env.example` to `.env` and fill in your own TestRail URL, username, and API key.
6. Start the console: `cd test-ops-platform` then `.venv\Scripts\python.exe -m uvicorn Platform.webapp.app:app --host 127.0.0.1 --port 8791`.
7. Open `http://127.0.0.1:8791` in your browser.

## Using it — the full journey for a new project

1. Click the target name at the top, click **"Add / edit this pair"**, type your new project/device name, tick "Fresh build" (no old suite), and pick the real TestRail project + suite from the dropdowns — never type numbers by hand.
2. Tick "I approve" and click **"Approve & apply target"** — adding the pair alone doesn't switch to it.
3. Click **Start** and **Run** to check readiness first.
4. Upload your requirement documents on the Docs page.
5. Open **ingest-docs**, click **Run**, and click **Continue** at each pause after actually reading what it says.
6. Once the specs are committed (via GitHub Desktop or `git commit`), open **onboard-suite** and click **Run**.
7. Read each pause carefully and click **Continue** — some of these are asking you to confirm real facts, not just rubber-stamp.
8. When you reach a push step, actually read what it's about to push into TestRail, then click **Approve & Push** only when you're happy with it — do this once per functional area.
9. If a step fails, click **"Retry from here"** on that step — never restart the whole run from scratch.
10. Once `onboard-suite` finishes, open **export-automation** and click **Run** — this produces a backlog of which pushed cases are flagged automatable.

## Passing failures to Claude

1. Just paste the exact "Run failed" text and whatever "Result"/output is shown — don't summarise it yourself.
2. If it looks like the tool is asking you to guess or invent something you don't actually know, don't — say so and ask instead.

## Known quirks to watch for

1. The old suite and the new suite can live under **different** real TestRail projects — always check both when adding a target, don't assume they match.
2. The console's own "project" label (e.g. "NJT") is not the same thing as a real TestRail project name — always pick the real one from the dropdown.
3. You'll see "George Oliver" at the bottom of the page no matter who's using it — that's cosmetic, your own data stays separate on your own machine.
4. Some steps (author_area, especially) genuinely take several minutes each — that's normal, not a hang.
5. `onboard-suite` is the least proven pipeline so far — expect more rough edges there than elsewhere.
