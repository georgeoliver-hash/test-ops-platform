from __future__ import annotations

import os

from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

from ..registry.models import Device
from .base import UIDriver


class AndroidUIDriver(UIDriver):
    """Appium/UiAutomator2-backed driver for Android POS devices.

    Required env: APPIUM_URL (default http://127.0.0.1:4723)
    """

    def __init__(self, device: Device, appium_url: str | None = None):
        self.device = device
        self.appium_url = appium_url or os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
        self._driver = None

    def start(self) -> None:
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        # Use the ADB serial so Appium targets the right device over TCP
        options.udid = self.device.transport.serial
        options.app_package = self.device.appium_app_package
        # Launch into the existing app session without reinstalling or resetting
        options.no_reset = True
        options.dont_stop_app_on_reset = True
        options.new_command_timeout = 120
        self._driver = webdriver.Remote(self.appium_url, options=options)

    def stop(self) -> None:
        if self._driver:
            self._driver.quit()
            self._driver = None

    def login(self, role: str, username: str, password: str) -> None:
        raise NotImplementedError(
            "AndroidUIDriver.login: use the pos_nav fixture and pos_nav.sign_on() for POS sign-on."
        )

    def screenshot(self, path: str) -> None:
        if self._driver:
            self._driver.save_screenshot(path)
