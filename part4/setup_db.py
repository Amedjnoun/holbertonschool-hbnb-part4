#!/usr/bin/env python3
"""Database initialization script"""
import os
from app import create_app
from app.extensions import db, init_db_events
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place_photo import PlacePhoto

def init_db(app):
    """Initialize the database and create tables if needed"""
    print("🔄 Checking database...")

    # Create instance folder if needed
    if not os.path.exists(app.instance_path):
        print(f"📁 Creating folder {app.instance_path}")
        os.makedirs(app.instance_path)

    db_path = os.path.join(app.root_path, 'hbnb.db')
    if not os.path.exists(db_path):
        print("📁 Creating new database...")

        # Enable foreign key support for SQLite
        init_db_events()

        # Create tables
        with app.app_context():
            db.create_all()
            print("✅ Tables created successfully.")

        # Create default amenities
        with app.app_context():
            default_amenities = [
                "WiFi", "Air conditioning", "Heating", "Kitchen",
                "TV", "Free parking", "Washing machine", "Swimming pool",
                "Hot tub", "Gym"
            ]

            for name in default_amenities:
                if not Amenity.query.filter_by(name=name).first():
                    amenity = Amenity(name=name)
                    db.session.add(amenity)

            try:
                db.session.commit()
                print("✅ Default amenities created.")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating amenities: {str(e)}")
                return False

        print("✅ Initial database setup completed.")
        return True
    else:
        print("✅ Database already exists.")
        return True

def reset_db(app):
    """Reset the database (for development only)"""
    print("🔄 Resetting database...")

    db_path = os.path.join(app.root_path, 'hbnb.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("✅ Old database removed.")
        except Exception as e:
            print(f"❌ Error removing database: {str(e)}")
            return False

    return init_db(app)

if __name__ == "__main__":
    import sys
    app = create_app()

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        if reset_db(app):
            print("✅ Database reset successfully.")
        else:
            print("❌ Database reset failed.")
            sys.exit(1)
    else:
        if init_db(app):
            print("✅ Database initialization completed.")
        else:
            print("❌ Database initialization failed.")
            sys.exit(1)
