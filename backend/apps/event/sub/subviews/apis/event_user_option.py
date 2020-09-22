from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ....models import EventUserOption
from ....serializers import EventUserOptionDetailSerializer, EventUserOptionListSerializer

__all__ = [
    "EventUserOptionViewSet"
]


class EventUserOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return EventUserOption.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return EventUserOptionListSerializer
        return EventUserOptionDetailSerializer
