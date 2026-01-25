def test_navigate_to_elements_page():
    """Test navigation to Elements page"""
    
    def test_robust_automation(page):
        print("\n🧪 Starting Robust Text Box Test")
        # 1. Go to homepage
        page.goto("https://demoqa.com")
        
        # 2. Click on "Elements" card
        page.click("text=Elements")
        assert "elements" in page.url
        heading = page.get_by_text("Elements", exact=True).text_content()
        assert heading == "Elements"
        
        # 3. Verify URL contains "elements"
        assert "elements" in page.url, f"Expected 'elements' in URL, but got {page.url}"
        print(f"✅ URL verified: {page.url}")
        
        # 4. Verify page heading is "Elements"
        heading = page.get_by_text("Elements", exact=True).text_content()
        assert heading == "Elements", f"Expected heading 'Elements', but got '{heading}'"
        print(f"✅ Heading verified: {heading}")
        
        browser.close()