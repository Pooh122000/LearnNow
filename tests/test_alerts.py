"""
Test Suite: Handling Alerts and Dialogs
"""

from playwright.sync_api import sync_playwright


def test_handle_javascript_alert():
    """
    Test: Handle JavaScript alert dialog
    URL: https://demoqa.com/alerts
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing Alert Handling")
        
        # Navigate to Alerts page
        page.goto("https://demoqa.com/alerts")
        
        # Set up alert handler BEFORE triggering alert
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Click button that triggers alert
        page.click("#alertButton")
        print("✅ Alert handled automatically")
        
        browser.close()


def test_handle_confirmation_dialog():
    """
    Test: Handle confirmation dialog (OK/Cancel)
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing Confirmation Dialog")
        
        page.goto("https://demoqa.com/alerts")
        
        # Variable to store dialog message
        dialog_message = None
        
        def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            print(f"📢 Dialog message: {dialog_message}")
            dialog.accept()  # Click OK
            # Or: dialog.dismiss() to click Cancel
        
        page.on("dialog", handle_dialog)
        
        # Click confirmation button
        page.click("#confirmButton")
        
        # Verify we got the dialog
        assert dialog_message is not None, "Dialog did not appear"
        print("✅ Confirmation dialog handled")
        
        browser.close()


def test_handle_prompt_dialog():
    """
    Test: Handle prompt dialog (with input)
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing Prompt Dialog")
        
        page.goto("https://demoqa.com/alerts")
        
        # Handle prompt and enter text
        def handle_prompt(dialog):
            print(f"📢 Prompt message: {dialog.message}")
            dialog.accept("Playwright Automation")  # Enter this text
        
        page.on("dialog", handle_prompt)
        
        # Click prompt button
        page.click("#promtButton")
        
        # Verify the entered text appears on page
        result = page.locator("#promptResult").text_content()
        assert "Playwright Automation" in result
        print(f"✅ Prompt result: {result}")
        
        browser.close()
        
#handling new window
def test_handle_new_window():
    """
    Test: Handle new browser window/tab
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing New Window")
        
        page.goto("https://demoqa.com/browser-windows")
        
        # Listen for new page event
        with context.expect_page() as new_page_info:
            page.click("#windowButton")  # Opens new window
        
        # Get the new page object
        new_page = new_page_info.value
        
        # Wait for new page to load
        new_page.wait_for_load_state()
        
        print(f"✅ New window URL: {new_page.url}")
        
        # Work with new window
        heading = new_page.locator("#sampleHeading").text_content()
        print(f"✅ New window heading: {heading}")
        
        # Close new window
        new_page.close()
        
        # Original page still accessible
        print(f"✅ Original page URL: {page.url}")
        
        browser.close()
        
#Scenario 3: Handling Iframes
def test_handle_iframe():
    """
    Test: Interact with elements inside iframe
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing Iframe Handling")
        
        page.goto("https://demoqa.com/frames")
        
        # Method 1: Using frame locator
        frame = page.frame_locator("#frame1")
        heading = frame.locator("#sampleHeading").text_content()
        print(f"✅ Iframe heading: {heading}")
        
        # Method 2: Using frame selector
        # iframe_element = page.frame(name="frame1")
        # heading = iframe_element.locator("#sampleHeading").text_content()
        
        browser.close()
#Scenario 4: Waiting for Dynamic Elements
def test_wait_for_dynamic_element():
    """
    Test: Wait for element that appears after delay
    """
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()
        
        print("\n🧪 Testing Dynamic Element Wait")
        
        page.goto("https://demoqa.com/dynamic-properties")
        
        # Element appears after 5 seconds
        visible_button = page.locator("#visibleAfter")
        
        # Playwright automatically waits up to 30 seconds
        expect(visible_button).to_be_visible()
        print("✅ Dynamic button became visible")
        
        # Element enabled after 5 seconds
        enabled_button = page.locator("#enableAfter")
        expect(enabled_button).to_be_enabled()
        print("✅ Button became enabled")
        
        browser.close()
