from rest_framework import serializers

from apps.django.main.homework.models import Material

__all__ = [
    "LessonMaterialSerializer"
]


class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "name", "added_at", "size", "id", "file", "is_deleted"
        ]
