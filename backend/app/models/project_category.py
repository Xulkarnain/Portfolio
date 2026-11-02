from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProjectCategory(Base):
    __tablename__ = "project_categories"

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )

    category: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="category_assignments",
    )

    __table_args__ = (
        CheckConstraint(
            "category IN ('ai', 'backend', 'data')",
            name="ck_project_categories_valid_category",
        ),
        Index(
            "idx_project_categories_category",
            "category",
        ),
    )