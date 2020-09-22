from apps.subject.sub.subserializers import LessonDataDetailSerializer
from apps.timetable.models import TimeTable
from apps.utils.serializers import IdMixinSerializer

__all__ = [
    "TimeTableDetailSerializer", "TimeTableListSerializer"
]


class TimeTableListSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["designation", "id"]


class TimeTableDetailSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["lessons_data", "designation", "id"]
    
    lessons_data = LessonDataDetailSerializer(many=True)
