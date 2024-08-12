# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Generic, List, Optional, Tuple
from typing_extensions import TypeVar, Self
from selenium.webdriver.remote.webelement import WebElement

from .exception import UsageError
from .page import Page
from .view import WebView

T = TypeVar("T", default=Page, bound=Page)


class Region(WebView, Generic[T]):
    """A page region object.

    Used as a base class for your project's page region objects.

    :param page: Page object this region appears in.
    :param root: (optional) element that serves as the root for the region.
    :type page: `~.page.Page`
    :type root: `~selenium.webdriver.remote.webelement.WebElement`

    Usage::

      from pypom_selenium import Page, Region
      from selenium.webdriver import Firefox
      from selenium.webdriver.common.by import By

      class Mozilla(Page):
          URL_TEMPLATE = 'https://www.mozilla.org/'

          @property
          def newsletter(self):
              return Newsletter(self)

          class Newsletter(Region):
              _root_locator = (By.ID, 'newsletter-form')
              _submit_locator = (By.ID, 'footer_email_submit')

              def sign_up(self):
                  self.find_element(*self._submit_locator).click()

      driver = Firefox()
      page = Mozilla(driver).open()
      page.newsletter.sign_up()

    """

    _root_locator: Optional[Tuple[str, str]] = None

    def __init__(self, page: T, root: Optional[WebElement] = None):
        super().__init__(page.driver, page.timeout)
        self._root = root
        self.page = page
        self.wait_for_region_to_load()

    @property
    def root(self) -> WebElement:
        """Root element for the page region.

        Page regions should define a root element either by passing this on
        instantiation or by defining a `_root_locator` attribute. To
        reduce the chances of hitting
        `~selenium.common.exceptions.StaleElementReferenceException` or similar
        you should use `_root_locator`, as this is looked up every time the
        `root` property is accessed.
        """
        if self._root is not None:
            return self._root

        if self._root_locator is not None:
            strategy, locator = self._root_locator
            return self.page.find_element(strategy, locator)

        raise UsageError(
            "Set a root element or define a _root_locator to be able to use the root property."
        )

    def wait_for_region_to_load(self) -> Self:
        """Wait for the page region to load."""
        self.wait.until(lambda _: self.loaded)
        return self

    def find_element(self, strategy: str, locator: str) -> WebElement:
        """Finds an element on the page.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: An element.
        :rytpe: `~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver_adapter.find_element(strategy, locator, root=self.root)

    def find_elements(self, strategy: str, locator: str) -> List[WebElement]:
        """Finds elements on the page.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of `~selenium.webdriver.remote.webelement.WebElement`
        :rtype: list

        """
        return self.driver_adapter.find_elements(strategy, locator, root=self.root)

    def is_element_present(self, strategy: str, locator: str) -> bool:
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_present(strategy, locator, root=self.root)

    def is_element_displayed(self, strategy: str, locator: str) -> bool:
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See `~selenium.webdriver.common.by.By`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_displayed(
            strategy, locator, root=self.root
        )

    @property
    def loaded(self) -> bool:
        """Loaded state of the page region.

        You may need to initialise your page region before it's ready for you
        to interact with it. If this is the case, you can override
        `loaded` to return ``True`` when the region has finished
        loading.

        :return: ``True`` if page is loaded, else ``False``.
        :rtype: bool

        Usage::

          from pypom_selenium import Page, Region
          from selenium.webdriver.common.by import By

          class Mozilla(Page):
              URL_TEMPLATE = 'https://www.mozilla.org/'

              @property
              def newsletter(self):
                  return Newsletter(self)

              class Newsletter(Region):
                  _root_locator = (By.ID, 'newsletter-form')

                  @property
                  def loaded(self):
                      return 'loaded' in self.root.get_attribute('class')

        """
        return True
