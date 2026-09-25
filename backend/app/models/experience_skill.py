from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ExperienceSkill(Base):
    __tablename__ = "experience_skills"

    experience_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "experiences.id",
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