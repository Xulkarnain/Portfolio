
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser


class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> AdminUser | None:
        statement = select(AdminUser).where(
            AdminUser.email == email
        )

        return self.db.scalar(statement)

    def get_by_id(self, admin_id: int) -> AdminUser | None:
        statement = select(AdminUser).where(
            AdminUser.id == admin_id
        )

        return self.db.scalar(statement)

    def create(
        self,
        email: str,
        hashed_password: str,
    ) -> AdminUser:
        admin = AdminUser(
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(admin)
        self.db.flush()

        return admin
