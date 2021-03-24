from pages.Main.page import MainPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class MainPage_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        #Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)
        self.main = MainPage(self.driver)

    @pytest.mark.run(order=3)
    def test_links(self):
        self.main.check_links()
        boolResult = self.main.verify_brokenLink()
        self.ts.markFinal("test_links", boolResult,
                          "BROKEN_LINKS ", self.main.brokenLinks)

    @pytest.mark.run(order=1)
    @data(('admin', 'admin'), ('jsmith', 'demo1234'))
    @unpack
    def test_loginSuccessful(self, userName, password):
        self.main.check_Login(userName, password)
        boolResult = self.main.verifyLoginSuccessful()
        self.ts.markFinal("test_loginSuccessful", boolResult,
                          "LOGIN_SUCCESSFUL")

    @pytest.mark.run(order=2)
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
