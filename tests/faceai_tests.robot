*** Settings ***
Documentation    Face AI Uygulaması Test Suite
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
    [Documentation]    Uygulamanın başarıyla başlatıldığını doğrular
    [Tags]    smoke    launch    allure
    Given Application Is Launched
    Then Log    Uygulama başarıyla başlatıldı!

Verify Paywall Screen Appears Within 10 Seconds
    [Documentation]    Paywall ekranının 10 saniye içinde görünür olduğunu doğrular
    [Tags]    smoke    paywall    allure
    Given Application Is Launched
    When Verify Paywall Screen Appears Within Timeout    10
    Then Log    Paywall ekranı başarıyla görüntülendi!

Verify All Subscription Plans Are Visible
    [Documentation]    Tüm abonelik planlarının görünür olduğunu doğrular
    [Tags]    smoke    paywall    allure
    Given Application Is Launched
    When Verify Paywall Screen Appears Within Timeout    10
    Then Verify Weekly Plan Elements Are Present
    And Verify Yearly Plan Elements Are Present
    And Verify Lifetime Plan Elements Are Present 