# Selenium Page

## Purpose

Collection of base classes and utilities to use when following the locator
-> element -> page design pattern.

Example:

Setup
```python
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium_page.page.page import BasePage
from selenium_page.page.element import BasePageElement
```
Create a class to hold the locators
```python
class GoogleHomeLocators(object):
    search_box = (By.ID, 'lst-ib')
    search_btn = (By.NAME, 'btnK')
```
Create data-descriptor with the locator of the search box
```python
class GoogleSearchBoxElement(BasePageElement):
    locator = GoogleHomeLocators.search_box
```
Create data-descriptor with the locator of the search button
```python
class GoogleSearchButton(BasePageElement):
    locator = GoogleHomeLocators.search_btn
```
Define a GoogleHomePage page using the BasePage and the above descriptors
```python
class GoogleHomePage(BasePage):
    search_box = GoogleSearchBoxElement()
    search_button = GoogleSearchButton()
```
Obtain a browser object
```python
chrome_path = Path(r'./drivers/chromedriver.exe')
browser = webdriver.Chrome(executable_path=str(chrome_path.absolute()))
browser.get('https://www.google.com/')
```
Create a page instance
```python
google_home = GoogleHomePage(browser)
```
Using the data-descriptor easily set the search box value
```python
google_home.search_box = 'Selenium'
google_home.search_button.submit()
```


### Documentation

Repository documentation can be found [here]()
TODO: Host the docs
