from sqlalchemy.orm import Session

from app.models.contact_message import ContactMessage
from app.schemas.contact import ContactMessageCreate


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(
        self,
        message_data: ContactMessageCreate,
    ) -> ContactMessage:
        contact_message = ContactMessage(
            visitor_name=message_data.visitor_name,
            email=str(message_data.email),
            subject=message_data.subject,
            message=message_data.message,
        )

        try:
            self.db.add(contact_message)
            self.db.commit()
            self.db.refresh(contact_message)

            return contact_message

        except Exception:
            self.db.rollback()
            raise