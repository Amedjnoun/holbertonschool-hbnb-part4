"""Booking model for the HBNB application"""
from app.extensions import db
from app.models.BaseModel import BaseModel
from datetime import datetime, timedelta

class Booking(BaseModel):
    """Model for property bookings/reservations."""

    __tablename__ = 'bookings'

    # Booking dates
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)

    # Number of guests
    num_guests = db.Column(db.Integer, nullable=False)

    # Booking status (pending, confirmed, cancelled, completed)
    status = db.Column(db.String(20), nullable=False, default='pending')

    # Special requests
    special_requests = db.Column(db.Text, nullable=True)

    # Relationships
    tenant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def validate(self):
        """Validate booking data."""
        # Date validation
        today = datetime.now().date()

        if not self.check_in_date:
            raise ValueError("Check-in date is required")

        if not self.check_out_date:
            raise ValueError("Check-out date is required")

        if self.check_in_date < today:
            raise ValueError("Check-in date cannot be in the past")

        if self.check_out_date <= self.check_in_date:
            raise ValueError("Check-out date must be after check-in date")

        # Number of guests validation
        if self.num_guests is None or self.num_guests <= 0:
            raise ValueError("Number of guests must be greater than 0")

        # Status validation
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

        # Check for availability (no overlapping confirmed bookings)
        if self.status == 'confirmed':
            from app.models.place import Place
            place = Place.query.get(self.place_id)

            if not place:
                raise ValueError("Invalid place ID")

            # Check availability excluding this booking
            conflicting_bookings = Booking.query.filter(
                Booking.place_id == self.place_id,
                Booking.status == 'confirmed',
                Booking.id != self.id,
                Booking.check_in_date <= self.check_out_date,
                Booking.check_out_date >= self.check_in_date
            ).all()

            if conflicting_bookings:
                raise ValueError("The property is not available for these dates")

    def to_dict(self):
        """Convert the booking to a dictionary."""
        from app.models.user import User
        from app.models.place import Place

        # Get tenant information
        tenant = User.query.get(self.tenant_id) if self.tenant_id else None
        tenant_info = {
            'id': tenant.id,
            'first_name': tenant.first_name,
            'last_name': tenant.last_name
        } if tenant else None

        # Get place information
        place = Place.query.get(self.place_id) if self.place_id else None
        place_info = {
            'id': place.id,
            'name': place.name,
            'address': place.address,
            'city': place.city,
            'country': place.country
        } if place else None

        # Calculate booking length and total price
        nights = (self.check_out_date - self.check_in_date).days
        total_price = nights * place.price_per_night if place else 0

        return {
            'id': self.id,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'num_guests': self.num_guests,
            'status': self.status,
            'special_requests': self.special_requests,
            'tenant': tenant_info,
            'place': place_info,
            'nights': nights,
            'total_price': total_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_booking(data):
        """Create a new booking."""
        # Convert string dates to date objects if needed
        check_in = data['check_in_date']
        check_out = data['check_out_date']

        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, '%Y-%m-%d').date()

        booking = Booking(
            check_in_date=check_in,
            check_out_date=check_out,
            num_guests=data['num_guests'],
            special_requests=data.get('special_requests'),
            tenant_id=data['tenant_id'],
            place_id=data['place_id'],
            status='pending'  # All bookings start as pending
        )

        # Validate and save
        booking.validate()
        booking.save()
        return booking

    def update_status(self, new_status):
        """Update the booking status."""
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

        self.status = new_status
        self.validate()
        self.save()

    def can_be_cancelled(self):
        """Check if the booking can be cancelled."""
        # Only confirmed or pending bookings can be cancelled
        if self.status not in ['confirmed', 'pending']:
            return False

        # Cannot cancel a booking on the same day or after check-in
        today = datetime.now().date()
        return self.check_in_date > today

    def __repr__(self):
        """String representation of the booking."""
        return f'<Booking {self.id} - Status: {self.status}>'
