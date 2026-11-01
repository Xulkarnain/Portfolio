from fastapi import APIRouter, Depends

from app.api.dependencies import get_certification_service
from app.schemas.certification import CertificationPublicResponse
from app.services.certification import CertificationService


router = APIRouter(prefix="/certifications", tags=["Certifications"])


@router.get("", response_model=list[CertificationPublicResponse])
def get_certifications(
    service: CertificationService = Depends(get_certification_service),
):
    return service.get_public_certifications()