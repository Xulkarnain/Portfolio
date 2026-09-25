from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column ,relationship

from app.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

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
        back_populates="resumes",
    )

    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
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
        UniqueConstraint(
            "owner_id",
            "version",
            name="uq_resumes_owner_version",
        ),
        Index(
            "uq_resumes_one_current_per_owner",
            "owner_id",
            unique=True,
            postgresql_where=(
                "is_current = true"
            ),
        ),
    )