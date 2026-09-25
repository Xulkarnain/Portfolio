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
)
from sqlalchemy.orm import Mapped, mapped_column , relationship

from app.database.base import Base


class Certification(Base):
    __tablename__ = "certifications"

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
        back_populates="certifications",
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    issuing_organization: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    credential_id: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    credential_url: Mapped[str | None] = mapped_column(
        String(500),
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
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "expiry_date IS NULL OR expiry_date >= issue_date",
            name="chk_certifications_dates",
        ),
    )