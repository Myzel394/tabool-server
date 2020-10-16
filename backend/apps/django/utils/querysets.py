from abc import abstractmethod
from typing import *

from django.db.models import Model
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin
from django_hint import *

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "RelationQuerySetMixin", "RelationAllUserQuerySetMixin"
]


# TODO: Add documentation!
class RelationQuerySetMixin:
    ref_filter_statement: str
    related_model: StandardModelType
    ref_model: Type[CustomQuerySetMixin]
    model_field_name: Optional[str] = None
    user_field_name: str = "user"
    ref_user_find_filter_statement: Optional[str] = None
    
    @property
    def model_field_name_full(self):
        return self.model_field_name or self.model.__name__.lower()
    
    @property
    def ref_user_find_filter_statement_full(self):
        return self.ref_user_find_filter_statement or f"{self.ref_filter_statement}__participants__in"
    
    def manage_relations(self, users: List["User"], ref) -> None:
        model_field_name = self.model_field_name_full
        
        for obj in self.filter(**{
            self.ref_filter_statement: ref
        }):
            # Add
            for user in users:
                self.related_model.objects.get_or_create(**{
                    model_field_name: obj,
                    self.user_field_name: user
                })
            
            # Remove
            for user in self.related_model.objects.all().values_list(self.user_field_name, flat=True).distinct():
                self.related_model \
                    .objects \
                    .all() \
                    .filter(**{self.user_field_name: user}) \
                    .exclude(**{f"{self.model_field_name_full}__{self.ref_user_find_filter_statement_full}": [user]}) \
                    .delete()
    
    def manage_relations_with_given_user(self, user: "User"):
        for element in self.all().filter(**{
            self.ref_user_find_filter_statement_full: [user]
        }):
            ref = self.get_ref_from_element(element)
            
            self.manage_relations([user], ref)
    
    @staticmethod
    @abstractmethod
    def get_ref_from_element(element) -> Model:
        raise NotImplementedError()


class RelationAllUserQuerySetMixin:
    related_model: StandardModelType
    ref_model: Type[CustomQuerySetMixin]
    ref_name: Optional[str] = None
    
    def manage_relations(self, users: List["User"], ref) -> None:
        ref_name = self.ref_name or ref.__class__.__name__.lower()
        
        for user in users:
            self.related_model.objects.get_or_create(**{
                "user": user,
                ref_name: ref
            })
    
    def manage_relations_with_given_user(self, user: "User"):
        for element in self.all():
            self.manage_relations([user], element)
