"""
Selenium maintains a library of wait conditions under the support module.
However, custom wait conditions can be created when none of the convenience methods
fit. A custom wait condition can be created using a class with a __call__ method which reutrns False
when the condition does not match.
"""


class LazyLoadElementHasDataCondition(object):
    """
    A custom wait condition to check if the lazy loaded element has data.

    Attributes:
        locator (tuple): locator to find the root element, see `Locators`_ design pattern.
        data_selector (str): css selector to find the data elements from the :attr:`locator`.

    .. _Locators:
        http://selenium-python.readthedocs.io/selenium_page-objects.html#locators
    """

    def __init__(self, locator, data_selector):
        self.locator = locator
        self.data_selector = data_selector

    def __call__(self, driver):
        lazy_element = driver.find_element(*self.locator)
        data_elements = lazy_element.find_elements_by_css_selector(self.data_selector)
        if any([self._check(d) for d in data_elements]):
            return True
        return False

    def _check(self, element):
        return bool(element.text)


class LazyLoadInputElementHasDataCondition(LazyLoadElementHasDataCondition):
    """
    Similar to :class:`LazyLoadElementHasDataCondition` only checks for value instead of text.
    """
    def _check(self, element):
        value = element.get_attribute('value')
        return bool(value)
