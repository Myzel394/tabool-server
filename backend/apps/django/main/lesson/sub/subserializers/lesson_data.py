from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import LessonData
from ...public.serializer_fields.course import CourseField

__all__ = [
    "LessonDataListSerializer", "LessonDataDetailSerializer"
]


class LessonDataListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson_data"
    
    class Meta:
        model = LessonData
        fields = [
            "course", "start_time", "end_time", "weekday", "id"
        ]
    
    course = CourseField()


class LessonDataDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson_data"
    
    class Meta:
        model = LessonData
        fields = [
            "room", "course", "start_time", "end_time", "weekday", "id"
        ]
    
    room = RoomField(required=False, detail=True)
    course = CourseField(detail=True)
