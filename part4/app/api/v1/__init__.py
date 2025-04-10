"""Module d'initialisation de l'API v1"""
from flask import Blueprint
from .auth import auth_bp
from .places import places_bp
from .reviews import reviews_bp
from .amenities import amenities_bp
from .admin import admin_bp

# Création du blueprint principal de l'API v1
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Enregistrement des blueprints
api_v1.register_blueprint(auth_bp)      # Routes d'authentification
api_v1.register_blueprint(places_bp)    # Routes des lieux
api_v1.register_blueprint(reviews_bp)   # Routes des avis
api_v1.register_blueprint(amenities_bp) # Routes des équipements
api_v1.register_blueprint(admin_bp)     # Routes d'administration

# Liste des routes disponibles pour la documentation
routes = {
    'auth': {
        'login': '/auth/login',
        'profile': '/auth/profile',
        'check': '/auth/check'
    },
    'places': {
        'list': '/places',
        'create': '/places',
        'get': '/places/<id>',
        'update': '/places/<id>',
        'delete': '/places/<id>',
        'reviews': '/places/<id>/reviews'
    },
    'reviews': {
        'create': '/places/<place_id>/reviews',
        'get': '/reviews/<id>',
        'update': '/reviews/<id>',
        'delete': '/reviews/<id>'
    },
    'amenities': {
        'list': '/amenities',
        'create': '/amenities',
        'get': '/amenities/<id>',
        'delete': '/amenities/<id>'
    },
    'admin': {
        'users': '/admin/users',
        'user': '/admin/users/<id>',
        'promote': '/admin/users/<id>/promote',
        'demote': '/admin/users/<id>/demote'
    }
}
