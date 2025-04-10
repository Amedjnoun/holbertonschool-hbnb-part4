from app import create_app
from app.services.facade import HBnBFacade

app = create_app()
facade = HBnBFacade()


def create_admin_user():
    admin_data = {
        "first_name": "Admins",
        "last_name": "HairBedsnBeers",
        "email": "admin@example.com",
        "password": "admin123",
        "is_admin": True
    }
    existing_user = facade.user_repo.get_user_by_email(admin_data["email"])
    if existing_user:
        print(
            "Admin user already exists. "
            "Check the README for default credentials."
        )
    else:
        facade.create_user(admin_data)
        print(
            "Admin user has been created. "
            "Check the README for default credentials."
        )


if __name__ == "__main__":
    with app.app_context():  # Ensure application context is active
        create_admin_user()
    app.run(debug=True)
