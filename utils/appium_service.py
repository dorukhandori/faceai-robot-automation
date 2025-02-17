import os
import subprocess
import logging
from pathlib import Path
from utils.test_utils import TestUtils
from typing import Dict, Optional
import requests
import time
from appium.webdriver.webdriver import WebDriver
from appium.options.ios import XCUITestOptions
from robot.api.deco import keyword

logger = TestUtils.get_logger(__name__)

class AppiumService:
    def __init__(self, port=4723):
        self.process = None
        self.node_path = "/usr/local/bin/node"
        self.appium_main = "/usr/local/lib/node_modules/appium/build/lib/main.js"
        # Log dizinini proje kök dizininde oluştur
        self.log_directory = Path(__file__).parent.parent / "logs"
        self.port = port
        
    def get_environment(self) -> Dict[str, str]:
        """Appium sunucusu için gerekli ortam değişkenlerini ayarlar"""
        env = os.environ.copy()
        
        # Java path ayarları
        java_home = "/Library/Java/JavaVirtualMachines/jdk-19.jdk/Contents/Home"
        env["JAVA_HOME"] = java_home
        env["PATH"] = f"{java_home}/bin:{env.get('PATH', '')}"
        
        # Android SDK path ayarları
        android_home = os.path.expanduser("~/Library/Android/sdk")
        env["ANDROID_HOME"] = android_home
        env["PATH"] = f"{android_home}/platform-tools:{env['PATH']}"
        
        # Node.js ve Appium path ayarları
        env["PATH"] = f"/usr/local/bin:{env['PATH']}"
        
        return env
        
    def create_log_file(self, device_name: str, platform_name: str) -> Path:
        """Log dosyasını oluşturur ve yolunu döndürür"""
        try:
            # Log dizinini oluştur
            device_log_dir = self.log_directory / f"{platform_name}_{device_name}"
            device_log_dir.mkdir(parents=True, exist_ok=True)
            
            # Log dosyası yolu
            log_file = device_log_dir / "server.log"
            
            # Log dosyasını oluştur (veya varsa üzerine yaz)
            log_file.touch(exist_ok=True)
            
            return log_file
            
        except Exception as e:
            logger.error(f"[{TestUtils.get_datetime()}] Log dosyası oluşturulurken hata: {str(e)}")
            raise
        
    def is_server_running(self) -> bool:
        """Appium sunucusunun çalışıp çalışmadığını kontrol eder"""
        try:
            response = requests.get(f'http://127.0.0.1:{self.port}/wd/hub', timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def wait_for_server(self, timeout: int = 30) -> bool:
        """Appium sunucusunun hazır olmasını bekler"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_server_running():
                return True
            time.sleep(1)
            logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu bekleniyor...")
        return False
        
    def start_server(self, device_name: str, platform_name: str) -> bool:
        """Appium sunucusunu başlatır"""
        try:
            logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu başlatılıyor...")
            
            # Log dosyasını oluştur
            log_file = self.create_log_file(device_name, platform_name)
            
            # Appium sunucusu komut ve argümanları
            command = [
                self.node_path,
                self.appium_main,
                "--session-override",
                "--log-level", "debug",
                "--local-timezone",
                "--relaxed-security",
                "--allow-insecure", "chromedriver_autodownload",
                "--address", "127.0.0.1",
                "--port", str(self.port)
            ]
            
            logger.info(f"[{TestUtils.get_datetime()}] Komut: {' '.join(command)}")
            
            # Sunucuyu başlat
            with open(log_file, 'w') as log_output:
                self.process = subprocess.Popen(
                    command,
                    env=self.get_environment(),
                    stdout=log_output,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            
            # Sunucunun hazır olmasını bekle
            if not self.wait_for_server(timeout=30):
                raise Exception("Appium sunucusu başlatılamadı: Zaman aşımı")
            
            logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu başlatıldı (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"[{TestUtils.get_datetime()}] Appium sunucusu başlatılırken hata: {str(e)}")
            if self.process:
                self.stop_server()
            return False
            
    def stop_server(self):
        """Appium sunucusunu durdurur"""
        try:
            if self.process:
                logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu durduruluyor...")
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu durduruldu")
                self.process = None
        except Exception as e:
            logger.error(f"[{TestUtils.get_datetime()}] Appium sunucusu durdurulurken hata: {str(e)}")

    def start(self):
        """Appium sunucusunu başlatır ve loglarını gösterir."""
        try:
            logger.info("Appium sunucusu başlatılıyor...")
            self.process = subprocess.Popen(
                ["appium", "--port", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            time.sleep(5)  # Sunucunun başlaması için kısa bir bekleme
            logger.info(f"Appium sunucusu {self.port} portunda başlatıldı.")
            
            # Logları gerçek zamanlı olarak göster
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    logger.info(output.strip())
        except Exception as e:
            logger.error(f"Appium sunucusu başlatılırken hata: {str(e)}")
            raise

    def stop(self):
        """Appium sunucusunu durdurur."""
        if self.process:
            logger.info("Appium sunucusu durduruluyor...")
            self.process.terminate()
            self.process.wait()
            logger.info("Appium sunucusu durduruldu.")
        else:
            logger.warning("Appium sunucusu zaten çalışmıyor.")

# Örnek kullanım
if __name__ == "__main__":
    appium_service = AppiumService()
    appium_service.start()
    try:
        # Testler burada çalıştırılabilir
        pass
    finally:
        appium_service.stop()

# Robot Framework tarafından tanınması için sınıfı dışa aktar
AppiumService = AppiumService() 