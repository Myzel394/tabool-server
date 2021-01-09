from datetime import date, timedelta

from rest_framework import serializers

__all__ = [
    "DailyDataSerializer"
]


def get_date():
    today = date.today()
    weekday = today.weekday()
    
    if weekday >= 5:
        today += timedelta(days=7 - weekday)
    
    return today


class DailyDataSerializer(serializers.Serializer):
    date = serializers.DateField(default=get_date)
    max_future_days = serializers.IntegerField(min_value=0, max_value=30, default=5)
