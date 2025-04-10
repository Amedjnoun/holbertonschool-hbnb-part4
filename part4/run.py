#!/usr/bin/env python3
"""Main entry point for the HBNB application"""
import os
import sys
from app import create_app
from setup_db import init_db
from create_admin import create_admin

def main():
    """Initialize and start the application"""
    try:
        # Create Flask instance
        app = create_app()

        # Initialize database if needed
        if not init_db(app):
            print("❌ Database initialization failed")
            sys.exit(1)

        # Create admin user if needed
        if not create_admin():
            print("❌ Admin creation failed")
            sys.exit(1)

        # Server configuration
        host = os.getenv('FLASK_HOST', '0.0.0.0')  # Listen interface
        port = int(os.getenv('FLASK_PORT', 5001))  # Listen port
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'  # Debug mode

        # Start server
        print(f"🚀 Server running at http://localhost:{port}/")
        app.run(host=host, port=port, debug=debug)

    except Exception as e:
        print(f"❌ Application startup error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
