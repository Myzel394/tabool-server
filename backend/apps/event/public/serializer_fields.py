from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import ClassTest, Event

__all__ = [
    "EventField", "ClassTestField",
]


class EventField(WritableFromUserFieldMixin):
    model = Event
    # TODO: Add from_user to event's qs!


class ClassTestField(WritableFromUserFieldMixin):
    model = ClassTest
