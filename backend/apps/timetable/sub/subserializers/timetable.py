from apps.subject.sub.subserializers import LessonDataDetailSerializer
from apps.timetable.models import TimeTable
from apps.utils.serializers import RandomIDSerializerMixin

__all__ = [
    "TimeTableDetailSerializer", "TimeTableListSerializer"
]


class TimeTableListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = TimeTable
        fields = ["designation", "id"]


class TimeTableDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = TimeTable
        fields = ["lessons_data", "designation", "id"]
    
    lessons_data = LessonDataDetailSerializer(many=True)
