from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Event

__all__ = [
    "EventScoosoScraperSerializer"
]


class EventScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime"
        ]
