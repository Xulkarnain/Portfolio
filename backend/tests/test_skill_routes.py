from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_skill_service
from app.core.exceptions import ResourceNotFoundException


class FakeSkill:
    def __init__(self, name, proficiency_level, display_order):
        self.name = name
        self.proficiency_level = proficiency_level
        self.display_order = display_order


class FakeSkillCategory:
    def __init__(self, name, display_order, skills):
        self.name = name
        self.display_order = display_order
        self.skills = skills


class FakeSkillService:
    def get_public_skills(self):
        return [
            FakeSkillCategory(
                name="Programming Languages",
                display_order=1,
                skills=[
                    FakeSkill("Python", "expert", 1),
                    FakeSkill("C++", "intermediate", 2),
                ],
            ),
            FakeSkillCategory(
                name="Machine Learning",
                display_order=2,
                skills=[
                    FakeSkill("Scikit-Learn", "advanced", 1),
                ],
            ),
        ]


def test_get_skills():
    app.dependency_overrides[get_skill_service] = FakeSkillService

    try:
        client = TestClient(app)
        response = client.get("/api/v1/skills")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2

        assert data[0]["name"] == "Programming Languages"
        assert data[0]["display_order"] == 1

        assert data[0]["skills"][0]["name"] == "Python"
        assert data[0]["skills"][0]["proficiency_level"] == "expert"

        assert data[1]["name"] == "Machine Learning"

        # Internal database fields should not be exposed
        assert "id" not in data[0]
        assert "created_at" not in data[0]

    finally:
        app.dependency_overrides.clear()