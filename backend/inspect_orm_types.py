from app.database.base import Base
from app.models import User, Project, Post, Resume, SyncLog


models = [
    User,
    Project,
    Post,
    Resume,
    SyncLog,
]


for model in models:
    print(f"\n[{model.__tablename__}]")

    for column in model.__table__.columns:
        if column.name in {
            "created_at",
            "updated_at",
            "published_at",
            "uploaded_at",
            "started_at",
            "completed_at",
        }:
            column_type = column.type

            print(
                f"{column.name}: "
                f"type={column_type!r}, "
                f"timezone={getattr(column_type, 'timezone', None)}"
            )