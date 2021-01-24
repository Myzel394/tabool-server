from rest_framework import serializers

from ....models import Exam

__all__ = [
    "BaseExamSerializer"
]


class BaseExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
