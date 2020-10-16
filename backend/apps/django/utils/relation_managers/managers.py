from abc import ABC, abstractmethod
from typing import *

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

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
    
    @staticmethod
    @abstractmethod
    def create_relations_with_given_user(user: "User"):
        raise NotImplementedError()


class SimpleRelatedRelationManagerMixin(RelationManagerMixin, ABC):
    related_model: Type[R]
    
    @abstractmethod
    def get_users(self):
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod
    def get_model_from_related_instance(instance: R) -> T:
        raise NotImplementedError()
    
    def create_relations(self) -> None:
        users = self.get_users()
        self.related_model.objects.manage_relations(users, self.instance)
    
    @classmethod
    def create_relations_with_given_user(cls, user: "User"):
        cls.related_model.objects.manage_relations_with_given_user(user)


class SimpleAllUserRelationManagerMixin(RelationManagerMixin, ABC):
    @staticmethod
    def get_users():
        return get_user_model().objects.active_users()
    
    def create_relations(self) -> None:
        users = self.get_users()
        self.Meta.model.objects.manage_relations(users, self.instance)
    
    @classmethod
    def create_relations_with_given_user(cls, user: "User"):
        cls.Meta.model.objects.manage_relations_with_given_user(user)
