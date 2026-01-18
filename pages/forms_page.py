"""
Forms Page Object
Contains locators and methods for DemoQA Practice Form page
"""

from pages.base_page import BasePage


class FormsPage(BasePage):
    """
    Page Object for DemoQA Practice Form
    URL: https://demoqa.com/automation-practice-form
    """
    
    # ========== LOCATORS ==========
    
    URL = "https://demoqa.com/automation-practice-form"
    
    # Form fields
    FIRST_NAME = "#firstName"
    LAST_NAME = "#lastName"
    EMAIL = "#userEmail"
    MOBILE = "#userNumber"
    
    # Gender radio buttons
    GENDER_MALE = "label[for='gender-radio-1']"
    GENDER_FEMALE = "label[for='gender-radio-2']"
    GENDER_OTHER = "label[for='gender-radio-3']"
    
    # Buttons
    SUBMIT_BUTTON = "#submit"
    
    # Success modal
    SUCCESS_MODAL = "#example-modal-sizes-title-lg"
    
    
    # ========== METHODS ==========
    
    def open(self):
        """Open the Practice Form page"""
        self.navigate(self.URL)
    
    
    def fill_first_name(self, name: str):
        """Fill first name field"""
        self.fill_text(self.FIRST_NAME, name)
    
    
    def fill_last_name(self, name: str):
        """Fill last name field"""
        self.fill_text(self.LAST_NAME, name)
    
    
    def fill_email(self, email: str):
        """Fill email field"""
        self.fill_text(self.EMAIL, email)
    
    
    def fill_mobile(self, mobile: str):
        """Fill mobile number field"""
        self.fill_text(self.MOBILE, mobile)
    
    
    def select_gender_male(self):
        """Select Male gender"""
        self.click_element(self.GENDER_MALE)
    
    
    def click_submit(self):
        """Click submit button"""
        self.click_element(self.SUBMIT_BUTTON)
    
    
    def is_success_modal_visible(self) -> bool:
        """Check if success modal appears after submission"""
        return self.is_visible(self.SUCCESS_MODAL)