from pathlib import Path
from typing import *

from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields import LessonField
from apps.django.utils.serializers import (
    AssociatedUserSerializerMixin, PrivatizeSerializerMixin,
    RandomIDSerializerMixin,
)
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


class SubmissionDetailSerializer(
    PrivatizeSerializerMixin,
    AssociatedUserSerializerMixin,
    RandomIDSerializerMixin,
):
    class Meta:
        model = Submission
        fields = [
            "lesson", "file", "privatize", "upload_at", "is_uploaded", "id"
        ]
        read_only_fields = [
            "is_uploaded", "id"
        ]
    
    lesson = LessonField()
    
    def get_file_to_privatize(self, instance: Submission, _) -> List[str]:
        return [instance.file.path]
