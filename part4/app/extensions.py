"""Flask extensions and initialization functions"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key support for SQLite"""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def init_db_events():
    """Configure database events"""

    @event.listens_for(db.session, 'after_commit')
    def after_commit(session):
        """Actions to perform after a commit"""
        session.info.clear()

    @event.listens_for(db.session, 'after_rollback')
    def after_rollback(session):
        """Actions to perform after a rollback"""
        session.info.clear()

    @event.listens_for(db.session, 'after_soft_rollback')
    def after_soft_rollback(session, previous_transaction):
        """Actions to perform after a soft rollback"""
        session.info.clear()

@jwt.user_identity_loader
def user_identity_lookup(user_id):
    """Convert user identity for JWT"""
    return str(user_id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Load user from JWT"""
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

# JWT error messages configuration
jwt_messages = {
    'token_expired': 'The token has expired',
    'invalid_token': 'Invalid token',
    'unauthorized': 'Unauthorized access',
    'token_revoked': 'The token has been revoked',
    'fresh_token_required': 'A fresh token is required',
    'jwt_decode_error': 'Token decoding error',
    'invalid_header': 'Invalid token header',
    'revoked_token': 'The token has been revoked',
    'user_lookup_error': 'Error during user lookup',
    'fresh_token_required': 'A fresh token is required',
    'invalid_audience': 'Invalid audience',
    'invalid_issuer': 'Invalid issuer',
    'invalid_claim': 'Invalid claim',
    'missing_claim': 'Missing claim',
    'invalid_header_padding': 'Invalid header padding'
}

# Apply JWT error messages
for error_key, message in jwt_messages.items():
    if hasattr(jwt, error_key + '_loader'):
        getattr(jwt, error_key + '_loader')(lambda: ({"msg": message}, 401))
