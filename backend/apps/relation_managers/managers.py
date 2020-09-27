from abc import ABC, abstractmethod
from typing import *

__all__ = [
    "RelationManagerMixin", "SimpleRelatedRelationManagerMixin"
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
    class Meta:
        model: Type[T]
    
    related_model: Type[R]
    
    @abstractmethod
    def get_users(self):
        raise NotImplementedError()
    
    def create_relations(self) -> None:
        users = self.get_users()
        self.related_model.objects.manage_relations(users, self.instance)
