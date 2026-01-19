"""
Pytest configuration file
Handles fixtures, browser selection, screenshots, and CI/CD optimizations
"""

import os
import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime


# ========== COMMAND LINE OPTIONS ==========
def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (LOCAL only)"
    )


# ========== BROWSER NAME FIXTURE ==========
@pytest.fixture(scope="session")
def browser_name():
    """
    Browser is selected ONLY via environment variable
    Default: chromium
    """
    return os.getenv("PLAYWRIGHT_BROWSER", "chromium")


# ========== BROWSER FIXTURE ==========
@pytest.fixture(scope="session")
def browser(request, browser_name):
    is_ci = os.getenv("CI") == "true"
    headed_flag = request.config.getoption("--headed")
    headless = is_ci or not headed_flag
    slow_mo = 0 if headless else 300

    with sync_playwright() as playwright:
        if browser_name == "chromium":
            browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
        elif browser_name == "firefox":
            browser = playwright.firefox.launch(headless=headless, slow_mo=slow_mo)
        elif browser_name == "webkit":
            browser = playwright.webkit.launch(headless=headless, slow_mo=slow_mo)
        else:
            raise ValueError(f"Unknown browser: {browser_name}")

        print(f"\n🌐 Running tests on {browser_name.upper()} (headless={headless})")
        yield browser
        browser.close()
        print(f"\n✅ Browser {browser_name.upper()} closed")


# ========== PAGE FIXTURE ==========
@pytest.fixture
def page(browser, request):
    Path("screenshots").mkdir(exist_ok=True)
    Path("videos").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720}
    )

    page = context.new_page()
    page.test_name = request.node.name
    yield page
    context.close()


# ========== SCREENSHOT ON FAILURE ==========
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace("::", "_")
        path = screenshot_dir / f"FAILED_{test_name}_{timestamp}.png"

        try:
            page.screenshot(path=str(path), full_page=True)
            print(f"\n📸 Screenshot captured: {path}")
        except Exception as e:
            print(f"\n⚠️ Screenshot failed: {e}")


# ========== MARKERS ==========
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke")
    config.addinivalue_line("markers", "regression")
    config.addinivalue_line("markers", "slow")


# ========== SESSION LOGGING ==========
def pytest_sessionstart(session):
    print("\n" + "="*80)
    print("🚀 STARTING PLAYWRIGHT TEST EXECUTION")
    print("="*80)
    print(f"📍 Environment: {os.getenv('TEST_ENV', 'LOCAL').upper()}")
    print(f"🖥️  CI Mode: {'YES' if os.getenv('CI') == 'true' else 'NO'}")
    print("="*80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    print("\n" + "="*80)
    print("🏁 TEST EXECUTION COMPLETED")
    print("✅ ALL TESTS PASSED" if exitstatus == 0 else "❌ SOME TESTS FAILED")
    print("="*80 + "\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    print(f"\n▶️  Running: {item.name}")
    yield
