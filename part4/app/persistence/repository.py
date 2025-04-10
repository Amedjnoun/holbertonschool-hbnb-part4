"""
Interface et implémentation du pattern Repository.
Fournit une abstraction de la couche de persistance.

Patterns:
    - Repository Pattern
    - Interface Segregation
    - Dependency Inversion
"""

from abc import ABC, abstractmethod

class Repository(ABC):
    """Interface abstraite définissant les opérations de persistance.

    Cette interface assure une séparation entre la logique métier
    et la couche de persistance, permettant de changer facilement
    d'implémentation (SQL, NoSQL, fichiers, etc.)
    """
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """Implémentation en mémoire pour les tests.

    Stocke les données dans un dictionnaire en mémoire.
    Utile pour les tests unitaires et le développement.
    """
    def __init__(self):
        self._storage = {}

    def get_by_title(self, title):
        for place in self.places:
            if place.title == title:
                return place
        return None

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
