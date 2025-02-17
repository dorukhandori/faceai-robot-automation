#!/bin/bash

# PYTHONPATH'i ayarla
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Appium sunucusunu başlat
echo "Appium sunucusu başlatılıyor..."

# Capability'leri Appium'a geçir
appium \
  --port 4723 \
  --log-level debug \
  --relaxed-security \
  --allow-insecure chromedriver_autodownload \
  --default-capabilities '{
    "platformName": "iOS",
    "platformVersion": "15.0",
    "deviceName": "iPhone",
    "automationName": "XCUITest",
    "udid": "15b95c4404b92c876d5aab4e4e1a5b896febc4c1",
    "bundleId": "co.koiapps.faceai",
    "newCommandTimeout": 300,
    "autoDismissAlerts": true
  }' &
APPIUM_PID=$!

# Appium'un başlaması için kısa bir bekleme
sleep 10

# Appium sunucusunun çalıştığını kontrol et
if ! curl -s http://127.0.0.1:4723/status | grep -q "build"; then
  echo "Appium sunucusu başlatılamadı!"
  kill $APPIUM_PID
  exit 1
fi

echo "Appium sunucusu başarıyla başlatıldı."

# Testleri çalıştır
echo "Testler çalıştırılıyor..."
robot -V envm.yaml -v ENVIRONMENT:ios_real_device tests/faceai_tests.robot

# Appium sunucusunu durdur
echo "Appium sunucusu durduruluyor..."
kill $APPIUM_PID 