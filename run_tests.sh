#!/bin/bash

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Clean Allure reports
echo "Cleaning previous Allure reports..."
rm -rf ./allure-results
rm -rf ./allure-report

# Start Appium server
echo "Starting Appium server..."
appium &
APPIUM_PID=$!

# Short wait for Appium to start
sleep 10

# Check if Appium server is running
if ! curl -s http://localhost:4723/status | grep -q "build"; then
  echo "Appium server could not be started!"
  kill $APPIUM_PID
  exit 1
fi

echo "Appium server started successfully."

# Run tests with Allure reports
echo "Running tests..."
robot --variable PYTHONPATH:$(pwd) \
      --pythonpath . \
      --pythonpath ./resources \
      --pythonpath ./utils \
      --listener allure_robotframework:allure-results \
      --outputdir results \
      ./tests/faceai_tests.robot

# Generate Allure reports
echo "Generating Allure reports..."
allure generate allure-results -o allure-report --clean

# Open Allure reports automatically
allure open allure-report &

# Stop Appium server
echo "Stopping Appium server..."
kill $APPIUM_PID
