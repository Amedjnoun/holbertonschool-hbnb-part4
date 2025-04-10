from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.models.place import Place
from app.models.user import User
from app.extensions import db

# Create reviews blueprint
reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/places/<string:place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Get all reviews for a specific place."""
    try:
        reviews = Review.query.filter_by(place_id=place_id).all()
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/places/<string:place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    """Create a new review for a place.

    Required JWT authentication.
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Check if place exists
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404

        # Check if user owns the place
        if place.owner_id == current_user_id:
            return jsonify({'error': 'Cannot review your own place'}), 400

        # Check if user already reviewed this place
        existing_review = Review.query.filter_by(
            user_id=current_user_id,
            place_id=place_id
        ).first()
        if existing_review:
            return jsonify({'error': 'You have already reviewed this place'}), 400

        # Create review
        review = Review(
            text=data['text'],
            rating=int(data['rating']),
            user_id=current_user_id,
            place_id=place_id
        )

        review.validate()
        db.session.add(review)
        db.session.commit()

        return jsonify(review.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review by ID."""
    try:
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        return jsonify(review.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/reviews/<string:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update an existing review.

    Required JWT authentication.
    Only the author can update their review.
    """
    try:
        current_user_id = get_jwt_identity()
        review = Review.query.get(review_id)

        if not review:
            return jsonify({'error': 'Review not found'}), 404

        if review.user_id != current_user_id:
            return jsonify({'error': 'Cannot modify another user\'s review'}), 403

        data = request.get_json()
        review.text = data.get('text', review.text)
        review.rating = int(data.get('rating', review.rating))
        review.validate()

        db.session.commit()
        return jsonify(review.to_dict()), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/reviews/<string:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review.

    Required JWT authentication.
    Only the author can delete their review.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        review = Review.query.get(review_id)

        if not review:
            return jsonify({'error': 'Review not found'}), 404

        # Allow deletion by review owner or place owner or admin
        if not (review.user_id == current_user_id or
                review.place.owner_id == current_user_id or
                user.is_admin):
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
