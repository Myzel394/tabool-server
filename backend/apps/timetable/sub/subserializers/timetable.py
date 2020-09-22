from apps.subject.sub.subserializers import LessonDataSerializer
from apps.timetable.models import TimeTable
from apps.utils.serializers import IdMixinSerializer

__all__ = [
    "TimeTableSerializer"
]


class TimeTableSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["lessons_data", "designation", "id"]
    
    lessons_data = LessonDataSerializer(many=True)
