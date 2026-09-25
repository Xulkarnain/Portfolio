from datetime import datetime

from sqlalchemy import BigInteger, String, Text, func , DateTime
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
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

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="owner",
    )

    experiences: Mapped[list["Experience"]] = relationship(
        "Experience",
        back_populates="owner",
    )

    education: Mapped[list["Education"]] = relationship(
        "Education",
        back_populates="owner",
    )

    certifications: Mapped[list["Certification"]] = relationship(
        "Certification",
        back_populates="owner",
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="owner",
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="owner",
    )