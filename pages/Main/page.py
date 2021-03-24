import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import requests


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

    def verifyLoginSuccessful(self):
        result = self.elementPresenceCheck(self.LOGIN_SUCCESSFUL, self.LOGIN_SUCCESSFUL_LOCATOR)
        self.logOut()
        return result

    def verifyLoginFailed(self):
        result = self.elementPresenceCheck(self.LOGIN_FAILED, self.LOGIN_FAILED_LOCATOR)
        self.logOut()
        return result

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
