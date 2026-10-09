"""The Status page is a dashboard you can customise: add, remove, reorder, resize; the layout sticks across reloads."""


def _ids(page):
    return page.evaluate("() => [...document.querySelectorAll('.dash-grid .dw')].map(d => d.dataset.wid)")


def test_default_widgets_show_and_the_old_cards_are_gone(spage):
    spage.wait_for_selector(".dash-grid .dw", timeout=60000)
    ids = _ids(spage)
    for w in ("cases", "oldnew", "gaps", "activity", "runhealth", "onegap"):
        assert w in ids, w
    text = spage.inner_text("#content").lower()
    assert "suite health breakdown" not in text and "open suggestions" not in text


def test_customise_add_remove_reorder_resize_and_it_persists(spage):
    spage.wait_for_selector(".dash-grid .dw", timeout=60000)
    spage.evaluate("localStorage.removeItem('testops.dashboard.layout.v1')")
    spage.click("#dashEditBtn")
    spage.wait_for_selector('[data-dw-add="lastjira"]')
    spage.click('[data-dw-add="lastjira"]')
    spage.wait_for_function("[...document.querySelectorAll('.dash-grid .dw')].some(d => d.dataset.wid === 'lastjira')")
    first = _ids(spage)[0]
    spage.click('button[data-dw="hide"][data-i="0"]')
    # the page re-renders (briefly empty) after each change: wait for the new grid, not just the old widget's absence
    spage.wait_for_function(f"document.querySelectorAll('.dash-grid .dw').length > 1 && ![...document.querySelectorAll('.dash-grid .dw')].some(d => d.dataset.wid === '{first}')")
    before = _ids(spage)
    spage.click('button[data-dw="right"][data-i="0"]')
    spage.wait_for_function(f"document.querySelectorAll('.dash-grid .dw')[1]?.dataset.wid === '{before[0]}'")
    spage.select_option('select[data-dw="size"][data-i="0"]', "l")
    spage.wait_for_selector(".dash-grid .dw.dw-l")
    spage.reload()
    spage.wait_for_selector(".dash-grid .dw", timeout=60000)
    ids = _ids(spage)
    assert "lastjira" in ids and first not in ids and spage.locator(".dash-grid .dw.dw-l").count() >= 1
    spage.evaluate("localStorage.removeItem('testops.dashboard.layout.v1')")
