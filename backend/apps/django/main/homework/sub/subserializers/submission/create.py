from rest_framework import serializers

from apps.django.main.homework.validators import only_future
from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseSubmissionSerializer

__all__ = [
    "CreateSubmissionSerializer"
]


class CreateSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name"
        ]

    lesson = LessonField()

    publish_datetime = serializers.DateTimeField(
        required=False,
        allow_null=True,
        validators=[only_future]
    )

    # TODO: Add tests!
    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student

        return super().create(validated_data)
