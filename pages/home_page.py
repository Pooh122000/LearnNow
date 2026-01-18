"""
Page Object Model: Home Page
Description: Page object for DemoQA homepage
"""

from playwright.sync_api import Page


class HomePage:
    """Page Object for DemoQA Homepage"""
    URL = "https://demoqa.com/"

    BANNER_IMAGE = ".home-banner"
    ELEMENTS_CARD = "div.card-body h5:has-text('Elements')"
    ALL_CARDS = "div.card"

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/"
        
        # Locators
        self.banner = ".banner-image"
        self.elements_card = "div.card:has-text('Elements')"
        self.cards = ".card"
    
    def open(self):
        """Navigate to homepage"""
        self.page.goto(self.url)
    
    def get_title(self):
        """Get page title"""
        return self.page.title()
    
    def get_url(self):
        """Get current URL"""
        return self.page.url
    
    def is_banner_visible(self):
        """Check if banner is visible"""
        return self.page.locator(self.banner).is_visible()
    
    def is_elements_card_visible(self):
        """Check if Elements card is visible"""
        return self.page.locator(self.elements_card).is_visible()
    
    def get_cards_count(self):
        """Count total cards on page"""
        return self.page.locator(self.cards).count()
    
    def click_elements_card(self):
        """Click on Elements card"""
        self.page.locator(self.elements_card).click()