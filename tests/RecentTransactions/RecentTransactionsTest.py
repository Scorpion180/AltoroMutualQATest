import time

from pages.Main.MainPage import MainPage
from pages.RecentTransactions.RecentTransactions import RecentTransactions
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RecentTransactions_test(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)
        self.main = MainPage(self.driver)
        self.rt = RecentTransactions(self.driver)

    @pytest.mark.run(order=4)
    def test_validDate(self):
        self.rt.check_afterDate('2020-11-20')
        boolResult2 = self.rt.verify_validDate()
        self.ts.mark(boolResult2, "After_date_verified")
        boolResult1 = self.rt.verify_datesOnTable(after='2020-11-20', type='AFTER')
        self.ts.mark(boolResult1, "Dates_After_on_Table_verified")

        self.rt.check_beforeDate('2021-03-20')
        boolResult1 = self.rt.verify_validDate()
        self.ts.mark(boolResult1, "Before_date_verified")
        boolResult2 = self.rt.verify_datesOnTable(before='2021-03-20', type='BEFORE')
        self.ts.mark(boolResult2, "Dates_Before_on_Table_verified")

        self.rt.check_dates('2020-11-20', '2021-03-20')
        time.sleep(5)
        boolResult1 = self.rt.verify_datesOnTable('2020-11-20', '2021-03-20', 'BOTH')
        self.ts.markFinal('test_validDate', boolResult1, "Valid_dates_verified")

    @pytest.mark.run(order=3)
    def test_invalidDate(self):
        self.rt.check_afterDate('02/12/2015')
        boolResult1 = self.rt.verify_invalidDate()
        self.ts.mark(boolResult1, "After_date_verified")
        self.rt.clearRecentTransactionsFields()
        self.rt.check_beforeDate('02/12/2015')
        boolResult2 = self.rt.verify_invalidDate()
        self.ts.markFinal("test_invalidDate", boolResult2,
                          "Before_date_verified")

    @pytest.mark.run(order=2)
    @data(('jsmith', 'demo1234', True), ('admin', 'admin', False))
    @unpack
    def test_loginSuccessful(self, userName, password, logOut):
        self.main.check_Login(userName, password)
        boolResult = self.main.verifyLoginSuccessful(logOut)
        self.ts.markFinal("test_loginSuccessful", boolResult,
                          "LOGIN_SUCCESSFUL")

    @pytest.mark.run(order=1)
    @data(('123', '123'), ('jsmith', 'demo124'))
    @unpack
    def test_loginFailed(self, userName, password):
        self.main.check_Login(userName, password)
        boolResult = self.main.verifyLoginFailed()
        self.ts.markFinal("test_loginFailed", boolResult,
                          "LOGIN_FAILED")

'''

    @pytest.mark.run(order=4)
    def test_links(self):
        self.main.check_links()
        boolResult = self.main.verify_brokenLink()
        self.ts.markFinal("test_links", boolResult,
                          "BROKEN_LINKS ", self.main.brokenLinks)

    @pytest.mark.run(order=2)
    # For multiple data test
    @data(("banana", 1))
    @unpack
    # ALL of the test methods here SHOULD start with test_
    def test_invalidSearch(self, searchString, number):
        # Test methods from test clase here
        self.main.search(searchString)
        boolResult = self.main.verifySearchWrong()
        # Use TS for testing the expected result
        self.ts.markFinal("test_validSearch", boolResult,
                          "ERROR ON SEARCHING " + searchString)
'''
