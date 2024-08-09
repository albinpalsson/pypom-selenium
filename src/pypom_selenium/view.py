# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .selenium_driver import Selenium


class WebView:
    def __init__(self, driver: WebDriver, timeout: float):
        self.driver = driver
        self.driver_adapter = Selenium(driver)
        self.timeout = timeout
        self.wait = self.driver_adapter.wait_factory(self.timeout)

    def find_element(self, strategy: str, locator: str) -> WebElement:
        return self.driver_adapter.find_element(strategy, locator)

    def find_elements(self, strategy: str, locator: str) -> List[WebElement]:
        """Finds elements on the page.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of `~selenium.webdriver.remote.webelement.WebElement`
        :rtype: list

        """
        return self.driver_adapter.find_elements(strategy, locator)

    def is_element_present(self, strategy: str, locator: str) -> bool:
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_present(strategy, locator)

    def is_element_displayed(self, strategy: str, locator: str) -> bool:
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_displayed(strategy, locator)
