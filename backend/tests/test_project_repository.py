from app.database.session import SessionLocal
from app.repositories.project import ProjectRepository
from uuid import uuid4

from sqlalchemy import select

from app.models.skill import Skill
def test_get_existing_project():
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        project = repository.get_by_id(1)

        assert project is not None
        assert project.id == 1
        assert project.title == "Adaptive Learning Recommendation Engine"

    finally:
        db.close()


def test_get_non_existing_project():
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        project = repository.get_by_id(999999)

        assert project is None

    finally:
        db.close()

def test_get_published_projects():
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        projects = repository.get_published_projects()

        assert len(projects) == 5
        assert [project.id for project in projects] == [1, 2, 3, 4, 9]
        assert all(project.is_published for project in projects)

    finally:
        db.close()


def test_create_project_with_relationships():
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        # Resolve the portfolio owner.
        owner = repository.get_portfolio_owner()

        assert owner is not None

        # Retrieve two existing skills.
        skills = list(
            db.scalars(
                select(Skill)
                .order_by(Skill.id)
                .limit(2)
            ).all()
        )

        assert len(skills) == 2

        skill_ids = {skill.id for skill in skills}

        # Generate a unique slug to avoid database conflicts.
        unique_slug = f"repository-test-{uuid4().hex[:12]}"

        # Create a project and its relationships.
        project = repository.create(
            project_data={
                "title": "Repository Integration Test",
                "slug": unique_slug,
                "short_description": "Testing project persistence",
                "detailed_description": "Testing SQLAlchemy relationships",
                "github_url": "https://github.com/example/test",
                "live_url": None,
                "is_featured": False,
                "is_published": False,
                "display_order": 99,
            },
            owner_id=owner.id,
            skills=skills,
            categories=["ai", "backend"],
        )

        project_id = project.id

        # Reload the project with its relationships.
        saved_project = repository.get_by_id(project_id)

        assert saved_project is not None
        assert saved_project.title == "Repository Integration Test"
        assert saved_project.owner_id == owner.id

        assert {skill.id for skill in saved_project.skills} == skill_ids
        assert set(saved_project.categories) == {"ai", "backend"}

        # Roll back so the test does not permanently modify the database.
        db.rollback()

        assert repository.get_by_id(project_id) is None

    finally:
        db.rollback()
        db.close()
