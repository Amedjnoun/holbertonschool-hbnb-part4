#!/usr/bin/python3
"""
BaseModel class that defines all common attributes/methods for other classes
"""

from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """
        Update the updated_at timestamp and persist changes to the database.
        """
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
