"""The Live page's Schedule & manual run card: shown, previews safely, and refuses to start without the tick."""


def _open_live(spage):
    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview="dashboard"]')
    spage.wait_for_selector("#lvSched h2", timeout=30000)
    spage.wait_for_selector("#lvStartBox", timeout=60000)           # the schedule read may call gh; the form renders either way


def test_the_card_shows_and_previews_without_starting(spage):
    _open_live(spage)
    spage.click("#lvStartBox summary")
    spage.fill("#lvTag", "screen-spine")
    spage.click("#lvPreview")
    spage.wait_for_function("document.getElementById('lvStartMsg').innerText.includes('Would run')", timeout=60000)
    assert "gh workflow run" in spage.inner_text("#lvStartMsg") and "pos_tag_filter=screen-spine" in spage.inner_text("#lvStartMsg")


def test_start_is_refused_until_the_box_is_ticked(spage):
    _open_live(spage)
    spage.click("#lvStartBox summary")
    spage.click("#lvStart")
    assert "Tick the box first" in spage.inner_text("#lvStartMsg")
    assert "Started" not in spage.inner_text("#lvStartMsg")
