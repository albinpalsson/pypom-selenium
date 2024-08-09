# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock

from pypom_selenium import Page

# pylint: disable=redefined-outer-name


@pytest.fixture
def base_url() -> str:
    return "https://www.mozilla.org/"


@pytest.fixture
def element(driver: Mock) -> Mock:
    element = Mock()
    driver.find_element.return_value = element
    return element


@pytest.fixture
def page(driver: Mock, base_url: str) -> Page:
    return Page(driver, base_url)


@pytest.fixture
def driver() -> Mock:
    """All drivers"""
    return Mock()
