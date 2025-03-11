from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns, places_reviews_ns
from app.api.v1.places import api as places_ns
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# instanciate the bcrypt object
bcrypt = Bcrypt()

# instanciate the jwt object
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Register the differents namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(places_reviews_ns, path='/api/v1/places')

    # Initialize bcrypt
    bcrypt.init_app(app)

    # initialize jwt
    jwt.init_app(app)

    return app
