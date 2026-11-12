
import getpass

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.admin_user import AdminUser
from app.core.security import hash_password


def create_admin():
    email = input("Admin email: ").strip().lower()

    password = getpass.getpass("Admin password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if not email or not password:
        print("Email and password are required.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    if len(password) < 12:
        print("Password must contain at least 12 characters.")
        return

    db = SessionLocal()

    try:
        existing_admin = db.scalar(
            select(AdminUser).where(AdminUser.email == email)
        )

        if existing_admin:
            print("An admin with this email already exists.")
            return

        admin = AdminUser(
            email=email,
            hashed_password=hash_password(password),
        )

        db.add(admin)
        db.commit()

        print(f"Admin account created successfully: {email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
