from rest_framework import serializers

from .base import BaseLessonSerializer
from ....models import Lesson
from ....public.serializer_fields.course import CourseField

__all__ = [
    "ListLessonSerializer"
]


class ListLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        model = Lesson
        fields = [
            "course", "start_time", "end_time",
            "date", "has_video_conference", "id"
        ]
    
    course = CourseField()
    
    has_video_conference = serializers.SerializerMethodField()
    
    @staticmethod
    def get_has_video_conference(instance: Lesson) -> str:
        return instance.video_conference_link is not None
