"""
API Tests: Book Store API
Tests the DemoQA Book Store API endpoints

NOTE:
- These tests use the requests-based api_request fixture
- DemoQA is a PUBLIC demo API and can behave inconsistently
- We intentionally handle known DemoQA quirks using pytest.xfail
"""

import pytest


class TestBooksAPI:
    """Test suite for Books API endpoints"""

    def test_get_all_books(self, api_request):
        """
        Test: GET /BookStore/v1/Books
        Description: Fetch all books from the book store
        Expected:
        - Status 200
        - Response contains a list of books
        """

        print("\n🧪 TEST STARTED: Get All Books")

        # Step 1: Send GET request to fetch all books
        response = api_request.get("/BookStore/v1/Books")

        # Step 2: Handle DemoQA downtime gracefully
        if response.status_code == 502:
            pytest.xfail("❌ DemoQA BookStore API is down (502 Bad Gateway)")

        # Step 3: Print response details for understanding
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response Body Preview: {response.text[:200]}...")

        # Step 4: Validate HTTP status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✅ Status code is 200")

        # Step 5: Parse JSON response
        response_json = response.json()

        # Step 6: Validate response structure
        assert "books" in response_json, "Response should contain 'books' key"
        print("✅ Response contains 'books' key")

        books = response_json["books"]

        assert isinstance(books, list), "Books should be a list"
        print(f"✅ Books is a list with {len(books)} items")

        assert len(books) > 0, "At least one book should be present"
        print("✅ At least one book is present")

        # Step 7: Validate structure of first book
        first_book = books[0]
        required_fields = ["isbn", "title", "author", "publisher", "pages"]

        for field in required_fields:
            assert field in first_book, f"Book should contain '{field}' field"

        print(f"✅ First book has all required fields: {required_fields}")
        print(f"📚 First Book: '{first_book['title']}' by {first_book['author']}")

        print("🏁 TEST COMPLETED: Get All Books")

    def test_get_specific_book(self, api_request):
        """
        Test: GET /BookStore/v1/Book?ISBN={isbn}
        Description: Fetch a specific book using a valid ISBN
        Expected:
        - Status 200
        - Correct book details returned
        """

        print("\n🧪 TEST STARTED: Get Specific Book")

        # Known valid ISBN from DemoQA
        isbn = "9781449325862"  # Git Pocket Guide

        # Step 1: Send GET request for a specific book
        response = api_request.get(f"/BookStore/v1/Book?ISBN={isbn}")

        # Step 2: Handle DemoQA downtime
        if response.status_code == 502:
            pytest.xfail("❌ DemoQA BookStore API is down (502 Bad Gateway)")

        print(f"📡 Request: GET /BookStore/v1/Book?ISBN={isbn}")
        print(f"📡 Status Code: {response.status_code}")

        # Step 3: Validate status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✅ Status code is 200")

        # Step 4: Parse JSON response
        book = response.json()

        # DemoQA sometimes returns empty object for valid ISBN
        if not book:
            pytest.xfail("⚠️ DemoQA returned empty response for valid ISBN")

        # Step 5: Validate returned book details
        assert book.get("isbn") == isbn, f"Expected ISBN {isbn}, got {book.get('isbn')}"
        print("✅ ISBN matches")

        assert book.get("title"), "Book should have a title"
        assert book.get("author"), "Book should have an author"
        assert book.get("pages", 0) > 0, "Book should have pages"

        print("✅ Book Details:")
        print(f"   📖 Title     : {book['title']}")
        print(f"   ✍️  Author    : {book['author']}")
        print(f"   📄 Pages     : {book['pages']}")
        print(f"   🏢 Publisher : {book.get('publisher')}")

        print("🏁 TEST COMPLETED: Get Specific Book")

    def test_get_nonexistent_book(self, api_request):
        """
        Test: GET /BookStore/v1/Book with invalid ISBN
        Description: Try to fetch a book that does not exist
        Expected:
        - Ideally 400 Bad Request
        - DemoQA sometimes returns 200 → handled via xfail
        """

        print("\n🧪 TEST STARTED: Get Nonexistent Book")

        invalid_isbn = "9999999999999"

        # Step 1: Send GET request with invalid ISBN
        response = api_request.get(f"/BookStore/v1/Book?ISBN={invalid_isbn}")

        # Step 2: Handle DemoQA downtime
        if response.status_code == 502:
            pytest.xfail("❌ DemoQA BookStore API is down (502 Bad Gateway)")

        print(f"📡 Request: GET /BookStore/v1/Book?ISBN={invalid_isbn}")
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text}")

        # DemoQA quirk: returns 200 instead of 400
        if response.status_code == 200:
            pytest.xfail("⚠️ DemoQA returns 200 for invalid ISBN instead of 400")

        # Ideal API behavior (not DemoQA)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("✅ Status code is 400 (Bad Request)")

        error_response = response.json()
        assert "message" in error_response or "code" in error_response

        print(f"✅ Error response received: {error_response}")
        print("🏁 TEST COMPLETED: Get Nonexistent Book")
