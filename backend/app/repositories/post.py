from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_published_posts(self) -> list[Post]:
        now = datetime.now(timezone.utc)

        statement = (
            select(Post)
            .where(
                Post.published_at.is_not(None),
                Post.published_at <= now,
            )
            .order_by(Post.published_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def get_published_post_by_slug(self, slug: str) -> Post | None:
        now = datetime.now(timezone.utc)

        statement = (
            select(Post)
            .where(
                Post.slug == slug,
                Post.published_at.is_not(None),
                Post.published_at <= now,
            )
        )

        return self.db.scalar(statement)