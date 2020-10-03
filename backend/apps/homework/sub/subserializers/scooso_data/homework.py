from rest_framework import serializers

from apps.lesson.public.serializer_fields import LessonField
from ....models import Homework

__all__ = [
    "HomeworkScoosoScraperSerializer"
]


class HomeworkScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "information", "due_date", "lesson"
        ]
    
    lesson = LessonField()
