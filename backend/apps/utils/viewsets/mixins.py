from django.db.models import Model
from django_hint import *
from rest_framework import serializers, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .helpers.mixins import DefaultAccessSerializer

__all__ = [
    "UserRelationViewSetMixin", "RetrieveFromUserMixin", "RetrieveAllMixin"
]


class UserRelationViewSetMixin(
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticated
    ]
    access_serializer: Type[serializers.ModelSerializer] = DefaultAccessSerializer
    model: StandardModelType
    related_name: str = "user_relations"
    model_lookup_name: str = "id"
    serializer_lookup_key_name: str = "id"
    
    def get_queryset(self):
        return self.model.objects.all().from_user(self.request.user)
    
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
    permission_classes = [
        IsAuthenticated
    ]
    model: Type[Model]
    
    def get_queryset(self):
        return self.model.objects.all().from_user(self.request.user)


class RetrieveAllMixin(RetrieveFromUserMixin):
    def get_queryset(self):
        return self.model.objects.all()
