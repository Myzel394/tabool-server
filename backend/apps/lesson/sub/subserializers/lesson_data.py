from apps.utils.serializers import RandomIDSerializerMixin
from ...models import LessonData
from ...public.serializer_fields import CourseField, RoomField

__all__ = [
    "LessonDataListSerializer", "LessonDataDetailSerializer"
]


class LessonDataListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = LessonData
        fields = [
            "course", "start_time", "end_time", "weekday", "id"
        ]
    
    course = CourseField()


# TODO: News model hinzufügen!


class LessonDataDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = LessonData
        fields = [
            "room", "course", "start_time", "end_time", "weekday", "id"
        ]
    
    room = RoomField()
    course = CourseField()
