"""Module for managing administration"""
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db

# Create admin blueprint
admin_bp = Blueprint('admin', __name__)

def require_admin(fn):
    """Decorator to check if user is admin."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Get all users."""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['POST'])
@require_admin
def create_user():
    """Create a new user."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['email', 'password', 'first_name', 'last_name']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data.get('is_admin', False)
        )
        user.hash_password(data['password'])

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            raise e

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<string:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete a user."""
    try:
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot delete yourself'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<string:user_id>/promote', methods=['POST'])
@require_admin
def promote_user(user_id):
    """Promote a user to admin."""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_admin = True
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<string:user_id>/demote', methods=['POST'])
@require_admin
def demote_user(user_id):
    """Remove admin status from a user."""
    try:
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot demote yourself'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_admin = False
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
