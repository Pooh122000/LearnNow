"""
Test Suite: Assertion Examples
Demonstrates different types of assertions in Playwright
"""

from playwright.sync_api import sync_playwright, expect
from pages.home_page import HomePage


def test_python_built_in_assertions():
    """
    Test: Using Python's built-in assert statements
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()
        
        home_page = HomePage(page)
        
        print("\n🧪 Testing Python Built-in Assertions")
        
        home_page.open()
        
        # === STRING ASSERTIONS ===
        
        # 1. Equality assertion
        title = home_page.get_title()
        assert title == "DEMOQA", f"Expected 'DEMOQA', got '{title}'"
        print("✅ Title equals DEMOQA")
        
        page.pause()
        
        
        # 2. Contains assertion
        url = home_page.get_url()
        assert "demoqa.com" in url, f"Expected 'demoqa.com' in URL, got '{url}'"
        print("✅ URL contains demoqa.com")
        
        # 3. Starts with assertion
        assert url.startswith("https://"), f"Expected URL to start with https://"
        print("✅ URL starts with https://")
        
        # 4. Ends with assertion
        assert url.endswith("/"), f"Expected URL to end with /"
        print("✅ URL ends with /")
        
        
        # === BOOLEAN ASSERTIONS ===
        
        # 5. Is visible
        assert home_page.is_banner_visible() == True, "Banner should be visible"
        print("✅ Banner is visible")
        
        # 6. Shortened boolean check
        assert home_page.is_elements_card_visible(), "Elements card should be visible"
        print("✅ Elements card is visible")
        
        
        # === NUMERIC ASSERTIONS ===
        
        # 7. Equality
        cards_count = home_page.get_cards_count()
        assert cards_count == 6, f"Expected 6 cards, got {cards_count}"
        print(f"✅ Cards count equals 6")
        
        # 8. Greater than
        assert cards_count > 0, f"Expected cards count > 0, got {cards_count}"
        print(f"✅ Cards count is greater than 0")
        
        # 9. Range check
        assert 5 <= cards_count <= 10, f"Expected cards between 5-10, got {cards_count}"
        print(f"✅ Cards count is within range")
        
        
        # === NEGATIVE ASSERTIONS ===
        
        # 10. Not equal
        assert title != "Google", f"Title should not be 'Google'"
        print("✅ Title is not Google")
        
        # 11. Not in
        assert "facebook" not in url, f"URL should not contain 'facebook'"
        print("✅ URL does not contain facebook")
        
        browser.close()
        print("✅ All Python assertions passed!\n")


def test_playwright_expect_assertions():
    """
    Test: Using Playwright's expect API (RECOMMENDED)
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()
        
        home_page = HomePage(page)
        
        print("\n🧪 Testing Playwright Expect Assertions")
        
        home_page.open()
        
        # === PAGE LEVEL ASSERTIONS ===
        
        # 1. Page title
        expect(page).to_have_title("DEMOQA")
        print("✅ Page title is DEMOQA")
        
        # 2. Page URL (exact match)
        expect(page).to_have_url("https://demoqa.com/")
        print("✅ Page URL matches exactly")
        
        # 3. Page URL (contains)
        expect(page).to_have_url(re.compile(".*demoqa.*"))  # Regex
        print("✅ Page URL contains 'demoqa'")
        
        
        # === ELEMENT VISIBILITY ASSERTIONS ===
        
        # 4. Element is visible
        banner = page.locator(home_page.BANNER_IMAGE)
        expect(banner).to_be_visible()
        print("✅ Banner is visible")
        
        # 5. Element is hidden
        non_existent = page.locator("#does-not-exist")
        expect(non_existent).to_be_hidden()
        print("✅ Non-existent element is hidden")
        
        
        # === ELEMENT STATE ASSERTIONS ===
        
        # 6. Element is enabled
        elements_card = page.locator(home_page.ELEMENTS_CARD)
        expect(elements_card).to_be_enabled()
        print("✅ Elements card is enabled")
        
        # 7. Element contains text
        expect(elements_card).to_contain_text("Elements")
        print("✅ Elements card contains text 'Elements'")
        
        # 8. Element has exact text
        expect(elements_card).to_have_text("Elements")
        print("✅ Elements card has exact text")
        
        
        # === COUNT ASSERTIONS ===
        
        # 9. Count elements
        cards = page.locator(home_page.ALL_CARDS)
        expect(cards).to_have_count(6)
        print("✅ Found exactly 6 cards")
        
        
        # === ATTRIBUTE ASSERTIONS ===
        
        # 10. Has attribute
        expect(banner).to_have_attribute("src", "/images/Toolsqa.jpg")
        print("✅ Banner has correct src attribute")
        
        
        # === NEGATIVE ASSERTIONS (NOT) ===
        
        # 11. Not visible
        expect(non_existent).not_to_be_visible()
        print("✅ Non-existent element is NOT visible")
        
        # 12. Does not contain text
        expect(elements_card).not_to_contain_text("Google")
        print("✅ Elements card does NOT contain 'Google'")
        
        browser.close()
        print("✅ All Playwright expect assertions passed!\n")