*** Settings ***
Library    AppiumLibrary
Library    ${CURDIR}/../../utils/driver_factory.py    WITH NAME    Driver
Library    ${CURDIR}/../pages/paywall_page.py    WITH NAME    Paywall

Variables    ${CURDIR}/../../envm.yaml

*** Keywords ***
Application Is Launched
    [Documentation]    Verifies that the application is launched
    ${is_initialized}=    Driver.Is Driver Initialized
    Should Be True    ${is_initialized}    WebDriver could not be initialized!
    Sleep    2s    # Short wait for the application to load

Verify Paywall Screen Appears Within Timeout
    [Documentation]    Verifies if the paywall screen appears within the specified timeout
    [Arguments]    ${timeout}=10
    ${result}=    Paywall.Verify Paywall Screen Is Visible    ${timeout}
    Should Be True    ${result}    Paywall screen is not visible within ${timeout} seconds!

Verify Weekly Plan Elements Are Present
    [Documentation]    Verifies that weekly plan elements are visible
    ${result}=    Paywall.Verify Weekly Plan Elements Are Visible
    Should Be True    ${result}    Weekly plan elements are not visible!

Verify Yearly Plan Elements Are Present
    [Documentation]    Verifies that yearly plan elements are visible
    ${result}=    Paywall.Verify Yearly Plan Elements Are Visible
    Should Be True    ${result}    Yearly plan elements are not visible!

Verify Lifetime Plan Elements Are Present
    [Documentation]    Verifies that lifetime plan element is visible
    ${result}=    Paywall.Verify Lifetime Plan Elements Are Visible
    Should Be True    ${result}    Lifetime plan element is not visible!

Verify Try Now Button Is Present
    [Documentation]    Verifies that Try Now button is visible
    ${result}=    Paywall.Verify Try Now Button Is Visible
    Should Be True    ${result}    Try Now button is not visible!

Verify Close Button Is Present
    [Documentation]    Verifies that close button is visible
    ${result}=    Paywall.Verify Close Button Is Visible
    Should Be True    ${result}    Close button is not visible!

Check Appium Logs For Success
    [Documentation]    Checks Appium logs for successful HTTP request
    [Tags]    allure
    ${log_file}=    Set Variable    ${EXECDIR}/appium.log
    ${log_content}=    Get File    ${log_file}
    ${success}=    Evaluate    "GET /status 200" in """${log_content}"""
    Should Be True    ${success}    Successful request not found in Appium logs 