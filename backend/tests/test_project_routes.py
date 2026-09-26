from fastapi.testclient import TestClient

from app.api.dependencies import get_project_service
from app.core.exceptions import ResourceNotFoundException
from app.main import app


class FakeProject:
    def __init__(self, project_id: int, title: str):
        self.id = project_id
        self.owner_id = 1
        self.title = title
        self.slug = title.lower().replace(" ", "-")
        self.short_description = "Test project"
        self.detailed_description = None
        self.github_url = None
        self.live_url = None
        self.is_featured = True
        self.is_published = True
        self.display_order = project_id
        self.created_at = "2026-01-01T00:00:00+00:00"
        self.updated_at = "2026-01-01T00:00:00+00:00"


class FakeProjectService:
    def get_public_projects(self):
        return [
            FakeProject(1, "Project One"),
            FakeProject(2, "Project Two"),
        ]

    def get_project(self, project_id: int):
        if project_id == 1:
            return FakeProject(1, "Project One")

        raise ResourceNotFoundException("Project", project_id)


def test_get_projects():
    app.dependency_overrides[get_project_service] = (
        lambda: FakeProjectService()
    )

    client = TestClient(app)

    try:
        response = client.get("/api/v1/projects")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 2

        assert data[0]["id"] == 1
        assert data[0]["title"] == "Project One"

        assert data[1]["id"] == 2
        assert data[1]["title"] == "Project Two"

    finally:
        app.dependency_overrides.clear()


def test_get_project():
    app.dependency_overrides[get_project_service] = (
        lambda: FakeProjectService()
    )

    client = TestClient(app)

    try:
        response = client.get("/api/v1/projects/1")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 1
        assert data["title"] == "Project One"

    finally:
        app.dependency_overrides.clear()


def test_get_project_not_found():
    app.dependency_overrides[get_project_service] = (
        lambda: FakeProjectService()
    )

    client = TestClient(app)

    try:
        response = client.get("/api/v1/projects/9999")

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Project with id 9999 was not found"
        }

    finally:
        app.dependency_overrides.clear()

def test_get_project_invalid_id():
    app.dependency_overrides[get_project_service] = (
        lambda: FakeProjectService()
    )

    client = TestClient(app)

    try:
        response = client.get("/api/v1/projects/abc")

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()