from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import ClassTest, Event

__all__ = [
    "EventField", "ClassTestField",
]


class EventField(WritableFromUserFieldMixin):
    model = Event


class ClassTestField(WritableFromUserFieldMixin):
    model = ClassTest
