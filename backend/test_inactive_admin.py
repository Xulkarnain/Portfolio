
from fastapi.testclient import TestClient

from app.main import app
from app.database.session import SessionLocal
from app.models.admin_user import AdminUser
from app.core.security import create_access_token

client = TestClient(app)
db = SessionLocal()

try:
    admin = db.get(AdminUser, 1)

    if admin is None:
        raise RuntimeError("Admin account not found")

    original_status = admin.is_active

    # Disable the admin account
    admin.is_active = False
    db.commit()

    # Generate a valid JWT for this admin
    token = create_access_token(str(admin.id))

    client.cookies.set("admin_access_token", token)

    response = client.get("/api/v1/admin/auth/me")

    print("--- Inactive Admin Test ---")
    print("Status:", response.status_code)
    print("Response:", response.json())
    print("Inactive admin rejected:", response.status_code == 401)

finally:
    # Restore the original account status
    if "original_status" in locals() and admin is not None:
        admin.is_active = original_status
        db.commit()

    db.close()
