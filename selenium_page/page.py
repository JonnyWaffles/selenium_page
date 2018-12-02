from collections import namedtuple, OrderedDict

from .utils import unique_key_generator, chunks, make_valid_field_names


class BasePage(object):
    """Base class to init the base selenium_page will be called from all pages

    Attributes:
        driver (:class:`selenium.webdriver`): browser instance
    """

    def __init__(self, driver):
        self.driver = driver
        self.main_window_handle = driver.current_window_handle

    @staticmethod
    def get_element_next_sibling(element):
        """
        Helper function to return the next sibling from element

        Args:
            element: A web element
        Returns:
            element: Sibling element
        """
        sibling = element.find_element_by_xpath('following-sibling::*[1]')
        return sibling

    def _change_window(self):
        """Selects the other window, assuming only two handles are present.

        Raises:
            AssertionError: When more than 2 handles are present
        """
        driver = self.driver
        current_window_handle = driver.current_window_handle

        handles = driver.window_handles

        assert len(handles) == 2, (
            'Expected two handles found {}, '
            'unable to determine note pop-up'.format(
                len(handles)
            )
        )

        for handle in handles:
            if handle != current_window_handle:
                driver.switch_to_window(handle)

    def _select_main_window(self):
        """Selects the main window
        """
        self.driver.switch_to.window(self.main_window_handle)


class BaseResultsPage(BasePage):
    """
    Base class for single table results pages like Invoices, Matters, etc.

    If only one data element is found in the table_data, row_objects will empty.

    Attributes:
        table_data (list(elements)): A list of data elements
        table_headers (list(elements)): A list of table header elements
        data_name (str): Name for the container class
        key_field_index (int): Index of the field to use as the container instance's key.
            Note: The objects will exist in the class instance's 'row_objects' attribute.
        row_objects (:class:`OrderedDict` of :class:`namedtuple`): An ordered dictionary of results objects
            as namedtuples. The key_field_index will be used to generate key names. If a key is duplicated,
            for example multiple invoice results with the same invoice number, a postfix counting the occurrences will
            be inserted by a :func:`unique_key_generator` so each result row maintains a unique key.
    """
    table_body = None
    table_data = None
    table_headers = None
    data_name = 'Container'
    key_field_index = 0

    def __init__(self, driver):
        super().__init__(driver)
        self.row_objects = self._get_row_objects()

    def _build_data_container(self):
        names = [h.text for h in self.table_headers]
        field_names = make_valid_field_names(names)
        return namedtuple(self.data_name, field_names)

    def _get_row_objects(self):
        container = self._build_data_container()
        row_dict = OrderedDict()

        # It isn't enough to use rows, because some results pages split a single
        # object's data across multiple rows. Chunking is more reliable.
        generator = chunks(self.table_data, len(container._fields))

        # create a co-routine instance that checks our row_dict
        unique_key_coroutine = unique_key_generator(row_dict)

        for data_set in generator:
            data_count, field_count = len(data_set), len(container._fields)
            # Handle 1 returned element, which indicates no results
            if data_count == 1:
                return row_dict

            # If we have results, make sure the headers and data match
            assert data_count == field_count, (
                '{} data elements found in a set but {} object has {} fields'.format(
                    data_count, container, field_count
                )
            )

            container_obj = container(*data_set)
            key_text = container_obj[self.key_field_index].text

            # Insure a unique key
            key = unique_key_coroutine.send(key_text)

            row_dict[key] = container_obj

        return row_dict
