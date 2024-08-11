# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from typing_extensions import Self

from pypom_selenium import Region
from pypom_selenium.exception import UsageError
from pypom_selenium.page import Page


class TestWaitForRegion:
    def test_wait_for_region(self, page: Page) -> None:
        assert isinstance(Region(page).wait_for_region_to_load(), Region)

    def test_wait_for_region_timeout(self, page: Page) -> None:
        class MyRegion(Region):
            def wait_for_region_to_load(self) -> Self:
                self.wait.until(lambda s: False)
                return self

        page.timeout = 0

        with pytest.raises(TimeoutException):
            MyRegion(page)

    def test_wait_for_region_timeout_loaded(self, page: Page) -> None:
        class MyRegion(Region):
            @property
            def loaded(self) -> bool:
                return False

        page.timeout = 0

        with pytest.raises(TimeoutException):
            MyRegion(page)


def test_no_root(page: Page) -> None:
    with pytest.raises(UsageError):
        Region(page).root


def test_root(page: Page) -> None:
    element = Mock()
    assert Region(page, root=element).root == element


def test_root_locator(page: Page, element: Mock) -> None:
    class MyRegion(Region):
        _root_locator = (By.ID, "test")

    assert MyRegion(page).root == element
    page.driver.find_element.assert_called_once_with(By.ID, "test")  # type: ignore
    page.driver.find_element.call_count == 1  # type: ignore

    # If a root element is passed on Region instantiation, this root should be used
    # instead of finding one with the _root_locator
    element = Mock()
    assert MyRegion(page, root=element).root == element
    page.driver.find_element.call_count == 1  # type: ignore
