#!/usr/bin/python3
"""
Module for Review
"""

from app.extensions import db
from .base_model import BaseModel
from sqlalchemy import ForeignKey


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)  # Foreign key to User
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)  # Foreign key to Place
