from app.extensions import db
from app.models.BaseModel import BaseModel
import re

# Place-Amenity association table with explicit foreign keys
place_amenity = db.Table('place_amenities',
    db.Column('place_id', db.String(36),
              db.ForeignKey('places.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('amenity_id', db.String(36),
              db.ForeignKey('amenities.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('created_at', db.DateTime, server_default=db.func.now()),
    db.Column('updated_at', db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
)

class Place(BaseModel):
    """Model for property listings."""

    __tablename__ = 'places'

    # Basic information
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    price_per_night = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    # Property features
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)

    # Relationships
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships with cascading delete
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
    photos = db.relationship('PlacePhoto', backref='place', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='place', cascade='all, delete-orphan')

    # Many-to-many relationship with amenities
    amenities = db.relationship('Amenity', secondary=place_amenity,
                               backref=db.backref('places', lazy='dynamic'))

    def validate(self):
        """Validate place data."""
        # Basic validations
        if not self.name or len(self.name) > 128:
            raise ValueError("Name is required and must be less than 128 characters")

        if not self.description:
            raise ValueError("Description is required")

        if not self.address:
            raise ValueError("Address is required")

        if not self.city or len(self.city) > 64:
            raise ValueError("City is required and must be less than 64 characters")

        if not self.country or len(self.country) > 64:
            raise ValueError("Country is required and must be less than 64 characters")

        # Numerical validations
        if self.price_per_night is None or self.price_per_night <= 0:
            raise ValueError("Price per night must be greater than 0")

        if self.max_guests is None or self.max_guests <= 0:
            raise ValueError("Maximum guests must be greater than 0")

        if self.number_of_rooms is None or self.number_of_rooms <= 0:
            raise ValueError("Number of rooms must be greater than 0")

        if self.number_of_bathrooms is None or self.number_of_bathrooms <= 0:
            raise ValueError("Number of bathrooms must be greater than 0")

        # Geographic coordinates validation (if provided)
        if self.latitude is not None and (self.latitude < -90 or self.latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")

        if self.longitude is not None and (self.longitude < -180 or self.longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")

    def to_dict(self, include_relationships=False):
        """Convert the place to a dictionary."""
        from app.models.user import User

        # Get owner information
        owner = User.query.get(self.owner_id) if self.owner_id else None
        owner_info = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name
        } if owner else None

        # Basic place information
        place_dict = {
            'id': self.id,
            'owner': owner_info,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        # Include relationship data if requested
        if include_relationships:
            # Add photos
            place_dict['photos'] = [photo.to_dict() for photo in self.photos]

            # Add amenities
            place_dict['amenities'] = [amenity.to_dict() for amenity in self.amenities]

            # Add reviews
            place_dict['reviews'] = [review.to_dict() for review in self.reviews]

            # Calculate average rating if reviews exist
            if self.reviews:
                total_rating = sum(review.rating for review in self.reviews)
                place_dict['avg_rating'] = round(total_rating / len(self.reviews), 1)
            else:
                place_dict['avg_rating'] = 0

            # Add booking information (upcoming confirmed bookings)
            from app.models.booking import Booking
            import datetime

            upcoming_bookings = Booking.query.filter(
                Booking.place_id == self.id,
                Booking.status == 'confirmed',
                Booking.check_out_date >= datetime.datetime.now().date()
            ).all()

            place_dict['booked_dates'] = []
            for booking in upcoming_bookings:
                # Add all dates between check-in and check-out
                current_date = booking.check_in_date
                while current_date <= booking.check_out_date:
                    place_dict['booked_dates'].append(current_date.isoformat())
                    current_date += datetime.timedelta(days=1)

        return place_dict

    @staticmethod
    def create_place(data, amenity_ids=None):
        """Create a new place."""
        place = Place(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            country=data['country'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            number_of_rooms=data['number_of_rooms'],
            number_of_bathrooms=data['number_of_bathrooms'],
            owner_id=data['owner_id']
        )

        # Validate and save
        place.validate()
        place.save()

        # Add amenities if provided
        if amenity_ids:
            from app.models.amenity import Amenity
            for amenity_id in amenity_ids:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
            db.session.commit()

        return place

    def update_from_dict(self, data, amenity_ids=None):
        """Update the place from a dictionary."""
        # Update basic fields
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']
        if 'address' in data:
            self.address = data['address']
        if 'city' in data:
            self.city = data['city']
        if 'country' in data:
            self.country = data['country']
        if 'latitude' in data:
            self.latitude = data['latitude']
        if 'longitude' in data:
            self.longitude = data['longitude']
        if 'price_per_night' in data:
            self.price_per_night = data['price_per_night']
        if 'max_guests' in data:
            self.max_guests = data['max_guests']
        if 'number_of_rooms' in data:
            self.number_of_rooms = data['number_of_rooms']
        if 'number_of_bathrooms' in data:
            self.number_of_bathrooms = data['number_of_bathrooms']

        # Update amenities if provided
        if amenity_ids is not None:
            from app.models.amenity import Amenity

            # Clear existing amenities
            self.amenities = []

            # Add new amenities
            for amenity_id in amenity_ids:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    self.amenities.append(amenity)

        # Validate and save
        self.validate()
        self.save()

    def get_availability(self, start_date, end_date):
        """Check if the place is available for the given dates."""
        from app.models.booking import Booking
        import datetime

        # Convert string dates to datetime objects if needed
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Check for conflicting bookings
        conflicting_bookings = Booking.query.filter(
            Booking.place_id == self.id,
            Booking.status == 'confirmed',
            Booking.check_in_date <= end_date,
            Booking.check_out_date >= start_date
        ).all()

        return len(conflicting_bookings) == 0

    def __repr__(self):
        """String representation of the place."""
        return f'<Place {self.name}>'

