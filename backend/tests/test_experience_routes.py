from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_experience_service


class FakeSkill:
    def __init__(self, name, proficiency_level):
        self.name = name
        self.proficiency_level = proficiency_level


class FakeExperience:
    def __init__(self):
        self.company = "Koshur Scientist"
        self.role_title = "AI/Backend Intern"
        self.employment_type = "internship"
        self.location = "Hybrid"
        self.description = "Worked on the KS Adaptive Learning AI platform."
        self.start_date = "2026-06-01"
        self.end_date = "2026-09-01"
        self.is_current = False
        self.external_url = None
        self.display_order = 1

        self.skills = [
            FakeSkill("Docker", "intermediate"),
            FakeSkill("FastAPI", "advanced"),
        ]


class FakeExperienceService:
    def get_public_experiences(self):
        return [FakeExperience()]


def test_get_experiences():
    app.dependency_overrides[get_experience_service] = FakeExperienceService

    try:
        client = TestClient(app)
        response = client.get("/api/v1/experiences")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1

        experience = data[0]

        assert experience["company"] == "Koshur Scientist"
        assert experience["role_title"] == "AI/Backend Intern"
        assert experience["employment_type"] == "internship"
        assert experience["location"] == "Hybrid"

        assert experience["start_date"] == "2026-06-01"
        assert experience["end_date"] == "2026-09-01"
        assert experience["is_current"] is False

        assert len(experience["skills"]) == 2

        assert experience["skills"][0]["name"] == "Docker"
        assert experience["skills"][1]["name"] == "FastAPI"

        # Internal database fields must not be exposed
        assert "id" not in experience
        assert "owner_id" not in experience
        assert "created_at" not in experience

    finally:
        app.dependency_overrides.clear()