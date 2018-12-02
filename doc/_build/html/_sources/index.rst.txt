.. Selenium Page documentation master file, created by
   sphinx-quickstart on Fri Jan 19 10:50:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Selenium Page's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   page



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Getting started
---------------
Example:

Setup::

    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    from selenium_page.page import BasePage
    from selenium_page.element import BasePageElement

Create a class to hold the locators::

    class GoogleHomeLocators(object):
        search_box = (By.ID, 'lst-ib')
        search_btn = (By.NAME, 'btnK')

Create data-descriptor with the locator of the search box::

    class GoogleSearchBoxElement(BasePageElement):
        locator = GoogleHomeLocators.search_box

Create data-descriptor with the locator of the search button::

    class GoogleSearchButton(BasePageElement):
        locator = GoogleHomeLocators.search_btn

Define a GoogleHomePage page using the BasePage and the above descriptors::

    class GoogleHomePage(BasePage):
        search_box = GoogleSearchBoxElement()
        search_button = GoogleSearchButton()

Obtain a browser object::

    chrome_path = Path(r'./drivers/chromedriver.exe')
    browser = webdriver.Chrome(executable_path=str(chrome_path.absolute()))
    browser.get('https://www.google.com/')

Create a page instance::

    google_home = GoogleHomePage(browser)

Using the data-descriptor easily set the search box value::

    google_home.search_box = 'Selenium'
    google_home.search_button.submit()

