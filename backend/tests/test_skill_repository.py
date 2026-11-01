from app.database.session import SessionLocal
from app.repositories.skill import SkillRepository


def test_get_all_categories_with_skills():
    db = SessionLocal()

    try:
        repository = SkillRepository(db)

        categories = repository.get_all_categories_with_skills()

        # Verify category count
        assert len(categories) == 6

        # Verify category ordering
        category_names = [category.name for category in categories]

        assert category_names == [
            "Programming Languages",
            "Machine Learning",
            "Deep Learning",
            "Backend",
            "Databases",
            "DevOps",
        ]

        # Verify total skill count
        total_skills = sum(
            len(category.skills) for category in categories
        )

        assert total_skills == 15

        # Verify skill ordering within the first category
        programming_skills = [
            skill.name for skill in categories[0].skills
        ]

        assert programming_skills == [
            "Python",
            "C++",
            "Java",
        ]

    finally:
        db.close()