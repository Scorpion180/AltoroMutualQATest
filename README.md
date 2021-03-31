# Altoro Mutual tests

This is a project for automated AQ testing with selenium for the practice page [Alroto Mutual](http://demo.testfire.net)

### Requirements 📋

- Python 3
- Selenium 3
- Pytest 6.2
- ddt 1.4

### Runnig the project 🔧
> Running as test suite

py.test -v -s tests/test_suite.py --browser DESIRED_BROWSER_HERE --html=report.html --capture=tee-sys

> Running as single test

py.test -v -s PATH_TO_TEST --browser DESIRED_BROWSER_HERE --html=report.html --capture=tee-sys

### Possible browsers
1. firefox
2. ie
3. chrome
