"""
API Tests: Account API
Tests the DemoQA Account-related endpoints

NOTE:
- Uses requests-based api_request fixture
- DemoQA is a public demo API and may behave inconsistently
"""

import pytest
import random
import string


class TestAccountAPI:
    """Test suite for Account API endpoints"""

    def _generate_username(self):
        """Generate a random username to avoid duplicates"""
        return "testuser_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def test_create_user_account(self, api_request):
        """
        Test: POST /Account/v1/User
        Description: Create a new user account
        Expected: Status 201, user created successfully
        """

        print("\n🧪 TEST STARTED: Create User Account")

        username = self._generate_username()
        password = "Test@12345"

        payload = {
            "userName": username,
            "password": password
        }

        print("📝 Creating user account...")
        print(f"   Username: {username}")
        print(f"   Password: {password}")

        response = api_request.post("/Account/v1/User", json=payload)

        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text}")

        # DemoQA sometimes returns 400 if username already exists
        if response.status_code == 400:
            pytest.xfail("⚠️ DemoQA rejected user creation (possibly duplicate user)")

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        print("✅ User created successfully")

        response_json = response.json()
        assert "userID" in response_json, "userID should be present in response"
        print(f"✅ User ID created: {response_json['userID']}")

        print("🏁 TEST COMPLETED: Create User Account")

    def test_create_user_with_weak_password(self, api_request):
        """
        Test: POST /Account/v1/User with weak password
        Description: Attempt user creation with invalid password
        Expected: Status 400, validation error
        """

        print("\n🧪 TEST STARTED: Create User with Weak Password")

        username = self._generate_username()
        weak_password = "test123"

        payload = {
            "userName": username,
            "password": weak_password
        }

        print("🔓 Attempting to create user with weak password...")
        print(f"   Password: {weak_password}")

        response = api_request.post("/Account/v1/User", json=payload)

        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("✅ Correctly rejected weak password")

        error_response = response.json()
        assert "message" in error_response, "Error message should be returned"
        print(f"✅ Error message received: {error_response['message']}")

        print("🏁 TEST COMPLETED: Weak Password Validation")

    def test_generate_token(self, api_request):
        """
        Test: POST /Account/v1/GenerateToken
        Description: Generate auth token for valid user
        Expected: Status 200, token generated
        """

        print("\n🧪 TEST STARTED: Generate Token")

        # Step 1: Create user
        username = self._generate_username()
        password = "Test@12345"

        print("🔐 Step 1: Creating user account...")

        create_response = api_request.post(
            "/Account/v1/User",
            json={"userName": username, "password": password}
        )

        if create_response.status_code != 201:
            pytest.xfail("⚠️ User creation failed, cannot test token generation")

        print("✅ User created successfully")

        # Step 2: Generate token
        print("🔐 Step 2: Generating token...")

        token_response = api_request.post(
            "/Account/v1/GenerateToken",
            json={"userName": username, "password": password}
        )

        print(f"\n📡 Status Code: {token_response.status_code}")
        print(f"📄 Response Body: {token_response.text}")

        assert token_response.status_code == 200, f"Expected 200, got {token_response.status_code}"
        print("✅ Token generated successfully")

        token_json = token_response.json()
        assert token_json.get("token"), "Token should be present"
        print(f"🔑 Token: {token_json['token'][:25]}...")

        print("🏁 TEST COMPLETED: Generate Token")

    def test_generate_token_invalid_credentials(self, api_request):
        """
        Test: POST /Account/v1/GenerateToken with invalid credentials
        Description: Attempt token generation with wrong password
        Expected: Status 200 but authorized = false (DemoQA behavior)
        """

        print("\n🧪 TEST STARTED: Generate Token with Invalid Credentials")

        payload = {
            "userName": "invalid_user",
            "password": "WrongPassword123"
        }

        print("🔓 Attempting to generate token with invalid credentials...")

        response = api_request.post("/Account/v1/GenerateToken", json=payload)

        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text}")

        assert response.status_code == 200, "DemoQA returns 200 even for invalid creds"

        response_json = response.json()
        assert response_json.get("status") == "Failed"
        assert response_json.get("result") == "User authorization failed."

        print("✅ Invalid credentials correctly rejected")
        print("🏁 TEST COMPLETED: Invalid Token Generation")
