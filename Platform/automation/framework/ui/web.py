from __future__ import annotations

import os

from playwright.sync_api import sync_playwright

from ..registry.models import Device
from .base import UIDriver

_USERNAME_SELECTORS = [
    "input[type=email]",
    "input[name*=email i]",
    "input[id*=email i]",
    "input[name*=user i]",
    "input[id*=user i]",
]
_PASSWORD_SELECTORS = [
    "input[type=password]",
    "input[name*=pass i]",
    "input[id*=pass i]",
]


class WebUIDriver(UIDriver):
    """Playwright-backed driver for web-portal devices (BOS/ABT/CloudFare/Merit
    back-office UIs). Headless Chromium by default; set WEB_UI_HEADLESS=0 to
    watch it run.

    Login form fields differ per portal, so `login()` guesses common
    username/password selectors. Portals whose fields don't match should set
    `Device.login_selectors` in devices.yaml as an escape hatch.
    """

    def __init__(self, device: Device, headless: bool | None = None):
        self.device = device
        if headless is None:
            headless = os.getenv("WEB_UI_HEADLESS", "1") != "0"
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def start(self) -> None:
        url = self.device.web_ui_url
        if not url and self.device.env_web_ui_url_var:
            url = os.getenv(self.device.env_web_ui_url_var)
        if not url:
            raise ValueError(
                f"Device {self.device.id} has no web_ui_url "
                f"(and env var {self.device.env_web_ui_url_var!r} is unset)"
            )
        self.url = url

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        self._page.goto(url, timeout=15000)

    def stop(self) -> None:
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None
        self._page = None

    def login(self, role: str, username: str, password: str) -> None:
        if self._page is None:
            raise RuntimeError("WebUIDriver.login called before start()")
        selectors = self.device.login_selectors or {}
        username_selector = selectors.get("username") or self._first_matching(_USERNAME_SELECTORS)
        password_selector = selectors.get("password") or self._first_matching(_PASSWORD_SELECTORS)
        if not username_selector or not password_selector:
            raise RuntimeError(
                f"Could not locate login fields for {self.device.id}; set "
                "login_selectors (username/password/submit) in devices.yaml"
            )

        self._page.fill(username_selector, username)
        self._page.fill(password_selector, password)
        submit_selector = selectors.get("submit")
        if submit_selector:
            self._page.click(submit_selector)
        else:
            self._page.keyboard.press("Enter")

    def screenshot(self, path: str) -> None:
        if self._page is None:
            raise RuntimeError("WebUIDriver.screenshot called before start()")
        self._page.screenshot(path=path)

    def title(self) -> str:
        return self._page.title() if self._page else ""

    def current_url(self) -> str:
        return self._page.url if self._page else ""

    def _first_matching(self, selectors: list[str]) -> str | None:
        for selector in selectors:
            if self._page.locator(selector).count() > 0:
                return selector
        return None
