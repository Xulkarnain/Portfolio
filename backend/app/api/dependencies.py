from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.project import ProjectRepository
from app.services.project import ProjectService


def get_project_repository(
    db: Session = Depends(get_db),
) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)