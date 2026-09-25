from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.database.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    skill_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "skill_categories.id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    skill_category: Mapped["SkillCategory"] = relationship(
        "SkillCategory",
        back_populates="skills",
    )

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary="project_skills",
        back_populates="skills",
    )

    name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    proficiency_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
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

    experiences: Mapped[list["Experience"]] = relationship(
        "Experience",
        secondary="experience_skills",
        back_populates="skills",
    )

    __table_args__ = (
        CheckConstraint(
            "proficiency_level IN "
            "('beginner', 'intermediate', 'advanced', 'expert')",
            name="chk_skills_proficiency_level",
        ),
        UniqueConstraint(
            "skill_category_id",
            "name",
            name="uq_skills_category_name",
        ),
    )