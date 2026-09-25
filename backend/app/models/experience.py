from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column , relationship 

from app.database.base import Base


class Experience(Base):
    __tablename__ = "experiences"

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
        back_populates="experiences",
    )

    company: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    role_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
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

    is_current: Mapped[bool] = mapped_column(
        nullable=False,
        server_default="false",
    )

    external_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        nullable=False,
        server_default="0",
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "employment_type IN "
            "('full_time', 'part_time', 'contract', "
            "'internship', 'freelance') "
            "OR employment_type IS NULL",
            name="chk_experiences_employment_type",
        ),
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="chk_experiences_dates",
        ),
        CheckConstraint(
            "NOT (is_current = true AND end_date IS NOT NULL)",
            name="chk_experiences_current",
        ),
    )