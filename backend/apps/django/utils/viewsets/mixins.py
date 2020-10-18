from abc import abstractmethod

from django.db.models import Model
from django_hint import *
from rest_framework import serializers, viewsets
from rest_framework.generics import get_object_or_404

from .helpers.mixins import DefaultAccessSerializer

__all__ = [
    "UserRelationViewSetMixin", "RetrieveFromUserMixin", "RetrieveAllMixin", "ModelHistoryMixin"
]


class UserRelationViewSetMixin(
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    access_serializer: Type[serializers.ModelSerializer] = DefaultAccessSerializer
    model: StandardModelType
    related_name: str = "user_relations"
    model_lookup_name: str = "id"
    serializer_lookup_key_name: str = "id"
    
    def get_queryset(self):
        return self.model.objects.from_user(self.request.user).distinct()
    
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        # Validation
        serializer = self.access_serializer(data={
            self.serializer_lookup_key_name: self.kwargs[lookup_url_kwarg]
        })
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        available_objects = self.get_queryset()
        obj = get_object_or_404(available_objects, **{
            self.model_lookup_name: validated_data[self.serializer_lookup_key_name]
        })
        
        return getattr(obj, self.related_name).only("user").get(user=self.request.user)


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