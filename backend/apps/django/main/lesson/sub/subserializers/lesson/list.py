from rest_framework import serializers

from .base import BaseLessonSerializer
from ..lesson_data.detail import DetailLessonDataSerializer
from ....models import Lesson

__all__ = [
    "ListLessonSerializer"
]


class ListLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        model = Lesson
        fields = [
            "lesson_data", "date", "has_video_conference", "id"
        ]
    
    lesson_data = DetailLessonDataSerializer()
    
    has_video_conference = serializers.SerializerMethodField()
    
    @staticmethod
    def get_has_video_conference(instance: Lesson) -> str:
        return instance.video_conference_link is not None
