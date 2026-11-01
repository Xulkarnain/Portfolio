from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_post_service
from app.core.exceptions import ResourceNotFoundException


class FakePost:
    def __init__(self):
        self.source = "portfolio"
        self.title = "Building My Production Portfolio Backend"
        self.slug = "building-my-production-portfolio-backend"
        self.excerpt = "How I designed and built my portfolio backend."
        self.cover_image_url = None
        self.published_at = datetime(2026, 9, 19, 10, 34, tzinfo=timezone.utc)
        self.content = "Full article content goes here."
        self.external_url = None


class FakePostService:
    def get_public_posts(self):
        return [FakePost()]

    def get_public_post(self, slug):
        if slug == "building-my-production-portfolio-backend":
            return FakePost()

        raise ResourceNotFoundException("Post", slug)


def test_get_blog_posts():
    app.dependency_overrides[get_post_service] = FakePostService

    try:
        client = TestClient(app)
        response = client.get("/api/v1/blog")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["title"] == "Building My Production Portfolio Backend"
        assert data[0]["slug"] == "building-my-production-portfolio-backend"

        # Listing should not expose full article content
        assert "content" not in data[0]
        assert "external_url" not in data[0]

    finally:
        app.dependency_overrides.clear()


def test_get_blog_post():
    app.dependency_overrides[get_post_service] = FakePostService

    try:
        client = TestClient(app)
        response = client.get(
            "/api/v1/blog/building-my-production-portfolio-backend"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["title"] == "Building My Production Portfolio Backend"
        assert data["content"] == "Full article content goes here."
        assert data["external_url"] is None

        # Internal fields should not be exposed
        assert "id" not in data
        assert "owner_id" not in data
        assert "created_at" not in data

    finally:
        app.dependency_overrides.clear()


def test_get_blog_post_not_found():
    app.dependency_overrides[get_post_service] = FakePostService

    try:
        client = TestClient(app)
        response = client.get("/api/v1/blog/non-existent-post")

        assert response.status_code == 404

    finally:
        app.dependency_overrides.clear()