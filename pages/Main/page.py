import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import requests


class MainPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver, self.log)
        self.driver = driver
        self.brokenLinks = 'None'

    def check_links(self, httpsLinksOnly = False):
        #Check if any link is broken in the given page
        self.brokenLinks = ''
        links = self.getElementList("a", "css")
        if httpsLinksOnly:
            links = [n for n in links if 'https' in n.get_attribute('href')]
        for link in links:
            print(link.get_attribute('href'))
            try:
                r = requests.head(link.get_attribute('href'))
                if r.status_code == 404:
                    self.brokenLinks += link.get_attribute('href') + ' 404 '
                print(r.status_code)
            except:
                print('Time out')
                self.brokenLinks += link.get_attribute('href') + ' Time out '

    def verify_brokenLink(self):
        if self.brokenLinks == '':
            return True
        return False
