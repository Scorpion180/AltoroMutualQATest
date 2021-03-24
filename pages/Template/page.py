import utilities.custom_logger as cl
import logging
from base.basepage import BasePage


class Page(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver


