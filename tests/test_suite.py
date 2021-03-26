'''
Run various test cases in order
EXAMPLE:
    # Get all tests from the test classes
tc1 = unittest.TestLoader().loadTestsFromTestCase(TestClass1)
tc2 = unittest.TestLoader().loadTestsFromTestCase(TestClass2)

# Create a test suite combining all test classes
smokeTest = unittest.TestSuite([tc1, tc2])

unittest.TextTestRunner(verbosity=2).run(smokeTest)
'''
import unittest
from tests.Main.MainPageTest import MainPage_tests
from tests.RecentTransactions.RecentTransactionsTest import RecentTransactions_tests

tc1 = unittest.TestLoader().loadTestsFromTestCase(MainPage_tests)
tc2 = unittest.TestLoader().loadTestsFromTestCase(RecentTransactions_tests)

smokeTest = unittest.TestSuite([tc1, tc2])

unittest.TextTestRunner(verbosity=2).run(smokeTest)
