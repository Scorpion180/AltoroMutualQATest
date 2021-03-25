import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import requests

import time

class MainPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver
        self.brokenLinks = 'None'

    #Locators

    LOGIN = 'ONLINE BANKING LOGIN'
    LOGIN_LOCATOR = 'link'

    LOGOUT = 'LoginLink'
    LOGOUT_LOCATOR = 'id'

    USERNAME = 'uid'
    USERNAME_LOCATOR = 'id'

    PASSWORD = 'passw'
    PASSWORD_LOCATOR = 'id'

    LOGIN_BTN = 'btnSubmit'
    LOGIN_BTN_LOCATOR = 'name'

    LOGIN_FAILED = '//span[contains(text(),\'Login Failed\')]'
    LOGIN_FAILED_LOCATOR = 'xpath'

    LOGIN_SUCCESSFUL = 'AccountLink'
    LOGIN_SUCCESSFUL_LOCATOR = 'id'

    RECENT_TRANSACTIONS = 'View Recent Transactions'
    RECENT_TRANSACTIONS_LOCATOR = 'link'

    AFTER_DATE = 'startDate'
    AFTER_DATE_LOCATOR = 'id'

    SUBMIT_DATE = '//input[@value=\'Submit\']'
    SUBMIT_DATE_LOCATOR = 'xpath'

    def clickLogin(self):
        self.elementClick(self.LOGIN, self.LOGIN_LOCATOR)

    def sendCredentials(self, userName, password):
        self.sendKeys(userName, self.USERNAME, self.USERNAME_LOCATOR)
        self.sendKeys(password, self.PASSWORD, self.PASSWORD_LOCATOR)

    def clickLoginButton(self):
        self.elementClick(self.LOGIN_BTN, self.LOGIN_BTN_LOCATOR)

    def logOut(self):
        self.elementClick(self.LOGOUT, self.LOGOUT_LOCATOR)

    def check_Login(self, userName, password):
        self.clickLogin()
        self.sendCredentials(userName, password)
        self.clickLoginButton()

    def verifyLoginSuccessful(self, _logOut = True):
        result = self.elementPresenceCheck(self.LOGIN_SUCCESSFUL, self.LOGIN_SUCCESSFUL_LOCATOR)
        if _logOut:
            self.logOut()
        return result

    def verifyLoginFailed(self):
        result = self.elementPresenceCheck(self.LOGIN_FAILED, self.LOGIN_FAILED_LOCATOR)
        self.logOut()
        return result

    def clickRecentTransactions(self):
        self.elementClick(self.RECENT_TRANSACTIONS, self.RECENT_TRANSACTIONS_LOCATOR)

    def sendAfterDate(self, date):
        self.sendKeys(date, self.AFTER_DATE, self.AFTER_DATE_LOCATOR)

    def clickSubmitDate(self):
        self.elementClick(self.SUBMIT_DATE, self.SUBMIT_DATE_LOCATOR)

    def clickAlert(self):
        alert1 = self.driver.switch_to.alert
        alert1.accept()

    def check_invalidDate(self, date):
        self.clickRecentTransactions()
        self.sendAfterDate(date)
        time.sleep(3)
        self.clickSubmitDate()
        time.sleep(3)
        self.clickAlert()

    def verify_invalidDate(self):
        self.waitForAlert()

    def check_links(self, httpsLinksOnly = False):
        #Check if any link is broken in the given page
        self.brokenLinks = ''
        links = self.getElementList("a", "css")
        if httpsLinksOnly:
            links = [n for n in links if 'https' in n.get_attribute('href')]
        for link in links:
            print(link.get_attribute('href'))
            try:
                r = requests.head(link.get_attribute('href'))
                if r.status_code == 404:
                    self.brokenLinks += link.get_attribute('href') + ' 404 '
                print(r.status_code)
            except:
                print('Time out')
                self.brokenLinks += link.get_attribute('href') + ' Time out '

    def verify_brokenLink(self):
        if self.brokenLinks == '':
            return True
        return False
