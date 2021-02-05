from rest_framework import serializers

from ....models import Homework

__all__ = [
    "BaseHomeworkSerializer"
]


class BaseHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
