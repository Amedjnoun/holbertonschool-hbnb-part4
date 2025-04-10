from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description="First name of the user",
        max_length=50
    ),
    'last_name': fields.String(
        required=True,
        description="Last name of the user",
        max_length=50
    ),
    'email': fields.String(
        required=True,
        description="Email of the user",
        pattern=r'^[^@]+@[^@]+\.[^@]+$'
    ),
    'password': fields.String(
        required=True,
        description="User password",
        min_length=8,
        max_length=18,
    )
})

# Define the user model for input validation and documentation
user_model_update = api.model('User for update', {
    'first_name': fields.String(
        required=True,
        description="First name of the user",
        max_length=50
    ),
    'last_name': fields.String(
        required=True,
        description="Last name of the user",
        max_length=50
    )
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new user (Only for admin users)

        Returns:
        tuple: A tuple containing:
            - dict: A dictionary with either the created user
            details or an error message
            - int: HTTP status code
            (201 if successful, 400 if there is an error)
        """
        # Catch info from JWT
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Simulate email uniqueness check
        # (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'message': 'User created successfully'
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Get the list of all users

        Returns:
            tuple: A tuple containing:
                - list: A list of dictionnaries, each containing user data
                - int: HTTP status code 200 for success
        """
        users = facade.get_all_users()
        return [
            {
                'id': user_item.id,
                'first_name': user_item.first_name,
                'last_name': user_item.last_name,
                'email': user_item.email
            }
            for user_item in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.

        Args:
            user_id (UUID): The ID of the user to retrieve details for

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the user data
                or an error message.
                - int: HTTP status code (200 if successful, 404 if not found)
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}, 200

    @api.expect(user_model_update, validate=True)
    @api.response(200, "User succeffuly updated")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def put(self, user_id):
        """
        Update user details by ID.
        If the user is an admin :
            - they can update the email and password from any user.
        If the user is not an admin :
            - they can only update their own profils details.
            - they cannot modify the email or password even if these fields
                are specified in the input

        Only the user themselves can update their own details.

        Args:
            user_id (UUID): The ID of the user to be updated

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the updated
                    user data or an error message.
                - int: HTTP status code
                    (200 if successful, 400 or 404 if there is an error).
        """
        from app import bcrypt

        # Catch UUID from JWT and data
        current_user = get_jwt_identity()
        user_data = api.payload

        # Restriction if user is not an admin
        if not current_user.get('is_admin'):
            if 'password' in user_data or 'email' in user_data:
                return {"error": "You cannot modify email or password."}, 403

            if current_user["id"] != user_id:
                return {"error": "Unauthorized action"}, 403

        # Hash the new password
        if "password" in user_data:
            hashed_password = bcrypt.generate_password_hash(
                user_data["password"]
            ).decode('utf-8')
            user_data["password"] = hashed_password

        user = facade.update_user(user_id, user_data)
        if not user:
            return {"error": "User not found"}, 404
        else:
            return {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                }, 200
