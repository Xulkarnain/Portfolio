from fastapi import APIRouter, Depends

from app.api.dependencies import get_experience_service
from app.schemas.experience import ExperiencePublicResponse
from app.services.experience import ExperienceService


router = APIRouter(prefix="/experiences", tags=["Experience"])


@router.get("", response_model=list[ExperiencePublicResponse])
def get_experiences(
    service: ExperienceService = Depends(get_experience_service),
):
    return service.get_public_experiences()