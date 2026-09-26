from app.database.session import SessionLocal
from app.repositories.project import ProjectRepository


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

        assert len(projects) == 4

        assert [project.id for project in projects] == [1, 2, 3, 4]
        assert all(project.is_published for project in projects)

    finally:
        db.close()