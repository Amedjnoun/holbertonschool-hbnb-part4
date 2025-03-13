#!/usr/bin/python3
"""
Module for User
"""

from app.models.base_model import BaseModel


class User(BaseModel):

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
        Hashes the password before storing it
        Args: password
        """
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password
        Args: password
        """
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
