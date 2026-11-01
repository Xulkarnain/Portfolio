from app.database.session import SessionLocal
from app.repositories.education import EducationRepository


def test_get_all_public_education():
    db = SessionLocal()

    try:
        repository = EducationRepository(db)

        records = repository.get_all_public_education()

        # Verify record count
        assert len(records) == 1

        education = records[0]

        # Verify education details
        assert education.institution == "Central University of Kashmir"
        assert education.degree == "B.Tech CSE"
        assert education.field_of_study == "Computer Science and Engineering"

        # Verify dates
        assert str(education.start_date) == "2023-06-01"
        assert str(education.end_date) == "2027-06-01"

        # Verify nullable fields
        assert education.grade is None
        assert education.description is None

        # Verify display order
        assert education.display_order == 1

    finally:
        db.close()