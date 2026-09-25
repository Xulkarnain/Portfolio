from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column ,relationship

from app.database.base import Base


class Education(Base):
    __tablename__ = "education"

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
        back_populates="education",
    )

    institution: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    degree: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    field_of_study: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    grade: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="chk_education_dates",
        ),
    )