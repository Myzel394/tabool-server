from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....filters import ModificationFilterSet
from ....models import Modification
from ....serializers import DetailModificationSerializer, ListModificationSerializer

__all__ = [
    "ModificationViewSet"
]


class ModificationViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    model = Modification
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ModificationFilterSet
    search_fields = ["information"]
    ordering_fields = ["start_datetime", "end_datetime"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return ListModificationSerializer
        return DetailModificationSerializer
