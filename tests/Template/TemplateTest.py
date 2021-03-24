from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class TemplateTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        #Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)

    '''
    #Run order of the test
    @pytest.mark.run(order=1)
    #For multiple data test
    @data(("JavaScript for beginners", "377210020926314"), ("Learn Python 3 from scratch", "377210020926314"))
    @unpack
    #ALL of the test methods here SHOULD start with test_
    def test_invalidEnrollment(self, courseName, ccNum):
        #Test methods from test clase here
        #Use TS for testing the expected result 
        self.ts.markFinal("test_invalidEnrollment", boolResult,
                          "ERROR MESSAGE")
    '''