"""
Elements Page Object
Contains locators and methods for DemoQA Elements page
"""
from ui_tests.pages.base_page import BasePage


class ElementsPage(BasePage):
    """
    Page Object for DemoQA Elements Page
    URL: https://demoqa.com/elements
    """
    
    # ========== LOCATORS ==========
    # Main header - using the selector we found in debug test
    MAIN_HEADER = "[class*='header']"
    
    # Left side menu items
    MENU_TEXT_BOX = "text=Text Box"
    MENU_CHECK_BOX = "text=Check Box"
    MENU_RADIO_BUTTON = "text=Radio Button"
    MENU_WEB_TABLES = "text=Web Tables"
    MENU_BUTTONS = "text=Buttons"
    MENU_LINKS = "text=Links"
    MENU_BROKEN_LINKS = "text=Broken Links - Images"
    MENU_UPLOAD_DOWNLOAD = "text=Upload and Download"
    MENU_DYNAMIC_PROPERTIES = "text=Dynamic Properties"
    
    # ========== METHODS ==========
    
    def get_header_text(self):
        """
        Get the main header text
        Returns:
            str: Header text (trimmed)
        """
        text = self.get_text(self.MAIN_HEADER, timeout=5000)
        return text.strip() if text else ""
    
    def is_on_elements_page(self):
        """
        Verify we are on Elements page
        Returns:
            bool: True if on Elements page
        """
        try:
            self.page.wait_for_url("**/elements", timeout=5000)
        except:
            pass
        return "elements" in self.get_url().lower()
    
    def click_text_box(self):
        """Click on 'Text Box' menu item"""
        self.click_element(self.MENU_TEXT_BOX)
    
    def click_check_box(self):
        """Click on 'Check Box' menu item"""
        self.click_element(self.MENU_CHECK_BOX)
    def is_text_box_visible(self):
        """
        Check if Text Box menu item is visible
        Returns:
            bool: True if visible
        """
        return self.is_visible(self.MENU_TEXT_BOX)

