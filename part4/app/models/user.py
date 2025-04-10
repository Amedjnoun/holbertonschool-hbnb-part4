"""User management module."""
from app.extensions import db, bcrypt
from app.models.BaseModel import BaseModel
import re

class User(BaseModel):
    """Model for users."""

    # Column definitions
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def validate(self):
        """Validate user data."""
        # Email validation
        if not self.email:
            raise ValueError("Email is required")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

        # First name and last name validation
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be less than 50 characters")

        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be less than 50 characters")

    def hash_password(self, password):
        """Hash the user's password."""
        if not password:
            raise ValueError("Password is required")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify the user's password."""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def promote_to_admin(self):
        """Promote the user to admin."""
        self.is_admin = True
        self.save()

    def demote_from_admin(self):
        """Demote the admin to a regular user."""
        self.is_admin = False
        self.save()

    def to_dict(self):
        """Convert the user to a dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_user(data):
        """Create a new user."""
        if not data.get('password'):
            raise ValueError("Password is required")

        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data.get('is_admin', False)
        )
        user.hash_password(data['password'])
        user.validate()
        user.save()
        return user

    def update_from_dict(self, data):
        """Update the user from a dictionary."""
        if 'email' in data:
            self.email = data['email']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'password' in data:
            self.hash_password(data['password'])
        if 'is_admin' in data:
            self.is_admin = data['is_admin']

        self.validate()
        self.save()

    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.email}>'
