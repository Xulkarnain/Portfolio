
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)

# Create a correctly signed JWT that has already expired
expired_token = jwt.encode(
    {
        "sub": "1",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        "iss": settings.app_name,
        "aud": "portfolio-admin",
    },
    settings.jwt_secret_key,
    algorithm=settings.jwt_algorithm,
)

client.cookies.set("admin_access_token", expired_token)

response = client.get("/api/v1/admin/auth/me")

print("--- Expired JWT Test ---")
print("Status:", response.status_code)
print("Response:", response.json())
print("Expired token rejected:", response.status_code == 401)
