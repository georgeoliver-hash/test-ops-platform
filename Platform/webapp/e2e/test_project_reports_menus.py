"""Project and Reports have a menu per onboarded project (and device, for Reports); Reports has a Report and a Test tree tab,
and no "Generated reports" file list any more."""


def _settled(page):
    page.wait_for_function("!document.querySelector('#content .loading')", timeout=30000)


def test_project_menu_lists_onboarded_projects_and_opens_a_dashboard(page):
    page.click("#tabProject")
    page.wait_for_selector('#projectNavItems [data-projview="Translink"]')
    assert page.is_visible('#projectNavItems [data-projview="@all"]')
    page.click('#projectNavItems [data-projview="Translink"]')
    _settled(page)
    page.wait_for_selector("#pdGrid .dw")
    text = page.inner_text("#content").lower()
    assert "devices onboarded" in text and "dashboard for" in text
    assert page.is_visible('#projectNavItems [data-projview="Translink"].active')
    page.click('#projectNavItems [data-projview="@all"]')
    _settled(page)
    assert "every project/device" in page.inner_text("#content").lower()


def test_reports_menu_per_device_with_report_and_tree_tabs(page):
    page.click("#tabReports")
    page.wait_for_selector('#reportsNavgroups [data-rep="Translink|POS"]')
    page.click('#reportsNavgroups [data-rep="Translink|POS"]')
    _settled(page)
    page.wait_for_selector("#repGrid .dw")
    text = page.inner_text("#content").lower()
    assert "report — translink / pos" in text and "generated reports" not in text
    page.click('[data-rep-tab="tree"]')
    _settled(page)
    assert "test tree" in page.inner_text("#content").lower()
    page.click('#reportsNavgroups [data-rep="@tool"]')
    _settled(page)
    assert "tool activity" in page.inner_text("#content").lower()
    assert page.locator("#projectNavgroups:visible").count() == 0 and page.locator("#navgroups:visible").count() == 0
