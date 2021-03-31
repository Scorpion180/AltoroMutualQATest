import time

from pages.Jobs.JobsPage import JobsPage
from pages.Main.MainPage import MainPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class MainPage_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)
        self.main = MainPage(self.driver)
        self.jobs = JobsPage(self.driver)

    @pytest.mark.run(order=8)
    def test_jobsList(self):
        self.jobs.check_jobOpenings()
        boolResult = self.jobs.verify_correctInfo()
        self.ts.mark(boolResult, 'info_correct')
        self.ts.markFinal("test_jobsList", boolResult,
                          "Jobs_info_correct")

    @pytest.mark.run(order=7)
    def test_subscribeUnsuccessful(self):
        self.main.check_subscribeForm('myname')
        boolResult = self.main.verify_subscribeUnsuccessful()
        self.ts.markFinal("test_subscribeUnsuccessful", boolResult,
                          "Subscribe_working_correctly")

    @pytest.mark.run(order=6)
    def test_subscribeSuccessful(self):
        self.main.check_subscribeForm('myname@email.com')
        boolResult = self.main.verify_subscribeSuccessful()
        self.ts.markFinal("test_subscribeSuccessful", boolResult,
                          "Subscribe_working_correctly")

    @pytest.mark.run(order=5)
    def test_clearForm(self):
        self.main.check_contactForm('Efren', 'efren', 'test', 'idk')
        self.main.clickClearForm()
        boolResult = self.main.verify_clearForm()
        self.ts.markFinal("test_clearForm", boolResult,
                          "Form_clear_successful ")

    @pytest.mark.run(order=4)
    def test_unsuccessfulContactForm(self):
        self.main.check_contactForm('Efren', 'efren', 'test', 'idk')
        self.main.clickSubmitForm()
        boolResult = self.main.verify_formResultMessage('the email you gave is incorrect')
        self.ts.markFinal("test_unsuccessfulContactForm", boolResult,
                          "Form_unsuccessful_working ")

    @pytest.mark.run(order=3)
    def test_successfulContactForm(self):
        self.main.check_contactForm('Efren', 'efren@gmail.com', 'test', 'idk')
        self.main.clickSubmitForm()
        boolResult = self.main.verify_formResultMessage('Our reply will be sent to your email')
        self.ts.markFinal("test_successfulContactForm", boolResult,
                          "Form_successful_working ")

    @pytest.mark.run(order=2)
    def test_links(self):
        self.main.check_links()
        boolResult = self.main.verify_brokenLink()
        self.ts.markFinal("test_links", boolResult,
                          "BROKEN_LINKS ", self.main.brokenLinks)

    @pytest.mark.run(order=1)
    def test_mainLinks(self):
        self.main.check_mainLinks()
        boolResult = self.main.verify_mainLinks()
        self.ts.markFinal("test_mainLinks", boolResult,
                          "MAIN_LINKS_WORKING ", self.main.brokenContent)


'''

    @pytest.mark.run(order=1)
    def test_mainLinks(self):
        self.main.check_mainLinks()
        boolResult = self.main.verify_mainLinks()
        self.ts.markFinal("test_mainLinks", boolResult,
                          "MAIN_LINKS_WORKING ", self.main.brokenContent)

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
