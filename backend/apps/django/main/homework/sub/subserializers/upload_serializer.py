from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField

__all__ = [
    "UploadSerializer"
]


class UploadSerializer(serializers.Serializer):
    lesson = LessonField()
    file = serializers.FileField(label=_("Datei"))
