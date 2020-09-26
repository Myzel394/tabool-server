from apps.utils.serializers import WritableFromUserFieldMixin
from ..models import Timetable


class TimetableField(WritableFromUserFieldMixin):
    model = Timetable
