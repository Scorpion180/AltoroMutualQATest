import os
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class SeleniumDriver():

    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    def screenShot(self, resultMessage):
        """
        Takes screenshot of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def findElement(self, property, locator = '', locatorType='id', element = None):
        try:
            if element is None:
                self.getElement(locator, locatorType)
            byType = self.getByType(locatorType)
            if By.XPATH == byType:
                element.find_element_by_xpath(locator).get_property(property)
            self.log.info('Element found in element by ' + byType + ' and property ' + property)
        except:
            self.log.info('Element not found in element by ' + locatorType + ' and property ' + property)

    def getElement(self, locator, locatorType="id", element = None):
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = WebDriverWait(self.driver, 10, .5).until(
                EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element found with locator: '" + locator + "' and locatorType: " + byType)
        except:
            self.log.info("Element not found with locator: '" + locator + "' and locatorType: " + locatorType)
        return element

    def getElementList(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        except:
            self.log.info("Element list not found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        return element

    def elementClick(self, locator="", locatorType="id", clickType="click", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if clickType == "click":
                element.click()
            elif clickType == "script":
                self.driver.execute_script("arguments[0].click();", element)
            elif clickType == "mouse":
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
            self.log.info("Clicked on element with locator: '" + locator + "' locatorType: " + locatorType +
                          " clickType: " + clickType)
        except:
            self.log.info("Clicked on element with locator: '" + locator + "' locatorType: " + locatorType +
                          " clickType: " + clickType)
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def sendKeys(self, data, locator="", locatorType="id", click=False, element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if click:
                self.elementClick(clickType="mouse", element=element)
            element.send_keys(data)
            self.log.info("Sent data on element with locator: '" + locator + "' locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data on the element with locator: '" + locator + "' locatorType: " + locatorType)
            print_stack()

    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            return isDisplayed
        except:
            print("Element not found")
            return False

    def elementPresenceCheck(self, locator, locatorType):
        try:
            elementList = self.driver.find_elements(locatorType, locator)
            if len(elementList) > 0:
                self.log.info("Element found with locator: '" + locator + "' and locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not found with locator: '" + locator + "' and locatorType: " + locatorType)
                return False
        except:
            self.log.info("Element not found with locator: '" + locator + "' and locatorType: " + locatorType)
            return False

    def waitForElement(self, locator, locatorType="id",
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            element = WebDriverWait(self.driver, timeout, pollFrequency).until(
                EC.presence_of_element_located((byType, locator)))
            self.log.info(
                "Element appeared on the web page with locator '" + locator + "' and locatorType: " + locatorType)
        except:
            self.log.info(
                "Element not appeared on the web page with locator '" + locator + "' and locatorType: " + locatorType)
            print_stack()
        return element

    def waitForAlert(self, timeout=10, pollFrequency=0.5):
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for alert to be present")
            WebDriverWait(self.driver, timeout, pollFrequency).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            self.log.info("Alert found")
            return True
        except:
            self.log.info("Alert not found")
            return False

    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def switchToFrame(self, data):
        try:
            self.driver.switch_to.frame(data)
            self.log.info("Switched to iFrame: " + str(data))
        except:
            self.log.info("Cannot switch to iFrame: " + str(data))
            print_stack()

    def switchToDefault(self):
        try:
            self.driver.switch_to.default_content()
            self.log.info("Switched back to default window")
        except:
            self.log.info("Cannot switch back to default window")
            print_stack()

    def switchToWindow(self, window):
        try:
            self.driver.switch_to.window(window)
            self.log.info("Switched to window "+self.driver.current_url)
        except:
            self.log.error("Failed to get switch to window")
            print_stack()

    def selectByIndex(self, index, element):
        try:
            element.select_by_index(index)
            self.log.info("Selected index: " + index)
        except:
            self.log.error("Failed to select index: " + index)
            print_stack()

    def executeScript(self, script):
        try:
            self.driver.execute_script(script)
            self.log.info("Executed script: " + script)
        except:
            self.log.info("Cannot execute script: " + script)
            print_stack()
