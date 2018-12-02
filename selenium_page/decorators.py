from functools import wraps

from selenium.webdriver.support.ui import WebDriverWait


def scroll_to_element(element):
    """
    Decorator to execute a function only when an element is in view

    Args:
        element: The element to bring in to view
    """
    def wrap(func):

        @wraps(func)
        def wrapper(instance, *args):
            if not element.is_displayed():
                element.parent.execute_script(
                    'arguments[0].scrollIntoView();', element
                )
            return func(instance, *args)

        return wrapper

    return wrap


def wait_until_condition(condition, timeout=10):
    """
    Decorator to execute a function only after a condition is met.

    A condition is any object with a call method returning True or False. See the
    :class:`LazyLoadElementHasDataCondition` example.

    Args:
        condition (object): The condition to check
        timeout (int, optional): Time in seconds before condition times out in failure

    """
    def wrap(func):

        @wraps(func)
        def wrapper(instance, *args):
            wait = WebDriverWait(instance.driver, timeout)
            wait.until(condition)
            result = func(instance, *args)
            return result

        return wrapper

    return wrap


def wrapper(func, *args, **kwargs):
    @wraps(func)
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def coroutine(func):
    """
    Decorator to create a co-routine (automatically primes it).

    Args:
        func (Coroutine): co-routine to be primed

    Returns:
        Coroutine: primed co-routine.
    """
    @wraps(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        # Prime the co-routine
        next(cr)
        return cr
    return start
