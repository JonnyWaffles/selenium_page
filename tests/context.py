"""
Following best `practice`_, context ensures the tests always work, regardless of the installation
method.

.. _practice:
    http://docs.python-guide.org/en/latest/writing/structure/#test-suite
"""
from pathlib import Path
import sys
# Make sure the repo root is on the Path by moving two levels up
root_path = Path(__file__).parents[1]

sys.path.insert(0, str(root_path))

from selenium_page.page import BasePage
from selenium_page.element import BasePageElement, BasePageElements