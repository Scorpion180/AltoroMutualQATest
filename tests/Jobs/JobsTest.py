import time

from pages.Jobs.JobsPage import JobsPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class Jobs_tests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        # Instantiate here your test class located at "pages"
        self.ts = TestStatus(self.driver)
        self.jobs = JobsPage(self.driver)

    @pytest.mark.run(order=1)
    def test_jobsList(self):
        self.jobs.check_jobOpenings()
        boolResult = self.jobs.verify_correctInfo()
        self.ts.mark(boolResult, 'info_correct')
        self.ts.markFinal("test_jobsList", boolResult,
                          "Jobs_info_correct")
