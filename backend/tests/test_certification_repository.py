from app.database.session import SessionLocal
from app.repositories.certification import CertificationRepository


def test_get_all_public_certifications():
    db = SessionLocal()

    try:
        repository = CertificationRepository(db)

        certifications = repository.get_all_public_certifications()

        # Verify record count
        assert len(certifications) == 1

        certification = certifications[0]

        # Verify certification details
        assert certification.title == "Ultimate Data Science & AI Bootcamp"
        assert certification.issuing_organization == "Krish Naik Academy"

        # Verify dates
        assert str(certification.issue_date) == "2026-09-01"
        assert certification.expiry_date is None

        # Verify optional fields
        assert certification.credential_id is None
        assert certification.credential_url is None

        # Verify description
        assert certification.description == (
            "Data Science and AI training covering Python, statistics, "
            "machine learning, deep learning, NLP and related technologies."
        )

        # Verify display order
        assert certification.display_order == 1

    finally:
        db.close()