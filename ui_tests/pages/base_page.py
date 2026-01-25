"""
Base Page Class
Contains common methods that all page classes will inherit
"""
from playwright.sync_api import Page


class BasePage:
    """
    Base class for all page objects
    Provides common functionality like navigation, waiting, etc.
    """
    
    def __init__(self, page: Page):
        """
        Initialize the base page
        Args:
            page: Playwright Page object
        """
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout
    
    def navigate(self, url: str):
        """
        Navigate to a specific URL
        Args:
            url: The URL to navigate to
        """
        self.page.goto(url, wait_until="domcontentloaded")
        print(f"✅ Navigated to: {url}")
    
    def get_title(self) -> str:
        """
        Get the current page title
        Returns:
            str: Page title
        """
        return self.page.title()
    
    def get_url(self) -> str:
        """
        Get the current page URL
        Returns:
            str: Current URL
        """
        return self.page.url
    
    def click_element(self, selector: str):
        """
        Click on an element
        Args:
            selector: Element selector (CSS, text, XPath)
        """
        self.page.locator(selector).click()
        print(f"✅ Clicked element: {selector}")
    
    def fill_text(self, selector: str, text: str):
        """
        Fill text into an input field
        Args:
            selector: Element selector
            text: Text to fill
        """
        self.page.locator(selector).fill(text)
        print(f"✅ Filled text '{text}' into: {selector}")
    
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is visible
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else self.timeout
            return self.page.locator(selector).is_visible(timeout=timeout_ms)
        except:
            return False
    
    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        Get text content of an element
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        Returns:
            str: Text content (empty string if not found)
        """
        try:
            timeout_ms = timeout if timeout else self.timeout
            return self.page.locator(selector).text_content(timeout=timeout_ms)
        except:
            return ""
    
    def wait_for_element(self, selector: str):
        """
        Explicitly wait for element to be visible
        Args:
            selector: Element selector
        """
        self.page.locator(selector).wait_for(state="visible", timeout=self.timeout)
        print(f"✅ Element is visible: {selector}")
    
    def take_screenshot(self, filename: str):
        """
        Take a screenshot of current page
        Args:
            filename: Name of screenshot file
        """
        self.page.screenshot(path=f"screenshots/{filename}")
        print(f"✅ Screenshot saved: {filename}")