from apps.lesson.models import LessonData
from apps.lesson.public.serializer_fields import CourseField, RoomField
from apps.timetable.models import Timetable
from apps.utils.serializers import RandomIDSerializerMixin

__all__ = [
    "TimetableDetailSerializer", "TimetableListSerializer"
]


class TimetableLessonDataSerializer(RandomIDSerializerMixin):
    class Meta:
        model = LessonData
        fields = [
            "room", "course", "start_time", "weekday", "id"
        ]
    
    room = RoomField()
    course = CourseField()


class TimetableListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Timetable
        fields = ["designation", "id"]


class TimetableDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Timetable
        fields = ["lessons_data", "designation", "id"]
    
    lessons_data = TimetableLessonDataSerializer(many=True)
