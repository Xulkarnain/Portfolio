from datetime import date

from pydantic import BaseModel, ConfigDict


class ExperienceSkillPublicResponse(BaseModel):
    name: str
    proficiency_level: str

    model_config = ConfigDict(from_attributes=True)


class ExperiencePublicResponse(BaseModel):
    company: str
    role_title: str
    employment_type: str | None
    location: str | None
    description: str | None
    start_date: date
    end_date: date | None
    is_current: bool
    external_url: str | None
    display_order: int
    skills: list[ExperienceSkillPublicResponse]

    model_config = ConfigDict(from_attributes=True)