from app.database.session import SessionLocal
from app.models.skill_category import SkillCategory

db = SessionLocal()

try:
    categories = (
        db.query(SkillCategory)
        .order_by(SkillCategory.display_order)
        .all()
    )

    for category in categories:
        print(f"\n{category.name} | Order: {category.display_order}")

        skills = sorted(
            category.skills,
            key=lambda skill: skill.display_order
        )

        for skill in skills:
            print(
                f"  {skill.name} | "
                f"{skill.proficiency_level} | "
                f"Order: {skill.display_order}"
            )

finally:
    db.close()