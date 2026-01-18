"""
Test Suite: Homepage Tests
Description: Tests using Page Object Model pattern
"""
import pytest
from pages.home_page import HomePage

def test_verify_homepage_elements(page):
    """
    Test: Verify DemoQA homepage loads with all elements
    Uses: Page Object Model pattern
    """
    
    # Start Playwright
    def test_robust_automation(page):
        print("\n🧪 Starting Robust Text Box Test")
            
        # Create page object
        home_page = HomePage(page)
        
        # Test Steps
        print("\n🧪 Starting test: Verify Homepage Elements")
        
        # Step 1: Open homepage
        home_page.open()
        
        # Step 2: Verify page title
        title = home_page.get_title()
        assert "DEMOQA" in title, f"Expected 'DEMOQA' in title, got '{title}'"
        print(f"✅ Title verified: {title}")
        
        # Step 3: Verify URL
        url = home_page.get_url()
        assert url == "https://demoqa.com/", f"Expected 'https://demoqa.com/', got '{url}'"
        print(f"✅ URL verified: {url}")
        
        # Step 4: Verify banner is visible
        assert home_page.is_banner_visible(), "Banner is not visible"
        print("✅ Banner is visible")
        
        # Step 5: Verify Elements card is visible
        assert home_page.is_elements_card_visible(), "Elements card is not visible"
        print("✅ Elements card is visible")
        
        # Step 6: Verify total cards count
        cards_count = home_page.get_cards_count()
        assert cards_count == 6, f"Expected 6 cards, found {cards_count}"
        print(f"✅ Found {cards_count} category cards")
        
        # Cleanup
        browser.close()
        print("✅ Test completed successfully!\n")


def test_navigate_to_elements_page(page):
    """
    Test: Navigate from homepage to Elements page
    Uses: Multiple page objects
    """
        
    # Import ElementsPage here
    from pages.elements_page import ElementsPage
    
    # Create page objects
    home_page = HomePage(page)
    elements_page = ElementsPage(page)
    
    # Test Steps
    print("\n🧪 Starting test: Navigate to Elements Page")
    
    # Step 1: Open homepage
    home_page.open()
    
    # Step 2: Click Elements card
    home_page.click_elements_card()
    print("✅ Clicked Elements card")
    
    # Step 3: Verify we're on Elements page
    assert elements_page.is_on_elements_page(), "Not on Elements page"
    print("✅ Navigated to Elements page")
    
    # Step 4: Verify header text (optional)
    header = elements_page.get_header_text()
    if header:
        assert header == "Elements", f"Expected 'Elements', got '{header}'"
        print(f"✅ Header verified: {header}")
    else:
        print("ℹ️  Header not found (checking alternative verification)")
    
    # Step 5: Verify Text Box menu item is visible
    assert elements_page.is_text_box_visible(), "Text Box menu not visible"
    print("✅ Text Box menu item is visible")
        
    # Cleanup
    print("✅ Test completed successfully!\n")

@pytest.mark.skipif(
    pytest.browser == "webkit",
    reason="WebKit is flaky for demoqa.com in CI"
)
def test_debug_elements_page(page):
    """Debug test to find the correct header selector"""
    
    home_page = HomePage(page)
    home_page.open()
    home_page.click_elements_card()
    
    # Wait a bit for page to load
    page.wait_for_timeout(2000)
    
    # Try different selectors
    selectors_to_try = [
        ".main-header",
        "h1",
        ".text-center",
        "h1.text-center",
        ".playgound-header",
        "div.main-header",
        "[class*='header']"
    ]
    
    print("\n🔍 Testing selectors:")
    for selector in selectors_to_try:
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                text = element.text_content(timeout=2000)
                print(f"✅ {selector} = '{text}'")
            else:
                print(f"❌ {selector} - not found")
        except:
            print(f"❌ {selector} - error/timeout")
    