"""Place-related API endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.extensions import db

places_bp = Blueprint('places', __name__)

@places_bp.route('/places', methods=['GET'])
def get_places():
    """Retrieve all places.

    Optional query parameters:
    - city: Filter by city
    - min_price: Filter by minimum price
    - max_price: Filter by maximum price
    - amenities: Comma-separated list of amenity IDs
    """
    try:
        # Get query parameters
        city = request.args.get('city')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        amenity_ids = request.args.get('amenities')

        # Start with all places
        query = Place.query

        # Apply filters if provided
        if city:
            query = query.filter(Place.city.ilike(f'%{city}%'))

        if min_price:
            query = query.filter(Place.price_per_night >= int(min_price))

        if max_price:
            query = query.filter(Place.price_per_night <= int(max_price))

        # Filter by amenities if provided
        if amenity_ids:
            amenity_id_list = amenity_ids.split(',')
            for amenity_id in amenity_id_list:
                query = query.filter(Place.amenities.any(Amenity.id == amenity_id.strip()))

        # Execute the query
        places = query.all()

        # Return the results
        return jsonify([place.to_dict(include_relationships=True) for place in places]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@places_bp.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific place by ID."""
    try:
        place = Place.query.get(place_id)

        if not place:
            return jsonify({"error": "Place not found"}), 404

        return jsonify(place.to_dict(include_relationships=True)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new place.

    Required JWT authentication.
    """
    try:
        # Get the current user ID from the JWT token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get place data from request
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ['name', 'description', 'address', 'city', 'country',
                           'price_per_night', 'max_guests', 'number_of_rooms',
                           'number_of_bathrooms']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        # Add owner ID to data
        data['owner_id'] = user_id

        # Get amenity IDs if provided
        amenity_ids = data.pop('amenity_ids', None)

        # Create the place
        place = Place.create_place(data, amenity_ids)

        return jsonify(place.to_dict(include_relationships=True)), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@places_bp.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update an existing place.

    Required JWT authentication.
    Only the owner can update their place.
    """
    try:
        # Get the current user ID from the JWT token
        user_id = get_jwt_identity()

        # Get the place
        place = Place.query.get(place_id)

        if not place:
            return jsonify({"error": "Place not found"}), 404

        # Check if the user is the owner
        if place.owner_id != user_id:
            return jsonify({"error": "You can only update your own places"}), 403

        # Get update data from request
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Get amenity IDs if provided
        amenity_ids = data.pop('amenity_ids', None)

        # Update the place
        place.update_from_dict(data, amenity_ids)

        return jsonify(place.to_dict(include_relationships=True)), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@places_bp.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Delete a place.

    Required JWT authentication.
    Only the owner can delete their place.
    """
    try:
        # Get the current user ID from the JWT token
        user_id = get_jwt_identity()

        # Get the place
        place = Place.query.get(place_id)

        if not place:
            return jsonify({"error": "Place not found"}), 404

        # Check if the user is the owner
        if place.owner_id != user_id:
            return jsonify({"error": "You can only delete your own places"}), 403

        # Delete the place
        place.delete()

        return jsonify({"message": "Place deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
