from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.webdriver import WebDriver
from appium.options.ios import XCUITestOptions
from utils.appium_service import AppiumService
from utils.test_utils import TestUtils
import logging
import time
import requests
import certifi
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import subprocess
from robot.api.deco import keyword
from utils.server_manager import ServerManager
from pathlib import Path
from appium.webdriver.common.appiumby import AppiumBy

try:
    import yaml
except ImportError:
    logger.error("PyYAML module is not installed. Please install it with 'pip install pyyaml' command.")
    raise

logger = logging.getLogger(__name__)

class DriverFactory:
    """Appium Driver management for Robot Framework"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_AUTO_KEYWORDS = True
    
    def __init__(self):
        self.driver = None
        self.server_manager = ServerManager()
        self.wait_time = TestUtils.WAIT
        self.builtin = BuiltIn()
        self.appium = self.builtin.get_library_instance('AppiumLibrary')
        
        # SSL doğrulamasını yapılandır
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        
        # Retry mekanizmasını yapılandır
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
    
    def get_appium_driver(self) -> WebDriver:
        """Creates and returns Appium driver"""
        try:
            logger.info("Creating Appium driver...")
            
            # iOS capabilities settings
            capabilities = {
                'appium:platformName': 'iOS',
                'appium:automationName': 'XCUITest',
                'appium:deviceName': 'iPhone(2)',
                'appium:platformVersion': '15',
                'appium:bundleId': 'co.koiapps.faceai',
                'appium:udid': '15b95c4404b92c876d5aab4e4e1a5b896febc4c1',
                'appium:xcodeOrgId': 'YY55LFW3H2',
                'appium:xcodeSigningId': 'Apple Distributor',
                'appium:noReset': True,
                'appium:fullReset': False,
                'appium:useNewWDA': False,
                'appium:usePrebuiltWDA': True,
                'appium:autoAcceptAlerts': True,
                'appium:newCommandTimeout': 60000
            }
            
            # Create XCUITest options
            options = XCUITestOptions()
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            # Appium connection URL - Updated URL for Appium 2.0
            appium_url = 'http://localhost:4723'
            
            # Initialize driver
            self.driver = self.appium.open_application(
                appium_url,
                **capabilities
            )
            
            logger.info("Appium driver created successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"Error creating Appium driver: {str(e)}")
            raise
    
    def is_driver_initialized(self) -> bool:
        """Checks if WebDriver is initialized"""
        try:
            if self.appium._current_application():
                return True
            return False
        except:
            return False
    
    def quit_appium_driver(self):
        """Closes Appium driver"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.server_manager.stop_server()
                logger.info("Driver closed successfully")
        except Exception as e:
            logger.error(f"Error closing driver: {str(e)}")
            raise

    def run_tests(self):
        """Runs the tests"""
        try:
            print("\n" + "="*80)
            print("RUNNING TESTS...")
            print("="*80 + "\n")
            result = subprocess.run(["robot", "tests/faceai_tests.robot"], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}") 