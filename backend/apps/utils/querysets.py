from django_common_utils.libraries.models import CustomQuerySetMixin
from django_hint import *

from apps.authentication.public.model_references import *

__all__ = [
    "RelationQuerySetMixin", "RelationAllUserQuerySetMixin"
]


# TODO: Remove Inheritance in RelationQuerySetMixin
class RelationQuerySetMixin(CustomQuerySetMixin.QuerySet):
    ref_filter_statement: str
    related_model: StandardModelType
    model_field_name: Optional[str] = None
    user_field_name: str = "user"
    ref_delete_filter_statement: Optional[str] = None
    
    def manage_relations(self, users: List[USER], ref) -> None:
        model_field_name = self.model_field_name or self.model.__name__.lower()
        ref_delete_filter_statement = self.ref_delete_filter_statement or \
                                      f"{model_field_name}__{self.ref_filter_statement}__participants__in"
        
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
                    .exclude(**{ref_delete_filter_statement: [user]}) \
                    .delete()


class RelationAllUserQuerySetMixin:
    related_model: StandardModelType
    ref_name: Optional[str] = None
    
    def manage_relations(self, users: List[USER], ref) -> None:
        ref_name = self.ref_name or ref.__class__.__name__.lower()
        
        for user in users:
            self.related_model.objects.get_or_create(**{
                "user": user,
                ref_name: ref
            })
        

