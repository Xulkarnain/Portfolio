from app.repositories.education import EducationRepository


class EducationService:
    def __init__(self, repository: EducationRepository):
        self.repository = repository

    def get_public_education(self):
        return self.repository.get_all_public_education()