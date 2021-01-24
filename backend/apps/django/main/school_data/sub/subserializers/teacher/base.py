from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "BaseTeacherSerializer"
]


class BaseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
