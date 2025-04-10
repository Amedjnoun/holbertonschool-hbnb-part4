"""Authentication endpoints for the API."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from app.models.user import User
from app.extensions import db

# Create the blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint.

    Creates a new user and returns JWT token.
    """
    try:
        # Get registration data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user (always non-admin)
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=False
        )
        user.hash_password(data['password'])

        # Save the user
        db.session.add(user)
        db.session.commit()

        # Create the JWT token
        access_token = create_access_token(identity=user.id)

        # Return the token and user info
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint.

    Returns JWT token for authenticated users.
    """
    try:
        # Get login data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Create the JWT token
        access_token = create_access_token(identity=user.id)

        # Return the token and user info
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile.

    Requires JWT authentication.
    """
    try:
        # Get the user ID from the token
        current_user_id = get_jwt_identity()

        # Retrieve the user
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Return the user information
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
