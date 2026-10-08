"""The Judge failures page offers a run picker whose default is the newest finished run."""


def test_the_run_picker_defaults_to_the_newest_finished_run(spage):
    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview-pipeline="judge-failures"]')
    spage.wait_for_selector("#sitRunPicker", timeout=45000)       # listing runs may call gh; the select renders either way
    assert spage.input_value("#sitRunPicker") == ""
    first = spage.inner_text("#sitRunPicker option:first-child")
    assert "newest finished run" in first.lower()
    page_text = spage.inner_text("#content").lower()
    assert "run to judge" in page_text
    for step in ("pull run", "collect failures", "judge", "validate", "confirm"):
        assert step in page_text.replace("_", " ")
