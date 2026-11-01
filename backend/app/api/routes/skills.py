from fastapi import APIRouter, Depends

from app.api.dependencies import get_skill_service
from app.schemas.skill import SkillCategoryPublicResponse
from app.services.skill import SkillService


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("", response_model=list[SkillCategoryPublicResponse])
def get_skills(
    service: SkillService = Depends(get_skill_service),
):
    return service.get_public_skills()