import time

from pages.Jobs.JobsPage import JobsPage
from pages.Main.MainPage import MainPage
from pages.RecentTransactions.RecentTransactions import RecentTransactions
from pages.User.UserPage import UserPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class User_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.main = MainPage(self.driver)
        self.page = UserPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.rt = RecentTransactions(self.driver)

    def validDate(self):
        results = []
        self.rt.check_afterDate('2020-11-20')
        results.append(self.rt.verify_validDate())
        self.ts.mark(results[-1], "After_date_verified")
        results.append(self.rt.verify_datesOnTable(after='2020-11-20', type='AFTER'))
        self.ts.mark(results[-1], "Dates_After_on_Table_verified")

        self.rt.check_beforeDate('2021-03-20')
        results.append(self.rt.verify_validDate())
        self.ts.mark(results[-1], "Before_date_verified")
        results.append(self.rt.verify_datesOnTable(before='2021-03-20', type='BEFORE'))
        self.ts.mark(results[-1], "Dates_Before_on_Table_verified")

        self.rt.check_dates('2020-11-20', '2021-03-20')
        results.append(self.rt.verify_datesOnTable('2020-11-20', '2021-03-20', 'BOTH'))
        self.ts.mark(results[-1], "Valid_dates_verified")
        self.ts.markFinal('test_validDate', all(x == results[0] for x in results), "dates_test_successful")

    def invalidDate(self):
        results = []
        self.rt.check_afterDate('02/12/2015')
        results.append(self.rt.verify_invalidDate())
        self.ts.mark(results[-1], "After_date_verified")
        self.rt.clearRecentTransactionsFields()
        self.rt.check_beforeDate('02/12/2015')
        results.append(self.rt.verify_invalidDate())
        self.ts.mark(results[-1], "Before_date_verified")
        self.ts.markFinal("test_invalidDate", all(x == results[0] for x in results),
                          "invalid_date_test_successful")

    @pytest.mark.run(order=1)
    @data(('admin', 'admin', 'watchfire', 'Savings', '456datil'), ('jsmith', 'demo1234',  'watchfire', '', ''))
    @unpack
    def test_accountOptions(self, username, password, articleName, accountType, newPswd):
        results = []
        self.main.check_Login(username, password)
        self.page.check_accountSummary()
        results.append(self.page.verify_accountInfo())
        self.ts.mark(results[-1], username+'_account_summary_correct')

        self.page.check_apply(password)
        results.append(self.page.verify_aplly())
        self.ts.mark(results[-1], username + '_apply_form_correct')

        self.page.check_transferFounds(1, testError=False)
        results.append(self.page.verify_transferSuccessful())
        self.ts.mark(results[-1], username + '_transfer_successful_correct')

        self.page.check_transferFounds(1, testError=True)
        results.append(self.page.verify_transferUnsuccessful())
        self.ts.mark(results[-1], username + '_transfer_unsuccessful_correct')

        self.page.check_articlesSearch(articleName)
        results.append(self.page.verify_querySuccessful())
        self.ts.mark(results[-1], username + '_article_search_successful')

        self.validDate()

        self.invalidDate()

        if username == 'admin':

            self.page.check_addAccount(username, accountType)
            results.append(self.page.verify_addedAccount())
            self.ts.mark(results[-1], username + '_add_account_successful')

            self.page.check_changePassword(username, newPswd)
            self.main.logOut()
            self.main.check_Login(username, newPswd)
            results.append(self.main.verify_loginSuccessful(False))
            self.ts.mark(results[-1], username + '_change_password_successful')
        self.ts.markFinal('test_accountOptions', all(x == results[0] for x in results), username+'_test_successful')

