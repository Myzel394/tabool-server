from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.utils.viewsets import RetrieveFromUserMixin
from ....filters import EventFilterSet
from ....models import Event
from ....serializers import EventDetailSerializer, EventListSerializer

__all__ = [
    "EventViewSet"
]


class EventViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    model = Event
    filterset_class = EventFilterSet
    search_fields = ["title"]
    ordering_fields = ["start_datetime", "end_datetime"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventDetailSerializer
