import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage


class JobsPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver
        self.Error = 'None'

    # Locators

    CAREERS = 'MenuHyperLink18'
    CAREERS_LOCATOR = 'id'

    JOBS = 'Current Job Openings'
    JOBS_LOCATOR = 'link'

    JOBS_TABLE = '//div[@class=\'fl\']//table'
    JOBS_TABLE_LOCATOR = 'xpath'

    CATEGORY = '//div[@class=\'fl\']//table//tr[1]//td[2]'
    CATEGORY_LOCATOR = 'xpath'

    DATE = '//div[@class=\'fl\']//table//tr[2]//td[2]'
    DATE_LOCATOR = 'xpath'

    CONTENT_TITLE = '//div[@class=\'fl\']//h1'
    CONTENT_TITLE_LOCATOR = 'xpath'

    def clickCareers(self):
        self.elementClick(self.CAREERS, self.CAREERS_LOCATOR)

    def clickJobOpenings(self):
        self.elementClick(self.JOBS, self.JOBS_LOCATOR)

    def writeBrokenContent(self, header, message):
        self.Error += header + message + ' | '
        self.screenShot(header + message)

    def verifyJobInfo(self, category, date, title):
        _category = self.getElement(self.CATEGORY, self.CATEGORY_LOCATOR)
        _date = self.getElement(self.DATE, self.DATE_LOCATOR)
        _title = self.getElement(self.CONTENT_TITLE, self.CONTENT_TITLE_LOCATOR)
        if self.util.verifyTextMatch(category, self.getText(element=_category)) and \
                self.util.verifyTextMatch(date, self.getText(element=_date)) and \
                self.util.verifyTextMatch(title, _title.text):
            self.writeBrokenContent(title, '_info_wrong')

    def jobsTableValues(self):
        self.Error = ''
        table = self.getElement(self.JOBS_TABLE, self.JOBS_TABLE_LOCATOR)
        for row in table.find_elements_by_xpath('.//tr[not(@class)]'):
            info = row.find_elements_by_xpath(".//td")
            category = self.getText(element=info[0])
            date = self.getText(element=info[1])
            title = self.getText(element=info[2])
            link = info[2].find_element_by_xpath('.//a').get_property('href')
            self.executeScript('window.open("' + link + '","_blank");')
            windows = self.driver.window_handles
            self.switchToWindow(windows[1])
            self.verifyJobInfo(category, date, title)
            self.driver.close()
            self.switchToWindow(windows[0])

    def check_jobOpenings(self):
        self.clickCareers()
        self.clickJobOpenings()
        self.jobsTableValues()

    def verify_correctInfo(self):
        if self.util.verifyTextMatch(self.Error, ''):
            return True
        return False
