from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Timetable

__all__ = [
    "TimetableField"
]


class TimetableField(WritableFromUserFieldMixin):
    model = Timetable
