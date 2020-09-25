from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import RandomIDSerializerMixin
from .course import CourseDetailSerializer, CourseListSerializer
from .room import RoomDetailSerializer
from .teacher import TeacherDetailSerializer
from ...models import LessonData

__all__ = [
    "LessonDataListSerializer", "LessonDataDetailSerializer"
]


class LessonDataListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = LessonData
        fields = [
            "course", "start_time", "end_time", "weekday", "id"
        ]
    
    course = CourseListSerializer()


# TODO: News model hinzufügen!


class LessonDataDetailSerializer(
    RandomIDSerializerMixin,
    WritableNestedModelSerializer
):
    class Meta:
        model = LessonData
        fields = [
            "room", "course", "start_time", "end_time", "weekday", "id"
        ]
    
    room = RoomDetailSerializer()
    course = CourseDetailSerializer()
