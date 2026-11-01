from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.skill_category import SkillCategory


class SkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories_with_skills(self) -> list[SkillCategory]:
        statement = (
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .order_by(SkillCategory.display_order)
        )

        return list(self.db.scalars(statement).all())