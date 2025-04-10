"""
Package d'initialisation pour la couche de persistance.
Implémente le pattern Repository pour l'accès aux données.

Structure:
    - Repository: Interface abstraite de persistance
    - SQLAlchemyRepository: Implémentation SQL
    - InMemoryRepository: Implémentation en mémoire pour tests

Design Patterns:
    - Repository Pattern: Abstraction de la persistance
    - Strategy Pattern: Permet de changer d'implémentation
"""

from app.persistence.repository import Repository, InMemoryRepository
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository

__all__ = [
    'Repository',
    'SQLAlchemyRepository',
    'InMemoryRepository'
]

# Configuration par défaut
DEFAULT_REPOSITORY = SQLAlchemyRepository
