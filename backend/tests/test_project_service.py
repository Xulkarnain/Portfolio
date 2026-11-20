import pytest

from app.core.exceptions import PortfolioOwnerNotFoundException, ResourceNotFoundException 
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


from types import SimpleNamespace

from app.core.exceptions import (
    DuplicateResourceException,
    InvalidInputException,
    InvalidReferenceException,
)
from app.schemas.project import AdminProjectCreate


class FakeDatabase:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


class FakeProjectCreationRepository:
    def __init__(self):
        self.db = FakeDatabase()
        self.owner = SimpleNamespace(id=1)
        self.skills = [
            SimpleNamespace(id=10),
            SimpleNamespace(id=20),
        ]
        self.existing_project = None
        self.created_data = None
        self.created_project = None

    def get_portfolio_owner(self):
        return self.owner

    def get_by_slug(self, slug):
        return self.existing_project

    def get_skills_by_ids(self, skill_ids):
        return [
            skill for skill in self.skills
            if skill.id in skill_ids
        ]

    def create(self, project_data, owner_id, skills, categories):
        self.created_data = {
            **project_data,
            "owner_id": owner_id,
        }

        self.created_project = SimpleNamespace(
            id=101,
            **project_data,
            owner_id=owner_id,
        )

        return self.created_project
    def get_by_id(self, project_id):
        if self.created_project and self.created_project.id == project_id:
            return self.created_project

        return None


def make_project_data(**overrides):
    data = {
        "title": "AI Recommendation Engine",
        "slug": "ai-recommendation-engine",
        "short_description": "An adaptive learning recommendation system",
        "detailed_description": "A project description",
        "github_url": "https://github.com/example/project",
        "live_url": None,
        "is_featured": False,
        "is_published": False,
        "display_order": 1,
        "categories": ["ai", "backend"],
        "skill_ids": [10, 20],
    }

    data.update(overrides)
    return AdminProjectCreate(**data)


def test_create_project_success():
    repository = FakeProjectCreationRepository()
    service = ProjectService(repository)

    project = service.create_project(make_project_data())

    assert project.id == 101
    assert repository.created_data["title"] == "AI Recommendation Engine"
    assert repository.created_data["owner_id"] == 1
    assert isinstance(repository.created_data["github_url"], str)
    assert repository.db.committed is True
    assert repository.db.rolled_back is False


def test_create_project_duplicate_slug():
    repository = FakeProjectCreationRepository()
    repository.existing_project = SimpleNamespace(id=5)

    service = ProjectService(repository)

    with pytest.raises(DuplicateResourceException):
        service.create_project(make_project_data())

    assert repository.db.rolled_back is True
    assert repository.db.committed is False


def test_create_project_invalid_skill_id():
    repository = FakeProjectCreationRepository()
    service = ProjectService(repository)

    data = make_project_data(skill_ids=[10, 999])

    with pytest.raises(InvalidReferenceException) as exc_info:
        service.create_project(data)

    assert exc_info.value.invalid_ids == [999]
    assert repository.db.rolled_back is True


def test_create_project_duplicate_skill_ids():
    repository = FakeProjectCreationRepository()
    service = ProjectService(repository)

    data = make_project_data(skill_ids=[10, 10])

    with pytest.raises(InvalidInputException):
        service.create_project(data)

    assert repository.db.rolled_back is True
    assert repository.db.committed is False

def test_create_project_without_portfolio_owner():
    repository = FakeProjectCreationRepository()
    repository.owner = None

    service = ProjectService(repository)

    with pytest.raises(PortfolioOwnerNotFoundException):
        service.create_project(make_project_data())

    assert repository.db.rolled_back is True
    assert repository.db.committed is False
    assert repository.created_project is None