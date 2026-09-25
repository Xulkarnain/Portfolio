from sqlalchemy import inspect

from app.database.connection import engine


inspector = inspect(engine)

timestamp_columns = {
    "users": ["created_at", "updated_at"],
    "projects": ["created_at", "updated_at"],
    "skill_categories": ["created_at", "updated_at"],
    "skills": ["created_at", "updated_at"],
    "experiences": ["created_at", "updated_at"],
    "education": ["created_at", "updated_at"],
    "certifications": ["created_at", "updated_at"],
    "posts": ["published_at", "created_at", "updated_at"],
    "resumes": ["uploaded_at", "created_at", "updated_at"],
    "contact_messages": ["created_at"],
    "visitor_logs": ["created_at"],
    "sync_logs": ["started_at", "completed_at"],
}


for table_name, columns in timestamp_columns.items():
    print(f"\n[{table_name}]")

    db_columns = {
        column["name"]: column
        for column in inspector.get_columns(table_name)
    }

    for column_name in columns:
        column = db_columns[column_name]
        column_type = column["type"]

        print(
            f"{column_name}: "
            f"type={column_type!r}, "
            f"python_type={getattr(column_type, 'python_type', None)}, "
            f"timezone={getattr(column_type, 'timezone', None)}"
        )