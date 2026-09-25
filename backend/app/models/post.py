from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column , relationship 

from app.database.base import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    owner_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    external_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(280),
        nullable=False,
        unique=True,
    )

    excerpt: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cover_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "source IN ('portfolio', 'devto', 'medium', 'linkedin')",
            name="chk_posts_source",
        ),
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_posts_source_external_id",
        ),
    )