from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certification import Certification


class CertificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_public_certifications(self) -> list[Certification]:
        statement = (
            select(Certification)
            .order_by(Certification.display_order)
        )

        return list(self.db.scalars(statement).all())