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
    """Add command-line options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, or webkit",
        choices=["chromium", "firefox", "webkit"]
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (visible browser)"
    )


# ========== BROWSER FIXTURE ==========

@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line or default to chromium"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def browser(request, browser_name):
    """
    Browser fixture - creates browser instance for entire test session
    Automatically detects CI environment and runs headless
    """
    # Detect CI environment
    is_ci = os.getenv("CI") == "true"
    
    # Check if user wants headed mode (only works locally)
    headed_flag = request.config.getoption("--headed")
    headless = is_ci or not headed_flag
    
    # Slow motion only in headed mode
    slow_mo = 0 if headless else 300
    
    with sync_playwright() as playwright:
        # Select browser based on option
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
    """
    Page fixture - creates new page for each test
    Includes video recording and automatic cleanup
    """
    # Create necessary directories
    Path("screenshots").mkdir(exist_ok=True)
    Path("videos").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Create context with video recording
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720}
    )
    
    page = context.new_page()
    
    # Store test name for later use
    page.test_name = request.node.name
    
    yield page
    
    # Cleanup
    context.close()


# ========== AUTO-SCREENSHOT ON FAILURE ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure
    Automatically saves screenshot with test name and timestamp
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture on test call phase (not setup/teardown)
    if report.when == "call" and report.failed:
        # Get the page fixture if it exists
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            
            # Create screenshots directory
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("::", "_").replace("[", "_").replace("]", "")
            screenshot_path = screenshot_dir / f"FAILED_{test_name}_{timestamp}.png"
            
            try:
                # Capture full page screenshot
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"\n📸 Screenshot captured: {screenshot_path}")
            except Exception as e:
                print(f"\n⚠️ Failed to capture screenshot: {e}")


# ========== PYTEST MARKERS ==========

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for critical functionality"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression test suite"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer than 30 seconds"
    )


# ========== SESSION START/END HOOKS ==========

def pytest_sessionstart(session):
    """
    Called before test session starts
    Useful for setup tasks and logging
    """
    print("\n" + "="*80)
    print("🚀 STARTING PLAYWRIGHT TEST EXECUTION")
    print("="*80)
    
    # Log environment info
    is_ci = os.getenv("CI") == "true"
    env_type = os.getenv("TEST_ENV", "local")
    print(f"📍 Environment: {env_type.upper()}")
    print(f"🖥️  CI Mode: {'YES' if is_ci else 'NO'}")
    print("="*80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after test session finishes
    Useful for cleanup and reporting
    """
    print("\n" + "="*80)
    print("🏁 TEST EXECUTION COMPLETED")
    
    # Print summary
    if exitstatus == 0:
        print("✅ Status: ALL TESTS PASSED")
    elif exitstatus == 1:
        print("❌ Status: SOME TESTS FAILED")
    else:
        print(f"⚠️ Status: EXIT CODE {exitstatus}")
    
    print("="*80 + "\n")


# ========== TEST RESULT LOGGING ==========

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """Log test start"""
    print(f"\n▶️  Running: {item.name}")
    yield