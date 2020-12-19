from rest_framework import serializers

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
            "room", "course", "start_time", "end_time", "weekday", "weekdays", "id"
        ]
    
    weekdays = serializers.SerializerMethodField()
    room = RoomField(required=False, detail=True)
    course = CourseField(detail=True)
    
    def get_weekdays(self, instance: LessonData):
        return list(set(
            LessonData.objects
                .only("course")
                .filter(course=instance.course)
                .values_list("weekday", flat=True)
        ))
