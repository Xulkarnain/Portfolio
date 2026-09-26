from datetime import datetime, timezone

from app.schemas.project import ProjectCreate, ProjectResponse


def test_project_create_schema():
    project = ProjectCreate(
        owner_id=1,
        title="Customer Churn Prediction",
        slug="customer-churn-prediction",
        short_description="Predict customer churn using machine learning.",
        github_url="https://github.com/example/project",
        is_featured=True,
        is_published=True,
    )

    assert project.owner_id == 1
    assert project.title == "Customer Churn Prediction"
    assert project.is_featured is True
    assert project.is_published is True


def test_project_response_schema():
    project = ProjectResponse(
        id=1,
        owner_id=1,
        title="Customer Churn Prediction",
        slug="customer-churn-prediction",
        short_description="Predict customer churn using machine learning.",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    assert project.id == 1
    assert project.owner_id == 1