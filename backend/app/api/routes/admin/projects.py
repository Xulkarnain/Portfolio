
from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.api.dependencies import (
    get_project_service,
    require_admin_mutation_security,
)
from app.schemas.project import AdminProjectCreate, AdminProjectUpdate,AdminProjectResponse
from app.services.project import ProjectService


router = APIRouter(
    prefix="/admin/projects",
    tags=["Admin Projects"],
)
@router.get(
    "/{project_id}",
    response_model=AdminProjectResponse,
)
def get_admin_project(
    project_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_project(project_id)
@router.get(
    "",
    response_model=list[AdminProjectResponse],
)
def get_admin_projects(
    current_admin: AdminUser = Depends(get_current_admin),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_all_projects()
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
@router.put(
    "/{project_id}",
    response_model=AdminProjectResponse,
    dependencies=[Depends(require_admin_mutation_security)],
)
def update_admin_project(
    project_id: int,
    project_data: AdminProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    return service.update_project(project_id, project_data)