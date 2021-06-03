from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

__all__ = [
    "UserRelationViewSetMixin", "RetrieveFromUserMixin", "RetrieveAllMixin"
]


class UserRelationViewSetMixin(
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    model: StandardModelType
    relation_model: StandardModelType
    
    # Lookup
    kwargs_field_name: str = "pk"
    model_lookup_field_name: str = "id"
    
    relation_model_lookup: Optional[str] = None
    relation_model_user_lookup: str = "user"
    
    def get_queryset(self):
        return self.model.objects.from_user(self.request.user).distinct()
    
    def get_model_object(self) -> StandardModelType:
        """Gets the model (not relation model) via the key argument in kwargs"""
        key = self.kwargs.get(self.kwargs_field_name)
        
        if key == "":
            raise ValidationError(_("ID fehlt."))
        
        available_objects = self.get_queryset()
        obj = get_object_or_404(available_objects, **{
            self.model_lookup_field_name: key
        })
        
        return obj
    
    def get_relation_object(self, obj: StandardModelType) -> StandardModelType:
        """Gets the relation model from `obj`"""
        field = self.relation_model_lookup or self.model.__name__.lower()
        user_field = self.relation_model_user_lookup
        model_data = {
            field: obj,
            user_field: self.request.user
        }
        
        try:
            relation_obj = self.relation_model.objects \
                .only(field, user_field) \
                .get(**model_data)
        except ObjectDoesNotExist:
            relation_obj = self.relation_model.objects \
                .create(**model_data)
        
        return relation_obj
    
    def get_object(self):
        obj = self.get_model_object()
        relation_object = self.get_relation_object(obj)
        
        return relation_object


class RetrieveFromUserMixin(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    model: Type[Model]
    
    def get_queryset(self):
        return self.model.objects.from_user(self.request.user).distinct()


class RetrieveAllMixin(RetrieveFromUserMixin):
    def get_queryset(self):
        return self.model.objects.all().distinct()
