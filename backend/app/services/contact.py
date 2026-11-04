import logging

from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactMessageCreate
from app.services.email import send_contact_notification

logger = logging.getLogger(__name__)


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def create_contact_message(self, message_data: ContactMessageCreate):
        # First, save the message in the database.
        contact_message = self.repository.create_message(message_data)

        # Then, attempt to send the email notification.
        try:
            email_sent = send_contact_notification(
                visitor_name=contact_message.visitor_name,
                visitor_email=contact_message.email,
                subject=contact_message.subject,
                message=contact_message.message,
            )

            if not email_sent:
                logger.warning(
                    "Contact message saved, but notification email was not sent."
                )

        except Exception:
            # Email failure must never undo a successful database save.
            logger.exception(
                "Contact message saved, but email notification failed."
            )

        return contact_message