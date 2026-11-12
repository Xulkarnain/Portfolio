from app.repositories.admin import AdminRepository
from app.services.auth import AuthService
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Cookie, HTTPException, status
from fastapi import Header
from app.core.security import verify_csrf_token
import hmac
from fastapi import Request
from app.core.security import decode_access_token
from app.models.admin_user import AdminUser
from app.database.dependencies import get_db
from app.repositories.project import ProjectRepository
from app.services.project import ProjectService
from app.repositories.skill import SkillRepository
from app.services.skill import SkillService
from app.repositories.experience import ExperienceRepository
from app.services.experience import ExperienceService
from app.repositories.education import EducationRepository
from app.services.education import EducationService
from app.repositories.certification import CertificationRepository
from app.services.certification import CertificationService
from app.repositories.post import PostRepository
from app.services.post import PostService
from app.repositories.contact import ContactRepository
from app.services.contact import ContactService


def get_project_repository(
    db: Session = Depends(get_db),
) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)

def get_skill_repository(db: Session = Depends(get_db)) -> SkillRepository:
    return SkillRepository(db)


def get_skill_service(
    repository: SkillRepository = Depends(get_skill_repository),
) -> SkillService:
    return SkillService(repository)

def get_experience_repository(
    db: Session = Depends(get_db),
) -> ExperienceRepository:
    return ExperienceRepository(db)


def get_experience_service(
    repository: ExperienceRepository = Depends(get_experience_repository),
) -> ExperienceService:
    return ExperienceService(repository)

def get_education_repository(
    db: Session = Depends(get_db),
) -> EducationRepository:
    return EducationRepository(db)


def get_education_service(
    repository: EducationRepository = Depends(get_education_repository),
) -> EducationService:
    return EducationService(repository)

def get_certification_repository(
    db: Session = Depends(get_db),
) -> CertificationRepository:
    return CertificationRepository(db)


def get_certification_service(
    repository: CertificationRepository = Depends(get_certification_repository),
) -> CertificationService:
    return CertificationService(repository)

def get_post_repository(
    db: Session = Depends(get_db),
) -> PostRepository:
    return PostRepository(db)


def get_post_service(
    repository: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(repository)

def get_contact_repository(
    db: Session = Depends(get_db),
) -> ContactRepository:
    return ContactRepository(db)


def get_contact_service(
    repository: ContactRepository = Depends(get_contact_repository),
) -> ContactService:
    return ContactService(repository)

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    repository = AdminRepository(db)
    return AuthService(repository)

def get_current_admin(
    token: str | None = Cookie(default=None, alias="admin_access_token"),
    db: Session = Depends(get_db),
) -> AdminUser:

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )

    try:
        admin_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    admin_repository = AdminRepository(db)
    admin = admin_repository.get_by_id(admin_id)

    if admin is None or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin account is unavailable",
        )

    return admin

def require_csrf_token(
    access_token: str | None = Cookie(
        default=None,
        alias="admin_access_token",
    ),
    csrf_cookie: str | None = Cookie(
        default=None,
        alias="admin_csrf_token",
    ),
    csrf_header: str | None = Header(
        default=None,
        alias="X-CSRF-Token",
    ),
) -> None:

    if not access_token or not csrf_cookie or not csrf_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing",
        )

    if not hmac.compare_digest(csrf_cookie, csrf_header):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token mismatch",
        )

    if not verify_csrf_token(access_token, csrf_cookie):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token",
        )

ALLOWED_ADMIN_ORIGINS = {
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://zulkarnain.vercel.app",
}


def require_admin_origin(request: Request) -> None:
    origin = request.headers.get("origin")

    if origin not in ALLOWED_ADMIN_ORIGINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Untrusted request origin",
        )

def require_admin_mutation_security(
    _: AdminUser = Depends(get_current_admin),
    __: None = Depends(require_admin_origin),
    ___: None = Depends(require_csrf_token),
) -> None:
    pass