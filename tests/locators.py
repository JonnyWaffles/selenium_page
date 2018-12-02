from selenium.webdriver.common.by import By


class GoogleHomeLocators(object):
    search_box = (By.ID, 'lst-ib')
    search_btn = (By.NAME, 'btnK')
    raises_error = (By.ID, 'ThisElementDoesNotExist')


class MozillaSelectLocators(object):
    select_input = (By.NAME, 'select')
