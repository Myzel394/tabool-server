from rest_framework import viewsets

from apps.django.main.event.models import Event
from apps.django.main.event.serializers import CreateEventSerializer, DetailEventSerializer, UpdateEventSerializer
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin

__all__ = [
    "EventViewSet"
]


class EventViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    detail_serializer = DetailEventSerializer
    serializer_action_map = {
        "create": CreateEventSerializer,
        "update": UpdateEventSerializer,
        "partial_update": UpdateEventSerializer,
        "retrieve": DetailEventSerializer,
        "list": DetailEventSerializer
    }
    
    def get_queryset(self):
        return Event.ordering.from_user(self.request.user)
