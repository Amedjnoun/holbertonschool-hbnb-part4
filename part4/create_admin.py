#!/usr/bin/env python3
"""Administrator user creation script"""
from app import create_app
from app.extensions import db
from app.models.user import User

def create_admin():
    """Creates an administrator user if it doesn't exist"""
    print("🔄 Creating administrator user...")

    try:
        app = create_app()
        with app.app_context():
            # Check if admin already exists
            existing_admin = User.query.filter_by(email='admin@hbnb.io').first()

            if existing_admin:
                print("ℹ️ Administrator already exists")
                return True

            # Create administrator
            admin = User(
                first_name='Admin',
                last_name='HBNB',
                email='admin@hbnb.io',
                is_admin=True
            )
            # Set password
            admin.hash_password('admin12345')

            # Save to database
            db.session.add(admin)
            db.session.commit()

            print("✅ Administrator created successfully!")
            print("\nLogin credentials:")
            print("📧 Email: admin@hbnb.io")
            print("🔑 Password: admin12345")
            return True

    except Exception as e:
        print(f"❌ Error creating administrator: {str(e)}")
        if 'db' in locals():
            db.session.rollback()
        return False

if __name__ == "__main__":
    if create_admin():
        print("✅ Administrator creation completed.")
    else:
        import sys
        print("❌ Administrator creation failed.")
        sys.exit(1)
