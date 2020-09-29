from abc import ABC, abstractmethod
from typing import *

from django.contrib.auth import get_user_model

__all__ = [
    "RelationManagerMixin", "SimpleRelatedRelationManagerMixin", "SimpleAllUserRelationManagerMixin"
]


T = TypeVar("T")
R = TypeVar("R")


class RelationManagerMixin(ABC):
    class Meta:
        model: Type[T]
    
    def __init__(
            self,
            instance: T,
            **kwargs
    ):
        self.instance = instance
        self.kwargs = kwargs
    
    @abstractmethod
    def create_relations(self) -> None:
        raise NotImplementedError()


class SimpleRelatedRelationManagerMixin(RelationManagerMixin, ABC):
    related_model: Type[R]
    
    @abstractmethod
    def get_users(self):
        raise NotImplementedError()
    
    def create_relations(self) -> None:
        users = self.get_users()
        self.related_model.objects.manage_relations(users, self.instance)


class SimpleAllUserRelationManagerMixin(RelationManagerMixin, ABC):
    @staticmethod
    def get_users():
        return get_user_model().objects.active_users()
    
    def create_relations(self) -> None:
        users = self.get_users()
        self.Meta.model.objects.manage_relations(users, self.instance)
