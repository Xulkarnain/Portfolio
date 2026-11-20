
from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_project_service,
    require_admin_mutation_security,
)
from app.schemas.project import AdminProjectCreate, AdminProjectResponse
from app.services.project import ProjectService


router = APIRouter(
    prefix="/admin/projects",
    tags=["Admin Projects"],
)


@router.post(
    "",
    response_model=AdminProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_mutation_security)],
)
def create_admin_project(
    project_data: AdminProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(project_data)
