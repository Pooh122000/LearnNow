"""
Test Suite: Handling Alerts and Dialogs
"""

from playwright.sync_api import expect


def test_handle_javascript_alert():
    """
    Test: Handle JavaScript alert dialog
    URL: https://demoqa.com/alerts
    """
    
    def test_robust_automation(page):
        print("\n🧪 Starting Robust Text Box Test")
        print("\n🧪 Testing Alert Handling")
        
        # Navigate to Alerts page
        page.goto("https://demoqa.com/alerts")
        
        # Set up alert handler BEFORE triggering alert
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Click button that triggers alert
        page.click("#alertButton")
        print("✅ Alert handled automatically")
        


def test_handle_confirmation_dialog(page):
    """
    Test: Handle confirmation dialog (OK/Cancel)
    """

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
    confirm_btn = page.locator("#confirmButton")
    confirm_btn.wait_for(state="visible", timeout=15000)
    confirm_btn.click()
    
    # Verify we got the dialog
    assert dialog_message is not None, "Dialog did not appear"
    print("✅ Confirmation dialog handled")
    


def test_handle_prompt_dialog(page):
    """
    Test: Handle prompt dialog (with input)
    """ 
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

def test_handle_new_window(page):
    """
    Test: Handle new browser window/tab
    """
    print("\n🧪 Testing New Window")

    page.goto("https://demoqa.com/browser-windows")

    # Listen for new page event
    with page.expect_popup() as popup_info:
        page.click("#tabButton")  # Opens new tab

    # Get the new page
    new_page = popup_info.value

    # Wait until DOM is ready
    new_page.wait_for_load_state("domcontentloaded")

    # Assert URL
    expect(new_page).to_have_url("https://demoqa.com/sample")
    print(f"✅ New window URL: {new_page.url}")

    # Assert heading (AUTO-WAIT)
    heading = new_page.locator("#sampleHeading")
    expect(heading).to_have_text("This is a sample page")
    print("✅ New window heading verified")

    # Close new window
    new_page.close()

    # Original page still active
    expect(page).to_have_url("https://demoqa.com/browser-windows")
    print("✅ Original page still accessible")
        
#Scenario 3: Handling Iframes
def test_handle_iframe(page):
    print("\n🧪 Testing Iframe Handling")

    page.goto(
        "https://demoqa.com/frames",
        wait_until="domcontentloaded",
        timeout=60000
    )

    frame = page.frame_locator("#frame1")

    heading = frame.locator("#sampleHeading")
    heading.wait_for(timeout=15000)

    text = heading.text_content()
    print(f"✅ Iframe heading: {text}")

    assert text == "This is a sample page"

    
    # Method 2: Using frame selector
    # iframe_element = page.frame(name="frame1")
    # heading = iframe_element.locator("#sampleHeading").text_content()
    
#Scenario 4: Waiting for Dynamic Elements
def test_wait_for_dynamic_element(page):
    print("\n🧪 Testing Dynamic Element Wait")

    page.goto("https://demoqa.com/dynamic-properties")

    # Locator defined early (safe)
    visible_button = page.locator("#visibleAfter")

    # ✅ FIRST: wait for it to appear in DOM
    expect(visible_button).to_have_count(1, timeout=10000)

    # ✅ THEN: wait for visibility
    expect(visible_button).to_be_visible()
    print("✅ Dynamic button became visible")
