from appium.webdriver.common.appiumby import AppiumBy
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from resources.pages.base_page import BasePage
import allure

@library(scope='GLOBAL')
class PaywallPage(BasePage):
    def __init__(self):
        super().__init__()
        self.appium = BuiltIn().get_library_instance('AppiumLibrary')
        
        # Weekly Plan Elements
        self.WEEKLY_PLAN_TEXT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == '1 Week'`]")
        self.WEEKLY_PRICE_TEXT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == '₺349,99'`]")
        self.WEEKLY_POPULAR_BADGE = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == 'POPULAR'`]")
        
        # Yearly Plan Elements
        self.YEARLY_PLAN_TEXT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == '1 Year'`]")
        self.YEARLY_PRICE_TEXT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == '₺2.299,99'`]")
        self.YEARLY_TOP_CHOICE_BADGE = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == 'TOP CHOICE'`]")
        
        # Lifetime Plan Elements
        self.LIFETIME_PLAN_TEXT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label == 'BEST VALUE'`]")
        
        # Paywall Screen
        self.PAYWALL_SCREEN = (AppiumBy.XPATH, "//XCUIElementTypeApplication[@name='Face AI']/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]")

        # Paywall Screen
        self.TRYNOW_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeButton[`label == 'Try Now'`]")
    @keyword
    def verify_paywall_screen_is_visible(self, timeout=10):
        """Verifies if the paywall screen is visible"""
        return self.wait_until_element_visible(self.PAYWALL_SCREEN, timeout)

    @keyword
    def verify_weekly_plan_elements_are_visible(self):
        """Verifies if weekly plan elements are visible"""
        elements = [
            
            self.TRYNOW_BUTTON
        ]
        return self.wait_until_elements_visible(elements)

    @keyword
    def verify_yearly_plan_elements_are_visible(self):
        """Verifies if yearly plan elements are visible"""
        elements = [
            self.YEARLY_TOP_CHOICE_BADGE
            
        ]
        return self.wait_until_elements_visible(elements)

    @keyword
    def verify_lifetime_plan_elements_are_visible(self):
        """Verifies if lifetime plan element is visible"""
        return self.wait_until_element_visible(self.LIFETIME_PLAN_TEXT) 