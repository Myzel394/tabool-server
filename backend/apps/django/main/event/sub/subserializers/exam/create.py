from apps.django.main.course.public.serializer_fields.course import CourseField
from .base import BaseExamSerializer

__all__ = [
    "CreateExamSerializer"
]


class CreateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "date", "title", "information"
        ]
    
    course = CourseField()
