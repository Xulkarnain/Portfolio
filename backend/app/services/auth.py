
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.admin import AdminRepository


class AuthService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def authenticate_admin(
        self,
        email: str,
        password: str,
    ) -> tuple[str, int] | None:
        admin = self.repository.get_by_email(email)

        if admin is None or not admin.is_active:
            return None

        if not verify_password(password, admin.hashed_password):
            return None

        token = create_access_token(str(admin.id))

        return token, admin.id
    