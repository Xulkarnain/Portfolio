
import getpass

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test 1: Access without authentication
response = client.get("/api/v1/admin/auth/me")

print("\n--- Without Authentication ---")
print("Status:", response.status_code)
print("Response:", response.json())

# Login
email = input("\nAdmin email: ").strip()
password = getpass.getpass("Admin password: ")

login_response = client.post(
    "/api/v1/admin/auth/login",
    json={
        "email": email,
        "password": password,
    },
)

print("\n--- Login ---")
print("Status:", login_response.status_code)

# Test 2: Access with authentication cookie
if login_response.status_code == 200:
    profile_response = client.get("/api/v1/admin/auth/me")

    print("\n--- With Authentication ---")
    print("Status:", profile_response.status_code)
    print("Profile:", profile_response.json())
else:
    print("Login failed. Protected endpoint test skipped.")
