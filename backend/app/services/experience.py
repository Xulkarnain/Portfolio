from app.repositories.experience import ExperienceRepository


class ExperienceService:
    def __init__(self, repository: ExperienceRepository):
        self.repository = repository

    def get_public_experiences(self):
        return self.repository.get_all_public_experiences()