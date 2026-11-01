from app.core.exceptions import ResourceNotFoundException
from app.repositories.post import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def get_public_posts(self):
        return self.repository.get_all_published_posts()

    def get_public_post(self, slug: str):
        post = self.repository.get_published_post_by_slug(slug)

        if post is None:
            raise ResourceNotFoundException("Post", slug)

        return post