*** Settings ***
Library    AppiumLibrary
Library    ${CURDIR}/../../utils/driver_factory.py    WITH NAME    Driver
Library    ${CURDIR}/../../resources/pages/paywall_page.py

*** Keywords ***
Application Is Launched
    [Documentation]    Launches the application and verifies it is initialized
    [Tags]    allure
    # Driver'ın aktif olduğunu kontrol et
    ${is_initialized}=    Driver.Is Driver Initialized
    Run Keyword If    not ${is_initialized}    Fatal Error    WebDriver başlatılamadı!
    
    # Uygulamanın başlatıldığını kontrol et
    Wait Until Keyword Succeeds    30s    2s    Page Should Contain Element    xpath=//XCUIElementTypeApplication[@name="Face AI"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]
    Sleep    10s    # Uygulamanın tam olarak yüklenmesi için 10 saniye bekle
    ${paywall_page}=    Get Library Instance    PaywallPage
    Wait Until Keyword Succeeds    30s    2s    Verify Weekly Elements Are Present

Wait Until Paywall Screen Appears
    [Documentation]    Waits until the paywall screen is visible
    [Tags]    allure
    [Arguments]    ${timeout}=30s
    # Driver'ın aktif olduğunu kontrol et
    ${is_initialized}=    Driver.Is Driver Initialized
    Run Keyword If    not ${is_initialized}    Fatal Error    WebDriver başlatılamadı!
    
    # Ekranın yüklenmesi için kısa bir bekleme
    Sleep    2s
    
    # Paywall ekranının yüklenmesini bekle
    ${paywall_page}=    Get Library Instance    PaywallPage
    Wait Until Keyword Succeeds    ${timeout}    2s    Page Should Contain Element    ${paywall_page.subscription_options}
    
    # Ekran görüntüsü al
    Capture Page Screenshot

Verify All Paywall Elements Are Present
    [Documentation]    Verifies that all paywall elements are visible
    [Tags]    allure
    ${paywall_page}=    Get Library Instance    PaywallPage
    ${result}=    Call Method    ${paywall_page}    verify_paywall_elements
    Should Be True    ${result}    Paywall elements are not visible

Verify Weekly Elements Are Present
    ${paywall_page}=    Get Library Instance    PaywallPage
    ${result}=    Call Method    ${paywall_page}    verify_weekly_elements
    Should Be True    ${result}    Weekly elements are not visible 