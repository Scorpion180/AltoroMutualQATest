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

from tests.Login.LoginTest import Login_tests
from tests.Main.MainPageTest import MainPage_tests
from tests.User.UserTest import User_tests

tc1 = unittest.TestLoader().loadTestsFromTestCase(MainPage_tests)
tc2 = unittest.TestLoader().loadTestsFromTestCase(Login_tests)
tc3 = unittest.TestLoader().loadTestsFromTestCase(User_tests)

smokeTest = unittest.TestSuite([tc1, tc2, tc3])

unittest.TextTestRunner(verbosity=2).run(smokeTest)
