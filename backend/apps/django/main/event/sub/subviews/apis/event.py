from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.main.event.filters import EventFilterSet
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

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilterSet
    search_fields = ["information", "title"]
    ordering_fields = ["start_datetime", "end_datetime", "title"]

    detail_serializer = DetailEventSerializer
    serializer_action_map = {
        "create": CreateEventSerializer,
        "update": UpdateEventSerializer,
        "partial_update": UpdateEventSerializer,
        "retrieve": DetailEventSerializer,
        "list": DetailEventSerializer
    }

    def get_queryset(self):
        return Event.objects.from_user(self.request.user)
