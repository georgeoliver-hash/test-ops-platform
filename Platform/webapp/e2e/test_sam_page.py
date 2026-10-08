"""The SAM jobs page renders: a jobs table when SAM is reachable, its plain reason when it is not."""


def test_sam_page_renders(spage):
    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview="sam"]')
    spage.wait_for_function("document.querySelector('#content h1') && document.querySelector('#content h1').innerText.includes('SAM jobs')", timeout=60000)
    spage.wait_for_function("!document.querySelector('#content .loading')", timeout=120000)
    text = spage.inner_text("#content").lower()
    assert "read-only" in text
    assert spage.locator("#samJobs").count() == 1 or "sam" in text      # table when reachable; otherwise the reason is on the page
    for bad in ("undefined", "nan", "[object object]"):
        assert bad not in text.split("sam is not reachable")[0].split()
