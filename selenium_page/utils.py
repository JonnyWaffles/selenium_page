import re
from time import sleep

from selenium.common.exceptions import (ElementClickInterceptedException, ElementNotVisibleException)


from .decorators import coroutine


def safe_send_keys(elem, keys):
    elem.clear()
    elem.send_keys(keys)


def make_valid_field_names(names):
    ret = []
    unknown_field_counter = 1
    for name in names:
        name = name.strip()
        if name == '':
            name = 'unnamed' + str(unknown_field_counter)
            unknown_field_counter += 1
        else:
            name = name.replace('#', 'number')
            name = clean(name)
            name = name.lower()
        ret.append(name)
    return ret


def clean(s):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)

    # Remove leading characters until we find a letter
    s = re.sub('^[^a-zA-Z]+', '', s)

    return s


def chunks(l, n):
    """
    Yields successive n-sized chunks from list
    credit to `Ned Batchelder`_

    Args:
        l (iterable): An iterable to be split in to n sized chunks
        n (int): The size of the yielded chunks

    Yields:
        list: An n-sized list

    .. _Ned Batchelder:
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


@coroutine
def unique_key_generator(dictionary):
    """This generator object creates unique keys for the target dictionary.

    If the key already exists in the dictionary it appends the number
    of occurrences to the key name. Useful when creating search results identifiers.

    Args:
        dictionary (dict): The target dictionary to check

    Yields:
        str: A unique key name
    """
    duplicate_keys = {}
    # prime the key variable
    key = None
    while True:
        key = (yield key)
        if dictionary.get(key, None):
            count = duplicate_keys.get(key, None) or 1
            count += 1
            duplicate_keys[key] = count
            key = key + "_{}".format(str(count))


def scroll_to_click_element_until_timeout(element, timeout=10):
    """Attempts to click an element until timeout.

    Scrolls to the element until the click succeeds or timeout.

    Args:
        element: Element to be clicked
        timeout: Time before failure occurs
    """
    driver = element.parent
    counter = 0
    while True:
        try:
            element.click()
            return
        except (ElementClickInterceptedException,
                ElementNotVisibleException):
            driver.execute_script('arguments[0].scrollIntoView();', element)
            counter += 1
            if counter > timeout:
                break
            sleep(1)
