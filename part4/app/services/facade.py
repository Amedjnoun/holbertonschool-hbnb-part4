"""
Facade principale de l'application HBnB.
Unifie l'accès à tous les services de l'application.

Pattern:
    - Facade Pattern: Fournit une interface unifiée pour tous les sous-systèmes
    - Singleton Pattern: Assure une instance unique de la facade

Responsabilités:
    - Coordination entre les différents services
    - Point d'entrée unique pour la logique métier
    - Gestion des dépendances entre services
"""

from app.services.UsersFacade import UsersFacade
from app.services.AmenityFacade import AmenityFacade
from app.services.PlaceFacade import PlaceFacade
from app.services.ReviewFacade import ReviewFacade
from app.models.user import User

class HBnBFacade:
    """Facade principale unifiant tous les services de l'application.

    Attributes:
        user_repo (UsersFacade): Service de gestion des utilisateurs
        place_repo (PlaceFacade): Service de gestion des lieux
        review_repo (ReviewFacade): Service de gestion des avis
        amenity_repo (AmenityFacade): Service de gestion des équipements
    """
    _instance = None

    def __new__(cls):
        """Implémente le pattern Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialise les services si ce n'est pas déjà fait."""
        if not hasattr(self, '_initialized') or not self._initialized:
            self.user_repo = UsersFacade()
            self.place_repo = PlaceFacade()
            self.review_repo = ReviewFacade()
            self.amenity_repo = AmenityFacade()
            self._initialized = True

    def create_user(self, user_data):
        """Crée un nouvel utilisateur.

        Args:
            user_data (dict): Données de l'utilisateur

        Returns:
            User: Instance utilisateur créée
        """
        return self.user_repo.create_user(user_data)

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son ID.

        Args:
            user_id (str): ID de l'utilisateur

        Returns:
            User: Instance utilisateur ou None
        """
        return self.user_repo.get_user(user_id)

    def get_all_users(self):
        """Récupère tous les utilisateurs.

        Returns:
            list[User]: Liste des utilisateurs
        """
        return self.user_repo.get_all_users()
