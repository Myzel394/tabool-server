from rest_framework import serializers

from ....models import Student

__all__ = [
    "BaseStudentSerializer"
]


class BaseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
