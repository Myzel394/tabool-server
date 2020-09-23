from apps.subject.sub.subserializers import LessonDataDetailSerializer
from apps.timetable.models import Timetable
from apps.utils.serializers import RandomIDSerializerMixin

__all__ = [
    "TimetableDetailSerializer", "TimetableListSerializer"
]


class TimetableListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Timetable
        fields = ["designation", "id"]
        read_only_fields = ["id"]


class TimetableDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Timetable
        fields = ["lessons_data", "designation", "id"]
        read_only_fields = ["id"]
    
    lessons_data = LessonDataDetailSerializer(many=True)
