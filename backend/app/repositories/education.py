from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education import Education


class EducationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_public_education(self) -> list[Education]:
        statement = (
            select(Education)
            .order_by(Education.display_order)
        )

        return list(self.db.scalars(statement).all())