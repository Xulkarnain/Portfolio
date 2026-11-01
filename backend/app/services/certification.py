from app.repositories.certification import CertificationRepository


class CertificationService:
    def __init__(self, repository: CertificationRepository):
        self.repository = repository

    def get_public_certifications(self):
        return self.repository.get_all_public_certifications()
    