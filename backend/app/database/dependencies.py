from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.admin import AdminRepository
from app.services.auth import AuthService

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    repository = AdminRepository(db)
    return AuthService(repository)