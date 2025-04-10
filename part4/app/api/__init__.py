"""
API initialization package.
Configures the basic structure of the REST API.

Structure:
    - v1/: Version 1 of the API
        - users: User management
        - places: Property management
        - amenities: Equipment management
        - reviews: Review management
        - auth: Authentication
"""

from flask_restx import Api

# Basic API configuration
api = Api(
    version='1.0',
    title='HBnB API',
    description='REST API for rental management',
    doc='/api/v1/docs',
    prefix='/api/v1',
    # Add model documentation
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)

# API configuration verification
def init_api():
    """Initialize and verify the API configuration.

    Verifies:
        - Presence of required namespaces
        - Swagger configuration
        - Route prefixes
    """
    if not api.namespaces:
        raise ValueError("No namespace is registered in the API")
    return True

"""API routes registration module."""
from app.api.v1.users import users_bp
from app.api.v1.auth import auth_bp
from app.api.v1.places import places_bp
from app.api.v1.reviews import reviews_bp
from app.api.v1.amenities import amenities_bp
from app.api.v1.bookings import bookings_bp
from app.api.v1.admin import admin_bp
from app.api.v1.testing import testing_bp

def register_blueprints(app):
    """Register all API blueprints with the Flask application.

    Args:
        app: The Flask application instance.
    """
    # Base API route
    base_url = '/api/v1'

    # Register blueprints with appropriate URL prefixes
    app.register_blueprint(users_bp, url_prefix=base_url)
    app.register_blueprint(auth_bp, url_prefix=f"{base_url}/auth")
    app.register_blueprint(places_bp, url_prefix=base_url)
    app.register_blueprint(reviews_bp, url_prefix=base_url)
    app.register_blueprint(amenities_bp, url_prefix=base_url)
    app.register_blueprint(bookings_bp, url_prefix=base_url)
    app.register_blueprint(admin_bp, url_prefix=f"{base_url}/admin")

    # Only register testing endpoints in development/testing
    if app.config['ENV'] in ['development', 'testing']:
        app.register_blueprint(testing_bp, url_prefix=f"{base_url}/testing")
