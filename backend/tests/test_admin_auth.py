
import getpass

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

email = input("Admin email: ").strip()
password = getpass.getpass("Admin password: ")

# Test 1: Correct credentials
response = client.post(
    "/api/v1/admin/auth/login",
    json={
        "email": email,
        "password": password,
    },
)

print("CSRF cookie set:", bool(response.cookies.get("admin_csrf_token")))

csrf_cookie = response.headers.get_list("set-cookie")

for cookie in csrf_cookie:
    print(
        "Cookie attributes:",
        cookie.split(";")[1:]
    )

print("\n--- Correct Credentials ---")
print("Status code:", response.status_code)
print("Response:", response.json())

cookie_header = response.headers.get("set-cookie", "").lower()

print(
    "Authentication cookie set:",
    bool(response.cookies.get("admin_access_token")),
)
print("HTTP-only cookie:", "httponly" in cookie_header)
print("SameSite=Lax:", "samesite=lax" in cookie_header)
print("JWT exposed in response:", "access_token" in response.json())

# Test 2: Incorrect credentials
wrong_response = client.post(
    "/api/v1/admin/auth/login",
    json={
        "email": email,
        "password": "DefinitelyWrongPassword123!",
    },
)

print("\n--- Incorrect Credentials ---")
print("Status code:", wrong_response.status_code)
print("Response:", wrong_response.json())
