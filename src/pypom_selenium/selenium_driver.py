# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from typing import List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait


class Selenium:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_factory(self, timeout: float) -> WebDriverWait[WebDriver]:
        """Returns a WebDriverWait like property for a given timeout.

        :param timeout: Timeout used by WebDriverWait calls
        :type timeout: int
        """
        return WebDriverWait(self.driver, timeout)

    def open(self, url: str) -> None:
        """Open the page.
        Navigates to `url`
        """
        self.driver.get(url)

    def find_element(
        self, strategy: str, locator: str, root: Optional[WebElement] = None
    ) -> WebElement:
        """Finds an element on the page.

        :param strategy: Location strategy to use. See
        `~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str `~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: `~selenium.webdriver.remote.webelement.WebElement` object.
        :rtype: selenium.webdriver.remote.webelement.WebElement

        """
        if root is not None:
            return root.find_element(strategy, locator)
        return self.driver.find_element(strategy, locator)

    def find_elements(
        self, strategy: str, locator: str, root: Optional[WebElement] = None
    ) -> List[WebElement]:
        """Finds elements on the page.

        :param strategy: Location strategy to use. See
        `~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target elements.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str `~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: List of `~selenium.webdriver.remote.webelement.WebElement` objects.
        :rtype: list

        """
        if root is not None:
            return root.find_elements(strategy, locator)
        return self.driver.find_elements(strategy, locator)

    def is_element_present(
        self, strategy: str, locator: str, root: Optional[WebElement] = None
    ) -> bool:
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See
        `~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str `~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        try:
            self.find_element(strategy, locator, root=root)
            return True
        except NoSuchElementException:
            return False

    def is_element_displayed(
        self, strategy: str, locator: str, root: Optional[WebElement] = None
    ) -> bool:
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See
        `~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str `~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator, root=root).is_displayed()
        except NoSuchElementException:
            return False
