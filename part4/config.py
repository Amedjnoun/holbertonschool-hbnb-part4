"""Flask application configuration for HBNB"""
import os
from datetime import timedelta

class Config:
    """Base configuration with common settings"""

    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # Secret key for sessions
    STATIC_FOLDER = 'static'  # Static files folder

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True  # Check connection before use
    }

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # Key for tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token validity duration
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token duration
    JWT_ERROR_MESSAGE_KEY = 'error'  # Error message key

    # Security configuration
    SESSION_COOKIE_SECURE = True  # Secure cookie (HTTPS)
    SESSION_COOKIE_HTTPONLY = True  # Cookie accessible only via HTTP
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Session duration

    # CORS configuration
    CORS_HEADERS = 'Content-Type'  # Allowed headers for CORS

class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True  # Enable debug mode
    TESTING = False
    ENV = 'development'

    # SQLite database for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb.db'

    # Disable certain security measures in development
    SESSION_COOKIE_SECURE = False

    # Longer JWT in development
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class TestingConfig(Config):
    """Testing configuration"""

    DEBUG = False
    TESTING = True
    ENV = 'testing'

    # In-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF for tests
    WTF_CSRF_ENABLED = False

    # Short JWT for tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3)

class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    TESTING = False
    ENV = 'production'

    # Database URL from environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb.db')

    # Enhanced security in production
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    # More restrictive JWT in production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    def __init__(self):
        """Validate production configuration"""
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key':
            raise ValueError("Production secret key must be set")

        if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == 'jwt-secret-key':
            raise ValueError("Production JWT key must be set")

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
