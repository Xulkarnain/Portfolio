from app.database.session import SessionLocal
from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactMessageCreate
from app.models.contact_message import ContactMessage


def test_create_contact_message():
    db = SessionLocal()
    created_message = None

    try:
        repository = ContactRepository(db)

        message_data = ContactMessageCreate(
            visitor_name="Test User",
            email="testuser@example.com",
            subject="Repository Test",
            message="Testing contact message database insertion.",
        )

        created_message = repository.create_message(message_data)

        # Verify inserted data
        assert created_message.id is not None
        assert created_message.visitor_name == "Test User"
        assert created_message.email == "testuser@example.com"
        assert created_message.subject == "Repository Test"

        # Verify database-generated values
        assert created_message.created_at is not None

        # Verify new messages are unread
        assert created_message.is_read is False

    finally:
        if created_message is not None:
            db.delete(created_message)
            db.commit()

        db.close()