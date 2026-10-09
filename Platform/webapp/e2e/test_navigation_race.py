"""A slow landing page must not land on top of the view the person opened while it was loading."""
import time


def test_the_landing_status_page_does_not_overwrite_a_view_opened_early(server, browser):
    ctx = browser.new_context(viewport={"width": 1400, "height": 1000})
    page = ctx.new_page()
    problems = []
    page.on("pageerror", lambda e: problems.append(str(e)))
    page.goto(server + "/")
    page.wait_for_selector('button.navitem[data-view="gaps"]')
    page.click('button.navitem[data-view="gaps"]')              # a real navigation, straight after load
    page.wait_for_function("document.querySelector('#content h1') && /gap/i.test(document.querySelector('#content h1').innerText)", timeout=30000)
    # the Status page's own fetches finish a few seconds later; the Gaps view has to survive that
    for _ in range(10):
        assert "status" not in page.inner_text("#content h1").lower(), page.inner_text("#content")[:80]
        time.sleep(1)
    assert not problems, problems
    ctx.close()
