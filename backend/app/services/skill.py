from app.repositories.skill import SkillRepository


class SkillService:
    def __init__(self, repository: SkillRepository):
        self.repository = repository

    def get_public_skills(self):
        return self.repository.get_all_categories_with_skills()