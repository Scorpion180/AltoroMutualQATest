

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
        self.brokenContent = 'None'

    # Locators

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

    CONTENT_TITLE = '//div[@class=\'fl\']//h1'
    CONTENT_TITLE_LOCATOR = 'xpath'

    CONTENT_LINKS = '//td[@class=\'bb\']//a[@href and not(@target)]'
    CONTENT_LINKS_LOCATOR = 'xpath'

    IFRAME = '//iframe'
    IFRAME_LOCATOR = 'xpath'

    SIDEBAR_LINKS = '//td[@class=\'cc br bb\']//a'
    SIDEBAR_LINKS_LOCATOR = 'xpath'

    LINKS = '//a[@href]'
    LINKS_LOCATOR = 'xpath'

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

    def verifyLoginSuccessful(self, _logOut=True):
        result = self.elementPresenceCheck(self.LOGIN_SUCCESSFUL, self.LOGIN_SUCCESSFUL_LOCATOR)
        if _logOut:
            self.logOut()
        return result

    def verifyLoginFailed(self):
        result = self.elementPresenceCheck(self.LOGIN_FAILED, self.LOGIN_FAILED_LOCATOR)
        self.logOut()
        return result

    def check_links(self, httpsLinksOnly=False):
        # Check if any link is broken in the given page
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

    def iFrameInContent(self, header, message):
        iframe = self.getElement(self.IFRAME, self.IFRAME_LOCATOR)
        if iframe is not None:
            self.driver.switch_to.frame(iframe)
            element = self.getElement(self.CONTENT_TITLE, self.CONTENT_TITLE_LOCATOR)
            if element is None:
                self.writeBrokenContent(header, message)
                return False, None
            return True, element
        else:
            return False, None

    def writeBrokenContent(self, header, message):
        self.brokenContent += header + message + ' | '
        self.screenShot(header + message)

    def check_contentH1(self, header, message):
        wordInText = True
        switchedToIframe = False
        element = self.getElement(self.CONTENT_TITLE, self.CONTENT_TITLE_LOCATOR)
        if element is None:
            switchedToIframe, element = self.iFrameInContent(header, message)
        elif element is not None and element.text != header:
            print(element.text)
            for word in header.split():
                if word.lower() in element.text.lower():
                    if switchedToIframe:
                        self.driver.switch_to.default_content()
                    return
                else:
                    wordInText = False
            if not wordInText:
                self.writeBrokenContent(header, message)
        if switchedToIframe:
            self.driver.switch_to.default_content()

    def check_mainLinks(self):
        self.brokenContent = ''
        uniqueLinks = self.getElementList(self.LINKS, self.LINKS_LOCATOR)
        for link in uniqueLinks:
            print(link.text)
            if '?' in link.get_attribute('href'):
                name = link.text
                ActionChains(self.driver).\
                    key_down(Keys.CONTROL).\
                    click(link).\
                    key_up(Keys.CONTROL).\
                    perform()
                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[1])
                self.check_contentH1(name, '_link_not_working')
                self.closeAllButMain()
                self.driver.switch_to.window(windows[0])

    def closeAllButMain(self):
        windows = self.driver.window_handles
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(windows[-1])
            self.driver.close()

    def iFramePresent(self):
        iframe = self.getElement(self.IFRAME, self.IFRAME_LOCATOR)
        if iframe is not None:
            self.driver.switch_to.frame(iframe)
            return True, self.getElementList(self.LINKS, self.LINKS_LOCATOR)
        return False, None

    def checkContentInLink(self):
        print('Switched to content')
        uniqueLinks1 = self.getElementList(self.CONTENT_LINKS, self.CONTENT_LINKS_LOCATOR)
        switchedToIframe = False
        if uniqueLinks1 is None:
            switchedToIframe, uniqueLinks = self.iFramePresent()
        if uniqueLinks1:
            for link1 in uniqueLinks1:
                name = link1.text
                ActionChains(self.driver).\
                    key_down(Keys.CONTROL).\
                    click(link1).\
                    key_up(Keys.CONTROL).\
                    perform()
                if switchedToIframe:
                    self.driver.switch_to.default_content()
                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[2])
                self.check_contentH1(name, '_link_not_working')
            return True
        return False

    def verify_mainLinks(self):
        if self.brokenContent == '':
            return True
        return False
