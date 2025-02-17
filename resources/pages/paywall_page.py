from resources.pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
import logging
from robot.api.deco import keyword

logger = logging.getLogger(__name__)

class PaywallPage(BasePage):
    def __init__(self):
        super().__init__()
        
        # Locators
        self.subscription_options = (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Subscription Options']")
        self.pricing_details = (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Pricing Details']")
        self.subscribe_button = (AppiumBy.ACCESSIBILITY_ID, "Subscribe Now")
        self.skip_button = (AppiumBy.ACCESSIBILITY_ID, "Skip")
        
        # New locators
        self.weekly_plan_text = (AppiumBy.ACCESSIBILITY_ID, "2D000000-0000-0000-AD0C-000000000000")
        self.weekly_price_text = (AppiumBy.ACCESSIBILITY_ID, "2E000000-0000-0000-AD0C-000000000000")
        self.weekly_button = (AppiumBy.ACCESSIBILITY_ID, "28000000-0000-0000-AD0C-000000000000")
        
    @keyword
    def verify_paywall_elements(self):
        """Paywall elementlerinin varlığını doğrular"""
        try:
            elements = [
                self.subscription_options,
                self.pricing_details,
                self.subscribe_button,
                self.skip_button
            ]
            
            for element in elements:
                if not self.wait_until_element_visible(element, timeout=10):
                    return False
            return True
        except Exception as e:
            logger.error(f"Paywall elementleri kontrol edilirken hata: {str(e)}")
            return False

    def wait_for_weekly_elements(self, timeout=None):
        """Weekly elementlerinin görünür olmasını bekler"""
        weekly_elements = [
            self.weekly_plan_text,
            self.weekly_price_text,
            self.weekly_button
        ]
        return self.wait_until_elements_visible(weekly_elements, timeout)
        
    @keyword
    def verify_weekly_elements(self):
        """Weekly elementlerinin varlığını doğrular"""
        if not self.wait_for_weekly_elements():
            raise AssertionError("Weekly elementleri görünür değil!")
        return True 