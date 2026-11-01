from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.experience import Experience


class ExperienceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_public_experiences(self) -> list[Experience]:
        statement = (
            select(Experience)
            .options(selectinload(Experience.skills))
            .order_by(Experience.display_order)
        )

        return list(self.db.scalars(statement).all())