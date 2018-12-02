"""
These tests the base classes and show a demo implementation of the locator -> element -> page
design pattern.
"""
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


# Import selenium page from context which sets the test path
from tests.context import BasePage, BasePageElement, BasePageElements

from tests.locators import GoogleHomeLocators, MozillaSelectLocators


# Create data-descriptor with the locator of the search box
class GoogleSearchBoxElement(BasePageElement):
    locator = GoogleHomeLocators.search_box


# Create data-descriptor with the locator of the search button
class GoogleSearchButton(BasePageElement):
    locator = GoogleHomeLocators.search_btn

# Trying to get this element results in a timeout exception.
class GoogleDoesNotExist(BasePageElement):
    locator = GoogleHomeLocators.raises_error


# Define a GoogleHomePage selenium_page using the BasePage and the above descriptors
class GoogleHomePage(BasePage):
    search_box = GoogleSearchBoxElement()
    search_button = GoogleSearchButton()
    raises_error = GoogleDoesNotExist(max_wait_time=1)


class BasePageTest(unittest.TestCase):
    def setUp(self):
        chrome_path = Path(r'./drivers/chromedriver.exe')
        browser = webdriver.Chrome(executable_path=str(chrome_path.absolute()))
        self.browser = browser

    def tearDown(self):
        self.browser.close()

    def test_base_page(self):
        browser = self.browser
        browser.get('https://www.google.com/')
        google_home = GoogleHomePage(browser)
        google_home.search_box = 'Selenium'
        google_home.search_button.submit()

    def test_timeout(self):
        with self.assertRaises(TimeoutException):
            browser = self.browser
            browser.get('https://www.google.com/')
            google_home = GoogleHomePage(browser)
            google_home.raises_error


# Create a data descriptor with the location of the select box
class MozillaSelectElement(BasePageElement):
    locator = MozillaSelectLocators.select_input


# Create an additional descriptor using the Elements object
# Note the array will be length 1
class MozillaSelectElements(BasePageElements):
    locator = 'select[name="select"]'


# Create the page for the select test
class MozillaSelectTestPage(BasePage):
    select_input = MozillaSelectElement()
    select_inputs = MozillaSelectElements()


class SelectElementTest(unittest.TestCase):
    def setUp(self):
        chrome_path = Path(r'./drivers/chromedriver.exe')
        browser = webdriver.Chrome(executable_path=str(chrome_path.absolute()))
        self.browser = browser

    def tearDown(self):
        self.browser.close()

    def test_select_element_get(self):
        browser = self.browser
        browser.get('https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select')
        mozilla_select_test_page = MozillaSelectTestPage(browser)
        element = mozilla_select_test_page.select_input
        self.assertIsInstance(element, Select)

    def test_select_elements_get(self):
        browser = self.browser
        browser.get('https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select')
        mozilla_select_test_page = MozillaSelectTestPage(browser)
        elements = mozilla_select_test_page.select_inputs
        self.assertIsInstance(elements, list)
        self.assertEqual(len(elements), 1)
        self.assertIsInstance(elements[0], Select)

    def test_select_element_set(self):
        browser = self.browser
        browser.get('https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select')
        mozilla_select_test_page = MozillaSelectTestPage(browser)
        mozilla_select_test_page.select_input = 'third'
        # Validate the value changed
        select = mozilla_select_test_page.select_input
        value = select.all_selected_options[0].get_attribute('value')
        self.assertEqual(value, 'third')

    def test_select_elements_set(self):
        browser = self.browser
        browser.get('https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select')
        mozilla_select_test_page = MozillaSelectTestPage(browser)
        mozilla_select_test_page.select_inputs = 'third'
        # Validate the value changed
        select = mozilla_select_test_page.select_inputs[0]
        value = select.all_selected_options[0].get_attribute('value')
        self.assertEqual(value, 'third')
