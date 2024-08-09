# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock
from selenium.common.exceptions import TimeoutException
from typing_extensions import Self

from pypom_selenium import Region
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
    assert Region(page).root is None


def test_root(page: Page) -> None:
    element = Mock()
    assert Region(page, root=element).root == element
