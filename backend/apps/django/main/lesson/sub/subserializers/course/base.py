from rest_framework import serializers

from ....models import Course

__all__ = [
    "BaseCourseSerializer"
]


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
