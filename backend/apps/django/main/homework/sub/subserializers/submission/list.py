from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseSubmissionSerializer
from .mixins import FilenameMixin
from ..mixins import SizeMixin

__all__ = [
    "ListSubmissionSerializer"
]


class ListSubmissionSerializer(BaseSubmissionSerializer, FilenameMixin, SizeMixin):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "filename", "size", "id"
        ]
    
    lesson = LessonField()
