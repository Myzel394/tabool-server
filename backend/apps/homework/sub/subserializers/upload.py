from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.lesson.public.serializer_fields import LessonField
from apps.utils.serializers import PrivatizeSerializerMixin

__all__ = [
    "UploadSerializer"
]


class UploadSerializer(serializers.Serializer, PrivatizeSerializerMixin):
    lesson = LessonField()
    file = serializers.FileField(label=_("Datei"))
