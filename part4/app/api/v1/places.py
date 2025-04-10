from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        description='Title of the place'),
    'description': fields.String(
        description='Description of the place',
        ),
    'price': fields.Float(
        required=True,
        description='Price per night',
        min=0,
        ),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place',
        min=-90,
        max=90,
        ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place',
        min=-180,
        max=180,
        ),
    'amenities': fields.List(
        fields.String,
        required=False,
        description="List of amenities ID's"
        )
})

# Special model when updating a place
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(
        required=True,
        description='Title of the place'),
    'description': fields.String(
        description='Description of the place',
        ),
    'price': fields.Float(
        required=True,
        description='Price per night',
        min=0,
        )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # Catch UUID from JWT and store in place_data['owner_id']
        current_user = get_jwt_identity()
        place_data['owner_id'] = current_user["id"]  # Use 'owner_id'

        # Convert price to 2 digit:
        place_data['price'] = round(place_data['price'], 2)

        # Create the place
        place = facade.create_place(place_data)

        # Retrieve owner details
        owner = facade.get_user(place.owner_id)

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places

        In view of the changes to the expected output in the
        instructions, the fields that are not
        currently required are commented on.
        """
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            # 'description': place.description,
            'price': place.price,
            # 'latitude': place.latitude,
            # 'longitude': place.longitude,
            # 'owner': place.owner,
            # 'amenities': place.amenities
        } for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID

        In view of the changes to the expected output in the
        instructions, the fields that are not
        currently required are commented on.
        """

        place = facade.get_place(place_id)
        if place:
            # Fetch owner details using the owner_id
            owner = facade.get_user(place.owner_id)  # Use 'owner_id'

            # Prepare owner data
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,  # Include owner details
                # 'amenities': place.amenities
            }, 200

        return {'message': 'Place not found'}, 404

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        if not place_data:
            return {'message': 'No data provided'}, 400

        # Catch user UUID from JWT token
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)

        place = facade.get_place(place_id)

        if not is_admin and place.owner_id != current_user["id"]:  # Use 'owner_id'
            return {'error': 'Unauthorized action'}, 403

        # Convert price to 2 digit :
        if "price" in place_data:
            place_data['price'] = round(place_data['price'], 2)

        place = facade.update_place(place_id, place_data)

        if place:
            return {'message': 'Place updated successfully'}, 200
        return {'message': 'Place not found'}, 404
