import re
from playwright.sync_api import expect


def test_robust_automation(page):
    print("\n🧪 Starting Robust Text Box Test")

    # Navigate
    page.goto(
    "https://demoqa.com/text-box",
    wait_until="domcontentloaded",
    timeout=60000)
    expect(page).to_have_url(re.compile(".*text-box.*"))
    print("✅ Navigated to Text Box page")

    # Fill form fields
    full_name = "John Doe"
    email = "john.doe@example.com"
    current_address = "123 Main Street, New York"
    permanent_address = "456 Park Avenue, Boston"

    page.fill("#userName", full_name)
    expect(page.locator("#userName")).to_have_value(full_name)
    print(f"✅ Filled full name: {full_name}")

    page.fill("#userEmail", email)
    expect(page.locator("#userEmail")).to_have_value(email)
    print(f"✅ Filled email: {email}")

    page.fill("#currentAddress", current_address)
    print("✅ Filled current address")

    page.fill("#permanentAddress", permanent_address)
    print("✅ Filled permanent address")

    # Submit form
    page.click("#submit")
    print("✅ Submitted form")

    # Verify output with auto-waiting
    output = page.locator("#output")
    expect(output).to_be_visible(timeout=10000)
    print("✅ Output section appeared")

    # Verify each output field
    expect(page.locator("#name")).to_contain_text(full_name)
    print("✅ Name verified in output")

    expect(page.locator("#email")).to_contain_text(email)
    print("✅ Email verified in output")

    print("✅ Test completed successfully!\n")
