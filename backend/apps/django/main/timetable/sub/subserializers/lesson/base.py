from rest_framework import serializers

from ....models import Lesson

__all__ = [
    "BaseLessonSerializer"
]


class BaseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
