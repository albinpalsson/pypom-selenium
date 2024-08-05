# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import random
import pytest
from selenium.common.exceptions import TimeoutException

from pypom_selenium import Page
from pypom_selenium.exception import UsageError


def test_base_url(base_url, page):
    assert base_url == page.seed_url


def test_seed_url_absolute(base_url, driver):
    url_template = "https://www.test.com/"

    class MyPage(Page):
        URL_TEMPLATE = url_template

    page = MyPage(driver, base_url)
    assert url_template == page.seed_url


def test_seed_url_absolute_keywords_tokens(base_url, driver):
    value = str(random.random())
    absolute_url = "https://www.test.com/"

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + "{key}"

    page = MyPage(driver, base_url, key=value)
    assert absolute_url + value == page.seed_url


def test_seed_url_absolute_keywords_params(base_url, driver):
    value = str(random.random())
    absolute_url = "https://www.test.com/"

    class MyPage(Page):
        URL_TEMPLATE = absolute_url

    page = MyPage(driver, base_url, key=value)
    assert f"{absolute_url}?key={value}" == page.seed_url


def test_seed_url_absolute_keywords_params_none(base_url, driver):
    value = None
    absolute_url = "https://www.test.com/"

    class MyPage(Page):
        URL_TEMPLATE = absolute_url

    page = MyPage(driver, base_url, key=value)
    assert absolute_url == page.seed_url


def test_seed_url_absolute_keywords_tokens_and_params(base_url, driver):
    values = (str(random.random()), str(random.random()))
    absolute_url = "https://www.test.com/"

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + "?key1={key1}"

    page = MyPage(driver, base_url, key1=values[0], key2=values[1])
    assert f"{absolute_url}?key1={values[0]}&key2={values[1]}" == page.seed_url


def test_seed_url_empty(driver):
    page = Page(driver)
    assert page.seed_url is None


def test_seed_url_keywords_tokens(base_url, driver):
    value = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = "{key}"

    page = MyPage(driver, base_url, key=value)
    assert base_url + value == page.seed_url


def test_seed_url_keywords_params(base_url, driver):
    value = str(random.random())
    page = Page(driver, base_url, key=value)
    assert f"{base_url}?key={value}" == page.seed_url


def test_seed_url_keywords_params_space(base_url, driver):
    value = "a value"
    page = Page(driver, base_url, key=value)
    assert f"{base_url}?key=a+value" == page.seed_url


def test_seed_url_keywords_params_special(base_url, driver):
    value = "mozilla&co"
    page = Page(driver, base_url, key=value)
    assert f"{base_url}?key=mozilla%26co" == page.seed_url


def test_seed_url_keywords_multiple_params(base_url, driver):
    value = ("foo", "bar")
    page = Page(driver, base_url, key=value)
    seed_url = page.seed_url
    assert f"key={value[0]}" in seed_url
    assert f"key={value[1]}" in seed_url

    assert re.match(rf"{base_url}\?key=(foo|bar)&key=(foo|bar)", seed_url)


def test_seed_url_keywords_multiple_params_special(base_url, driver):
    value = ("foo", "mozilla&co")
    page = Page(driver, base_url, key=value)
    seed_url = page.seed_url
    assert "key=foo" in seed_url
    assert "key=mozilla%26co" in seed_url

    assert re.match(
        rf"{base_url}\?key=(foo|mozilla%26co)&key=(foo|mozilla%26co)", seed_url
    )


def test_seed_url_keywords_keywords_and_params(base_url, driver):
    values = (str(random.random()), str(random.random()))

    class MyPage(Page):
        URL_TEMPLATE = "?key1={key1}"

    page = MyPage(driver, base_url, key1=values[0], key2=values[1])
    assert f"{base_url}?key1={values[0]}&key2={values[1]}" == page.seed_url


def test_seed_url_prepend(base_url, driver):
    url_template = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = url_template

    page = MyPage(driver, base_url)
    assert base_url + url_template == page.seed_url


def test_open(page):
    assert isinstance(page.open(), Page)


def test_open_seed_url_none(driver):

    page = Page(driver)
    with pytest.raises(UsageError):
        page.open()


def test_open_timeout(base_url, driver):
    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)

    page = MyPage(driver, base_url, timeout=0)

    with pytest.raises(TimeoutException):
        page.open()


def test_open_timeout_loaded(base_url, driver):
    class MyPage(Page):
        @property
        def loaded(self):
            return False

    page = MyPage(driver, base_url, timeout=0)

    with pytest.raises(TimeoutException):
        page.open()


def test_wait_for_page(page):
    assert isinstance(page.wait_for_page_to_load(), Page)


def test_wait_for_page_timeout(base_url, driver):
    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)

    page = MyPage(driver, base_url, timeout=0)

    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_timeout_loaded(base_url, driver):
    class MyPage(Page):
        @property
        def loaded(self):
            return False

    page = MyPage(driver, base_url, timeout=0)

    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_empty_base_url(driver):
    assert isinstance(Page(driver).wait_for_page_to_load(), Page)


def test_loaded(page):
    assert page.loaded is True
