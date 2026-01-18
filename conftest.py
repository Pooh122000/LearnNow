# conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    headless = os.getenv("CI") == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            slow_mo=300 if not headless else 0
        )
        yield browser
        browser.close()
