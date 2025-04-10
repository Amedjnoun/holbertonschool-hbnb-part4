#!/usr/bin/python3
"""
Module for User
"""

from app.extensions import db, bcrypt
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship('Place', backref='user', lazy=True, foreign_keys='Place.owner_id')  # Specify foreign key
    reviews = relationship('Review', backref='author', lazy=True)  # One-to-Many with Review

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Create the instance of user

        Args:
            first_name (string): first name of user
            last_name (string): last name of user
            email (string): email of user
            is_admin (bool, optional): if user is admin. Defaults to False.
        """
        super().__init__()  # Call parent to generate UUID & timestamps
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # list to store places user owns

        self.hash_password(password)  # Hash the password

    def hash_password(self, password):
        """
        Hash the password before storing it.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify the hashed password.
        """
        return bcrypt.check_password_hash(self.password, password)
