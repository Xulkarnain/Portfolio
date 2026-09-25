from datetime import datetime

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, func , DateTime
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    owner_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="projects",
    )
    

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
        unique=True,
    )

    short_description: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    detailed_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    github_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    live_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
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

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="project_skills",
        back_populates="projects",
    )