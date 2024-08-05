# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock
from selenium.common.exceptions import TimeoutException

from pypom_selenium import Region


class TestWaitForRegion:
    def test_wait_for_region(self, page):
        assert isinstance(Region(page).wait_for_region_to_load(), Region)

    def test_wait_for_region_timeout(self, page):
        class MyRegion(Region):
            def wait_for_region_to_load(self):
                self.wait.until(lambda s: False)

        page.timeout = 0

        with pytest.raises(TimeoutException):
            MyRegion(page)

    def test_wait_for_region_timeout_loaded(self, page):
        class MyRegion(Region):
            @property
            def loaded(self):
                return False

        page.timeout = 0

        with pytest.raises(TimeoutException):
            MyRegion(page)


def test_no_root(page):
    assert Region(page).root is None


def test_root(page):
    element = Mock()
    assert Region(page, root=element).root == element
