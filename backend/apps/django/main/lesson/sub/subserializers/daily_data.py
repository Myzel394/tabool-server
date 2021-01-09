from datetime import date

from rest_framework import serializers

__all__ = [
    "DailyDataSerializer"
]


class DailyDataSerializer(serializers.Serializer):
    date = serializers.DateField(default=lambda: date.today())
    max_future_days = serializers.IntegerField(min_value=0, max_value=30, default=5)
