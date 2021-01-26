import os

from rest_framework import serializers

from apps.django.main.homework.models import Submission
from apps.django.main.homework.sub.subserializers.mixins import SizeMixin

__all__ = [
    "LessonSubmissionSerializer"
]


class LessonSubmissionSerializer(serializers.ModelSerializer, SizeMixin):
    class Meta:
        model = Submission
        fields = [
            "file", "filename", "upload_date", "created_at", "is_uploaded", "size", "id"
        ]
    
    filename = serializers.SerializerMethodField()
    
    @staticmethod
    def get_filename(instance: Submission):
        return os.path.basename(instance.file.path)
