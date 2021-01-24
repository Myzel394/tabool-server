from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Event
from ...sub.subserializers.event.detail import DetailEventSerializer

__all__ = [
    "EventField"
]


class EventField(WritableFromUserFieldMixin):
    model = Event
    detail_serializer = DetailEventSerializer
