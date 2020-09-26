from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import Classtest, Event

__all__ = [
    "EventField", "ClasstestField",
]


class EventField(WritableFromUserFieldMixin):
    model = Event


class ClasstestField(WritableFromUserFieldMixin):
    model = Classtest
