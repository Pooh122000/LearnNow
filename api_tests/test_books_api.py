"""
API Tests: Book Store API
Tests the DemoQA Book Store API endpoints
"""

import pytest


class TestBooksAPI:
    """Test suite for Books API endpoints"""

    BASE_URL = "https://demoqa.com"

    def test_get_all_books(self, api_request):
        """
        Test: GET /BookStore/v1/Books
        Description: Fetch all books from book store
        Expected: Status 200, returns list of books
        """

        # Make GET request using Playwright API request fixture
        response = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )
        
        if response.status == 502:
            pytest.xfail("DemoQA BookStore API is down (502 Bad Gateway)")

        # Print response for learning
        print(f"\n📡 Status Code: {response.status}")
        print(f"📄 Response Body Preview: {response.text()[:200]}...")

        # Assertions
        assert response.status == 200, f"Expected 200, got {response.status}"
        print("✅ Status code is 200")

        # Parse JSON response
        response_json = response.json()

        # Verify response has 'books' key
        assert "books" in response_json, "Response should contain 'books' key"
        print("✅ Response contains 'books' key")

        # Verify books is a list
        books = response_json["books"]
        assert isinstance(books, list), "Books should be a list"
        print(f"✅ Books is a list with {len(books)} items")

        # Verify at least one book exists
        assert len(books) > 0, "Should have at least one book"
        print(f"✅ Found {len(books)} books")

        # Verify first book structure
        first_book = books[0]
        required_fields = ["isbn", "title", "author", "publisher", "pages"]

        for field in required_fields:
            assert field in first_book, f"Book should have '{field}' field"

        print(f"✅ First book has all required fields: {required_fields}")
        print(f"📚 First book: '{first_book['title']}' by {first_book['author']}")

    def test_get_specific_book(self, api_request):
        """
        Test: GET /BookStore/v1/Book?ISBN={isbn}
        Description: Fetch specific book by ISBN
        Expected: Status 200, returns book details
        """

        # Known ISBN from DemoQA
        isbn = "9781449325862"  # Git Pocket Guide

        # Make GET request
        response = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Book",
            params={"ISBN": isbn}
        )
        
        if response.status == 502:
            pytest.xfail("DemoQA BookStore API is down (502 Bad Gateway)")

        print(f"\n📡 Request: GET /BookStore/v1/Book?ISBN={isbn}")
        print(f"📡 Status Code: {response.status}")

        # Assertions
        assert response.status == 200, f"Expected 200, got {response.status}"
        print("✅ Status code is 200")

        # Parse JSON
        book = response.json()

        # Verify ISBN matches
        assert book["isbn"] == isbn, f"Expected ISBN {isbn}, got {book['isbn']}"
        print(f"✅ ISBN matches: {isbn}")

        # Verify book details
        assert "title" in book and book["title"], "Book should have a title"
        assert "author" in book and book["author"], "Book should have an author"
        assert "pages" in book and book["pages"] > 0, "Book should have pages"

        print("✅ Book Details:")
        print(f"   📖 Title: {book['title']}")
        print(f"   ✍️  Author: {book['author']}")
        print(f"   📄 Pages: {book['pages']}")
        print(f"   🏢 Publisher: {book['publisher']}")

    def test_get_nonexistent_book(self, api_request):
        """
        Test: GET /BookStore/v1/Book with invalid ISBN
        Description: Try to fetch book that doesn't exist
        Expected: Status 400, error message
        """

        # Invalid ISBN
        invalid_isbn = "9999999999999"

        # Make GET request
        response = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Book",
            params={"ISBN": invalid_isbn}
        )
        
        if response.status == 502:
            pytest.xfail("DemoQA BookStore API is down (502 Bad Gateway)")

        print(f"\n📡 Request: GET /BookStore/v1/Book?ISBN={invalid_isbn}")
        print(f"📡 Status Code: {response.status}")

        # Expect 400 Bad Request
        assert response.status == 400, f"Expected 400 for invalid ISBN, got {response.status}"
        print("✅ Status code is 400 (Bad Request)")

        # Parse response
        error_response = response.json()

        # Verify error message exists
        assert "message" in error_response or "code" in error_response, "Should return error details"
        print(f"✅ Error response: {error_response}")
