from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseSubmissionSerializer
from .mixins import FilenameMixin
from ..mixins import SizeMixin

__all__ = [
    "DetailSubmissionSerializer"
]


class DetailSubmissionSerializer(BaseSubmissionSerializer, SizeMixin, FilenameMixin):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "file", "filename", "upload_date", "created_at", "is_uploaded", "size", "id", "lesson"
        ]
    
    lesson = LessonField(detail=True)
