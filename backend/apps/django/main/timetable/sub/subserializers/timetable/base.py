from rest_framework import serializers

from ....models import Timetable

__all__ = [
    "BaseTimetableSerializer"
]


class BaseTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
