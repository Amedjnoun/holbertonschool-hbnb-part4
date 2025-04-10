""" API protected Endpoints with JWT auth """

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

api = Namespace('protected', description='Protected areas')


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Retrieve the user's identity from the token
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
