"""
Module de gestion des routes protégées.
Implémente les endpoints nécessitant une authentification.

Fonctionnalités:
    - Protection des routes par JWT
    - Vérification des tokens
    - Gestion des droits d'accès
    - Journalisation des accès
"""

from flask import jsonify, request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

api = Namespace('protected', description='Endpoints sécurisés')

def log_access(user_id, endpoint):
    """Journalise les accès aux endpoints protégés.

    Args:
        user_id (str): ID de l'utilisateur
        endpoint (str): Endpoint accédé
    """
    print(f"[{datetime.utcnow()}] Accès à {endpoint} par utilisateur {user_id}")

@api.route('/', strict_slashes=False)
class ProtectedResource(Resource):
    """Ressource nécessitant une authentification.

    Sécurité:
        - Token JWT valide requis
        - Vérification de l'expiration
        - Journalisation des accès
    """

    @api.doc(security='jwt')
    @jwt_required()
    @api.doc(security='jwt')
    @api.response(200, 'Accès autorisé')
    @api.response(401, 'Token invalide ou expiré')
    def get(self):
        """Endpoint protégé nécessitant un JWT valide.

        Returns:
            dict: Message de bienvenue avec ID utilisateur
            int: Code HTTP 200 si succès
        """
        current_user = get_jwt_identity()
        print(f"🔐 Accès autorisé pour {current_user}")  # Debug
        log_access(current_user["id"], request.endpoint)

        return {
            'message': f'Bienvenue, utilisateur {current_user["id"]}!',
            'timestamp': datetime.utcnow().isoformat()
        }, 200

@api.route('/secure-data')
class ProtectedResource(Resource):
    @api.doc(security='jwt')
    @jwt_required()
    def get(self):
        """Endpoint protégé nécessitant un token."""
        current_user = get_jwt_identity()
        return {"message": f"Bienvenue, {current_user['id']}!"}, 200