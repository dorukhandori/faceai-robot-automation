# Face AI Appium Test Automation

This project is designed to automate the testing of the **Face AI** application on iOS using **Appium** and **Robot Framework**. The tests are built to verify the core functionality and user interface of the application.

---

## 📋 Table of Contents

- [Project Goals](#-project-goals)
- [Installation](#-installation)
- [Test Scenarios](#-test-scenarios)
- [Technologies Used](#-technologies-used)
- [File Structure](#-file-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Goals

- **Paywall Screen Tests**: Verify that the paywall screen loads correctly and all elements are visible.
- **App Launch Tests**: Ensure the application launches successfully.
- **Automation Processes**: Automate manual testing processes to save time and resources.

---

## 🛠 Installation

To set up the project on your local machine, follow these steps:

### 1. Prerequisites

- **Python 3.8+**
- **Appium 2.0+**
- **Node.js**
- **Xcode** (for iOS simulator or real device)
- **Homebrew** (for macOS)

### 2. Clone the Repository
bash
git clone https://github.com/dorukhandori/faceai-robot-automation.git
cd faceai-appium-tests
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Start the Appium Server

```bash
./run_tests.sh
```

---

## 🧪 Test Scenarios

The project includes the following test scenarios:

1. **Appium Server Verification**:
   - Verifies that the Appium server is running successfully.

2. **Paywall Screen Verification**:
   - Verifies that the paywall screen appears within 10 seconds.

3. **Key Paywall Elements Verification**:
   - Verifies that the key elements (plan, price, button) are visible on the paywall screen.

---

## 🛠 Technologies Used

- **Appium**: An open-source tool for mobile test automation.
- **Robot Framework**: A framework for test automation.
- **Python**: The programming language used to write and manage test scenarios.
- **Xcode**: The development environment for iOS simulators and real devices.

---

## 📂 File Structure

The project has the following structure:

```
faceai-appium-tests/
├── README.md                   # Project documentation
├── run_tests.sh                # Script to run tests
├── envm.yaml                   # Environment configuration
├── requirements.txt            # Python dependencies
├── tests/
│   └── faceai_tests.robot      # Test cases
├── resources/
│   ├── steps/
│   │   └── faceai_steps.robot  # Test steps
│   └── pages/
│       ├── base_page.py        # Base page class
│       └── paywall_page.py      # Paywall page class
└── utils/
    ├── driver_factory.py       # Appium driver factory
    ├── server_manager.py       # Appium server manager
    └── test_utils.py           # Utility functions for tests
```

---

## 🤝 Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push your branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---
