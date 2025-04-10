#!/usr/bin/python3
"""
Module for amenity
"""

from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)
    places = relationship('Place', secondary='place_amenity', lazy='subquery',  # Many-to-Many with Place
                           backref=db.backref('associated_amenities', lazy=True, overlaps="associated_places"),
                           overlaps="associated_places,amenities")  # Refined overlaps
