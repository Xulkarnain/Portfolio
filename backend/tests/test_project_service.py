import pytest

from app.core.exceptions import ResourceNotFoundException
from app.services.project import ProjectService


class FakeProjectRepository:
    def get_published_projects(self):
        return [
            "project-1",
            "project-2",
        ]

    def get_by_id(self, project_id: int):
        if project_id == 1:
            return "project-1"

        return None


def test_get_public_projects():
    repository = FakeProjectRepository()
    service = ProjectService(repository)

    projects = service.get_public_projects()

    assert projects == [
        "project-1",
        "project-2",
    ]


def test_get_project():
    repository = FakeProjectRepository()
    service = ProjectService(repository)

    project = service.get_project(1)

    assert project == "project-1"


def test_get_project_not_found():
    repository = FakeProjectRepository()
    service = ProjectService(repository)

    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.get_project(999)

    assert exc_info.value.resource == "Project"
    assert exc_info.value.resource_id == 999