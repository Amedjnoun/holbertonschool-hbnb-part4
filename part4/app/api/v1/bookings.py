"""API for bookings in the HBNB application"""
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from datetime import datetime
from app.models.booking import Booking
from app.models.place import Place
from app.models.user import User
from app.extensions import jwt

# Creation of the bookings blueprint
bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/places/<string:place_id>/bookings', methods=['POST'])
@jwt_required()
def create_booking(place_id):
    """Creates a new booking for a place"""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Place not found'}), 404

        # Ensure the user does not book their own place
        if place.owner_id == current_user_id:
            return jsonify({'error': 'You cannot book your own place'}), 400

        data = request.get_json()

        # Date validation
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except (ValueError, KeyError):
            return jsonify({'error': 'Invalid dates'}), 400

        # Check if the dates are available
        existing_booking = Booking.query.filter(
            Booking.place_id == place_id,
            Booking.status != 'cancelled',
            ((Booking.start_date <= end_date) & (Booking.end_date >= start_date))
        ).first()

        if existing_booking:
            return jsonify({'error': 'These dates are not available'}), 400

        # Create the booking
        booking = Booking(
            place_id=place_id,
            user_id=current_user_id,
            start_date=start_date,
            end_date=end_date,
            message=data.get('message', ''),
            status='pending'
        )

        booking.validate()
        booking.save()

        # TODO: Send an email to the owner

        return jsonify(booking.to_dict()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/places/<string:place_id>/bookings', methods=['GET'])
def get_place_bookings(place_id):
    """Retrieves bookings for a place"""
    try:
        print(f"Accessing bookings for place {place_id}")  # Debug log
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404

        # For owners (with authentication)
        token = request.headers.get('Authorization')
        print(f"Auth token: {token}")  # Debug log

        if token and token.startswith('Bearer '):
            try:
                token_str = token.split(' ')[1]
                decoded_token = decode_token(token_str)
                print(f"Decoded token user: {decoded_token['sub']}")  # Debug log
                user_id = decoded_token['sub']
                if user_id == place.owner_id:
                    bookings = Booking.query.filter_by(place_id=place_id).all()
                    return jsonify([booking.to_dict() for booking in bookings]), 200
            except Exception as e:
                print(f"Token error: {str(e)}")  # Debug log

        # For other users or unauthenticated users
        print("Fetching confirmed bookings only")  # Debug log
        bookings = Booking.query.filter_by(
            place_id=place_id,
            status='confirmed'
        ).all()
        print(f"Found {len(bookings)} confirmed bookings")  # Debug log

        response_data = [{
            'start_date': booking.start_date.isoformat(),
            'end_date': booking.end_date.isoformat(),
            'status': booking.status
        } for booking in bookings]

        print(f"Sending response: {response_data}")  # Debug log
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/bookings/<string:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    """Updates the status of a booking"""
    try:
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Ensure the owner is updating the booking
        if booking.place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        status = data.get('status')

        if status not in ['confirmed', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400

        if status == 'confirmed':
            # Check that there are no other confirmed bookings for this period
            existing_booking = Booking.query.filter(
                Booking.place_id == booking.place_id,
                Booking.id != booking.id,
                Booking.status == 'confirmed',
                ((Booking.start_date <= booking.end_date) & (Booking.end_date >= booking.start_date))
            ).first()

            if existing_booking:
                return jsonify({'error': 'These dates are no longer available'}), 400

        booking.status = status
        booking.save()

        # For a confirmed booking, check and cancel overlapping pending bookings
        if status == 'confirmed':
            from app.models.booking import Booking
            overlapping_bookings = Booking.query.filter(
                Booking.place_id == booking.place_id,
                Booking.id != booking.id,
                Booking.status == 'pending',
                ((Booking.start_date <= booking.end_date) & (Booking.end_date >= booking.start_date))
            ).all()

            for overlap_booking in overlapping_bookings:
                overlap_booking.status = 'cancelled'
                overlap_booking.save()
                # TODO: Send an email to users whose bookings were cancelled

        # TODO: Send an email to the tenant to confirm/cancel

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/places/<string:place_id>/bookings/<string:booking_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_booking(place_id, booking_id):
    """Confirms a booking"""
    try:
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)

        if not booking or booking.place_id != place_id:
            return jsonify({'error': 'Booking not found'}), 404

        if booking.place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Check that there are no other confirmed bookings for this period
        existing_booking = Booking.query.filter(
            Booking.place_id == booking.place_id,
            Booking.id != booking.id,
            Booking.status == 'confirmed',
            ((Booking.start_date <= booking.end_date) & (Booking.end_date >= booking.start_date))
        ).first()

        if existing_booking:
            return jsonify({'error': 'These dates are no longer available'}), 400

        booking.status = 'confirmed'
        booking.save()

        # Cancel overlapping pending bookings
        overlapping_bookings = Booking.query.filter(
            Booking.place_id == booking.place_id,
            Booking.id != booking.id,
            Booking.status == 'pending',
            ((Booking.start_date <= booking.end_date) & (Booking.end_date >= booking.start_date))
        ).all()

        for overlap_booking in overlapping_bookings:
            overlap_booking.status = 'cancelled'
            overlap_booking.save()

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/places/<string:place_id>/bookings/<string:booking_id>/reject', methods=['POST'])
@jwt_required()
def reject_booking(place_id, booking_id):
    """Rejects a booking"""
    try:
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)

        if not booking or booking.place_id != place_id:
            return jsonify({'error': 'Booking not found'}), 404

        if booking.place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        booking.status = 'cancelled'
        booking.save()

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/users/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Retrieves bookings for the authenticated user"""
    try:
        current_user_id = get_jwt_identity()
        bookings = Booking.query.filter_by(user_id=current_user_id).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
