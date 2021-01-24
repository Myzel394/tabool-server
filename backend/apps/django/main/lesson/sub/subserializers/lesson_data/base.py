from rest_framework import serializers

from ....models import LessonData

__all__ = [
    "BaseLessonDataSerializer"
]


class BaseLessonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonData
