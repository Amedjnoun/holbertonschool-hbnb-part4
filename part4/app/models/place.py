#!/usr/bin/python3
"""
Module for place
"""

from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey

# Association table for Place and Amenity
place_amenity = Table(
    'place_amenity',
    db.Model.metadata,
    Column('place_id', db.String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', db.String(36), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)  # Foreign key to User
    # Removed redundant user_id column
    reviews = relationship('Review', backref='place', lazy=True)  # One-to-Many with Review
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery',  # Many-to-Many with Amenity
                              backref=db.backref('associated_places', lazy=True, overlaps="associated_amenities"),
                              overlaps="associated_amenities,places")  # Refined overlaps
