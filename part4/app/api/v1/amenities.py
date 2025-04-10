from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("amenities", description="Amenity operations")

# Define the amenity model for input validation and documentation
amenity_model = api.model("Amenity", {
    "name": fields.String(
        required=True,
        description="Name of the amenity",
        max_length=50
    )
})


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        """
        Add a new amenity (Only for admin users)

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the created amenity
                details or an error message
                - int: HTTP status code
                (201 if successful, 400 if there is an error)
        """
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload

        amenities = facade.get_all_amenities()
        for amenity_item in amenities:
            if amenity_item.name == amenity_data["name"]:
                return {"error": "Amenity already registered"}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            "id": new_amenity.id,
            "name": new_amenity.name
        }, 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """
        Get the list of all amenities

        Returns:
            tuple: A tuple containing:
                - list: A list of dictionnaries, each containing amenity data
                - int: HTTP status code 200 for success
        """
        amenities = facade.get_all_amenities()

        return [
            {
                "id": amenity_item.id,
                "name": amenity_item.name
            }
            for amenity_item in amenities
        ], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """
        Get amenity details by ID.

        Args:
            amenity_id (UUID): The ID of the amenity to retrieve details for

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the amenity data
                or an error message.
                - int: HTTP status code (200 if successful, 404 if not found)
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        else:
            return {
                "id": amenity.id,
                "name": amenity.name
            }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    @api.response(409, "Duplicate amenity name")
    @jwt_required()
    def put(self, amenity_id):
        """
        Update amenity details by ID.

        Args:
            amenity_id (UUID): The ID of the amenity to be updated

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with either the updated amenity data
                or an error message.
                - int: HTTP status code
                (200 if successful, 400 or 404 if error)
        """

        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload
        if not amenity_data or not isinstance(amenity_data, dict):
            return {"error": "Invalid input data"}, 400

        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"message": str(e)}, 409  # Return conflict error for duplicate name

        if not amenity:
            return {"error": "Amenity not found"}, 404
        else:
            return {
                "id": amenity.id,
                "name": amenity.name
            }, 200
