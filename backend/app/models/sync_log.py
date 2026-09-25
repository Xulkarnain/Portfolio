from datetime import datetime

from sqlalchemy import Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, Integer, String, Text, func
from app.database.base import Base


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    records_processed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )

    records_created: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )

    records_updated: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )

    records_failed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
    )

    error_details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "source IN ('devto', 'github', 'medium', 'linkedin')",
            name="chk_sync_logs_source",
        ),
        CheckConstraint(
            "status IN ('running', 'success', 'partial_failure', 'failed')",
            name="chk_sync_logs_status",
        ),
        CheckConstraint(
            """
            records_processed >= 0
            AND records_created >= 0
            AND records_updated >= 0
            AND records_failed >= 0
            """,
            name="chk_sync_logs_counts",
        ),
    )