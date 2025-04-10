from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.amenity import Amenity
from app.models.user import User

# Create amenities blueprint
amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/amenities', methods=['GET'])
def get_amenities():
    """Get all available amenities."""
    try:
        amenities = Amenity.query.all()
        return jsonify([amenity.to_dict() for amenity in amenities]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get a specific amenity by ID."""
    try:
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404
        return jsonify(amenity.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    """Create a new amenity.

    Required JWT authentication.
    Only administrators can create amenities.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Administrator privileges required'}), 403

        data = request.get_json()

        # Check if amenity already exists
        existing = Amenity.get_by_name(data.get('name'))
        if existing:
            return jsonify({'error': 'Amenity already exists'}), 400

        amenity = Amenity.create_amenity(data)
        return jsonify(amenity.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/amenities/<string:amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    """Update an existing amenity.

    Required JWT authentication.
    Only administrators can update amenities.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Administrator privileges required'}), 403

        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404

        data = request.get_json()
        amenity.update_from_dict(data)
        return jsonify(amenity.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/amenities/<string:amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    """Delete an amenity.

    Required JWT authentication.
    Only administrators can delete amenities.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Administrator privileges required'}), 403

        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404

        amenity.delete()
        return jsonify({'message': 'Amenity deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@amenities_bp.route('/places/<string:place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Get amenities for a specific place."""
    try:
        from app.models.place import Place
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        return jsonify([amenity.to_dict() for amenity in place.amenities]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
