
from app.database.session import SessionLocal
from app.repositories.admin import AdminRepository
from app.services.auth import AuthService


db = SessionLocal()

try:
    repository = AdminRepository(db)
    auth_service = AuthService(repository)

    email = "darzulkarnain@gmail.com"

    password = input("Enter admin password: ")

    result = auth_service.authenticate_admin(email, password)

    if result:
        token, admin_id = result

        print("Authentication successful!")
        print("Admin ID:", admin_id)
        print("JWT generated:", bool(token))
    else:
        print("Authentication failed!")

    wrong_result = auth_service.authenticate_admin(
        email,
        "DefinitelyWrongPassword123!"
    )

    print("Incorrect password rejected:", wrong_result is None)

finally:
    db.close()
