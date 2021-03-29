from selenium.webdriver.support.select import Select

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage


class UserPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver
        self.Error = 'None'
        self.account1 = 'None'
        self.account2 = 'None'


    # Locators

    ACCOUNT_SELECT = '//select//option'
    ACCOUNT_SELECT_LOCATOR = 'xpath'

    ACCOUNT_BTN = 'btnGetAccount'
    ACCOUNT_BTN_LOCATOR = 'id'

    CONTENT_TITLE = '//div[@class=\'fl\']//h1'
    CONTENT_TITLE_LOCATOR = 'xpath'

    APPLY = 'Here'
    APPLY_LOCATOR = 'Link'

    PSWD = 'passwd'
    PSWD_LOCATOR = 'name'

    SUBMIT_BTN = 'Submit'
    SUBMIT_BTN_LOCATOR = 'name'

    APPLY_CONTENT = '//div[@class=\'fl\']//span'
    APPLY_CONTENT_LOCATOR = 'xpath'
    EXPECTED_CONTENT = 'Your new Altoro Mutual Gold VISA with a $10000 and 7.9% APR will be sent in the mail.'

    TRANSFER = 'MenuHyperLink3'
    TRANSFER_LOCATOR = 'id'

    FROM = 'fromAccount'
    FROM_LOCATOR = 'id'

    TO = 'toAccount'
    TO_LOCATOR = 'id'

    AMOUNT = 'transferAmount'
    AMOUNT_LOCATOR = 'id'

    TRANSFER_BTN = 'transfer'
    TRANSFER_BTN_LOCATOR = 'id'

    TRANSFER_MSG = '//form[@id=\'tForm\']//tr[6]//span//span'
    TRANSFER_MSG_LOCATOR = 'xpath'

    ARTICLES = 'MenuHyperLink4'
    ARTICLES_LOCATOR = 'id'

    ARTICLES_INPUT = 'query'
    ARTICLES_INPUT_LOCATOR = 'id'

    ARTICLES_BTN = 'Button1'
    ARTICLES_BTN_LOCATOR = 'id'

    ARTICLES_FORM = 'QueryXpath'
    ARTICLES_FORM_LOCATOR = 'id'

    def writeBrokenContent(self, header, message):
        self.Error += header + message + ' | '
        self.screenShot(header + message)

    def clickGoButton(self):
        self.elementClick(self.ACCOUNT_BTN, self.ACCOUNT_BTN_LOCATOR)

    def getTitle(self):
        return self.getElement(self.CONTENT_TITLE, self.CONTENT_TITLE_LOCATOR)

    def verifyTitle(self, title):
        _title = self.getTitle()
        if title not in _title:
            self.writeBrokenContent(title, '_content_wrong')
            self.screenShot(title + '_content_wrong')

    def getAccounts(self):
        return self.getElementList(self.ACCOUNT_SELECT, self.ACCOUNT_SELECT_LOCATOR)

    def check_accountSummary(self):
        self.Error = ''
        options = self.getAccounts()
        for option in options:
            text = option.text
            self.elementClick(element=option)
            self.verifyTitle(text)

    def verify_accountInfo(self):
        if self.Error == '':
            return True
        return False

    def clickApply(self):
        self.elementClick(self.APPLY, self.APPLY_LOCATOR)

    def sendPswd(self, password):
        self.sendKeys(password, self.PSWD, self.PSWD_LOCATOR)

    def clickSubmit(self):
        self.elementClick(self.SUBMIT_BTN, self.SUBMIT_BTN_LOCATOR)

    def check_apply(self, password):
        self.clickApply()
        self.sendPswd(password)
        self.clickSubmit()

    def verify_aplly(self):
        element = self.getElement(self.APPLY_CONTENT, self.APPLY_CONTENT_LOCATOR)
        if element is not None and self.EXPECTED_CONTENT in element.text:
            return True
        return False

    def clickTransferFounds(self):
        self.elementClick(self.TRANSFER, self.TRANSFER_LOCATOR)

    def selectAccounts(self, fromI, toI):
        _from = Select(self.getElement(self.FROM, self.FROM_LOCATOR))
        _to = Select(self.getElement(self.TO, self.TO_LOCATOR))
        self.account1 = _from.options[fromI].text
        self.account2 = _to.options[toI].text
        _from.select_by_index(fromI)
        _to.select_by_index(toI)

    def clickTransferBtn(self):
        self.elementClick(self.TRANSFER_BTN, self.TRANSFER_BTN_LOCATOR)

    def check_transferFounds(self, testError = False):
        self.clickTransferFounds()
        if testError:
            self.selectAccounts(0, 0)
        else:
            self.selectAccounts(0, 1)
        self.clickTransferBtn()

    def verify_transferSuccessful(self):
        resultMsg = self.getElement(self.TRANSFER_MSG, self.TRANSFER_MSG_LOCATOR)
        if resultMsg.text != '':
            if self.account1 in resultMsg.text and self.account2 in resultMsg.text:
                return True
        return False

    def verify_transferUnsuccessful(self):
        return self.waitForAlert()

    def clickArticles(self):
        self.elementClick(self.ARTICLES, self.ARTICLES_LOCATOR)

    def sendArticleName(self, name):
        self.sendKeys(name, self.ARTICLES_INPUT, self.ARTICLES_INPUT_LOCATOR)

    def clickQuery(self):
        self.elementClick(self.ARTICLES_BTN, self.ARTICLES_BTN_LOCATOR)

    def check_articlesSearch(self, name):
        self.clickArticles()
        self.sendArticleName(name)
        self.clickQuery()

    def verify_querySuccessful(self):
        element = self.getElement(self.ARTICLES_FORM, self.ARTICLES_FORM_LOCATOR)
        if 'News title not found' in element.text:
            return False
        return True

