"""
Test Suite: Homepage Tests
Description: Basic tests to verify DemoQA homepage functionality
"""

from playwright.sync_api import sync_playwright, expect


def test_open_demoqa_homepage():
    """
    Test: Verify DemoQA homepage opens successfully
    Steps:
        1. Launch browser
        2. Navigate to https://demoqa.com
        3. Verify page title contains 'DEMOQA'
        4. Close browser
    """
    
    # Start Playwright
    with sync_playwright() as playwright:
        
        # Launch browser (Chromium)
        # headless=False means browser will be visible
        browser = playwright.chromium.launch(headless=True)
        
        # Create a new browser context (isolated session)
        context = browser.new_context()
        
        # Create a new page (tab)
        page = context.new_page()
        
        # Navigate to DemoQA
        page.goto("https://demoqa.com")
        
        # Get the page title
        title = page.title()
        
        # Print title to console
        print(f"Page title is: {title}")
        
        # Assertion: Verify title contains 'DEMOQA'
        assert "DEMOQA" in title, f"Expected 'DEMOQA' in title, but got '{title}'"
        print(f"✅ Title verified: {title}")
        
        # Assertion 2: Verify URL
        current_url = page.url
        assert current_url == "https://demoqa.com/", f"Expected 'https://demoqa.com/', but got '{current_url}'"
        print(f"✅ URL verified: {current_url}")
        
        # Assertion 3: Verify main banner is visible
        banner = page.locator("img[src='/images/Toolsqa.jpg']")
        assert banner.is_visible(), "Main banner is not visible"
        print("✅ Main banner is visible")
        
        # Assertion 4: Verify "Elements" card exists
        elements_card = page.locator("text=Elements")
        assert elements_card.is_visible(), "Elements card is not visible"
        print("✅ Elements card is visible")
        
        # Assertion 5: Count number of category cards
        cards = page.locator(".card-body")
        card_count = cards.count()
        assert card_count == 6, f"Expected 6 cards, but found {card_count}"
        print(f"✅ Found {card_count} category cards")
        
        # Close browser
        browser.close()
        print("✅ Test completed successfully!")