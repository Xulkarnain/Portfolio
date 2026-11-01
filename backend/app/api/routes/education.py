from fastapi import APIRouter, Depends

from app.api.dependencies import get_education_service
from app.schemas.education import EducationPublicResponse
from app.services.education import EducationService


router = APIRouter(prefix="/education", tags=["Education"])


@router.get("", response_model=list[EducationPublicResponse])
def get_education(
    service: EducationService = Depends(get_education_service),
):
    return service.get_public_education()