*** Settings ***
Documentation    Face AI Application Test Suite
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
Verify App Launch
    [Documentation]    Verifies that the application is launched successfully
    [Tags]    smoke    launch    allure
    Given Application Is Launched
    Then Log    Application launched successfully!

Verify Paywall Screen Appears Within 10 Seconds
    [Documentation]    Verifies that paywall screen appears within 10 seconds
    [Tags]    smoke    paywall    allure
    Given Application Is Launched
    When Verify Paywall Screen Appears Within Timeout    10
    Then Log    Paywall screen displayed successfully!

Verify All Subscription Plans Are Visible
    [Documentation]    Verifies that all Subscription Plans Are Visible
    [Tags]    smoke    paywall    allure
    Given Application Is Launched
    When Verify Paywall Screen Appears Within Timeout    10
    Then Verify Weekly Plan Elements Are Present
    And Verify Yearly Plan Elements Are Present
    And Verify Lifetime Plan Elements Are Present 