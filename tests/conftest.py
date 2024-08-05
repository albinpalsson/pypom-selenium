# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock

from pypom_selenium import Page

# pylint: disable=redefined-outer-name


@pytest.fixture
def base_url():
    return "https://www.mozilla.org/"


@pytest.fixture
def element(driver):
    element = Mock()
    driver.find_element.return_value = element
    return element


@pytest.fixture
def page(driver, base_url):
    return Page(driver, base_url)


@pytest.fixture
def driver():
    """All drivers"""
    return Mock()
