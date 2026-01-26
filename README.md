# LearnNow - Playwright Automation Framework


[![Playwright Tests](https://github.com/Pooh122000/LearnNow/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/Pooh122000/LearnNow/actions/workflows/playwright-tests.yml)

## 📋 Project Overview
This is a Playwright-based test automation framework for testing [DemoQA](https://demoqa.com).

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **Automation Tool:** Playwright
- **Test Framework:** pytest
- **CI/CD:** GitHub Actions
- **Reporting:** pytest-html

## 📁 Project Structure
```
Now let's organize our project to support both UI and API testing!

---

### **Step 1: Reorganize Your Project**

**Current structure:**
```
LearnNow/
├── tests/
├── pages/
├── ...
```

**New structure:**
```
LearnNow/
│
├── ui_tests/                    # All UI tests
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   └── elements_page.py
│   ├── __init__.py
│   ├── test_homepage.py
│   ├── test_forms.py
│   └── test_assertions.py
│
├── api_tests/                   # All API tests (NEW!)
│   ├── clients/                # API client classes
│   │   ├── __init__.py
│   │   ├── base_client.py
│   │   └── bookstore_client.py
│   ├── __init__.py
│   ├── test_books_api.py
│   └── test_account_api.py
│
├── config/
│   ├── __init__.py
│   ├── ui_config.py
│   └── api_config.py           # API
│
├── .github/workflows/
│   ├── ui-tests.yml
│   └── api-tests.yml           # API
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git

### Installation Steps

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd LearnNow
```

2. **Create virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Install Playwright browsers**
```bash
   playwright install
```

## ▶️ Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_login.py
```

### Run tests by marker
```bash
pytest -m smoke
```

### Run with HTML report
```bash
pytest --html=reports/report.html
```

## 📊 Viewing Reports
After test execution, open `reports/report.html` in a browser.

## 👤 Author
Sneha Poojary

## 📅 Last Updated
January 2026
