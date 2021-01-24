from rest_framework import serializers

from apps.django.main.homework.models import Material
from apps.django.main.homework.sub.subserializers.mixins import SizeMixin

__all__ = [
    "LessonMaterialSerializer"
]


class LessonMaterialSerializer(serializers.ModelSerializer, SizeMixin):
    class Meta:
        model = Material
        fields = [
            "name", "added_at", "size", "id", "file", "is_deleted"
        ]
