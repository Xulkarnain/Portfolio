from fastapi import APIRouter, Depends

from app.api.dependencies import get_post_service
from app.schemas.post import (
    BlogPostListResponse,
    BlogPostDetailResponse,
)
from app.services.post import PostService


router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("", response_model=list[BlogPostListResponse])
def get_blog_posts(
    service: PostService = Depends(get_post_service),
):
    return service.get_public_posts()


@router.get("/{slug}", response_model=BlogPostDetailResponse)
def get_blog_post(
    slug: str,
    service: PostService = Depends(get_post_service),
):
    return service.get_public_post(slug)