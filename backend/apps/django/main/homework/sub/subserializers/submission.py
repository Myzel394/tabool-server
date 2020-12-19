from pathlib import Path
from typing import *

from rest_framework import serializers

from apps.django.utils.serializers import (
    AssociatedUserSerializerMixin, PreferredIdsMixin, PrivatizeSerializerMixin,
    RandomIDSerializerMixin,
)
from ...models import Submission

__all__ = [
    "SubmissionDetailSerializer", "SizeMixin", "FilenameMixin"
]


class FilenameMixin(serializers.Serializer):
    filename = serializers.SerializerMethodField()
    
    def get_filename(self, instance: Submission):
        return Path(instance.file.path).name


class SizeMixin(serializers.Serializer):
    size = serializers.SerializerMethodField()
    
    def get_size(self, instance: Submission):
        return instance.file.size


class SubmissionDetailSerializer(
    PrivatizeSerializerMixin,
    AssociatedUserSerializerMixin,
    RandomIDSerializerMixin,
    FilenameMixin,
    PreferredIdsMixin,
    SizeMixin
):
    preferred_id_key = "submission"
    
    class Meta:
        model = Submission
        fields = [
            "file", "privatize", "filename", "upload_date", "created_at", "is_uploaded", "size", "id"
        ]
        read_only_fields = [
            "is_uploaded", "id", "filename"
        ]
    
    def get_file_to_privatize(self, instance: Submission, _) -> List[str]:
        return [instance.file.path]
