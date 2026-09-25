from app.database.base import Base
from app.models import SyncLog


print("Registered tables:")
print(Base.metadata.tables.keys())

print("\nSyncLog columns:")

for column in SyncLog.__table__.columns:
    print(
        column.name,
        "->",
        column.type,
        "| nullable:",
        column.nullable,
    )

print("\nSyncLog constraints:")

for constraint in SyncLog.__table__.constraints:
    print(constraint)