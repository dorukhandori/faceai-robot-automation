#!/bin/bash

# PYTHONPATH'i ayarla
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Allure raporlarını temizle
echo "Cleaning previous Allure reports..."
rm -rf ./allure-results
rm -rf ./allure-report

# Appium sunucusunu başlat
echo "Starting Appium server..."
appium &
APPIUM_PID=$!

# Appium'un başlaması için kısa bir bekleme
sleep 10

# Appium sunucusunun çalıştığını kontrol et
if ! curl -s http://localhost:4723/status | grep -q "build"; then
  echo "Appium server could not be started!"
  kill $APPIUM_PID
  exit 1
fi

echo "Appium server started successfully."

# Testleri Allure raporlarıyla çalıştır
echo "Running tests..."
robot --variable PYTHONPATH:$(pwd) \
      --pythonpath . \
      --pythonpath ./resources \
      --pythonpath ./utils \
      --listener allure_robotframework:allure-results \
      --outputdir results \
      ./tests/faceai_tests.robot

# Allure raporlarını oluştur
echo "Generating Allure reports..."
allure generate allure-results -o allure-report --clean

# Allure raporlarını otomatik olarak aç
allure open allure-report &

# Appium sunucusunu durdur
echo "Stopping Appium server..."
kill $APPIUM_PID
