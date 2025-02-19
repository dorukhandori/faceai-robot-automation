from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from robot.api.deco import keyword

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self):
        self.appium = BuiltIn().get_library_instance('AppiumLibrary')
        self.default_timeout = 30  # Default wait time
        
    @keyword
    def wait_until_element_visible(self, locator, timeout=10):
        """Waits for the element to be visible within specified timeout"""
        try:
            WebDriverWait(self.appium._current_application(), timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
            
    def wait_until_elements_visible(self, locators, timeout=10):
        """Birden fazla elementin görünür olmasını bekler"""
        try:
            for locator in locators:
                if not self.wait_until_element_visible(locator, timeout):
                    return False
            return True
        except:
            return False
            
    def wait_for_app_ready(self, timeout=None):
        """Waits until the application is ready"""
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.appium._current_application(), timeout).until(
                lambda x: x.is_app_installed('co.koiapps.faceai')
            )
            return True
        except:
            return False
            
    def find_element(self, locator):
        return self.appium._current_application().find_element(*locator)
        
    def click_element(self, locator):
        self.find_element(locator).click() 