# LearnNow - Playwright Automation Framework

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
LearnNow/
│
├── tests/              # Test files
├── pages/              # Page Object Model classes
├── utils/              # Helper functions
├── test_data/          # Test data (JSON, CSV)
├── reports/            # Test execution reports
├── screenshots/        # Failure screenshots
└── requirements.txt    # Dependencies
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