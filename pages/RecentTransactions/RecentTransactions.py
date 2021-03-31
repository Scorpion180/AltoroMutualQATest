import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import datetime

import time


class RecentTransactions(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver

    # Locators

    RECENT_TRANSACTIONS = 'View Recent Transactions'
    RECENT_TRANSACTIONS_LOCATOR = 'link'

    AFTER_DATE = 'startDate'
    AFTER_DATE_LOCATOR = 'id'

    BEFORE_DATE = 'endDate'
    BEFORE_DATE_LOCATOR = 'id'

    SUBMIT_DATE = '//input[@value=\'Submit\']'
    SUBMIT_DATE_LOCATOR = 'xpath'

    TABLE = '//table[contains(@id,\'MyTransactions\')]//tbody//tr'
    TABLE_LOCATOR = 'xpath'

    def clickRecentTransactions(self):
        self.elementClick(self.RECENT_TRANSACTIONS, self.RECENT_TRANSACTIONS_LOCATOR)

    def sendAfterDate(self, date):
        self.sendKeys(date, self.AFTER_DATE, self.AFTER_DATE_LOCATOR)

    def sendBeforeDate(self, date):
        self.sendKeys(date, self.BEFORE_DATE, self.BEFORE_DATE_LOCATOR)

    def clickSubmitDate(self):
        self.elementClick(self.SUBMIT_DATE, self.SUBMIT_DATE_LOCATOR)

    def clickAlert(self):
        alert1 = self.driver.switch_to.alert
        alert1.accept()

    def check_afterDate(self, date):
        self.clickRecentTransactions()
        self.sendAfterDate(date)
        self.clickSubmitDate()

    def check_beforeDate(self, date):
        self.clickRecentTransactions()
        self.sendBeforeDate(date)
        self.clickSubmitDate()

    def check_dates(self, after, before):
        self.clickRecentTransactions()
        self.sendBeforeDate(before)
        self.sendAfterDate(after)
        self.clickSubmitDate()

    def clearRecentTransactionsFields(self):
        after = self.getElement(self.AFTER_DATE, self.AFTER_DATE_LOCATOR)
        before = self.getElement(self.BEFORE_DATE, self.BEFORE_DATE_LOCATOR)
        after.clear()
        before.clear()

    def verify_invalidDate(self):
        return self.waitForAlert()

    def verify_validDate(self):
        if self.waitForAlert():
            return False
        return True

    def verify_datesOnTable(self, after='', before='', type=''):

        if after != '':
            dateArray = after.split('-')
            _after = datetime.datetime(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))

        if before != '':
            dateArray = before.split('-')
            _before = datetime.datetime(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))

        tableRows = self.getElementList(self.TABLE, self.TABLE_LOCATOR)
        #Delete first element because it's the header
        del tableRows[0]
        for row in tableRows:
            if row.text != '':
                dateArray = row.text.split()[1].split('-')
                _date = datetime.datetime(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))
                if type == "AFTER":
                    if _after > _date:
                        self.log.error('Found invalid date, filter', _after, 'date ', _date)
                        return False
                elif type == 'BEFORE':
                    if _before < _date:
                        self.log.error('Found invalid date, filter', _after, 'date ', _date)
                        return False
                elif type == 'BOTH':
                    if _before < _date or _after > _date:
                        self.log.error('Found invalid date, filter', _after, _before, 'date ', _date)
                        return False
        self.log.info('No invalid date found')
        return True
