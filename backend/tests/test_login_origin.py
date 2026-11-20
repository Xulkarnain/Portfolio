
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test 1: Trusted local frontend
trusted_response = client.post(
    "/api/v1/admin/auth/login",
    headers={"Origin": "http://localhost:5500"},
    json={
        "email": "darzulkarnain@gmail.com",
        "password": "dummy-password",
    },
)

print("--- Trusted Origin ---")
print("Status:", trusted_response.status_code)
print("Origin accepted:", trusted_response.status_code != 403)

# Test 2: Untrusted origin
untrusted_response = client.post(
    "/api/v1/admin/auth/login",
    headers={"Origin": "https://attacker.example"},
    json={
        "email": "darzulkarnain@gmail.com",
        "password": "dummy-password",
    },
)

print("\n--- Untrusted Origin ---")
print("Status:", untrusted_response.status_code)
print("Origin rejected:", untrusted_response.status_code == 403)

# Test 3: Missing origin
missing_response = client.post(
    "/api/v1/admin/auth/login",
    json={
        "email": "darzulkarnain@gmail.com",
        "password": "dummy-password",
    },
)

print("\n--- Missing Origin ---")
print("Status:", missing_response.status_code)
print("Origin rejected:", missing_response.status_code == 403)
