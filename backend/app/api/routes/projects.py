from fastapi import APIRouter, Depends

from app.api.dependencies import get_project_service
from app.schemas.project import ProjectResponse
from app.services.project import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=list[ProjectResponse])
def get_projects(
    service: ProjectService = Depends(get_project_service),
):
    return service.get_public_projects()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    return service.get_project(project_id)