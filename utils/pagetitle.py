# Playwright’s auto-waiting reduces flakiness significantly.
from playwright.sync_api import sync_playwright

def test_open_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Falsepython -m venv venv)
        page = browser.new_page()
        page.goto("https://demoqa.com")
        assert "DEMOQA" in page.title()
        browser.close()
        
test_open_site()