*** Settings ***
Library    AppiumLibrary
Library    ${CURDIR}/../utils/driver_factory.py    WITH NAME    Driver
Resource   ${CURDIR}/../resources/steps/faceai_steps.robot

Suite Setup       Initialize Driver
Suite Teardown    Cleanup Driver

*** Keywords ***
Initialize Driver
    ${driver}=    Driver.Get Appium Driver
    Set Suite Variable    ${DRIVER}    ${driver}

Cleanup Driver
    Run Keyword And Ignore Error    Driver.Quit Appium Driver

*** Test Cases ***
Verify Paywall Screen Appears
    [Documentation]    Verifies that the paywall screen appears with all required elements
    [Tags]    smoke    paywall
    
    Given Application Is Launched
    When Wait Until Paywall Screen Appears
    Then Verify All Paywall Elements Are Present

Example Test Case
    [Documentation]    This is an example test case
    Log    Running the test case...
    # Test adımları buraya eklenir 