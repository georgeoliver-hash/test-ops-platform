"""How to's tiles open a pop-up; links into a pipeline move the menu highlight with them."""


def test_how_tos_are_tiles_that_open_a_popup(spage):
    spage.click('.navitem[data-view="pipelines"]')
    spage.wait_for_selector(".howto-grid .howto-tile", timeout=30000)
    assert spage.locator(".howto-section").count() >= 2
    assert spage.locator('.howto-tile[data-howto="start"] .howto-star').count() == 1
    assert spage.locator('.howto-tile[data-howto="targeted-run"]').count() == 0          # archived
    assert spage.locator('.howto-tile[data-howto="scheduled-scan"] .howto-where').count() == 1   # folded: says where it lives
    spage.click('.howto-tile[data-howto="ingest-docs"]')
    spage.wait_for_selector("#howtoOpen")
    spage.click("#howtoOpen")
    spage.wait_for_selector('.navitem.active[data-pipeline="ingest-docs"]', timeout=20000)


def test_a_link_to_a_pipeline_highlights_it_in_the_menu(spage):
    spage.click('.navitem[data-view="gaps"]')
    spage.wait_for_selector('[data-gpt="log"]', timeout=30000)
    spage.click('[data-gpt="log"]')
    spage.wait_for_selector('[data-goto-pipeline="resolve-gaps"]', state="attached", timeout=30000)
    spage.evaluate("document.querySelector('[data-goto-pipeline=\"resolve-gaps\"]').click()")
    spage.wait_for_selector('.navitem.active[data-pipeline="resolve-gaps"]', timeout=20000)
    assert spage.locator('.navitem.active[data-view="gaps"]').count() == 0
