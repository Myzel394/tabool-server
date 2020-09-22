from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ....models import Event
from ....serializers import EventDetailSerializer, EventListSerializer

__all__ = [
    "EventViewSet"
]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return Event.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventDetailSerializer
