import allure
from robot.libraries.BuiltIn import BuiltIn

def attach_screenshot():
    allure.attach(
        BuiltIn().get_library_instance('AppiumLibrary').get_screenshot_as_file(),
        name="Screenshot",
        attachment_type=allure.attachment_type.PNG
    )

def log_step(step_name):
    allure.step(step_name) 