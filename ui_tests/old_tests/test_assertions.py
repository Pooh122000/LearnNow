"""
Test Suite: Assertion Examples
Demonstrates different types of assertions in Playwright
"""

import os
import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage

@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Banner is flaky in CI on demoqa.com")

def test_python_built_in_assertions(page):
    """
    Test: Using Python's built-in assert statements
    """
    print("\n🧪 Testing Python Built-in Assertions")

    home_page = HomePage(page)
    home_page.open()

    # === STRING ASSERTIONS ===

    title = home_page.get_title()
    assert title == "DEMOQA", f"Expected 'DEMOQA', got '{title}'"
    print("✅ Title equals DEMOQA")

    url = home_page.get_url()
    assert "demoqa.com" in url, f"Expected 'demoqa.com' in URL, got '{url}'"
    print("✅ URL contains demoqa.com")

    assert url.startswith("https://"), "Expected URL to start with https://"
    print("✅ URL starts with https://")

    assert url.endswith("/"), "Expected URL to end with /"
    print("✅ URL ends with /")

    # === BOOLEAN ASSERTIONS ===

    assert home_page.is_banner_visible(), "Banner should be visible"
    print("✅ Banner is visible")

    assert home_page.is_elements_card_visible(), "Elements card should be visible"
    print("✅ Elements card is visible")

    # === NUMERIC ASSERTIONS ===

    cards_count = home_page.get_cards_count()
    assert cards_count == 6, f"Expected 6 cards, got {cards_count}"
    print("✅ Cards count equals 6")

    assert cards_count > 0, "Cards count should be greater than 0"
    print("✅ Cards count > 0")

    assert 5 <= cards_count <= 10, "Cards count should be between 5 and 10"
    print("✅ Cards count within range")

    # === NEGATIVE ASSERTIONS ===

    assert title != "Google", "Title should not be Google"
    print("✅ Title is not Google")

    assert "facebook" not in url, "URL should not contain facebook"
    print("✅ URL does not contain facebook")

    print("✅ All Python built-in assertions passed!\n")


def test_playwright_expect_assertions(page):
    """
    Test: Using Playwright's expect API (RECOMMENDED)
    """
    print("\n🧪 Testing Playwright Expect Assertions")

    home_page = HomePage(page)
    home_page.open()

    # === PAGE ASSERTIONS ===

    banner = page.locator(".home-banner img")

    # Visibility
    expect(banner).to_be_visible()
    print("✅ Banner is visible")

    # Attribute (robust)
    expect(banner).to_have_attribute("src", re.compile("/images/"))
    print("✅ Banner src attribute verified")

    expect(page).to_have_url("https://demoqa.com/")
    print("✅ Page URL matches exactly")

    expect(page).to_have_url(re.compile(".*demoqa.*"))
    print("✅ Page URL regex matched")

    # === ELEMENT VISIBILITY ASSERTIONS ===

    expect(banner).to_have_attribute("src", re.compile("/images/"))
    expect(banner).to_be_visible()
    print("✅ Banner is visible")

    non_existent = page.locator("#does-not-exist")
    expect(non_existent).to_be_hidden()
    print("✅ Non-existent element is hidden")

    # === ELEMENT STATE ASSERTIONS ===

    elements_card = page.locator(home_page.ELEMENTS_CARD)
    expect(elements_card).to_be_enabled()
    print("✅ Elements card is enabled")

    expect(elements_card).to_contain_text("Elements")
    print("✅ Elements card contains text")

    expect(elements_card).to_have_text("Elements")
    print("✅ Elements card has exact text")

    # === COUNT ASSERTIONS ===

    cards = page.locator(home_page.ALL_CARDS)
    expect(cards).to_have_count(6)
    print("✅ Found exactly 6 cards")

    # === ATTRIBUTE ASSERTIONS ===

    expect(banner).to_have_attribute("src", re.compile("/images/"))
    print("✅ Banner src attribute verified")

    # === NEGATIVE EXPECT ASSERTIONS ===

    expect(non_existent).not_to_be_visible()
    print("✅ Non-existent element is NOT visible")

    expect(elements_card).not_to_contain_text("Google")
    print("✅ Elements card does NOT contain Google")

    print("✅ All Playwright expect assertions passed!\n")
