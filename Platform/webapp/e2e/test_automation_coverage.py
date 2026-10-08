"""The Automation > Coverage page renders the mapping and section-coverage numbers for the target."""


def test_coverage_page_shows_the_numbers_and_the_draft_label(spage):
    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview="coverage"]')
    spage.wait_for_function("document.querySelector('#content h1') && document.querySelector('#content h1').innerText.includes('Automation coverage')")
    spage.wait_for_function("!document.querySelector('#content .loading')")
    text = spage.inner_text("#content")
    low = text.lower()
    assert "draft" in low
    assert "linked to a case" in low and "testrail sections with a linked functional test" in low
    assert spage.locator("#covGaps tr").count() > 1
    for bad in ("undefined", "NaN", "[object Object]"):
        assert bad not in text


def test_show_all_expands_the_gap_table(spage):
    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview="coverage"]')
    spage.wait_for_selector("#covGaps")
    before = spage.locator("#covGaps tr").count()
    if spage.locator("#covToggle").count():
        spage.click("#covToggle")
        spage.wait_for_function(f"document.querySelectorAll('#covGaps tr').length > {before}")
