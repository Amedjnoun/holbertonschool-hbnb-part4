"""
Facade pour la gestion des avis.
Implémente la logique métier pour les avis et notes.

Responsabilités:
    - Validation des notes (1-5)
    - Vérification des droits utilisateur
    - Calcul des moyennes
    - Gestion des contraintes (ex: un avis par utilisateur)
"""

from app.models.review import Review
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository


class ReviewFacade:
    def __init__(self):
        """Initialisation du repo pour la gestion des reviews"""
        self.review_repo = SQLAlchemyRepository(Review)

    def create_review(self, review_data):
        """Crée un nouvel avis.

        Validation:
            - Note entre 1 et 5
            - Texte non vide
            - Un seul avis par utilisateur par lieu

        Args:
            review_data (dict): Données de l'avis

        Returns:
            Review: Instance créée ou None si erreur
        """
        # Validation
        if not review_data.get("text") or not isinstance(review_data["text"], str):
            return None
        if not (1 <= review_data.get("rating", 0) <= 5):
            return None

        # Vérifier si l'utilisateur a déjà laissé un avis sur ce lieu
        existing_review = self.review_repo.model.query.filter_by(
            user_id=review_data["user_id"], place_id=review_data["place_id"]
        ).first()

        if existing_review:
            return None  # L'utilisateur a déjà noté ce lieu

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Récupérer une review par ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Récupérer toutes les reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Récupérer toutes les reviews pour un lieu"""
        return self.review_repo.model.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, review_data):
        """Mettre à jour une review"""
        review = self.get_review(review_id)
        if not review:
            return None
        
        for key, value in review_data.items():
            setattr(review, key, value)
        
        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        """Supprimer une review"""
        review = self.get_review(review_id)
        if not review:
            return None
        
        self.review_repo.delete(review)
        return True
