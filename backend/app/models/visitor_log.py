from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    ip_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    device_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    browser: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    referrer: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    requested_path: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )