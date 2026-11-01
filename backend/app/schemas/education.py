from datetime import date

from pydantic import BaseModel, ConfigDict


class EducationPublicResponse(BaseModel):
    institution: str
    degree: str
    field_of_study: str | None
    start_date: date
    end_date: date | None
    grade: str | None
    description: str | None
    display_order: int

    model_config = ConfigDict(from_attributes=True)