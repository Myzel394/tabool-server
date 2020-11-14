from apps.django.main.event.models import Event
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "EventField"
]


class EventField(WritableFromUserFieldMixin):
    model = Event
    detail_serializer = EventDetailSerializer
