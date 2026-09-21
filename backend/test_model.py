from app.database.base import Base
from app.models import Project, User


print("User table:", User.__tablename__)
print("Project table:", Project.__tablename__)

print("\nProject columns:")

for column in Project.__table__.columns:
    print(
        column.name,
        "->",
        column.type,
        "| nullable:",
        column.nullable,
    )

print("\nRegistered tables:")
print(Base.metadata.tables.keys())