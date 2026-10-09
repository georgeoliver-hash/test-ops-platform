"""George's 2026-10-09 menu clean-up: removed items are gone, folded pipelines are tabs on their host page, Settings has tabs."""


def _menu_ids(page):
    return page.evaluate("""() => [...document.querySelectorAll('.navitem')].map(b => b.dataset.view || b.dataset.pipeline || b.dataset.aview || b.dataset.aviewPipeline).filter(Boolean)""")


def test_removed_and_folded_items_are_not_in_the_menu(spage):
    spage.wait_for_selector('.navitem[data-pipeline="ingest-docs"]')
    ids = _menu_ids(spage)
    for gone in ("repomap", "scheduled", "handoff", "tests", "targeted-run", "audit-flows", "audit", "fold-defect", "scheduled-scan",
                 "update-suite-from-docs", "consolidation-check", "traceability-check", "clarify-gaps", "group-gaps"):
        assert gone not in ids, gone
    for kept in ("health", "pipelines", "gaps", "caseReview", "start", "ingest-docs", "onboard-suite", "audit-coverage", "maintain", "settings"):
        assert kept in ids, kept


def test_a_folded_pipeline_is_a_tab_on_its_host_and_keeps_the_host_highlighted(spage):
    spage.click('.navitem[data-pipeline="ingest-docs"]')
    spage.wait_for_selector('.pipeline-family-tabs [data-family-tab="scheduled-scan"]')
    spage.click('.pipeline-family-tabs [data-family-tab="scheduled-scan"]')
    spage.wait_for_function("document.querySelector('.pipeline-family-tabs .tab-btn.active') && document.querySelector('.pipeline-family-tabs .tab-btn.active').dataset.familyTab === 'scheduled-scan'")
    assert spage.locator('.navitem.active[data-pipeline="ingest-docs"]').count() == 1


def test_gaps_has_clarify_and_group_tabs(spage):
    spage.click('.navitem[data-view="gaps"]')
    spage.wait_for_selector('.pipeline-family-tabs [data-family-tab="clarify-gaps"]')
    spage.click('.pipeline-family-tabs [data-family-tab="group-gaps"]')
    spage.wait_for_function("document.querySelector('.pipeline-family-tabs .tab-btn.active').dataset.familyTab === 'group-gaps'")
    assert spage.locator('.navitem.active[data-view="gaps"]').count() == 1


def test_settings_has_scheduled_checks_and_hand_offs_tabs(spage):
    spage.evaluate("document.querySelector('.navitem[data-view=settings]').click()")
    spage.wait_for_selector('[data-settings-tab="handoff"]')
    spage.click('[data-settings-tab="handoff"]')
    spage.wait_for_function("document.querySelector('#content h1') && document.querySelector('#content h1').innerText.includes('Hand-offs')", timeout=20000)
    assert spage.locator('[data-settings-tab="handoff"].active').count() == 1
    spage.click('[data-settings-tab="scheduled"]')
    spage.wait_for_function("document.querySelector('[data-settings-tab=scheduled].active') !== null")
    spage.click('[data-settings-tab="settings"]')
    spage.wait_for_selector('#setupReenable')
