from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

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

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        qs = self.get_queryset()
        obj = get_object_or_404(qs, user__id=self.kwargs[lookup_url_kwarg])

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
