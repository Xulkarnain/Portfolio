
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BlogPostListResponse(BaseModel):
    source: str
    title: str
    slug: str
    excerpt: str | None
    cover_image_url: str | None
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BlogPostDetailResponse(BlogPostListResponse):
    content: str | None
    external_url: str | None