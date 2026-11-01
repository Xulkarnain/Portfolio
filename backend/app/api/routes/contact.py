from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_contact_service
from app.schemas.contact import (
    ContactMessageCreate,
    ContactMessageCreatedResponse,
)
from app.services.contact import ContactService


router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post(
    "",
    response_model=ContactMessageCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact_message(
    message_data: ContactMessageCreate,
    service: ContactService = Depends(get_contact_service),
):
    service.create_contact_message(message_data)

    return {
        "message": "Your message has been submitted successfully."
    }