from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Project | None:
        statement = (
            select(Project)
            .options(
                selectinload(Project.skills),
                selectinload(Project.category_assignments),
            )
            .where(Project.id == project_id)
        )

        return self.db.scalar(statement)

    def get_published_projects(self) -> list[Project]:
        statement = (
            select(Project)
            .options(
                selectinload(Project.skills),
                selectinload(Project.category_assignments),
            )
            .where(Project.is_published.is_(True))
            .order_by(Project.display_order)
        )

        return list(self.db.scalars(statement).all())