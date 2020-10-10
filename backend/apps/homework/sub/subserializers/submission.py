from pathlib import Path

from rest_framework import serializers

from apps.lesson.public.serializer_fields import LessonField
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Submission

__all__ = [
    "SubmissionListSerializer", "SubmissionDetailSerializer"
]


class SubmissionListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Submission
        fields = [
            "lesson", "filename", "upload_at", "id"
        ]
    
    lesson = LessonField()
    filename = serializers.SerializerMethodField()
    
    def get_filename(self, instance: Submission):
        return Path(instance.file.path).name


class SubmissionDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Submission
        fields = [
            "lesson", "file", "upload_at", "is_uploaded", "id"
        ]
    
    lesson = LessonField()
