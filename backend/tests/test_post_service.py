import pytest

from app.services.post import PostService
from app.core.exceptions import ResourceNotFoundException


class FakePost:
    def __init__(self, title, slug):
        self.title = title
        self.slug = slug


class FakePostRepository:
    def get_all_published_posts(self):
        return [
            FakePost(
                "Building My Production Portfolio Backend",
                "building-my-production-portfolio-backend",
            )
        ]

    def get_published_post_by_slug(self, slug):
        if slug == "building-my-production-portfolio-backend":
            return FakePost(
                "Building My Production Portfolio Backend",
                slug,
            )

        return None


def test_get_public_posts():
    repository = FakePostRepository()
    service = PostService(repository)

    posts = service.get_public_posts()

    assert len(posts) == 1
    assert posts[0].title == "Building My Production Portfolio Backend"


def test_get_public_post():
    repository = FakePostRepository()
    service = PostService(repository)

    post = service.get_public_post(
        "building-my-production-portfolio-backend"
    )

    assert post is not None
    assert post.title == "Building My Production Portfolio Backend"


def test_get_public_post_not_found():
    repository = FakePostRepository()
    service = PostService(repository)

    with pytest.raises(ResourceNotFoundException):
        service.get_public_post("non-existent-post")