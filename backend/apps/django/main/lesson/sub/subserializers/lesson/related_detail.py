from rest_framework import serializers

from ..classbook import ClassbookSerializer
from ..lesson_data.detail import DetailLessonDataSerializer
from ....models import Lesson

__all__ = [
    "RelatedDetailLessonSerializer"
]


class RelatedDetailLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "classbook", "video_conference_link"
        ]
    
    lesson_data = DetailLessonDataSerializer()
    classbook = ClassbookSerializer()
