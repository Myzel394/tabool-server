from pathlib import Path
from typing import *

from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import (
    AssociatedUserSerializerMixin, PreferredIdsMixin, PrivatizeSerializerMixin,
    RandomIDSerializerMixin,
)
from ...models import Submission

__all__ = [
    "SubmissionListSerializer", "SubmissionDetailSerializer"
]


class FilenameMixin(serializers.Serializer):
    filename = serializers.SerializerMethodField()
    
    def get_filename(self, instance: Submission):
        return Path(instance.file.path).name


class SubmissionListSerializer(RandomIDSerializerMixin, FilenameMixin, PreferredIdsMixin):
    preferred_id_key = "submission"
    
    class Meta:
        model = Submission
        fields = [
            "lesson", "filename", "upload_at", "id"
        ]
    
    lesson = LessonField()


class SubmissionDetailSerializer(
    PrivatizeSerializerMixin,
    AssociatedUserSerializerMixin,
    RandomIDSerializerMixin,
    FilenameMixin,
    PreferredIdsMixin
):
    preferred_id_key = "submission"
    
    class Meta:
        model = Submission
        fields = [
            "lesson", "file", "privatize", "filename", "upload_at", "is_uploaded", "id"
        ]
        read_only_fields = [
            "is_uploaded", "id"
        ]
    
    lesson = LessonField(detail=True)
    
    def get_file_to_privatize(self, instance: Submission, _) -> List[str]:
        return [instance.file.path]
