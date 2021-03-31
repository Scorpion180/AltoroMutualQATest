import time

from pages.Main.MainPage import MainPage
from pages.RecentTransactions.RecentTransactions import RecentTransactions
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class Login_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)
        self.main = MainPage(self.driver)
        self.rt = RecentTransactions(self.driver)

    @pytest.mark.run(order=2)
    @data(('jsmith', 'demo1234', True), ('admin', 'admin', True))
    @unpack
    def test_loginSuccessful(self, userName, password, logOut):
        self.main.check_Login(userName, password)
        boolResult = self.main.verify_loginSuccessful(logOut)
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
