"""This module contains the base classes for instantiating page objects.
"""
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select as BaseSelect

from selenium_page.settings import DEFAULT_WAIT_TIME

from selenium_page.utils import safe_send_keys


class Select(BaseSelect):
    """For some dumb reason the Select wrapper does grant access
    to all the methods of the wrapped webelement, so manually
    set references here.

    Attributes:
          get_attribute (:meth:`~selenium.webdriver.remove.webelement.get_attribute`):
            The wrapped element's get_attribute method.
    """
    def __init__(self, webelement):
        super(Select, self).__init__(webelement)
        self.get_attribute = self._el.get_attribute


class BasePageElement(object):
    """'
    Page classes use data descriptor protocol to interact with their various elements.

    This is the base element data descriptor class.

    All concrete BasePageElement classes must have a `locator`_ class attribute.

    If the located element is a ``<select>`` a :class:`~selenium.webdriver.support.select.Select`
    webelement will be used.

    Attributes:
        locator: The locator to select the element.
        max_wait_time: The maximuum time to try and get an element. Defaults to 100 seconds.

    Example:
        Consider the following element class with a made up locator object.::

            class UserNameElement(BasePageElement):
                locator = 'userName'

            class LoginPage(BasePage):
                username_input = UserNameElement()

            login_page = LoginPage()

            # The below command will set the value on the element located by the data-descriptor
            login_page.username_input = 'My UserName'

    .. _locator:
        http://selenium-python.readthedocs.io/selenium_page-objects.html#locators

    Raises:
        :exc:`~selenium.common.exceptions.TimeoutException`: When the element cannot be found within the
            :attr:`max_wait_time`.
    """
    locator = None

    def __init__(self, max_wait_time: int=DEFAULT_WAIT_TIME):
        self.max_wait_time = max_wait_time

    def _get_find_element_func(self):
        """
        Helper function returns the appropriate driver function
        based on the descriptor's location attribute

        Returns:
            function: find element function to execute after wait.
        """
        if isinstance(self.locator, str):
            return lambda driver: driver.find_element_by_name(self.locator)
        elif isinstance(self.locator, tuple):
            return lambda driver: driver.find_element(*self.locator)
        else:
            raise AttributeError(
                '{} does not define a locator class attribute as str or tuple.'.format(
                    self.__class__.__name__
                )
            )

    def _wait(self, driver):
        """
        Checks for the element until it exists, or times out.
        Args:
            driver (:class:`selenium.driver`): browser instance
        """
        WebDriverWait(driver, self.max_wait_time).until(
            self._get_find_element_func()
        )

    def _wait_then_get_elem(self, instance):
        driver = instance.driver
        self._wait(driver)
        element_finder = self._get_find_element_func()
        element = element_finder(driver)
        # Check for selects
        if element.tag_name == 'select':
            element = Select(element)
        return element

    @staticmethod
    def _element_settr(element, value):
        """Helper function to handle setting :class:`~selenium.webdriver.support.select.Select`"""
        if isinstance(element, Select):
            element.select_by_value(value)
        else:
            safe_send_keys(element, value)

    def __set__(self, instance, value):
        """Sets the element to the value supplied"""
        element = self._wait_then_get_elem(instance)
        self._element_settr(element, value)

    def __get__(self, instance, owner) -> WebElement:
        """Returns the element after a delay"""
        element = self._wait_then_get_elem(instance)
        return element


class ReadonlyPageElement(BasePageElement):
    """Readonly data descriptor"""
    def __set__(self, instance, value):
        raise NotImplementedError(
            'This element is readonly.'
        )


class BasePageElements(BasePageElement):
    """
    Similar to the above, but uses find_elements to return lists
    rather than find_element which returns specific nodes. Uses CSS
    rather than name if locator is string.
    """
    def _get_find_element_func(self):
        """
        Helper function returns the appropriate driver function
        based on the descriptor's location attribute

        Returns:
            function: find element function to execute after wait.
        """
        if isinstance(self.locator, str):
            return lambda driver: driver.find_elements_by_css_selector(self.locator)
        elif isinstance(self.locator, tuple):
            return lambda driver: driver.find_elements(*self.locator)
        else:
            raise AttributeError(
                '{} does not define a locator class attribute as str or tuple.'.format(
                    self.__class__.__name__
                )
            )

    def _wait_then_get_elem(self, instance):
        driver = instance.driver
        self._wait(driver)
        element_finder = self._get_find_element_func()
        elements = element_finder(driver)
        # Replace element instances with select instances
        for (index, element) in enumerate(elements):
            if element.tag_name == 'select':
                elements[index] = Select(element)
        return elements

    def __set__(self, instance, value):
        """
        If value is an interable, place each value in each element, or if value
        is a non-iterable or string set all the elements to the value.

        Args:
            instance (:class:`selenium_page.selenium_page.BasePage'): Instance whose value will be set
            value: The value to set on the instance
        """
        elements = self._wait_then_get_elem(instance)
        generator = (e for e in elements)
        # is iterable
        if hasattr(value, '__next__') and not isinstance(value, str):
            # fill in each element with an iterable from value
            try:
                for v in value:
                    element = next(generator)
                    self._element_settr(element, v)
            except StopIteration:
                raise ValueError(
                    '{} values but only {} elements, unable to assign one to one.'.format(
                        len(value), len(elements)
                    )
                )
        else:
            for e in generator:
                self._element_settr(e, value)


class ReadonlyPageElements(BasePageElements):
    def __set__(self, instance, value):
        raise NotImplementedError(
            'These elements are readonly.'
        )
