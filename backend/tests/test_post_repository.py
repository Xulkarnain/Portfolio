from app.database.session import SessionLocal
from app.repositories.post import PostRepository


def test_get_all_published_posts():
    db = SessionLocal()

    try:
        repository = PostRepository(db)

        posts = repository.get_all_published_posts()

        # Verify published post count
        assert len(posts) == 1

        post = posts[0]

        # Verify post details
        assert post.title == "Building My Production Portfolio Backend"
        assert post.slug == "building-my-production-portfolio-backend"
        assert post.source == "portfolio"

        # Verify publication status
        assert post.published_at is not None

        # Verify unpublished/future posts are excluded
        from datetime import datetime, timezone

        assert post.published_at <= datetime.now(timezone.utc)

    finally:
        db.close()


def test_get_published_post_by_slug():
    db = SessionLocal()

    try:
        repository = PostRepository(db)

        post = repository.get_published_post_by_slug(
            "building-my-production-portfolio-backend"
        )

        assert post is not None
        assert post.title == "Building My Production Portfolio Backend"

    finally:
        db.close()


def test_get_published_post_by_invalid_slug():
    db = SessionLocal()

    try:
        repository = PostRepository(db)

        post = repository.get_published_post_by_slug(
            "non-existent-blog-post"
        )

        assert post is None

    finally:
        db.close()