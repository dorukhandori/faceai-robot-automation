import subprocess
import time
import os
import signal
import logging
import threading
import urllib3
import certifi
from utils.test_utils import TestUtils

logger = TestUtils.get_logger(__name__)

class AppiumServer:
    def __init__(self):
        self.process = None
        self.port = 4723
        self.appium_path = '/usr/local/bin/appium'  # Appium'un kurulu olduğu yolu belirtin

    def _stream_logs(self, pipe, prefix):
        """Streams Appium logs in real-time"""
        try:
            for line in iter(pipe.readline, ''):
                line = line.strip()
                print(f"{prefix}: {line}", flush=True)
                logger.info(f"{prefix}: {line}")
        except Exception as e:
            logger.error(f"Error reading logs: {str(e)}")

    def start_server(self):
        """Appium sunucusunu başlatır"""
        try:
            logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu başlatılıyor...")
            
            if self.is_server_running():
                logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu zaten çalışıyor")
                return True
            
            env = os.environ.copy()
            env['PATH'] = f"/usr/local/bin:{env.get('PATH', '')}"
            
            command = [
                self.appium_path,
                '--address', '127.0.0.1',
                '-p', str(self.port),
                '--base-path', '/wd/hub',
                '--log-level', 'debug'
            ]
            
            self.process = subprocess.Popen(
                command,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(5)  # Sunucunun başlaması için bekle
            
            if self.is_server_running():
                logger.info(f"[{TestUtils.get_datetime()}] Appium sunucusu başarıyla başlatıldı")
                return True
                
            raise Exception("Appium sunucusu başlatılamadı")
            
        except Exception as e:
            logger.error(f"[{TestUtils.get_datetime()}] Appium sunucusu başlatılırken hata: {str(e)}")
            return False

    def stop_server(self):
        """Stops the Appium server"""
        try:
            if self.process:
                logger.info("🔄 Stopping Appium server...")
                os.kill(self.process.pid, signal.SIGTERM)
                self.process.wait(timeout=5)
                logger.info(" Appium server stopped successfully")
                self.process = None
            else:
                logger.info("ℹ No running Appium server found")
        except Exception as e:
            logger.error(f" Error stopping Appium server: {str(e)}")

    def is_server_running(self):
        """Checks if the Appium server is running"""
        try:
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
            response = http.request('GET', f'http://127.0.0.1:{self.port}/')
            return response.status == 200
        except:
            return False

if __name__ == "__main__":
    server = AppiumServer()
    try:
        if server.start_server():
            print("Appium server started successfully. Press CTRL+C to exit.")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Appium server...")
        server.stop_server() 