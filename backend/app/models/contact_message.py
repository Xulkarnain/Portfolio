from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    String,
    Text,
    Boolean,    
    func,
    desc,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    visitor_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        Index(
            "idx_contact_messages_read_created",
            "is_read",
            desc("created_at"),
        ),
    )