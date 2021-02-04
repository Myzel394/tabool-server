from rest_framework import viewsets

from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....models import Preference
from ....serializers import DetailPreferenceSerializer, UpdatePreferenceSerializer

__all__ = [
    "PreferenceViewSet"
]


class PreferenceViewSet(
    DetailSerializerViewSetMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    serializer_action_map = {
        "update": UpdatePreferenceSerializer,
        "partial_update": UpdatePreferenceSerializer,
        "retrieve": DetailPreferenceSerializer
    }
    detail_serializer = DetailPreferenceSerializer
    
    def get_queryset(self):
        return Preference.objects.only("user").filter(user=self.request.user)
