from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactMessageCreate


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def create_contact_message(
        self,
        message_data: ContactMessageCreate,
    ):
        return self.repository.create_message(message_data)