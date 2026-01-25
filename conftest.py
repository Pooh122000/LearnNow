"""
Pytest configuration file
Stable for Chromium, Firefox, WebKit (Local + CI)
"""

import os
import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime

# ===============================
# BROWSER NAME (ENV ONLY)
# ===============================

@pytest.fixture(scope="session")
def browser_name():
    """
    Browser selection ONLY via environment variable.
    Default: chromium
    """
    return os.getenv("PLAYWRIGHT_BROWSER", "chromium").lower()


# ===============================
# BROWSER FIXTURE
# ===============================

@pytest.fixture(scope="session")
def browser(browser_name):
    is_ci = os.getenv("CI") == "true"

    # CI = always headless
    headless = True if is_ci else False
    slow_mo = 0 if is_ci else 300

    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless, slow_mo=slow_mo)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=headless, slow_mo=slow_mo)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        print(f"\n🌐 Browser: {browser_name.upper()} | Headless: {headless}")
        yield browser
        browser.close()
        print(f"\n✅ Browser closed: {browser_name.upper()}")


# ===============================
# PAGE FIXTURE
# ===============================

@pytest.fixture
def page(browser, request):
    Path("screenshots").mkdir(exist_ok=True)
    Path("videos").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720},
    )

    page = context.new_page()
    page.test_name = request.node.name

    yield page

    context.close()


# ===============================
# SCREENSHOT ON FAILURE
# ===============================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = item.name.replace("::", "_")
            path = Path("screenshots") / f"FAILED_{name}_{timestamp}.png"
            try:
                page.screenshot(path=str(path), full_page=True)
                print(f"\n📸 Screenshot saved: {path}")
            except Exception as e:
                print(f"\n⚠️ Screenshot failed: {e}")


# ===============================
# MARKERS
# ===============================

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke")
    config.addinivalue_line("markers", "regression")
    config.addinivalue_line("markers", "slow")


# ===============================
# SESSION LOGGING
# ===============================

def pytest_sessionstart(session):
    print("\n" + "=" * 80)
    print("🚀 STARTING PLAYWRIGHT TEST EXECUTION")
    print(f"📍 ENV: {os.getenv('TEST_ENV', 'LOCAL').upper()}")
    print(f"🖥️ CI MODE: {'YES' if os.getenv('CI') == 'true' else 'NO'}")
    print("=" * 80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    print("\n" + "=" * 80)
    print("🏁 TEST EXECUTION COMPLETED")
    print("✅ ALL TESTS PASSED" if exitstatus == 0 else "❌ SOME TESTS FAILED")
    print("=" * 80 + "\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    print(f"\n▶️ Running: {item.name}")
    yield


# ===============================
# API REQUEST FIXTURE (PLAYWRIGHT)
# ===============================

@pytest.fixture(scope="session")
def api_request():
    """
    Provides a Playwright APIRequestContext for API testing.
    Isolated from browser/page fixtures.
    """
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=os.getenv("API_BASE_URL", "https://demoqa.com"),
            extra_http_headers={
                "Content-Type": "application/json"
            }
        )
        yield request_context
        request_context.dispose()