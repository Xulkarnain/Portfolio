from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )

    skill_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "skills.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )