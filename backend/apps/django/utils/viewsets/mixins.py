from abc import abstractmethod

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

__all__ = [
    "UserRelationViewSetMixin", "RetrieveFromUserMixin", "RetrieveAllMixin", "ModelHistoryMixin", "BulkDeleteMixin"
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
        
        # Check if instance already exists
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


class ModelHistoryMixin(viewsets.ReadOnlyModelViewSet):
    instance_field_name: str
    
    @abstractmethod
    def get_obj_from_parent_qs(self, qs: QueryType) -> StandardModelType:
        raise NotImplementedError()
    
    def get_queryset(self):
        method = getattr(self, "get_base_queryset", getattr(super(), "get_queryset"))
        qs = method()
        instance = self.get_obj_from_parent_qs(qs)
        histories = instance.history.all().order_by("-history_date")
        current_instance = histories.latest()
        
        return histories.only("pk").exclude(pk=current_instance.pk)
    
    def get_serializer_context(self):
        qs = self.get_queryset()
        context = super().get_serializer_context()
        latest_instance = qs.latest()
        
        return context | {
            "latest_history_instance": latest_instance.next_record  # Getting the current instance
        }


class BulkDeleteMixin:
    @action(methods=["DELETE"], detail=False)
    def delete(self, request: RequestType):
        ids = request.GET.getlist("ids[]", [])
        
        if type(ids) is list and len(ids) > 0:
            queryset = self.get_queryset().only("id").filter(id__in=ids)
            
            if len(queryset) == len(ids):
                # Delete each object, otherwise some signals would be missing
                for obj in queryset:
                    pass
                    # obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                "message": _("Nicht alle Objekte gefunden.")
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": _('Feld "ids" fehlt oder ist ungültig.')
        }, status=status.HTTP_400_BAD_REQUEST)
