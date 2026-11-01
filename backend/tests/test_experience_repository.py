from app.database.session import SessionLocal
from app.repositories.experience import ExperienceRepository


def test_get_all_public_experiences():
    db = SessionLocal()

    try:
        repository = ExperienceRepository(db)

        experiences = repository.get_all_public_experiences()

        # Verify experience count
        assert len(experiences) == 1

        experience = experiences[0]

        # Verify experience details
        assert experience.company == "Koshur Scientist"
        assert experience.role_title == "AI/Backend Intern"
        assert experience.employment_type == "internship"
        assert experience.location == "Hybrid"

        # Verify associated skills
        skill_names = [skill.name for skill in experience.skills]

        assert len(skill_names) == 7

        assert skill_names == [
            "Docker",
            "FastAPI",
            "Git",
            "PostgreSQL",
            "Pydantic",
            "Python",
            "SQLAlchemy",
        ]

    finally:
        db.close()