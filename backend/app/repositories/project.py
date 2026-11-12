from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project
from app.models.user import User
from app.models.skill import Skill
from app.models.project_category import ProjectCategory
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

    def get_portfolio_owner(self) -> User | None:
        statement = select(User).order_by(User.id)
        users = list(self.db.scalars(statement).all())

        if len(users) != 1:
            return None

        return users[0]


    def get_skills_by_ids(self, skill_ids: list[int]) -> list[Skill]:
        if not skill_ids:
            return []

        statement = select(Skill).where(Skill.id.in_(skill_ids))

        return list(self.db.scalars(statement).all())

    def create(
        self,
        project_data: dict,
        owner_id: int,
        skills: list[Skill],
        categories: list[str],
    ) -> Project:
        project = Project(
            **project_data,
            owner_id=owner_id,
            skills=skills,
            category_assignments=[
                ProjectCategory(category=category)
                for category in categories
            ],
        )

        self.db.add(project)
        self.db.flush()

        return project

    def get_by_slug(self, slug: str) -> Project | None:
        statement = select(Project).where(Project.slug == slug)
        return self.db.scalar(statement)