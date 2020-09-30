from rest_framework import viewsets

from apps.utils.viewsets.mixins import RetrieveFromUserMixin
from ...subserializers import ModificationDetailSerializer, ModificationListSerializer
from ....models import Modification

__all__ = [
    "ModificationViewSet"
]


class ModificationViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    model = Modification
    
    def get_serializer_class(self):
        if self.action == "list":
            return ModificationListSerializer
        return ModificationDetailSerializer
