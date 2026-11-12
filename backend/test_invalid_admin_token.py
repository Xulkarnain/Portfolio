
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Set a deliberately invalid JWT
client.cookies.set(
    "admin_access_token",
    "this.is.not.a.valid.jwt",
)

response = client.get("/api/v1/admin/auth/me")

print("--- Invalid JWT Test ---")
print("Status:", response.status_code)
print("Response:", response.json())

print(
    "Invalid token rejected:",
    response.status_code == 401,
)
