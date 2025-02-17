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
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy

try:
    import yaml
except ImportError:
    logger.error("PyYAML modülü yüklü değil. Lütfen 'pip install pyyaml' komutu ile yükleyin.")
    raise

logger = TestUtils.get_logger(__name__)

class DriverFactory:
    """Robot Framework için Appium Driver yönetimi"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_AUTO_KEYWORDS = True
    
    def __init__(self, environment="ios_simulator"):
        self.driver = None
        self.server_manager = ServerManager()
        self.wait_time = TestUtils.WAIT
        self.builtin = BuiltIn()
        self.environment = self._load_environment(environment)
        
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
    
    def _load_environment(self, env_name):
        """envm.yaml dosyasından ortam ayarlarını yükler"""
        env_file = Path(__file__).parent.parent / "envm.yaml"
        try:
            with open(env_file) as f:
                # Güvenli yükleme için safe_load kullanıyoruz
                env_data = yaml.safe_load(f)
                return env_data['environments'][env_name]
        except Exception as e:
            logger.error(f"Environment yüklenirken hata: {str(e)}")
            raise
    
    @keyword
    def get_appium_driver(self):
        """Appium driver'ı oluşturur ve döndürür"""
        if not self.driver:
            logger.info("Appium driver oluşturuluyor...")
            try:
                options = XCUITestOptions()
                options.platform_name = self.environment['platformName']
                options.device_name = self.environment['deviceName']
                options.platform_version = self.environment['platformVersion']
                options.automation_name = self.environment['automationName']
                options.udid = self.environment['udid']
                options.bundle_id = self.environment['bundleId']
                options.new_command_timeout = self.environment['capabilities']['newCommandTimeout']
                options.auto_dismiss_alerts = self.environment['capabilities']['autoDismissAlerts']

                # Driver'ı başlat
                self.driver = WebDriver(
                    command_executor=f"http://{self.environment['appium']['host']}:{self.environment['appium']['port']}",
                    options=options
                )
                
                # Uygulamanın hazır olmasını bekle
                self.driver.implicitly_wait(10)
                
                # Uygulamanın başlatıldığını doğrula
                self.driver.find_element(
                    AppiumBy.XPATH,
                    '//XCUIElementTypeApplication[@name="Face AI"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]'
                )
                
                logger.info("Appium driver başarıyla oluşturuldu")
            except Exception as e:
                logger.error(f"Appium driver oluşturulurken hata: {str(e)}")
                raise
        
        return self.driver
    
    @keyword
    def quit_appium_driver(self):
        """Appium driver'ı kapatır"""
        if self.driver:
            logger.info(f"[{TestUtils.get_datetime()}] Driver kapatılıyor...")
            try:
                self.driver.quit()
                self.driver = None
                self.server_manager.stop_server()
                logger.info(f"[{TestUtils.get_datetime()}] Driver başarıyla kapatıldı")
            except Exception as e:
                logger.error(f"[{TestUtils.get_datetime()}] Driver kapatılırken hata: {str(e)}")

    @keyword
    def is_driver_initialized(self):
        """WebDriver'ın başlatılıp başlatılmadığını kontrol eder"""
        try:
            if self.driver:
                # Session ID'yi kontrol et
                if self.driver.session_id:
                    # Basit bir komut çalıştırarak bağlantıyı test et
                    self.driver.get_window_size()
                    return True
        except:
            pass
        
        self.driver = None
        return False

    def run_tests(self):
        """Testleri çalıştırır"""
        try:
            print("\n" + "="*80)
            print("TESTLER ÇALIŞTIRILIYOR...")
            print("="*80 + "\n")
            result = subprocess.run(["robot", "tests/faceai_tests.robot"], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}") 