"""
Test Suite: Forms Page Tests
"""

from playwright.sync_api import sync_playwright
from pages.forms_page import FormsPage


def test_fill_practice_form():
    """
    Test: Fill and submit practice form
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        # Create page object
        forms_page = FormsPage(page)
        
        print("\n🧪 Starting test: Fill Practice Form")
        
        # Open form page
        forms_page.open()
        
        # Fill form fields
        forms_page.fill_first_name("John")
        print("✅ Filled first name")
        
        forms_page.fill_last_name("Doe")
        print("✅ Filled last name")
        
        forms_page.fill_email("john.doe@test.com")
        print("✅ Filled email")
        
        forms_page.select_gender_male()
        print("✅ Selected gender")
        
        forms_page.fill_mobile("1234567890")
        print("✅ Filled mobile number")
        
        # Submit form
        forms_page.click_submit()
        print("✅ Clicked submit")
        
        # Verify success modal appears
        assert forms_page.is_success_modal_visible(), "Success modal not visible"
        print("✅ Success modal appeared")
        
        browser.close()
        print("✅ Test completed successfully!\n")