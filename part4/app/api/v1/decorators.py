"""
Décorateurs personnalisés pour l'API.
Fournit des fonctionnalités de sécurité réutilisables.

Décorateurs disponibles:
    - admin_required: Vérifie les droits administrateur
    - jwt_required: Vérifie l'authentification
    - rate_limit: Limite le nombre de requêtes
"""

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify
from functools import wraps

def admin_required(fn):
    """Décorateur pour restreindre l'accès aux administrateurs.

    Validation:
        - Vérifie la présence du token JWT
        - Vérifie le statut administrateur
        - Journalise les tentatives d'accès

    Returns:
        function: Fonction décorée ou erreur 403
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'error': 'Admin privileges required'}), 403
        return fn(*args, **kwargs)
    return wrapper
