from fastapi import Depends
from sqlalchemy.orm import Session

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