from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        Returns:
        tuple: A tuple containing:
            - dict: A dictionary with either the created user
            details or an error message
            - int: HTTP status code
            (201 if successful, 400 if there is an error)
        """
        user_data = api.payload

        # Simulate email uniqueness check
        # (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email}, 201

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

    @api.expect(user_model, validate=True)
    @api.response(200, "User succeffuly updated")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    def put(self, user_id):
        """
        Update user details by ID.

        Args:
            user_id (UUID): The ID of the user to be updated

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the updateduser data
                or an error message.
                - int: HTTP status code
                (200 if successful, 400 or 404 if error)
        """
        user_data = api.payload

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
