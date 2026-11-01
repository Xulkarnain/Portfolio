from pydantic import BaseModel, ConfigDict


class SkillPublicResponse(BaseModel):
    name: str
    proficiency_level: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class SkillCategoryPublicResponse(BaseModel):
    name: str
    display_order: int
    skills: list[SkillPublicResponse]

    model_config = ConfigDict(from_attributes=True)