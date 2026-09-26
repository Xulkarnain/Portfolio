from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    slug: str = Field(min_length=1, max_length=180)
    short_description: str = Field(min_length=1, max_length=300)
    detailed_description: str | None = None
    github_url: HttpUrl | None = None
    live_url: HttpUrl | None = None
    is_featured: bool = False
    is_published: bool = False
    display_order: int = 0


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)