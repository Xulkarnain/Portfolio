from app.core.exceptions import ResourceNotFoundException
from app.repositories.project import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_public_projects(self):
        return self.repository.get_published_projects()

    def get_project(self, project_id: int):
        project = self.repository.get_by_id(project_id)

        if project is None:
            raise ResourceNotFoundException("Project", project_id)

        return project