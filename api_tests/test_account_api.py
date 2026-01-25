"""
API Tests: Account/User API
Tests user creation, authentication, and account management
"""

import pytest
import random
import string
from playwright.sync_api import APIRequestContext


class TestAccountAPI:
    """Test suite for Account API endpoints"""
    
    BASE_URL = "https://demoqa.com"
    
    
    def generate_random_username(self):
        """Generate random username to avoid conflicts"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_str}"
    
    
    def test_create_user_account(self, api_request):
        """
        Test: POST /Account/v1/User
        Description: Create a new user account
        Expected: Status 201, returns user ID and username
        """
        request_context = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )
        
        # Generate unique username
        username = self.generate_random_username()
        password = "Test@12345"  # Meets password requirements
        
        print(f"\n📝 Creating user account...")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        
        
        
        # Make POST request
        response = api_request.post(
            "/Account/v1/User",
            data={
                "userName": username,
                "password": password
            }
        )
        
        print(f"\n📡 Status Code: {response.status}")
        print(f"📄 Response: {response.text()}")
        
        # Assertions
        assert response.status == 201, f"Expected 201 Created, got {response.status}"
        print("✅ Status code is 201 (Created)")
        
        # Parse response
        user_data = response.json()
        
        # Verify response structure
        assert "userID" in user_data, "Response should contain userID"
        assert "username" in user_data, "Response should contain username"
        assert "books" in user_data, "Response should contain books array"
        
        print(f"✅ User created successfully!")
        print(f"   User ID: {user_data['userID']}")
        print(f"   Username: {user_data['username']}")
        print(f"   Books: {user_data['books']}")
        
        # Verify username matches
        assert user_data["username"] == username, "Username should match"
        
        # Verify books array is empty for new user
        assert isinstance(user_data["books"], list), "Books should be a list"
        assert len(user_data["books"]) == 0, "New user should have no books"
        
        print("✅ All validations passed!")
        
    
    def test_create_user_with_weak_password(self, api_request):
        """
        Test: POST /Account/v1/User with weak password
        Description: Try to create user with password that doesn't meet requirements
        Expected: Status 400, error message
        """
        request_context = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )
        
        username = self.generate_random_username()
        weak_password = "test123"  # No uppercase, no special char
        
        print(f"\n🔓 Attempting to create user with weak password...")
        print(f"   Password: {weak_password}")
        
        
        response = api_request.post(
            "/Account/v1/User",
            data={
                "userName": username,
                "password": "test123"
            }
        )
        
        print(f"\n📡 Status Code: {response.status}")
        print(f"📄 Response: {response.text()}")
        
        # Should fail with 400 Bad Request
        assert response.status == 400, f"Expected 400 for weak password, got {response.status}"
        print("✅ Status code is 400 (Bad Request)")
        
        # Verify error message
        error_data = response.json()
        assert "code" in error_data or "message" in error_data, "Should return error details"
        print(f"✅ Error response: {error_data}")
        
        
    
    
    def test_generate_token(self, api_request):
        """
        Test: POST /Account/v1/GenerateToken
        Description: Generate authentication token for valid user
        Expected: Status 200, returns token
        """
        request_context = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )
        
        # First, create a user
        username = self.generate_random_username()
        password = "Test@12345"
        
        print(f"\n🔐 Step 1: Creating user account...")
        create_response = api_request.post(
            "/Account/v1/User",
            data={"userName": username, "password": password}
        )
        
        assert create_response.status == 201, "User creation should succeed"
        user_data = create_response.json()
        print(f"✅ User created: {username}")
        
        # Now, generate token
        print(f"\n🎫 Step 2: Generating authentication token...")
        
        token_response = api_request.post(
            "/Account/v1/GenerateToken",
            data={"userName": username, "password": password}
        )
        
        print(f"\n📡 Status Code: {token_response.status}")
        print(f"📄 Response: {token_response.text()}")
        
        # Assertions
        assert token_response.status == 200, f"Expected 200, got {token_response.status}"
        print("✅ Status code is 200")
        
        # Parse response
        token_data = token_response.json()
        
        # Verify response structure
        assert "token" in token_data, "Response should contain token"
        assert "status" in token_data, "Response should contain status"
        assert "result" in token_data, "Response should contain result"
        
        # Verify token is not empty
        assert token_data["token"] != "", "Token should not be empty"
        assert token_data["status"] == "Success", "Status should be Success"
        assert token_data["result"] == "User authorized successfully.", "Should show authorization message"
        
        print(f"✅ Token generated successfully!")
        print(f"   Token: {token_data['token'][:50]}... (truncated)")
        print(f"   Status: {token_data['status']}")
        print(f"   Result: {token_data['result']}")
        
    
    
    def test_generate_token_invalid_credentials(self, api_request):
        """
        Test: POST /Account/v1/GenerateToken with wrong password
        Description: Try to generate token with invalid credentials
        Expected: Status 200 but result = "User authorization failed"
        """
        request_context = api_request.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )
        
        print(f"\n🔓 Attempting to generate token with invalid credentials...")
        
        token_response = api_request.post(
            "/Account/v1/GenerateToken",
            data={
                "userName": "nonexistentuser",
                "password": "WrongPassword@123"
            }
        )
        
        print(f"\n📡 Status Code: {token_response.status}")
        print(f"📄 Response: {token_response.text()}")
        
        # DemoQA returns 200 even for failed auth (not ideal, but that's the API)
        assert token_response.status == 200, f"Expected 200, got {token_response.status}"
        
        token_data = token_response.json()
        
        # Token should be null/empty
        assert token_data["token"] == None or token_data["token"] == "", "Token should be empty for invalid credentials"
        assert token_data["status"] == "Failed", "Status should be Failed"
        assert "authorization failed" in token_data["result"].lower(), "Should indicate authorization failure"
        
        print("✅ Invalid credentials correctly rejected")
        print(f"   Status: {token_data['status']}")
        print(f"   Result: {token_data['result']}")
        
        