from rest_framework import serializers

from ...utils import get_date

__all__ = [
    "DailyDataViewSerializer"
]


class DailyDataViewSerializer(serializers.Serializer):
    date = serializers.DateField(default=get_date)
    max_future_days = serializers.IntegerField(min_value=0, max_value=30, default=5)
