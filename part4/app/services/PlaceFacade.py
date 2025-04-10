"""
Facade pour la gestion des lieux.
Implémente la logique métier pour les locations et propriétés.

Responsabilités:
    - CRUD des lieux
    - Validation des données géographiques
    - Gestion des relations propriétaire/équipements
    - Vérification des contraintes métier
"""

from app.models.place import Place
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade

class PlaceFacade:
    """Gère les opérations liées aux lieux et propriétés.

    Attributes:
        place_repo (SQLAlchemyRepository): Repository pour les lieux
        amenityfacade (AmenityFacade): Service de gestion des équipements
        userfacade (UsersFacade): Service de gestion des utilisateurs
    """

    def __init__(self):
        """Initialise les services nécessaires."""
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenityfacade = AmenityFacade()
        self.userfacade = UsersFacade()

    def create_place(self, place_data):
        """Crée un nouveau lieu.

        Args:
            place_data (dict): Données du lieu avec:
                - title: Titre de l'annonce
                - description: Description détaillée
                - price: Prix par nuit
                - latitude/longitude: Coordonnées GPS
                - owner_id: ID du propriétaire

        Returns:
            Place: Instance créée ou None si erreur

        Validation:
            - Titre unique
            - Propriétaire existant
            - Coordonnées valides
        """
        existing_places = self.place_repo.get_all()
        for place in existing_places:
            if place.title == place_data.get("title"):
                print(f"Title '{place_data['title']}' already exists.")  # Debug
                return None  # Retourne None si le titre existe déjà
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id= place_data["owner_id"]
        )
        if not place:
            print("Failed to create place.")
        self.place_repo.add(place)  # Ajoute le lieu à la base de données
        return place  # Retourne l'objet Place créé

    def get_place(self, place_id):
        """Retrieve complete place details with owner and amenities."""
        print(f"🔍 Fetching place with ID: {place_id}")  # Debug log

        place = self.place_repo.get(place_id)

        if not place:
            print(f"❌ Place {place_id} not found in database")  # Debug log
            return None  # ✅ Correct behavior

        return place  # ✅ Return the `Place` model object instead of a dictionary


    def get_all_places(self):
        """Retrieve all places and attach owner details."""
        places = self.place_repo.get_all()
        if not places:
            return []

        result = []
        for place in places:
            owner = self.userfacade.get_user(place.owner_id)  # Fetch owner details

            result.append({
                'id': place.id,
                'description': place.description,
                'title': place.title,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                } if owner else None,  # Ensure the owner exists
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in place.amenities] if place.amenities else [],
                'reviews': [{
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                } for review in place.reviews] if place.reviews else []
            })

        return result


    def update_place(self, place_id, place_data):
        """Met à jour un lieu existant.

        Args:
            place_id (str): Identifiant du lieu
            place_data (dict): Nouvelles données

        Returns:
            Place: Instance mise à jour ou None si non trouvé

        Validation:
            - Existence du lieu
            - Validité des nouvelles données
        """
        place = self.place_repo.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            self.place_repo.update(place.id, place_data)

            print(f"✅ Update successful: {place.to_dict()}")  # Debug
            return place.to_dict()

        print("❌ Update failed!")
        return None

    def delete_place(self, place_id):
        """Supprime un lieu.

        Args:
            place_id (str): Identifiant du lieu

        Returns:
            bool: True si supprimé, False sinon
        """
        return self.place_repo.delete(place_id)
