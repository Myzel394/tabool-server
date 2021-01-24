from rest_framework import serializers

from apps.django.main.homework.models import Submission

__all__ = [
    "LessonSubmissionSerializer"
]


class LessonSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "file", "filename", "upload_date", "created_at", "is_uploaded", "size", "id"
        ]
