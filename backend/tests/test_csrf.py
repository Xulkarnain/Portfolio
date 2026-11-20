
import getpass

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

email = input("Admin email: ").strip()
password = getpass.getpass("Admin password: ")

# Login and obtain both cookies
login_response = client.post(
    "/api/v1/admin/auth/login",
    json={"email": email, "password": password},
)

print("\nLogin status:", login_response.status_code)

if login_response.status_code != 200:
    raise RuntimeError("Login failed. CSRF tests stopped.")

csrf_token = client.cookies.get("admin_csrf_token")

if not csrf_token:
    raise RuntimeError("CSRF cookie was not created.")

# Test 1: Missing CSRF header
missing_response = client.post(
    "/api/v1/admin/auth/csrf-check"
)

print("\n--- Missing CSRF Header ---")
print("Status:", missing_response.status_code)
print("Rejected:", missing_response.status_code == 403)

# Test 2: Incorrect CSRF header
invalid_response = client.post(
    "/api/v1/admin/auth/csrf-check",
    headers={"X-CSRF-Token": "invalid-token"},
)

print("\n--- Invalid CSRF Header ---")
print("Status:", invalid_response.status_code)
print("Rejected:", invalid_response.status_code == 403)

# Test 3: Correct CSRF header
valid_response = client.post(
    "/api/v1/admin/auth/csrf-check",
    headers={"X-CSRF-Token": csrf_token},
)

print("\n--- Valid CSRF Header ---")
print("Status:", valid_response.status_code)
print("Response:", valid_response.json())
print("Accepted:", valid_response.status_code == 200)
