[![PyPI Version](https://img.shields.io/pypi/v/pypom-selenium)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pypom-selenium)
![PyPI - License](https://img.shields.io/pypi/l/pypom-selenium)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypom-selenium)](https://pypi.python.org/pypi/pypom-selenium)

# Selenium PyPOM
Selenium PyPOM is a Python Page Object Model library for Selenium. It presents a thin interface for implementing the page object model design pattern. The project is built based on [mozilla/PyPOM](https://github.com/mozilla/PyPOM), all credit goes to the authors.

This project is licensed under the Mozilla Public License version 2.0.

## Table of Contents
- [Installation](#installation)
- [User Guide](#user-guide)
    - [Drivers](#drivers)
    - [Pages](#pages)
        - [Base URL](#base-url)
        - [URL templates](#url-templates)
        - [URL parameters](#url-parameters)
        - [Waiting for pages to load](#waiting-for-pages-to-load)
    - [Regions](#regions)
        - [Root elements](#root-elements)
        - [Repeating regions](#repeating-regions)
        - [Nested regions](#nested-regions)
        - [Shared regions](#shared-regions)
        - [Waiting for regions to load](#waiting-for-regions-to-load)


## Installation
Selenium PyPOM requires Python >= 3.8  
To install PyPOM using [pip](https://pip.pypa.io/)
```sh
pip install pypom-selenium
```

## User Guide

### Drivers
PyPOM requires a driver object to be instantiated, and supports multiple driver types. The examples in this guide will assume that you have a driver instance.

To instantiate a Selenium driver you will need a `~selenium.webdriver.remote.webdriver.WebDriver` object
```py
  from selenium.webdriver import Firefox
  driver = Firefox()
```

### Pages
Page objects are representations of web pages. They provide functions to allow simulating user actions, and providing properties that return state from the page. The `~pypom.page.Page` class provided by PyPOM provides a simple implementation that can be sub-classed to apply to your project.

The following very simple example instantiates a page object representing the
landing page of the Mozilla website
```py
  from pypom import Page

  class Mozilla(Page):
      pass

  page = Mozilla(driver)
```
If a page has a seed URL then you can call the `~pypom.page.Page.open`
function to open the page in the browser. There are a number of ways to specify
a seed URL.

#### Base URL
A base URL can be passed to a page object on instantiation. If no URL template
is provided, then calling `~pypom.page.Page.open` will open this base
URL
```py
  from pypom import Page

  class Mozilla(Page):
      pass

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url).open()
```

#### URL templates
By setting a value for `~pypom.page.Page.URL_TEMPLATE`, pages can specify either an absolute URL or one that is relative to the base URL (when provided). In the following example, the URL https://www.mozilla.org/about/
will be opened
```py
  from pypom import Page

  class Mozilla(Page):
      URL_TEMPLATE = '/about/'

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url).open()
```

As this is a template, any additional keyword arguments passed when instantiating the page object will attempt to resolve any placeholders. In the following example, the URL https://www.mozilla.org/de/about/ will be opened
```py
  from pypom import Page

  class Mozilla(Page):
      URL_TEMPLATE = '/{locale}/about/'

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url, locale='de').open()
```

#### URL parameters
Any keyword arguments provided that are not used as placeholders in the URL template are added as query string parameters. In the following example, the URL https://developer.mozilla.org/fr/search?q=bold&topic=css will be opened
```py
  from pypom import Page

  class Search(Page):
      URL_TEMPLATE = '/{locale}/search'

  base_url = 'https://developer.mozilla.org/'
  page = Search(driver, base_url, locale='fr', q='bold', topic='css').open()
```

#### Waiting for pages to load
Whenever a driver detects that a page is loading, it does its best to block until it's complete. Unfortunately, as the driver does not know your application, it's quite common for it to return earlier than a user would consider the page to be ready. For this reason, the `~pypom.page.Page.loaded` property can be overridden and customised
for your project's needs by returning `True` when the page has loaded. This property is polled by `~pypom.page.Page.wait_for_page_to_load`, which is called by `~pypom.page.Page.open` after loading the seed URL, and can be called directly by functions that cause a page to load.

The following example waits for the seed URL to be in the current URL. You can
use this so long as the URL is not rewritten or redirected by your
application
```py
  from pypom import Page

  class Mozilla(Page):

      @property
      def loaded(self):
          return self.seed_url in self.selenium.current_url
```

Other things to wait for might include when elements are displayed or enabled,
or when an element has a particular class. This will be very dependent on your
application.

### Regions
Region objects represent one or more elements of a web page that are repeated multiple times on a page, or shared between multiple web pages. They prevent duplication, and can improve the readability and maintainability of your page objects.

#### Root elements
It's important for page regions to have a root element. This is the element that any child elements will be located within. This means that page region locators do not need to be unique on the page, only unique within the context of the root element.

If your page region contains a `~pypom.region.Region._root_locator` attribute, this will be used to locate the root element every time an instance of the region is created. This is recommended for most page regions as it avoids issues when the root element becomes stale.

Alternatively, you can locate the root element yourself and pass it to the region on construction. This is useful when creating regions that are repeated on a single page.

The root element can later be accessed via the `~pypom.region.Region.root` attribute on the region, which may be necessary if you need to interact with it.

#### Repeating regions
Page regions are useful when you have multiple items on a page that share the
same characteristics, such as a list of search results. By creating a page
region, you can interact with any of these items in a common way:

The following example uses Selenium to locate all results on a page and return a list of `Result` regions. This can be used to determine the number of results, and each result can be accessed from this list for further state or interactions.
```html
<!DOCTYPE html>
<html lang="en">
<body>
<h1>Repeated Regions Example</h1>

<ol>
    <li class="result">
        <span class="name">Result 1</span>
        <a href="./detail/1/">detail</a>
    </li>
    <li class="result">
        <span class="name">Result 2</span>
        <a href="./detail/2/">detail</a>
    </li>
    <li class="result">
        <span class="name">Result 3</span>
        <a href="./detail/3/">detail</a>
    </li>
    <li class="result">
        <span class="name">Result 4</span>
        <a href="./detail/4/">detail</a>
    </li>
</ol>

</body>
</html>
```
```py
from pypom import Page, Region
from selenium.webdriver.common.by import By


class Results(Page):
    _result_locator = (By.CLASS_NAME, "result")

    @property
    def results(self):
        return [
            self.Result(self, el) for el in self.find_elements(*self._result_locator)
        ]

    class Result(Region):
        _name_locator = (By.CLASS_NAME, "name")
        _detail_locator = (By.TAG_NAME, "a")

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def detail_link(self):
            return self.find_element(*self._detail_locator).get_property("href")
```

#### Nested regions
Regions can be nested inside other regions (i.e. a menu region with multiple entry regions). In the following example a main page contains two menu regions that include multiple repeated entry regions:

```html
<!DOCTYPE html>
<html lang="en">
<body>
<h1>Nested Regions Example</h1>
<div id="page">Main Page

    <div id="menu1" class="menu">
        <ol>
            <li class="entry">Menu1-Entry1</li>
            <li class="entry">Menu1-Entry2</li>
            <li class="entry">Menu1-Entry3</li>
            <li class="entry">Menu1-Entry4</li>
            <li class="entry">Menu1-Entry5</li>
        </ol>
    </div>
    <div id="menu2" class="menu">
        <ol>
            <li class="entry">Menu2-Entry1</li>
            <li class="entry">Menu2-Entry2</li>
            <li class="entry">Menu2-Entry3</li>
        </ol>
    </div>
</div>
</body>
</html>
```

As a region requires a page object to be passed you need to pass `self.page` when instantiating nested regions:

```py
from pypom import Region, Page
from selenium.webdriver.common.by import By


class MainPage(Page):
    @property
    def menu1(self):
        root = self.find_element(By.ID, "menu1")
        return Menu(self, root=root)

    @property
    def menu2(self):
        root = self.find_element(By.ID, "menu2")
        return Menu(self, root=root)


class Menu(Region):
    @property
    def entries(self):
        return [
            Entry(self.page, item) for item in self.find_elements(*Entry.entry_locator)
        ]


class Entry(Region):
    entry_locator = (By.CLASS_NAME, "entry")

    @property
    def name(self):
        return self.root.text
```


#### Shared regions
Pages with common characteristics can use regions to avoid duplication. Examples of this include page headers, navigation menus, login forms, and footers. These regions can either be defined in a base page object that is inherited by the pages that contain the region, or they can exist in their own module:

In the following example, any page objects that extend `Base` will inherit
the `header` property, and be able to check if it's displayed.
```py
  from pypom import Page, Region
  from selenium.webdriver.common.by import By

  class Base(Page):

      @property
      def header(self):
          return self.Header(self)

      class Header(Region):
          _root_locator = (By.ID, 'header')

          def is_displayed(self):
              return self.root.is_displayed()
```

#### Waiting for regions to load
The `~pypom.region.Region.loaded` property function can be overridden and customised for your project's needs by returning `True` when the region has loaded to ensure it's ready for interaction. This property is polled by :py:attr:`~pypom.region.Region.wait_for_region_to_load`, which is called whenever a region is instantiated, and can be called directly by functions that a region to reload.

The following example waits for an element within a page region to be displayed
```py
  from pypom import Region

  class Header(Region):

      @property
      def loaded(self):
          return self.root.is_displayed()
```

Other things to wait for might include when elements are displayed or enabled, or when an element has a particular class. This will be very dependent on your application.

## Development
### Running Tests
You will need Tox installed to run the tests against the supported Python versions.
```sh
$ python -m pip install tox
$ tox
```

## Release Notes
### 1.0.0 (2024-08-06)
First official release.

### 1.1.0 (2024-08-06)
Add support for python 3.10.  
The project now officially supports versions 3.8, 3.9, 3.11 and 3.12.