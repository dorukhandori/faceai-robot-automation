import os
import subprocess
from pathlib import Path
from typing import Optional, Dict
from utils.test_utils import TestUtils
import threading
import requests
import time

logger = TestUtils.get_logger(__name__)

class ServerManager:
    """Appium sunucusunu yöneten sınıf"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ServerManager, cls).__new__(cls)
                    cls._instance._server = None
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._server: Optional[subprocess.Popen] = None
            self.appium_path = "/usr/local/bin/appium"
            self._initialized = True
    
    def _check_xcuitest_driver(self):
        """XCUITest driver'ını kontrol eder ve günceller"""
        try:
            # Önce mevcut sürücüleri kontrol et
            result = subprocess.run(
                ["appium", "driver", "list", "--installed"],
                capture_output=True,
                text=True
            )
            
            if "xcuitest" in result.stdout.lower():
                # Sürücü zaten yüklü, güncelle
                logger.info("XCUITest driver güncelleniyor...")
                update_result = subprocess.run(
                    ["appium", "driver", "update", "xcuitest"],
                    capture_output=True,
                    text=True,
                    check=True  # Hata durumunda exception fırlatır
                )
                logger.info("XCUITest driver başarıyla güncellendi")
            else:
                # Sürücü yüklü değil, yeni kurulum yap
                logger.info("XCUITest driver yükleniyor...")
                install_result = subprocess.run(
                    ["appium", "driver", "install", "xcuitest"],
                    capture_output=True,
                    text=True,
                    check=True  # Hata durumunda exception fırlatır
                )
                logger.info("XCUITest driver başarıyla kuruldu")
            
        except subprocess.CalledProcessError as e:
            if "already installed" in str(e.stderr):
                # Driver zaten yüklü, bu durumu hata olarak değerlendirme
                logger.info("XCUITest driver zaten yüklü ve güncel")
                return
            logger.error(f"XCUITest driver işlemi sırasında hata: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"XCUITest driver işlemi sırasında beklenmeyen hata: {str(e)}")
            raise
    
    def get_environment(self) -> Dict[str, str]:
        """Appium sunucusu için gerekli ortam değişkenlerini ayarlar"""
        env = os.environ.copy()
        
        # PATH ayarları
        paths = [
            "/usr/local/bin",
            "/usr/bin",
            "/bin",
            "/usr/sbin",
            "/sbin"
        ]
        
        # Mevcut PATH'i koru ve yeni yolları ekle
        current_path = env.get("PATH", "")
        env["PATH"] = ":".join(paths + [current_path])
        
        return env
    
    def get_server(self) -> Optional[subprocess.Popen]:
        """Mevcut Appium sunucusunu döndürür"""
        return self._server
    
    def is_server_running(self) -> bool:
        """Appium sunucusunun çalışıp çalışmadığını kontrol eder"""
        try:
            response = requests.get('http://127.0.0.1:4723/status', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_server(self):
        """Appium sunucusunu başlatır"""
        logger.info("Appium sunucusu başlatılıyor...")
        
        # Log dizini oluştur
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "appium_server.log"
        
        try:
            # Appium komutu
            command = [
                self.appium_path,
                "--log-level", "debug",
                "--base-path", "/",
                "--address", "127.0.0.1",
                "--port", "4723",
                "--use-drivers", "xcuitest",
                "--relaxed-security",
                "--allow-insecure", "chromedriver_autodownload"
            ]
            
            logger.info(f"Komut çalıştırılıyor: {' '.join(command)}")
            
            # Sunucuyu başlat
            with open(log_file, 'w') as log_output:
                self._server = subprocess.Popen(
                    command,
                    env=os.environ.copy(),
                    stdout=log_output,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            
            # Sunucunun başlamasını bekle
            time.sleep(5)
            
            # Sunucunun çalışıp çalışmadığını kontrol et
            if not self.is_server_running():
                raise Exception("Appium sunucusu başlatılamadı")
            
            logger.info("Appium sunucusu başarıyla başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"Appium sunucusu başlatılırken hata: {str(e)}")
            if self._server:
                self.stop_server()
            return False
    
    def stop_server(self):
        """Appium sunucusunu durdurur"""
        try:
            if self._server:
                logger.info("Appium sunucusu durduruluyor...")
                self._server.terminate()
                self._server.wait(timeout=5)
                self._server = None
                logger.info("Appium sunucusu durduruldu")
        except Exception as e:
            logger.error(f"Appium sunucusu durdurulurken hata: {str(e)}") 