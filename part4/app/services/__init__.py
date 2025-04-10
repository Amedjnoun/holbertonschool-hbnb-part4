"""
Package d'initialisation pour la couche service.
Fournit un point d'accès unique à la facade principale.

Structure:
    - facade: Point d'entrée unique pour tous les services
    - UsersFacade: Gestion des utilisateurs
    - PlaceFacade: Gestion des lieux
    - AmenityFacade: Gestion des équipements
    - ReviewFacade: Gestion des avis
"""

from app.services.facade import HBnBFacade

def get_facade():
    """Récupère l'instance unique de la facade.

    Returns:
        HBnBFacade: Instance Singleton de la facade
    """
    return HBnBFacade()

# Instance partagée de la facade
facade = get_facade()

__all__ = ['facade', 'get_facade']
