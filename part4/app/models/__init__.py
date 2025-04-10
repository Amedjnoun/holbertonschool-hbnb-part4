"""
Package d'initialisation des modèles SQLAlchemy.
Définit les structures de données de l'application.

Modèles:
    - User: Utilisateurs et authentification
    - Place: Lieux et propriétés
    - Review: Avis et notations
    - Amenity: Équipements disponibles

Relations:
    - User -> Place: Propriétaire
    - User -> Review: Auteur
    - Place -> Review: Avis reçus
    - Place <-> Amenity: Équipements disponibles
"""

# Import des modèles principaux
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Définition des modèles exportés
__all__ = ['User', 'Place', 'Review', 'Amenity']
