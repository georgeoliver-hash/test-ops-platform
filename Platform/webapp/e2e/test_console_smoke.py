import re

import pytest

BAD_TEXT = ("undefined", "NaN", "[object Object]", "�")


def _views(page):
    return [b.get_attribute("data-view") for b in page.query_selector_all("button.navitem[data-view]:visible")]


def _settle(page):
    page.wait_for_function("!document.querySelector('#content .loading')", timeout=20000)


def test_every_view_renders_without_errors(page):
    views = _views(page)
    assert len(views) >= 6
    for v in views:
        page.click(f'button.navitem[data-view="{v}"]')
        _settle(page)
        text = page.inner_text("#content")
        assert text.strip(), f"{v}: empty page"
        for bad in BAD_TEXT:
            assert bad not in text, f"{v}: shows {bad!r}"


def test_status_page_fails_fast_offline(page):
    page.click('button.navitem[data-view="health"]')
    _settle(page)
    assert page.inner_text("#content").strip()


def test_change_target_modal_opens_and_closes(page):
    page.click("#changeTargetBtn")
    assert page.is_visible("#targetModal .modal")
    page.click("#modalCancel")
    assert not page.is_visible("#targetModal .modal")


def test_pair_form_is_a_second_popup_within_viewport(page):
    page.click("#changeTargetBtn")
    page.click("#suiteAddProjectBtn")
    assert page.is_visible("#pairModal .pair-modal")
    assert page.is_visible("#targetModal .modal")
    box = page.locator("#pairModal .pair-modal").bounding_box()
    vp = page.viewport_size
    assert box["y"] >= 0 and box["y"] + box["height"] <= vp["height"]
    page.click("#suiteEditCancel")
    assert not page.is_visible("#pairModal .pair-modal")


def _no_bad_text(page, label):
    text = page.inner_text("#content")
    assert text.strip(), f"{label}: empty page"
    for bad in BAD_TEXT:
        assert bad not in text, f"{label}: shows {bad!r}"


def test_every_pipeline_page_renders(page):
    page.wait_for_selector("button.navitem[data-pipeline]:not(.disabled)")
    ids = [b.get_attribute("data-pipeline") for b in page.query_selector_all("button.navitem[data-pipeline]:not(.disabled):visible")]
    assert ids
    for pid in ids:
        page.click(f'button.navitem[data-pipeline="{pid}"]')
        _settle(page)
        _no_bad_text(page, f"pipeline {pid}")
        page.wait_for_selector("#pipelineTabDetails", state="visible", timeout=15000)
        page.click("#pipelineTabLog")
        page.click("#pipelineTabDetails")


@pytest.mark.parametrize("tab", ["tabAutomation", "tabProject", "tabReports", "tabTestOps"])
def test_top_tabs_render(page, tab):
    page.click(f"#{tab}")
    _settle(page)
    _no_bad_text(page, tab)
    for b in page.query_selector_all("#navgroups button.navitem:visible"):
        try:
            b.click(timeout=1500, trial=True)
        except Exception:
            continue
        b.click()
        _settle(page)
        _no_bad_text(page, f"{tab} > {b.inner_text().strip()}")


def test_no_horizontal_page_overflow(page):
    for v in _views(page):
        page.click(f'button.navitem[data-view="{v}"]')
        _settle(page)
        over = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert over <= 2, f"{v}: page overflows horizontally by {over}px"
