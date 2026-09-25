from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, func , DateTime
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.database.base import Base


class SkillCategory(Base):
    __tablename__ = "skill_categories"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        back_populates="skill_category",
    )

    name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
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