import time

from pages.Jobs.JobsPage import JobsPage
from pages.Main.MainPage import MainPage
from pages.User.UserPage import UserPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class Admin_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.main = MainPage(self.driver)
        self.page = UserPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=1)
    @data( ('admin', 'admin', 'watchfire'), ('jsmith', 'demo1234', 'watchfire'))
    @unpack
    def test_accountSummary(self, username, password, articleName):
        self.main.check_Login(username, password)
        self.page.check_accountSummary()
        boolResult = self.page.verify_accountInfo()
        self.ts.mark(boolResult, 'Account_summary_correct')
        self.page.check_apply(password)
        boolResult = self.page.verify_aplly()
        self.ts.mark(boolResult, 'Apply_form_correct')
        self.page.check_transferFounds(testError=False)
        boolResult = self.page.verify_transferSuccessful()
        self.ts.mark(boolResult, 'Transfer_successful_correct')
        self.page.check_transferFounds(testError=True)
        boolResult = self.page.verify_transferUnsuccessful()
        self.ts.mark(boolResult, 'Transfer_unsuccessful_correct')
        self.page.check_articlesSearch(articleName)
        boolResult = self.page.verify_querySuccessful()
        self.ts.mark(boolResult, 'Query_successful')
